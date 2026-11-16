<?php
/**
 * nadlan-config - the developer deals map at the top of /developer-deals/ (HAD-743, Ben 15.11.2026: "בלי מתגים, תעלה").
 * Design: Claude Design canvas https://claude.ai/artifact/Rg8mHtQitrYSGF9McF1Bus (docs/design-lab/deals-map/).
 * Every deal carries the wording as published, the month it was published, its source and whether we confirmed it is still
 * offered; a deal that ended is kept in the archive, never on the map. Locations are approximate (city or neighbourhood).
 * Grey dots: our 1,003 project points (assets/deals/projects.json). JS: assets/deals/deals.js, CSS: assets/deals/deals.css.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_dm_deals' ) ) {
	/** The deals. k: pay | rent | loan | price | gift. first: share paid at signing; firstAbs: a sum; worth: published value in ILS. */
	function nadlan_dm_deals() {
		return array(
			array( 'id' => 'gindi-love', 'dev' => 'גינדי', 'devFull' => 'גינדי החזקות', 'project' => 'LOVE גליל ים, הרצליה', 'city' => 'הרצליה', 'lat' => 32.1570, 'lng' => 34.8120, 'color' => '#14161A', 'k' => 'pay', 'kind' => 'המפץ הגדול: 20/50/30', 'short' => 'הלוואה ל-10 שנים', 'terms' => '20% בחתימה ו-50% במסירה, לפי הפרסומים. את היתרה הקונה לוקח כהלוואת קרדיט ומחזיר בתום 10 שנים מהאכלוס, והחברה נושאת בריבית ובהצמדה של ההלוואה, בכפוף לתנאי המבצע ולאישור הבנק. המחיר המוצג, מ-4.2 מיליון ₪, אינו כולל את סכום ההלוואה.', 'first' => 0.20, 'bar' => array( array( 20, 'חתימה', 'a' ), array( 50, 'במסירה', 'b' ), array( 30, 'הלוואה, 10 שנים אחרי', 'c' ) ), 'pub' => 'נובמבר 2026', 'checked' => '15.11.2026', 'src' => 'https://mapatz.gindih.co.il/' , 'hot' => true ),
			array( 'id' => 'gindi-efal', 'dev' => 'גינדי', 'devFull' => 'גינדי החזקות', 'project' => 'רמת אפעל, רמת גן', 'city' => 'רמת גן', 'lat' => 32.0450, 'lng' => 34.8350, 'color' => '#14161A', 'k' => 'pay', 'kind' => 'המפץ הגדול: 20/50/30', 'short' => 'הלוואה ל-10 שנים', 'terms' => '20% בחתימה ו-50% במסירה, לפי הפרסומים. את היתרה הקונה לוקח כהלוואת קרדיט ומחזיר בתום 10 שנים מהאכלוס, והחברה נושאת בריבית ובהצמדה של ההלוואה, בכפוף לתנאי המבצע ולאישור הבנק. המחיר המוצג, מ-3.3 מיליון ₪, אינו כולל את סכום ההלוואה.', 'first' => 0.20, 'bar' => array( array( 20, 'חתימה', 'a' ), array( 50, 'במסירה', 'b' ), array( 30, 'הלוואה, 10 שנים אחרי', 'c' ) ), 'pub' => 'נובמבר 2026', 'checked' => '15.11.2026', 'src' => 'https://mapatz.gindih.co.il/'  ),
			array( 'id' => 'gindi-azar', 'dev' => 'גינדי', 'devFull' => 'גינדי החזקות', 'project' => 'כפר אז"ר', 'city' => 'כפר אז"ר', 'lat' => 32.0620, 'lng' => 34.8580, 'color' => '#14161A', 'k' => 'pay', 'kind' => 'המפץ הגדול: 20/50/30', 'short' => 'הלוואה ל-8 שנים', 'terms' => '20% בחתימה ו-50% במסירה, לפי הפרסומים. את היתרה הקונה לוקח כהלוואת קרדיט ומחזיר בתום 8 שנים מהאכלוס, והחברה נושאת בריבית ובהצמדה של ההלוואה, בכפוף לתנאי המבצע ולאישור הבנק. המחיר המוצג, מ-2.7 מיליון ₪, אינו כולל את סכום ההלוואה.', 'first' => 0.20, 'bar' => array( array( 20, 'חתימה', 'a' ), array( 50, 'במסירה', 'b' ), array( 30, 'הלוואה, 8 שנים אחרי', 'c' ) ), 'pub' => 'נובמבר 2026', 'checked' => '15.11.2026', 'src' => 'https://mapatz.gindih.co.il/'  ),
			array( 'id' => 'gindi-ayalon', 'dev' => 'גינדי', 'devFull' => 'גינדי החזקות', 'project' => 'נווה איילון', 'city' => 'אור יהודה', 'lat' => 32.0300, 'lng' => 34.8550, 'color' => '#14161A', 'k' => 'pay', 'kind' => 'המפץ הגדול: 20/50/30', 'short' => 'הלוואה ל-10 שנים', 'terms' => '20% בחתימה ו-50% במסירה, לפי הפרסומים. את היתרה הקונה לוקח כהלוואת קרדיט ומחזיר בתום 10 שנים מהאכלוס, והחברה נושאת בריבית ובהצמדה של ההלוואה, בכפוף לתנאי המבצע ולאישור הבנק. המחיר המוצג, מ-2.1 מיליון ₪, אינו כולל את סכום ההלוואה.', 'first' => 0.20, 'bar' => array( array( 20, 'חתימה', 'a' ), array( 50, 'במסירה', 'b' ), array( 30, 'הלוואה, 10 שנים אחרי', 'c' ) ), 'pub' => 'נובמבר 2026', 'checked' => '15.11.2026', 'src' => 'https://mapatz.gindih.co.il/'  ),
			array( 'id' => 'melisron', 'pid' => 8744, 'dev' => 'אביב מליסרון', 'devFull' => 'אביב מליסרון', 'project' => 'שמונה פרויקטים, ובהם אביב ברדינג', 'city' => 'תל אביב, גבעתיים, רמת גן, נתניה, הרצליה', 'lat' => 32.1160, 'lng' => 34.8070, 'color' => '#0F7B6C', 'k' => 'loan', 'kind' => '0% הון עצמי עד האכלוס', 'short' => '0% הון עצמי', 'terms' => '0% הון עצמי בכניסה לדירה: הלוואה כנגד שעבוד נכס קיים, גם של ההורים, והחברה נושאת בעלויות המימון והריבית עד האכלוס. בתוקף בנובמבר ובדצמבר 2026.', 'first' => 0, 'bar' => array( array( 3, '', 'a' ), array( 97, 'באכלוס', 'c' ) ), 'pub' => 'נובמבר 2026', 'checked' => '', 'src' => 'https://www.bizportal.co.il/realestates/news/article/20046907' ),
			array( 'id' => 'upview', 'dev' => 'אהרוני', 'devFull' => 'קבוצת אהרוני', 'project' => 'UPVIEW, נופי בן שמן, לוד', 'city' => 'לוד', 'lat' => 31.9570, 'lng' => 34.9100, 'color' => '#8C4A1D', 'k' => 'pay', 'kind' => '0% הון עצמי עד המסירה', 'short' => '0% עד המסירה', 'terms' => '0% הון עצמי עד המסירה, במגדל ובבנייני הבוטיק. בתוקף עד סוף 2026. מ-2.15 מיליון ₪.', 'price' => 2150000, 'first' => 0, 'bar' => array( array( 3, '', 'a' ), array( 97, 'במסירה', 'c' ) ), 'pub' => 'נובמבר 2026', 'checked' => '', 'src' => 'https://www.maariv.co.il/economy/realestate/article-1384354' ),
			array( 'id' => 'infinity', 'pid' => 6548, 'dev' => 'חג\'ג\'', 'devFull' => 'קבוצת חג\'ג\'', 'project' => 'H Infinity, מתחם סומייל, תל אביב', 'city' => 'תל אביב', 'lat' => 32.0873, 'lng' => 34.7827, 'color' => '#5A2A82', 'k' => 'pay', 'kind' => 'מיליון בחתימה ומפתח', 'short' => 'מיליון ומפתח', 'terms' => 'משלמים מיליון ₪ בחתימה ומקבלים מפתח. היתרה כשלוש שנים אחרי האכלוס, ללא ריבית וללא הצמדה, ושכירות מינימלית מובטחת ל-24 חודשים (10,000 ₪ לדירת 2 חדרים).', 'firstAbs' => 1000000, 'bar' => array( array( 24, 'מיליון בחתימה', 'a' ), array( 76, 'כ-3 שנים אחרי האכלוס', 'c' ) ), 'pub' => 'אוגוסט 2026, עדיין מופיע בנובמבר', 'checked' => '', 'src' => 'https://www.ice.co.il/realestate/news/article/1136624', 'link' => '/projects/h-infinity-somail-tel-aviv/' ),
			array( 'id' => 'ytown', 'dev' => 'צרפתי', 'devFull' => 'צרפתי צבי ובניו', 'project' => 'Y TOWN, ז\'בוטינסקי 42, ראשון לציון', 'city' => 'ראשון לציון', 'lat' => 31.9900, 'lng' => 34.7800, 'color' => '#00897B', 'k' => 'rent', 'kind' => 'הטבה חודשית עד האכלוס', 'short' => 'עד 7,000 ₪ לחודש', 'terms' => 'הטבה של עד 7,000 ₪ בחודש לכ-4 שנים, עד האכלוס. דירות 3 ו-4 חדרים מכ-2.88 מיליון ₪.', 'price' => 2880000, 'worth' => 336000, 'bar' => array( array( 100, 'לפי לוח התשלומים', 'c' ) ), 'pub' => 'יולי 2026', 'checked' => '', 'src' => 'https://www.yad2.co.il/yad1/project/12463', 'calcOk' => true, 'calc' => array( 'T' => 48, 'R' => 7000, 'M' => 48, 'same' => true ) ),
			array( 'id' => 'benshemen', 'dev' => 'אאורה', 'devFull' => 'אאורה ישראל', 'project' => 'נופי בן שמן, לוד', 'city' => 'לוד', 'lat' => 31.9520, 'lng' => 34.9010, 'color' => '#0B63B6', 'k' => 'pay', 'kind' => 'כניסה עם סכום קטן', 'short' => '550 אלף בכניסה', 'terms' => 'רק 550,000 ₪ נכנסים לדירה, והיתרה בעוד שנה וחצי. דירות 4 עד 6 חדרים מ-2.68 מיליון ₪.', 'price' => 2680000, 'firstAbs' => 550000, 'bar' => array( array( 21, 'כניסה', 'a' ), array( 79, 'אחרי שנה וחצי', 'c' ) ), 'pub' => '2026', 'checked' => '', 'src' => 'https://www.yad2.co.il/yad1/project/10032', 'calcOk' => true, 'calc' => array( 'T' => 18 ) ),
			array( 'id' => 'noga', 'dev' => 'בראל', 'devFull' => 'קבוצת בראל', 'project' => 'נגה, נוף הגליל', 'city' => 'נוף הגליל', 'lat' => 32.7150, 'lng' => 35.3300, 'color' => '#2E5BFF', 'k' => 'pay', 'kind' => '11/89 והלוואת קבלן', 'short' => '11/89', 'terms' => 'מסלול 11/89 והלוואת קבלן בגובה 50% ממחיר הדירה, שהיזם נושא במימון שלה, והנחה של 8% עד 10% ממחיר המחירון. 3 חדרים מ-1.36 מיליון ₪.', 'price' => 1360000, 'first' => 0.11, 'bar' => array( array( 11, 'חוזה', 'a' ), array( 50, 'הלוואת קבלן', 'b' ), array( 39, 'באכלוס', 'c' ) ), 'pub' => 'יולי 2026', 'checked' => '', 'src' => 'https://www.bizportal.co.il/realestates/news/article/20036395', 'calcOk' => true, 'calc' => array( 'T' => 30 ) ),
			array( 'id' => 'biltmore', 'dev' => 'י.ע.ז', 'devFull' => 'י.ע.ז', 'project' => 'Biltmore 16, כיכר המדינה, תל אביב', 'city' => 'תל אביב', 'lat' => 32.0870, 'lng' => 34.7890, 'color' => '#8A1C5C', 'k' => 'pay', 'kind' => '0% בחתימה', 'short' => '0% בחתימה', 'terms' => 'מבצע 0% בחתימה. 5 חדרים מ-7.65 מיליון ₪, בבניין בוטיק בן 7 קומות.', 'price' => 7650000, 'first' => 0, 'bar' => array( array( 3, '', 'a' ), array( 97, 'לפי לוח התשלומים', 'c' ) ), 'pub' => '2026', 'checked' => '', 'src' => 'https://www.yad2.co.il/yad1/project/tel-aviv-area/19126/apartment/1013357' ),
			array( 'id' => 'east', 'dev' => 'EAST&TLV', 'devFull' => 'EAST&TLV (סופרין ורבוע כחול נדל"ן)', 'project' => 'EAST&TLV, תל אביב', 'city' => 'תל אביב', 'lat' => 32.0690, 'lng' => 34.8060, 'color' => '#5B3FA8', 'k' => 'pay', 'kind' => '50/50', 'short' => '50/50', 'terms' => '50% מהמחיר עכשיו והיתרה בעוד שנתיים, עם בחירת מסלול תשלום, עיצוב הדירה ומועד הכניסה.', 'bar' => array( array( 50, 'עכשיו', 'a' ), array( 50, 'בעוד שנתיים', 'c' ) ), 'pub' => 'נובמבר 2026', 'checked' => '', 'src' => 'https://www.ice.co.il/realestate/news/article/1136624' ),
			array( 'id' => 'kata', 'dev' => 'קטה', 'devFull' => 'קטה גרופ', 'project' => 'TRIO, עין גנים, פתח תקווה', 'city' => 'פתח תקווה', 'lat' => 32.0780, 'lng' => 34.8940, 'color' => '#2F6F2A', 'k' => 'gift', 'kind' => 'שלוש שנים בלי דמי ניהול', 'short' => 'דמי ניהול חינם', 'terms' => 'שלוש שנים ללא דמי ניהול, בשווי של כ-25 אלף ₪ לדירה. 4 ו-5 חדרים מ-2.71 מיליון ₪.', 'price' => 2710000, 'worth' => 25000, 'bar' => array( array( 100, 'לפי לוח התשלומים', 'c' ) ), 'pub' => 'נובמבר 2026', 'checked' => '', 'src' => 'https://www.ice.co.il/realestate/news/article/1136624', 'calcOk' => true, 'calc' => array( 'cut' => 25000, 'same' => true ) ),
			array( 'id' => 'sharet', 'dev' => 'אשד ורוטשטיין', 'devFull' => 'אשד ורוטשטיין נדל"ן', 'project' => 'שרת 38, תל אביב', 'city' => 'תל אביב', 'lat' => 32.0990, 'lng' => 34.7890, 'color' => '#1D3F8F', 'k' => 'gift', 'kind' => 'דירה מרוהטת ומעוצבת', 'short' => 'מרוהטת', 'terms' => 'דירת 4 חדרים, 102 מ"ר, מרוהטת ומעוצבת במלואה, עם מרפסת, ממ"ד וחניה. 6.66 מיליון ₪.', 'price' => 6660000, 'bar' => array( array( 100, 'לפי לוח התשלומים', 'c' ) ), 'pub' => '2026', 'checked' => '', 'src' => 'https://www.yad2.co.il/yad1/project/tel-aviv-area/11172/apartment/1002059' ),
			array( 'id' => 'rayk', 'dev' => 'RAYK', 'devFull' => 'RAYK נדל"ן', 'project' => 'RAYK לוד החדשה, אנה פרנק 2', 'city' => 'לוד', 'lat' => 31.9480, 'lng' => 34.8880, 'color' => '#6D4C41', 'k' => 'pay', 'kind' => '215 אלף והיתרה באכלוס', 'short' => '215 אלף ביד', 'terms' => 'בדירת 4 חדרים: 215,000 ₪ והיתרה באכלוס, בכפוף להלוואת קבלן מסובסדת, והטבות מיוחדות ללוחמים. 3 חדרים מ-1.95 מיליון, 4 חדרים 2.15 מיליון ₪. אכלוס צפוי ביוני 2029.', 'price' => 2150000, 'firstAbs' => 215000, 'bar' => array( array( 10, '', 'a' ), array( 90, 'באכלוס', 'c' ) ), 'pub' => '2026', 'checked' => '', 'src' => 'https://www.yad2.co.il/yad1/project/19174', 'calcOk' => true, 'calc' => array( 'T' => 31 ) ),
			array( 'id' => 'tzahala', 'dev' => 'דנקנר', 'devFull' => 'דנקנר קנלוב', 'project' => 'רמות צהלה, טולקובסקי 12, תל אביב', 'city' => 'תל אביב', 'lat' => 32.1170, 'lng' => 34.8330, 'color' => '#B4541A', 'k' => 'price', 'kind' => 'מחיר פריסייל', 'short' => 'מחיר פריסייל', 'terms' => 'דירת 6 חדרים אחרונה במחיר פריסייל: 7.65 מיליון ₪.', 'price' => 7650000, 'bar' => array( array( 100, 'לפי לוח התשלומים', 'c' ) ), 'pub' => '2026', 'checked' => '', 'src' => 'https://www.madlan.co.il/projects/%D7%98%D7%95%D7%9C%D7%A7%D7%95%D7%91%D7%A1%D7%A7%D7%99_12_%D7%AA%D7%9C_%D7%90%D7%91%D7%99%D7%91' ),
			array( 'id' => 'isa', 'dev' => 'ISA', 'devFull' => 'קבוצת ISA, שיווק מאגמה', 'project' => 'מבשרת ציון', 'city' => 'מבשרת ציון', 'lat' => 31.8000, 'lng' => 35.1500, 'color' => '#3E5C76', 'k' => 'rent', 'kind' => 'שכירות שהופכת לקנייה', 'short' => 'Rent-to-Own', 'terms' => 'שוכרים דירה גמורה, וחלק משכר הדירה, ולעיתים כולו, נזקף כהון עצמי אם רוכשים בתום התקופה. לא פורסם מחיר.', 'bar' => array( array( 100, 'שכירות עם אופציה', 'c' ) ), 'pub' => 'יולי 2026', 'checked' => '', 'src' => 'https://www.mako.co.il/news-money/2026_q3/Article-8946b308def5f91026.htm' ),
		);
	}
}

if ( ! function_exists( 'nadlan_dm_archive' ) ) {
	function nadlan_dm_archive() {
		return array(
			array( 'גינדי, גליל ים', 'שכר דירה ל-3 שנים, 10% הון ו-30% הלוואת קבלן', 'הוחלף בנובמבר 2026 במבצע "המפץ הגדול"' ),
			array( 'אאורה וחבר, רמת השרון, חדרה, קריית אונו', '15/85 ופטור מהצמדה', 'ימי המכירה היו 24 עד 28.8.2026' ),
			array( 'אביב מליסרון', 'ריבית 0.99% על עד 30% מהמחיר', 'תקנון המבצע היה עד 31.5.2026' ),
			array( 'פרשקובסקי, שישה פרויקטים', 'מכרז הצעות חסויות', 'המכרז נסגר באוגוסט 2026' ),
			array( 'גינדי VOGUE, שדה דב', 'מחיר פתיחה של 49 אלף ₪ למ"ר', 'מבצע 2025' ),
		);
	}
}

if ( ! function_exists( 'nadlan_dm_en' ) ) {
	/** English wording of every deal (from the same verified Hebrew terms; nothing added). id => fields that replace the Hebrew ones. */
	function nadlan_dm_en() {
		$g = function ( $project, $city, $years, $from ) {
			return array( 'dev' => 'Gindi', 'devFull' => 'Gindi Holdings', 'project' => $project, 'city' => $city, 'kind' => '"Big Bang": 20/50/30', 'short' => 'loan, ' . $years . ' yrs',
				'terms' => '20% at signing and 50% at handover, as published. The buyer takes the rest as a credit loan and repays it ' . $years . ' years after occupancy; the company carries the loan\'s interest and indexation, subject to the campaign terms and the bank\'s approval. The displayed price, from ' . $from . ', does not include the loan amount.',
				'bar' => array( 'signing', 'handover', 'loan, ' . $years . ' yrs later' ), 'pub' => 'November 2026' );
		};
		return array(
			'gindi-love'   => $g( 'LOVE Glil Yam, Herzliya', 'Herzliya', 10, '₪4.2M' ),
			'gindi-efal'   => $g( 'Ramat Efal, Ramat Gan', 'Ramat Gan', 10, '₪3.3M' ),
			'gindi-azar'   => $g( 'Kfar Azar', 'Kfar Azar', 8, '₪2.7M' ),
			'gindi-ayalon' => $g( 'Neve Ayalon', 'Or Yehuda', 10, '₪2.1M' ),
			'melisron'  => array( 'dev' => 'Aviv Melisron', 'devFull' => 'Aviv Melisron', 'project' => 'Eight projects, including Aviv Reading', 'city' => 'Tel Aviv, Givatayim, Ramat Gan, Netanya, Herzliya', 'kind' => '0% equity until occupancy', 'short' => '0% equity', 'terms' => '0% equity when you buy: a loan secured on an existing property (parents\' too), and the company carries the financing and interest until occupancy. Valid in November and December 2026.', 'bar' => array( '', 'at occupancy' ), 'pub' => 'November 2026' ),
			'upview'    => array( 'dev' => 'Aharoni', 'devFull' => 'Aharoni Group', 'project' => 'UPVIEW, Nofei Ben Shemen, Lod', 'city' => 'Lod', 'kind' => '0% equity until handover', 'short' => '0% until handover', 'terms' => '0% equity until handover, in the tower and the boutique buildings. Valid until the end of 2026. From ₪2.15M.', 'bar' => array( '', 'at handover' ), 'pub' => 'November 2026' ),
			'infinity'  => array( 'dev' => 'Hagag', 'devFull' => 'Hagag Group', 'project' => 'H Infinity, Somail compound, Tel Aviv', 'city' => 'Tel Aviv', 'kind' => '₪1M and the keys', 'short' => '₪1M and keys', 'terms' => 'Pay ₪1M at signing and get the keys. The balance about three years after occupancy, without interest or indexation, with a guaranteed minimum rent for 24 months (₪10,000 for a 2-room apartment).', 'bar' => array( '₪1M at signing', '~3 yrs after occupancy' ), 'pub' => 'August 2026, still listed in November' ),
			'ytown'     => array( 'dev' => 'Tzarfati', 'devFull' => 'Tzarfati Tzvi & Sons', 'project' => 'Y TOWN, 42 Jabotinsky, Rishon LeZion', 'city' => 'Rishon LeZion', 'kind' => 'Monthly benefit until occupancy', 'short' => 'up to ₪7,000/mo', 'terms' => 'A benefit of up to ₪7,000 a month for about 4 years, until occupancy. 3 and 4-room apartments from about ₪2.88M.', 'bar' => array( 'regular payment plan' ), 'pub' => 'July 2026' ),
			'benshemen' => array( 'dev' => 'Aura', 'devFull' => 'Aura Israel', 'project' => 'Nofei Ben Shemen, Lod', 'city' => 'Lod', 'kind' => 'Move in with a small sum', 'short' => '₪550K in', 'terms' => 'Only ₪550,000 to get in, the balance in a year and a half. 4 to 6-room apartments from ₪2.68M.', 'bar' => array( 'entry', 'after 18 months' ), 'pub' => '2026' ),
			'noga'      => array( 'dev' => 'Barel', 'devFull' => 'Barel Group', 'project' => 'Noga, Nof HaGalil', 'city' => 'Nof HaGalil', 'kind' => '11/89 and a developer loan', 'short' => '11/89', 'terms' => 'An 11/89 payment plan and a developer loan of 50% of the price, financed by the developer, and 8% to 10% off the list price. 3 rooms from ₪1.36M.', 'bar' => array( 'contract', 'developer loan', 'at occupancy' ), 'pub' => 'July 2026' ),
			'biltmore'  => array( 'dev' => 'Y.A.Z', 'devFull' => 'Y.A.Z', 'project' => 'Biltmore 16, Kikar HaMedina, Tel Aviv', 'city' => 'Tel Aviv', 'kind' => '0% at signing', 'short' => '0% at signing', 'terms' => '0% at signing. 5 rooms from ₪7.65M, in a 7-floor boutique building.', 'bar' => array( '', 'regular payment plan' ), 'pub' => '2026' ),
			'east'      => array( 'dev' => 'EAST&TLV', 'devFull' => 'EAST&TLV (Sufrin and Blue Square Real Estate)', 'project' => 'EAST&TLV, Tel Aviv', 'city' => 'Tel Aviv', 'kind' => '50/50', 'short' => '50/50', 'terms' => '50% of the price now and the rest in two years, with a choice of payment plan, apartment design and move-in date.', 'bar' => array( 'now', 'in two years' ), 'pub' => 'November 2026' ),
			'kata'      => array( 'dev' => 'Kata', 'devFull' => 'Kata Group', 'project' => 'TRIO, Ein Ganim, Petah Tikva', 'city' => 'Petah Tikva', 'kind' => 'Three years without management fees', 'short' => 'no management fees', 'terms' => 'Three years without building management fees, worth about ₪25,000 per apartment. 4 and 5 rooms from ₪2.71M.', 'bar' => array( 'regular payment plan' ), 'pub' => 'November 2026' ),
			'sharet'    => array( 'dev' => 'Ashed & Rotshtein', 'devFull' => 'Ashed & Rotshtein Real Estate', 'project' => '38 Sharet, Tel Aviv', 'city' => 'Tel Aviv', 'kind' => 'Fully furnished apartment', 'short' => 'furnished', 'terms' => 'A 4-room, 102 m² apartment, fully furnished and designed, with a balcony, safe room and parking. ₪6.66M.', 'bar' => array( 'regular payment plan' ), 'pub' => '2026' ),
			'rayk'      => array( 'dev' => 'RAYK', 'devFull' => 'RAYK Real Estate', 'project' => 'RAYK New Lod, 2 Anne Frank', 'city' => 'Lod', 'kind' => '₪215K and the rest at occupancy', 'short' => '₪215K in', 'terms' => 'On a 4-room apartment: ₪215,000 and the rest at occupancy, subject to a subsidised developer loan, with special benefits for combat soldiers. 3 rooms from ₪1.95M, 4 rooms ₪2.15M. Occupancy expected June 2029.', 'bar' => array( '', 'at occupancy' ), 'pub' => '2026' ),
			'tzahala'   => array( 'dev' => 'Dankner', 'devFull' => 'Dankner Kanlov', 'project' => 'Ramot Tzahala, 12 Tolkovsky, Tel Aviv', 'city' => 'Tel Aviv', 'kind' => 'Presale price', 'short' => 'presale price', 'terms' => 'The last 6-room apartment at the presale price: ₪7.65M.', 'bar' => array( 'regular payment plan' ), 'pub' => '2026' ),
			'isa'       => array( 'dev' => 'ISA', 'devFull' => 'ISA Group, marketed by Magma', 'project' => 'Mevaseret Zion', 'city' => 'Mevaseret Zion', 'kind' => 'Rent-to-own', 'short' => 'rent-to-own', 'terms' => 'Rent a finished apartment; part of the rent, sometimes all of it, counts as equity if you buy at the end of the period. No price published.', 'bar' => array( 'rent with an option' ), 'pub' => 'July 2026' ),
		);
	}
}

if ( ! function_exists( 'nadlan_dm_deal_for_post' ) ) {
	/** The live deal on the map that belongs to this catalog project (by 'pid'), or null. Used for the red label on its card. */
	function nadlan_dm_deal_for_post( $id ) {
		static $by = null;
		if ( null === $by ) { $by = array(); foreach ( nadlan_dm_deals() as $d ) { if ( ! empty( $d['pid'] ) ) { $by[ (int) $d['pid'] ] = $d; } } }
		return $by[ (int) $id ] ?? null;
	}
}

if ( ! function_exists( 'nadlan_dm_fx' ) ) {
	/** The Bank of Israel dollar rate kept for the language pages (assets/instruments/data/boi-fx.json): array( rate, date ) or null. */
	function nadlan_dm_fx() {
		$f = dirname( __DIR__ ) . '/assets/instruments/data/boi-fx.json';
		$j = is_readable( $f ) ? json_decode( (string) file_get_contents( $f ), true ) : null; // phpcs:ignore WordPress.WP.AlternativeFunctions
		$u = is_array( $j ) ? ( $j['fx']['USD'] ?? ( $j['USD'] ?? null ) ) : null;
		return ( is_array( $u ) && ! empty( $u['rate'] ) ) ? array( (float) $u['rate'], (string) $u['date'] ) : null;
	}
}

if ( ! function_exists( 'nadlan_dm_is_page' ) ) {
	/** True on the Hebrew page only (the "דירות חדשות בהנחה" section is Hebrew). */
	function nadlan_dm_is_page() { return 'he' === nadlan_dm_lang(); }
}

if ( ! function_exists( 'nadlan_dm_lang' ) ) {
	/** 'he' on /developer-deals/, 'en' on /en/developer-deals/, '' anywhere else (fr/ru/ar pages keep their article). */
	function nadlan_dm_lang() {
		if ( ! is_page() ) { return ''; }
		$p = get_queried_object();
		if ( ! $p || 0 !== strpos( (string) $p->post_name, 'developer-deals' ) ) { return ''; }
		$u = (string) ( $_SERVER['REQUEST_URI'] ?? '' );
		if ( preg_match( '~^/en/~', $u ) ) { return 'en'; }
		return preg_match( '~^/(fr|ru|ar)/~', $u ) ? '' : 'he';
	}
}

if ( ! function_exists( 'nadlan_dm_fmt' ) ) {
	function nadlan_dm_fmt( $n ) {
		$n = (float) $n;
		return $n >= 1000000 ? rtrim( rtrim( number_format( $n / 1000000, 2, '.', '' ), '0' ), '.' ) . ' מיליון ₪' : number_format( round( $n / 1000 ) ) . ' אלף ₪';
	}
}

if ( ! function_exists( 'nadlan_dm_render' ) ) {
	function nadlan_dm_render() {
		$deals = nadlan_dm_deals();
		$wa    = preg_replace( '/\D+/', '', (string) get_option( 'nadlan_whatsapp_e164', '972525101555' ) );
		$base  = plugins_url( 'assets/deals/', dirname( __FILE__ ) );
		$data  = array(
			'deals'     => $deals,
			'hotId'     => 'gindi-love',
			'wa'        => $wa,
			'pointsUrl' => $base . 'projects.json?v=1',
			'mlJs'      => 'https://cdnjs.cloudflare.com/ajax/libs/maplibre-gl/5.24.0/maplibre-gl.js',
			'mlCss'     => 'https://cdnjs.cloudflare.com/ajax/libs/maplibre-gl/5.24.0/maplibre-gl.css',
			'style'     => 'https://tiles.openfreemap.org/styles/positron',
		);
		$kinds = array( 'all' => 'הכל', 'pay' => '10/90, 20/80 ותשלומים', 'rent' => 'שכר דירה עד האכלוס', 'price' => 'הנחה במחיר', 'gift' => 'מתנות ופטורים' );
		$waq   = function ( $t ) use ( $wa ) { return 'https://wa.me/' . $wa . '?text=' . rawurlencode( $t ); };
		ob_start();
		?>
<section id="nldm" class="nldm" dir="rtl" aria-label="מפת מבצעי הקבלנים">
	<p class="nldm-lead">כל מבצעי הקבלנים על מפה אחת, וכל הדירות החדשות בהנחה ובמבצע שאפשר לקנות עכשיו בלי הגרלה: 20/80 ו-10/90, הלוואת קבלן, שכר דירה עד האכלוס, הנחות במחיר ופטורים. לכל מבצע כתוב מה בדיוק פורסם ומתי, כמה צריך ביד ביום החתימה, כמה הוא שווה בשקלים, ואם בדקנו שהוא עדיין בתוקף.</p>
	<div class="nldm-live"><span class="nldm-pulse" aria-hidden="true"></span><span><b><?php echo (int) count( $deals ); ?></b> מבצעים על המפה · <b><?php echo (int) count( nadlan_dm_archive() ); ?></b> בארכיון · עודכן 15.11.2026</span></div>
	<div class="nldm-ctas">
		<a class="nldm-btn is-main" href="<?php echo esc_url( $waq( 'היי, אשמח למחירון מעודכן ולתנאי המבצעים של הקבלנים' ) ); ?>" target="_blank" rel="noopener">בקשו מחירון מעודכן</a>
		<a class="nldm-btn" href="<?php echo esc_url( $waq( 'היי, אשמח להתייעץ עם יועץ משכנתאות על מבצע קבלן' ) ); ?>" target="_blank" rel="noopener">ייעוץ משכנתא חינם</a>
	</div>

	<div class="nldm-cash">
		<div class="nldm-cash-top"><label for="nldm-cash">כמה יש לכם ביד היום?</label><output id="nldm-cash-out" for="nldm-cash">600 אלף ₪</output></div>
		<input id="nldm-cash" type="range" min="0" max="1500000" step="10000" value="600000">
		<div class="nldm-legend" aria-live="polite"><span class="nldm-think" hidden><i></i><i></i><i></i> מחשב</span><span class="nldm-lg is-fit">מתאים לכם: <b data-n="fit">0</b></span><span class="nldm-lg is-no">צריך יותר: <b data-n="no">0</b></span><span class="nldm-lg is-unk">בקשו מחיר: <b data-n="unk">0</b></span></div>
	</div>

	<nav class="nldm-chips" aria-label="סוג המבצע">
		<?php foreach ( $kinds as $k => $l ) : ?><button type="button" data-k="<?php echo esc_attr( $k ); ?>"<?php echo 'all' === $k ? ' class="is-on" aria-pressed="true"' : ' aria-pressed="false"'; ?>><?php echo esc_html( $l ); ?></button><?php endforeach; ?>
	</nav>

	<div class="nldm-stage">
		<div id="nldm-map" class="nldm-map" role="region" aria-label="מפה תלת ממדית של המבצעים"><div class="nldm-map-wait"><span></span><span></span><span></span></div></div>
		<div class="nldm-mapbar">
			<button type="button" data-act="tilt">מבט מלמעלה</button>
			<button type="button" data-act="all">כל הארץ</button>
			<button type="button" data-act="near">קרוב אליי</button>
		</div>
		<p class="nldm-mapnote">נקודה אפורה: פרויקט חדש מהמאגר שלנו, לחצו עליה לכרטיס שלו. מיקומי המבצעים משוערים, לפי העיר או השכונה.</p>
	</div>

	<article class="nldm-sheet" aria-live="polite">
		<div class="nldm-sheet-head"><span class="nldm-chip" data-f="init"></span><div><span class="nldm-sub" data-f="sub"></span><h2 data-f="project"></h2><span class="nldm-kind" data-f="kind"></span></div></div>
		<blockquote class="nldm-terms"><small>כפי שפורסם</small><span data-f="terms"></span></blockquote>
		<div class="nldm-when"><b>מתי משלמים</b><div class="nldm-bar" data-f="bar"></div></div>
		<div class="nldm-nums">
			<div><small>מחיר מ-</small><b data-f="price"></b></div>
			<div><small>ביד בחתימה</small><b data-f="need"></b></div>
			<div class="is-worth"><small>שווה בשקלים</small><b data-f="worth"></b></div>
		</div>
		<p class="nldm-check" data-f="check"></p>
		<p class="nldm-sheet-legal">הפרטים לפי פרסומים, ועשויים להשתנות. התנאים המחייבים הם אלה שבחוזה מול היזם.</p>
		<div class="nldm-act">
			<a class="nldm-btn is-main" data-f="wa1" target="_blank" rel="noopener" href="#">בדקו אם המבצע בתוקף וקבלו מחירון</a>
			<a class="nldm-btn" data-f="wa2" target="_blank" rel="noopener" href="#">משכנתא והשלמת הון למבצע הזה</a>
		</div>
		<button type="button" class="nldm-tocalc">חשבו כמה הנחה המבצע הזה נותן באמת ›</button>
		<div class="nldm-tools">
			<a href="/mortgage-calculator/"><b>מחשבון משכנתא</b><span>ההחזר החודשי עם המבצע</span></a>
			<a href="/purchase-tax-calculator/"><b>מחשבון מס רכישה</b><span>כמה מס על הדירה</span></a>
			<a href="/projects/"><b>כל הפרויקטים החדשים</b><span>דירות מקבלן עם מחירים ומפה</span></a>
			<a href="/my-rentals/"><b>קונים להשקעה?</b><span>ניהול השכירות עלינו</span></a>
		</div>
	</article>

	<section id="nldm-calc" class="nldm-calc" aria-label="מחשבון ההנחה האמיתית">
		<h2>כמה הנחה קיבלתם באמת? המחשבון של מבצעי הקבלנים</h2>
		<p>בחרו מבצע. המחשבון משווה אותו ללוח תשלומים רגיל של דירה חדשה מקבלן, עם הריבית, ההצמדה למדד תשומות הבנייה ושכר הדירה, ומחזיר מספר אחד בשקלים.</p>
		<div class="nldm-calc-pre" role="group" aria-label="מבצע לחישוב"></div>
		<p class="nldm-calc-note">רק מבצעים שפורסמו להם מחיר ולוח תשלומים נכנסים לחישוב. את מבצע גינדי "המפץ הגדול" אי אפשר לחשב מהפרסומים: המחיר המוצג לא כולל את הלוואת הקרדיט, ובלי המחיר המלא בחוזה ובלי סכום ההלוואה כל מספר יהיה ניחוש. יש לכם הצעה כתובה מהיזם? בחרו "המבצע שלי" והזינו את המספרים ממנה.</p>
		<div class="nldm-calc-res">
			<div class="nldm-gauge" aria-hidden="true"><svg viewBox="0 0 96 96"><circle cx="48" cy="48" r="40" class="g0"/><circle cx="48" cy="48" r="40" class="g1"/></svg><b class="nldm-gauge-n">0%</b></div>
			<div class="nldm-calc-big"><span>הערכה: המבצע שווה לכם בערך</span><b class="nldm-calc-total" aria-live="polite">0 ₪</b><span class="nldm-calc-pct"></span></div>
		</div>
		<p class="nldm-calc-est">הערכה בלבד, לפי פרסומי היזם והנחות החישוב שלמטה. התנאים המחייבים הם אלה שבחוזה.</p>
		<div class="nldm-calc-parts"></div>
		<details class="nldm-calc-in"><summary>הנחות החישוב, אפשר לשנות</summary><div class="nldm-calc-fields"></div></details>
		<div class="nldm-act">
			<a class="nldm-btn is-main" data-f="calc-wa1" target="_blank" rel="noopener" href="<?php echo esc_url( $waq( 'היי, אשמח למחיר עם המבצע ובלעדיו' ) ); ?>">בקשו מהיזם מחיר עם המבצע ובלעדיו</a>
			<a class="nldm-btn" target="_blank" rel="noopener" href="<?php echo esc_url( $waq( 'היי, אשמח שיועץ משכנתאות יבדוק את המספרים של מבצע קבלן' ) ); ?>">יועץ משכנתאות יבדוק, חינם</a>
		</div>
		<p class="nldm-calc-how">איך מחשבים: לוח רגיל הוא 20% בחתימה והיתרה בתשלומים חודשיים עד האכלוס, כשמחצית מכל תשלום צמודה למדד (כמו בחוק המכר). כל תשלום מהוון להיום לפי הריבית שבחרתם. ההפרש בין שני הלוחות, ועוד שכר הדירה מהיזם, פחות התוספת למחיר, הוא ההנחה המשוערת. המחשבון לא יודע על עמלות, ביטוחים, תנאי הבנק, מס רכישה או סעיפים מיוחדים בחוזה.</p>
		<p class="nldm-legal">המידע בעמוד מבוסס על פרסומים פומביים של היזמים ושל כלי התקשורת, כפי שנמצאו בתאריך שמופיע ליד כל מבצע. מבצעים משתנים ומסתיימים בלי הודעה, ולכן ייתכנו פערים וטעויות. החישובים משוערים בלבד, ואינם ייעוץ פיננסי, משפטי, מיסויי או ייעוץ השקעות, ואינם הצעה או המלצה לרכוש. לפני כל החלטה בקשו מהיזם את התנאים בכתב, בדקו את החוזה עם עורך דין, והתייעצו עם יועץ משכנתאות ושמאי. נדל״ן אינו מתווך ואינו צד לעסקה.</p>
	</section>

	<section class="nldm-list" aria-label="כל המבצעים">
		<h2>כל מבצעי הקבלנים: דירות חדשות בהנחה, מהמתאים לכם ביותר</h2>
		<ol>
		<?php foreach ( $deals as $d ) : ?>
			<li data-id="<?php echo esc_attr( $d['id'] ); ?>"><button type="button" data-pick="<?php echo esc_attr( $d['id'] ); ?>"><span class="nldm-dot" style="background:<?php echo esc_attr( $d['color'] ); ?>"></span><span class="nldm-li"><b><?php echo esc_html( $d['project'] ); ?></b><span><?php echo esc_html( $d['devFull'] . ' · ' . $d['kind'] . ' · פורסם ' . $d['pub'] ); ?></span><span class="nldm-li-terms"><?php echo esc_html( $d['terms'] ); ?></span></span><span class="nldm-need"></span></button></li>
		<?php endforeach; ?>
		</ol>
	</section>

	<section class="nldm-expert" aria-label="התייעצות עם מומחה">
		<h2>מצאתם מבצע? אל תחתמו לבד</h2>
		<p>מבצע של קבלן משנה בעיקר מתי משלמים. לפני שחותמים כדאי לבדוק שלושה דברים: האם הבנק יאשר משכנתא למבנה התשלומים, מה המחיר בלי המבצע, ומה כתוב בחוזה על ההצמדה.</p>
		<div class="nldm-expert-grid">
			<a href="<?php echo esc_url( $waq( 'היי, אשמח לייעוץ משכנתא למבצע קבלן (20/80 או 10/90)' ) ); ?>" target="_blank" rel="noopener"><b>יועץ משכנתאות</b><span>האם הבנק יאשר את מבנה התשלומים</span></a>
			<a href="<?php echo esc_url( $waq( 'היי, אשמח לשמוע על הלוואה להשלמת הון לדירה מקבלן' ) ); ?>" target="_blank" rel="noopener"><b>השלמת הון</b><span>הלוואה לסכום שחסר ביום החתימה</span></a>
			<a href="<?php echo esc_url( $waq( 'היי, אשמח לבדיקה של חוזה מקבלן לפני חתימה' ) ); ?>" target="_blank" rel="noopener"><b>בדיקה לפני חתימה</b><span>עורך דין ושמאי על החוזה והמחיר</span></a>
		</div>
	</section>

	<p class="nldm-legal">המידע בעמוד מבוסס על פרסומים פומביים של היזמים ושל כלי התקשורת, כפי שנמצאו בתאריך שמופיע ליד כל מבצע. מבצעים משתנים ומסתיימים בלי הודעה, ולכן ייתכנו פערים וטעויות. החישובים משוערים בלבד, ואינם ייעוץ פיננסי, משפטי, מיסויי או ייעוץ השקעות, ואינם הצעה או המלצה לרכוש. לפני כל החלטה בקשו מהיזם את התנאים בכתב, בדקו את החוזה עם עורך דין, והתייעצו עם יועץ משכנתאות ושמאי. נדל״ן אינו מתווך ואינו צד לעסקה.</p>

	<section class="nldm-archive" aria-label="ארכיון מבצעים שהסתיימו">
		<h2>ארכיון: מבצעים שהסתיימו</h2>
		<ul>
		<?php foreach ( nadlan_dm_archive() as $a ) : ?><li><b><?php echo esc_html( $a[0] ); ?></b> · <?php echo esc_html( $a[1] ); ?> · <span><?php echo esc_html( $a[2] ); ?></span></li><?php endforeach; ?>
		</ul>
	</section>
	<script type="application/json" id="nldm-data"><?php echo wp_json_encode( $data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG ); ?></script>
	<?php echo nadlan_dm_jsonld( $deals, 'he' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
</section>
		<?php
		return (string) ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_dm_jsonld' ) ) {
	/** Structured data for Google and AI answer engines (AEO/GEO): the deals as an ItemList of ApartmentComplex (name, developer, place,
	 * approximate geo, the terms as published, publish month, source) plus a Dataset describing the table. Nothing beyond the visible
	 * page; no prices are claimed as offers of ours. */
	function nadlan_dm_jsonld( $deals, $lang ) {
		$url  = 'en' === $lang ? home_url( '/en/developer-deals/' ) : home_url( '/developer-deals/' );
		$items = array(); $i = 0;
		foreach ( $deals as $d ) {
			$i++;
			$prop = array( array( '@type' => 'PropertyValue', 'name' => 'en' === $lang ? 'Deal type' : 'סוג המבצע', 'value' => $d['kind'] ),
				array( '@type' => 'PropertyValue', 'name' => 'en' === $lang ? 'Published' : 'פורסם', 'value' => $d['pub'] ) );
			if ( ! empty( $d['src'] ) ) { $prop[] = array( '@type' => 'PropertyValue', 'name' => 'en' === $lang ? 'Source' : 'מקור', 'value' => $d['src'] ); }
			$items[] = array( '@type' => 'ListItem', 'position' => $i, 'item' => array_filter( array(
				'@type' => 'ApartmentComplex', 'name' => $d['project'], 'description' => $d['terms'],
				'address' => array( '@type' => 'PostalAddress', 'addressLocality' => $d['city'], 'addressCountry' => 'IL' ),
				'geo' => array( '@type' => 'GeoCoordinates', 'latitude' => $d['lat'], 'longitude' => $d['lng'] ),
				'url' => ! empty( $d['link'] ) ? home_url( ( 'en' === $lang ? '' : '' ) . $d['link'] ) : null,
				'additionalProperty' => $prop,
			) ) );
		}
		$name = 'en' === $lang ? 'Israel developer deals map, November 2026' : 'מפת מבצעי הקבלנים בישראל, נובמבר 2026';
		$graph = array(
			'@context' => 'https://schema.org',
			'@graph'   => array(
				array( '@type' => 'ItemList', '@id' => $url . '#deals', 'name' => $name, 'numberOfItems' => count( $items ), 'itemListElement' => $items ),
				array( '@type' => 'Dataset', '@id' => $url . '#dataset', 'name' => $name, 'inLanguage' => 'en' === $lang ? 'en' : 'he',
					'description' => 'en' === $lang ? 'Live new-build developer deals in Israel (payment plans, 0% equity, developer loans, rent until handover) with the terms as published, the publish date and the source of each deal.' : 'מבצעי קבלנים פעילים בישראל (לוחות תשלומים, 0% הון עצמי, הלוואות קבלן, שכר דירה עד האכלוס) עם התנאים כפי שפורסמו, תאריך הפרסום והמקור של כל מבצע.',
					'url' => $url, 'dateModified' => '2026-11-16', 'spatialCoverage' => array( '@type' => 'Place', 'name' => 'Israel' ),
					'creator' => array( '@type' => 'Organization', 'name' => 'NadLan', 'url' => home_url( '/' ) ),
					'isAccessibleForFree' => true ),
			),
		);
		return '<script type="application/ld+json">' . wp_json_encode( $graph, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG ) . '</script>';
	}
}

if ( ! function_exists( 'nadlan_dm_t_en' ) ) {
	/** English for every Hebrew text the script prints (the Hebrew text is the key). */
	function nadlan_dm_t_en() {
		return array(
			'בקשו מחיר ›' => 'Ask for the price ›', '0 ₪ בחתימה' => '₪0 at signing', ' ביד' => ' in hand', 'בקשו מחיר' => 'Ask for price',
			' · מבצע חם' => ' · Hot deal', 'לא פורסם' => 'Not published', 'כ-' => '~', ' לפי פרסום' => ' as published',
			'בדקנו שהמבצע עדיין מוצע ב-' => 'We checked the deal is still offered on ', 'פורסם: ' => 'Published: ',
			'. עוד לא אישרנו שהוא עדיין בתוקף: לחצו ונבדוק מול היזם. ' => '. Not yet confirmed as still valid: tap and we will check with the developer. ',
			'לעמוד הפרויקט' => 'Project page', 'המקור' => 'Source',
			'היי, אשמח לבדוק אם המבצע ב' => 'Hi, please check whether the deal at ', ') עדיין בתוקף ולקבל מחירון ותוכניות' => ') is still valid and send me the price list and plans',
			'היי, אשמח לייעוץ משכנתא והשלמת הון למבצע ב' => 'Hi, I would like mortgage and equity advice for the deal at ',
			'מבצע חם' => 'Hot deal', 'פרויקט חדש מהמאגר שלנו' => 'A new project from our database', 'מבט מלמעלה' => 'Top view', 'תלת ממד' => '3D view',
			'מחיר הדירה' => 'Apartment price', 'משלמים בחתימה' => 'Paid at signing', 'חודשים עד האכלוס' => 'Months to occupancy', ' חודשים' => ' months',
			'מדד תשומות הבנייה לשנה' => 'Construction index per year', 'ריבית אלטרנטיבית (משכנתא)' => 'Alternative rate (mortgage)',
			'שכר דירה מהיזם לחודש' => 'Rent from the developer per month', 'לכמה חודשים' => 'For how many months', 'הנחה ישירה במחיר' => 'Direct price cut',
			'תוספת למחיר בגלל המבצע' => 'Price premium because of the deal', 'שהם ' => 'that is ', '% הנחה אמיתית ממחיר הדירה' => '% real discount on the price',
			'כסף שנשאר אצלכם, גם אחרי האכלוס' => 'Money that stays with you, past occupancy', 'כסף שנשאר אצלכם עד האכלוס' => 'Money that stays with you until occupancy',
			'חלק מהמחיר משולם ' => 'Part of the price is paid ', ' שנים אחרי האכלוס, בלי ריבית והצמדה' => ' years after occupancy, without interest or indexation',
			'משלמים מאוחר יותר, והכסף עובד בינתיים בריבית ' => 'You pay later, and the money earns meanwhile at ',
			'הצמדה למדד שנחסכה' => 'Indexation saved', 'הצמדה נוספת בגלל הדחייה' => 'Extra indexation from the deferral', 'פטור מלא מהצמדה ליתרה' => 'Full index exemption on the balance',
			'בלי פטור, היתרה הדחויה צמודה עד האכלוס' => 'No exemption: the deferred balance is indexed until occupancy', 'שכר דירה או הטבה חודשית מהיזם' => 'Rent or monthly benefit from the developer',
			' חודשים של ' => ' months of ', 'עד ' => 'up to ', ', לפי פרסום. לוח התשלומים לא פורסם ולכן נספר כרגיל' => ', as published. No payment plan was published, so it counts as regular',
			'אין במבצע הזה' => 'Not in this deal', 'כפי שפורסם' => 'As published', 'שאלו את היזם מחיר בלי המבצע' => 'Ask the developer for the price without the deal',
			'פטור מהצמדה: כן' => 'Index exemption: yes', 'פטור מהצמדה: לא' => 'Index exemption: no', 'המבצע שלי' => 'My deal',
		);
	}
}

if ( ! function_exists( 'nadlan_dm_render_en' ) ) {
	/** The English map (/en/developer-deals/): same blocks and script as the Hebrew one, English text, approximate dollars. */
	function nadlan_dm_render_en() {
		$en = nadlan_dm_en(); $deals = array();
		foreach ( nadlan_dm_deals() as $d ) {
			if ( ! isset( $en[ $d['id'] ] ) ) { continue; }
			$e = $en[ $d['id'] ];
			foreach ( array( 'dev', 'devFull', 'project', 'city', 'kind', 'short', 'terms', 'pub' ) as $f ) { $d[ $f ] = $e[ $f ]; }
			foreach ( $d['bar'] as $k => $b ) { $d['bar'][ $k ][1] = $e['bar'][ $k ] ?? ''; }
			$d['checked'] = '' !== (string) ( $d['checked'] ?? '' ) ? '15 November 2026' : '';
			$deals[] = $d;
		}
		$wa  = preg_replace( '/\D+/', '', (string) get_option( 'nadlan_whatsapp_e164', '972525101555' ) );
		$fx  = nadlan_dm_fx();
		$base = plugins_url( 'assets/deals/', dirname( __FILE__ ) );
		$data = array( 'deals' => $deals, 'hotId' => 'gindi-love', 'wa' => $wa, 'lang' => 'en', 't' => nadlan_dm_t_en(), 'fx' => $fx,
			'pointsUrl' => $base . 'projects.json?v=1', 'mlJs' => 'https://cdnjs.cloudflare.com/ajax/libs/maplibre-gl/5.24.0/maplibre-gl.js',
			'mlCss' => 'https://cdnjs.cloudflare.com/ajax/libs/maplibre-gl/5.24.0/maplibre-gl.css', 'style' => 'https://tiles.openfreemap.org/styles/positron' );
		$kinds = array( 'all' => 'All', 'pay' => 'Payment plans (20/80, 10/90)', 'rent' => 'Rent until handover', 'price' => 'Price cuts', 'gift' => 'Gifts and waivers' );
		$waq = function ( $t ) use ( $wa ) { return 'https://wa.me/' . $wa . '?text=' . rawurlencode( $t ); };
		$fxl = $fx ? 'Dollar figures are approximate, at the Bank of Israel rate of ' . number_format( $fx[0], 3 ) . ' (' . $fx[1] . '); the shekel price is the price.' : '';
		$legal = 'This page is based on public announcements by developers and the press, as found on the date shown next to each deal. Deals change and end without notice, so gaps and mistakes are possible. All calculations are estimates and are not financial, legal, tax or investment advice, nor an offer or recommendation to buy. Before any decision, get the terms in writing from the developer, have a lawyer check the contract, and consult a mortgage advisor and an appraiser. NadLan is not a broker and is not a party to any transaction.';
		ob_start(); ?>
<section id="nldm" class="nldm" dir="ltr" lang="en" aria-label="Israel developer deals map">
	<p class="nldm-lead">Every live Israeli developer deal on one map: 20/80 and 10/90 payment plans, 0% equity, developer loans, rent paid until handover, price cuts and waivers. For each deal: the terms as published and when, the cash you need at signing, an estimate of what it is worth in shekels with an approximate dollar figure, and whether we confirmed it is still on.</p>
	<div class="nldm-live"><span class="nldm-pulse" aria-hidden="true"></span><span><b><?php echo (int) count( $deals ); ?></b> deals on the map · <b><?php echo (int) count( nadlan_dm_archive() ); ?></b> in the archive · updated 16 November 2026</span></div>
	<div class="nldm-ctas">
		<a class="nldm-btn is-main" href="<?php echo esc_url( $waq( 'Hi, I would like the current price list and deal terms for new projects in Israel' ) ); ?>" target="_blank" rel="noopener">Get the price list</a>
		<a class="nldm-btn" href="<?php echo esc_url( $waq( 'Hi, I would like to talk to a mortgage advisor about buying a new apartment in Israel' ) ); ?>" target="_blank" rel="noopener">Free mortgage advice</a>
	</div>
	<div class="nldm-cash">
		<div class="nldm-cash-top"><label for="nldm-cash">Cash in hand today?</label><output id="nldm-cash-out" for="nldm-cash">₪600K<?php echo $fx ? ' (≈ $' . (int) round( 600000 / $fx[0] / 1000 ) . 'K)' : ''; ?></output></div>
		<input id="nldm-cash" type="range" min="0" max="1500000" step="10000" value="600000">
		<div class="nldm-legend" aria-live="polite"><span class="nldm-think" hidden><i></i><i></i><i></i> working</span><span class="nldm-lg is-fit">Fits you: <b data-n="fit">0</b></span><span class="nldm-lg is-no">Needs more: <b data-n="no">0</b></span><span class="nldm-lg is-unk">Ask for price: <b data-n="unk">0</b></span></div>
	</div>
	<nav class="nldm-chips" aria-label="Deal type">
		<?php foreach ( $kinds as $k => $l ) : ?><button type="button" data-k="<?php echo esc_attr( $k ); ?>"<?php echo 'all' === $k ? ' class="is-on" aria-pressed="true"' : ' aria-pressed="false"'; ?>><?php echo esc_html( $l ); ?></button><?php endforeach; ?>
	</nav>
	<div class="nldm-stage">
		<div id="nldm-map" class="nldm-map" role="region" aria-label="3D map of the deals"><div class="nldm-map-wait"><span></span><span></span><span></span></div></div>
		<div class="nldm-mapbar"><button type="button" data-act="tilt">Top view</button><button type="button" data-act="all">All Israel</button><button type="button" data-act="near">Near me</button></div>
		<p class="nldm-mapnote">Grey dot: a new project from our database, tap it for its page. Deal locations are approximate, by city or neighbourhood.</p>
	</div>
	<article class="nldm-sheet" aria-live="polite">
		<div class="nldm-sheet-head"><span class="nldm-chip" data-f="init"></span><div><span class="nldm-sub" data-f="sub"></span><h2 data-f="project"></h2><span class="nldm-kind" data-f="kind"></span></div></div>
		<blockquote class="nldm-terms"><small>As published</small><span data-f="terms"></span></blockquote>
		<div class="nldm-when"><b>When you pay</b><div class="nldm-bar" data-f="bar"></div></div>
		<div class="nldm-nums"><div><small>Price from</small><b data-f="price"></b></div><div><small>Cash at signing</small><b data-f="need"></b></div><div class="is-worth"><small>Worth</small><b data-f="worth"></b></div></div>
		<p class="nldm-check" data-f="check"></p>
		<p class="nldm-sheet-legal">Details as published and subject to change. The contract with the developer is binding.</p>
		<div class="nldm-act">
			<a class="nldm-btn is-main" data-f="wa1" target="_blank" rel="noopener" href="#">Check it is still on, get the price list</a>
			<a class="nldm-btn" data-f="wa2" target="_blank" rel="noopener" href="#">Mortgage and equity for this deal</a>
		</div>
		<button type="button" class="nldm-tocalc">Work out what this deal is really worth ›</button>
		<div class="nldm-tools">
			<a href="/en/mortgage-calculator/"><b>Mortgage calculator</b><span>Monthly payment with the deal</span></a>
			<a href="/en/projects/"><b>All new projects</b><span>New-build apartments with prices and a map</span></a>
		</div>
	</article>
	<section id="nldm-calc" class="nldm-calc" aria-label="True discount calculator">
		<h2>What is the deal really worth? The developer-deal calculator</h2>
		<p>Pick a deal. The calculator compares it with a regular new-build payment plan, with interest, indexation to the construction input index and any rent from the developer, and returns one figure in shekels.</p>
		<div class="nldm-calc-pre" role="group" aria-label="Deal to calculate"></div>
		<p class="nldm-calc-note">Only deals with a published price and payment plan are calculated. Gindi's "Big Bang" cannot be priced from what was published: the displayed price excludes the credit loan, so without the full contract price and the loan amount any figure would be a guess. Have a written offer? Pick "My deal" and enter its numbers.</p>
		<div class="nldm-calc-res">
			<div class="nldm-gauge" aria-hidden="true"><svg viewBox="0 0 96 96"><circle cx="48" cy="48" r="40" class="g0"/><circle cx="48" cy="48" r="40" class="g1"/></svg><b class="nldm-gauge-n">0%</b></div>
			<div class="nldm-calc-big"><span>Estimate: the deal is worth about</span><b class="nldm-calc-total" aria-live="polite">₪0</b><span class="nldm-calc-pct"></span></div>
		</div>
		<p class="nldm-calc-est">An estimate only, from the developer's announcements and the assumptions below. The contract terms are binding.</p>
		<div class="nldm-calc-parts"></div>
		<details class="nldm-calc-in"><summary>Assumptions, you can change them</summary><div class="nldm-calc-fields"></div></details>
		<div class="nldm-act">
			<a class="nldm-btn is-main" target="_blank" rel="noopener" href="<?php echo esc_url( $waq( 'Hi, I would like the price with and without the deal' ) ); ?>">Ask for the price with and without the deal</a>
			<a class="nldm-btn" target="_blank" rel="noopener" href="<?php echo esc_url( $waq( 'Hi, I would like a mortgage advisor to check the numbers of a developer deal' ) ); ?>">A mortgage advisor will check, free</a>
		</div>
		<p class="nldm-calc-how">How it works: a regular plan is 20% at signing and monthly payments until occupancy, half of each indexed (as in Israel's Sale of Apartments Law). Every payment is discounted to today at the rate you chose. The difference between the two plans, plus rent from the developer, minus any price premium, is the estimated discount. It does not know about fees, insurance, bank terms, purchase tax or special contract clauses. <?php echo esc_html( $fxl ); ?></p>
		<p class="nldm-legal"><?php echo esc_html( $legal ); ?></p>
	</section>
	<section class="nldm-list" aria-label="All deals">
		<h2>All developer deals in Israel, best fit first</h2>
		<ol>
		<?php foreach ( $deals as $d ) : ?>
			<li data-id="<?php echo esc_attr( $d['id'] ); ?>"><button type="button" data-pick="<?php echo esc_attr( $d['id'] ); ?>"><span class="nldm-dot" style="background:<?php echo esc_attr( $d['color'] ); ?>"></span><span class="nldm-li"><b><?php echo esc_html( $d['project'] ); ?></b><span><?php echo esc_html( $d['devFull'] . ' · ' . $d['kind'] . ' · published ' . $d['pub'] ); ?></span><span class="nldm-li-terms"><?php echo esc_html( $d['terms'] ); ?></span></span><span class="nldm-need"></span></button></li>
		<?php endforeach; ?>
		</ol>
	</section>
	<section class="nldm-expert" aria-label="Talk to an expert">
		<h2>Found a deal? Do not sign alone</h2>
		<p>A developer deal mostly changes when you pay. Before signing, check three things: will an Israeli bank approve a mortgage for this payment plan (foreign buyers usually get up to 50% financing), what is the price without the deal, and what does the contract say about indexation.</p>
		<div class="nldm-expert-grid">
			<a href="<?php echo esc_url( $waq( 'Hi, I would like mortgage advice for a developer deal in Israel' ) ); ?>" target="_blank" rel="noopener"><b>Mortgage advisor</b><span>Will the bank approve this payment plan</span></a>
			<a href="<?php echo esc_url( $waq( 'Hi, I would like to hear about bridging the equity for a new apartment in Israel' ) ); ?>" target="_blank" rel="noopener"><b>Equity gap</b><span>A loan for what is missing at signing</span></a>
			<a href="<?php echo esc_url( $waq( 'Hi, I would like a lawyer to review a developer contract before signing' ) ); ?>" target="_blank" rel="noopener"><b>Contract check</b><span>A lawyer and an appraiser on the contract and price</span></a>
		</div>
	</section>
	<p class="nldm-legal"><?php echo esc_html( $legal ); ?></p>
	<script type="application/json" id="nldm-data"><?php echo wp_json_encode( $data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG ); ?></script>
	<?php echo nadlan_dm_jsonld( $deals, 'en' ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
</section>
		<?php
		return (string) ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_dm_discount_section' ) ) {
	/** HAD-743 (Ben 15.11.2026): "דירות חדשות בהנחה" in the middle of the article. Google splits that search between the state programme
	 * and market deals (manual search 15.11.2026); the state programme itself is owned by /dira-behanacha/, so this is a comparison
	 * that sends the programme intent there. Facts from that page (lottery 11, appraisers' range). */
	function nadlan_dm_discount_section() {
		ob_start(); ?>
<section class="nldm nldm-disc" dir="rtl" aria-labelledby="nldm-disc-h">
	<h2 id="nldm-disc-h">דירות חדשות בהנחה: תוכנית המדינה מול מבצעי הקבלנים</h2>
	<p>יש שתי דרכים לקנות דירה חדשה בהנחה. הראשונה היא דירה בהנחה של משרד הבינוי והשיכון: דירות חדשות מקבלן במחיר מופחת, בהגרלה, לזכאים חסרי דירה. השנייה היא מבצעי הקבלנים בשוק החופשי: בלי הגרלה ובלי תנאי זכאות, אבל ההנחה מסתתרת בלוח התשלומים, ולכן צריך לחשב אותה.</p>
	<div class="nldm-disc-t" role="table" aria-label="דירה בהנחה מול מבצע קבלן">
		<div role="row" class="h"><span role="columnheader"></span><span role="columnheader">דירה בהנחה של המדינה</span><span role="columnheader">מבצע קבלן</span></div>
		<div role="row"><span role="rowheader">למי</span><span role="cell">זכאים חסרי דירה, ומשפרי דיור בהגרלות המשך</span><span role="cell">לכל קונה</span></div>
		<div role="row"><span role="rowheader">איך קונים</span><span role="cell">נרשמים להגרלה. בהגרלה ה-11 נרשמו 114,848 משקי בית ל-7,922 דירות, וזכו 6.9%</span><span role="cell">פונים ליזם, בלי הגרלה</span></div>
		<div role="row"><span role="rowheader">כמה ההנחה</span><span role="cell">לא קבועה. שמאים מעריכים 20% עד 35% מתחת למחיר השוק באזורי ביקוש, ופחות בערים זולות</span><span role="cell">תלויה במבצע. המחשבון למעלה מתרגם אותה לשקלים</span></div>
		<div role="row"><span role="rowheader">מתי</span><span role="cell">על ההגרלה ה-12 עוד אין הודעה רשמית</span><span role="cell">עכשיו, כל עוד המבצע בתוקף</span></div>
	</div>
	<p>מחפשים דירות חדשות במבצע, דירות חדשות זולות או 10/90 באזור מסוים? המפה בראש העמוד מסננת לפי סוג המבצע וכמה יש לכם ביד. ואם אתם זכאים לתוכנית המדינה: <a href="/dira-behanacha/">דירה בהנחה: מי זכאי, ההגרלות והסיכוי לזכות בכל עיר</a>.</p>
</section>
		<?php
		return (string) ob_get_clean();
	}
}

add_filter( 'the_content', function ( $content ) {
	if ( ! in_the_loop() || ! is_main_query() || ! nadlan_dm_is_page() || false !== strpos( $content, 'nldm-disc' ) ) { return $content; }
	$pos = array(); $o = strpos( $content, 'id="nldm-data"' );
	$o = false === $o ? 0 : (int) strpos( $content, '</section>', $o ); // the article's headings only, after the map block
	while ( false !== ( $p = stripos( $content, '<h2', $o ) ) ) { $pos[] = $p; $o = $p + 3; }
	if ( count( $pos ) < 6 ) { return $content . nadlan_dm_discount_section(); }
	$at = $pos[ (int) floor( count( $pos ) * 0.55 ) ]; // a little past the middle of the article
	return substr( $content, 0, $at ) . nadlan_dm_discount_section() . substr( $content, $at );
}, 7 );

add_filter( 'the_content', function ( $content ) {
	$lang = nadlan_dm_lang();
	if ( ! in_the_loop() || ! is_main_query() || '' === $lang || false !== strpos( $content, 'id="nldm"' ) ) { return $content; }
	$html = 'en' === $lang ? nadlan_dm_render_en() : nadlan_dm_render();
	$at = stripos( $content, '</h1>' );
	if ( false === $at ) { return $html . $content; }
	$at += 5; // the article opens with its own h1: the map goes right under it (H1 -> answer -> CTAs -> stage)
	return substr( $content, 0, $at ) . $html . substr( $content, $at );
}, 6 );

add_action( 'wp_enqueue_scripts', function () {
	if ( '' === nadlan_dm_lang() ) { return; }
	$base = plugins_url( 'assets/deals/', dirname( __FILE__ ) );
	$dir  = dirname( __DIR__ ) . '/assets/deals/';
	wp_enqueue_style( 'nadlan-deals-map', $base . 'deals.css', array(), (string) @filemtime( $dir . 'deals.css' ) );
	wp_enqueue_script( 'nadlan-deals-map', $base . 'deals.js', array(), (string) @filemtime( $dir . 'deals.js' ), true );
} );
