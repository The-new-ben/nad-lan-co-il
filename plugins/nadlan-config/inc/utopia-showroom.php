<?php
/**
 * UTOPIA Sde Dov - project-local buyer showroom.
 *
 * This runtime deliberately does not use the shared showroom DOM, globals,
 * inventory, Studio or map adapter. The available public evidence supports
 * building-level model navigation and 29 references printed on seven official
 * sample-plan PDFs. It does not support availability, apartment-facing or
 * window-view claims.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_utopia_showroom_copy' ) ) {
	function nadlan_utopia_showroom_copy( $lang ) {
		$all = array(
			'he' => array(
				'eyebrow' => 'סיור קנייה אינטראקטיבי',
				'title' => 'להכיר את UTOPIA לפי מבנה, תוכנית וסביבה',
				'intro' => 'בחרו מבנה במודל, עברו על תוכניות הדוגמה הרשמיות ופתחו את מפת הסביבה של מגרש 103.',
				'model' => 'מודל תלת ממד',
				'concept' => 'תמונת קונספט',
				'reset' => 'איפוס המבט',
				'fullscreen' => 'מסך מלא',
				'exit_fullscreen' => 'יציאה ממסך מלא',
				'cinematic' => 'מבט קולנועי',
				'select_building' => 'בחרו אחד מארבעת המבנים',
				'building_prompt' => 'לחצו על סימון במודל או על שם המבנה.',
				'floors' => 'קומות שפורסמו',
				'height' => 'גובה מרבי מתוכנן',
				'planning_source' => 'למסמך התכנון העירוני',
				'orientation_note' => 'המודל ממחיש מסות בנייה ויחסי גובה. הוא אינו מודל מכר ואינו קובע חזית, מרחק או נוף מדירה.',
				'west' => 'מערב - הים',
				'north' => 'צפון - שטח ציבורי 603',
				'east' => 'מזרח - מגרש 401',
				'south' => 'דרום - רחוב 2 המתוכנן',
				'plans_title' => 'תוכניות דוגמה וייחוסי דירות שפורסמו',
				'plans_intro' => 'שבעת הקבצים הרשמיים מציגים 29 מספרי דירות וקומות. אלה ייחוסי תוכנית שפורסמו, לא רשימת מלאי ולא אישור זמינות.',
				'all_buildings' => 'כל המבנים',
				'rooms' => 'חדרים',
				'sqm' => 'מ״ר',
				'interior_area' => 'שטח דירה',
				'balcony_area' => 'שטח מרפסת',
				'published_refs' => 'ייחוסים שמופיעים בקובץ',
				'floor' => 'קומה',
				'apartment' => 'דירה',
				'open_plan' => 'פתיחת התוכנית הרשמית',
				'preview_plan' => 'צפייה בתוכנית',
				'close_plan' => 'סגירת התוכנית',
				'unknown_availability' => 'הזמינות והמחיר של הדירות האלה לא פורסמו בעמוד הציבורי.',
				'label_mismatch' => 'באותו קובץ מופיעים הסימונים 5E ו-C5. יש לאשר את סימון הטיפוס מול היזם.',
				'map_title' => 'מפת הסביבה של מגרש 103',
				'map_intro' => 'המפה מציגה את מרכז המגרש, מוקדי סביבה ופרויקטים סמוכים. הסימון אינו כתובת של דירה מסוימת.',
				'nearby_projects' => 'פרויקטים סמוכים',
				'education' => 'חינוך',
				'parks' => 'פארקים',
				'transit' => 'תחבורה',
				'shops' => 'קניות',
				'health' => 'בריאות',
				'food' => 'קפה ומסעדות',
				'satellite' => 'לוויין',
				'buildings_3d' => 'מבנים בתלת ממד',
				'map_project' => 'UTOPIA - מרכז מגרש 103',
				'map_selected' => 'המבנה שנבחר במודל',
				'map_open_external' => 'פתיחת המיקום במפה',
				'map_unavailable' => 'המפה האינטראקטיבית אינה זמינה כרגע. אפשר לפתוח את נקודת המגרש במפה חיצונית.',
				'cta_title' => 'רוצים לבדוק תוכנית, מחיר ותנאי רכישה?',
				'cta_text' => 'השאירו פרטים וציינו את המבנה או תוכנית הדוגמה שמעניינים אתכם.',
				'name' => 'שם',
				'phone' => 'טלפון',
				'email' => 'אימייל',
				'submit' => 'בקשת פרטים על UTOPIA',
				'submitting' => 'שולח...',
				'success' => 'הפרטים התקבלו. נחזור אליכם בהקדם.',
				'error' => 'נא למלא שם וטלפון או אימייל.',
				'consent' => 'בשליחת הטופס אתם מאשרים שיחזרו אליכם לגבי הפרויקט.',
				'no_selection' => 'ללא תוכנית נבחרת',
				'selected_prefix' => 'נבחרה תוכנית',
				'language' => 'שפה',
			),
			'en' => array(
				'eyebrow' => 'Interactive buying tour',
				'title' => 'Explore UTOPIA by building, plan and surroundings',
				'intro' => 'Choose a building in the model, inspect the official sample plans and open the live context map for lot 103.',
				'model' => '3D model',
				'concept' => 'Concept image',
				'reset' => 'Reset view',
				'fullscreen' => 'Full screen',
				'exit_fullscreen' => 'Exit full screen',
				'cinematic' => 'Cinematic view',
				'select_building' => 'Choose one of the four buildings',
				'building_prompt' => 'Select a marker in the model or a building name.',
				'floors' => 'Published floors',
				'height' => 'Planned maximum height',
				'planning_source' => 'Open the municipal planning document',
				'orientation_note' => 'The model illustrates building massing and relative height. It is not a sales model and does not establish a facade, distance or apartment view.',
				'west' => 'West - Mediterranean Sea',
				'north' => 'North - public open-space lot 603',
				'east' => 'East - lot 401',
				'south' => 'South - planned Street 2',
				'plans_title' => 'Published sample plans and apartment references',
				'plans_intro' => 'The seven official files identify 29 apartment numbers and floors. They are published plan references, not live inventory or proof of availability.',
				'all_buildings' => 'All buildings',
				'rooms' => 'rooms',
				'sqm' => 'sqm',
				'interior_area' => 'Apartment area',
				'balcony_area' => 'Balcony area',
				'published_refs' => 'References printed in the file',
				'floor' => 'Floor',
				'apartment' => 'Apartment',
				'open_plan' => 'Open official plan',
				'preview_plan' => 'View plan',
				'close_plan' => 'Close plan',
				'unknown_availability' => 'Public availability and prices for these apartments have not been published.',
				'label_mismatch' => 'The same file uses both 5E and C5. Confirm the type code with the developer.',
				'map_title' => 'Lot 103 surroundings map',
				'map_intro' => 'The map shows the lot centroid, nearby places and nearby projects. The marker is not the address of a particular apartment.',
				'nearby_projects' => 'Nearby projects',
				'education' => 'Education',
				'parks' => 'Parks',
				'transit' => 'Transit',
				'shops' => 'Shopping',
				'health' => 'Health',
				'food' => 'Cafes and restaurants',
				'satellite' => 'Satellite',
				'buildings_3d' => '3D buildings',
				'map_project' => 'UTOPIA - lot 103 centroid',
				'map_selected' => 'Building selected in the model',
				'map_open_external' => 'Open location in maps',
				'map_unavailable' => 'The interactive map is unavailable right now. You can still open the lot point in an external map.',
				'cta_title' => 'Want to check a plan, price and purchase terms?',
				'cta_text' => 'Leave your details and mention the building or sample plan you want to discuss.',
				'name' => 'Name',
				'phone' => 'Phone',
				'email' => 'Email',
				'submit' => 'Request UTOPIA details',
				'submitting' => 'Sending...',
				'success' => 'Your details were received. We will contact you shortly.',
				'error' => 'Enter your name and either a phone number or email.',
				'consent' => 'By submitting, you agree to be contacted about the project.',
				'no_selection' => 'No plan selected',
				'selected_prefix' => 'Selected plan',
				'language' => 'Language',
			),
			'fr' => array(
				'eyebrow' => 'Visite d’achat interactive',
				'title' => 'Découvrir UTOPIA par bâtiment, plan et environnement',
				'intro' => 'Choisissez un bâtiment dans le modèle, consultez les plans d’exemple officiels et ouvrez la carte du secteur de la parcelle 103.',
				'model' => 'Modèle 3D',
				'concept' => 'Image conceptuelle',
				'reset' => 'Réinitialiser la vue',
				'fullscreen' => 'Plein écran',
				'exit_fullscreen' => 'Quitter le plein écran',
				'cinematic' => 'Vue cinématique',
				'select_building' => 'Choisissez l’un des quatre bâtiments',
				'building_prompt' => 'Sélectionnez un repère dans le modèle ou le nom d’un bâtiment.',
				'floors' => 'Étages publiés',
				'height' => 'Hauteur maximale projetée',
				'planning_source' => 'Ouvrir le document municipal d’urbanisme',
				'orientation_note' => 'Le modèle illustre les volumes et les hauteurs relatives. Ce n’est pas un modèle de vente et il ne garantit ni façade, ni distance, ni vue.',
				'west' => 'Ouest - Méditerranée',
				'north' => 'Nord - espace public 603',
				'east' => 'Est - parcelle 401',
				'south' => 'Sud - rue 2 projetée',
				'plans_title' => 'Plans d’exemple et références d’appartements publiés',
				'plans_intro' => 'Les sept fichiers officiels indiquent 29 numéros d’appartement et étages. Ce sont des références de plans publiées, pas un stock en temps réel.',
				'all_buildings' => 'Tous les bâtiments',
				'rooms' => 'pièces',
				'sqm' => 'm²',
				'interior_area' => 'Surface de l’appartement',
				'balcony_area' => 'Surface du balcon',
				'published_refs' => 'Références indiquées dans le fichier',
				'floor' => 'Étage',
				'apartment' => 'Appartement',
				'open_plan' => 'Ouvrir le plan officiel',
				'preview_plan' => 'Voir le plan',
				'close_plan' => 'Fermer le plan',
				'unknown_availability' => 'La disponibilité et les prix de ces appartements ne sont pas publiés.',
				'label_mismatch' => 'Le même fichier utilise 5E et C5. Le code du type doit être confirmé auprès du promoteur.',
				'map_title' => 'Carte autour de la parcelle 103',
				'map_intro' => 'La carte montre le centre de la parcelle, les services et les projets voisins. Le repère n’est pas l’adresse d’un appartement.',
				'nearby_projects' => 'Projets voisins',
				'education' => 'Éducation',
				'parks' => 'Parcs',
				'transit' => 'Transports',
				'shops' => 'Commerces',
				'health' => 'Santé',
				'food' => 'Cafés et restaurants',
				'satellite' => 'Satellite',
				'buildings_3d' => 'Bâtiments 3D',
				'map_project' => 'UTOPIA - centre de la parcelle 103',
				'map_selected' => 'Bâtiment sélectionné dans le modèle',
				'map_open_external' => 'Ouvrir le lieu sur la carte',
				'map_unavailable' => 'La carte interactive est momentanément indisponible. Le point de la parcelle reste accessible sur une carte externe.',
				'cta_title' => 'Vous souhaitez vérifier un plan, un prix et les conditions d’achat ?',
				'cta_text' => 'Laissez vos coordonnées et indiquez le bâtiment ou le plan d’exemple qui vous intéresse.',
				'name' => 'Nom',
				'phone' => 'Téléphone',
				'email' => 'E-mail',
				'submit' => 'Demander des informations',
				'submitting' => 'Envoi...',
				'success' => 'Vos coordonnées ont bien été reçues. Nous vous contacterons prochainement.',
				'error' => 'Indiquez votre nom et un téléphone ou une adresse e-mail.',
				'consent' => 'En envoyant le formulaire, vous acceptez d’être contacté au sujet du projet.',
				'no_selection' => 'Aucun plan sélectionné',
				'selected_prefix' => 'Plan sélectionné',
				'language' => 'Langue',
			),
			'ru' => array(
				'eyebrow' => 'Интерактивный обзор для покупателя',
				'title' => 'UTOPIA: здания, планы и окружение проекта',
				'intro' => 'Выберите здание в модели, изучите официальные примеры планов и откройте карту участка 103.',
				'model' => '3D-модель',
				'concept' => 'Концептуальное изображение',
				'reset' => 'Сбросить вид',
				'fullscreen' => 'На весь экран',
				'exit_fullscreen' => 'Выйти из полноэкранного режима',
				'cinematic' => 'Кинематографический вид',
				'select_building' => 'Выберите одно из четырех зданий',
				'building_prompt' => 'Нажмите на метку в модели или на название здания.',
				'floors' => 'Опубликованная этажность',
				'height' => 'Планируемая предельная высота',
				'planning_source' => 'Открыть муниципальный документ',
				'orientation_note' => 'Модель показывает объемы и относительную высоту. Это не модель продаж, и она не подтверждает фасад, расстояние или вид из квартиры.',
				'west' => 'Запад - Средиземное море',
				'north' => 'Север - общественное пространство 603',
				'east' => 'Восток - участок 401',
				'south' => 'Юг - проектируемая улица 2',
				'plans_title' => 'Опубликованные примеры планов и номера квартир',
				'plans_intro' => 'В семи официальных файлах указаны 29 номеров квартир и этажей. Это опубликованные ссылки на планы, а не текущий список продаж.',
				'all_buildings' => 'Все здания',
				'rooms' => 'комнат',
				'sqm' => 'м²',
				'interior_area' => 'Площадь квартиры',
				'balcony_area' => 'Площадь балкона',
				'published_refs' => 'Данные, указанные в файле',
				'floor' => 'Этаж',
				'apartment' => 'Квартира',
				'open_plan' => 'Открыть официальный план',
				'preview_plan' => 'Посмотреть план',
				'close_plan' => 'Закрыть план',
				'unknown_availability' => 'Наличие и цены этих квартир публично не опубликованы.',
				'label_mismatch' => 'В одном файле используются обозначения 5E и C5. Код типа нужно подтвердить у застройщика.',
				'map_title' => 'Карта окружения участка 103',
				'map_intro' => 'Карта показывает центр участка, объекты инфраструктуры и соседние проекты. Метка не является адресом конкретной квартиры.',
				'nearby_projects' => 'Проекты рядом',
				'education' => 'Образование',
				'parks' => 'Парки',
				'transit' => 'Транспорт',
				'shops' => 'Магазины',
				'health' => 'Медицина',
				'food' => 'Кафе и рестораны',
				'satellite' => 'Спутник',
				'buildings_3d' => 'Здания 3D',
				'map_project' => 'UTOPIA - центр участка 103',
				'map_selected' => 'Здание выбрано в модели',
				'map_open_external' => 'Открыть место на карте',
				'map_unavailable' => 'Интерактивная карта сейчас недоступна. Точку участка можно открыть на внешней карте.',
				'cta_title' => 'Хотите уточнить план, цену и условия покупки?',
				'cta_text' => 'Оставьте контакты и укажите интересующее здание или пример плана.',
				'name' => 'Имя',
				'phone' => 'Телефон',
				'email' => 'Электронная почта',
				'submit' => 'Запросить информацию',
				'submitting' => 'Отправка...',
				'success' => 'Ваши данные получены. Мы свяжемся с вами в ближайшее время.',
				'error' => 'Укажите имя и телефон или электронную почту.',
				'consent' => 'Отправляя форму, вы соглашаетесь на связь по поводу проекта.',
				'no_selection' => 'План не выбран',
				'selected_prefix' => 'Выбран план',
				'language' => 'Язык',
			),
			'ar' => array(
				'eyebrow' => 'جولة شراء تفاعلية',
				'title' => 'تعرّفوا على UTOPIA حسب المبنى والمخطط والمحيط',
				'intro' => 'اختاروا مبنى في النموذج، تصفحوا نماذج المخططات الرسمية وافتحوا خريطة محيط القسيمة 103.',
				'model' => 'نموذج ثلاثي الأبعاد',
				'concept' => 'صورة تصورية',
				'reset' => 'إعادة ضبط المشهد',
				'fullscreen' => 'ملء الشاشة',
				'exit_fullscreen' => 'الخروج من ملء الشاشة',
				'cinematic' => 'مشهد سينمائي',
				'select_building' => 'اختاروا واحدا من المباني الأربعة',
				'building_prompt' => 'اضغطوا على علامة في النموذج أو على اسم المبنى.',
				'floors' => 'الطوابق المنشورة',
				'height' => 'الارتفاع الأقصى المخطط',
				'planning_source' => 'فتح وثيقة التخطيط البلدية',
				'orientation_note' => 'يوضح النموذج الكتل والارتفاعات النسبية. ليس نموذجا للبيع ولا يثبت واجهة أو مسافة أو إطلالة من شقة.',
				'west' => 'غربا - البحر المتوسط',
				'north' => 'شمالا - المساحة العامة 603',
				'east' => 'شرقا - القسيمة 401',
				'south' => 'جنوبا - الشارع 2 المخطط',
				'plans_title' => 'نماذج مخططات وأرقام شقق منشورة',
				'plans_intro' => 'تذكر الملفات الرسمية السبعة 29 رقم شقة وطابقا. هذه إحالات منشورة للمخططات وليست قائمة وحدات متاحة.',
				'all_buildings' => 'جميع المباني',
				'rooms' => 'غرف',
				'sqm' => 'م²',
				'interior_area' => 'مساحة الشقة',
				'balcony_area' => 'مساحة الشرفة',
				'published_refs' => 'الإحالات الواردة في الملف',
				'floor' => 'الطابق',
				'apartment' => 'الشقة',
				'open_plan' => 'فتح المخطط الرسمي',
				'preview_plan' => 'عرض المخطط',
				'close_plan' => 'إغلاق المخطط',
				'unknown_availability' => 'لم تنشر إتاحة هذه الشقق أو أسعارها في الصفحة العامة.',
				'label_mismatch' => 'يستخدم الملف نفسه الرمزين 5E وC5. يجب تأكيد رمز النموذج مع المطور.',
				'map_title' => 'خريطة محيط القسيمة 103',
				'map_intro' => 'تعرض الخريطة مركز القسيمة والمرافق والمشاريع القريبة. العلامة ليست عنوان شقة محددة.',
				'nearby_projects' => 'مشاريع قريبة',
				'education' => 'التعليم',
				'parks' => 'حدائق',
				'transit' => 'المواصلات',
				'shops' => 'التسوق',
				'health' => 'الصحة',
				'food' => 'مقاه ومطاعم',
				'satellite' => 'قمر صناعي',
				'buildings_3d' => 'مبان ثلاثية الأبعاد',
				'map_project' => 'UTOPIA - مركز القسيمة 103',
				'map_selected' => 'المبنى المختار في النموذج',
				'map_open_external' => 'فتح الموقع في الخريطة',
				'map_unavailable' => 'الخريطة التفاعلية غير متاحة الآن. يمكن فتح نقطة القسيمة في خريطة خارجية.',
				'cta_title' => 'هل تريدون فحص مخطط وسعر وشروط شراء؟',
				'cta_text' => 'اتركوا بياناتكم واذكروا المبنى أو نموذج المخطط الذي يهمكم.',
				'name' => 'الاسم',
				'phone' => 'الهاتف',
				'email' => 'البريد الإلكتروني',
				'submit' => 'طلب معلومات عن UTOPIA',
				'submitting' => 'جار الإرسال...',
				'success' => 'وصلت بياناتكم. سنتواصل معكم قريبا.',
				'error' => 'يرجى إدخال الاسم ورقم الهاتف أو البريد الإلكتروني.',
				'consent' => 'بإرسال النموذج توافقون على التواصل معكم بخصوص المشروع.',
				'no_selection' => 'لم يتم اختيار مخطط',
				'selected_prefix' => 'المخطط المختار',
				'language' => 'اللغة',
			),
		);
		return isset( $all[ $lang ] ) ? $all[ $lang ] : $all['he'];
	}
}

if ( ! function_exists( 'nadlan_utopia_showroom_language_urls' ) ) {
	function nadlan_utopia_showroom_language_urls() {
		$out = array();
		foreach ( nadlan_utopia_release_slugs() as $lang => $slug ) {
			$post = get_page_by_path( $slug, OBJECT, 'nadlan_project' );
			if ( $post && get_post_status( $post ) === 'publish' ) {
				$out[ $lang ] = get_permalink( $post->ID );
			}
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_utopia_showroom_nearby' ) ) {
	function nadlan_utopia_showroom_nearby( $lang ) {
		$out    = array();
		$suffix = $lang === 'he' ? '' : '-' . $lang;
		foreach ( nadlan_utopia_nearby_project_bases() as $base ) {
			$post = get_page_by_path( $base . $suffix, OBJECT, 'nadlan_project' );
			if ( ! $post || get_post_status( $post ) !== 'publish' ) { continue; }
			$lat = (float) get_post_meta( $post->ID, 'lat', true );
			$lng = (float) get_post_meta( $post->ID, 'lng', true );
			if ( ! $lat || ! $lng ) { continue; }
			$out[] = array(
				'name' => get_the_title( $post->ID ),
				'url'  => get_permalink( $post->ID ),
				'lat'  => $lat,
				'lng'  => $lng,
			);
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_utopia_showroom_pois' ) ) {
	function nadlan_utopia_showroom_pois() {
		$raw = function_exists( 'nadlan_poi_fetch' ) ? nadlan_poi_fetch( 32.105979, 34.784524, 1200 ) : array();
		$out = array();
		foreach ( array( 'schools', 'kindergartens', 'parks', 'transit', 'shops', 'health', 'food' ) as $group ) {
			$out[ $group ] = array();
			foreach ( array_slice( isset( $raw[ $group ] ) ? (array) $raw[ $group ] : array(), 0, 14 ) as $item ) {
				$lat = isset( $item['lat'] ) ? (float) $item['lat'] : 0;
				$lng = isset( $item['lng'] ) ? (float) $item['lng'] : 0;
				if ( ! $lat || ! $lng ) { continue; }
				$out[ $group ][] = array(
					'name' => sanitize_text_field( isset( $item['name'] ) ? (string) $item['name'] : '' ),
					'lat'  => $lat,
					'lng'  => $lng,
					'd'    => isset( $item['d'] ) ? max( 0, (int) $item['d'] ) : 0,
				);
			}
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_utopia_showroom_payload' ) ) {
	function nadlan_utopia_showroom_payload( $post_id ) {
		$lang  = nadlan_utopia_slug_lang( $post_id );
		$copy  = nadlan_utopia_showroom_copy( $lang );
		$token = function_exists( 'nadlan_mapbox_token' )
			? (string) nadlan_mapbox_token()
			: (string) get_option( 'nadlan_mapbox_token', '' );
		return array(
			'lang' => $lang,
			'rtl' => in_array( $lang, array( 'he', 'ar' ), true ),
			'copy' => $copy,
			'project' => array(
				'slug' => (string) get_post_field( 'post_name', $post_id ),
				'title' => get_the_title( $post_id ),
				'id' => (int) $post_id,
				'units_total' => 337,
				'buildings_total' => 4,
				'model_url' => trailingslashit( nadlan_showroom_engine_base_url() ) . 'models/utopia-rich-v1.glb',
				'poster_url' => nadlan_utopia_asset_url( 'utopia-concept-exterior-v1.webp' ),
				'model_triangles' => 21416,
				'model_kind' => 'independent_orientation',
			),
			'buildings' => nadlan_utopia_buildings( $lang ),
			'sample_plans' => nadlan_utopia_sample_plans( $lang ),
			'map' => array(
				'lat' => 32.105979,
				'lng' => 34.784524,
				'token' => $token,
				'external_url' => 'https://www.google.com/maps/search/?api=1&query=32.105979,34.784524',
				'pois' => nadlan_utopia_showroom_pois(),
				'nearby' => nadlan_utopia_showroom_nearby( $lang ),
			),
			'language_urls' => nadlan_utopia_showroom_language_urls(),
			'lead_endpoint' => esc_url_raw( rest_url( 'nadlan/v1/lead' ) ),
			'whatsapp' => preg_replace( '/\D+/', '', (string) get_option( 'nadlan_whatsapp_e164', '' ) ),
		);
	}
}

if ( ! function_exists( 'nadlan_utopia_showroom_assets' ) ) {
	function nadlan_utopia_showroom_assets() {
		if ( ! is_singular( 'nadlan_project' ) || ! nadlan_utopia_is_family( get_queried_object_id() ) ) { return; }
		$base = trailingslashit( nadlan_showroom_engine_base_url() );
		$ver  = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1';

		wp_enqueue_style( 'nadlan-engine-tokens', $base . 'tokens.css', array(), $ver );
		wp_enqueue_style( 'nadlan-engine-editorial', $base . 'editorial.css', array( 'nadlan-engine-tokens' ), $ver );
		wp_enqueue_style(
			'nadlan-utopia-showroom',
			nadlan_utopia_asset_url( 'utopia.css' ),
			array( 'nadlan-engine-tokens', 'nadlan-engine-editorial' ),
			$ver
		);

		wp_enqueue_script(
			'nadlan-model-viewer',
			'https://ajax.googleapis.com/ajax/libs/model-viewer/4.3.1/model-viewer.min.js',
			array(),
			'4.3.1',
			true
		);
		wp_script_add_data( 'nadlan-model-viewer', 'type', 'module' );

		$deps  = array( 'nadlan-model-viewer' );
		$token = function_exists( 'nadlan_mapbox_token' )
			? (string) nadlan_mapbox_token()
			: (string) get_option( 'nadlan_mapbox_token', '' );
		if ( $token !== '' ) {
			wp_enqueue_style( 'mapbox-gl', 'https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css', array(), '3.7.0' );
			wp_enqueue_script( 'mapbox-gl', 'https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js', array(), '3.7.0', true );
			$deps[] = 'mapbox-gl';
		}
		wp_enqueue_script(
			'nadlan-utopia-showroom',
			nadlan_utopia_asset_url( 'utopia-showroom.js' ),
			$deps,
			$ver,
			true
		);
	}
}
add_action( 'wp_enqueue_scripts', 'nadlan_utopia_showroom_assets', 99 );

if ( ! function_exists( 'nadlan_utopia_showroom_dequeue_generic_scripts' ) ) {
	function nadlan_utopia_showroom_dequeue_generic_scripts() {
		foreach ( array(
			'nadlan-engine-core',
			'nadlan-engine-buyflow',
			'nadlan-engine-studio',
			'nadlan-engine-mapbox',
			'nadlan-engine-i18n',
			'nadlan-engine-i18n-utopia',
		) as $handle ) {
			wp_dequeue_script( $handle );
		}
	}
}

if ( ! function_exists( 'nadlan_utopia_showroom_render' ) ) {
	function nadlan_utopia_showroom_render( $post_id ) {
		nadlan_utopia_showroom_dequeue_generic_scripts();
		$payload   = nadlan_utopia_showroom_payload( $post_id );
		$lang      = $payload['lang'];
		$copy      = $payload['copy'];
		$buildings = $payload['buildings'];
		$plans     = $payload['sample_plans'];
		$dir       = $payload['rtl'] ? 'rtl' : 'ltr';
		$building_by_id = array();
		foreach ( $buildings as $building ) { $building_by_id[ $building['id'] ] = $building; }

		ob_start();
		?>
		<section id="utopia-showroom" class="utopia-atlas" lang="<?php echo esc_attr( $lang ); ?>" dir="<?php echo esc_attr( $dir ); ?>">
			<header class="utopia-atlas__intro">
				<div>
					<span class="utopia-kicker"><?php echo esc_html( $copy['eyebrow'] ); ?></span>
					<h2><?php echo esc_html( $copy['title'] ); ?></h2>
					<p><?php echo esc_html( $copy['intro'] ); ?></p>
				</div>
				<?php if ( count( $payload['language_urls'] ) > 1 ) : ?>
					<nav class="utopia-languages" aria-label="<?php echo esc_attr( $copy['language'] ); ?>">
						<?php foreach ( $payload['language_urls'] as $code => $url ) : ?>
							<a href="<?php echo esc_url( $url ); ?>" hreflang="<?php echo esc_attr( $code ); ?>"<?php echo $code === $lang ? ' aria-current="page"' : ''; ?>><?php echo esc_html( strtoupper( $code ) ); ?></a>
						<?php endforeach; ?>
					</nav>
				<?php endif; ?>
			</header>

			<div class="utopia-stage-grid">
				<div class="utopia-stage">
					<div class="utopia-stage__toolbar" role="group" aria-label="<?php echo esc_attr( $copy['model'] ); ?>">
						<button type="button" class="is-active" data-utopia-view="model"><?php echo esc_html( $copy['model'] ); ?></button>
						<button type="button" data-utopia-view="concept"><?php echo esc_html( $copy['concept'] ); ?></button>
						<button type="button" data-utopia-action="cinematic"><?php echo esc_html( $copy['cinematic'] ); ?></button>
						<button type="button" data-utopia-action="reset"><?php echo esc_html( $copy['reset'] ); ?></button>
						<button type="button" data-utopia-action="fullscreen" data-label-enter="<?php echo esc_attr( $copy['fullscreen'] ); ?>" data-label-exit="<?php echo esc_attr( $copy['exit_fullscreen'] ); ?>"><?php echo esc_html( $copy['fullscreen'] ); ?></button>
					</div>
					<div class="utopia-stage__viewport">
						<model-viewer
							id="utopia-model-viewer"
							src="<?php echo esc_url( $payload['project']['model_url'] ); ?>"
							poster="<?php echo esc_url( $payload['project']['poster_url'] ); ?>"
							camera-controls
							interaction-prompt="auto"
							environment-image="neutral"
							exposure=".72"
							shadow-intensity=".65"
							shadow-softness=".9"
							camera-orbit="-28deg 68deg 220m"
							camera-target="0m 42m 0m"
							min-camera-orbit="auto 45deg auto"
							max-camera-orbit="auto 86deg auto"
							min-field-of-view="16deg"
							max-field-of-view="68deg"
							touch-action="pan-y"
							alt="<?php echo esc_attr( $copy['title'] ); ?>"
						>
							<?php foreach ( $buildings as $building ) : ?>
								<button
									type="button"
									class="utopia-model-hotspot"
									slot="hotspot-<?php echo esc_attr( $building['id'] ); ?>"
									data-position="<?php echo esc_attr( preg_replace( '/(-?\d+(?:\.\d+)?)(?=\s|$)/', '$1m', $building['hotspot_position'] ) ); ?>"
									data-normal="<?php echo esc_attr( $building['hotspot_normal'] ); ?>"
									data-visibility-attribute="visible"
									data-building="<?php echo esc_attr( $building['id'] ); ?>"
									aria-label="<?php echo esc_attr( $building['label'] ); ?>"
								><?php echo esc_html( strtoupper( $building['id'] ) ); ?></button>
							<?php endforeach; ?>
						</model-viewer>
						<div class="utopia-concept-frame" hidden>
							<img src="<?php echo esc_url( $payload['project']['poster_url'] ); ?>" alt="<?php echo esc_attr( nadlan_utopia_copy( $lang )['media_alt'] ); ?>" loading="lazy" width="1536" height="1024">
						</div>
						<div class="utopia-orientation" aria-label="<?php echo esc_attr( $copy['orientation_note'] ); ?>">
							<span class="utopia-orientation__north">N</span>
							<span><?php echo esc_html( $copy['west'] ); ?></span>
							<span><?php echo esc_html( $copy['south'] ); ?></span>
							<span><?php echo esc_html( $copy['east'] ); ?></span>
						</div>
					</div>
					<p class="utopia-stage__note"><?php echo esc_html( $copy['orientation_note'] ); ?></p>
				</div>

				<aside class="utopia-building-panel" aria-live="polite">
					<span class="utopia-kicker"><?php echo esc_html( $copy['select_building'] ); ?></span>
					<h3 id="utopia-building-title"><?php echo esc_html( $copy['select_building'] ); ?></h3>
					<p id="utopia-building-facts"><?php echo esc_html( $copy['building_prompt'] ); ?></p>
					<div class="utopia-building-panel__metrics" id="utopia-building-metrics" hidden>
						<div><span><?php echo esc_html( $copy['floors'] ); ?></span><strong data-building-floors></strong></div>
						<div><span><?php echo esc_html( $copy['height'] ); ?></span><strong data-building-height></strong></div>
					</div>
					<a id="utopia-building-source" href="#" target="_blank" rel="noopener noreferrer" hidden><?php echo esc_html( $copy['planning_source'] ); ?></a>
					<div class="utopia-building-buttons">
						<?php foreach ( $buildings as $building ) : ?>
							<button type="button" data-utopia-building="<?php echo esc_attr( $building['id'] ); ?>"><?php echo esc_html( $building['label'] ); ?></button>
						<?php endforeach; ?>
					</div>
				</aside>
			</div>

			<section class="utopia-plans" id="utopia-published-plans">
				<div class="utopia-section-heading">
					<span class="utopia-kicker"><?php echo esc_html( $copy['plans_title'] ); ?></span>
					<h3><?php echo esc_html( $copy['plans_title'] ); ?></h3>
					<p><?php echo esc_html( $copy['plans_intro'] ); ?></p>
				</div>
				<div class="utopia-plan-filters" role="group" aria-label="<?php echo esc_attr( $copy['select_building'] ); ?>">
					<button type="button" class="is-active" data-plan-filter="all"><?php echo esc_html( $copy['all_buildings'] ); ?></button>
					<?php foreach ( $buildings as $building ) : ?>
						<?php if ( in_array( $building['id'], array_column( $plans, 'building' ), true ) ) : ?>
							<button type="button" data-plan-filter="<?php echo esc_attr( $building['id'] ); ?>"><?php echo esc_html( $building['label'] ); ?></button>
						<?php endif; ?>
					<?php endforeach; ?>
				</div>
				<div class="utopia-plan-grid">
					<?php foreach ( $plans as $plan ) : ?>
						<article class="utopia-plan-card" data-plan-card="<?php echo esc_attr( $plan['id'] ); ?>" data-building="<?php echo esc_attr( $plan['building'] ); ?>">
							<div class="utopia-plan-card__top">
								<span><?php echo esc_html( isset( $building_by_id[ $plan['building'] ] ) ? $building_by_id[ $plan['building'] ]['label'] : strtoupper( $plan['building'] ) ); ?></span>
								<strong><?php echo esc_html( $plan['type'] ); ?></strong>
								<small><?php echo esc_html( $plan['rooms'] . ' ' . $copy['rooms'] ); ?></small>
							</div>
							<dl>
								<div><dt><?php echo esc_html( $copy['interior_area'] ); ?></dt><dd><?php echo esc_html( number_format_i18n( $plan['interior_sqm'], 2 ) . ' ' . $copy['sqm'] ); ?></dd></div>
								<div><dt><?php echo esc_html( $copy['balcony_area'] ); ?></dt><dd><?php echo esc_html( number_format_i18n( $plan['balcony_sqm'], 2 ) . ' ' . $copy['sqm'] ); ?></dd></div>
							</dl>
							<p class="utopia-plan-card__refs-title"><?php echo esc_html( $copy['published_refs'] ); ?></p>
							<div class="utopia-plan-card__refs">
								<?php foreach ( $plan['references'] as $reference ) : ?>
									<button
										type="button"
										data-utopia-reference="<?php echo esc_attr( $plan['id'] . '-' . $reference['apartment'] ); ?>"
										data-plan="<?php echo esc_attr( $plan['id'] ); ?>"
										data-floor="<?php echo esc_attr( $reference['floor'] ); ?>"
										data-apartment="<?php echo esc_attr( $reference['apartment'] ); ?>"
									><?php echo esc_html( $copy['floor'] . ' ' . $reference['floor'] . ' · ' . $copy['apartment'] . ' ' . $reference['apartment'] ); ?></button>
								<?php endforeach; ?>
							</div>
							<?php if ( ! empty( $plan['label_mismatch'] ) ) : ?>
								<p class="utopia-plan-card__mismatch"><?php echo esc_html( $copy['label_mismatch'] ); ?></p>
							<?php endif; ?>
							<p class="utopia-plan-card__availability"><?php echo esc_html( $copy['unknown_availability'] ); ?></p>
							<div class="utopia-plan-card__actions">
								<button type="button" data-utopia-plan="<?php echo esc_attr( $plan['id'] ); ?>"><?php echo esc_html( $copy['preview_plan'] ); ?></button>
								<a href="<?php echo esc_url( $plan['url'] ); ?>" target="_blank" rel="noopener noreferrer"><?php echo esc_html( $copy['open_plan'] ); ?></a>
							</div>
						</article>
					<?php endforeach; ?>
				</div>
			</section>

			<section class="utopia-map-section" id="utopia-map-section">
				<div class="utopia-section-heading">
					<span class="utopia-kicker"><?php echo esc_html( $copy['map_title'] ); ?></span>
					<h3><?php echo esc_html( $copy['map_title'] ); ?></h3>
					<p><?php echo esc_html( $copy['map_intro'] ); ?></p>
				</div>
				<div class="utopia-map-layers" role="group" aria-label="<?php echo esc_attr( $copy['map_title'] ); ?>">
					<button type="button" class="is-active" data-map-layer="nearby"><?php echo esc_html( $copy['nearby_projects'] ); ?></button>
					<button type="button" class="is-active" data-map-layer="education"><?php echo esc_html( $copy['education'] ); ?></button>
					<button type="button" class="is-active" data-map-layer="parks"><?php echo esc_html( $copy['parks'] ); ?></button>
					<button type="button" data-map-layer="transit"><?php echo esc_html( $copy['transit'] ); ?></button>
					<button type="button" data-map-layer="shops"><?php echo esc_html( $copy['shops'] ); ?></button>
					<button type="button" data-map-layer="health"><?php echo esc_html( $copy['health'] ); ?></button>
					<button type="button" data-map-layer="food"><?php echo esc_html( $copy['food'] ); ?></button>
					<button type="button" data-map-layer="satellite"><?php echo esc_html( $copy['satellite'] ); ?></button>
					<button type="button" data-map-layer="buildings3d"><?php echo esc_html( $copy['buildings_3d'] ); ?></button>
				</div>
				<div id="utopia-context-map" aria-label="<?php echo esc_attr( $copy['map_title'] ); ?>"></div>
				<div class="utopia-map-fallback" hidden>
					<p><?php echo esc_html( $copy['map_unavailable'] ); ?></p>
					<a href="<?php echo esc_url( $payload['map']['external_url'] ); ?>" target="_blank" rel="noopener noreferrer"><?php echo esc_html( $copy['map_open_external'] ); ?></a>
				</div>
			</section>

			<section class="utopia-inquiry" id="utopia-inquiry">
				<div>
					<span class="utopia-kicker"><?php echo esc_html( $copy['cta_title'] ); ?></span>
					<h3><?php echo esc_html( $copy['cta_title'] ); ?></h3>
					<p><?php echo esc_html( $copy['cta_text'] ); ?></p>
				</div>
				<form id="utopia-inquiry-form" novalidate>
					<div class="utopia-inquiry__context" data-utopia-form-context><?php echo esc_html( $copy['no_selection'] ); ?></div>
					<input type="text" name="name" autocomplete="name" placeholder="<?php echo esc_attr( $copy['name'] ); ?>">
					<div class="utopia-inquiry__row">
						<input type="tel" name="phone" autocomplete="tel" inputmode="tel" placeholder="<?php echo esc_attr( $copy['phone'] ); ?>">
						<input type="email" name="email" autocomplete="email" inputmode="email" placeholder="<?php echo esc_attr( $copy['email'] ); ?>">
					</div>
					<button type="submit" data-label-default="<?php echo esc_attr( $copy['submit'] ); ?>" data-label-sending="<?php echo esc_attr( $copy['submitting'] ); ?>"><?php echo esc_html( $copy['submit'] ); ?></button>
					<p class="utopia-inquiry__message" role="status" aria-live="polite" hidden></p>
					<small><?php echo esc_html( $copy['consent'] ); ?></small>
				</form>
			</section>

			<dialog id="utopia-plan-dialog" class="utopia-plan-dialog">
				<div class="utopia-plan-dialog__bar">
					<strong data-plan-dialog-title></strong>
					<button type="button" data-utopia-dialog-close aria-label="<?php echo esc_attr( $copy['close_plan'] ); ?>"><?php echo esc_html( $copy['close_plan'] ); ?></button>
				</div>
				<iframe title="<?php echo esc_attr( $copy['preview_plan'] ); ?>" loading="lazy"></iframe>
				<div class="utopia-plan-dialog__fallback">
					<a href="#" target="_blank" rel="noopener noreferrer"><?php echo esc_html( $copy['open_plan'] ); ?></a>
				</div>
			</dialog>

			<script type="application/json" id="utopia-showroom-data"><?php
				echo wp_json_encode(
					$payload,
					JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT
				); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
			?></script>
		</section>
		<?php
		return ob_get_clean();
	}
}
