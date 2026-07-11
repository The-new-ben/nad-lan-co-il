<?php
/**
 * i18n engine (2026-07-03) - systematic 5-language chrome for nad-lan.co.il.
 *
 * LAW (see handoff/research/2026-07-03-multilingual-architecture.md):
 * - CHROME (nav, hero, footer, labels, switcher) is systematic: one string
 *   table per language, resolved via nadlan_i18n('key'). Change once, every
 *   surface reflects it. 'he' values equal the exact current Hebrew, so the
 *   Hebrew page renders byte-identical.
 * - CONTENT (article/news/project bodies) is NOT here - it must be real
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
			// market band
			'tk_tlv' => 'מחיר ממוצע למ״ר, פרויקטים חדשים בת״א', 'tk_watch' => 'מחיר ממוצע למ״ר, פרויקטים שבמעקב', 'tk_projects' => 'פרויקטים במעקב', 'tk_source' => 'מבוסס על קטלוג נדלן', 'mk_title' => 'לאן השוק הולך', 'mk_tlv' => 'מחיר ממוצע למ״ר בפרויקטים חדשים בתל אביב', 'mk_watch' => 'מחיר ממוצע למ״ר בפרויקטים שבמעקב', 'mk_yoy' => 'שינוי שנתי במחירי הדירות', 'mk_rate' => 'ריבית משכנתא ממוצעת', 'mk_note_pre' => 'מבוסס על קטלוג נדלן · עודכן ',
			// projects band
			'pj_kicker' => 'דירות חדשות מקבלן', 'pj_title' => 'בוחרים דירה מתוך הבניין', 'pj_all' => 'לכל הפרויקטים ←', 'pj_pick' => 'בחירת דירה מתוך הבניין', 'pj_units_pick' => 'דירות לבחירה', 'pj_est_pre' => 'אומדן ~', 'pj_est_suf' => '₪/מ״ר · לא מחייב', 'pj_live' => 'תצוגה חיה', 'pj_viewer_note' => 'הדמיה להמחשה. גררו לסיבוב, לחצו על שם הפרויקט למעבר לעמוד המלא.', 'pj_dark_note' => 'האומדנים אינם מחייבים ומבוססים על נתונים גלויים. ההדמיות להמחשה עד לאישור חומרים רשמיים של היזם.',
			// listings band
			'ls_kicker' => 'דירות למכירה ולהשכרה', 'ls_title' => 'נכסים חדשים במערכת', 'ls_all' => 'לכל הדירות ←', 'ls_cta_b' => '+ מפרסמים דירה?', 'ls_cta_s' => 'פרסום חינם עם עוזר חכם לניסוח המודעה', 'u_rooms' => "חד'", 'u_sqm' => 'מ״ר', 'u_floor' => 'קומה', 'ls_city_pre' => 'דירות למכירה ב',
			// areas band
			'ar_kicker' => 'אזורי ביקוש', 'ar_title' => 'לאן קונים מסתכלים עכשיו', 'ar_projects' => 'פרויקטים', 'ar_apts' => 'דירות', 'ar_project_one' => 'פרויקט אחד', 'ar_apt_one' => 'דירה אחת',
			'sh_chip' => 'הדגם התלת ממדי האמיתי של הפרויקט', 'sh_spin' => 'הקישו לסיבוב בתלת ממד', 'sh_floors' => 'קומות', 'fl_kicker' => 'החוויה המלאה', 'fl_title' => 'בחרו דירה מתוך הבניין, בתלת ממד', 'fl_sub' => 'מגדלי הדגל של קו החוף החדש: מסובבים את הבניין, בוחרים קומה וכיוון, רואים את הנוף על המפה, ובונים בקשת הצעה בחינם.', 'fl_all' => 'לקטלוג התלת ממד ←', 'fl_go' => 'לסיור בפרויקט ←',
			// magazine band
			'mg_kicker' => 'המגזין', 'mg_title' => 'חדשות, ניתוחים ומדריכים', 'mg_rail' => 'המדריכים החשובים', 'guide_buy' => 'קניית דירה: המדריך המלא',
			// tools band
			'tl_kicker' => 'כלים', 'tl_title' => 'בדיקות שחוסכות טעויות יקרות', 'tl_lead_b' => 'כמה שווה הדירה שלכם?', 'tl_lead_s' => 'אומדן ראשוני חינם, ומשם לשמאי מוסמך אם רוצים הערכה מדויקת', 'tl_mort_s' => 'ההחזר החודשי האמיתי', 'tl_tax_b' => 'מס רכישה', 'tl_tax_s' => 'מדרגות 2026', 'tl_full_s' => 'כל ההוצאות הנלוות', 'tl_glos_s' => 'תמ״א, פינוי-בינוי, הערת אזהרה',
			// pros band
			'pr_kicker' => 'אנשי מקצוע', 'pr_title' => 'הליווי הנכון לעסקה', 'pr_more_pre' => 'עוד', 'pr_more_suf' => 'אנשי מקצוע ←', 'pr_lawyer' => 'עו״ד מקרקעין', 'pr_shamai' => 'שמאי מקרקעין', 'pr_mashkanta' => 'יועץ משכנתאות', 'pr_bedek' => 'בדק בית', 'pr_sponsored' => 'ממומן', 'pr_join_b' => '+ הצטרפו למאגר', 'pr_join_s' => 'חשיפה לקונים ומשקיעים',
			// megafooter
			'mf_apts_city' => 'דירות לפי עיר', 'mf_proj_city' => 'פרויקטים לפי עיר', 'mf_calc' => 'מחשבונים ומדריכים', 'buying_kablan' => 'קניית דירה מקבלן', 'mf_pros' => 'אנשי מקצוע', 'mf_brand' => 'נדלן', 'advertise_pros' => 'פרסום לבעלי מקצוע ויזמים', 'contact' => 'צור קשר', 'legal' => 'המידע באתר כללי ואינו ייעוץ. אומדני מחיר אינם מחייבים. הדמיות להמחשה בלבד עד לאישור חומרים רשמיים של היזם.',
			// switcher / generic
			'lang_label' => 'שפה', 'content_he_note' => 'התוכן המלא מוצג בעברית; תרגום מלא בקרוב.',
		),
		'en' => array(
			'hero_h1'   => 'Find an apartment, check the price, know the area - before you sign',
			'hero_sub'  => 'Apartments for sale and rent, new projects where you pick your apartment from inside the building, real transaction prices and check-it-yourself tools - in one place.',
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
			'tk_tlv' => 'Avg price/m², new Tel Aviv projects', 'tk_watch' => 'Avg price/m², tracked projects', 'tk_projects' => 'projects tracked', 'tk_source' => 'based on the NadLan catalog', 'mk_title' => 'Where the market is heading', 'mk_tlv' => 'Avg price/m² in new Tel Aviv projects', 'mk_watch' => 'Avg price/m² in tracked projects', 'mk_yoy' => 'Yearly change in home prices', 'mk_rate' => 'Average mortgage rate', 'mk_note_pre' => 'Based on the NadLan catalog · updated ',
			'pj_kicker' => 'New from the developer', 'pj_title' => 'Pick your apartment from inside the building', 'pj_all' => 'All projects →', 'pj_pick' => 'Choose an apartment from inside the building', 'pj_units_pick' => 'apartments to choose', 'pj_est_pre' => 'est. ~', 'pj_est_suf' => '₪/m² · non-binding', 'pj_live' => 'Live view', 'pj_viewer_note' => 'Illustration only. Drag to rotate; click the project name for the full page.', 'pj_dark_note' => 'Estimates are non-binding and based on public data. Renderings are illustrative until the developer confirms official materials.',
			'ls_kicker' => 'For sale and rent', 'ls_title' => 'New in the system', 'ls_all' => 'All apartments →', 'ls_cta_b' => '+ Listing an apartment?', 'ls_cta_s' => 'Post free with a smart assistant to write the ad', 'u_rooms' => 'rooms', 'u_sqm' => 'm²', 'u_floor' => 'Floor', 'ls_city_pre' => 'Apartments for sale in ',
			'ar_kicker' => 'In-demand areas', 'ar_title' => 'Where buyers are looking now', 'ar_projects' => 'projects', 'ar_apts' => 'apartments', 'ar_project_one' => 'one project', 'ar_apt_one' => 'one apartment',
			'sh_chip' => 'The project\'s real 3D model', 'sh_spin' => 'Tap to spin in 3D', 'sh_floors' => 'floors', 'fl_kicker' => 'The full experience', 'fl_title' => 'Choose your apartment from inside the building, in 3D', 'fl_sub' => 'The flagship towers of the new coastline: rotate the building, pick a floor and orientation, see the view on the map, and build a free offer request.', 'fl_all' => 'Open the 3D catalog', 'fl_go' => 'Tour the project',
			'mg_kicker' => 'The magazine', 'mg_title' => 'News, analysis and guides', 'mg_rail' => 'Essential guides', 'guide_buy' => 'Buying a home: the full guide',
			'tl_kicker' => 'Tools', 'tl_title' => 'Checks that save costly mistakes', 'tl_lead_b' => "What's your home worth?", 'tl_lead_s' => 'A free first estimate, then a certified appraiser if you want a precise valuation', 'tl_mort_s' => 'Your real monthly payment', 'tl_tax_b' => 'Purchase tax', 'tl_tax_s' => '2026 brackets', 'tl_full_s' => 'All the side costs', 'tl_glos_s' => 'TAMA, evacuate-rebuild, caution note',
			'pr_kicker' => 'Professionals', 'pr_title' => 'The right guidance for the deal', 'pr_more_pre' => 'Another', 'pr_more_suf' => 'professionals →', 'pr_lawyer' => 'Real-estate lawyer', 'pr_shamai' => 'Property appraiser', 'pr_mashkanta' => 'Mortgage advisor', 'pr_bedek' => 'Home inspection', 'pr_sponsored' => 'Sponsored', 'pr_join_b' => '+ Join the directory', 'pr_join_s' => 'Exposure to buyers and investors',
			'mf_apts_city' => 'Apartments by city', 'mf_proj_city' => 'Projects by city', 'mf_calc' => 'Calculators & guides', 'buying_kablan' => 'Buying from a developer', 'mf_pros' => 'Professionals', 'mf_brand' => 'NadLan', 'advertise_pros' => 'Advertise for professionals & developers', 'contact' => 'Contact', 'legal' => 'Information on the site is general and not advice. Price estimates are non-binding. Renderings are illustrative only until the developer confirms official materials.',
			'lang_label' => 'Language', 'content_he_note' => 'Full content is shown in Hebrew; complete translation coming soon.',
		),
		'fr' => array(
			'hero_h1'   => 'Trouvez un appartement, vérifiez le prix, connaissez le quartier - avant de signer',
			'hero_sub'  => 'Appartements à vendre et à louer, projets neufs où vous choisissez votre appartement depuis le bâtiment, prix de transactions réels et outils de vérification - au même endroit.',
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
			'tk_tlv' => 'Prix moyen/m², projets neufs à Tel Aviv', 'tk_watch' => 'Prix moyen/m², projets suivis', 'tk_projects' => 'projets suivis', 'tk_source' => "d'après le catalogue NadLan", 'mk_title' => 'Où va le marché', 'mk_tlv' => 'Prix moyen/m² dans les projets neufs à Tel Aviv', 'mk_watch' => 'Prix moyen/m² dans les projets suivis', 'mk_yoy' => 'Variation annuelle des prix', 'mk_rate' => 'Taux de prêt moyen', 'mk_note_pre' => 'D\'après le catalogue NadLan · mis à jour ',
			'pj_kicker' => 'Neuf du promoteur', 'pj_title' => "Choisissez votre appartement depuis le bâtiment", 'pj_all' => 'Tous les projets →', 'pj_pick' => "Choisir un appartement depuis le bâtiment", 'pj_units_pick' => 'appartements au choix', 'pj_est_pre' => 'est. ~', 'pj_est_suf' => '₪/m² · non contractuel', 'pj_live' => 'Vue en direct', 'pj_viewer_note' => 'Illustration seulement. Faites glisser pour tourner ; cliquez sur le nom du projet pour la page complète.', 'pj_dark_note' => 'Les estimations sont non contractuelles et basées sur des données publiques. Les rendus sont illustratifs jusqu\'à confirmation des documents officiels du promoteur.',
			'ls_kicker' => 'À vendre et à louer', 'ls_title' => 'Nouveautés dans le système', 'ls_all' => 'Tous les appartements →', 'ls_cta_b' => '+ Publier un appartement ?', 'ls_cta_s' => 'Publication gratuite avec un assistant intelligent pour rédiger l\'annonce', 'u_rooms' => 'pièces', 'u_sqm' => 'm²', 'u_floor' => 'Étage', 'ls_city_pre' => 'Appartements à vendre à ',
			'ar_kicker' => 'Zones prisées', 'ar_title' => 'Où regardent les acheteurs', 'ar_projects' => 'projets', 'ar_apts' => 'appartements', 'ar_project_one' => 'un projet', 'ar_apt_one' => 'un appartement',
			'sh_chip' => 'Le vrai modele 3D du projet', 'sh_spin' => 'Touchez pour faire pivoter en 3D', 'sh_floors' => 'etages', 'fl_kicker' => 'L experience complete', 'fl_title' => 'Choisissez votre appartement depuis le batiment, en 3D', 'fl_sub' => 'Les tours phares du nouveau littoral: faites pivoter le batiment, choisissez etage et orientation, voyez la vue sur la carte.', 'fl_all' => 'Catalogue 3D', 'fl_go' => 'Visiter le projet',
			'mg_kicker' => 'Le magazine', 'mg_title' => 'Actualités, analyses et guides', 'mg_rail' => 'Guides essentiels', 'guide_buy' => 'Acheter un bien : le guide complet',
			'tl_kicker' => 'Outils', 'tl_title' => 'Des vérifications qui évitent des erreurs coûteuses', 'tl_lead_b' => 'Combien vaut votre bien ?', 'tl_lead_s' => 'Une première estimation gratuite, puis un expert agréé pour une évaluation précise', 'tl_mort_s' => 'Votre vraie mensualité', 'tl_tax_b' => "Taxe d'achat", 'tl_tax_s' => 'Barèmes 2026', 'tl_full_s' => 'Tous les frais annexes', 'tl_glos_s' => 'TAMA, démolition-reconstruction, note d\'avertissement',
			'pr_kicker' => 'Professionnels', 'pr_title' => "Le bon accompagnement pour l'affaire", 'pr_more_pre' => 'Encore', 'pr_more_suf' => 'professionnels →', 'pr_lawyer' => 'Avocat immobilier', 'pr_shamai' => 'Expert immobilier', 'pr_mashkanta' => 'Conseiller en prêt', 'pr_bedek' => 'Inspection du logement', 'pr_sponsored' => 'Sponsorisé', 'pr_join_b' => "+ Rejoindre l'annuaire", 'pr_join_s' => 'Visibilité auprès des acheteurs et investisseurs',
			'mf_apts_city' => 'Appartements par ville', 'mf_proj_city' => 'Projets par ville', 'mf_calc' => 'Calculateurs & guides', 'buying_kablan' => 'Acheter chez un promoteur', 'mf_pros' => 'Professionnels', 'mf_brand' => 'NadLan', 'advertise_pros' => 'Publicité pour pros & promoteurs', 'contact' => 'Contact', 'legal' => 'Les informations du site sont générales et ne constituent pas un conseil. Les estimations de prix sont non contractuelles. Les rendus sont illustratifs jusqu\'à confirmation des documents officiels du promoteur.',
			'lang_label' => 'Langue', 'content_he_note' => 'Le contenu complet est en hébreu ; traduction complète à venir.',
		),
		'ru' => array(
			'hero_h1'   => 'Найдите квартиру, проверьте цену, узнайте район - до подписания',
			'hero_sub'  => 'Квартиры на продажу и в аренду, новые проекты с выбором квартиры прямо из здания, реальные цены сделок и инструменты проверки - в одном месте.',
			'tab_buy' => 'Купить', 'tab_rent' => 'Аренда', 'tab_projects' => 'Новые проекты', 'tab_pros' => 'Специалисты',
			'search_ph' => 'Город, район, проект или специалист…', 'search_btn' => 'Поиск',
			'trust_projects' => 'проектов и реновации', 'trust_pros' => 'проверенных специалистов (gov.il)',
			'trust_calc' => 'профессиональных калькулятора', 'trust_law' => 'юрист по недвижимости', 'trust_law_pre' => 'сопровождение -',
			'flag_pick' => 'Выберите квартиру прямо из здания',
			'nav_label' => 'Основная навигация',
			'm_apts' => 'Квартиры', 'apts_sale' => 'Продажа', 'apts_rent' => 'Аренда', 'apts_in' => 'Квартиры в ', 'post_free' => 'Разместить объявление бесплатно',
			'm_projects' => 'Новые проекты', 'all_projects' => 'Все проекты', 'projects_in' => 'Проекты в ', 'pinui' => 'Снос-застройка', 'tama' => 'ТАМА 38',
			'm_prices' => 'Цены и данные', 'my_value' => 'Сколько стоит моя квартира', 'prices_in' => 'Цены в ',
			'm_guides' => 'Гиды и инструменты', 'calc_mortgage' => 'Ипотечный калькулятор', 'calc_tax' => 'Калькулятор налога на покупку', 'calc_full' => 'Полная стоимость сделки',
			'value' => 'Стоимость жилья', 'buying_guide' => 'Покупка жилья: гид', 'tabu' => 'Проверка в земельном реестре', 'invest' => 'Инвестиции в недвижимость', 'glossary' => 'Глоссарий',
			'm_pros' => 'Специалисты', 'all_pros' => 'Весь каталог', 'join_dir' => 'Присоединиться к каталогу',
			'tk_tlv' => 'Ср. цена/м², новые проекты ТА', 'tk_watch' => 'Ср. цена/м², отслеживаемые проекты', 'tk_projects' => 'проектов отслеживается', 'tk_source' => 'по каталогу NadLan', 'mk_title' => 'Куда идёт рынок', 'mk_tlv' => 'Средняя цена/м² в новых проектах Тель-Авива', 'mk_watch' => 'Средняя цена/м² в отслеживаемых проектах', 'mk_yoy' => 'Годовое изменение цен', 'mk_rate' => 'Средняя ставка по ипотеке', 'mk_note_pre' => 'По каталогу NadLan · обновлено ',
			'pj_kicker' => 'Новое от застройщика', 'pj_title' => 'Выберите квартиру прямо из здания', 'pj_all' => 'Все проекты →', 'pj_pick' => 'Выбрать квартиру прямо из здания', 'pj_units_pick' => 'квартир на выбор', 'pj_est_pre' => 'оц. ~', 'pj_est_suf' => '₪/м² · необязывающе', 'pj_live' => 'Живой просмотр', 'pj_viewer_note' => 'Иллюстрация. Тяните для поворота; нажмите название проекта для полной страницы.', 'pj_dark_note' => 'Оценки необязывающие и основаны на открытых данных. Визуализации иллюстративны до подтверждения официальных материалов застройщика.',
			'ls_kicker' => 'Продажа и аренда', 'ls_title' => 'Новое в системе', 'ls_all' => 'Все квартиры →', 'ls_cta_b' => '+ Размещаете квартиру?', 'ls_cta_s' => 'Бесплатно с умным помощником для составления объявления', 'u_rooms' => 'комн.', 'u_sqm' => 'м²', 'u_floor' => 'Этаж', 'ls_city_pre' => 'Квартиры на продажу в ',
			'ar_kicker' => 'Востребованные районы', 'ar_title' => 'Куда смотрят покупатели сейчас', 'ar_projects' => 'проектов', 'ar_apts' => 'квартир', 'ar_project_one' => 'один проект', 'ar_apt_one' => 'одна квартира',
			'sh_chip' => 'Настоящая 3D модель проекта', 'sh_spin' => 'Нажмите чтобы вращать в 3D', 'sh_floors' => 'этажей', 'fl_kicker' => 'Полный опыт', 'fl_title' => 'Выберите квартиру изнутри здания, в 3D', 'fl_sub' => 'Флагманские башни новой береговой линии: вращайте здание, выбирайте этаж и ориентацию, смотрите вид на карте.', 'fl_all' => '3D каталог', 'fl_go' => 'Тур по проекту',
			'mg_kicker' => 'Журнал', 'mg_title' => 'Новости, аналитика и гиды', 'mg_rail' => 'Ключевые гиды', 'guide_buy' => 'Покупка жилья: полный гид',
			'tl_kicker' => 'Инструменты', 'tl_title' => 'Проверки, что берегут от дорогих ошибок', 'tl_lead_b' => 'Сколько стоит ваша квартира?', 'tl_lead_s' => 'Бесплатная первичная оценка, затем сертифицированный оценщик для точной оценки', 'tl_mort_s' => 'Ваш реальный ежемесячный платёж', 'tl_tax_b' => 'Налог на покупку', 'tl_tax_s' => 'Ставки 2026', 'tl_full_s' => 'Все сопутствующие расходы', 'tl_glos_s' => 'ТАМА, снос-застройка, предупреждение',
			'pr_kicker' => 'Специалисты', 'pr_title' => 'Верное сопровождение сделки', 'pr_more_pre' => 'Ещё', 'pr_more_suf' => 'специалистов →', 'pr_lawyer' => 'Юрист по недвижимости', 'pr_shamai' => 'Оценщик', 'pr_mashkanta' => 'Ипотечный консультант', 'pr_bedek' => 'Осмотр жилья', 'pr_sponsored' => 'Реклама', 'pr_join_b' => '+ В каталог', 'pr_join_s' => 'Доступ к покупателям и инвесторам',
			'mf_apts_city' => 'Квартиры по городам', 'mf_proj_city' => 'Проекты по городам', 'mf_calc' => 'Калькуляторы и гиды', 'buying_kablan' => 'Покупка у застройщика', 'mf_pros' => 'Специалисты', 'mf_brand' => 'NadLan', 'advertise_pros' => 'Реклама для специалистов и застройщиков', 'contact' => 'Контакты', 'legal' => 'Информация на сайте общая и не является консультацией. Оценки цен необязывающие. Визуализации иллюстративны до подтверждения официальных материалов застройщика.',
			'lang_label' => 'Язык', 'content_he_note' => 'Полный контент показан на иврите; полный перевод скоро.',
		),
		'ar' => array(
			'hero_h1'   => 'اعثر على شقة، تحقق من السعر، اعرف الحي - قبل التوقيع',
			'hero_sub'  => 'شقق للبيع والإيجار، مشاريع جديدة تختار فيها شقتك من داخل المبنى، أسعار صفقات حقيقية وأدوات فحص - في مكان واحد.',
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
			'tk_tlv' => 'متوسط السعر/م²، مشاريع تل أبيب الجديدة', 'tk_watch' => 'متوسط السعر/م²، مشاريع متابَعة', 'tk_projects' => 'مشاريع متابَعة', 'tk_source' => 'بناءً على كتالوج ندلان', 'mk_title' => 'إلى أين يتجه السوق', 'mk_tlv' => 'متوسط السعر/م² في مشاريع تل أبيب الجديدة', 'mk_watch' => 'متوسط السعر/م² في المشاريع المتابَعة', 'mk_yoy' => 'التغير السنوي في الأسعار', 'mk_rate' => 'متوسط فائدة الرهن', 'mk_note_pre' => 'بناءً على كتالوج ندلان · محدّث ',
			'pj_kicker' => 'جديد من المطوّر', 'pj_title' => 'اختر شقتك من داخل المبنى', 'pj_all' => 'كل المشاريع →', 'pj_pick' => 'اختر شقة من داخل المبنى', 'pj_units_pick' => 'شقق للاختيار', 'pj_est_pre' => 'تقدير ~', 'pj_est_suf' => '₪/م² · غير مُلزم', 'pj_live' => 'عرض حي', 'pj_viewer_note' => 'محاكاة توضيحية. اسحب للتدوير، انقر اسم المشروع للصفحة الكاملة.', 'pj_dark_note' => 'التقديرات غير مُلزمة ومبنية على بيانات علنية. الصور توضيحية حتى تأكيد المطوّر للمواد الرسمية.',
			'ls_kicker' => 'للبيع والإيجار', 'ls_title' => 'جديد في النظام', 'ls_all' => 'كل الشقق →', 'ls_cta_b' => '+ تنشر شقة؟', 'ls_cta_s' => 'نشر مجاني مع مساعد ذكي لصياغة الإعلان', 'u_rooms' => 'غرف', 'u_sqm' => 'م²', 'u_floor' => 'طابق', 'ls_city_pre' => 'شقق للبيع في ',
			'ar_kicker' => 'مناطق مطلوبة', 'ar_title' => 'أين ينظر المشترون الآن', 'ar_projects' => 'مشاريع', 'ar_apts' => 'شقق', 'ar_project_one' => 'مشروع واحد', 'ar_apt_one' => 'شقة واحدة',
			'sh_chip' => 'نموذج ثلاثي الأبعاد حقيقي للمشروع', 'sh_spin' => 'انقروا للتدوير ثلاثي الأبعاد', 'sh_floors' => 'طوابق', 'fl_kicker' => 'التجربة الكاملة', 'fl_title' => 'اختاروا شقتكم من داخل المبنى، بتقنية ثلاثية الأبعاد', 'fl_sub' => 'أبراج الواجهة البحرية الجديدة: دوروا المبنى، اختاروا الطابق والاتجاه، وشاهدوا الإطلالة على الخريطة.', 'fl_all' => 'كتالوج ثلاثي الأبعاد', 'fl_go' => 'جولة في المشروع',
			'mg_kicker' => 'المجلة', 'mg_title' => 'أخبار وتحليلات وأدلة', 'mg_rail' => 'الأدلة الأساسية', 'guide_buy' => 'شراء شقة: الدليل الكامل',
			'tl_kicker' => 'أدوات', 'tl_title' => 'فحوصات توفّر أخطاءً مكلفة', 'tl_lead_b' => 'كم تساوي شقتك؟', 'tl_lead_s' => 'تقدير أولي مجاني، ثم مثمّن معتمد لتقييم دقيق إن أردت', 'tl_mort_s' => 'قسطك الشهري الحقيقي', 'tl_tax_b' => 'ضريبة الشراء', 'tl_tax_s' => 'شرائح 2026', 'tl_full_s' => 'كل التكاليف الجانبية', 'tl_glos_s' => 'تاما، هدم وإعادة بناء، ملاحظة تحذير',
			'pr_kicker' => 'مختصون', 'pr_title' => 'المرافقة الصحيحة للصفقة', 'pr_more_pre' => 'المزيد', 'pr_more_suf' => 'مختصين →', 'pr_lawyer' => 'محامي عقارات', 'pr_shamai' => 'مثمّن عقاري', 'pr_mashkanta' => 'مستشار رهن', 'pr_bedek' => 'فحص المنزل', 'pr_sponsored' => 'مموَّل', 'pr_join_b' => '+ انضم إلى الدليل', 'pr_join_s' => 'وصول إلى المشترين والمستثمرين',
			'mf_apts_city' => 'شقق حسب المدينة', 'mf_proj_city' => 'مشاريع حسب المدينة', 'mf_calc' => 'حاسبات وأدلة', 'buying_kablan' => 'الشراء من مطوّر', 'mf_pros' => 'مختصون', 'mf_brand' => 'ندلان', 'advertise_pros' => 'إعلان للمختصين والمطوّرين', 'contact' => 'اتصل بنا', 'legal' => 'المعلومات في الموقع عامة وليست استشارة. تقديرات الأسعار غير مُلزمة. الصور توضيحية فقط حتى تأكيد المطوّر للمواد الرسمية.',
			'lang_label' => 'اللغة', 'content_he_note' => 'المحتوى الكامل معروض بالعبرية؛ الترجمة الكاملة قريباً.',
		),
		);
		return $t;
	}
}

/* CMS-backed override layer: translations editable in the DB (option per lang)
   without a code deploy - "wired to the CMS". A generation run / editor pushes
   strings via POST /nadlan/v1/i18n/<lang>. Overrides win over the code default. */
if ( ! function_exists( 'nadlan_i18n_overrides' ) ) {
	function nadlan_i18n_overrides( $lang ) {
		static $c = array();
		if ( ! isset( $c[ $lang ] ) ) { $c[ $lang ] = (array) get_option( 'nadlan_i18n_ov_' . $lang, array() ); }
		return $c[ $lang ];
	}
}
if ( ! function_exists( 'nadlan_i18n' ) ) {
	function nadlan_i18n( $key, $lang = null ) {
		$lang = $lang ? $lang : nadlan_current_lang();
		$ov = nadlan_i18n_overrides( $lang );
		if ( isset( $ov[ $key ] ) && '' !== $ov[ $key ] ) { return $ov[ $key ]; }
		$t = nadlan_i18n_table();
		if ( isset( $t[ $lang ][ $key ] ) ) { return $t[ $lang ][ $key ]; }
		if ( isset( $t['he'][ $key ] ) ) { return $t['he'][ $key ]; } // honest fallback
		return $key;
	}
}
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/i18n/(?P<lang>[a-z]{2})', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback'            => function ( $req ) {
			$lang = (string) $req['lang'];
			if ( ! in_array( $lang, nadlan_langs(), true ) ) { return new WP_Error( 'bad_lang', 'unknown language', array( 'status' => 400 ) ); }
			$params = (array) $req->get_json_params();
			$strings = isset( $params['strings'] ) && is_array( $params['strings'] ) ? $params['strings'] : array();
			$cur = (array) get_option( 'nadlan_i18n_ov_' . $lang, array() );
			foreach ( $strings as $k => $v ) { $cur[ sanitize_key( $k ) ] = sanitize_text_field( (string) $v ); }
			update_option( 'nadlan_i18n_ov_' . $lang, $cur );
			return array( 'lang' => $lang, 'stored' => count( $cur ) );
		},
	) );
} );
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

/* Translate the block-theme HEADER + FOOTER (hardcoded Hebrew, not in this
   plugin) on language pages via a scoped output buffer + finite string map.
   Systematic (map-driven), only runs on /en /fr /ru /ar, never touches Hebrew. */
if ( ! function_exists( 'nadlan_i18n_theme_map' ) ) {
	function nadlan_i18n_theme_map( $lang ) {
		$m = array(
			'en' => array( 'פרויקטים'=>'Projects','אזורי ביקוש'=>'Areas','מחשבונים'=>'Calculators','אנשי מקצוע'=>'Professionals','מדריכים'=>'Guides','בחרו פרויקט'=>'Choose a project','נדל״ן לפני שפונים ליזם'=>'Real estate - before you approach the developer','לדלג לתוכן'=>'Skip to content','כל הפרויקטים'=>'All projects','מחשבון משכנתא'=>'Mortgage calculator','מס רכישה'=>'Purchase tax','מדריך קנייה'=>'Buying guide','בדיקה משפטית'=>'Legal check','אודות'=>'About','צור קשר'=>'Contact','רובע שדה דב'=>'Sde Dov district','עו״ד מקרקעין'=>'Real-estate lawyer','שמאי מקרקעין'=>'Property appraiser','יועץ משכנתאות'=>'Mortgage advisor','בדק בית'=>'Home inspection','קבלן'=>'Contractor','אדריכל'=>'Architect' ),
			'fr' => array( 'פרויקטים'=>'Projets','אזורי ביקוש'=>'Zones','מחשבונים'=>'Calculateurs','אנשי מקצוע'=>'Professionnels','מדריכים'=>'Guides','בחרו פרויקט'=>'Choisir un projet','נדל״ן לפני שפונים ליזם'=>"L'immobilier - avant de contacter le promoteur",'לדלג לתוכן'=>'Aller au contenu','כל הפרויקטים'=>'Tous les projets','מחשבון משכנתא'=>'Calculateur de prêt','מס רכישה'=>"Taxe d'achat",'מדריך קנייה'=>"Guide d'achat",'בדיקה משפטית'=>'Vérification juridique','אודות'=>'À propos','צור קשר'=>'Contact','רובע שדה דב'=>'Quartier Sde Dov','עו״ד מקרקעין'=>'Avocat immobilier','שמאי מקרקעין'=>'Expert immobilier','יועץ משכנתאות'=>'Conseiller en prêt','בדק בית'=>'Inspection du logement','קבלן'=>'Entrepreneur','אדריכל'=>'Architecte' ),
			'ru' => array( 'פרויקטים'=>'Проекты','אזורי ביקוש'=>'Районы','מחשבונים'=>'Калькуляторы','אנשי מקצוע'=>'Специалисты','מדריכים'=>'Гиды','בחרו פרויקט'=>'Выбрать проект','נדל״ן לפני שפונים ליזם'=>'Недвижимость - до обращения к застройщику','לדלג לתוכן'=>'Перейти к содержимому','כל הפרויקטים'=>'Все проекты','מחשבון משכנתא'=>'Ипотечный калькулятор','מס רכישה'=>'Налог на покупку','מדריך קנייה'=>'Гид покупки','בדיקה משפטית'=>'Юридическая проверка','אודות'=>'О нас','צור קשר'=>'Контакты','רובע שדה דב'=>'Район Сде-Дов','עו״ד מקרקעין'=>'Юрист по недвижимости','שמאי מקרקעין'=>'Оценщик','יועץ משכנתאות'=>'Ипотечный консультант','בדק בית'=>'Осмотр жилья','קבלן'=>'Подрядчик','אדריכל'=>'Архитектор' ),
			'ar' => array( 'פרויקטים'=>'مشاريع','אזורי ביקוש'=>'مناطق','מחשבונים'=>'حاسبات','אנשי מקצוע'=>'مختصون','מדריכים'=>'أدلة','בחרו פרויקט'=>'اختر مشروعاً','נדל״ן לפני שפונים ליזם'=>'عقارات - قبل التوجه إلى المطوّر','לדלג לתוכן'=>'تخطَّ إلى المحتوى','כל הפרויקטים'=>'كل المشاريع','מחשבון משכנתא'=>'حاسبة الرهن','מס רכישה'=>'ضريبة الشراء','מדריך קנייה'=>'دليل الشراء','בדיקה משפטית'=>'فحص قانوني','אודות'=>'حول','צור קשר'=>'اتصل بنا','רובע שדה דב'=>'حي سديه دوف','עו״ד מקרקעין'=>'محامي عقارات','שמאי מקרקעין'=>'مثمّن عقاري','יועץ משכנתאות'=>'مستشار رهن','בדק בית'=>'فحص المنزل','קבלן'=>'مقاول','אדריכל'=>'معماري' ),
		);
		return isset( $m[ $lang ] ) ? $m[ $lang ] : array();
	}
}
add_action( 'template_redirect', function () {
	if ( is_admin() || ! nadlan_is_language_home() || 'he' === nadlan_current_lang() ) { return; }
	ob_start( function ( $html ) {
		$map = nadlan_i18n_theme_map( nadlan_current_lang() );
		return $map ? strtr( $html, $map ) : $html;
	} );
}, 1 );

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
	echo "\n<link rel=\"canonical\" href=\"" . esc_url( $urls[ $cur ] ) . "\">\n";
	foreach ( nadlan_langs() as $l ) {
		printf( "<link rel=\"alternate\" hreflang=\"%s\" href=\"%s\">\n", esc_attr( $l ), esc_url( $urls[ $l ] ) );
	}
	printf( "<link rel=\"alternate\" hreflang=\"x-default\" href=\"%s\">\n", esc_url( $urls['he'] ) );
}, 1 );
