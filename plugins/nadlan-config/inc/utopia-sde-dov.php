<?php
/**
 * nadlan-config - UTOPIA Sde Dov five-language project release.
 *
 * This module is intentionally limited to the UTOPIA slug family. It installs
 * the reviewed articles and verified project fields once, exposes localized
 * building-level 3D context, and supplies page-specific search and schema data.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_utopia_slug_lang' ) ) {
	function nadlan_utopia_slug_lang( $post_id = 0 ) {
		$implicit = ! $post_id;
		if ( $implicit && ( ! function_exists( 'is_singular' ) || ! is_singular( 'nadlan_project' ) ) ) { return ''; }
		$post_id = $post_id ? (int) $post_id : (int) get_queried_object_id();
		if ( ! $post_id || get_post_type( $post_id ) !== 'nadlan_project' ) { return ''; }
		$slug = (string) get_post_field( 'post_name', $post_id );
		if ( ! preg_match( '/^utopia-sde-dov(?:-(en|fr|ru|ar))?$/', $slug, $m ) ) { return ''; }
		$lang = isset( $m[1] ) && $m[1] !== '' ? $m[1] : 'he';
		if ( $lang === 'he' && $post_id !== 4749 ) { return ''; }
		if ( (string) get_post_meta( $post_id, '_nadlan_utopia_identity', true ) !== nadlan_utopia_identity_marker( $lang ) ) { return ''; }
		return $lang;
	}
}

if ( ! function_exists( 'nadlan_utopia_is_family' ) ) {
	function nadlan_utopia_is_family( $post_id = 0 ) {
		return nadlan_utopia_slug_lang( $post_id ) !== '';
	}
}

if ( ! function_exists( 'nadlan_utopia_asset_url' ) ) {
	function nadlan_utopia_asset_url( $file ) {
		$base = function_exists( 'nadlan_showroom_engine_base_url' )
			? trailingslashit( nadlan_showroom_engine_base_url() )
			: plugins_url( 'assets/showroom-engine/', dirname( __DIR__ ) . '/nadlan-config.php' );
		return $base . 'projects/utopia-sde-dov/' . ltrim( (string) $file, '/' );
	}
}

if ( ! function_exists( 'nadlan_utopia_rewrite_asset_urls' ) ) {
	function nadlan_utopia_rewrite_asset_urls( $html ) {
		$published_base = 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/';
		return str_replace( $published_base, nadlan_utopia_asset_url( '' ), (string) $html );
	}
}

if ( ! function_exists( 'nadlan_utopia_article_path' ) ) {
	function nadlan_utopia_article_path( $lang ) {
		$dir = function_exists( 'nadlan_showroom_engine_dir' )
			? trailingslashit( nadlan_showroom_engine_dir() )
			: dirname( __DIR__ ) . '/assets/showroom-engine/';
		return $dir . 'projects/utopia-sde-dov/article-' . sanitize_key( $lang ) . '.html';
	}
}

if ( ! function_exists( 'nadlan_utopia_release_slugs' ) ) {
	function nadlan_utopia_release_slugs() {
		return array(
			'he' => 'utopia-sde-dov',
			'en' => 'utopia-sde-dov-en',
			'fr' => 'utopia-sde-dov-fr',
			'ru' => 'utopia-sde-dov-ru',
			'ar' => 'utopia-sde-dov-ar',
		);
	}
}

if ( ! function_exists( 'nadlan_utopia_identity_marker' ) ) {
	function nadlan_utopia_identity_marker( $lang ) {
		return 'nadlan-utopia:lot-103:base-4749:' . sanitize_key( $lang );
	}
}

if ( ! function_exists( 'nadlan_utopia_expected_canonical' ) ) {
	function nadlan_utopia_expected_canonical( $lang ) {
		$slugs = nadlan_utopia_release_slugs();
		$slug  = isset( $slugs[ $lang ] ) ? $slugs[ $lang ] : $slugs['he'];
		return home_url( '/projects/' . $slug . '/' );
	}
}

if ( ! function_exists( 'nadlan_utopia_article_manifest' ) ) {
	function nadlan_utopia_article_manifest() {
		return array(
			'he' => array(
				'sha256' => 'fdc161bc1c760ec28baebaebf529daf1f84d36d02641419e52e1ed88e1fc1da9',
				'locale' => 'he-IL',
				'dir' => 'rtl',
				'h1' => 'UTOPIA שדה דב תל אביב - מחירים, דירות ובחירה מהבניין',
				'h2' => array( 'סקירה', 'מיקום וסביבה', 'הבניינים והדירות', 'מחירים ואומדנים', 'היזם', 'שלבי הפרויקט', 'למי זה מתאים', 'שאלות נפוצות', 'מקורות' ),
			),
			'en' => array(
				'sha256' => 'a7cb8b69c50a9cc5bb1f2370bd22871589ddb68bf45c2651421a070eda903fe5',
				'locale' => 'en-US',
				'dir' => 'ltr',
				'h1' => 'UTOPIA Sde Dov Tel Aviv - Apartments for Sale, Prices and Choosing a Home',
				'h2' => array( 'Overview', 'Location and surroundings', 'The buildings and apartments', 'Prices and estimates', 'The developer', 'Project stages', 'Who the project suits', 'Frequently asked questions', 'Sources' ),
			),
			'fr' => array(
				'sha256' => 'd344bafb736b0f56aaa4a5a0f1db59007556632c170983edb2a7f3c489fcbb51',
				'locale' => 'fr-FR',
				'dir' => 'ltr',
				'h1' => 'UTOPIA Sde Dov Tel Aviv - Appartements à vendre, prix et choix d\'un logement',
				'h2' => array( 'Vue d\'ensemble', 'Emplacement et environnement', 'Les bâtiments et les appartements', 'Prix et estimations', 'Le promoteur', 'Étapes du projet', 'À qui ce projet convient-il', 'Questions fréquentes', 'Sources' ),
			),
			'ru' => array(
				'sha256' => 'a004900d6e9dff39fa626ea04be3e65db0f95e962c567badc3309a75db5412ea',
				'locale' => 'ru-RU',
				'dir' => 'ltr',
				'h1' => 'UTOPIA Sde Dov Тель-Авив - квартиры на продажу, цены и выбор квартиры',
				'h2' => array( 'Обзор', 'Расположение и окружение', 'Здания и квартиры', 'Цены и оценки', 'Девелопер', 'Этапы проекта', 'Кому подходит проект', 'Частые вопросы', 'Источники' ),
			),
			'ar' => array(
				'sha256' => '9793250681d45fe6c34d1b480755488d3fb606b06fdfa24ca22657ece854248b',
				'locale' => 'ar',
				'dir' => 'rtl',
				'h1' => 'UTOPIA Sde Dov تل أبيب - شقق للبيع والأسعار واختيار الشقة',
				'h2' => array( 'نظرة عامة', 'الموقع والبيئة المحيطة', 'المباني والشقق', 'الأسعار والتقديرات', 'المطور', 'مراحل المشروع', 'لمن يناسب المشروع', 'أسئلة شائعة', 'المصادر' ),
			),
		);
	}
}

if ( ! function_exists( 'nadlan_utopia_source_contract' ) ) {
	function nadlan_utopia_source_contract() {
		return array(
			'https://utopiatlv.co.il/',
			'https://www.nahmias-group.co.il/project/utopia-%D7%A9%D7%93%D7%94-%D7%93%D7%91-%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91/',
			'https://www.nahmias-group.co.il/en/project/utopia/',
			'https://apps.land.gov.il/IturTabotData/takanonim/telmer/5050215.pdf',
			'https://apps.land.gov.il/IturTabotData/nispachim/telmer/5050215/20.pdf',
			'https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/772/query?where=request_num%3D20250165&outFields=*&returnGeometry=false&f=pjson',
			'https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/772/query?where=request_num%3D20250165&outFields=*&returnGeometry=true&outSR=4326&f=json',
			'https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/772/query?where=request_num%3D20250403&outFields=*&returnGeometry=false&f=pjson',
			'https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx',
			'https://www.tel-aviv.gov.il/Residents/Development/DocLib/%D7%9E%D7%92%D7%A8%D7%A9%20103%20%D7%93%D7%99%D7%95%D7%9F%20%D7%91%D7%A2%D7%99%D7%A6%D7%95%D7%91.pdf',
			'https://utopiatlv.co.il/wp-content/uploads/2025/07/UTOPIA-N1-4A-21222-copy.pdf',
			'https://utopiatlv.co.il/wp-content/uploads/2025/07/UTOPIA-N1-5G-62-copy.pdf',
			'https://utopiatlv.co.il/wp-content/uploads/2025/07/5G-S1-204.pdf',
			'https://utopiatlv.co.il/wp-content/uploads/2025/07/3P-S18094108122136150164.pdf',
			'https://utopiatlv.co.il/wp-content/uploads/2025/07/UTOPIA-N1-3A-81828-copy.pdf',
			'https://utopiatlv.co.il/wp-content/uploads/2025/07/4D-S156708498112126140154.pdf',
			'https://utopiatlv.co.il/wp-content/uploads/2025/07/UTOPIA-N1-5E-404448525660-copy.pdf',
			'https://en.globes.co.il/news/article.aspx?did=1001526410',
			'https://www.globes.co.il/news/article.aspx?did=1001515692',
			'https://www.bizportal.co.il/realestates/news/article/20033505',
			'https://www.calcalist.co.il/article/r12n2qiowx',
			'https://www.calcalist.co.il/real-estate/article/rybd6fiz9',
			'https://www.globes.co.il/news/article.aspx?did=1001497375',
		);
	}
}

if ( ! function_exists( 'nadlan_utopia_internal_link_contract' ) ) {
	function nadlan_utopia_internal_link_contract() {
		return array(
			'https://nad-lan.co.il/mortgage-calculator/',
			'https://nad-lan.co.il/purchase-tax-calculator/',
			'https://nad-lan.co.il/new-projects/',
			'https://nad-lan.co.il/tel-aviv-apartment-prices/',
			'https://nad-lan.co.il/cities/%d7%aa%d7%9c-%d7%90%d7%91%d7%99%d7%91-%d7%99%d7%a4%d7%95/',
			'https://nad-lan.co.il/sde-dov/',
		);
	}
}

if ( ! function_exists( 'nadlan_utopia_copy' ) ) {
	function nadlan_utopia_copy( $lang ) {
		$all = array(
			'he' => array(
				'post_title' => 'UTOPIA שדה דב - קבוצת נחמיאס',
				'seo_title'  => 'UTOPIA שדה דב תל אביב - מחירים, דירות ובחירה מהבניין',
				'seo_desc'   => 'UTOPIA שדה דב תל אביב: 337 דירות בארבעה מבנים, מגדל בן 34 קומות, דירות 2 עד 5 חדרים, סטטוס היתרים, מחירים ואומדנים לקנייה.',
				'excerpt'    => 'UTOPIA שדה דב הוא פרויקט בן 337 דירות במגרש 103 במתחם אשכול, עם מגדל בן 34 קומות, בניין בן 15 קומות ושני מבנים בני 7 קומות. הפרויקט נמצא בהליך היתר, ומחירון רשמי עדכני לא פורסם.',
				'developer'  => 'קבוצת נחמיאס',
				'architect'  => 'אבנר ישר',
				'address'    => 'מגרש 103, מתחם אשכול, רובע שדה דב',
				'city'       => 'תל אביב-יפו',
				'neighborhood' => 'שדה דב',
				'price_note' => 'מחירון רשמי עדכני לא פורסם.',
				'focus'      => 'UTOPIA שדה דב תל אביב',
				'media_note' => 'הדמיה עצמאית המבוססת על נתוני התכנון הפומביים. זו אינה הדמיה רשמית, מפרט מכר או מבט מדירה מסוימת.',
				'media_alt'  => 'UTOPIA שדה דב - הדמיה עצמאית המבוססת על נתוני תכנון פומביים',
				'orientation' => array( 'west' => 'כיוון הים התיכון', 'south' => 'רחוב 2 המתוכנן', 'east' => 'מגרש 401' ),
				'building_mode' => array(
					'eyebrow' => 'מודל התמצאות',
					'title' => 'ארבעת מבני הפרויקט',
					'prompt' => 'לחצו על מבנה כדי לראות את נתוני התכנון שפורסמו.',
					'model_note' => 'המודל מציג מסות בנייה לצורך התמצאות. החזיתות, החומרים, המרחקים והנוף אינם מפרט מכר.',
					'floors_label' => 'קומות שפורסמו',
					'buildings_label' => 'מבנים',
					'height_label' => 'גובה מרבי מתוכנן',
					'source_label' => 'מסמך התכנון העירוני',
					'plans_title' => 'תוכניות דוגמה שפורסמו',
					'plans_note' => 'התוכניות הן דוגמאות פומביות ואינן מעידות על מלאי או זמינות.',
					'map_note' => 'סימון המפה מייצג את מרכז מגרש 103. מיפוי של דירה מסוימת ידרוש טבלת דירות רשמית.',
					'close_label' => 'סגירת פרטי המבנה',
				),
			),
			'en' => array(
				'post_title' => 'UTOPIA Sde Dov - Nahmias Group',
				'seo_title'  => 'UTOPIA Sde Dov Tel Aviv - Apartments for Sale, Prices and Choosing a Home',
				'seo_desc'   => 'UTOPIA Sde Dov Tel Aviv: 337 apartments in four buildings, a 34-floor tower, 2 to 5-room homes, permit status, prices and purchase estimates.',
				'excerpt'    => 'UTOPIA Sde Dov is a 337-apartment project on lot 103 in the Eshkol complex, with a 34-floor tower, a 15-floor building and two 7-floor buildings. The project is in the permit process, and no current official price list has been published.',
				'developer'  => 'Nahmias Group',
				'architect'  => 'Avner Yashar',
				'address'    => 'Lot 103, Eshkol complex, Sde Dov district',
				'city'       => 'Tel Aviv-Yafo',
				'neighborhood' => 'Sde Dov',
				'price_note' => 'No current official price list has been published.',
				'focus'      => 'UTOPIA Sde Dov Tel Aviv apartments',
				'media_note' => 'Independent concept image based on public planning data. It is not an official rendering, sales specification or view from a particular apartment.',
				'media_alt'  => 'UTOPIA Sde Dov - independent concept illustration based on public planning data',
				'orientation' => array( 'west' => 'Mediterranean Sea direction', 'south' => 'Planned Street 2', 'east' => 'Lot 401' ),
				'building_mode' => array(
					'eyebrow' => 'Orientation model',
					'title' => 'The project\'s four buildings',
					'prompt' => 'Select a building to view its published planning data.',
					'model_note' => 'The model shows planning massing for orientation. Facades, materials, spacing and views are not sales specifications.',
					'floors_label' => 'Published floors',
					'buildings_label' => 'Buildings',
					'height_label' => 'Planned maximum height',
					'source_label' => 'Municipal planning document',
					'plans_title' => 'Published sample plans',
					'plans_note' => 'These are public examples and do not indicate inventory or availability.',
					'map_note' => 'The map pin marks the centroid of lot 103. Mapping a specific apartment requires an official apartment stack.',
					'close_label' => 'Close building details',
				),
			),
			'fr' => array(
				'post_title' => 'UTOPIA Sde Dov - Groupe Nahmias',
				'seo_title'  => 'UTOPIA Sde Dov Tel Aviv - Appartements à vendre, prix et choix d\'un logement',
				'seo_desc'   => 'UTOPIA Sde Dov Tel Aviv: 337 appartements dans quatre bâtiments, tour de 34 étages, logements de 2 à 5 pièces, permis, prix et estimations.',
				'excerpt'    => 'UTOPIA Sde Dov est un projet de 337 appartements sur la parcelle 103 du complexe Eshkol, avec une tour de 34 étages, un bâtiment de 15 étages et deux bâtiments de 7 étages. Le projet est en cours de permis et aucun tarif officiel actuel n\'a été publié.',
				'developer'  => 'Groupe Nahmias',
				'architect'  => 'Avner Yashar',
				'address'    => 'Parcelle 103, complexe Eshkol, quartier de Sde Dov',
				'city'       => 'Tel Aviv-Yafo',
				'neighborhood' => 'Sde Dov',
				'price_note' => 'Aucun tarif officiel actuel n\'a été publié.',
				'focus'      => 'UTOPIA Sde Dov Tel Aviv appartements',
				'media_note' => 'Image conceptuelle indépendante fondée sur les données publiques d\'urbanisme. Ce n\'est ni un rendu officiel, ni une notice de vente, ni une vue depuis un appartement précis.',
				'media_alt'  => 'UTOPIA Sde Dov - illustration conceptuelle indépendante fondée sur les données publiques d\'urbanisme',
				'orientation' => array( 'west' => 'Direction de la Méditerranée', 'south' => 'Rue 2 projetée', 'east' => 'Parcelle 401' ),
				'building_mode' => array(
					'eyebrow' => 'Modèle d\'orientation',
					'title' => 'Les quatre bâtiments du projet',
					'prompt' => 'Sélectionnez un bâtiment pour consulter les données d\'urbanisme publiées.',
					'model_note' => 'Le modèle présente les volumes à titre d\'orientation. Façades, matériaux, distances et vues ne constituent pas une notice de vente.',
					'floors_label' => 'Étages publiés',
					'buildings_label' => 'Bâtiments',
					'height_label' => 'Hauteur maximale projetée',
					'source_label' => 'Document municipal d\'urbanisme',
					'plans_title' => 'Plans d\'exemple publiés',
					'plans_note' => 'Ces plans publics sont des exemples et ne prouvent ni stock ni disponibilité.',
					'map_note' => 'Le repère cartographique correspond au centre de la parcelle 103. La localisation d\'un appartement précis exige une grille officielle.',
					'close_label' => 'Fermer les détails du bâtiment',
				),
			),
			'ru' => array(
				'post_title' => 'UTOPIA Sde Dov - группа Nahmias',
				'seo_title'  => 'UTOPIA Sde Dov Тель-Авив - квартиры на продажу, цены и выбор квартиры',
				'seo_desc'   => 'UTOPIA Sde Dov в Тель-Авиве: 337 квартир в четырех зданиях, башня на 34 этажа, квартиры на 2-5 комнат, разрешения, цены и оценки.',
				'excerpt'    => 'UTOPIA Sde Dov - проект на 337 квартир на участке 103 в комплексе Эшколь. В составе заявлены башня на 34 этажа, здание на 15 этажей и два здания на 7 этажей. Проект проходит разрешительный процесс, актуальный официальный прайс-лист не опубликован.',
				'developer'  => 'Группа Nahmias',
				'architect'  => 'Авнер Яшар',
				'address'    => 'Участок 103, комплекс Эшколь, район Сде-Дов',
				'city'       => 'Тель-Авив-Яффо',
				'neighborhood' => 'Сде-Дов',
				'price_note' => 'Актуальный официальный прайс-лист не опубликован.',
				'focus'      => 'UTOPIA Sde Dov Тель-Авив квартиры',
				'media_note' => 'Независимая концептуальная визуализация на основе открытых данных планирования. Это не официальный рендер, не спецификация продажи и не вид из конкретной квартиры.',
				'media_alt'  => 'UTOPIA Sde Dov - независимая концептуальная иллюстрация по открытым данным планирования',
				'orientation' => array( 'west' => 'В сторону Средиземного моря', 'south' => 'Проектируемая улица 2', 'east' => 'Участок 401' ),
				'building_mode' => array(
					'eyebrow' => 'Ориентационная модель',
					'title' => 'Четыре здания проекта',
					'prompt' => 'Выберите здание, чтобы увидеть опубликованные параметры планирования.',
					'model_note' => 'Модель показывает объемы застройки для ориентации. Фасады, материалы, расстояния и виды не являются спецификацией продажи.',
					'floors_label' => 'Опубликованная этажность',
					'buildings_label' => 'Здания',
					'height_label' => 'Планируемая предельная высота',
					'source_label' => 'Муниципальный документ планирования',
					'plans_title' => 'Опубликованные примеры планов',
					'plans_note' => 'Это открытые примеры, они не подтверждают наличие или доступность квартир.',
					'map_note' => 'Метка на карте показывает центр участка 103. Для привязки конкретной квартиры нужна официальная квартирография.',
					'close_label' => 'Закрыть сведения о здании',
				),
			),
			'ar' => array(
				'post_title' => 'UTOPIA Sde Dov - مجموعة نحمياس',
				'seo_title'  => 'UTOPIA Sde Dov تل أبيب - شقق للبيع والأسعار واختيار الشقة',
				'seo_desc'   => 'UTOPIA Sde Dov تل أبيب: 337 شقة في أربعة مبان، برج من 34 طابقا، شقق من غرفتين إلى 5 غرف، حالة التراخيص والأسعار وتقديرات الشراء.',
				'excerpt'    => 'UTOPIA Sde Dov مشروع يضم 337 شقة في القسيمة 103 ضمن مجمع إشكول، ويتكون من برج من 34 طابقا ومبنى من 15 طابقا ومبنيين من 7 طوابق. المشروع في مسار الترخيص، ولم تنشر قائمة أسعار رسمية حديثة.',
				'developer'  => 'مجموعة نحمياس',
				'architect'  => 'أفنير ياشار',
				'address'    => 'القسيمة 103، مجمع إشكول، حي سديه دوف',
				'city'       => 'تل أبيب-يافا',
				'neighborhood' => 'سديه دوف',
				'price_note' => 'لم تنشر قائمة أسعار رسمية حديثة.',
				'focus'      => 'UTOPIA Sde Dov تل أبيب شقق',
				'media_note' => 'صورة تصورية مستقلة مبنية على بيانات التخطيط العامة. ليست تصميما رسميا أو مواصفات بيع أو إطلالة من شقة بعينها.',
				'media_alt'  => 'UTOPIA Sde Dov - صورة تصورية مستقلة مبنية على بيانات التخطيط العامة',
				'orientation' => array( 'west' => 'باتجاه البحر المتوسط', 'south' => 'الشارع المخطط رقم 2', 'east' => 'القسيمة 401' ),
				'building_mode' => array(
					'eyebrow' => 'نموذج للتعرف على المشروع',
					'title' => 'المباني الأربعة في المشروع',
					'prompt' => 'اختر مبنى للاطلاع على بيانات التخطيط المنشورة.',
					'model_note' => 'يعرض النموذج كتل البناء بغرض التعرف على المشروع. الواجهات والمواد والمسافات والإطلالات ليست مواصفات بيع.',
					'floors_label' => 'الطوابق المنشورة',
					'buildings_label' => 'مبان',
					'height_label' => 'الارتفاع الأقصى المخطط',
					'source_label' => 'وثيقة التخطيط البلدية',
					'plans_title' => 'نماذج المخططات المنشورة',
					'plans_note' => 'هذه أمثلة عامة ولا تثبت المخزون أو توافر الشقق.',
					'map_note' => 'تشير علامة الخريطة إلى مركز القسيمة 103. ربط شقة محددة يتطلب جدولا رسميا للشقق.',
					'close_label' => 'إغلاق تفاصيل المبنى',
				),
			),
		);
		return isset( $all[ $lang ] ) ? $all[ $lang ] : $all['he'];
	}
}

if ( ! function_exists( 'nadlan_utopia_buildings' ) ) {
	function nadlan_utopia_buildings( $lang ) {
		$packet = 'https://www.tel-aviv.gov.il/Residents/Development/DocLib/%D7%9E%D7%92%D7%A8%D7%A9%20103%20%D7%93%D7%99%D7%95%D7%9F%20%D7%91%D7%A2%D7%99%D7%A6%D7%95%D7%91.pdf';
		$text = array(
			'he' => array(
				's1' => array( 'מגדל S1', '34 קומות מגורים בתוספת קומת קרקע וקומה טכנית. מסמכי התכנון מציגים גובה מרבי של כ-137 מטר ומייחסים 205 דירות לבינוי המגדלי.', '34 קומות מגורים', 'כ-137 מטר' ),
				'n1' => array( 'בניין N1', '14 קומות מגורים בתוספת קומת קרקע וקומה טכנית. בפרסום הפרויקט הוא מוצג כבניין בן 15 קומות. הגובה המרבי במסמכי התכנון הוא כ-70 מטר.', '15 קומות בפרסום הפרויקט', 'כ-70 מטר' ),
				'n2' => array( 'בניין N2', '7 קומות מגורים בתוספת קומת קרקע וקומה טכנית. מסמכי התכנון מציגים גובה מרבי של כ-38 מטר.', '7 קומות מגורים', 'כ-38 מטר' ),
				's2' => array( 'בניין S2', '7 קומות מגורים בתוספת קומת קרקע וקומה טכנית. מסמכי התכנון מציגים גובה מרבי של כ-38 מטר.', '7 קומות מגורים', 'כ-38 מטר' ),
			),
			'en' => array(
				's1' => array( 'S1 tower', '34 residential floors plus ground and technical levels. Planning documents show a maximum height of about 137 metres and assign 205 homes to the tower construction.', '34 residential floors', 'About 137 metres' ),
				'n1' => array( 'N1 building', '14 residential floors plus ground and technical levels. Project marketing describes it as a 15-floor building. The planned maximum height is about 70 metres.', '15 floors in project marketing', 'About 70 metres' ),
				'n2' => array( 'N2 building', '7 residential floors plus ground and technical levels. Planning documents show a maximum height of about 38 metres.', '7 residential floors', 'About 38 metres' ),
				's2' => array( 'S2 building', '7 residential floors plus ground and technical levels. Planning documents show a maximum height of about 38 metres.', '7 residential floors', 'About 38 metres' ),
			),
			'fr' => array(
				's1' => array( 'Tour S1', '34 étages résidentiels, plus le rez-de-chaussée et un niveau technique. Les documents indiquent environ 137 mètres au maximum et attribuent 205 logements à la construction de la tour.', '34 étages résidentiels', 'Environ 137 mètres' ),
				'n1' => array( 'Bâtiment N1', '14 étages résidentiels, plus le rez-de-chaussée et un niveau technique. La communication du projet le présente comme un bâtiment de 15 étages. La hauteur maximale prévue est d\'environ 70 mètres.', '15 étages dans la communication', 'Environ 70 mètres' ),
				'n2' => array( 'Bâtiment N2', '7 étages résidentiels, plus le rez-de-chaussée et un niveau technique. La hauteur maximale prévue est d\'environ 38 mètres.', '7 étages résidentiels', 'Environ 38 mètres' ),
				's2' => array( 'Bâtiment S2', '7 étages résidentiels, plus le rez-de-chaussée et un niveau technique. La hauteur maximale prévue est d\'environ 38 mètres.', '7 étages résidentiels', 'Environ 38 mètres' ),
			),
			'ru' => array(
				's1' => array( 'Башня S1', '34 жилых этажа, а также первый и технический уровни. В документах указана предельная высота около 137 метров, к башенной части отнесено 205 квартир.', '34 жилых этажа', 'Около 137 метров' ),
				'n1' => array( 'Здание N1', '14 жилых этажей, а также первый и технический уровни. В материалах проекта оно представлено как 15-этажное. Предельная планируемая высота составляет около 70 метров.', '15 этажей в материалах проекта', 'Около 70 метров' ),
				'n2' => array( 'Здание N2', '7 жилых этажей, а также первый и технический уровни. Предельная планируемая высота составляет около 38 метров.', '7 жилых этажей', 'Около 38 метров' ),
				's2' => array( 'Здание S2', '7 жилых этажей, а также первый и технический уровни. Предельная планируемая высота составляет около 38 метров.', '7 жилых этажей', 'Около 38 метров' ),
			),
			'ar' => array(
				's1' => array( 'البرج S1', '34 طابقا سكنيا إضافة إلى الطابق الأرضي والطابق التقني. تعرض وثائق التخطيط ارتفاعا أقصى يقارب 137 مترا وتنسب 205 شقق إلى بناء البرج.', '34 طابقا سكنيا', 'نحو 137 مترا' ),
				'n1' => array( 'المبنى N1', '14 طابقا سكنيا إضافة إلى الطابق الأرضي والطابق التقني. تعرضه مواد المشروع كمبنى من 15 طابقا. الارتفاع الأقصى المخطط يقارب 70 مترا.', '15 طابقا في مواد المشروع', 'نحو 70 مترا' ),
				'n2' => array( 'المبنى N2', '7 طوابق سكنية إضافة إلى الطابق الأرضي والطابق التقني. الارتفاع الأقصى المخطط يقارب 38 مترا.', '7 طوابق سكنية', 'نحو 38 مترا' ),
				's2' => array( 'المبنى S2', '7 طوابق سكنية إضافة إلى الطابق الأرضي والطابق التقني. الارتفاع الأقصى المخطط يقارب 38 مترا.', '7 طوابق سكنية', 'نحو 38 مترا' ),
			),
		);
		$t = isset( $text[ $lang ] ) ? $text[ $lang ] : $text['he'];
		$raw = array(
			's1' => array( 'id' => 's1', 'hotspot_position' => '-38 75 -13', 'hotspot_normal' => '-0.2 0 1', 'camera_target' => '-38m 54m -13m', 'camera_orbit' => '-30deg 64deg 128m' ),
			'n1' => array( 'id' => 'n1', 'hotspot_position' => '24 34 -20', 'hotspot_normal' => '0.2 0 1', 'camera_target' => '24m 24m -20m', 'camera_orbit' => '25deg 68deg 105m' ),
			'n2' => array( 'id' => 'n2', 'hotspot_position' => '-17 18 36', 'hotspot_normal' => '0 0 1', 'camera_target' => '-17m 13m 36m', 'camera_orbit' => '-40deg 70deg 92m' ),
			's2' => array( 'id' => 's2', 'hotspot_position' => '39 18 34', 'hotspot_normal' => '0 0 1', 'camera_target' => '39m 13m 34m', 'camera_orbit' => '40deg 70deg 92m' ),
		);
		$out = array();
		foreach ( $raw as $key => $item ) {
			$item['label']       = $t[ $key ][0];
			$item['facts']       = $t[ $key ][1];
			$item['floors']      = $t[ $key ][2];
			$item['height']      = $t[ $key ][3];
			$item['source_url']  = $packet;
			$out[] = $item;
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_utopia_sample_plans' ) ) {
	function nadlan_utopia_sample_plans( $lang ) {
		$prefix = array(
			'he' => 'תוכנית דוגמה',
			'en' => 'Sample plan',
			'fr' => 'Plan d\'exemple',
			'ru' => 'Пример плана',
			'ar' => 'نموذج مخطط',
		);
		$p = isset( $prefix[ $lang ] ) ? $prefix[ $lang ] : $prefix['he'];
		return array(
			array(
				'id' => 'n1-4a', 'building' => 'n1', 'type' => '4A', 'rooms' => 4,
				'interior_sqm' => 100.46, 'balcony_sqm' => 12.78,
				'references' => array(
					array( 'floor' => 1, 'apartment' => 2 ),
					array( 'floor' => 3, 'apartment' => 12 ),
					array( 'floor' => 5, 'apartment' => 22 ),
				),
				'label' => $p . ' N1 4A',
				'url' => 'https://utopiatlv.co.il/wp-content/uploads/2025/07/UTOPIA-N1-4A-21222-copy.pdf',
				'source_page' => 1,
				'source_pdf_sha256' => 'e2d532eddf48d5c92a733b7112315836aa6a675ee88862910a50a4d2249a85e2',
			),
			array(
				'id' => 'n1-5g', 'building' => 'n1', 'type' => '5G', 'rooms' => 5,
				'interior_sqm' => 233.18, 'balcony_sqm' => 42.60,
				'references' => array( array( 'floor' => 15, 'apartment' => 62 ) ),
				'label' => $p . ' N1 5G',
				'url' => 'https://utopiatlv.co.il/wp-content/uploads/2025/07/UTOPIA-N1-5G-62-copy.pdf',
				'source_page' => 1,
				'source_pdf_sha256' => '768353673a6032b11d52e3e4dee51e20081559a159c3853381efc1572d08254c',
			),
			array(
				'id' => 'n1-5e', 'building' => 'n1', 'type' => '5E / C5', 'rooms' => 5,
				'interior_sqm' => 145.95, 'balcony_sqm' => 26.80,
				'references' => array(
					array( 'floor' => 9, 'apartment' => 40 ),
					array( 'floor' => 10, 'apartment' => 44 ),
					array( 'floor' => 11, 'apartment' => 48 ),
					array( 'floor' => 12, 'apartment' => 52 ),
					array( 'floor' => 13, 'apartment' => 56 ),
					array( 'floor' => 14, 'apartment' => 60 ),
				),
				'label' => $p . ' N1 5E / C5',
				'label_mismatch' => true,
				'url' => 'https://utopiatlv.co.il/wp-content/uploads/2025/07/UTOPIA-N1-5E-404448525660-copy.pdf',
				'source_page' => 1,
				'source_pdf_sha256' => 'cb2b8d534a72dc15ce01f4e7f4b178b2b9e77fb359a6b9b9c506dc5aa5a46a4e',
			),
			array(
				'id' => 'n1-3a', 'building' => 'n1', 'type' => '3A', 'rooms' => 3,
				'interior_sqm' => 86.88, 'balcony_sqm' => 15.80,
				'references' => array(
					array( 'floor' => 2, 'apartment' => 8 ),
					array( 'floor' => 4, 'apartment' => 18 ),
					array( 'floor' => 6, 'apartment' => 28 ),
				),
				'label' => $p . ' N1 3A',
				'url' => 'https://utopiatlv.co.il/wp-content/uploads/2025/07/UTOPIA-N1-3A-81828-copy.pdf',
				'source_page' => 1,
				'source_pdf_sha256' => 'a939675f06622471e6d5f6f9ce07e7c7325ced58ea2726dd887cca4698cf497b',
			),
			array(
				'id' => 's1-5g', 'building' => 's1', 'type' => '5G', 'rooms' => 5,
				'interior_sqm' => 292.45, 'balcony_sqm' => 130.22,
				'references' => array( array( 'floor' => 33, 'apartment' => 204 ) ),
				'label' => $p . ' S1 5G',
				'url' => 'https://utopiatlv.co.il/wp-content/uploads/2025/07/5G-S1-204.pdf',
				'source_page' => 1,
				'source_pdf_sha256' => '170c009dd0914cde493e56ae9572bd7cb59421b0273d11064addb8068d7b2478',
			),
			array(
				'id' => 's1-3p', 'building' => 's1', 'type' => '3P', 'rooms' => 3,
				'interior_sqm' => 88.44, 'balcony_sqm' => 11.40,
				'references' => array(
					array( 'floor' => 11, 'apartment' => 80 ),
					array( 'floor' => 13, 'apartment' => 94 ),
					array( 'floor' => 15, 'apartment' => 108 ),
					array( 'floor' => 17, 'apartment' => 122 ),
					array( 'floor' => 19, 'apartment' => 136 ),
					array( 'floor' => 21, 'apartment' => 150 ),
					array( 'floor' => 23, 'apartment' => 164 ),
				),
				'label' => $p . ' S1 3P',
				'url' => 'https://utopiatlv.co.il/wp-content/uploads/2025/07/3P-S18094108122136150164.pdf',
				'source_page' => 1,
				'source_pdf_sha256' => '500d9780375f3b71b6b7c76d0ee81c2c1bd31bbcad74d47d6d0b2fc0522e19ba',
			),
			array(
				'id' => 's1-4d', 'building' => 's1', 'type' => '4D', 'rooms' => 4,
				'interior_sqm' => 101.67, 'balcony_sqm' => 8.70,
				'references' => array(
					array( 'floor' => 8, 'apartment' => 56 ),
					array( 'floor' => 10, 'apartment' => 70 ),
					array( 'floor' => 12, 'apartment' => 84 ),
					array( 'floor' => 14, 'apartment' => 98 ),
					array( 'floor' => 16, 'apartment' => 112 ),
					array( 'floor' => 18, 'apartment' => 126 ),
					array( 'floor' => 20, 'apartment' => 140 ),
					array( 'floor' => 22, 'apartment' => 154 ),
				),
				'label' => $p . ' S1 4D',
				'url' => 'https://utopiatlv.co.il/wp-content/uploads/2025/07/4D-S156708498112126140154.pdf',
				'source_page' => 1,
				'source_pdf_sha256' => 'dfff581a4f7f1358b55b2e396e962e0cc6f831de1e74dada8451ae83a90aafa7',
			),
		);
	}
}

if ( ! function_exists( 'nadlan_utopia_area_payload' ) ) {
	function nadlan_utopia_area_payload() {
		return array(
			'label_key' => 'area_sde_dov',
			'blurb_key' => 'area_sde_dov_blurb',
			'map' => array(
				'center' => array( 'lat' => 32.105979, 'lng' => 34.784524 ),
				'zoom' => 14,
				'bbox' => array( 'w' => 34.766, 's' => 32.092, 'e' => 34.802, 'n' => 32.116 ),
				'coast_x' => 16,
				'project_pin' => array( 'x' => 52, 'y' => 43 ),
				'pins' => array(
					array( 'ref' => 'reading-tower', 'x' => 24, 'y' => 82 ),
					array( 'ref' => 'tlv-beach', 'x' => 11, 'y' => 34 ),
					array( 'ref' => 'light-rail-green', 'x' => 58, 'y' => 60 ),
					array( 'ref' => 'yarkon-park', 'x' => 70, 'y' => 80 ),
					array( 'ref' => 'sde-dov-school', 'x' => 62, 'y' => 30 ),
					array( 'ref' => 'commercial-hub', 'x' => 52, 'y' => 42 ),
					array( 'ref' => 'ayalon-access', 'x' => 86, 'y' => 56 ),
				),
			),
			'spoke_groups' => array(
				array( 'id' => 'transport', 'icon' => 'train', 'label_key' => 'spoke_transport', 'items' => array( 'light-rail-green', 'ayalon-access' ) ),
				array( 'id' => 'education', 'icon' => 'school', 'label_key' => 'spoke_education', 'items' => array( 'sde-dov-school' ) ),
				array( 'id' => 'facilities', 'icon' => 'store', 'label_key' => 'spoke_facilities', 'items' => array( 'tlv-beach', 'yarkon-park', 'commercial-hub' ) ),
				array( 'id' => 'anchor', 'icon' => 'landmark', 'label_key' => 'spoke_anchor', 'items' => array( 'reading-tower' ) ),
			),
			'stats' => array(
				array( 'id' => 'plan', 'value' => 'TML/3001', 'label_key' => 'stat_plan' ),
				array( 'id' => 'units', 'value' => '337', 'label_key' => 'stat_units' ),
				array( 'id' => 'dunams', 'value' => '5.203', 'label_key' => 'stat_dunams' ),
			),
		);
	}
}

if ( ! function_exists( 'nadlan_utopia_spokes_payload' ) ) {
	function nadlan_utopia_spokes_payload() {
		return array(
			'reading-tower' => array( 'id' => 'reading-tower', 'type' => 'anchor', 'icon' => 'landmark', 'label_key' => 'spoke_reading_tower' ),
			'tlv-beach' => array( 'id' => 'tlv-beach', 'type' => 'facility', 'icon' => 'wave', 'label_key' => 'spoke_beach' ),
			'light-rail-green' => array( 'id' => 'light-rail-green', 'type' => 'transport', 'icon' => 'train', 'label_key' => 'spoke_light_rail' ),
			'yarkon-park' => array( 'id' => 'yarkon-park', 'type' => 'facility', 'icon' => 'tree', 'label_key' => 'spoke_yarkon_park' ),
			'sde-dov-school' => array( 'id' => 'sde-dov-school', 'type' => 'education', 'icon' => 'school', 'label_key' => 'spoke_school' ),
			'commercial-hub' => array( 'id' => 'commercial-hub', 'type' => 'facility', 'icon' => 'store', 'label_key' => 'spoke_commercial' ),
			'ayalon-access' => array( 'id' => 'ayalon-access', 'type' => 'transport', 'icon' => 'road', 'label_key' => 'spoke_road' ),
		);
	}
}

if ( ! function_exists( 'nadlan_utopia_nearby_project_bases' ) ) {
	function nadlan_utopia_nearby_project_bases() {
		return array( 'rainbow-tel-aviv', 'ashira-sde-dov', 'dimri-yama-sde-dov', 'first-sde-dov', 'zohi-sde-dov' );
	}
}

if ( ! function_exists( 'nadlan_utopia_faq' ) ) {
	function nadlan_utopia_faq( $lang ) {
		$faq = array(
			'he' => array(
				array( 'כמה דירות ומבנים מתוכננים ב-UTOPIA שדה דב?', 'פורסמו 337 דירות בארבעה מבנים: מגדל בן 34 קומות, בניין בן 15 קומות ושני מבנים בני 7 קומות.' ),
				array( 'מה מצב ההיתרים בפרויקט?', 'הבקשה העיקרית נמצאת בהליך היתר. היתר לעבודות חפירה, דיפון ויסודות ניתן ב-18 ביוני 2025, ורישום תחילת עבודה מופיע מ-14 בספטמבר 2025.' ),
				array( 'האם פורסם מחירון רשמי עדכני?', 'לא פורסם מחירון רשמי עדכני. דיווחי עיתונות ואומדנים בעמוד אינם הצעת מחיר ויש לבדוק מחיר ותנאים לדירה מסוימת.' ),
				array( 'האם אפשר לבחור דירה מדויקת מתוך המודל?', 'לא פורסמו טבלת דירות מלאה או קובץ BIM רשמי. המודל מציג את ארבעת המבנים לצורך התמצאות, ותוכניות הדוגמה אינן מעידות על זמינות.' ),
			),
			'en' => array(
				array( 'How many apartments and buildings are planned at UTOPIA Sde Dov?', 'Published plans show 337 apartments in four buildings: a 34-floor tower, a 15-floor building and two 7-floor buildings.' ),
				array( 'What is the project permit status?', 'The main application remains in the permit process. A permit for excavation, shoring and foundations was issued on 18 June 2025, with a work-start record dated 14 September 2025.' ),
				array( 'Has a current official price list been published?', 'No current official price list has been published. Press reports and estimates on this page are not offers, so price and terms must be checked for a specific apartment.' ),
				array( 'Can I select an exact apartment in the model?', 'No complete apartment stack or official BIM file has been published. The model identifies the four buildings for orientation, and sample plans do not indicate availability.' ),
			),
			'fr' => array(
				array( 'Combien de logements et de bâtiments sont prévus à UTOPIA Sde Dov ?', 'Les données publiées indiquent 337 appartements dans quatre bâtiments : une tour de 34 étages, un bâtiment de 15 étages et deux bâtiments de 7 étages.' ),
				array( 'Où en est le permis du projet ?', 'La demande principale est toujours en cours. Un permis pour excavation, soutènement et fondations a été délivré le 18 juin 2025, avec un enregistrement de début des travaux daté du 14 septembre 2025.' ),
				array( 'Un tarif officiel actuel a-t-il été publié ?', 'Aucun tarif officiel actuel n\'a été publié. Les articles de presse et estimations de cette page ne sont pas des offres ; le prix et les conditions doivent être vérifiés pour chaque appartement.' ),
				array( 'Peut-on choisir un appartement précis dans le modèle ?', 'Aucune grille complète des appartements ni aucun fichier BIM officiel n\'ont été publiés. Le modèle sert à identifier les quatre bâtiments, et les plans d\'exemple n\'indiquent pas la disponibilité.' ),
			),
			'ru' => array(
				array( 'Сколько квартир и зданий запланировано в UTOPIA Sde Dov?', 'Опубликованные материалы указывают 337 квартир в четырех зданиях: башне на 34 этажа, здании на 15 этажей и двух зданиях на 7 этажей.' ),
				array( 'На какой стадии находятся разрешения?', 'Основная заявка остается в разрешительном процессе. Разрешение на выемку грунта, ограждение котлована и фундаменты выдано 18 июня 2025 года, запись о начале работ датирована 14 сентября 2025 года.' ),
				array( 'Опубликован ли актуальный официальный прайс-лист?', 'Актуальный официальный прайс-лист не опубликован. Сообщения прессы и оценки на этой странице не являются офертой; цену и условия нужно проверять для конкретной квартиры.' ),
				array( 'Можно ли выбрать точную квартиру в модели?', 'Полная квартирография и официальный BIM-файл не опубликованы. Модель помогает различить четыре здания, а примеры планов не подтверждают наличие квартир.' ),
			),
			'ar' => array(
				array( 'كم عدد الشقق والمباني المخططة في UTOPIA Sde Dov؟', 'تشير البيانات المنشورة إلى 337 شقة في أربعة مبان: برج من 34 طابقا، ومبنى من 15 طابقا، ومبنيان من 7 طوابق.' ),
				array( 'ما وضع تراخيص المشروع؟', 'ما زال الطلب الرئيسي في مسار الترخيص. صدر تصريح للحفر والتدعيم والأساسات في 18 يونيو 2025، ويوجد تسجيل لبدء العمل بتاريخ 14 سبتمبر 2025.' ),
				array( 'هل نشرت قائمة أسعار رسمية حديثة؟', 'لم تنشر قائمة أسعار رسمية حديثة. تقارير الصحافة والتقديرات في الصفحة ليست عروضا ملزمة، ويجب فحص السعر والشروط لكل شقة بعينها.' ),
				array( 'هل يمكن اختيار شقة محددة من النموذج؟', 'لم ينشر جدول كامل للشقق أو ملف BIM رسمي. يساعد النموذج على التعرف على المباني الأربعة، ومخططات العينة لا تثبت التوافر.' ),
			),
		);
		return isset( $faq[ $lang ] ) ? $faq[ $lang ] : $faq['he'];
	}
}

if ( ! function_exists( 'nadlan_utopia_html_text' ) ) {
	function nadlan_utopia_html_text( $html ) {
		$html = preg_replace( '/<(script|style)\b[^>]*>.*?<\/\1>/isu', ' ', (string) $html );
		return trim( preg_replace( '/\s+/u', ' ', html_entity_decode( wp_strip_all_tags( $html ), ENT_QUOTES | ENT_HTML5, 'UTF-8' ) ) );
	}
}

if ( ! function_exists( 'nadlan_utopia_tag_texts' ) ) {
	function nadlan_utopia_tag_texts( $html, $tag ) {
		$out = array();
		if ( preg_match_all( '/<' . preg_quote( $tag, '/' ) . '\b[^>]*>(.*?)<\/' . preg_quote( $tag, '/' ) . '>/isu', (string) $html, $matches ) ) {
			foreach ( $matches[1] as $match ) {
				$out[] = nadlan_utopia_html_text( $match );
			}
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_utopia_validate_article' ) ) {
	function nadlan_utopia_validate_article( $lang, $path ) {
		$manifest = nadlan_utopia_article_manifest();
		if ( ! isset( $manifest[ $lang ] ) ) {
			return new WP_Error( 'utopia_bad_language', 'Unknown article language: ' . $lang );
		}
		if ( ! is_readable( $path ) ) {
			return new WP_Error( 'utopia_missing_article', 'Missing article file: ' . basename( $path ) );
		}

		$spec = $manifest[ $lang ];
		$html = (string) file_get_contents( $path );
		if ( ! hash_equals( $spec['sha256'], hash( 'sha256', $html ) ) ) {
			return new WP_Error( 'utopia_article_hash', 'Article SHA-256 mismatch: ' . basename( $path ) );
		}
		if ( ! preg_match( '/<article\b([^>]*)>/iu', $html, $article ) ) {
			return new WP_Error( 'utopia_article_element', 'Article element missing: ' . basename( $path ) );
		}
		if ( ! preg_match( '/\blang=(["\'])' . preg_quote( $spec['locale'], '/' ) . '\1/iu', $article[1] ) ||
			! preg_match( '/\bdir=(["\'])' . preg_quote( $spec['dir'], '/' ) . '\1/iu', $article[1] ) ) {
			return new WP_Error( 'utopia_article_locale', 'Article language or direction mismatch: ' . basename( $path ) );
		}
		if ( strpos( $html, 'nadlan-project-lead' ) === false ) {
			return new WP_Error( 'utopia_article_lead', 'Article lead marker missing: ' . basename( $path ) );
		}

		$h1 = nadlan_utopia_tag_texts( $html, 'h1' );
		$h2 = nadlan_utopia_tag_texts( $html, 'h2' );
		if ( count( $h1 ) !== 1 || $h1[0] !== $spec['h1'] ) {
			return new WP_Error( 'utopia_article_h1', 'Article H1 mismatch: ' . basename( $path ) );
		}
		if ( $h2 !== $spec['h2'] ) {
			return new WP_Error( 'utopia_article_h2', 'Article H2 sequence mismatch: ' . basename( $path ) );
		}

		$text = nadlan_utopia_html_text( $html );
		$word_count = preg_match_all( '/[\p{L}\p{N}]+(?:[\'’־-][\p{L}\p{N}]+)*/u', $text, $words );
		if ( $word_count === false || $word_count < 5000 ) {
			return new WP_Error( 'utopia_article_depth', 'Article is below 5,000 words: ' . basename( $path ) );
		}

		foreach ( nadlan_utopia_internal_link_contract() as $url ) {
			if ( strpos( $html, 'href="' . $url . '"' ) === false && strpos( $html, "href='" . $url . "'" ) === false ) {
				return new WP_Error( 'utopia_article_internal_link', 'Required internal link missing in ' . basename( $path ) . ': ' . $url );
			}
		}

		if ( ! preg_match_all( '/<h2\b[^>]*>.*?<\/h2>/isu', $html, $heading_matches, PREG_OFFSET_CAPTURE ) || count( $heading_matches[0] ) !== 9 ) {
			return new WP_Error( 'utopia_article_sources', 'Sources chapter boundary missing: ' . basename( $path ) );
		}
		$last_heading = $heading_matches[0][8];
		$source_html  = substr( $html, (int) $last_heading[1] );
		$hrefs        = array();
		if ( preg_match_all( '/<a\b[^>]*\bhref=(["\'])(.*?)\1/isu', $source_html, $link_matches ) ) {
			foreach ( $link_matches[2] as $href ) {
				$hrefs[] = html_entity_decode( $href, ENT_QUOTES | ENT_HTML5, 'UTF-8' );
			}
		}
		$actual_sources   = array_values( array_unique( $hrefs ) );
		$expected_sources = nadlan_utopia_source_contract();
		sort( $actual_sources );
		sort( $expected_sources );
		if ( $actual_sources !== $expected_sources ) {
			return new WP_Error( 'utopia_article_source_contract', 'Sources contract mismatch: ' . basename( $path ) );
		}

		return $html;
	}
}

if ( ! function_exists( 'nadlan_utopia_validate_existing_identity' ) ) {
	function nadlan_utopia_validate_existing_identity( $post, $lang, $is_base = false ) {
		$post  = get_post( $post );
		$slugs = nadlan_utopia_release_slugs();
		if ( ! $post || ! isset( $slugs[ $lang ] ) || $post->post_type !== 'nadlan_project' || $post->post_name !== $slugs[ $lang ] ) {
			return new WP_Error( 'utopia_identity_slug', 'UTOPIA identity mismatch for language ' . $lang . '.' );
		}
		if ( in_array( $post->post_status, array( 'trash', 'auto-draft' ), true ) ) {
			return new WP_Error( 'utopia_identity_status', 'UTOPIA target is not an editable project: ' . $slugs[ $lang ] );
		}
		$marker = (string) get_post_meta( $post->ID, '_nadlan_utopia_identity', true );
		if ( $is_base ) {
			if ( (int) $post->ID !== 4749 || stripos( (string) $post->post_title, 'UTOPIA' ) === false ) {
				return new WP_Error( 'utopia_identity_base', 'Approved UTOPIA base post 4749 was not found with the expected title and slug.' );
			}
			$source_url = untrailingslashit( (string) get_post_meta( $post->ID, 'source_url', true ) );
			if ( $source_url !== '' && $source_url !== 'https://utopiatlv.co.il' ) {
				return new WP_Error( 'utopia_identity_source', 'Approved UTOPIA base post has an unexpected source URL.' );
			}
			if ( $marker !== '' && $marker !== nadlan_utopia_identity_marker( 'he' ) ) {
				return new WP_Error( 'utopia_identity_marker', 'Approved UTOPIA base post has a conflicting identity marker.' );
			}
			return true;
		}
		if ( $marker !== nadlan_utopia_identity_marker( $lang ) ) {
			return new WP_Error( 'utopia_identity_collision', 'Slug collision: existing project is not a marked UTOPIA translation: ' . $slugs[ $lang ] );
		}
		return true;
	}
}

if ( ! function_exists( 'nadlan_utopia_acquire_release_lock' ) ) {
	function nadlan_utopia_acquire_release_lock() {
		$key   = 'nadlan_utopia_release_v172135_lock';
		$token = function_exists( 'wp_generate_uuid4' ) ? wp_generate_uuid4() : uniqid( 'utopia-', true );
		$value = array( 'token' => $token, 'acquired_at' => time() );
		if ( add_option( $key, $value, '', 'no' ) ) {
			return $token;
		}
		$existing = get_option( $key, array() );
		if ( is_array( $existing ) && ! empty( $existing['acquired_at'] ) && ( time() - (int) $existing['acquired_at'] ) > 900 ) {
			global $wpdb;
			if ( isset( $wpdb, $wpdb->options ) ) {
				$updated = $wpdb->query( $wpdb->prepare(
					"UPDATE {$wpdb->options} SET option_value = %s WHERE option_name = %s AND option_value = %s",
					maybe_serialize( $value ),
					$key,
					maybe_serialize( $existing )
				) );
				if ( (int) $updated === 1 ) {
					wp_cache_delete( $key, 'options' );
					$verified = get_option( $key, array() );
					if ( is_array( $verified ) && isset( $verified['token'] ) && hash_equals( $token, (string) $verified['token'] ) ) {
						return $token;
					}
				}
			}
		}
		return '';
	}
}

if ( ! function_exists( 'nadlan_utopia_release_lock' ) ) {
	function nadlan_utopia_release_lock( $token ) {
		$key      = 'nadlan_utopia_release_v172135_lock';
		$existing = get_option( $key, array() );
		if ( is_array( $existing ) && isset( $existing['token'] ) && hash_equals( (string) $existing['token'], (string) $token ) ) {
			delete_option( $key );
		}
	}
}

if ( ! function_exists( 'nadlan_utopia_release_context_allowed' ) ) {
	function nadlan_utopia_release_context_allowed() {
		if ( defined( 'WP_CLI' ) && WP_CLI ) { return false; }
		if ( ! function_exists( 'is_admin' ) || ! is_admin() ) { return false; }
		if ( function_exists( 'wp_doing_ajax' ) && wp_doing_ajax() ) { return false; }
		return nadlan_utopia_recovery_context_allowed();
	}
}

if ( ! function_exists( 'nadlan_utopia_recovery_context_allowed' ) ) {
	function nadlan_utopia_recovery_context_allowed() {
		return function_exists( 'current_user_can' )
			&& current_user_can( 'manage_options' )
			&& current_user_can( 'unfiltered_html' );
	}
}

if ( ! function_exists( 'nadlan_utopia_db_option' ) ) {
	/**
	 * Read a release-control option directly from MySQL.
	 *
	 * The atomic commit deliberately bypasses WordPress' object cache. A direct
	 * read here prevents a stale "notoptions" cache entry from starting a second
	 * release after MySQL has already committed the first one.
	 */
	function nadlan_utopia_db_option( $key, $default = false ) {
		global $wpdb;
		if ( ! isset( $wpdb, $wpdb->options ) || ! method_exists( $wpdb, 'prepare' ) || ! method_exists( $wpdb, 'get_var' ) ) {
			return get_option( $key, $default );
		}
		$value = $wpdb->get_var( $wpdb->prepare(
			"SELECT option_value FROM {$wpdb->options} WHERE option_name = %s LIMIT 1",
			(string) $key
		) );
		return $value === null ? $default : maybe_unserialize( $value );
	}
}

if ( ! function_exists( 'nadlan_utopia_release_complete' ) ) {
	function nadlan_utopia_release_complete() {
		return (string) nadlan_utopia_db_option( 'nadlan_utopia_release_v172135', '' ) === '1';
	}
}

if ( ! function_exists( 'nadlan_utopia_run_checksum' ) ) {
	function nadlan_utopia_run_checksum( $run ) {
		unset( $run['checksum'] );
		return hash( 'sha256', maybe_serialize( $run ) );
	}
}

if ( ! function_exists( 'nadlan_utopia_read_run' ) ) {
	function nadlan_utopia_read_run() {
		$run = get_option( 'nadlan_utopia_release_v172135_run', false );
		if ( $run === false ) { return false; }
		if ( ! is_array( $run ) || ! isset( $run['schema'], $run['token'], $run['checksum'] ) ||
			$run['schema'] !== 'nadlan-utopia-release-run/v1' ||
			! hash_equals( (string) $run['checksum'], nadlan_utopia_run_checksum( $run ) ) ) {
			return new WP_Error( 'utopia_run_invalid', 'UTOPIA release run journal is invalid.' );
		}
		return $run;
	}
}

if ( ! function_exists( 'nadlan_utopia_store_run' ) ) {
	function nadlan_utopia_store_run( $run, $create = false ) {
		$run['checksum'] = nadlan_utopia_run_checksum( $run );
		$stored = $create
			? add_option( 'nadlan_utopia_release_v172135_run', $run, '', 'no' )
			: update_option( 'nadlan_utopia_release_v172135_run', $run, false );
		if ( ! $stored && get_option( 'nadlan_utopia_release_v172135_run', false ) !== $run ) {
			return new WP_Error( 'utopia_run_write', 'Could not persist the UTOPIA release run journal.' );
		}
		$verified = nadlan_utopia_read_run();
		return is_wp_error( $verified ) ? $verified : true;
	}
}

if ( ! function_exists( 'nadlan_utopia_start_run' ) ) {
	function nadlan_utopia_start_run( $token ) {
		$run = array(
			'schema' => 'nadlan-utopia-release-run/v1',
			'token' => (string) $token,
			'started_at' => gmdate( 'c' ),
			'state' => 'prepared',
			'planned_slugs' => array_values( nadlan_utopia_release_slugs() ),
			'planned_files' => array(),
			'created_post_ids' => array(),
			'created_attachment_ids' => array(),
			'created_files' => array(),
		);
		return nadlan_utopia_store_run( $run, true );
	}
}

if ( ! function_exists( 'nadlan_utopia_update_run' ) ) {
	function nadlan_utopia_update_run( $token, $changes ) {
		$run = nadlan_utopia_read_run();
		if ( is_wp_error( $run ) ) { return $run; }
		if ( ! is_array( $run ) || ! isset( $run['token'] ) ||
			! hash_equals( (string) $run['token'], (string) $token ) ) {
			return new WP_Error( 'utopia_run_token', 'UTOPIA release run token does not match the journal.' );
		}
		foreach ( (array) $changes as $key => $value ) {
			$run[ $key ] = $value;
		}
		return nadlan_utopia_store_run( $run );
	}
}

if ( ! function_exists( 'nadlan_utopia_run_add_resource' ) ) {
	function nadlan_utopia_run_add_resource( $token, $key, $value ) {
		$allowed = array( 'planned_files', 'created_post_ids', 'created_attachment_ids', 'created_files' );
		if ( ! in_array( $key, $allowed, true ) ) {
			return new WP_Error( 'utopia_run_resource', 'Unknown UTOPIA run resource type.' );
		}
		$run = nadlan_utopia_read_run();
		if ( is_wp_error( $run ) ) { return $run; }
		if ( ! is_array( $run ) || ! isset( $run['token'] ) ||
			! hash_equals( (string) $run['token'], (string) $token ) ) {
			return new WP_Error( 'utopia_run_token', 'UTOPIA release run token does not match the journal.' );
		}
		if ( ! in_array( $value, $run[ $key ], true ) ) {
			$run[ $key ][] = $value;
		}
		return nadlan_utopia_store_run( $run );
	}
}

if ( ! function_exists( 'nadlan_utopia_run_tag' ) ) {
	function nadlan_utopia_run_tag( $token, $kind ) {
		return 'nadlan-utopia-run:' . (string) $token . ':' . sanitize_key( $kind );
	}
}

if ( ! function_exists( 'nadlan_utopia_discover_run_posts' ) ) {
	function nadlan_utopia_discover_run_posts( $token ) {
		global $wpdb;
		if ( ! isset( $wpdb, $wpdb->posts ) || ! method_exists( $wpdb, 'prepare' ) || ! method_exists( $wpdb, 'get_col' ) ) {
			return new WP_Error( 'utopia_run_query', 'WordPress database access is unavailable for UTOPIA recovery.' );
		}
		$prefix = 'nadlan-utopia-run:' . (string) $token . ':';
		$like   = method_exists( $wpdb, 'esc_like' ) ? $wpdb->esc_like( $prefix ) . '%' : $prefix . '%';
		$ids    = $wpdb->get_col( $wpdb->prepare(
			"SELECT ID FROM {$wpdb->posts} WHERE post_content_filtered LIKE %s AND post_type IN ('nadlan_project','attachment')",
			$like
		) );
		return array_map( 'intval', (array) $ids );
	}
}

if ( ! function_exists( 'nadlan_utopia_meta_equal' ) ) {
	function nadlan_utopia_meta_equal( $actual, $expected ) {
		if ( is_array( $expected ) || is_object( $expected ) ) {
			return maybe_serialize( $actual ) === maybe_serialize( $expected );
		}
		return (string) $actual === (string) $expected;
	}
}

if ( ! function_exists( 'nadlan_utopia_meta_payload' ) ) {
	function nadlan_utopia_meta_payload( $lang ) {
		$c = nadlan_utopia_copy( $lang );
		$asset = function ( $name ) { return nadlan_utopia_asset_url( $name ); };
		$plans = nadlan_utopia_sample_plans( $lang );
		$drawings = array();
		foreach ( $plans as $plan ) {
			$drawings[] = array(
				'title' => $plan['label'],
				'url' => $plan['url'],
				'type' => 'sample_floor_plan',
				'source' => 'UTOPIA official project website',
			);
		}
		return array(
			'developer_name' => $c['developer'],
			'contractor_name' => '',
			'architect_name' => $c['architect'],
			'address' => $c['address'],
			'city' => $c['city'],
			'neighborhood' => $c['neighborhood'],
			'project_type' => 'new_build',
			'project_status' => 'permits',
			'num_units' => 337,
			'num_buildings' => 4,
			'num_floors' => 34,
			'project_floors' => 34,
			'completion_year' => 0,
			'price_min' => 0,
			'price_max' => 0,
			'price_range' => '',
			'website' => 'https://utopiatlv.co.il/',
			'official_site_url' => 'https://utopiatlv.co.il/,https://www.nahmias-group.co.il/project/utopia-%D7%A9%D7%93%D7%94-%D7%93%D7%91-%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91/',
			'source' => 'Nahmias Group; Tel Aviv-Yafo Municipality; Israel Planning Administration',
			'source_url' => 'https://utopiatlv.co.il/',
			'source_id' => 'utopia-sde-dov-lot-103',
			'data_quality' => 'enriched',
			'lat' => '32.105979',
			'lng' => '34.784524',
			'geo_confidence' => 'planning-lot-centroid',
			'project_subtitle' => $c['excerpt'],
			'project_3d_image' => $asset( 'utopia-concept-exterior-v1.webp' ),
			'project_model_glb' => function_exists( 'nadlan_showroom_engine_base_url' ) ? trailingslashit( nadlan_showroom_engine_base_url() ) . 'models/utopia-rich-v1.glb' : '',
			'project_model_poster' => $asset( 'utopia-concept-exterior-v1.webp' ),
			'project_default_interior' => $asset( 'utopia-concept-interior-v1.webp' ),
			'project_3d_model_type' => 'gltf',
			'project_model_scale_floor_height_m' => '3.15',
			'project_model_asset_validated' => '1',
			'project_model_official' => '0',
			'project_model_kind' => 'independent_concept',
			'project_3d_demo' => '1',
			'project_3d_units' => '[]',
			'project_3d_facade_images' => '[]',
			'project_comps_json' => '[]',
			'project_faq_json' => '',
			'project_3d_avg_price_per_sqm' => '',
			'project_3d_price_source_note' => $c['price_note'],
			'project_price_updated' => '',
			'project_3d_drawings_json' => wp_json_encode( $drawings, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ),
			'project_3d_environment_json' => wp_json_encode( array( 'orientation' => $c['orientation'] ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ),
			'amenities' => '',
			'nlp3d_use_engine' => '1',
			'_yoast_wpseo_title' => $c['seo_title'],
			'_yoast_wpseo_metadesc' => $c['seo_desc'],
			'_yoast_wpseo_focuskw' => $c['focus'],
		);
	}
}

if ( ! function_exists( 'nadlan_utopia_mutated_meta_keys' ) ) {
	function nadlan_utopia_mutated_meta_keys( $lang ) {
		return array_values( array_unique( array_merge(
			array_keys( nadlan_utopia_meta_payload( $lang ) ),
			array( '_yoast_wpseo_canonical', '_nadlan_utopia_identity', '_thumbnail_id', 'project_3d_floor_height_m' )
		) ) );
	}
}

if ( ! function_exists( 'nadlan_utopia_backup_checksum' ) ) {
	function nadlan_utopia_backup_checksum( $backup ) {
		unset( $backup['checksum'] );
		return hash( 'sha256', maybe_serialize( $backup ) );
	}
}

if ( ! function_exists( 'nadlan_utopia_read_backup' ) ) {
	function nadlan_utopia_read_backup() {
		$backup = get_option( 'nadlan_utopia_backup_v172135', false );
		if ( ! is_array( $backup ) || ! isset( $backup['schema'], $backup['checksum'] ) ||
			$backup['schema'] !== 'nadlan-utopia-release-backup/v3' ||
			! hash_equals( (string) $backup['checksum'], nadlan_utopia_backup_checksum( $backup ) ) ) {
			return new WP_Error( 'utopia_backup_invalid', 'Verified UTOPIA release backup is missing or invalid.' );
		}
		return $backup;
	}
}

if ( ! function_exists( 'nadlan_utopia_store_backup' ) ) {
	function nadlan_utopia_store_backup( $backup ) {
		$backup['checksum'] = nadlan_utopia_backup_checksum( $backup );
		$changed = update_option( 'nadlan_utopia_backup_v172135', $backup, false );
		if ( ! $changed ) {
			$current = get_option( 'nadlan_utopia_backup_v172135', false );
			if ( $current !== $backup ) {
				return new WP_Error( 'utopia_backup_write', 'Could not update the verified UTOPIA release backup.' );
			}
		}
		$verified = nadlan_utopia_read_backup();
		return is_wp_error( $verified ) ? $verified : true;
	}
}

if ( ! function_exists( 'nadlan_utopia_backup_state' ) ) {
	function nadlan_utopia_backup_state( $posts ) {
		if ( get_option( 'nadlan_utopia_backup_v172135', false ) !== false ) {
			return nadlan_utopia_read_backup();
		}
		$backup = array(
			'schema' => 'nadlan-utopia-release-backup/v3',
			'captured_at' => gmdate( 'c' ),
			'posts' => array(),
			'created_post_ids' => array(),
			'created_attachment_ids' => array(),
			'created_files' => array(),
		);
		foreach ( nadlan_utopia_release_slugs() as $lang => $slug ) {
			$post = isset( $posts[ $lang ] ) ? get_post( $posts[ $lang ] ) : null;
			if ( ! $post ) {
				$backup['posts'][ $lang ] = array( 'exists' => false, 'slug' => $slug );
				continue;
			}
			$meta = array();
			foreach ( nadlan_utopia_mutated_meta_keys( $lang ) as $key ) {
				$meta[ $key ] = get_post_meta( $post->ID, $key, false );
			}
			$taxonomies = array();
			foreach ( array( 'nadlan_city', 'nadlan_compound' ) as $taxonomy ) {
				$terms = wp_get_object_terms( $post->ID, $taxonomy, array( 'fields' => 'ids' ) );
				if ( is_wp_error( $terms ) ) {
					return $terms;
				}
				$taxonomies[ $taxonomy ] = array_map( 'intval', $terms );
			}
			$backup['posts'][ $lang ] = array(
				'exists' => true,
				'id' => (int) $post->ID,
				'fields' => array(
					'post_name' => $post->post_name,
					'post_title' => $post->post_title,
					'post_content' => $post->post_content,
					'post_excerpt' => $post->post_excerpt,
					'post_status' => $post->post_status,
					'post_author' => (int) $post->post_author,
					'comment_status' => $post->comment_status,
					'ping_status' => $post->ping_status,
					'post_date' => $post->post_date,
					'post_date_gmt' => $post->post_date_gmt,
					'post_modified' => $post->post_modified,
					'post_modified_gmt' => $post->post_modified_gmt,
				),
				'meta' => $meta,
				'taxonomies' => $taxonomies,
				'revision_ids' => function_exists( 'wp_get_post_revisions' )
					? array_map( 'intval', array_keys( wp_get_post_revisions( $post->ID, array( 'check_enabled' => false ) ) ) )
					: array(),
			);
		}
		$backup['checksum'] = nadlan_utopia_backup_checksum( $backup );
		if ( ! add_option( 'nadlan_utopia_backup_v172135', $backup, '', 'no' ) ) {
			return new WP_Error( 'utopia_backup_create', 'Could not create the verified UTOPIA release backup.' );
		}
		$verified = nadlan_utopia_read_backup();
		return is_wp_error( $verified ) ? $verified : $verified;
	}
}

if ( ! function_exists( 'nadlan_utopia_record_created_resource' ) ) {
	function nadlan_utopia_record_created_resource( $key, $value ) {
		$allowed = array( 'created_post_ids', 'created_attachment_ids', 'created_files' );
		if ( ! in_array( $key, $allowed, true ) ) {
			return new WP_Error( 'utopia_backup_resource', 'Unknown UTOPIA backup resource type.' );
		}
		$backup = nadlan_utopia_read_backup();
		if ( is_wp_error( $backup ) ) { return $backup; }
		if ( ! in_array( $value, $backup[ $key ], true ) ) {
			$backup[ $key ][] = $value;
		}
		return nadlan_utopia_store_backup( $backup );
	}
}

if ( ! function_exists( 'nadlan_utopia_restore_post_dates' ) ) {
	function nadlan_utopia_restore_post_dates( $post_id, $fields ) {
		global $wpdb;
		$date_fields = array();
		foreach ( array( 'post_date', 'post_date_gmt', 'post_modified', 'post_modified_gmt' ) as $field ) {
			if ( array_key_exists( $field, $fields ) ) {
				$date_fields[ $field ] = (string) $fields[ $field ];
			}
		}
		if ( count( $date_fields ) !== 4 || ! isset( $wpdb, $wpdb->posts ) || ! method_exists( $wpdb, 'update' ) ) {
			return new WP_Error( 'utopia_restore_dates', 'WordPress database access is unavailable for exact UTOPIA timestamp restoration.' );
		}
		$result = $wpdb->update( $wpdb->posts, $date_fields, array( 'ID' => (int) $post_id ), array( '%s', '%s', '%s', '%s' ), array( '%d' ) );
		if ( $result === false ) {
			return new WP_Error( 'utopia_restore_dates', 'Could not restore exact UTOPIA post timestamps.' );
		}
		if ( function_exists( 'clean_post_cache' ) ) { clean_post_cache( $post_id ); }
		return true;
	}
}

if ( ! function_exists( 'nadlan_utopia_restore_revisions' ) ) {
	function nadlan_utopia_restore_revisions( $post_id, $baseline_ids ) {
		if ( ! function_exists( 'wp_get_post_revisions' ) ) { return true; }
		$baseline = array_values( array_unique( array_map( 'intval', (array) $baseline_ids ) ) );
		$current  = array_map( 'intval', array_keys( wp_get_post_revisions( $post_id, array( 'check_enabled' => false ) ) ) );
		foreach ( array_diff( $current, $baseline ) as $revision_id ) {
			if ( ! wp_delete_post( $revision_id, true ) || get_post( $revision_id ) ) {
				return new WP_Error( 'utopia_restore_revision', 'Could not remove release-created revision ' . (int) $revision_id . '.' );
			}
		}
		$remaining = array_map( 'intval', array_keys( wp_get_post_revisions( $post_id, array( 'check_enabled' => false ) ) ) );
		sort( $baseline );
		sort( $remaining );
		return $remaining === $baseline
			? true
			: new WP_Error( 'utopia_restore_revision', 'UTOPIA revision history did not return to its verified baseline.' );
	}
}

if ( ! function_exists( 'nadlan_utopia_restore_backup' ) ) {
	function nadlan_utopia_restore_backup( $extra_resources = array(), $operator_hold = false, $run_token = '' ) {
		$backup = nadlan_utopia_read_backup();
		if ( is_wp_error( $backup ) ) {
			update_option( 'nadlan_utopia_release_v172135_hold', 'blocked-recovery', false );
			return $backup;
		}
		$errors = array();
		$run    = nadlan_utopia_read_run();
		if ( is_wp_error( $run ) ) {
			update_option( 'nadlan_utopia_release_v172135_hold', 'blocked-recovery', false );
			return $run;
		}
		if ( is_array( $run ) ) {
			if ( $run_token === '' ) { $run_token = (string) $run['token']; }
			foreach ( array( 'created_post_ids', 'created_attachment_ids', 'created_files' ) as $key ) {
				$values = isset( $run[ $key ] ) ? (array) $run[ $key ] : array();
				$extra_resources[ $key ] = array_merge( isset( $extra_resources[ $key ] ) ? (array) $extra_resources[ $key ] : array(), $values );
			}
			$extra_resources['created_files'] = array_merge(
				isset( $extra_resources['created_files'] ) ? (array) $extra_resources['created_files'] : array(),
				isset( $run['planned_files'] ) ? (array) $run['planned_files'] : array()
			);
		}
		if ( $run_token !== '' ) {
			$discovered = nadlan_utopia_discover_run_posts( $run_token );
			if ( is_wp_error( $discovered ) ) {
				$errors[] = $discovered->get_error_message();
			} else {
				foreach ( $discovered as $post_id ) {
					$post = get_post( $post_id );
					if ( ! $post ) { continue; }
					$key = $post->post_type === 'attachment' ? 'created_attachment_ids' : 'created_post_ids';
					$extra_resources[ $key ][] = (int) $post_id;
				}
			}
		}

		$created_posts = array_unique( array_map( 'intval', array_merge(
			$backup['created_post_ids'],
			isset( $extra_resources['created_post_ids'] ) ? (array) $extra_resources['created_post_ids'] : array()
		) ) );
		foreach ( array_reverse( $created_posts ) as $post_id ) {
			$post = get_post( $post_id );
			if ( ! $post ) { continue; }
			$marker    = (string) get_post_meta( $post->ID, '_nadlan_utopia_identity', true );
			$run_field = isset( $post->post_content_filtered ) ? (string) $post->post_content_filtered : '';
			$owned     = strpos( $marker, 'nadlan-utopia:lot-103:base-4749:' ) === 0 ||
				( $run_token !== '' && strpos( $run_field, 'nadlan-utopia-run:' . $run_token . ':' ) === 0 );
			if ( ! $owned ) {
				$errors[] = 'Refused to remove an unmarked post ' . $post_id . '.';
				continue;
			}
			if ( ! wp_delete_post( $post->ID, true ) || get_post( $post_id ) ) {
				$errors[] = 'Could not remove created post ' . $post_id . '.';
			}
		}

		foreach ( $backup['posts'] as $lang => $state ) {
			if ( empty( $state['exists'] ) ) { continue; }
			$post_id = (int) $state['id'];
			if ( ! get_post( $post_id ) ) {
				$errors[] = 'Backup target post is missing: ' . $post_id . '.';
				continue;
			}
			$updated = wp_update_post( wp_slash( array_merge( array( 'ID' => $post_id ), $state['fields'] ) ), true );
			if ( is_wp_error( $updated ) || (int) $updated !== $post_id ) {
				$errors[] = 'Could not restore post fields for ' . $post_id . '.';
				continue;
			}
			$dates = nadlan_utopia_restore_post_dates( $post_id, $state['fields'] );
			if ( is_wp_error( $dates ) ) {
				$errors[] = $dates->get_error_message();
				continue;
			}
			foreach ( nadlan_utopia_mutated_meta_keys( $lang ) as $key ) {
				delete_post_meta( $post_id, $key );
				$values = isset( $state['meta'][ $key ] ) ? $state['meta'][ $key ] : array();
				foreach ( $values as $value ) {
					if ( add_post_meta( $post_id, $key, $value ) === false ) {
						$errors[] = 'Could not restore meta ' . $key . ' for ' . $post_id . '.';
					}
				}
			}
			foreach ( array( 'nadlan_city', 'nadlan_compound' ) as $taxonomy ) {
				$terms  = isset( $state['taxonomies'][ $taxonomy ] ) ? array_map( 'intval', $state['taxonomies'][ $taxonomy ] ) : array();
				$result = wp_set_object_terms( $post_id, $terms, $taxonomy, false );
				if ( is_wp_error( $result ) ) {
					$errors[] = 'Could not restore ' . $taxonomy . ' for ' . $post_id . '.';
				}
			}

			$restored = get_post( $post_id );
			foreach ( $state['fields'] as $field => $expected ) {
				$actual = $restored && isset( $restored->{$field} ) ? $restored->{$field} : null;
				if ( (string) $actual !== (string) $expected ) {
					$errors[] = 'Post field readback mismatch for ' . $post_id . ': ' . $field . '.';
				}
			}
			foreach ( nadlan_utopia_mutated_meta_keys( $lang ) as $key ) {
				$expected = isset( $state['meta'][ $key ] ) ? array_values( $state['meta'][ $key ] ) : array();
				$actual   = array_values( get_post_meta( $post_id, $key, false ) );
				if ( maybe_serialize( $actual ) !== maybe_serialize( $expected ) ) {
					$errors[] = 'Post meta readback mismatch for ' . $post_id . ': ' . $key . '.';
				}
			}
			foreach ( array( 'nadlan_city', 'nadlan_compound' ) as $taxonomy ) {
				$expected = isset( $state['taxonomies'][ $taxonomy ] ) ? array_map( 'intval', $state['taxonomies'][ $taxonomy ] ) : array();
				$actual   = wp_get_object_terms( $post_id, $taxonomy, array( 'fields' => 'ids' ) );
				if ( is_wp_error( $actual ) ) {
					$errors[] = 'Could not read back ' . $taxonomy . ' for ' . $post_id . '.';
					continue;
				}
				$actual = array_map( 'intval', $actual );
				sort( $expected );
				sort( $actual );
				if ( $actual !== $expected ) {
					$errors[] = 'Taxonomy readback mismatch for ' . $post_id . ': ' . $taxonomy . '.';
				}
			}
			$revisions = nadlan_utopia_restore_revisions(
				$post_id,
				isset( $state['revision_ids'] ) ? $state['revision_ids'] : array()
			);
			if ( is_wp_error( $revisions ) ) {
				$errors[] = $revisions->get_error_message();
			}
		}

		$created_attachments = array_unique( array_map( 'intval', array_merge(
			$backup['created_attachment_ids'],
			isset( $extra_resources['created_attachment_ids'] ) ? (array) $extra_resources['created_attachment_ids'] : array()
		) ) );
		foreach ( array_reverse( $created_attachments ) as $attachment_id ) {
			$post = get_post( $attachment_id );
			if ( ! $post ) { continue; }
			$run_field = isset( $post->post_content_filtered ) ? (string) $post->post_content_filtered : '';
			$owned = get_post_meta( $attachment_id, '_nadlan_utopia_concept_asset', true ) === 'exterior-v1' ||
				( $run_token !== '' && strpos( $run_field, 'nadlan-utopia-run:' . $run_token . ':' ) === 0 );
			if ( ! $owned ) {
				$errors[] = 'Refused to remove an unmarked attachment ' . $attachment_id . '.';
				continue;
			}
			if ( ! wp_delete_attachment( $attachment_id, true ) || get_post( $attachment_id ) ) {
				$errors[] = 'Could not remove created attachment ' . $attachment_id . '.';
			}
		}

		$created_files = array_unique( array_merge(
			$backup['created_files'],
			isset( $extra_resources['created_files'] ) ? (array) $extra_resources['created_files'] : array()
		) );
		$uploads = wp_upload_dir();
		$base    = isset( $uploads['basedir'] ) ? trailingslashit( wp_normalize_path( $uploads['basedir'] ) ) : '';
		foreach ( $created_files as $file ) {
			$normalized = wp_normalize_path( $file );
			if ( $base === '' || strpos( $normalized, $base ) !== 0 || basename( $normalized ) !== 'utopia-sde-dov-independent-concept-v1.webp' ) {
				$errors[] = 'Refused to remove an unexpected file path.';
				continue;
			}
			if ( file_exists( $file ) ) {
				wp_delete_file( $file );
				if ( file_exists( $file ) ) {
					$errors[] = 'Could not remove created UTOPIA concept file.';
				}
			}
		}

		foreach ( $created_posts as $post_id ) {
			if ( get_post( $post_id ) ) { $errors[] = 'Created post still exists after restore: ' . $post_id . '.'; }
		}
		foreach ( $created_attachments as $attachment_id ) {
			if ( get_post( $attachment_id ) ) { $errors[] = 'Created attachment still exists after restore: ' . $attachment_id . '.'; }
		}

		if ( ! empty( $errors ) ) {
			update_option( 'nadlan_utopia_release_v172135_hold', 'blocked-recovery', false );
			return new WP_Error( 'utopia_restore_failed', implode( ' ', array_unique( $errors ) ) );
		}
		delete_option( 'nadlan_utopia_release_v172135' );
		delete_option( 'nadlan_utopia_release_v172135_manifest' );
		delete_option( 'nadlan_utopia_release_v172135_run' );
		if ( $operator_hold ) {
			update_option( 'nadlan_utopia_release_v172135_hold', 'operator', false );
		} else {
			delete_option( 'nadlan_utopia_release_v172135_hold' );
			delete_option( 'nadlan_utopia_backup_v172135' );
		}
		return true;
	}
}

if ( ! function_exists( 'nadlan_utopia_runtime_asset_manifest' ) ) {
	function nadlan_utopia_runtime_asset_manifest() {
		$root = dirname( __DIR__ ) . '/assets/showroom-engine/';
		return array(
			'model' => array(
				'path' => $root . 'models/utopia-rich-v1.glb',
				'sha256' => 'ba267a241f7b5d943f5eebd6f32aae9241f14da420207ddadc4d5d74ac392f24',
			),
			'exterior' => array(
				'path' => $root . 'projects/utopia-sde-dov/utopia-concept-exterior-v1.webp',
				'sha256' => '55122e051450af3e2715af36df05837e06f96f73db9f8291bf4a3f3e8dc263c6',
			),
			'interior' => array(
				'path' => $root . 'projects/utopia-sde-dov/utopia-concept-interior-v1.webp',
				'sha256' => 'd89457f00cd52385107072902e7df06fab3750f16b9b18a923396398b59d7c6b',
			),
			'window_view' => array(
				'path' => $root . 'projects/utopia-sde-dov/utopia-concept-window-view-v1.webp',
				'sha256' => '995a982ea8aed6ded92f3ac30c86c86b20737dd5f20b371a9cf8a4aea2c5f9f4',
			),
			'wellness' => array(
				'path' => $root . 'projects/utopia-sde-dov/utopia-concept-wellness-v1.webp',
				'sha256' => 'c1d1a1a53b85fc61ad1c39598f4a0a404b92cb4144d3a51c2093cbaabe046a61',
			),
			'showroom_css' => array(
				'path' => $root . 'projects/utopia-sde-dov/utopia.css',
				'sha256' => 'c63c5287b9e9b495ec217ae549f6b20164367b292b22f7c1a19cb3c743419ef0',
			),
			'showroom_js' => array(
				'path' => $root . 'projects/utopia-sde-dov/utopia-showroom.js',
				'sha256' => 'bce8e9afecd34eba36b327c725a7ae39ce3d6cf7eb86b27749b8a745a9ea3227',
			),
		);
	}
}

if ( ! function_exists( 'nadlan_utopia_validate_runtime_assets' ) ) {
	function nadlan_utopia_validate_runtime_assets() {
		foreach ( nadlan_utopia_runtime_asset_manifest() as $name => $asset ) {
			if ( ! is_readable( $asset['path'] ) ) {
				return new WP_Error( 'utopia_asset_missing', 'UTOPIA runtime asset is missing: ' . $name . '.' );
			}
			$actual = hash_file( 'sha256', $asset['path'] );
			if ( ! is_string( $actual ) || ! hash_equals( $asset['sha256'], $actual ) ) {
				return new WP_Error( 'utopia_asset_hash', 'UTOPIA runtime asset hash mismatch: ' . $name . '.' );
			}
		}
		return true;
	}
}

if ( ! function_exists( 'nadlan_utopia_validate_concept_attachment' ) ) {
	function nadlan_utopia_validate_concept_attachment( $attachment_id ) {
		$attachment_id = (int) $attachment_id;
		$post          = get_post( $attachment_id );
		$manifest      = nadlan_utopia_runtime_asset_manifest();
		$path          = function_exists( 'get_attached_file' ) ? get_attached_file( $attachment_id, true ) : '';
		$mime          = function_exists( 'get_post_mime_type' ) ? get_post_mime_type( $attachment_id ) : ( $post && isset( $post->post_mime_type ) ? $post->post_mime_type : '' );
		$alt           = (string) get_post_meta( $attachment_id, '_wp_attachment_image_alt', true );
		if ( ! $post || $post->post_type !== 'attachment' || $post->post_status !== 'inherit' ||
			get_post_meta( $attachment_id, '_nadlan_utopia_concept_asset', true ) !== 'exterior-v1' ||
			$mime !== 'image/webp' || ! is_string( $path ) || ! is_readable( $path ) ||
			$alt !== 'UTOPIA Sde Dov - independent concept illustration based on public planning data.' ) {
			return new WP_Error( 'utopia_attachment_invalid', 'The tracked UTOPIA concept attachment is incomplete or does not match its public disclosure.' );
		}
		$actual = hash_file( 'sha256', $path );
		if ( ! is_string( $actual ) || ! hash_equals( $manifest['exterior']['sha256'], $actual ) ) {
			return new WP_Error( 'utopia_attachment_hash', 'The tracked UTOPIA concept attachment does not match the verified exterior asset.' );
		}
		return true;
	}
}

if ( ! function_exists( 'nadlan_utopia_concept_attachment' ) ) {
	function nadlan_utopia_concept_attachment( &$resources, $run_token ) {
		$found = get_posts( array(
			'post_type' => 'attachment',
			'post_status' => 'inherit',
			'posts_per_page' => 2,
			'fields' => 'ids',
			'meta_key' => '_nadlan_utopia_concept_asset',
			'meta_value' => 'exterior-v1',
		) );
		if ( count( $found ) > 1 ) {
			return new WP_Error( 'utopia_attachment_duplicate', 'More than one attachment claims the UTOPIA exterior concept marker.' );
		}
		if ( ! empty( $found ) ) {
			$validated = nadlan_utopia_validate_concept_attachment( (int) $found[0] );
			return is_wp_error( $validated ) ? $validated : (int) $found[0];
		}
		$manifest = nadlan_utopia_runtime_asset_manifest();
		$src      = $manifest['exterior']['path'];
		$uploads = wp_upload_dir();
		if ( ! empty( $uploads['error'] ) || empty( $uploads['path'] ) || empty( $uploads['url'] ) ) {
			return new WP_Error( 'utopia_uploads', 'WordPress uploads directory is unavailable.' );
		}
		$name = 'utopia-sde-dov-independent-concept-v1.webp';
		$dst  = trailingslashit( $uploads['path'] ) . $name;
		if ( file_exists( $dst ) ) {
			return new WP_Error( 'utopia_concept_collision', 'An untracked UTOPIA concept file already exists.' );
		}
		$planned = nadlan_utopia_run_add_resource( $run_token, 'planned_files', $dst );
		if ( is_wp_error( $planned ) ) { return $planned; }
		if ( ! copy( $src, $dst ) ) {
			return new WP_Error( 'utopia_concept_copy', 'Could not copy the UTOPIA concept asset.' );
		}
		$resources['created_files'][] = $dst;
		$run_recorded = nadlan_utopia_run_add_resource( $run_token, 'created_files', $dst );
		if ( is_wp_error( $run_recorded ) ) { return $run_recorded; }
		$recorded = nadlan_utopia_record_created_resource( 'created_files', $dst );
		if ( is_wp_error( $recorded ) ) { return $recorded; }

		$type = wp_check_filetype( $name, null );
		$id = wp_insert_attachment( array(
			'post_mime_type' => $type['type'] ? $type['type'] : 'image/webp',
			'post_title' => 'UTOPIA Sde Dov',
			'post_content' => '',
			'post_content_filtered' => nadlan_utopia_run_tag( $run_token, 'attachment' ),
			'post_status' => 'inherit',
			'guid' => trailingslashit( $uploads['url'] ) . $name,
		), $dst, 0, true );
		if ( is_wp_error( $id ) || ! $id ) {
			return is_wp_error( $id ) ? $id : new WP_Error( 'utopia_attachment', 'Could not create the UTOPIA concept attachment.' );
		}
		$id = (int) $id;
		$resources['created_attachment_ids'][] = $id;
		$run_recorded = nadlan_utopia_run_add_resource( $run_token, 'created_attachment_ids', $id );
		if ( is_wp_error( $run_recorded ) ) { return $run_recorded; }
		$recorded = nadlan_utopia_record_created_resource( 'created_attachment_ids', $id );
		if ( is_wp_error( $recorded ) ) { return $recorded; }

		update_post_meta( $id, '_nadlan_utopia_concept_asset', 'exterior-v1' );
		update_post_meta( $id, '_wp_attachment_image_alt', 'UTOPIA Sde Dov - independent concept illustration based on public planning data.' );
		if ( get_post_meta( $id, '_nadlan_utopia_concept_asset', true ) !== 'exterior-v1' ) {
			return new WP_Error( 'utopia_attachment_marker', 'Could not verify the UTOPIA concept attachment.' );
		}
		require_once ABSPATH . 'wp-admin/includes/image.php';
		$metadata = wp_generate_attachment_metadata( $id, $dst );
		if ( is_array( $metadata ) ) {
			wp_update_attachment_metadata( $id, $metadata );
		}
		$validated = nadlan_utopia_validate_concept_attachment( $id );
		return is_wp_error( $validated ) ? $validated : $id;
	}
}

if ( ! function_exists( 'nadlan_utopia_set_verified_meta' ) ) {
	function nadlan_utopia_set_verified_meta( $post_id, $key, $value ) {
		update_post_meta( $post_id, $key, $value );
		return nadlan_utopia_meta_equal( get_post_meta( $post_id, $key, true ), $value );
	}
}

if ( ! function_exists( 'nadlan_utopia_stage_post' ) ) {
	function nadlan_utopia_stage_post( $post_id, $lang, $article, $thumbnail_id, $taxonomies, $stage_status ) {
		$slugs = nadlan_utopia_release_slugs();
		$c     = nadlan_utopia_copy( $lang );
		$stage_status = $stage_status === 'publish' ? 'publish' : 'draft';
		$updated = wp_update_post( wp_slash( array(
			'ID' => (int) $post_id,
			'post_name' => $slugs[ $lang ],
			'post_title' => $c['post_title'],
			'post_content' => $article,
			'post_excerpt' => $c['excerpt'],
			'post_status' => $stage_status,
			'comment_status' => 'closed',
			'ping_status' => 'closed',
		) ), true );
		if ( is_wp_error( $updated ) || (int) $updated !== (int) $post_id ) {
			return is_wp_error( $updated ) ? $updated : new WP_Error( 'utopia_stage_post', 'Could not stage UTOPIA post ' . (int) $post_id . '.' );
		}
		foreach ( nadlan_utopia_meta_payload( $lang ) as $key => $value ) {
			if ( ! nadlan_utopia_set_verified_meta( $post_id, $key, $value ) ) {
				return new WP_Error( 'utopia_stage_meta', 'Could not verify meta ' . $key . ' for UTOPIA post ' . (int) $post_id . '.' );
			}
		}
		delete_post_meta( $post_id, 'project_3d_floor_height_m' );
		if ( get_post_meta( $post_id, 'project_3d_floor_height_m', false ) !== array() ) {
			return new WP_Error( 'utopia_stage_legacy_meta', 'Could not remove legacy model floor-height metadata.' );
		}
		if ( ! nadlan_utopia_set_verified_meta( $post_id, '_yoast_wpseo_canonical', nadlan_utopia_expected_canonical( $lang ) ) ||
			! nadlan_utopia_set_verified_meta( $post_id, '_nadlan_utopia_identity', nadlan_utopia_identity_marker( $lang ) ) ) {
			return new WP_Error( 'utopia_stage_identity', 'Could not verify UTOPIA canonical or identity metadata.' );
		}
		set_post_thumbnail( $post_id, $thumbnail_id );
		if ( (int) get_post_thumbnail_id( $post_id ) !== (int) $thumbnail_id ) {
			return new WP_Error( 'utopia_stage_thumbnail', 'Could not verify UTOPIA featured media.' );
		}
		foreach ( array( 'nadlan_city', 'nadlan_compound' ) as $taxonomy ) {
			$terms  = isset( $taxonomies[ $taxonomy ] ) ? array_map( 'intval', $taxonomies[ $taxonomy ] ) : array();
			$result = wp_set_object_terms( $post_id, $terms, $taxonomy, false );
			if ( is_wp_error( $result ) ) { return $result; }
			$actual = wp_get_object_terms( $post_id, $taxonomy, array( 'fields' => 'ids' ) );
			if ( is_wp_error( $actual ) ) { return $actual; }
			$actual = array_map( 'intval', $actual );
			sort( $actual );
			sort( $terms );
			if ( $actual !== $terms ) {
				return new WP_Error( 'utopia_stage_taxonomy', 'Could not verify ' . $taxonomy . ' for UTOPIA post ' . (int) $post_id . '.' );
			}
		}
		return true;
	}
}

if ( ! function_exists( 'nadlan_utopia_validate_staged_post' ) ) {
	function nadlan_utopia_validate_staged_post( $post_id, $lang, $article, $thumbnail_id, $expected_status ) {
		$post     = get_post( $post_id );
		$slugs    = nadlan_utopia_release_slugs();
		$manifest = nadlan_utopia_article_manifest();
		if ( ! $post || $post->post_type !== 'nadlan_project' || $post->post_name !== $slugs[ $lang ] ||
			$post->post_status !== $expected_status || ! hash_equals( $manifest[ $lang ]['sha256'], hash( 'sha256', (string) $post->post_content ) ) ||
			! hash_equals( hash( 'sha256', $article ), hash( 'sha256', (string) $post->post_content ) ) ) {
			return new WP_Error( 'utopia_stage_validation', 'Staged UTOPIA post validation failed for ' . $lang . '.' );
		}
		if ( get_post_meta( $post_id, '_nadlan_utopia_identity', true ) !== nadlan_utopia_identity_marker( $lang ) ||
			get_post_meta( $post_id, '_yoast_wpseo_canonical', true ) !== nadlan_utopia_expected_canonical( $lang ) ||
			(int) get_post_thumbnail_id( $post_id ) !== (int) $thumbnail_id ) {
			return new WP_Error( 'utopia_stage_validation_meta', 'Staged UTOPIA identity, canonical or media validation failed for ' . $lang . '.' );
		}
		foreach ( nadlan_utopia_meta_payload( $lang ) as $key => $value ) {
			if ( ! nadlan_utopia_meta_equal( get_post_meta( $post_id, $key, true ), $value ) ) {
				return new WP_Error( 'utopia_stage_validation_payload', 'Staged UTOPIA payload validation failed for ' . $lang . ': ' . $key );
			}
		}
		return true;
	}
}

if ( ! function_exists( 'nadlan_utopia_transactional_tables_ready' ) ) {
	function nadlan_utopia_transactional_tables_ready() {
		global $wpdb;
		$required = array( 'posts', 'postmeta', 'term_relationships', 'term_taxonomy', 'options' );
		foreach ( $required as $property ) {
			if ( ! isset( $wpdb->{$property} ) ) {
				return new WP_Error( 'utopia_transaction_table', 'A required WordPress table is unavailable for the atomic UTOPIA release.' );
			}
			$engine = $wpdb->get_var( $wpdb->prepare(
				'SELECT ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s',
				$wpdb->{$property}
			) );
			if ( ! in_array( strtoupper( (string) $engine ), array( 'INNODB', 'XTRADB' ), true ) ) {
				return new WP_Error( 'utopia_transaction_engine', 'UTOPIA release requires transactional WordPress tables; ' . $wpdb->{$property} . ' is not transactional.' );
			}
		}
		return true;
	}
}

if ( ! function_exists( 'nadlan_utopia_begin_release_transaction' ) ) {
	function nadlan_utopia_begin_release_transaction() {
		global $wpdb;
		$ready = nadlan_utopia_transactional_tables_ready();
		if ( is_wp_error( $ready ) ) { return $ready; }
		$cache_addition = function_exists( 'wp_suspend_cache_addition' ) ? (bool) wp_suspend_cache_addition() : false;
		if ( function_exists( 'wp_suspend_cache_addition' ) ) { wp_suspend_cache_addition( true ); }
		if ( $wpdb->query( 'START TRANSACTION' ) === false ) {
			if ( function_exists( 'wp_suspend_cache_addition' ) ) { wp_suspend_cache_addition( $cache_addition ); }
			return new WP_Error( 'utopia_transaction_begin', 'Could not begin the atomic UTOPIA database transaction.' );
		}
		return array( 'cache_addition' => $cache_addition );
	}
}

if ( ! function_exists( 'nadlan_utopia_transaction_set_option' ) ) {
	function nadlan_utopia_transaction_set_option( $key, $value ) {
		global $wpdb;
		$result = $wpdb->query( $wpdb->prepare(
			"INSERT INTO {$wpdb->options} (option_name, option_value, autoload) VALUES (%s, %s, 'no')
			 ON DUPLICATE KEY UPDATE option_value = VALUES(option_value), autoload = 'no'",
			(string) $key,
			maybe_serialize( $value )
		) );
		return $result === false
			? new WP_Error( 'utopia_transaction_option', 'Could not write atomic UTOPIA release option ' . $key . '.' )
			: true;
	}
}

if ( ! function_exists( 'nadlan_utopia_transaction_delete_option' ) ) {
	function nadlan_utopia_transaction_delete_option( $key ) {
		global $wpdb;
		$result = $wpdb->query( $wpdb->prepare(
			"DELETE FROM {$wpdb->options} WHERE option_name = %s",
			(string) $key
		) );
		return $result === false
			? new WP_Error( 'utopia_transaction_option', 'Could not delete atomic UTOPIA release option ' . $key . '.' )
			: true;
	}
}

if ( ! function_exists( 'nadlan_utopia_finish_release_transaction' ) ) {
	function nadlan_utopia_finish_release_transaction( $transaction, $commit, $post_ids = array() ) {
		global $wpdb;
		$sql    = $commit ? 'COMMIT' : 'ROLLBACK';
		$result = $wpdb->query( $sql );
		if ( function_exists( 'wp_suspend_cache_addition' ) ) {
			wp_suspend_cache_addition( ! empty( $transaction['cache_addition'] ) );
		}
		foreach ( array_unique( array_map( 'intval', (array) $post_ids ) ) as $post_id ) {
			if ( function_exists( 'clean_post_cache' ) ) { clean_post_cache( $post_id ); }
		}
		foreach ( array(
			'nadlan_utopia_release_v172135',
			'nadlan_utopia_release_v172135_manifest',
			'nadlan_utopia_release_v172135_run',
			'nadlan_utopia_release_v172135_error',
		) as $key ) {
			wp_cache_delete( $key, 'options' );
		}
		return $result === false
			? new WP_Error( 'utopia_transaction_finish', 'Could not ' . strtolower( $sql ) . ' the atomic UTOPIA database transaction.' )
			: true;
	}
}

if ( ! function_exists( 'nadlan_utopia_seed_v172135' ) ) {
	function nadlan_utopia_seed_v172135() {
		if ( nadlan_utopia_release_complete() ) { return; }
		if ( get_option( 'nadlan_utopia_release_v172135_hold', false ) !== false ) { return; }
		if ( ! nadlan_utopia_release_context_allowed() ) { return; }
		$lock = nadlan_utopia_acquire_release_lock();
		if ( $lock === '' ) { return; }
		$resources = array( 'created_post_ids' => array(), 'created_attachment_ids' => array(), 'created_files' => array() );
		$backup_ready = false;
		$run_started  = false;
		$transaction  = false;
		$committed    = false;
		$ids          = array();

		try {
			$prior_run = nadlan_utopia_read_run();
			if ( is_wp_error( $prior_run ) ) {
				update_option( 'nadlan_utopia_release_v172135_hold', 'blocked-recovery', false );
				throw new RuntimeException( $prior_run->get_error_message() );
			}
			if ( is_array( $prior_run ) ) {
				$recovered = nadlan_utopia_restore_backup( array(), false, (string) $prior_run['token'] );
				if ( is_wp_error( $recovered ) ) { throw new RuntimeException( $recovered->get_error_message() ); }
			}

			$slugs = nadlan_utopia_release_slugs();
			$langs = array_keys( $slugs );
			$posts = array();
			$base  = get_post( 4749 );
			$identity = nadlan_utopia_validate_existing_identity( $base, 'he', true );
			if ( is_wp_error( $identity ) ) { throw new RuntimeException( $identity->get_error_message() ); }
			$posts['he'] = $base;

			foreach ( array( 'en', 'fr', 'ru', 'ar' ) as $lang ) {
				$post = get_page_by_path( $slugs[ $lang ], OBJECT, 'nadlan_project' );
				if ( $post ) {
					$identity = nadlan_utopia_validate_existing_identity( $post, $lang, false );
					if ( is_wp_error( $identity ) ) { throw new RuntimeException( $identity->get_error_message() ); }
				}
				$posts[ $lang ] = $post;
			}

			$articles = array();
			foreach ( $langs as $lang ) {
				$article = nadlan_utopia_validate_article( $lang, nadlan_utopia_article_path( $lang ) );
				if ( is_wp_error( $article ) ) { throw new RuntimeException( $article->get_error_message() ); }
				$articles[ $lang ] = $article;
			}
			$assets = nadlan_utopia_validate_runtime_assets();
			if ( is_wp_error( $assets ) ) { throw new RuntimeException( $assets->get_error_message() ); }

			$backup = nadlan_utopia_backup_state( $posts );
			if ( is_wp_error( $backup ) ) { throw new RuntimeException( $backup->get_error_message() ); }
			$backup_ready = true;
			$started = nadlan_utopia_start_run( $lock );
			if ( is_wp_error( $started ) ) { throw new RuntimeException( $started->get_error_message() ); }
			$run_started = true;

			$base_taxonomies = array();
			foreach ( array( 'nadlan_city', 'nadlan_compound' ) as $taxonomy ) {
				$terms = wp_get_object_terms( $base->ID, $taxonomy, array( 'fields' => 'ids' ) );
				if ( is_wp_error( $terms ) ) { throw new RuntimeException( $terms->get_error_message() ); }
				$base_taxonomies[ $taxonomy ] = array_map( 'intval', $terms );
			}

			$ids = array( 'he' => (int) $base->ID );
			$stage_statuses = array(
				'he' => $base->post_status === 'publish' ? 'publish' : 'draft',
			);
			foreach ( array( 'en', 'fr', 'ru', 'ar' ) as $lang ) {
				if ( $posts[ $lang ] ) {
					$ids[ $lang ] = (int) $posts[ $lang ]->ID;
					$stage_statuses[ $lang ] = $posts[ $lang ]->post_status === 'publish' ? 'publish' : 'draft';
					continue;
				}
				$c = nadlan_utopia_copy( $lang );
				$id = wp_insert_post( wp_slash( array(
					'post_type' => 'nadlan_project',
					'post_status' => 'draft',
					'post_name' => $slugs[ $lang ],
					'post_title' => $c['post_title'],
					'post_content' => '',
					'post_content_filtered' => nadlan_utopia_run_tag( $lock, 'project-' . $lang ),
					'post_excerpt' => $c['excerpt'],
					'post_author' => (int) $base->post_author,
					'comment_status' => 'closed',
					'ping_status' => 'closed',
				) ), true );
				if ( is_wp_error( $id ) || ! $id ) {
					throw new RuntimeException( is_wp_error( $id ) ? $id->get_error_message() : 'Could not create UTOPIA translation draft.' );
				}
				$id = (int) $id;
				$resources['created_post_ids'][] = $id;
				$run_recorded = nadlan_utopia_run_add_resource( $lock, 'created_post_ids', $id );
				if ( is_wp_error( $run_recorded ) ) { throw new RuntimeException( $run_recorded->get_error_message() ); }
				$recorded = nadlan_utopia_record_created_resource( 'created_post_ids', $id );
				if ( is_wp_error( $recorded ) ) { throw new RuntimeException( $recorded->get_error_message() ); }
				if ( ! nadlan_utopia_set_verified_meta( $id, '_nadlan_utopia_identity', nadlan_utopia_identity_marker( $lang ) ) ) {
					throw new RuntimeException( 'Could not mark created UTOPIA translation draft.' );
				}
				$created = get_post( $id );
				if ( ! $created || $created->post_name !== $slugs[ $lang ] ) {
					throw new RuntimeException( 'UTOPIA translation slug was altered during draft creation.' );
				}
				$ids[ $lang ] = $id;
				$stage_statuses[ $lang ] = 'draft';
			}

			$thumbnail_id = nadlan_utopia_concept_attachment( $resources, $lock );
			if ( is_wp_error( $thumbnail_id ) || ! $thumbnail_id ) {
				throw new RuntimeException( is_wp_error( $thumbnail_id ) ? $thumbnail_id->get_error_message() : 'Could not prepare UTOPIA concept media.' );
			}

			$run_state = nadlan_utopia_update_run( $lock, array( 'state' => 'staging-drafts', 'post_ids' => $ids ) );
			if ( is_wp_error( $run_state ) ) { throw new RuntimeException( $run_state->get_error_message() ); }
			foreach ( $langs as $lang ) {
				if ( $stage_statuses[ $lang ] === 'publish' ) { continue; }
				$staged = nadlan_utopia_stage_post( $ids[ $lang ], $lang, $articles[ $lang ], $thumbnail_id, $base_taxonomies, $stage_statuses[ $lang ] );
				if ( is_wp_error( $staged ) ) { throw new RuntimeException( $staged->get_error_message() ); }
			}
			foreach ( $langs as $lang ) {
				if ( $stage_statuses[ $lang ] === 'publish' ) { continue; }
				$validated = nadlan_utopia_validate_staged_post( $ids[ $lang ], $lang, $articles[ $lang ], $thumbnail_id, $stage_statuses[ $lang ] );
				if ( is_wp_error( $validated ) ) { throw new RuntimeException( $validated->get_error_message() ); }
			}
			$run_state = nadlan_utopia_update_run( $lock, array( 'state' => 'ready-for-atomic-commit' ) );
			if ( is_wp_error( $run_state ) ) { throw new RuntimeException( $run_state->get_error_message() ); }

			$transaction = nadlan_utopia_begin_release_transaction();
			if ( is_wp_error( $transaction ) ) {
				throw new RuntimeException( $transaction->get_error_message() );
			}
			foreach ( $langs as $lang ) {
				if ( $stage_statuses[ $lang ] !== 'publish' ) { continue; }
				$staged = nadlan_utopia_stage_post( $ids[ $lang ], $lang, $articles[ $lang ], $thumbnail_id, $base_taxonomies, 'publish' );
				if ( is_wp_error( $staged ) ) { throw new RuntimeException( $staged->get_error_message() ); }
				if ( function_exists( 'do_action' ) ) {
					do_action( 'nadlan_utopia_atomic_after_public_stage', $lang, (int) $ids[ $lang ] );
				}
			}
			foreach ( $langs as $lang ) {
				$validated = nadlan_utopia_validate_staged_post( $ids[ $lang ], $lang, $articles[ $lang ], $thumbnail_id, $stage_statuses[ $lang ] );
				if ( is_wp_error( $validated ) ) { throw new RuntimeException( $validated->get_error_message() ); }
			}
			foreach ( $langs as $lang ) {
				if ( $stage_statuses[ $lang ] === 'publish' ) { continue; }
				$published = wp_update_post( array( 'ID' => (int) $ids[ $lang ], 'post_status' => 'publish' ), true );
				if ( is_wp_error( $published ) || (int) $published !== (int) $ids[ $lang ] ) {
					throw new RuntimeException( is_wp_error( $published ) ? $published->get_error_message() : 'Could not publish UTOPIA language ' . $lang . '.' );
				}
			}
			foreach ( $langs as $lang ) {
				$post = get_post( $ids[ $lang ] );
				if ( ! $post || $post->post_status !== 'publish' || $post->post_name !== $slugs[ $lang ] ||
					get_post_meta( $post->ID, '_nadlan_utopia_identity', true ) !== nadlan_utopia_identity_marker( $lang ) ) {
					throw new RuntimeException( 'Final UTOPIA publication validation failed for ' . $lang . '.' );
				}
			}

			$release_manifest = array(
				'release' => '1.72.135',
				'published_at' => gmdate( 'c' ),
				'post_ids' => $ids,
				'article_sha256' => array_map( function ( $article ) { return hash( 'sha256', $article ); }, $articles ),
				'model_sha256' => 'ba267a241f7b5d943f5eebd6f32aae9241f14da420207ddadc4d5d74ac392f24',
				'model_triangles' => 21416,
				'asset_sha256' => array_map( function ( $asset ) { return $asset['sha256']; }, nadlan_utopia_runtime_asset_manifest() ),
			);
			foreach ( array(
				nadlan_utopia_transaction_set_option( 'nadlan_utopia_release_v172135_manifest', $release_manifest ),
				nadlan_utopia_transaction_set_option( 'nadlan_utopia_release_v172135', '1' ),
				nadlan_utopia_transaction_delete_option( 'nadlan_utopia_release_v172135_error' ),
				nadlan_utopia_transaction_delete_option( 'nadlan_utopia_release_v172135_run' ),
			) as $option_result ) {
				if ( is_wp_error( $option_result ) ) {
					throw new RuntimeException( $option_result->get_error_message() );
				}
			}
			$finished = nadlan_utopia_finish_release_transaction( $transaction, true, $ids );
			if ( is_wp_error( $finished ) ) { throw new RuntimeException( $finished->get_error_message() ); }
			$transaction = false;
			$committed   = true;
			if ( ! nadlan_utopia_release_complete() ) {
				update_option( 'nadlan_utopia_release_v172135_hold', 'blocked-recovery', false );
				throw new RuntimeException( 'The atomic UTOPIA release committed but its completion marker could not be read back.' );
			}
		} catch ( Throwable $error ) {
			$message  = $error->getMessage();
			if ( is_array( $transaction ) ) {
				$rolled_back = nadlan_utopia_finish_release_transaction( $transaction, false, $ids );
				$transaction = false;
				if ( is_wp_error( $rolled_back ) ) {
					$message .= ' Transaction rollback error: ' . $rolled_back->get_error_message();
					update_option( 'nadlan_utopia_release_v172135_hold', 'blocked-recovery', false );
				}
			}
			if ( $committed ) {
				update_option( 'nadlan_utopia_release_v172135_hold', 'blocked-recovery', false );
			} elseif ( $backup_ready ) {
				$rollback = nadlan_utopia_restore_backup( $resources, false, $run_started ? $lock : '' );
				if ( is_wp_error( $rollback ) ) {
					$message .= ' Rollback error: ' . $rollback->get_error_message();
				}
			}
			update_option( 'nadlan_utopia_release_v172135_error', array( 'time' => gmdate( 'c' ), 'message' => $message ), false );
		} finally {
			nadlan_utopia_release_lock( $lock );
		}
	}
}
add_action( 'init', 'nadlan_utopia_seed_v172135', 40 );

if ( ! function_exists( 'nadlan_utopia_resume_release' ) ) {
	function nadlan_utopia_resume_release() {
		$hold = get_option( 'nadlan_utopia_release_v172135_hold', false );
		if ( $hold === false ) { return true; }
		if ( $hold !== 'operator' ) {
			return new WP_Error( 'utopia_resume_blocked', 'UTOPIA recovery is blocked and must be repaired before release can resume.' );
		}
		$backup = nadlan_utopia_read_backup();
		if ( is_wp_error( $backup ) ) { return $backup; }
		$run = nadlan_utopia_read_run();
		if ( is_wp_error( $run ) ) { return $run; }
		if ( $run !== false ) {
			return new WP_Error( 'utopia_resume_run', 'An incomplete UTOPIA run journal still exists; recovery must finish before resume.' );
		}
		if ( ! delete_option( 'nadlan_utopia_backup_v172135' ) &&
			get_option( 'nadlan_utopia_backup_v172135', false ) !== false ) {
			return new WP_Error( 'utopia_resume_backup', 'The prior UTOPIA backup could not be retired before a fresh release baseline.' );
		}
		delete_option( 'nadlan_utopia_release_v172135_hold' );
		return true;
	}
}

if ( defined( 'WP_CLI' ) && WP_CLI && class_exists( 'WP_CLI' ) ) {
	WP_CLI::add_command( 'nadlan utopia-restore-v172135', function () {
		if ( ! nadlan_utopia_recovery_context_allowed() ) {
			WP_CLI::error( 'Run this command with --user=<administrator> for a user who has manage_options and unfiltered_html.' );
		}
		$lock = nadlan_utopia_acquire_release_lock();
		if ( $lock === '' ) {
			WP_CLI::error( 'Another UTOPIA release or recovery operation holds the lock.' );
		}
		try {
			$result = nadlan_utopia_restore_backup( array(), true );
			if ( is_wp_error( $result ) ) {
				WP_CLI::error( $result->get_error_message() );
			}
			WP_CLI::success( 'UTOPIA release 1.72.135 was restored and placed on operator hold.' );
		} finally {
			nadlan_utopia_release_lock( $lock );
		}
	} );
	WP_CLI::add_command( 'nadlan utopia-resume-v172135', function () {
		if ( ! nadlan_utopia_recovery_context_allowed() ) {
			WP_CLI::error( 'Run this command with --user=<administrator> for a user who has manage_options and unfiltered_html.' );
		}
		$lock = nadlan_utopia_acquire_release_lock();
		if ( $lock === '' ) {
			WP_CLI::error( 'Another UTOPIA release or recovery operation holds the lock.' );
		}
		try {
			$result = nadlan_utopia_resume_release();
			if ( is_wp_error( $result ) ) { WP_CLI::error( $result->get_error_message() ); }
			WP_CLI::success( 'UTOPIA operator hold removed. The next authorized admin request may apply the release.' );
		} finally {
			nadlan_utopia_release_lock( $lock );
		}
	} );
}

require_once __DIR__ . '/utopia-showroom.php';

if ( ! function_exists( 'nadlan_utopia_compose_public_content' ) ) {
	function nadlan_utopia_compose_public_content( $raw, $post_id, $engine ) {
		$raw = nadlan_utopia_rewrite_asset_urls( $raw );
		if ( preg_match( '#<header\b[^>]*class="[^"]*nadlan-project-lead[^"]*"[^>]*>.*?</header>#is', $raw, $lead_match, PREG_OFFSET_CAPTURE ) ) {
			$lead        = $lead_match[0][0];
			$lead_offset = $lead_match[0][1];
			$rest        = substr_replace( $raw, '', $lead_offset, strlen( $lead ) );
			if ( trim( wp_strip_all_tags( $lead ) ) !== '' && trim( wp_strip_all_tags( $rest ) ) !== '' ) {
				return '<div class="nadlan-project-article nadlan-guide nadlan-project-lead-wrap utopia-project-content">' . $lead . '</div>'
					. $engine
					. '<div class="nadlan-project-article nadlan-guide utopia-project-content">' . $rest . '</div>';
			}
		}
		return $engine . '<div class="nadlan-project-article nadlan-guide utopia-project-content">' . $raw . '</div>';
	}
}

if ( ! function_exists( 'nadlan_utopia_final_content_filter' ) ) {
	function nadlan_utopia_final_content_filter( $content ) {
		if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
		$post_id = get_queried_object_id();
		if ( ! nadlan_utopia_is_family( $post_id ) || ! function_exists( 'nadlan_utopia_showroom_render' ) ) {
			return $content;
		}
		$raw = (string) get_post_field( 'post_content', $post_id );
		if ( $raw === '' ) { return $content; }
		$engine = nadlan_utopia_showroom_render( $post_id );
		return nadlan_utopia_compose_public_content( $raw, $post_id, $engine );
	}
}
add_filter( 'the_content', 'nadlan_utopia_final_content_filter', PHP_INT_MAX );

if ( ! function_exists( 'nadlan_utopia_filter_title' ) ) {
	function nadlan_utopia_filter_title( $title ) {
		$lang = nadlan_utopia_slug_lang();
		if ( $lang === '' ) { return $title; }
		$c = nadlan_utopia_copy( $lang );
		return $c['seo_title'];
	}
}
if ( ! function_exists( 'nadlan_utopia_filter_desc' ) ) {
	function nadlan_utopia_filter_desc( $description ) {
		$lang = nadlan_utopia_slug_lang();
		if ( $lang === '' ) { return $description; }
		$c = nadlan_utopia_copy( $lang );
		return $c['seo_desc'];
	}
}
if ( ! function_exists( 'nadlan_utopia_filter_image' ) ) {
	function nadlan_utopia_filter_image( $image ) {
		return nadlan_utopia_is_family() ? nadlan_utopia_asset_url( 'utopia-concept-exterior-v1.webp' ) : $image;
	}
}
if ( ! function_exists( 'nadlan_utopia_filter_canonical' ) ) {
	function nadlan_utopia_filter_canonical( $canonical ) {
		return nadlan_utopia_is_family() ? get_permalink( get_queried_object_id() ) : $canonical;
	}
}
add_filter( 'wpseo_title', 'nadlan_utopia_filter_title', 100 );
add_filter( 'pre_get_document_title', 'nadlan_utopia_filter_title', 100 );
add_filter( 'wpseo_opengraph_title', 'nadlan_utopia_filter_title', 100 );
add_filter( 'wpseo_twitter_title', 'nadlan_utopia_filter_title', 100 );
add_filter( 'wpseo_metadesc', 'nadlan_utopia_filter_desc', 100 );
add_filter( 'wpseo_opengraph_desc', 'nadlan_utopia_filter_desc', 100 );
add_filter( 'wpseo_twitter_description', 'nadlan_utopia_filter_desc', 100 );
add_filter( 'wpseo_opengraph_image', 'nadlan_utopia_filter_image', 100 );
add_filter( 'wpseo_twitter_image', 'nadlan_utopia_filter_image', 100 );
add_filter( 'wpseo_canonical', 'nadlan_utopia_filter_canonical', 100 );

add_filter( 'wp_get_attachment_image_attributes', function ( $attr, $attachment ) {
	if ( nadlan_utopia_is_family() && $attachment instanceof WP_Post &&
		get_post_meta( $attachment->ID, '_nadlan_utopia_concept_asset', true ) === 'exterior-v1' ) {
		$lang = nadlan_utopia_slug_lang();
		$copy = nadlan_utopia_copy( $lang );
		$attr['alt'] = isset( $copy['media_alt'] ) ? $copy['media_alt'] : 'UTOPIA Sde Dov';
	}
	return $attr;
}, 100, 2 );

add_filter( 'nadlan_card_jsonld', function ( $data, $id, $type ) {
	if ( $type !== 'nadlan_project' || ! nadlan_utopia_is_family( $id ) ) { return $data; }
	$lang = nadlan_utopia_slug_lang( $id );
	$c = nadlan_utopia_copy( $lang );
	unset( $data['offers'], $data['amenityFeature'] );
	$data['name'] = $c['post_title'];
	$data['description'] = $c['excerpt'];
	$data['image'] = nadlan_utopia_asset_url( 'utopia-concept-exterior-v1.webp' );
	$data['numberOfAccommodationUnits'] = 337;
	$data['sameAs'] = array(
		'https://utopiatlv.co.il/',
		'https://www.nahmias-group.co.il/project/utopia-%D7%A9%D7%93%D7%94-%D7%93%D7%91-%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91/',
	);
	$data['address'] = array(
		'@type' => 'PostalAddress',
		'addressLocality' => $c['city'],
		'addressCountry' => 'IL',
	);
	$data['identifier'] = array(
		'@type' => 'PropertyValue',
		'name' => 'Planning lot',
		'value' => '103, Eshkol compound, TML/3001',
	);
	$data['geo'] = array(
		'@type' => 'GeoCoordinates',
		'latitude' => 32.105979,
		'longitude' => 34.784524,
		'description' => 'Planning-lot centroid, not a postal address or apartment location',
	);
	$data['additionalProperty'] = array(
		array( '@type' => 'PropertyValue', 'name' => 'Planning lot', 'value' => '103' ),
		array( '@type' => 'PropertyValue', 'name' => 'Coordinate meaning', 'value' => 'Planning-lot centroid' ),
		array( '@type' => 'PropertyValue', 'name' => 'Buildings', 'value' => 4 ),
		array( '@type' => 'PropertyValue', 'name' => 'Tallest published residential floor count', 'value' => 34 ),
		array( '@type' => 'PropertyValue', 'name' => 'Permit status', 'value' => 'Main application in permit process' ),
	);
	return $data;
}, 100, 3 );

add_action( 'wp', function () {
	if ( ! nadlan_utopia_is_family() ) { return; }
	remove_filter( 'the_content', 'nadlan_pjx_top', 7 );
	remove_filter( 'the_content', 'nadlan_fc_project_hero', 8 );
	remove_filter( 'the_content', 'nadlan_pjx_price_band', 9 );
	remove_filter( 'the_content', 'nadlan_pjx_bottom', 19 );
	remove_filter( 'the_content', 'nadlan_card_append_content', 20 );
	remove_action( 'wp_enqueue_scripts', 'nadlan_pjx_assets' );
	remove_action( 'wp_footer', 'nadlan_card_assets' );
	remove_action( 'wp_head', 'nadlan_pjx_faq_jsonld', 30 );
	remove_filter( 'wpseo_metadesc', 'nadlan_pjx_meta_desc', 25 );
} );

if ( ! function_exists( 'nadlan_utopia_visible_faq' ) ) {
	function nadlan_utopia_visible_faq( $post_id ) {
		$content = (string) get_post_field( 'post_content', $post_id );
		if ( $content === '' || ! preg_match_all( '/<h2\b[^>]*>.*?<\/h2>/isu', $content, $headings, PREG_OFFSET_CAPTURE ) ||
			count( $headings[0] ) !== 9 ) {
			return array();
		}
		$faq_start = (int) $headings[0][7][1] + strlen( $headings[0][7][0] );
		$faq_end   = (int) $headings[0][8][1];
		if ( $faq_end <= $faq_start ) { return array(); }
		$section = substr( $content, $faq_start, $faq_end - $faq_start );
		$rows    = array();
		if ( preg_match_all( '/<h3\b[^>]*>(.*?)<\/h3>\s*<p\b[^>]*>(.*?)<\/p>/isu', $section, $matches, PREG_SET_ORDER ) ) {
			foreach ( $matches as $match ) {
				$question = nadlan_utopia_html_text( $match[1] );
				$answer   = nadlan_utopia_html_text( $match[2] );
				if ( $question !== '' && $answer !== '' ) {
					$rows[] = array( $question, $answer );
				}
			}
		}
		return $rows;
	}
}

add_action( 'wp_head', function () {
	$lang = nadlan_utopia_slug_lang();
	if ( $lang === '' ) { return; }
	$entities = array();
	foreach ( nadlan_utopia_visible_faq( get_queried_object_id() ) as $row ) {
		$entities[] = array(
			'@type' => 'Question',
			'name' => $row[0],
			'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $row[1] ),
		);
	}
	if ( empty( $entities ) ) { return; }
	echo "\n<script type=\"application/ld+json\">" . wp_json_encode( array(
		'@context' => 'https://schema.org',
		'@type' => 'FAQPage',
		'mainEntity' => $entities,
	), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
}, 31 );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['utopia_sde_dov'] = array(
		'release' => '1.72.135',
		'five_languages' => true,
		'model_asset_validated' => true,
		'official_model' => false,
		'model_kind' => 'independent_concept',
		'model_triangles' => 21416,
		'building_mode' => true,
		'empty_apartment_inventory' => true,
	);
	return $out;
} );
