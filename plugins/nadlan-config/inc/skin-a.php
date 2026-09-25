<?php
/* x-skin-a v1.4 (3.9.2026: concept page availability chip hidden; original product bands kept on the new home; /en /fr /ru /ar homes share the renderer through a string table; 2.9.2026, owner GO "לך") - Direction A skin behind a switch.
 * Preview: ?skin=a sets cookie nl_skin=a (7 days); ?skin=off clears. Global: option nadlan_skin_a = 'all'.
 * Skinned responses are never page-cached (LiteSpeed no-cache) until the global switch is on.
 * Additive: no URL, menu, schema or content change. The homepage gets a new renderer that REUSES the
 * existing home-v2 bands (mega nav, listings, areas, magazine, pros, megafooter) plus a new hero and
 * a real-projects band. Aurelia Sports (7514) is never listed on the front. Rollback: deactivate snippet. */

if ( ! function_exists( 'nadlan_skin_a_on' ) ) {
	function nadlan_skin_a_on() {
		static $on = null;
		if ( null !== $on ) { return $on; }
		if ( is_admin() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) { return $on = false; }
		if ( 'all' === get_option( 'nadlan_skin_a', '' ) ) { return $on = true; }
		$q = isset( $_GET['skin'] ) ? sanitize_key( wp_unslash( $_GET['skin'] ) ) : '';
		if ( 'a' === $q ) { return $on = true; }
		if ( 'off' === $q ) { return $on = false; }
		return $on = ( isset( $_COOKIE['nl_skin'] ) && 'a' === $_COOKIE['nl_skin'] );
	}
}

add_action( 'init', function () {
	if ( is_admin() ) { return; }
	$q = isset( $_GET['skin'] ) ? sanitize_key( wp_unslash( $_GET['skin'] ) ) : '';
	if ( 'a' === $q && ! headers_sent() ) { setcookie( 'nl_skin', 'a', time() + 7 * DAY_IN_SECONDS, '/', '', is_ssl(), true ); }
	if ( 'off' === $q && ! headers_sent() ) { setcookie( 'nl_skin', '', time() - 3600, '/', '', is_ssl(), true ); }
}, 1 );

/* never let a preview-skinned page land in the shared page cache */
add_action( 'template_redirect', function () {
	if ( ! nadlan_skin_a_on() || 'all' === get_option( 'nadlan_skin_a', '' ) ) { return; }
	do_action( 'litespeed_control_set_nocache', 'nadlan skin preview' );
	if ( ! headers_sent() ) { header( 'X-LiteSpeed-Cache-Control: no-cache' ); header( 'X-NL-Skin: a-preview' ); }
}, 0 );

add_filter( 'body_class', function ( $c ) {
	if ( nadlan_skin_a_on() ) { $c[] = 'nl-skin-a'; }
	return $c;
} );

add_action( 'wp_enqueue_scripts', function () {
	if ( ! nadlan_skin_a_on() ) { return; }
	$up  = wp_get_upload_dir();
	$css = trailingslashit( $up['baseurl'] ) . 'nadlan-skin/skin-a.css';
	$ver = (string) get_option( 'nadlan_skin_a_ver', '1' );
	wp_enqueue_style( 'nadlan-skin-fonts', 'https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@500;600;700&family=Assistant:wght@300;400;600;700&display=swap', array(), null );
	wp_enqueue_style( 'nadlan-skin-a', $css, array( 'nadlan-skin-fonts' ), $ver );
}, 9999 );

add_action( 'wp_head', function () {
	if ( ! nadlan_skin_a_on() ) { return; }
	echo '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\n";
}, 1 );

/* ------------------------------------------------------------------ homepage */
if ( ! function_exists( 'nadlan_skin_a_hero_img' ) ) {
	function nadlan_skin_a_hero_img( $lang = 'he' ) {
		$s   = nadlan_skin_a_strings( $lang );
		$own = trim( (string) get_option( 'nadlan_home_hero_aerial', '' ) );
		if ( $own ) { return array( $own, $s['hero_cap_own'] ); }
		$up = wp_get_upload_dir();
		return array( trailingslashit( $up['baseurl'] ) . 'nadlan-skin/hero-tel-aviv-coast.jpg', $s['hero_cap'] );
	}
}

if ( ! function_exists( 'nadlan_skin_a_strings' ) ) {
	/** Portal copy per language (owner law: chrome strings from one table; body content from real translated pages). */
	function nadlan_skin_a_strings( $lang = 'he' ) {
		static $t = null;
		if ( null === $t ) {
			$t = array(
			'he' => array(
				'aria_search' => 'חיפוש נדל"ן', 'kicker' => 'לוח נדל"ן · פרויקטים חדשים · דירות מקבלן · מחירי דירות',
				'h1' => 'פרויקטים חדשים, דירות למכירה ומחירי דירות בכל הארץ',
				'sub' => 'פורטל הנדל"ן של ישראל: כל הפרויקטים החדשים מקבלן, דירות למכירה ולהשכרה, מחירי דירות לפי עיר ושכונה, מחשבון משכנתא ומס רכישה, ומגזין נדל"ן לרוכשים.',
				'tab_projects' => 'פרויקטים חדשים', 'tab_sale' => 'למכירה', 'tab_rent' => 'להשכרה', 'tab_pros' => 'אנשי מקצוע',
				'ph' => 'עיר, שכונה, רחוב או פרויקט', 'search' => 'חיפוש',
				'quick' => array( 'פרויקטים חדשים בתל אביב', 'פרויקטים חדשים בכל הארץ', 'פרויקטים חדשים בשדה דב', 'מחירי דירות בתל אביב', 'דירות למכירה' ),
				'hero_alt' => 'קו החוף של תל אביב', 'hero_cap' => 'קו החוף של תל אביב · צילום אווירה', 'hero_cap_own' => 'צילום אווירה',
				'b1_k' => 'פרויקטים חדשים', 'b1_h' => 'פרויקטים חדשים בתל אביב', 'b1_more' => 'לכל הפרויקטים החדשים',
				'card_k' => 'פרויקט חדש', 'card_cap' => 'הדמיה להמחשה', 'card_link' => 'עוד על הפרויקט',
				'b2_k' => 'מחירי דירות ומחשבונים', 'b2_h' => 'מחירי דירות, מחשבון משכנתא ומס רכישה', 'b2_more' => 'לכל המחשבונים',
				'tools' => array(
					array( 'מחירי דירות שנמכרו', 'עסקאות נדל"ן אחרונות ומחיר למטר לפי עיר, שכונה ורחוב.' ),
					array( 'מחשבון משכנתא', 'החזר חודשי, הון עצמי ותקרת מימון לפי הוראות בנק ישראל.' ),
					array( 'מחשבון מס רכישה', 'מס רכישה לדירה יחידה, דירה נוספת ומשקיעים, לפי מדרגות המס.' ),
					array( 'הערכת שווי דירה', 'שווי דירה לפי עסקאות נדל"ן באזור, עם המקורות.' ),
				),
				'b3_k' => 'עוד בנדלן', 'b3_h' => 'סיורים, מפה, השכרה והתחדשות עירונית',
				'more' => array( 'סיורים בפרויקטים', 'קטלוג תלת ממד', 'התחדשות עירונית', 'דירות להשכרה', 'נדל"ן בחו"ל', 'נדל"ן מסחרי', 'מילון נדל"ן' ),
				'status' => array( 'construction' => 'בבנייה', 'marketing' => 'בשיווק', 'planning' => 'בתכנון', 'occupied' => 'מאוכלס' ),
			),
			'en' => array(
				'aria_search' => 'Real estate search', 'kicker' => 'Real estate portal · New projects · Apartments from developers · Apartment prices',
				'h1' => 'New projects, apartments for sale and apartment prices across Israel',
				'sub' => "Israel's real estate portal: every new project from developers, apartments for sale and rent, apartment prices by city and neighbourhood, mortgage and purchase-tax calculators, and a real estate magazine for buyers.",
				'tab_projects' => 'New projects', 'tab_sale' => 'For sale', 'tab_rent' => 'For rent', 'tab_pros' => 'Professionals',
				'ph' => 'City, neighbourhood, street or project', 'search' => 'Search',
				'quick' => array( 'New projects in Tel Aviv', 'New projects across Israel', 'New projects in Sde Dov', 'Apartment prices in Tel Aviv', 'Apartments for sale' ),
				'hero_alt' => 'Tel Aviv coastline', 'hero_cap' => 'Tel Aviv coastline · ambience photo', 'hero_cap_own' => 'Ambience photo',
				'b1_k' => 'New projects', 'b1_h' => 'New projects in Tel Aviv', 'b1_more' => 'All new projects',
				'card_k' => 'New project', 'card_cap' => "Artist's impression", 'card_link' => 'About the project',
				'b2_k' => 'Apartment prices and calculators', 'b2_h' => 'Apartment prices, mortgage and purchase-tax calculators', 'b2_more' => 'All calculators',
				'tools' => array(
					array( 'Sold apartment prices', 'Recent real estate transactions and price per square metre by city, neighbourhood and street.' ),
					array( 'Mortgage calculator', 'Monthly repayment, equity and financing cap under Bank of Israel rules.' ),
					array( 'Purchase tax calculator', 'Purchase tax for a first apartment, an additional apartment and investors, by tax bracket.' ),
					array( 'Apartment valuation', 'Apartment value based on real estate transactions in the area, with sources.' ),
				),
				'b3_k' => 'More on NadLan', 'b3_h' => 'Tours, map, rentals and urban renewal',
				'more' => array( 'Project tours', '3D catalogue', 'Urban renewal', 'Apartments for rent', 'Real estate abroad', 'Commercial real estate', 'Real estate glossary' ),
				'status' => array( 'construction' => 'Under construction', 'marketing' => 'Now selling', 'planning' => 'In planning', 'occupied' => 'Occupied' ),
			),
			'fr' => array(
				'aria_search' => 'Recherche immobilière', 'kicker' => 'Portail immobilier · Projets neufs · Appartements de promoteur · Prix des appartements',
				'h1' => 'Projets neufs, appartements à vendre et prix des appartements dans tout Israël',
				'sub' => "Le portail immobilier d'Israël : tous les projets neufs de promoteurs, appartements à vendre et à louer, prix des appartements par ville et quartier, simulateurs de crédit immobilier et de taxe d'acquisition, et un magazine immobilier pour les acheteurs.",
				'tab_projects' => 'Projets neufs', 'tab_sale' => 'À vendre', 'tab_rent' => 'À louer', 'tab_pros' => 'Professionnels',
				'ph' => 'Ville, quartier, rue ou projet', 'search' => 'Rechercher',
				'quick' => array( 'Projets neufs à Tel Aviv', 'Projets neufs dans tout Israël', 'Projets neufs à Sde Dov', 'Prix des appartements à Tel Aviv', 'Appartements à vendre' ),
				'hero_alt' => 'Littoral de Tel Aviv', 'hero_cap' => "Littoral de Tel Aviv · photo d'ambiance", 'hero_cap_own' => "Photo d'ambiance",
				'b1_k' => 'Projets neufs', 'b1_h' => 'Projets neufs à Tel Aviv', 'b1_more' => 'Tous les projets neufs',
				'card_k' => 'Projet neuf', 'card_cap' => "Image d'illustration", 'card_link' => 'En savoir plus sur le projet',
				'b2_k' => 'Prix des appartements et simulateurs', 'b2_h' => "Prix des appartements, crédit immobilier et taxe d'acquisition", 'b2_more' => 'Tous les simulateurs',
				'tools' => array(
					array( 'Prix des appartements vendus', 'Transactions immobilières récentes et prix au mètre carré par ville, quartier et rue.' ),
					array( 'Simulateur de crédit immobilier', "Mensualité, apport personnel et plafond de financement selon les règles de la Banque d'Israël." ),
					array( "Simulateur de taxe d'acquisition", "Taxe d'acquisition pour un premier appartement, un appartement supplémentaire et les investisseurs, par tranche." ),
					array( "Estimation d'appartement", "Valeur d'un appartement d'après les transactions immobilières du secteur, sources à l'appui." ),
				),
				'b3_k' => 'Plus sur NadLan', 'b3_h' => 'Visites, carte, location et rénovation urbaine',
				'more' => array( 'Visites de projets', 'Catalogue 3D', 'Rénovation urbaine', 'Appartements à louer', "Immobilier à l'étranger", 'Immobilier commercial', 'Lexique immobilier' ),
				'status' => array( 'construction' => 'En construction', 'marketing' => 'En commercialisation', 'planning' => 'En planification', 'occupied' => 'Livré' ),
			),
			'ru' => array(
				'aria_search' => 'Поиск недвижимости', 'kicker' => 'Портал недвижимости · Новостройки · Квартиры от застройщика · Цены на квартиры',
				'h1' => 'Новостройки, квартиры на продажу и цены на квартиры по всему Израилю',
				'sub' => 'Портал недвижимости Израиля: все новостройки от застройщиков, квартиры на продажу и в аренду, цены на квартиры по городам и районам, ипотечный калькулятор и калькулятор налога на покупку, а также журнал о недвижимости для покупателей.',
				'tab_projects' => 'Новостройки', 'tab_sale' => 'Продажа', 'tab_rent' => 'Аренда', 'tab_pros' => 'Специалисты',
				'ph' => 'Город, район, улица или проект', 'search' => 'Поиск',
				'quick' => array( 'Новостройки в Тель-Авиве', 'Новостройки по всему Израилю', 'Новостройки в Сде-Дов', 'Цены на квартиры в Тель-Авиве', 'Квартиры на продажу' ),
				'hero_alt' => 'Побережье Тель-Авива', 'hero_cap' => 'Побережье Тель-Авива · атмосферное фото', 'hero_cap_own' => 'Атмосферное фото',
				'b1_k' => 'Новостройки', 'b1_h' => 'Новостройки в Тель-Авиве', 'b1_more' => 'Все новостройки',
				'card_k' => 'Новый проект', 'card_cap' => 'Визуализация', 'card_link' => 'Подробнее о проекте',
				'b2_k' => 'Цены на квартиры и калькуляторы', 'b2_h' => 'Цены на квартиры, ипотека и налог на покупку', 'b2_more' => 'Все калькуляторы',
				'tools' => array(
					array( 'Цены проданных квартир', 'Последние сделки с недвижимостью и цена за квадратный метр по городу, району и улице.' ),
					array( 'Ипотечный калькулятор', 'Ежемесячный платёж, собственный капитал и лимит финансирования по правилам Банка Израиля.' ),
					array( 'Калькулятор налога на покупку', 'Налог на покупку для единственной квартиры, дополнительной квартиры и инвесторов по ставкам.' ),
					array( 'Оценка стоимости квартиры', 'Стоимость квартиры по сделкам с недвижимостью в районе, с источниками.' ),
				),
				'b3_k' => 'Ещё на NadLan', 'b3_h' => 'Туры, карта, аренда и городское обновление',
				'more' => array( 'Туры по проектам', '3D-каталог', 'Городское обновление', 'Квартиры в аренду', 'Недвижимость за рубежом', 'Коммерческая недвижимость', 'Словарь недвижимости' ),
				'status' => array( 'construction' => 'Строится', 'marketing' => 'В продаже', 'planning' => 'В планировании', 'occupied' => 'Заселён' ),
			),
			'ar' => array(
				'aria_search' => 'بحث عقاري', 'kicker' => 'بوابة العقارات · مشاريع جديدة · شقق من المقاول · أسعار الشقق',
				'h1' => 'مشاريع جديدة، شقق للبيع وأسعار الشقق في جميع أنحاء البلاد',
				'sub' => 'بوابة العقارات في إسرائيل: جميع المشاريع الجديدة من المقاولين، شقق للبيع وللإيجار، أسعار الشقق حسب المدينة والحي، حاسبة الرهن العقاري وضريبة الشراء، ومجلة عقارية للمشترين.',
				'tab_projects' => 'مشاريع جديدة', 'tab_sale' => 'للبيع', 'tab_rent' => 'للإيجار', 'tab_pros' => 'أصحاب مهن',
				'ph' => 'مدينة، حي، شارع أو مشروع', 'search' => 'بحث',
				'quick' => array( 'مشاريع جديدة في تل أبيب', 'مشاريع جديدة في جميع أنحاء البلاد', 'مشاريع جديدة في سديه دوف', 'أسعار الشقق في تل أبيب', 'شقق للبيع' ),
				'hero_alt' => 'شاطئ تل أبيب', 'hero_cap' => 'شاطئ تل أبيب · صورة أجواء', 'hero_cap_own' => 'صورة أجواء',
				'b1_k' => 'مشاريع جديدة', 'b1_h' => 'مشاريع جديدة في تل أبيب', 'b1_more' => 'جميع المشاريع الجديدة',
				'card_k' => 'مشروع جديد', 'card_cap' => 'صورة توضيحية', 'card_link' => 'المزيد عن المشروع',
				'b2_k' => 'أسعار الشقق والحاسبات', 'b2_h' => 'أسعار الشقق، حاسبة الرهن العقاري وضريبة الشراء', 'b2_more' => 'جميع الحاسبات',
				'tools' => array(
					array( 'أسعار الشقق المباعة', 'أحدث صفقات العقارات وسعر المتر حسب المدينة والحي والشارع.' ),
					array( 'حاسبة الرهن العقاري', 'القسط الشهري، رأس المال الذاتي وسقف التمويل وفق تعليمات بنك إسرائيل.' ),
					array( 'حاسبة ضريبة الشراء', 'ضريبة الشراء لشقة وحيدة، شقة إضافية وللمستثمرين حسب الشرائح.' ),
					array( 'تقدير قيمة الشقة', 'قيمة الشقة حسب صفقات العقارات في المنطقة، مع المصادر.' ),
				),
				'b3_k' => 'المزيد في نادلان', 'b3_h' => 'جولات، خريطة، إيجار وتجديد حضري',
				'more' => array( 'جولات في المشاريع', 'كتالوج ثلاثي الأبعاد', 'تجديد حضري', 'شقق للإيجار', 'عقارات في الخارج', 'عقارات تجارية', 'قاموس العقارات' ),
				'status' => array( 'construction' => 'قيد البناء', 'marketing' => 'في التسويق', 'planning' => 'في التخطيط', 'occupied' => 'مأهول' ),
			),
			);
		}
		return isset( $t[ $lang ] ) ? $t[ $lang ] : $t['he'];
	}
}

if ( ! function_exists( 'nadlan_skin_a_status_label' ) ) {
	function nadlan_skin_a_status_label( $s, $lang = 'he' ) {
		$s   = trim( (string) $s );
		$key = array( 'construction' => 'construction', 'marketing' => 'marketing', 'planning' => 'planning', 'occupied' => 'occupied', 'בהקמה' => 'construction', 'בבנייה' => 'construction', 'בשיווק' => 'marketing', 'בתכנון' => 'planning', 'מאוכלס' => 'occupied' );
		$tbl = nadlan_skin_a_strings( $lang );
		if ( isset( $key[ $s ] ) ) { return $tbl['status'][ $key[ $s ] ]; }
		/* unknown free text: shown only on the Hebrew home and only if it is Hebrew; otherwise omitted (never announce unknowns) */
		return ( 'he' === $lang && preg_match( '/^[\x{0590}-\x{05FF}\s]+$/u', $s ) ) ? $s : '';
	}
}

if ( ! function_exists( 'nadlan_skin_a_projects' ) ) {
	/** Real, published, non-concept projects with a featured image. Aurelia (7514) and drafts never appear.
	 *  Language homes: first the projects that have a language sibling (/projects/<slug>-<lang>/, its title and link),
	 *  then projects whose title carries a Latin brand name (shown alone, never a Hebrew line on a foreign page). */
	function nadlan_skin_a_projects( $lang = 'he' ) {
		$prefer = array( 'rainbow-tel-aviv', 'h-infinity-somail-tel-aviv', 'six-8-herbert-samuel-tel-aviv', 'dimri-yama-sde-dov', 'ashira-sde-dov', 'einstein-tower' );
		$base = array();
		foreach ( $prefer as $slug ) {
			$p = get_page_by_path( $slug, OBJECT, 'nadlan_project' );
			if ( ! $p || 'publish' !== $p->post_status || 7514 === (int) $p->ID || ! has_post_thumbnail( $p ) ) { continue; }
			$base[ $slug ] = $p;
		}
		$out = array();
		if ( 'he' === $lang ) {
			foreach ( $base as $p ) { $out[] = array( 'post' => $p, 'link' => get_permalink( $p ), 'title' => get_the_title( $p ) ); if ( count( $out ) >= 3 ) { break; } }
			return $out;
		}
		$used = array();
		foreach ( $base as $slug => $p ) {
			$sib = get_page_by_path( $slug . '-' . $lang, OBJECT, 'nadlan_project' );
			if ( $sib && 'publish' === $sib->post_status ) { $out[] = array( 'post' => $p, 'link' => get_permalink( $sib ), 'title' => get_the_title( $sib ) ); $used[ $slug ] = 1; }
			if ( count( $out ) >= 3 ) { return $out; }
		}
		foreach ( $base as $slug => $p ) {
			if ( isset( $used[ $slug ] ) ) { continue; }
			if ( preg_match( '/[A-Za-z][A-Za-z0-9&\.\- ]{2,}[A-Za-z0-9]/', get_the_title( $p ), $m ) ) { $out[] = array( 'post' => $p, 'link' => get_permalink( $p ), 'title' => trim( $m[0] ) ); }
			if ( count( $out ) >= 3 ) { break; }
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_skin_a_home' ) ) {
	function nadlan_skin_a_home( $lang = 'he' ) {
		$s   = nadlan_skin_a_strings( $lang );
		$dir = ( function_exists( 'nadlan_lang_is_rtl' ) && ! nadlan_lang_is_rtl( $lang ) ) ? 'ltr' : 'rtl';
		list( $hero_img, $hero_cap ) = nadlan_skin_a_hero_img( $lang );
		$cities  = function_exists( 'nadlan_hv2_cities' ) ? nadlan_hv2_cities( 12 ) : array();
		$quick_u = array( '/new-projects/new-projects-tel-aviv/', '/projects/', '/sde-dov/', '/tel-aviv-apartment-prices/', '/properties/?listing_type=sale' );
		$tools_u = array( '/apartment-prices/', '/mortgage-calculator/', '/purchase-tax-calculator/', '/property-value-estimator/' );
		$tools_i = array( 'M4 20h16M6 20V9l6-5 6 5v11M10 20v-6h4v6', 'M5 3h14v18H5zM8 7h8M8 12h3M13 12h3M8 16h3M13 16h3', 'M4 18l5-6 4 3 7-9M15 6h5v5', 'M12 3l9 8h-3v9H6v-9H3zM10 20v-5h4v5' );
		$more_u  = array( '/tours/', '/premium/', '/urban-renewal/', '/properties/?listing_type=rent', '/global/', '/commercial-real-estate/', '/glossary/' );
		ob_start();
		?>
<div class="nlhv2 nlsa" dir="<?php echo esc_attr( $dir ); ?>" lang="<?php echo esc_attr( $lang ); ?>">
	<?php if ( function_exists( 'nadlan_lang_switcher' ) ) { echo '<div class="nlhv2-langbar">' . nadlan_lang_switcher() . '</div>'; } ?>
	<?php if ( function_exists( 'nadlan_hv2_band_browse' ) ) { nadlan_hv2_band_browse(); } ?>

	<section class="nlsa-hero" aria-label="<?php echo esc_attr( $s['aria_search'] ); ?>">
		<div class="nlsa-hero-copy">
			<p class="nlsa-kicker"><?php echo esc_html( $s['kicker'] ); ?></p>
			<h1><?php echo esc_html( $s['h1'] ); ?></h1>
			<p class="nlsa-sub"><?php echo esc_html( $s['sub'] ); ?></p>
			<form class="nlhv2-search nlsa-search" action="<?php echo esc_url( home_url( '/properties/' ) ); ?>" method="get" role="search">
				<div class="nlhv2-tabs" role="tablist">
					<button type="button" data-action="<?php echo esc_url( home_url( '/projects/' ) ); ?>" data-extra="" class="is-on"><?php echo esc_html( $s['tab_projects'] ); ?></button>
					<button type="button" data-action="<?php echo esc_url( home_url( '/properties/' ) ); ?>" data-extra="listing_type=sale"><?php echo esc_html( $s['tab_sale'] ); ?></button>
					<button type="button" data-action="<?php echo esc_url( home_url( '/properties/' ) ); ?>" data-extra="listing_type=rent"><?php echo esc_html( $s['tab_rent'] ); ?></button>
					<button type="button" data-action="<?php echo esc_url( home_url( '/professionals/' ) ); ?>" data-extra=""><?php echo esc_html( $s['tab_pros'] ); ?></button>
				</div>
				<div class="nlhv2-box">
					<input type="search" name="q" list="nlhv2-cities" placeholder="<?php echo esc_attr( $s['ph'] ); ?>" aria-label="<?php echo esc_attr( $s['aria_search'] ); ?>">
					<datalist id="nlhv2-cities"><?php foreach ( $cities as $c ) { echo '<option value="' . esc_attr( $c['name'] ) . '">'; } ?></datalist>
					<button type="submit"><?php echo esc_html( $s['search'] ); ?></button>
				</div>
			</form>
			<div class="nlsa-quick">
				<?php foreach ( $quick_u as $i => $u ) : ?><a href="<?php echo esc_url( home_url( $u ) ); ?>"><?php echo esc_html( $s['quick'][ $i ] ); ?></a><?php endforeach; ?>
			</div>
		</div>
		<figure class="nlsa-hero-media">
			<img src="<?php echo esc_url( $hero_img ); ?>" alt="<?php echo esc_attr( $s['hero_alt'] ); ?>" loading="eager" fetchpriority="high" width="1400" height="1049">
			<figcaption><?php echo esc_html( $hero_cap ); ?></figcaption>
		</figure>
	</section>

	<?php $projects = nadlan_skin_a_projects( $lang ); if ( $projects ) : ?>
	<section class="nlsa-band" aria-label="<?php echo esc_attr( $s['b1_k'] ); ?>">
		<header class="nlsa-head"><div><p class="nlsa-kicker"><?php echo esc_html( $s['b1_k'] ); ?></p><h2><?php echo esc_html( $s['b1_h'] ); ?></h2></div><a class="nlsa-more" href="<?php echo esc_url( home_url( '/projects/' ) ); ?>"><?php echo esc_html( $s['b1_more'] ); ?></a></header>
		<div class="nlsa-cards">
			<?php foreach ( $projects as $row ) :
				$p    = $row['post'];
				$city = '';
				if ( 'he' === $lang ) { $city = wp_get_post_terms( $p->ID, 'nadlan_city', array( 'fields' => 'names' ) ); $city = ( ! is_wp_error( $city ) && $city ) ? $city[0] : ''; }
				$stat  = nadlan_skin_a_status_label( get_post_meta( $p->ID, 'project_status', true ), $lang );
				$kick  = implode( ' · ', array_filter( array( $s['card_k'], $city, $stat ) ) );
				$title = preg_replace( '/\s+-\s+.*$/u', '', $row['title'] );
				$ex    = '';
				if ( 'he' === $lang ) {
					$ex = trim( wp_strip_all_tags( (string) $p->post_excerpt ) );
					if ( '' === $ex ) { $ex = trim( wp_strip_all_tags( strip_shortcodes( (string) $p->post_content ) ) ); }
					$ex = $ex ? wp_trim_words( $ex, 24, '…' ) : '';
				}
				?>
			<article class="nlsa-card">
				<a class="nlsa-card-media" href="<?php echo esc_url( $row['link'] ); ?>"><?php echo get_the_post_thumbnail( $p, 'large', array( 'loading' => 'lazy' ) ); ?><span class="nlsa-cap"><?php echo esc_html( $s['card_cap'] ); ?></span></a>
				<div class="nlsa-card-body">
					<span class="nlsa-kicker"><?php echo esc_html( $kick ); ?></span>
					<h3><a href="<?php echo esc_url( $row['link'] ); ?>"><?php echo esc_html( $title ); ?></a></h3>
					<?php if ( $ex ) : ?><p><?php echo esc_html( $ex ); ?></p><?php endif; ?>
					<a class="nlsa-link" href="<?php echo esc_url( $row['link'] ); ?>"><?php echo esc_html( $s['card_link'] ); ?></a>
				</div>
			</article>
			<?php endforeach; ?>
		</div>
	</section>
	<?php endif; ?>

	<?php if ( function_exists( 'nadlan_hv2_band_listings' ) ) { nadlan_hv2_band_listings(); } ?>

	<section class="nlsa-band nlsa-band--alt" aria-label="<?php echo esc_attr( $s['b2_k'] ); ?>">
		<header class="nlsa-head"><div><p class="nlsa-kicker"><?php echo esc_html( $s['b2_k'] ); ?></p><h2><?php echo esc_html( $s['b2_h'] ); ?></h2></div><a class="nlsa-more" href="<?php echo esc_url( home_url( '/mortgage-calculator/' ) ); ?>"><?php echo esc_html( $s['b2_more'] ); ?></a></header>
		<div class="nlsa-tools">
			<?php foreach ( $tools_u as $i => $u ) : ?>
			<a class="nlsa-tool" href="<?php echo esc_url( home_url( $u ) ); ?>"><span class="nlsa-ico" aria-hidden="true"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="<?php echo esc_attr( $tools_i[ $i ] ); ?>"/></svg></span><span><b><?php echo esc_html( $s['tools'][ $i ][0] ); ?></b><small><?php echo esc_html( $s['tools'][ $i ][1] ); ?></small></span></a>
			<?php endforeach; ?>
		</div>
	</section>

	<?php if ( function_exists( 'nadlan_hv2_band_areas' ) ) { nadlan_hv2_band_areas(); } ?>
	<?php if ( function_exists( 'nadlan_hv2_band_market' ) ) { nadlan_hv2_band_market(); } ?>
	<?php if ( function_exists( 'nadlan_hv2_band_magazine' ) ) { nadlan_hv2_band_magazine(); } ?>
	<?php if ( function_exists( 'nadlan_hv2_band_pros' ) ) { nadlan_hv2_band_pros(); } ?>
	<?php /* additive law: the product bands of the original home stay on the new home (renewal room, live map, tours, rentals) */ ?>
	<?php if ( function_exists( 'nadlan_hv2_band_renewal' ) ) { nadlan_hv2_band_renewal(); } ?>
	<?php if ( function_exists( 'nadlan_hv2_band_dronemap' ) ) { nadlan_hv2_band_dronemap(); } ?>
	<?php if ( function_exists( 'nadlan_hv2_band_tourvideo' ) ) { nadlan_hv2_band_tourvideo(); } ?>
	<?php if ( function_exists( 'nadlan_hv2_band_rentals' ) ) { nadlan_hv2_band_rentals(); } ?>

	<section class="nlsa-band nlsa-more-row" aria-label="<?php echo esc_attr( $s['b3_k'] ); ?>">
		<header class="nlsa-head"><div><p class="nlsa-kicker"><?php echo esc_html( $s['b3_k'] ); ?></p><h2><?php echo esc_html( $s['b3_h'] ); ?></h2></div></header>
		<div class="nlsa-morelinks">
			<?php foreach ( $more_u as $i => $u ) : ?><a href="<?php echo esc_url( home_url( $u ) ); ?>"><?php echo esc_html( $s['more'][ $i ] ); ?></a><?php endforeach; ?>
		</div>
	</section>

	<?php if ( function_exists( 'nadlan_hv2_band_intl' ) ) { nadlan_hv2_band_intl(); } ?>
	<?php if ( function_exists( 'nadlan_hv2_band_megafooter' ) ) { nadlan_hv2_band_megafooter(); } ?>
</div>
		<?php
		return ob_get_clean();
	}
}

/* Hebrew front page + the four language homes (/en /fr /ru /ar) share the renderer; same URLs, same hreflang cluster. */
add_filter( 'the_content', function ( $content ) {
	static $busy = false;
	if ( $busy || is_admin() || ! in_the_loop() || ! is_main_query() || ! nadlan_skin_a_on() ) { return $content; }
	$is_lang_home = function_exists( 'nadlan_is_language_home' ) && nadlan_is_language_home();
	if ( ! is_front_page() && ! $is_lang_home ) { return $content; }
	if ( get_queried_object_id() !== get_the_ID() ) { return $content; }
	$lang = ( $is_lang_home && function_exists( 'nadlan_current_lang' ) ) ? nadlan_current_lang() : 'he';
	$busy = true;
	$out  = nadlan_skin_a_home( $lang );
	$busy = false;
	return $out;
}, PHP_INT_MAX - 2 );

/* header: portal category labels on the skin only (same URLs, same order; labels are the skin's copy). Hebrew chrome only. */
/* concept project page (7514): the engine prints an availability chip with a zero count; a concept has no stock to announce (honesty law: unknown = omitted) */
add_action( 'wp_footer', function () {
	if ( ! nadlan_skin_a_on() || ! is_singular( 'nadlan_project' ) || 7514 !== (int) get_queried_object_id() ) { return; }
	?>
<script>(function(){function h(){document.querySelectorAll('#inventory .nl-chip').forEach(function(c){var t=(c.textContent||'').replace(/\s+/g,' ').trim();if(/^זמינות\s*0?$/.test(t)||/^זמינות 0\b/.test(t)||(t.indexOf('זמינות')===0&&/\b0\b/.test(t))){c.style.display='none';}});}h();var n=0,iv=setInterval(function(){h();if(++n>20)clearInterval(iv);},500);})();</script>
	<?php
}, 98 );

add_action( 'wp_footer', function () {
	if ( ! nadlan_skin_a_on() ) { return; }
	if ( function_exists( 'nadlan_current_lang' ) && 'he' !== nadlan_current_lang() ) { return; }
	?>
<script>(function(){var m={"/projects/":"פרויקטים חדשים","/premium/":"קטלוג תלת ממד","/sde-dov/":"אזורי ביקוש","/mortgage-calculator/":"מחשבונים","/global/":"נדל\"ן בחו\"ל","/professionals/":"אנשי מקצוע","/guides/":"מגזין נדל\"ן"};document.querySelectorAll('.nlpc-primary-nav a').forEach(function(a){var p=a.getAttribute('href')||'';try{p=new URL(p,location.origin).pathname;}catch(e){}if(m[p]&&a.textContent.trim()!==m[p]){a.textContent=m[p];}});var s=document.querySelector('.nlpc-brand__text small');if(s){s.textContent='פורטל נדל"ן: פרויקטים חדשים, דירות ומחירים';}var c=document.querySelector('.nlpc-header-cta');if(c){c.textContent='פרויקטים חדשים';}})();</script>
	<?php
}, 99 );
