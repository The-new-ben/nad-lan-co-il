<?php
/**
 * ProjectShell (HAD-794, package 3 of the film gaps, 19.11.2026): every buyer capability on every project page, in every
 * language, as shared components. Design board: https://claude.ai/artifact/VdA956RZtEthDSgziFSJTW
 *
 *  1. Four more projects join the fleet's stage shell (inc/project-stage.php) through the 'nadlan_ps_config' filter, on the
 *     ONE shared massing stage (assets/project-stage/massing/massing.js; each project's folder holds only its data and its
 *     poster): H Infinity, FIRST Sde Dov, Gindi Vogue, Einstein Tower. The bridge gives them what Rainbow has: the view from
 *     a floor, the beam on the area map, WhatsApp, the designer. Every fact below is the page's own published fact table
 *     (Merkaz HaNadlan, ice, the company's report), shortened; nothing is added. On a language page the entry is written in
 *     that language (the stage's translator only knows the older pages' words).
 *  2. One action row on every developer project page (a Latin slug: the urban-renewal compounds are not showrooms), right
 *     after the page's buttons: a live video call now (the designer's LiveKit call, package 2's address
 *     /tour/designer/?project=&call=1&lang=; a page with its own live room keeps it), the apartment designer for this
 *     project, the project's film where the page has none, the 360 inside the apartment where the page has one, and an empty
 *     slot that package 4's basket fills (data-nl-slot="basket"). Server-side, inside the page's HTML, so nothing jumps.
 *  3. The hero's "video call with a representative" opens one sheet: now (live) or book a time (the page's scheduler).
 *
 * Never on: the frozen engine (engine.js) and the beam (bridge.js draws it; untouched). No text of Ashira's is changed and
 * its order stays; it only gets the row (owner, 19.11.2026: approved).
 *
 * @package nadlan-config
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_sh_page' ) ) {
	/** The current project page: array( id, slug, base, lang ) or null. */
	function nadlan_sh_page() {
		static $memo = false;
		if ( false !== $memo ) { return $memo; }
		$memo = null;
		if ( is_admin() || ! is_singular( 'nadlan_project' ) ) { return $memo; }
		$id   = (int) get_queried_object_id();
		$slug = (string) get_post_field( 'post_name', $id );
		if ( '' === $slug || ! preg_match( '/^[a-z0-9-]+$/', $slug ) ) { return $memo; } // urban-renewal compounds carry Hebrew slugs
		$base = $slug;
		$lang = 'he';
		if ( preg_match( '/^(.+)-(en|fr|ru|ar)$/', $slug, $m ) ) { $base = $m[1]; $lang = $m[2]; }
		$memo = array( 'id' => $id, 'slug' => $slug, 'base' => $base, 'lang' => $lang );
		return $memo;
	}
}

if ( ! function_exists( 'nadlan_sh_words' ) ) {
	function nadlan_sh_words( $lang ) {
		$w = array(
			'he' => array( 'rent' => 'השכרה אחרי המסירה', 'ask' => 'שאלות של קונים', 'call' => 'שיחת וידאו עכשיו', 'design' => 'לעצב את הדירה', 'film' => 'סרטון הפרויקט', 'tour' => 'סיור 360 בדירה', 'row' => 'כלים לפרויקט', 'now_k' => 'שיחה ישירה מהעמוד', 'now_h' => 'שיחת וידאו על %s', 'now_p' => 'רואים יחד את המגדל, הקומה ותוכנית הדירה. אפשר להזמין בן או בת זוג, מעצבת או מהנדס בקישור.', 'now_go' => 'להתחיל שיחה עכשיו', 'book' => 'לקבוע מועד', 'close' => 'סגירה', 'note' => 'אין הקלטה. הנציג מצטרף לחדר ברגע שהוא פנוי.', 'film_lang' => 'באנגלית, עם כתוביות' ),
			'en' => array( 'rent' => 'Rent it out after handover', 'ask' => 'Buyers’ questions', 'call' => 'Video call now', 'design' => 'Design the apartment', 'film' => 'Project film', 'tour' => '360 inside the apartment', 'row' => 'Project tools', 'now_k' => 'Straight from this page', 'now_h' => 'Video call about %s', 'now_p' => 'See the tower, the floor and the apartment plan together. Invite a partner, a designer or an engineer by link.', 'now_go' => 'Start the call now', 'book' => 'Book a time', 'close' => 'Close', 'note' => 'Nothing is recorded. A representative joins the room as soon as one is free.', 'film_lang' => 'In English' ),
			'fr' => array( 'ask' => 'Questions d’acheteurs', 'call' => 'Appel vidéo maintenant', 'design' => 'Aménager l’appartement', 'film' => 'Film du projet', 'tour' => '360 dans l’appartement', 'row' => 'Outils du projet', 'now_k' => 'Directement depuis cette page', 'now_h' => 'Appel vidéo sur %s', 'now_p' => 'Voyez ensemble la tour, l’étage et le plan. Invitez un proche, une décoratrice ou un ingénieur par lien.', 'now_go' => 'Lancer l’appel', 'book' => 'Prendre rendez-vous', 'close' => 'Fermer', 'note' => 'Aucun enregistrement. Un représentant rejoint la salle dès qu’il est libre.', 'film_lang' => 'En anglais' ),
			'ru' => array( 'ask' => 'Вопросы покупателей', 'call' => 'Видеозвонок сейчас', 'design' => 'Обустроить квартиру', 'film' => 'Фильм о проекте', 'tour' => '360 внутри квартиры', 'row' => 'Инструменты проекта', 'now_k' => 'Прямо с этой страницы', 'now_h' => 'Видеозвонок о проекте %s', 'now_p' => 'Смотрите вместе башню, этаж и планировку. Пригласите партнёра, дизайнера или инженера по ссылке.', 'now_go' => 'Начать звонок', 'book' => 'Назначить время', 'close' => 'Закрыть', 'note' => 'Без записи. Представитель присоединится, как только освободится.', 'film_lang' => 'На английском' ),
			'ar' => array( 'ask' => 'أسئلة المشترين', 'call' => 'مكالمة فيديو الآن', 'design' => 'تصميم الشقة', 'film' => 'فيلم المشروع', 'tour' => '360 داخل الشقة', 'row' => 'أدوات المشروع', 'now_k' => 'مباشرة من هذه الصفحة', 'now_h' => 'مكالمة فيديو حول %s', 'now_p' => 'شاهدوا معاً البرج والطابق ومخطط الشقة. ادعوا شريكاً أو مصممة أو مهندساً برابط.', 'now_go' => 'ابدأوا المكالمة الآن', 'book' => 'تحديد موعد', 'close' => 'إغلاق', 'note' => 'لا يوجد تسجيل. ينضم ممثل إلى الغرفة فور تفرّغه.', 'film_lang' => 'بالإنجليزية' ),
		);
		return $w[ $lang ] ?? $w['he'];
	}
}

/* ---------------------------------------------------------------------------------------------------------------------
 * 1. The four projects on the shared massing stage
 * ------------------------------------------------------------------------------------------------------------------- */
if ( ! function_exists( 'nadlan_sh_massing_config' ) ) {
	function nadlan_sh_massing_config( $lang ) {
		$lang = in_array( $lang, array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ? $lang : 'he';
		$T    = function ( $he, $en, $fr, $ru, $ar ) use ( $lang ) { $m = array( 'he' => $he, 'en' => $en, 'fr' => $fr, 'ru' => $ru, 'ar' => $ar ); return $m[ $lang ]; };
		// what lies that way, true bearings measured from each tower's coordinates to the landmarks (19.11.2026): Sde Dov
		// towers: the waterline 245-300°, Tel Baruch beach 24-28°, Ramat Aviv and the university 67-93°, Yarkon Park 117-125°,
		// the Azrieli towers 169-171°, the Old North 192°, the port 209-213°
		$sea   = $T( 'לכיוון הים', 'Toward the sea', 'Vers la mer', 'К морю', 'باتجاه البحر' );
		$north = $T( 'לכיוון תל ברוך והרצליה', 'Toward Tel Baruch and Herzliya', 'Vers Tel Baruch et Herzliya', 'К Тель-Баруху и Герцлии', 'باتجاه تل باروخ وهرتسليا' );
		$univ  = $T( 'לכיוון רמת אביב והאוניברסיטה', 'Toward Ramat Aviv and the university', 'Vers Ramat Aviv et l’université', 'К Рамат-Авиву и университету', 'باتجاه رمات أفيف والجامعة' );
		$park  = $T( 'לכיוון פארק הירקון', 'Toward Yarkon Park', 'Vers le parc HaYarkon', 'К парку Яркон', 'باتجاه حديقة اليركون' );
		$city  = $T( 'לכיוון מגדלי העיר', 'Toward the city towers', 'Vers les tours de la ville', 'К башням города', 'باتجاه أبراج المدينة' );
		$old   = $T( 'לכיוון הצפון הישן', 'Toward the Old North', 'Vers le Vieux Nord', 'К Старому Северу', 'باتجاه الشمال القديم' );
		$sdedov = array( array( 230, 345, $sea ), array( 345, 50, $north ), array( 50, 105, $univ ), array( 105, 150, $park ), array( 150, 195, $city ), array( 195, 230, $old ) );
		$units  = array( array( 'n', 11 ), array( 'e', 101 ), array( 's', 191 ), array( 'w', 281 ) );
		$src    = $T( 'מקורות הבמה: מספרי הקומות והבניינים לפי טבלת העובדות בעמוד; צורת הבניינים ומקומם במגרש להמחשה. הבניינים סביב לפי עיריית תל אביב-יפו (9.2026).',
			'Stage sources: floor and building counts per the facts table on this page; building shapes and positions are illustrative. Surrounding buildings per the Tel Aviv-Yafo municipality (9.2026).',
			'Sources : nombre d’étages et de bâtiments selon le tableau des faits de cette page ; formes et emplacements à titre d’illustration. Bâtiments alentour selon la municipalité de Tel-Aviv-Jaffa (9.2026).',
			'Источники: число этажей и зданий по таблице фактов на этой странице; форма и расположение условны. Окружающие здания по данным муниципалитета Тель-Авива-Яффо (9.2026).',
			'المصادر: عدد الطوابق والمباني حسب جدول الحقائق في هذه الصفحة؛ الأشكال والمواقع للتوضيح. المباني المحيطة حسب بلدية تل أبيب-يافا (9.2026).' );
		$base = array( 'mount' => 'mountMassingStage', 'bearing_offset' => 0, 'rail' => array(), 'units' => $units, 'src_line' => esc_html( $src ) );
		$out  = array();

		$out['h-infinity-somail-tel-aviv'] = array_merge( $base, array(
			'dir' => 'massing/h-infinity', 'name' => 'H Infinity', 'name_en' => 'H Infinity', 'developer' => $T( 'קבוצת חג׳ג׳', 'Hagag Group', 'Groupe Hagag', 'Группа Хагаг', 'مجموعة حجاج' ),
			'place' => $T( 'מתחם סומייל, תל אביב', 'Somail compound, Tel Aviv', 'Quartier Somail, Tel-Aviv', 'Квартал Сомейль, Тель-Авив', 'مجمع سوميل، تل أبيب' ),
			'poster_alt' => 'הדמיה של H Infinity: מגדל בן 52 קומות ובניין בוטיק במתחם סומייל',
			'facts' => array(
				array( 'מיקום', 'פינת אבן גבירול וז׳בוטינסקי', 'מתחם סומייל, צפון' ),
				array( 'בניינים', 'מגדל של 52 קומות', 'ובניין בוטיק מעל קומת מסחר' ),
				array( 'דירות', '278', '221 נמכרו עד 8.2026, לפי הפרסומים' ),
				array( 'קבלן', 'אלקטרה', 'אדריכל: משה צור' ),
				array( 'מתקנים', 'בריכה, ספא וכושר', 'ובר דיירים' ),
				array( 'מצב', 'ביצוע מתקדם', 'אכלוס ברבעון הראשון של 2027, להערכת החברה' ),
			),
			'progress' => array( array( 'בביצוע', 'עכשיו', 'now' ), array( 'אכלוס', 'צפוי ב-2027', 'next' ) ),
			'tower_lat' => 32.087284, 'tower_lng' => 34.78272,
			// from the tower (19.11.2026): the Old North 280° at 450 m and the sea beyond it, the port 323°, Ramat Aviv 22°,
			// Yarkon Park 63°, the Azrieli towers 149°, Rabin Square 194°
			'units' => array( array( 'n', 10 ), array( 'e', 100 ), array( 's', 190 ), array( 'w', 280 ) ),
			'sectors' => array( array( 245, 305, 'לכיוון הצפון הישן והים' ), array( 305, 345, 'לכיוון נמל תל אביב' ), array( 345, 45, 'לכיוון צפון העיר ורמת אביב' ), array( 45, 110, 'לכיוון פארק הירקון' ), array( 110, 175, 'לכיוון מגדלי העיר' ), array( 175, 245, 'לכיוון כיכר רבין ומרכז העיר' ) ),
		) );

		$out['first-sde-dov'] = array_merge( $base, array(
			'dir' => 'massing/first', 'name' => 'FIRST ' . $T( 'שדה דב', 'Sde Dov', 'Sde Dov', 'Сде-Дов', 'سدي دوف' ), 'name_en' => 'FIRST Sde Dov',
			'developer' => $T( 'קבוצת חג׳ג׳', 'Hagag Group', 'Groupe Hagag', 'Группа Хагаг', 'مجموعة حجاج' ),
			'place' => $T( 'מגרש 2270, רובע שדה דב', 'Lot 2270, Sde Dov quarter', 'Lot 2270, quartier Sde Dov', 'Участок 2270, квартал Сде-Дов', 'القسيمة 2270، حي سدي دوف' ),
			'poster_alt' => 'הדמיה של FIRST שדה דב: מגדל בן 45 קומות ושלושה בנייני בוטיק בני 9 קומות',
			'facts' => array(
				array( $T( 'מיקום', 'Location', 'Emplacement', 'Расположение', 'الموقع' ), $T( 'מגרש 2270', 'Lot 2270', 'Lot 2270', 'Участок 2270', 'القسيمة 2270' ), $T( 'מרכז רובע שדה דב', 'Centre of the Sde Dov quarter', 'Centre du quartier Sde Dov', 'Центр квартала Сде-Дов', 'وسط حي سدي دوف' ) ),
				array( $T( 'בניינים', 'Buildings', 'Bâtiments', 'Здания', 'المباني' ), $T( 'מגדל של 45 קומות', 'A 45-floor tower', 'Une tour de 45 étages', 'Башня в 45 этажей', 'برج من 45 طابقاً' ), $T( 'ושלושה בנייני בוטיק של 9 קומות', 'and three 9-floor boutique buildings', 'et trois immeubles boutique de 9 étages', 'и три бутик-здания по 9 этажей', 'وثلاثة مبانٍ بوتيك من 9 طوابق' ) ),
				array( $T( 'דירות', 'Homes', 'Logements', 'Квартиры', 'الشقق' ), '350', $T( '258 במגדל ו-92 בבנייה המרקמית', '258 in the tower, 92 in the low-rise', '258 dans la tour, 92 dans les immeubles bas', '258 в башне, 92 в малоэтажных зданиях', '258 في البرج و92 في المباني المنخفضة' ) ),
				array( $T( 'מכירות', 'Sales', 'Ventes', 'Продажи', 'المبيعات' ), $T( '155 מתוך 350', '155 of 350', '155 sur 350', '155 из 350', '155 من 350' ), $T( 'נמכרו עד 4.2026, לפי הפרסומים', 'sold by 4.2026, as published', 'vendus à 4.2026, selon les publications', 'продано к 4.2026, по публикациям', 'بيعت حتى 4.2026، حسب المنشور' ) ),
				array( $T( 'מחיר השקה', 'Launch price', 'Prix de lancement', 'Цена запуска', 'سعر الإطلاق' ), $T( 'מ-71 אלף ₪ למ״ר', 'From ₪71,000 per m²', 'Dès 71 000 ₪ le m²', 'От 71 000 ₪ за м²', 'من 71 ألف ₪ للمتر' ), $T( 'בפריסייל, 7.2025, לפי ice', 'Pre-sale, 7.2025, per ice', 'Prévente, 7.2025, selon ice', 'Предпродажа, 7.2025, по ice', 'البيع المسبق، 7.2025، حسب ice' ) ),
				array( $T( 'אדריכלות', 'Architects', 'Architectes', 'Архитекторы', 'التصميم المعماري' ), 'ODA', $T( 'ניו יורק, עם בר אוריין אדריכלים', 'New York, with Bar Orian Architects', 'New York, avec Bar Orian Architectes', 'Нью-Йорк, с Bar Orian Architects', 'نيويورك، مع بار أوريان معماريين' ) ),
			),
			'progress' => array(
				array( $T( 'מכרז הקרקע', 'Land tender', 'Appel d’offres', 'Тендер на землю', 'مناقصة الأرض' ), '2.2025', 'done' ),
				array( $T( 'פריסייל', 'Pre-sale', 'Prévente', 'Предпродажа', 'البيع المسبق' ), '7.2025', 'done' ),
				array( $T( 'שיווק', 'Marketing', 'Commercialisation', 'Продажи', 'التسويق' ), $T( 'עכשיו', 'Now', 'Maintenant', 'Сейчас', 'الآن' ), 'now' ),
			),
			'tower_lat' => 32.114141, 'tower_lng' => 34.784411, 'sectors' => $sdedov,
		) );

		$out['gindi-vogue-sde-dov'] = array_merge( $base, array(
			'dir' => 'massing/gindi-vogue', 'name' => 'GINDI VOGUE ' . $T( 'שדה דב', 'Sde Dov', 'Sde Dov', 'Сде-Дов', 'سدي دوف' ), 'name_en' => 'Gindi Vogue Sde Dov',
			'developer' => $T( 'גינדי החזקות', 'Gindi Holdings', 'Gindi Holdings', 'Gindi Holdings', 'غيندي القابضة' ),
			'place' => $T( 'מגרשים 2206 ו-2255, רובע שדה דב', 'Lots 2206 and 2255, Sde Dov quarter', 'Lots 2206 et 2255, quartier Sde Dov', 'Участки 2206 и 2255, квартал Сде-Дов', 'القسيمتان 2206 و2255، حي سدي دوف' ),
			'poster_alt' => 'הדמיה של גינדי ווג שדה דב: מגדל בן 44 קומות ובניינים של 20 ו-9 קומות',
			'facts' => array(
				array( $T( 'מיקום', 'Location', 'Emplacement', 'Расположение', 'الموقع' ), $T( 'מגרשים 2206 ו-2255', 'Lots 2206 and 2255', 'Lots 2206 et 2255', 'Участки 2206 и 2255', 'القسيمتان 2206 و2255' ), $T( 'מרכז רובע שדה דב', 'Centre of the Sde Dov quarter', 'Centre du quartier Sde Dov', 'Центр квартала Сде-Дов', 'وسط حي سدي دوف' ) ),
				array( $T( 'בניינים', 'Buildings', 'Bâtiments', 'Здания', 'المباني' ), $T( 'מגדל של 44 קומות', 'A 44-floor tower', 'Une tour de 44 étages', 'Башня в 44 этажа', 'برج من 44 طابقاً' ), $T( 'ובניינים של 20 ו-9 קומות', 'and buildings of 20 and 9 floors', 'et des immeubles de 20 et 9 étages', 'и здания в 20 и 9 этажей', 'ومبنيان من 20 و9 طوابق' ) ),
				array( $T( 'דירות', 'Homes', 'Logements', 'Квартиры', 'الشقق' ), '708', $T( '450 נמכרו בשבוע הראשון, 6.2025', '450 sold in the first week, 6.2025', '450 vendus la première semaine, 6.2025', '450 продано в первую неделю, 6.2025', 'بيعت 450 في الأسبوع الأول، 6.2025' ) ),
				array( $T( 'מחיר השקה', 'Launch price', 'Prix de lancement', 'Цена запуска', 'سعر الإطلاق' ), $T( 'מ-49 אלף ₪ למ״ר', 'From ₪49,000 per m²', 'Dès 49 000 ₪ le m²', 'От 49 000 ₪ за м²', 'من 49 ألف ₪ للمتر' ), '6.2025' ),
				array( $T( 'קבלן', 'Contractor', 'Entrepreneur', 'Подрядчик', 'المقاول' ), $T( 'דניה סיבוס', 'Danya Cebus', 'Danya Cebus', 'Danya Cebus', 'دانيا سيبوس' ), $T( 'אדריכלות: קיקה ברא״ז', 'Architect: Kika Braz', 'Architecte : Kika Braz', 'Архитектор: Кика Браз', 'المعمارية: كيكا براز' ) ),
				array( $T( 'מצב', 'Status', 'Statut', 'Статус', 'الحالة' ), $T( 'לפני ביצוע', 'Before construction', 'Avant les travaux', 'До начала строительства', 'قبل التنفيذ' ), $T( 'החברה העריכה אכלוס בעוד כ-6.5 שנים (6.2025)', 'The company estimated occupancy in about 6.5 years (6.2025)', 'La société estime la livraison dans 6,5 ans environ (6.2025)', 'Компания оценила заселение примерно через 6,5 лет (6.2025)', 'قدّرت الشركة الإسكان بعد نحو 6.5 سنوات (6.2025)' ) ),
			),
			'progress' => array(
				array( $T( 'השקה', 'Launch', 'Lancement', 'Запуск', 'الإطلاق' ), '6.2025', 'done' ),
				array( $T( 'שיווק', 'Marketing', 'Commercialisation', 'Продажи', 'التسويق' ), $T( 'עכשיו', 'Now', 'Maintenant', 'Сейчас', 'الآن' ), 'now' ),
			),
			'tower_lat' => 32.110644, 'tower_lng' => 34.783587, 'sectors' => $sdedov,
		) );

		$out['einstein-tower'] = array_merge( $base, array(
			'dir' => 'massing/einstein', 'name' => 'EINSTEIN TOWER', 'name_en' => 'Einstein Tower', 'developer' => 'קבוצת חג׳ג׳',
			'place' => 'פינת איינשטיין ולוי אשכול, רמת אביב', 'poster_alt' => 'הדמיה של EINSTEIN TOWER: מגדל בן 28 קומות ושני מבנים בני 13 קומות מעל בסיס מסחרי',
			'facts' => array(
				array( 'מיקום', 'פינת איינשטיין ולוי אשכול', 'רמת אביב, תל אביב' ),
				array( 'בניינים', 'מגדל של 28 קומות', 'ושני מבנים של 13 קומות מעל בסיס מסחרי' ),
				array( 'דירות', '215', 'ב-3 מבנים, לפי דוח החברה' ),
				array( 'היתר', '9.7.2026', 'היתר 20241734, עיריית תל אביב' ),
				array( 'מצב', 'חפירה ודיפון', 'לפי דוח החברה, 12.2025' ),
				array( 'סיום משוער', 'רבעון שלישי 2030', 'הערכת החברה, לא מועד חוזי' ),
			),
			'progress' => array( array( 'היתר', '7.2026', 'done' ), array( 'חפירה ודיפון', 'עכשיו', 'now' ), array( 'סיום', 'צפוי ב-2030', 'next' ) ),
			'tower_lat' => 32.111736, 'tower_lng' => 34.788433,
			// from the tower (19.11.2026): Tel Baruch beach 8°, Ramat Aviv 63°, the university 83°, Yarkon Park 125°, the
			// Azrieli towers 176°, the Old North 200°, the port 222°, the sea west of the Sde Dov quarter
			'sectors' => array( array( 235, 330, 'לכיוון רובע שדה דב והים' ), array( 330, 45, 'לכיוון תל ברוך והרצליה' ), array( 45, 105, 'לכיוון רמת אביב והאוניברסיטה' ), array( 105, 150, 'לכיוון פארק הירקון' ), array( 150, 195, 'לכיוון מגדלי העיר' ), array( 195, 235, 'לכיוון הצפון הישן' ) ),
		) );
		return $out;
	}
}

add_filter( 'nadlan_ps_config', function ( $all ) {
	if ( '0' === (string) get_option( 'nadlan_project_shell_stage', '1' ) ) { return $all; } // the off switch (Settings: options)
	$pg   = nadlan_sh_page();
	$lang = $pg ? $pg['lang'] : 'he';
	foreach ( nadlan_sh_massing_config( $lang ) as $slug => $cfg ) {
		if ( ! isset( $all[ $slug ] ) ) { $all[ $slug ] = $cfg; } // a hand-built stage, when one comes, always wins
	}
	return $all;
} );

/* ---------------------------------------------------------------------------------------------------------------------
 * 2. The action row and 3. the call sheet
 * ------------------------------------------------------------------------------------------------------------------- */
if ( ! function_exists( 'nadlan_sh_film' ) ) {
	/** A film for a page that shows none of its own (Ashira: the showroom film already on the server, English). */
	function nadlan_sh_film( $base ) {
		$dir = dirname( __DIR__ ) . '/assets/project-stage/';
		$map = array( 'ashira-sde-dov' => array( 'ashira/film-showroom-en.mp4', 'ashira/film-showroom-en.jpg', 'en' ) );
		if ( empty( $map[ $base ] ) || ! is_readable( $dir . $map[ $base ][0] ) ) { return null; }
		$u = plugins_url( 'assets/project-stage/', dirname( __FILE__ ) );
		return array( 'src' => $u . $map[ $base ][0], 'poster' => $u . $map[ $base ][1], 'lang' => $map[ $base ][2] );
	}
}

if ( ! function_exists( 'nadlan_sh_row' ) ) {
	function nadlan_sh_row( $pg, $html ) {
		$w     = nadlan_sh_words( $pg['lang'] );
		$name  = trim( wp_strip_all_tags( (string) get_the_title( $pg['id'] ) ) );
		$name  = preg_split( '/\s+[-–|]\s+/u', $name )[0];
		$q     = array( 'project' => $pg['base'], 'lang' => $pg['lang'] );
		$call  = add_query_arg( array_merge( $q, array( 'call' => '1' ) ), home_url( '/tour/designer/' ) );
		// a page with its own live room (the Kikar showroom's TogetherRoom) keeps it: the row's call opens that room
		if ( false !== strpos( $html, 'room=new' ) || ( false !== strpos( $html, 'nlps-page--world' ) && ( false !== strpos( $html, 'room\/available?post=' ) || false !== strpos( $html, 'room/available?post=' ) ) ) ) { $call = add_query_arg( 'room', 'new', (string) get_permalink( $pg['id'] ) ); }
		$design = add_query_arg( $q, home_url( '/tour/designer/' ) );
		$film   = false === strpos( $html, 'nlps-hero__film' ) && false === strpos( $html, 'nlfilm' ) && false === strpos( $html, 'nlpsw-film' ) ? nadlan_sh_film( $pg['base'] ) : null;
		$sched  = false !== strpos( $html, 'id="nlsch"' );
		$dir    = in_array( $pg['lang'], array( 'he', 'ar' ), true ) ? 'rtl' : 'ltr';
		$o  = '<nav class="nlsh" dir="' . $dir . '" lang="' . esc_attr( $pg['lang'] ) . '" aria-label="' . esc_attr( $w['row'] ) . '" data-project="' . esc_attr( $pg['base'] ) . '">';
		$o .= '<a class="nlsh-b nlsh-b--live" href="' . esc_url( $call ) . '" data-nlsh="call" aria-haspopup="dialog"><i class="nlsh-dot" aria-hidden="true"></i><span>' . esc_html( $w['call'] ) . '</span></a>';
		$o .= '<a class="nlsh-b" href="' . esc_url( $design ) . '" data-nlsh="design"><span>' . esc_html( $w['design'] ) . '</span></a>';
		// the film's chain (22.11.2026 loop, cycle 1): from the project to the buyers' questions about it in the forum, where the forum
		// has the project as a place (inc/pro-forum-place.php, nlfp2_places())
		$fk = 'he' === $pg['lang'] ? nadlan_sh_forum_key( $pg['base'] ) : ''; // the forum speaks Hebrew: the link stays on the Hebrew page
		if ( '' !== $fk ) {
			$o .= '<a class="nlsh-b" href="' . esc_url( add_query_arg( 'place', $fk, home_url( '/forum/' ) ) ) . '" data-nlsh="ask"><span>' . esc_html( $w['ask'] ) . '</span></a>';
		}
		// cycle 3 (22.11.2026 loop): from the project to renting the apartment out after handover, the owner's own rentals tool
		// (/my-rentals/, Hebrew and English only, like the rentals product). The site never rents out and is never a broker.
		if ( ! empty( $w['rent'] ) ) {
			$o .= '<a class="nlsh-b" href="' . esc_url( home_url( 'en' === $pg['lang'] ? '/my-rentals/?lang=en' : '/my-rentals/' ) ) . '" data-nlsh="rent"><span>' . esc_html( $w['rent'] ) . '</span></a>';
		}
		if ( $film ) {
			$o .= '<button type="button" class="nlsh-b" data-nlsh="film" data-src="' . esc_url( $film['src'] ) . '" data-poster="' . esc_url( $film['poster'] ) . '"><i class="nlsh-play" aria-hidden="true"></i><span>' . esc_html( $w['film'] ) . '</span>' . ( $film['lang'] !== $pg['lang'] ? ' <small>' . esc_html( $w['film_lang'] ) . '</small>' : '' ) . '</button>';
		}
		$o .= '<button type="button" class="nlsh-b" data-nlsh="tour" hidden><span>' . esc_html( $w['tour'] ) . '</span></button>';
		$o .= '<div class="nlsh-slot" data-nl-slot="basket" data-project="' . esc_attr( $pg['base'] ) . '" data-lang="' . esc_attr( $pg['lang'] ) . '" data-unit=""></div>';
		$o .= '</nav>';
		// the sheet: now (live) or a booked time (the page's scheduler, when it has one)
		$o .= '<dialog class="nlsh-sheet" id="nlsh-sheet" dir="' . $dir . '" lang="' . esc_attr( $pg['lang'] ) . '" aria-labelledby="nlsh-sheet-h">'
			. '<form method="dialog" class="nlsh-x"><button type="submit" aria-label="' . esc_attr( $w['close'] ) . '">&times;</button></form>'
			. '<p class="nlsh-k"><i class="nlsh-dot" aria-hidden="true"></i>' . esc_html( $w['now_k'] ) . '</p>'
			. '<h2 id="nlsh-sheet-h">' . esc_html( sprintf( $w['now_h'], $name ) ) . '</h2>'
			. '<p class="nlsh-p">' . esc_html( $w['now_p'] ) . '</p>'
			. '<a class="nlsh-go" href="' . esc_url( $call ) . '" data-nlsh="call-go">' . esc_html( $w['now_go'] ) . '</a>'
			. ( $sched ? '<a class="nlsh-book" href="#nlsch" data-nlsh="book">' . esc_html( $w['book'] ) . '</a>' : '' )
			. '<p class="nlsh-n">' . esc_html( $w['note'] ) . '</p></dialog>';
		return $o;
	}
}

if ( ! function_exists( 'nadlan_sh_forum_key' ) ) {
	/** The forum place key of a project page (inc/pro-forum-place.php), or '' when the forum does not list it as a place. */
	function nadlan_sh_forum_key( $base ) {
		$map = array( 'rainbow-tel-aviv' => 'rainbow', 'duo-tel-aviv' => 'duo', 'ashira-sde-dov' => 'ashira', 'dimri-yama-sde-dov' => 'dimri-yama',
			'h-infinity-somail-tel-aviv' => 'h-infinity', 'first-sde-dov' => 'first-sde-dov', 'gindi-vogue-sde-dov' => 'gindi-vogue',
			'einstein-tower' => 'einstein', 'hamedina' => 'hamedina' );
		$k = $map[ $base ] ?? '';
		return ( '' !== $k && function_exists( 'nlfp2_key_ok' ) && nlfp2_key_ok( $k ) ) ? $k : '';
	}
}

if ( ! function_exists( 'nadlan_sh_insert' ) ) {
	/** Puts the row right after the page's buttons (the stage hero's), else after the lead, else after the h1. */
	function nadlan_sh_insert( $html, $row ) {
		$b = strpos( $html, '<body' );
		if ( false === $b ) { return $html; }
		$at = false;
		$p  = strpos( $html, 'data-nlps-ev="hero-pick"', $b );
		if ( false === $p ) { $p = strpos( $html, 'data-nlpsw-ev="hero-', $b ); }
		if ( false !== $p && function_exists( 'nadlan_ps_close' ) ) {
			$d = strrpos( substr( $html, 0, $p ), '<div' );
			if ( false !== $d ) { $e = nadlan_ps_close( $html, $d, 'div' ); if ( $e ) { $at = $e; } }
		}
		// the stage page's buttons block (the Kikar world has no hero-pick): inside it, at its end, so the grid keeps the row in the
		// buttons' area; a direct child of .nlps-page with no grid area would fall to the end of the page (1.72.708-711 on Kikar)
		if ( false === $at && function_exists( 'nadlan_ps_close' ) ) {
			$c = strpos( $html, '<div class="nlds nlps-ctawrap"', $b );
			if ( false !== $c ) { $e = nadlan_ps_close( $html, $c, 'div' ); if ( $e ) { $at = $e - strlen( '</div>' ); } }
		}
		if ( false === $at && function_exists( 'nadlan_ps_close' ) ) {
			$l = strpos( $html, '<div class="nl-lead">', $b );
			if ( false !== $l ) { $e = nadlan_ps_close( $html, $l, 'div' ); if ( $e ) { $at = $e; } }
		}
		if ( false === $at && preg_match( '#</h1>#', $html, $m, PREG_OFFSET_CAPTURE, $b ) ) { $at = $m[0][1] + 5; }
		if ( false === $at ) { return $html; }
		return substr( $html, 0, $at ) . $row . substr( $html, $at );
	}
}

// priority -10: this buffer must open before the stage's (template_redirect priority 0, nadlan_ps_compose), so it is the outer one
// and sees the composed page last (1.72.708 opened at 5, so the row was placed before the stage moved the lead: deep in the page)
add_action( 'template_redirect', function () {
	$pg = nadlan_sh_page();
	if ( ! $pg || '0' === (string) get_option( 'nadlan_project_shell_row', '1' ) || is_feed() || post_password_required( $pg['id'] ) ) { return; }
	ob_start( function ( $html ) use ( $pg ) {
		if ( ! is_string( $html ) || '' === $html || false !== strpos( $html, 'class="nlsh"' ) || false === stripos( $html, '</html>' ) ) { return $html; }
		// one price guide per page: a page whose content already prints [nadlan_price_guide] and that now has the stage shell
		// (which adds its own above the stage) would show it twice; the first, the fleet's place, stays
		$f = strpos( $html, 'id="nlpg"' );
		$n = false !== $f ? strpos( $html, 'id="nlpg"', $f + 9 ) : false;
		if ( false !== $n && function_exists( 'nadlan_ps_close' ) ) {
			$st = strrpos( substr( $html, 0, $n ), '<section' );
			$en = false !== $st ? nadlan_ps_close( $html, $st, 'section' ) : 0;
			if ( $en ) { $html = substr( $html, 0, $st ) . substr( $html, $en ); }
		}
		return nadlan_sh_insert( $html, nadlan_sh_row( $pg, $html ) );
	} );
}, -10 );

add_action( 'wp_enqueue_scripts', function () {
	$pg = nadlan_sh_page();
	if ( ! $pg || '0' === (string) get_option( 'nadlan_project_shell_row', '1' ) ) { return; }
	$v    = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1';
	$base = plugins_url( 'assets/project-shell/', dirname( __FILE__ ) );
	wp_enqueue_style( 'nadlan-project-shell', $base . 'shell.css', array(), $v );
	wp_enqueue_script( 'nadlan-project-shell', $base . 'shell.js', array(), $v, true );
	if ( function_exists( 'wp_script_add_data' ) ) { wp_script_add_data( 'nadlan-project-shell', 'strategy', 'defer' ); }
}, 40 );
