<?php
/**
 * i18n engine (2026-07-03) — systematic 5-language chrome for nad-lan.co.il.
 *
 * LAW (see handoff/research/2026-07-03-multilingual-architecture.md):
 * - CHROME (nav, hero, footer, labels, switcher) is systematic: one string
 *   table per language, resolved via nadlan_i18n('key'). Change once, every
 *   surface reflects it. 'he' values equal the exact current Hebrew, so the
 *   Hebrew page renders byte-identical.
 * - CONTENT (article/news/project bodies) is NOT here — it must be real
 *   translated CMS text (generation run), never machine-faked. Until then it
 *   falls back to Hebrew with correct hreflang (no SEO penalty).
 * - SEO: distinct URL per language (/ , /en/, /fr/, /ru/, /ar/), self-canonical
 *   + bidirectional hreflang + x-default on every language page.
 * Missing keys fall back to the 'he' value (never blank, never broken).
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_langs' ) ) {
	function nadlan_langs() { return array( 'he', 'en', 'fr', 'ru', 'ar' ); }
}
if ( ! function_exists( 'nadlan_lang_names' ) ) {
	function nadlan_lang_names() { return array( 'he' => 'עברית', 'en' => 'English', 'fr' => 'Français', 'ru' => 'Русский', 'ar' => 'العربية' ); }
}
if ( ! function_exists( 'nadlan_lang_is_rtl' ) ) {
	function nadlan_lang_is_rtl( $l ) { return in_array( $l, array( 'he', 'ar' ), true ); }
}
if ( ! function_exists( 'nadlan_set_lang' ) ) {
	function nadlan_set_lang( $l ) {
		$l = in_array( $l, nadlan_langs(), true ) ? $l : 'he';
		$GLOBALS['nadlan_lang'] = $l;
	}
}
if ( ! function_exists( 'nadlan_current_lang' ) ) {
	function nadlan_current_lang() {
		return isset( $GLOBALS['nadlan_lang'] ) && in_array( $GLOBALS['nadlan_lang'], nadlan_langs(), true )
			? $GLOBALS['nadlan_lang'] : 'he';
	}
}

/* The chrome string table. Add keys here; every surface that routes through
   nadlan_i18n() reflects them in all languages automatically. */
if ( ! function_exists( 'nadlan_i18n_table' ) ) {
	function nadlan_i18n_table() {
		static $t = null;
		if ( null !== $t ) { return $t; }
		$t = array(
		'he' => array(
			// hero
			'hero_h1'   => 'מוצאים דירה, בודקים מחיר, מכירים את הסביבה - לפני שחותמים',
			'hero_sub'  => 'דירות למכירה ולהשכרה, פרויקטים חדשים עם בחירת דירה מתוך הבניין, מחירי עסקאות אמיתיים וכלי בדיקה - במקום אחד.',
			'tab_buy' => 'לקנייה', 'tab_rent' => 'להשכרה', 'tab_projects' => 'פרויקטים חדשים', 'tab_pros' => 'בעלי מקצוע',
			'search_ph' => 'עיר, שכונה, פרויקט או בעל מקצוע...', 'search_btn' => 'חיפוש',
			'trust_projects' => 'פרויקטים והתחדשות', 'trust_pros' => 'בעלי מקצוע מאומתים (gov.il)',
			'trust_calc' => 'מחשבונים מקצועיים', 'trust_law' => 'עורך דין מקרקעין', 'trust_law_pre' => 'ליווי',
			'flag_pick' => 'בחרו דירה מתוך הבניין',
			// browse nav
			'nav_label' => 'ניווט ראשי באתר',
			'm_apts' => 'דירות', 'apts_sale' => 'דירות למכירה', 'apts_rent' => 'דירות להשכרה', 'apts_in' => 'דירות ב', 'post_free' => 'פרסום דירה חינם',
			'm_projects' => 'פרויקטים חדשים', 'all_projects' => 'כל הפרויקטים', 'projects_in' => 'פרויקטים ב', 'pinui' => 'פינוי-בינוי', 'tama' => 'תמ״א 38',
			'm_prices' => 'מחירים ונתונים', 'my_value' => 'כמה שווה הדירה שלי', 'prices_in' => 'מחירים ב',
			'm_guides' => 'מדריכים וכלים', 'calc_mortgage' => 'מחשבון משכנתא', 'calc_tax' => 'מחשבון מס רכישה', 'calc_full' => 'עלות עסקה מלאה',
			'value' => 'שווי דירה', 'buying_guide' => 'קניית דירה: המדריך', 'tabu' => 'בדיקת נסח טאבו', 'invest' => 'נדל״ן להשקעה', 'glossary' => 'מילון מונחים',
			'm_pros' => 'אנשי מקצוע', 'all_pros' => 'כל המאגר', 'join_dir' => 'הצטרפות למאגר',
			// switcher / generic
			'lang_label' => 'שפה', 'content_he_note' => 'התוכן המלא מוצג בעברית; תרגום מלא בקרוב.',
		),
		'en' => array(
			'hero_h1'   => 'Find an apartment, check the price, know the area — before you sign',
			'hero_sub'  => 'Apartments for sale and rent, new projects where you pick your apartment from inside the building, real transaction prices and check-it-yourself tools — in one place.',
			'tab_buy' => 'Buy', 'tab_rent' => 'Rent', 'tab_projects' => 'New projects', 'tab_pros' => 'Professionals',
			'search_ph' => 'City, neighborhood, project or professional…', 'search_btn' => 'Search',
			'trust_projects' => 'projects & urban renewal', 'trust_pros' => 'verified professionals (gov.il)',
			'trust_calc' => 'professional calculators', 'trust_law' => 'real-estate lawyer', 'trust_law_pre' => 'guided by a',
			'flag_pick' => 'Choose an apartment from inside the building',
			'nav_label' => 'Main site navigation',
			'm_apts' => 'Apartments', 'apts_sale' => 'For sale', 'apts_rent' => 'For rent', 'apts_in' => 'Apartments in ', 'post_free' => 'Post a listing free',
			'm_projects' => 'New projects', 'all_projects' => 'All projects', 'projects_in' => 'Projects in ', 'pinui' => 'Evacuate-rebuild', 'tama' => 'TAMA 38',
			'm_prices' => 'Prices & data', 'my_value' => "What's my home worth", 'prices_in' => 'Prices in ',
			'm_guides' => 'Guides & tools', 'calc_mortgage' => 'Mortgage calculator', 'calc_tax' => 'Purchase-tax calculator', 'calc_full' => 'Full deal cost',
			'value' => 'Home value', 'buying_guide' => 'Buying a home: the guide', 'tabu' => 'Land-registry check', 'invest' => 'Real-estate investment', 'glossary' => 'Glossary',
			'm_pros' => 'Professionals', 'all_pros' => 'Full directory', 'join_dir' => 'Join the directory',
			'lang_label' => 'Language', 'content_he_note' => 'Full content is shown in Hebrew; complete translation coming soon.',
		),
		'fr' => array(
			'hero_h1'   => 'Trouvez un appartement, vérifiez le prix, connaissez le quartier — avant de signer',
			'hero_sub'  => 'Appartements à vendre et à louer, projets neufs où vous choisissez votre appartement depuis le bâtiment, prix de transactions réels et outils de vérification — au même endroit.',
			'tab_buy' => 'Acheter', 'tab_rent' => 'Louer', 'tab_projects' => 'Projets neufs', 'tab_pros' => 'Professionnels',
			'search_ph' => 'Ville, quartier, projet ou professionnel…', 'search_btn' => 'Rechercher',
			'trust_projects' => 'projets & renouvellement urbain', 'trust_pros' => 'professionnels vérifiés (gov.il)',
			'trust_calc' => 'calculateurs professionnels', 'trust_law' => 'avocat immobilier', 'trust_law_pre' => 'accompagné par un',
			'flag_pick' => "Choisissez un appartement depuis le bâtiment",
			'nav_label' => 'Navigation principale',
			'm_apts' => 'Appartements', 'apts_sale' => 'À vendre', 'apts_rent' => 'À louer', 'apts_in' => 'Appartements à ', 'post_free' => 'Publier une annonce gratuite',
			'm_projects' => 'Projets neufs', 'all_projects' => 'Tous les projets', 'projects_in' => 'Projets à ', 'pinui' => 'Démolition-reconstruction', 'tama' => 'TAMA 38',
			'm_prices' => 'Prix & données', 'my_value' => 'Valeur de mon bien', 'prices_in' => 'Prix à ',
			'm_guides' => 'Guides & outils', 'calc_mortgage' => 'Calculateur de prêt', 'calc_tax' => "Calculateur de taxe d'achat", 'calc_full' => "Coût total de l'opération",
			'value' => 'Valeur du bien', 'buying_guide' => 'Acheter un bien : le guide', 'tabu' => 'Vérification cadastrale', 'invest' => 'Investissement immobilier', 'glossary' => 'Glossaire',
			'm_pros' => 'Professionnels', 'all_pros' => 'Annuaire complet', 'join_dir' => "Rejoindre l'annuaire",
			'lang_label' => 'Langue', 'content_he_note' => 'Le contenu complet est en hébreu ; traduction complète à venir.',
		),
		'ru' => array(
			'hero_h1'   => 'Найдите квартиру, проверьте цену, узнайте район — до подписания',
			'hero_sub'  => 'Квартиры на продажу и в аренду, новые проекты с выбором квартиры прямо из здания, реальные цены сделок и инструменты проверки — в одном месте.',
			'tab_buy' => 'Купить', 'tab_rent' => 'Аренда', 'tab_projects' => 'Новые проекты', 'tab_pros' => 'Специалисты',
			'search_ph' => 'Город, район, проект или специалист…', 'search_btn' => 'Поиск',
			'trust_projects' => 'проектов и реновации', 'trust_pros' => 'проверенных специалистов (gov.il)',
			'trust_calc' => 'профессиональных калькулятора', 'trust_law' => 'юрист по недвижимости', 'trust_law_pre' => 'сопровождение —',
			'flag_pick' => 'Выберите квартиру прямо из здания',
			'nav_label' => 'Основная навигация',
			'm_apts' => 'Квартиры', 'apts_sale' => 'Продажа', 'apts_rent' => 'Аренда', 'apts_in' => 'Квартиры в ', 'post_free' => 'Разместить объявление бесплатно',
			'm_projects' => 'Новые проекты', 'all_projects' => 'Все проекты', 'projects_in' => 'Проекты в ', 'pinui' => 'Снос-застройка', 'tama' => 'ТАМА 38',
			'm_prices' => 'Цены и данные', 'my_value' => 'Сколько стоит моя квартира', 'prices_in' => 'Цены в ',
			'm_guides' => 'Гиды и инструменты', 'calc_mortgage' => 'Ипотечный калькулятор', 'calc_tax' => 'Калькулятор налога на покупку', 'calc_full' => 'Полная стоимость сделки',
			'value' => 'Стоимость жилья', 'buying_guide' => 'Покупка жилья: гид', 'tabu' => 'Проверка в земельном реестре', 'invest' => 'Инвестиции в недвижимость', 'glossary' => 'Глоссарий',
			'm_pros' => 'Специалисты', 'all_pros' => 'Весь каталог', 'join_dir' => 'Присоединиться к каталогу',
			'lang_label' => 'Язык', 'content_he_note' => 'Полный контент показан на иврите; полный перевод скоро.',
		),
		'ar' => array(
			'hero_h1'   => 'اعثر على شقة، تحقق من السعر، اعرف الحي — قبل التوقيع',
			'hero_sub'  => 'شقق للبيع والإيجار، مشاريع جديدة تختار فيها شقتك من داخل المبنى، أسعار صفقات حقيقية وأدوات فحص — في مكان واحد.',
			'tab_buy' => 'شراء', 'tab_rent' => 'إيجار', 'tab_projects' => 'مشاريع جديدة', 'tab_pros' => 'مختصون',
			'search_ph' => 'مدينة، حي، مشروع أو مختص…', 'search_btn' => 'بحث',
			'trust_projects' => 'مشاريع وتجديد حضري', 'trust_pros' => 'مختصون موثّقون (gov.il)',
			'trust_calc' => 'حاسبات مهنية', 'trust_law' => 'محامي عقارات', 'trust_law_pre' => 'بمرافقة',
			'flag_pick' => 'اختر شقة من داخل المبنى',
			'nav_label' => 'التنقل الرئيسي',
			'm_apts' => 'شقق', 'apts_sale' => 'للبيع', 'apts_rent' => 'للإيجار', 'apts_in' => 'شقق في ', 'post_free' => 'أضف إعلاناً مجاناً',
			'm_projects' => 'مشاريع جديدة', 'all_projects' => 'كل المشاريع', 'projects_in' => 'مشاريع في ', 'pinui' => 'هدم وإعادة بناء', 'tama' => 'تاما 38',
			'm_prices' => 'الأسعار والبيانات', 'my_value' => 'كم تساوي شقتي', 'prices_in' => 'الأسعار في ',
			'm_guides' => 'أدلة وأدوات', 'calc_mortgage' => 'حاسبة الرهن', 'calc_tax' => 'حاسبة ضريبة الشراء', 'calc_full' => 'التكلفة الكاملة للصفقة',
			'value' => 'قيمة العقار', 'buying_guide' => 'شراء شقة: الدليل', 'tabu' => 'فحص سجل الطابو', 'invest' => 'استثمار عقاري', 'glossary' => 'مسرد المصطلحات',
			'm_pros' => 'مختصون', 'all_pros' => 'الدليل الكامل', 'join_dir' => 'انضم إلى الدليل',
			'lang_label' => 'اللغة', 'content_he_note' => 'المحتوى الكامل معروض بالعبرية؛ الترجمة الكاملة قريباً.',
		),
		);
		return $t;
	}
}

if ( ! function_exists( 'nadlan_i18n' ) ) {
	function nadlan_i18n( $key, $lang = null ) {
		$lang = $lang ? $lang : nadlan_current_lang();
		$t = nadlan_i18n_table();
		if ( isset( $t[ $lang ][ $key ] ) ) { return $t[ $lang ][ $key ]; }
		if ( isset( $t['he'][ $key ] ) ) { return $t['he'][ $key ]; } // honest fallback
		return $key;
	}
}
if ( ! function_exists( 'nadlan_e' ) ) {
	function nadlan_e( $key, $lang = null ) { echo esc_html( nadlan_i18n( $key, $lang ) ); }
}

/* Language -> homepage URL (subdirectories; Hebrew at root). */
if ( ! function_exists( 'nadlan_home_urls' ) ) {
	function nadlan_home_urls() {
		return array(
			'he' => home_url( '/' ), 'en' => home_url( '/en/' ), 'fr' => home_url( '/fr/' ),
			'ru' => home_url( '/ru/' ), 'ar' => home_url( '/ar/' ),
		);
	}
}

/* The switcher (chrome). Links to real language URLs (crawlable), JS optional. */
if ( ! function_exists( 'nadlan_lang_switcher' ) ) {
	function nadlan_lang_switcher() {
		$cur   = nadlan_current_lang();
		$urls  = nadlan_home_urls();
		$names = nadlan_lang_names();
		$out   = '<div class="nlhv2-langs" role="navigation" aria-label="' . esc_attr( nadlan_i18n( 'lang_label' ) ) . '">';
		foreach ( nadlan_langs() as $l ) {
			$out .= '<a href="' . esc_url( $urls[ $l ] ) . '" hreflang="' . esc_attr( $l ) . '"'
				. ( $l === $cur ? ' class="on" aria-current="true"' : '' ) . '>' . esc_html( $names[ $l ] ) . '</a>';
		}
		return $out . '</div>';
	}
}

/* Detect the language homepage EARLY (before wp_head) from the page slug, so
   hreflang/canonical emit correctly and the whole page renders in that language.
   /en/ /fr/ /ru/ /ar/ are the language homepages; / (Hebrew) is the default. */
add_action( 'wp', function () {
	if ( is_admin() || ! is_page() ) { return; }
	$slug = get_post_field( 'post_name', get_queried_object_id() );
	if ( in_array( $slug, array( 'en', 'fr', 'ru', 'ar' ), true ) ) {
		nadlan_set_lang( $slug );
		$GLOBALS['nadlan_is_lang_home'] = true;
	}
} );

/* SEO head: self-canonical + bidirectional hreflang + x-default, for the
   homepage language cluster only (front page or a language homepage). */
if ( ! function_exists( 'nadlan_is_language_home' ) ) {
	function nadlan_is_language_home() {
		return isset( $GLOBALS['nadlan_is_lang_home'] ) && $GLOBALS['nadlan_is_lang_home'];
	}
}
add_action( 'wp_head', function () {
	if ( ! is_front_page() && ! nadlan_is_language_home() ) { return; }
	$urls = nadlan_home_urls();
	$cur  = nadlan_current_lang();
	// Language pages are frame-translated but not yet content-complete (theme
	// header/footer + content bodies await the translation run). Keep them out
	// of Google until complete so we never get a duplicate/thin-content penalty.
	// Flip option nadlan_i18n_complete to '1' when a language is fully done.
	if ( 'he' !== $cur && '1' !== get_option( 'nadlan_i18n_complete', '' ) ) {
		echo "<meta name=\"robots\" content=\"noindex,follow\">\n";
	}
	echo "\n<link rel=\"canonical\" href=\"" . esc_url( $urls[ $cur ] ) . "\">\n";
	foreach ( nadlan_langs() as $l ) {
		printf( "<link rel=\"alternate\" hreflang=\"%s\" href=\"%s\">\n", esc_attr( $l ), esc_url( $urls[ $l ] ) );
	}
	printf( "<link rel=\"alternate\" hreflang=\"x-default\" href=\"%s\">\n", esc_url( $urls['he'] ) );
}, 1 );
