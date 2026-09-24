<?php
/**
 * nadlan-config · Broker drop box (x-broker-drop) · v1.1.0 · 23.9.2026
 *
 * Owner order 23.9.2026 (voice): a broker gets one private address, throws photos and a few lines at it,
 * and the system builds the property in the broker's own website. No replies. No login. No owner step.
 * For every future broker, not only the first one.
 *
 * The address is a personal link: https://nad-lan.co.il/drop/<token>/
 *   photos + free text  ->  the AI reads the facts and keeps only what the broker wrote (numbers are checked)
 *   ->  it writes the page in the luxury-broker voice (docs/dna/luxury-broker-copy-dna-2026-09.md), gated
 *   ->  a Hebrew listing at /properties/<latin-slug>/ and, when the broker has an English site, its English twin
 *   ->  the property shows first in the broker's own site, with hreflang between the languages.
 * The broker sees the result on the same screen; nothing is sent to anyone.
 * The same screen lists the broker's properties: sold or let in one tap (Brokers Ethics Regulations,
 * reg. 19(c): a publication is removed or updated once the property is off the market), a new price in two.
 * Every listing carries the broker's name, "broker" status and licence number (reg. 19(a)).
 *
 * 1.1 (owner order 23.9, "do it all, each one in the best and most profound way"):
 *   - four languages: Hebrew and English from the writing step, Russian and French from a second, gated
 *     translation step (no hype words, the broker's numbers only, place names kept out of the claim check);
 *   - the broker's site in each language: a broker who joined alone (x-broker-join) gets an engine-built site;
 *     the English, Russian and French sites appear with the first listing in that language;
 *   - owners (x-owner-wizard) publish through the same engine, without a licence line and without a site;
 *   - the token use and cost of every submission are kept on it (nl_usage).
 *
 * Installed as the persistent Code Snippet "x-broker-drop" by scripts/broker-drop/deploydrop.py.
 * Rollback: python scripts/broker-drop/deploydrop.py --off
 */

if ( ! defined( 'ABSPATH' ) ) { return; }
if ( defined( 'NL_DROP_VERSION' ) ) { return; }
define( 'NL_DROP_VERSION', '1.1.3' );
define( 'NL_DROP_MAX_BYTES', 15728640 );
define( 'NL_DROP_MAX_PHOTOS', 30 );

/* =====================================================================================================
 * Registration: meta the deploy script and the admin box write, and the private submissions log.
 * ===================================================================================================== */
add_action( 'init', function () {
	$auth = function () { return current_user_can( 'edit_posts' ); };
	$str  = array( 'type' => 'string', 'single' => true, 'show_in_rest' => true, 'auth_callback' => $auth );
	foreach ( array( 'nl_drop_on', 'nl_name_he', 'nl_name_en', 'nl_name_ru', 'nl_brand_en', 'nl_gender', 'nl_site_he', 'nl_site_en', 'nl_site_ru', 'nl_site_fr', 'nl_auto_publish', 'nl_langs', 'nl_tier', 'nl_slug', 'nl_hero', 'nl_areas_en', 'nl_areas_ru', 'nl_areas_fr', 'nl_bio_en' ) as $k ) {
		register_post_meta( 'nadlan_professional', $k, $str );
	}
	foreach ( array( 'nadlan_property', 'page' ) as $t ) {
		foreach ( array( 'nl_broker_id', 'nl_card_key', 'nl_twin', 'nl_twins', 'nl_status', 'nl_broker_site', 'nl_broker_auto', 'nl_lang', 'nl_drop_id' ) as $k ) {
			register_post_meta( $t, $k, $str );
		}
	}
	register_post_type( 'nadlan_drop', array(
		'labels'          => array( 'name' => 'תיבת נכסים', 'singular_name' => 'שליחה', 'menu_name' => 'תיבת נכסים', 'all_items' => 'תיבת נכסים' ),
		'public'          => false,
		'show_ui'         => true,
		'show_in_menu'    => 'edit.php?post_type=nadlan_professional',
		'supports'        => array( 'title', 'editor' ),
		'capability_type' => 'post',
		'map_meta_cap'    => true,
		'capabilities'    => array( 'create_posts' => 'do_not_allow' ),
	) );
}, 20 );

/* The personal link is a secret: never in a REST response, whatever else registers the key. */
add_filter( 'rest_prepare_nadlan_professional', function ( $resp ) {
	if ( $resp instanceof WP_REST_Response ) {
		$d = $resp->get_data();
		if ( isset( $d['meta'] ) && is_array( $d['meta'] ) ) {
			unset( $d['meta']['nl_drop_token'], $d['meta']['_nl_drop_token'], $d['meta']['_nl_email'] );
			$resp->set_data( $d );
		}
	}
	return $resp;
}, 99 );

/* =====================================================================================================
 * Brokers
 * ===================================================================================================== */
/** The languages a listing and a broker site can live in. Hebrew is always the first. */
function nl_drop_langs() {
	return array( 'he', 'en', 'ru', 'fr' );
}

function nl_drop_L( $lang ) {
	return in_array( (string) $lang, nl_drop_langs(), true ) ? (string) $lang : 'he';
}

function nl_drop_rtl( $lang ) {
	return nl_drop_L( $lang ) === 'he';
}

function nl_drop_broker( $pid ) {
	$p = get_post( (int) $pid );
	if ( ! $p || $p->post_type !== 'nadlan_professional' ) { return null; }
	$m = function ( $k ) use ( $p ) { return trim( (string) get_post_meta( $p->ID, $k, true ) ); };
	$split   = function ( $v ) { return array_values( array_filter( array_map( 'trim', explode( ',', (string) $v ) ) ) ); };
	$parts   = preg_split( '/\s*·\s*/u', (string) $p->post_title );
	$name_he = $m( 'nl_name_he' ) !== '' ? $m( 'nl_name_he' ) : trim( (string) $parts[0] );
	$name_en = $m( 'nl_name_en' ) !== '' ? $m( 'nl_name_en' ) : $name_he;
	$phone   = $m( 'phone' );
	$digits  = preg_replace( '/\D+/', '', $phone );
	if ( $digits !== '' && $digits[0] === '0' ) { $digits = '972' . substr( $digits, 1 ); }
	$nat  = strpos( $digits, '972' ) === 0 ? substr( $digits, 3 ) : '';
	$intl = strlen( $nat ) >= 8 ? '+972 ' . substr( $nat, 0, 2 ) . '-' . substr( $nat, 2, 3 ) . '-' . substr( $nat, 5 ) : $phone;
	$photos   = $split( $m( 'photos_csv' ) );
	$b = array(
		'id'         => (int) $p->ID,
		'kind'       => 'broker',
		'name_he'    => $name_he,
		'name_en'    => $name_en,
		'name_ru'    => $m( 'nl_name_ru' ) !== '' ? $m( 'nl_name_ru' ) : $name_en,
		'brand_he'   => $m( 'company_name' ),
		'brand_en'   => $m( 'nl_brand_en' ) !== '' ? $m( 'nl_brand_en' ) : ( preg_match( '/\p{Hebrew}/u', $m( 'company_name' ) ) ? '' : $m( 'company_name' ) ),
		'license'    => $m( 'license_number' ),
		'phone'      => $phone,
		'phone_intl' => $intl,
		'wa'         => $digits,
		'female'     => $m( 'nl_gender' ) === 'f',
		'site_he'    => (int) $m( 'nl_site_he' ),
		'site_en'    => (int) $m( 'nl_site_en' ),
		'site_ru'    => (int) $m( 'nl_site_ru' ),
		'site_fr'    => (int) $m( 'nl_site_fr' ),
		'auto'       => $m( 'nl_auto_publish' ) !== '0',
		'on'         => $m( 'nl_drop_on' ) === '1',
		'token'      => trim( (string) get_post_meta( $p->ID, '_nl_drop_token', true ) ),
		'areas'      => $split( $m( 'areas_served' ) ),
		'areas_l'    => array( 'he' => $split( $m( 'areas_served' ) ), 'en' => $split( $m( 'nl_areas_en' ) ), 'ru' => $split( $m( 'nl_areas_ru' ) ), 'fr' => $split( $m( 'nl_areas_fr' ) ) ),
		'bio'        => array( 'he' => $m( 'bio' ), 'en' => $m( 'nl_bio_en' ) ),
		'portrait'   => $photos ? $photos[0] : '',
		'hero'       => (int) $m( 'nl_hero' ),
		'tier'       => $m( 'nl_tier' ) !== '' ? $m( 'nl_tier' ) : 'free',
		'slug'       => $m( 'nl_slug' ),
	);
	$b['langs'] = nl_drop_broker_langs( $b, $m( 'nl_langs' ) );
	return $b;
}

/** The languages this broker's listings are written in: the saved choice, or Hebrew plus English when an English site exists. */
function nl_drop_broker_langs( $b, $csv ) {
	$want = array_values( array_intersect( nl_drop_langs(), array_map( 'trim', explode( ',', strtolower( (string) $csv ) ) ) ) );
	if ( ! $want ) {
		$want = array( 'he' );
		if ( ! empty( $b['site_en'] ) ) { $want[] = 'en'; }
	}
	if ( ! in_array( 'he', $want, true ) ) { array_unshift( $want, 'he' ); }
	return $want;
}

function nl_drop_name( $b, $lang ) {
	$lang = nl_drop_L( $lang );
	if ( $lang === 'he' ) { return (string) $b['name_he']; }
	if ( $lang === 'ru' ) { return (string) ( $b['name_ru'] ?? $b['name_en'] ); }
	return (string) $b['name_en'];
}

function nl_drop_brand( $b, $lang ) {
	return nl_drop_L( $lang ) === 'he' ? (string) $b['brand_he'] : (string) $b['brand_en'];
}

/** Hebrew joins a list with a vav on the last item; the other languages with their own word. */
function nl_drop_join( $items, $lang ) {
	$items = array_values( array_filter( array_map( 'trim', (array) $items ) ) );
	$n     = count( $items );
	if ( $n === 0 ) { return ''; }
	if ( $n === 1 ) { return $items[0]; }
	$last = array_pop( $items );
	$lang = nl_drop_L( $lang );
	if ( $lang === 'he' ) {
		$v = preg_match( '/^\p{Hebrew}/u', $last ) ? 'ו' : 'ו-';
		return implode( ', ', $items ) . ' ' . $v . $last;
	}
	$and = array( 'en' => 'and', 'ru' => 'и', 'fr' => 'et' );
	return implode( ', ', $items ) . ' ' . $and[ $lang ] . ' ' . $last;
}

/** Hebrew "in X": the letter bet joins a Hebrew word directly, anything else with a hyphen. */
function nl_drop_he_in( $s ) {
	$s = trim( (string) $s );
	return $s === '' ? '' : ( preg_match( '/^\p{Hebrew}/u', $s ) ? 'ב' . $s : 'ב-' . $s );
}

function nl_drop_broker_by_token( $token ) {
	$token = (string) $token;
	if ( ! preg_match( '/^[a-z0-9]{24}$/', $token ) ) { return null; }
	$ids = get_posts( array(
		'post_type'        => 'nadlan_professional',
		'post_status'      => 'publish',
		'numberposts'      => 1,
		'fields'           => 'ids',
		'no_found_rows'    => true,
		'suppress_filters' => true,
		'meta_query'       => array( array( 'key' => '_nl_drop_token', 'value' => $token ) ),
	) );
	if ( ! $ids ) { return null; }
	$b = nl_drop_broker( $ids[0] );
	if ( ! $b || ! $b['on'] || $b['token'] === '' || ! hash_equals( $b['token'], $token ) ) { return null; }
	return $b;
}

function nl_drop_new_token() {
	return substr( bin2hex( random_bytes( 16 ) ), 0, 24 );
}

function nl_drop_author() {
	$a = (int) get_option( 'nl_drop_author', 0 );
	if ( $a && get_userdata( $a ) ) { return $a; }
	$admins = get_users( array( 'role' => 'administrator', 'number' => 1, 'fields' => 'ID', 'orderby' => 'ID', 'order' => 'ASC' ) );
	return $admins ? (int) $admins[0] : 1;
}

function nl_drop_rate( $bid, $bucket, $limit, $window ) {
	$k = 'nldrop_' . $bucket . '_' . (int) $bid;
	$n = (int) get_transient( $k );
	if ( $n >= $limit ) { return true; }
	set_transient( $k, $n + 1, $window );
	return false;
}

function nl_drop_site_url( $b, $lang ) {
	$id = (int) ( $b[ 'site_' . nl_drop_L( $lang ) ] ?? 0 );
	if ( ! $id || get_post_status( $id ) !== 'publish' ) { return ''; }
	return (string) get_permalink( $id );
}

/* =====================================================================================================
 * Words, numbers, icons
 * ===================================================================================================== */
function nl_drop_t( $lang, $k ) {
	static $T = array(
		'he' => array(
			'sale' => 'למכירה', 'rent' => 'להשכרה', 'exclusive' => 'בלעדיות', 'sqm' => 'מ״ר', 'of' => 'מתוך', 'yes' => 'יש',
			'f_rooms' => 'חדרים', 'f_size' => 'שטח', 'f_balcony' => 'מרפסת', 'f_garden' => 'גינה', 'f_floor' => 'קומה', 'f_parking' => 'חניה',
			'f_storage' => 'מחסן', 'f_safe' => 'ממ״ד', 'f_lift' => 'מעלית', 'f_condition' => 'מצב', 'f_entry' => 'כניסה', 'f_furnished' => 'ריהוט',
			'c_new' => 'חדש', 'c_renovated' => 'משופץ', 'c_good' => 'שמור', 'c_needs_renovation' => 'דורש שיפוץ', 'furnished' => 'מרוהט',
			'price_sale' => 'מחיר', 'price_rent' => 'שכר דירה לחודש', 'ask_sale' => 'המחיר נמסר בפנייה ישירה', 'ask_rent' => 'שכר הדירה נמסר בפנייה ישירה',
			'psqm_sale' => 'למ״ר', 'psqm_rent' => 'למ״ר לחודש', 'year' => 'בשנה',
			'cta' => 'תיאום סיור פרטי', 'call' => 'חיוג', 'wa' => 'וואטסאפ', 'home' => 'הבית', 'photos' => 'תמונות', 'photos_h2' => 'הנכס בתמונות',
			'broker_f' => 'המתווכת', 'broker_m' => 'המתווך', 'broker_ex_f' => 'המתווכת', 'broker_ex_m' => 'המתווך',
			'lic_f' => 'מתווכת במקרקעין, רישיון', 'lic_m' => 'מתווך במקרקעין, רישיון', 'site' => 'האתר של %s', 'switch' => 'English',
			'toc' => 'תוכן העמוד', 'rail' => 'מחיר ויצירת קשר', 'sold' => 'הנכס נמכר', 'rented' => 'הנכס הושכר', 'more' => 'לנכסים נוספים של %s',
			'card_view' => 'לעמוד הנכס', 'updated' => 'עודכן', 'month' => 'לחודש', 'ask_short' => 'המחיר נמסר בפנייה', 'ask_short_rent' => 'שכר הדירה נמסר בפנייה',
			'ask_sub' => 'פרטים בפנייה ישירה', 'rooms_n' => '%s חדרים', 'size_n' => '%s מ״ר', 'balcony_n' => 'מרפסת %s מ״ר', 'garden_n' => 'גינה %s מ״ר',
			'floor_of' => 'קומה %1$s מתוך %2$s', 'floor_n' => 'קומה %s', 'parking_n' => '%s חניות', 'parking_1' => 'חניה', 'entry_n' => 'כניסה: %s',
			'wa_text' => 'שלום %1$s, אשמח לפרטים ולתיאום סיור: %2$s (nad-lan.co.il)',
			'ground' => 'קרקע', 'broker_tab_f' => 'המתווכת', 'broker_tab_m' => 'המתווך', 'owner' => 'בעלי הנכס', 'owner_chip' => 'מבעלי הנכס',
			'owner_note' => 'מודעה של בעלי הנכס, ללא תיווך.',
			'nav_listings' => 'הנכסים', 'nav_sale' => 'למכירה', 'nav_rent' => 'להשכרה', 'nav_about' => 'עליי', 'nav_contact' => 'יצירת קשר', 'nav_aria' => 'ניווט באתר של %s',
			'site_eyebrow' => 'תיווך נדל״ן', 'lede_areas' => 'נכסים למכירה ולהשכרה %s.', 'lede_plain' => 'נכסים למכירה ולהשכרה.',
			'stat_listings' => 'נכסים', 'stat_areas' => 'אזורים', 'listings_h2' => 'הנכסים', 'listings_lead' => 'לכל נכס עמוד מלא עם התמונות, הפרטים והמחיר.',
			'filter_all' => 'הכול', 'filter_aria' => 'סינון לפי סוג עסקה', 'empty' => 'כרגע אין נכסים פעילים באתר. לפרטים על נכסים נוספים אפשר לפנות ישירות.',
			'contact_h2' => 'לתיאום סיור', 'legal' => 'האתר של %s ב-nad-lan.co.il. המידע אינו הצעה מחייבת, שמאות או ייעוץ.',
			'wa_site' => 'שלום %s, הגעתי מהאתר שלך ב-nad-lan ואשמח לדבר', 'about_h2' => 'קצת עליי',
			'seo_site_t' => '%1$s | נכסים למכירה ולהשכרה %2$s', 'seo_site_t0' => '%s | נכסים למכירה ולהשכרה',
			'seo_site_d' => '%1$s. נכסים למכירה ולהשכרה %2$s, עמוד מלא לכל נכס ופנייה ישירה בוואטסאפ.', 'seo_site_d0' => '%s. נכסים למכירה ולהשכרה, עמוד מלא לכל נכס ופנייה ישירה בוואטסאפ.',
		),
		'en' => array(
			'sale' => 'For sale', 'rent' => 'For rent', 'exclusive' => 'Exclusive', 'sqm' => 'sqm', 'of' => 'of', 'yes' => 'Yes',
			'f_rooms' => 'Rooms', 'f_size' => 'Area', 'f_balcony' => 'Balcony', 'f_garden' => 'Garden', 'f_floor' => 'Floor', 'f_parking' => 'Parking',
			'f_storage' => 'Storage', 'f_safe' => 'Safe room', 'f_lift' => 'Lift', 'f_condition' => 'Condition', 'f_entry' => 'Entry', 'f_furnished' => 'Furniture',
			'c_new' => 'New', 'c_renovated' => 'Renovated', 'c_good' => 'Well kept', 'c_needs_renovation' => 'Needs renovation', 'furnished' => 'Furnished',
			'price_sale' => 'Asking price', 'price_rent' => 'Monthly rent', 'ask_sale' => 'Price on request', 'ask_rent' => 'Rent on request',
			'psqm_sale' => 'Per sqm', 'psqm_rent' => 'Per sqm a month', 'year' => 'A year',
			'cta' => 'Book a private viewing', 'call' => 'Call', 'wa' => 'WhatsApp', 'home' => 'The residence', 'photos' => 'Photographs', 'photos_h2' => 'The home in pictures',
			'broker_f' => 'The broker', 'broker_m' => 'The broker', 'broker_ex_f' => 'The broker', 'broker_ex_m' => 'The broker',
			'lic_f' => 'licensed real estate broker, licence', 'lic_m' => 'licensed real estate broker, licence', 'site' => '%s’s site', 'switch' => 'עברית',
			'toc' => 'On this page', 'rail' => 'Price and contact', 'sold' => 'This home has been sold', 'rented' => 'This home has been let', 'more' => 'More homes from %s',
			'card_view' => 'Listing page', 'updated' => 'Updated', 'month' => 'a month', 'ask_short' => 'Price on request', 'ask_short_rent' => 'Rent on request',
			'ask_sub' => 'Details given on direct enquiry', 'rooms_n' => '%s rooms', 'size_n' => '%s sqm', 'balcony_n' => '%s sqm balcony', 'garden_n' => '%s sqm garden',
			'floor_of' => 'Floor %1$s of %2$s', 'floor_n' => 'Floor %s', 'parking_n' => '%s parking', 'parking_1' => 'Parking', 'entry_n' => 'Entry: %s',
			'wa_text' => 'Hello %1$s, I would like details and a viewing: %2$s (nad-lan.co.il)',
			'ground' => 'Ground', 'broker_tab_f' => 'Broker', 'broker_tab_m' => 'Broker', 'owner' => 'The owners', 'owner_chip' => 'Private owner',
			'owner_note' => 'Listed by the owners, without a broker.',
			'nav_listings' => 'Listings', 'nav_sale' => 'For sale', 'nav_rent' => 'For rent', 'nav_about' => 'About', 'nav_contact' => 'Contact', 'nav_aria' => '%s: site navigation',
			'site_eyebrow' => 'Real estate', 'lede_areas' => 'Homes for sale and for rent in %s.', 'lede_plain' => 'Homes for sale and for rent.',
			'stat_listings' => 'Listings', 'stat_areas' => 'Areas', 'listings_h2' => 'Listings', 'listings_lead' => 'Every home has a full page with photographs, details and the price.',
			'filter_all' => 'All', 'filter_aria' => 'Filter by deal', 'empty' => 'No homes are listed right now. For other homes, get in touch directly.',
			'contact_h2' => 'Book a viewing', 'legal' => '%s’s site on nad-lan.co.il. The information is not a binding offer, an appraisal or advice.',
			'wa_site' => 'Hello %s, I found your site on nad-lan and would like to talk', 'about_h2' => 'About',
			'seo_site_t' => '%1$s | Homes for Sale and Rent in %2$s', 'seo_site_t0' => '%s | Homes for Sale and Rent',
			'seo_site_d' => '%1$s. Homes for sale and for rent in %2$s, a full page for every home and direct WhatsApp contact.', 'seo_site_d0' => '%s. Homes for sale and for rent, a full page for every home and direct WhatsApp contact.',
		),
		'ru' => array(
			'sale' => 'Продажа', 'rent' => 'Аренда', 'exclusive' => 'Эксклюзив', 'sqm' => 'м²', 'of' => 'из', 'yes' => 'Есть',
			'f_rooms' => 'Комнаты', 'f_size' => 'Площадь', 'f_balcony' => 'Балкон', 'f_garden' => 'Сад', 'f_floor' => 'Этаж', 'f_parking' => 'Парковка',
			'f_storage' => 'Кладовая', 'f_safe' => 'Мамад', 'f_lift' => 'Лифт', 'f_condition' => 'Состояние', 'f_entry' => 'Въезд', 'f_furnished' => 'Мебель',
			'c_new' => 'Новая', 'c_renovated' => 'После ремонта', 'c_good' => 'Ухоженная', 'c_needs_renovation' => 'Требует ремонта', 'furnished' => 'С мебелью',
			'price_sale' => 'Цена', 'price_rent' => 'Аренда в месяц', 'ask_sale' => 'Цена по запросу', 'ask_rent' => 'Стоимость аренды по запросу',
			'psqm_sale' => 'За м²', 'psqm_rent' => 'За м² в месяц', 'year' => 'В год',
			'cta' => 'Записаться на просмотр', 'call' => 'Позвонить', 'wa' => 'WhatsApp', 'home' => 'Объект', 'photos' => 'Фотографии', 'photos_h2' => 'Объект в фотографиях',
			'broker_f' => 'Риелтор', 'broker_m' => 'Риелтор', 'broker_ex_f' => 'Риелтор', 'broker_ex_m' => 'Риелтор',
			'lic_f' => 'лицензированный риелтор, лицензия №', 'lic_m' => 'лицензированный риелтор, лицензия №', 'site' => 'Сайт: %s', 'switch' => 'עברית',
			'toc' => 'Содержание', 'rail' => 'Цена и контакты', 'sold' => 'Объект продан', 'rented' => 'Объект сдан', 'more' => 'Другие объекты: %s',
			'card_view' => 'Страница объекта', 'updated' => 'Обновлено', 'month' => 'в месяц', 'ask_short' => 'Цена по запросу', 'ask_short_rent' => 'Аренда по запросу',
			'ask_sub' => 'Подробности по прямому запросу', 'rooms_n' => '%s комнаты', 'size_n' => '%s м²', 'balcony_n' => 'балкон %s м²', 'garden_n' => 'сад %s м²',
			'floor_of' => 'этаж %1$s из %2$s', 'floor_n' => 'этаж %s', 'parking_n' => '%s парковки', 'parking_1' => 'Парковка', 'entry_n' => 'Въезд: %s',
			'wa_text' => 'Здравствуйте, %1$s. Хочу узнать подробности и записаться на просмотр: %2$s (nad-lan.co.il)',
			'ground' => 'Партер', 'broker_tab_f' => 'Риелтор', 'broker_tab_m' => 'Риелтор', 'owner' => 'Владельцы', 'owner_chip' => 'От владельцев',
			'owner_note' => 'Объявление владельцев, без посредника.',
			'nav_listings' => 'Объекты', 'nav_sale' => 'Продажа', 'nav_rent' => 'Аренда', 'nav_about' => 'Обо мне', 'nav_contact' => 'Контакты', 'nav_aria' => 'Навигация по сайту: %s',
			'site_eyebrow' => 'Недвижимость', 'lede_areas' => 'Объекты на продажу и в аренду: %s.', 'lede_plain' => 'Объекты на продажу и в аренду.',
			'stat_listings' => 'Объекты', 'stat_areas' => 'Районы', 'listings_h2' => 'Объекты', 'listings_lead' => 'У каждого объекта своя страница с фотографиями, деталями и ценой.',
			'filter_all' => 'Все', 'filter_aria' => 'Фильтр по типу сделки', 'empty' => 'Сейчас на сайте нет активных объектов. О других объектах можно спросить напрямую.',
			'contact_h2' => 'Записаться на просмотр', 'legal' => 'Сайт %s на nad-lan.co.il. Информация не является офертой, оценкой или консультацией.',
			'wa_site' => 'Здравствуйте, %s. Пишу с вашего сайта на nad-lan', 'about_h2' => 'Обо мне',
			'seo_site_t' => '%1$s | Продажа и аренда недвижимости: %2$s', 'seo_site_t0' => '%s | Продажа и аренда недвижимости',
			'seo_site_d' => '%1$s. Объекты на продажу и в аренду: %2$s. У каждого объекта своя страница, связь напрямую в WhatsApp.', 'seo_site_d0' => '%s. Объекты на продажу и в аренду, у каждого своя страница, связь напрямую в WhatsApp.',
		),
		'fr' => array(
			'sale' => 'À vendre', 'rent' => 'À louer', 'exclusive' => 'Exclusivité', 'sqm' => 'm²', 'of' => 'sur', 'yes' => 'Oui',
			'f_rooms' => 'Pièces', 'f_size' => 'Surface', 'f_balcony' => 'Balcon', 'f_garden' => 'Jardin', 'f_floor' => 'Étage', 'f_parking' => 'Parking',
			'f_storage' => 'Cave', 'f_safe' => 'Mamad', 'f_lift' => 'Ascenseur', 'f_condition' => 'État', 'f_entry' => 'Entrée', 'f_furnished' => 'Mobilier',
			'c_new' => 'Neuf', 'c_renovated' => 'Rénové', 'c_good' => 'Bien entretenu', 'c_needs_renovation' => 'À rénover', 'furnished' => 'Meublé',
			'price_sale' => 'Prix', 'price_rent' => 'Loyer mensuel', 'ask_sale' => 'Prix sur demande', 'ask_rent' => 'Loyer sur demande',
			'psqm_sale' => 'Au m²', 'psqm_rent' => 'Au m² par mois', 'year' => 'Par an',
			'cta' => 'Organiser une visite privée', 'call' => 'Appeler', 'wa' => 'WhatsApp', 'home' => 'Le bien', 'photos' => 'Photos', 'photos_h2' => 'Le bien en images',
			'broker_f' => 'L’agente immobilière', 'broker_m' => 'L’agent immobilier', 'broker_ex_f' => 'L’agente immobilière', 'broker_ex_m' => 'L’agent immobilier',
			'lic_f' => 'agente immobilière agréée, licence n°', 'lic_m' => 'agent immobilier agréé, licence n°', 'site' => 'Le site %s', 'switch' => 'עברית',
			'toc' => 'Sur cette page', 'rail' => 'Prix et contact', 'sold' => 'Ce bien a été vendu', 'rented' => 'Ce bien a été loué', 'more' => 'Autres biens %s',
			'card_view' => 'Voir le bien', 'updated' => 'Mis à jour le', 'month' => 'par mois', 'ask_short' => 'Prix sur demande', 'ask_short_rent' => 'Loyer sur demande',
			'ask_sub' => 'Détails sur demande directe', 'rooms_n' => '%s pièces', 'size_n' => '%s m²', 'balcony_n' => 'balcon de %s m²', 'garden_n' => 'jardin de %s m²',
			'floor_of' => '%1$s étage sur %2$s', 'floor_n' => '%s étage', 'parking_n' => '%s places de parking', 'parking_1' => 'Parking', 'entry_n' => 'Entrée : %s',
			'wa_text' => 'Bonjour %1$s, je souhaite des détails et une visite : %2$s (nad-lan.co.il)',
			'ground' => 'Rez-de-chaussée', 'broker_tab_f' => 'L’agente', 'broker_tab_m' => 'L’agent', 'owner' => 'Les propriétaires', 'owner_chip' => 'De particulier',
			'owner_note' => 'Annonce des propriétaires, sans agence.',
			'nav_listings' => 'Les biens', 'nav_sale' => 'À vendre', 'nav_rent' => 'À louer', 'nav_about' => 'À propos', 'nav_contact' => 'Contact', 'nav_aria' => 'Navigation du site %s',
			'site_eyebrow' => 'Immobilier', 'lede_areas' => 'Biens à vendre et à louer : %s.', 'lede_plain' => 'Biens à vendre et à louer.',
			'stat_listings' => 'Biens', 'stat_areas' => 'Quartiers', 'listings_h2' => 'Les biens', 'listings_lead' => 'Chaque bien a sa page complète, avec les photos, les détails et le prix.',
			'filter_all' => 'Tous', 'filter_aria' => 'Filtrer par type de transaction', 'empty' => 'Aucun bien en ligne pour le moment. Pour d’autres biens, un contact direct suffit.',
			'contact_h2' => 'Organiser une visite', 'legal' => 'Le site %s sur nad-lan.co.il. Ces informations ne constituent ni une offre ferme, ni une expertise, ni un conseil.',
			'wa_site' => 'Bonjour %s, je vous écris depuis votre site sur nad-lan', 'about_h2' => 'À propos',
			'seo_site_t' => '%1$s | Biens à vendre et à louer : %2$s', 'seo_site_t0' => '%s | Biens à vendre et à louer',
			'seo_site_d' => '%1$s. Biens à vendre et à louer : %2$s. Une page complète pour chaque bien, contact direct sur WhatsApp.', 'seo_site_d0' => '%s. Biens à vendre et à louer, une page complète pour chaque bien, contact direct sur WhatsApp.',
		),
	);
	$lang = nl_drop_L( $lang );
	if ( isset( $T[ $lang ][ $k ] ) ) { return $T[ $lang ][ $k ]; }
	return isset( $T['en'][ $k ] ) ? $T['en'][ $k ] : $k;
}

/** A string with the broker's name in it; French says "de Meital" but "d’Israel". */
function nl_drop_tn( $lang, $k, $name ) {
	$lang = nl_drop_L( $lang );
	if ( $lang === 'fr' ) { $name = ( preg_match( '/^[aeiouyhàâéèêëîïôûùAEIOUYHÀÂÉÈÊËÎÏÔÛÙ]/u', (string) $name ) ? 'd’' : 'de ' ) . $name; }
	return sprintf( nl_drop_t( $lang, $k ), $name );
}

/** Cut on a whole word, never inside one. */
function nl_drop_cut_words( $s, $max ) {
	$s = trim( (string) $s );
	if ( ( function_exists( 'mb_strlen' ) ? mb_strlen( $s ) : strlen( $s ) ) <= $max ) { return $s; }
	$c = function_exists( 'mb_substr' ) ? mb_substr( $s, 0, $max ) : substr( $s, 0, $max );
	// a whole sentence first, then a whole clause, then a whole word
	foreach ( array( '. ' => '.', ', ' => '.' ) as $sep => $end ) {
		$p = function_exists( 'mb_strrpos' ) ? mb_strrpos( $c, $sep ) : strrpos( $c, $sep );
		if ( $p !== false && $p > $max * 0.55 ) { return ( function_exists( 'mb_substr' ) ? mb_substr( $c, 0, $p ) : substr( $c, 0, $p ) ) . $end; }
	}
	$p = function_exists( 'mb_strrpos' ) ? mb_strrpos( $c, ' ' ) : strrpos( $c, ' ' );
	return rtrim( $p ? ( function_exists( 'mb_substr' ) ? mb_substr( $c, 0, $p ) : substr( $c, 0, $p ) ) : $c, ' ,;:·' );
}

/** Each language named in itself, for the language links. */
function nl_drop_lang_name( $lang ) {
	static $n = array( 'he' => 'עברית', 'en' => 'English', 'ru' => 'Русский', 'fr' => 'Français' );
	return $n[ nl_drop_L( $lang ) ];
}

/** "4 rooms" in each language: Russian and French agree the noun with the number. */
function nl_drop_rooms_word( $n, $lang ) {
	$lang = nl_drop_L( $lang );
	$n    = (float) $n;
	if ( $lang === 'ru' ) {
		if ( floor( $n ) != $n ) { return 'комнаты'; }
		$i = (int) $n;
		if ( $i % 10 === 1 && $i % 100 !== 11 ) { return 'комната'; }
		if ( $i % 10 >= 2 && $i % 10 <= 4 && ( $i % 100 < 12 || $i % 100 > 14 ) ) { return 'комнаты'; }
		return 'комнат';
	}
	if ( $lang === 'fr' ) { return $n < 2 ? 'pièce' : 'pièces'; }
	if ( $lang === 'en' ) { return 'rooms'; }
	return 'חדרים';
}

function nl_drop_parking_word( $n, $lang ) {
	$lang = nl_drop_L( $lang );
	$i    = (int) $n;
	if ( $lang === 'ru' ) {
		if ( $i % 10 === 1 && $i % 100 !== 11 ) { return 'парковочное место'; }
		if ( $i % 10 >= 2 && $i % 10 <= 4 && ( $i % 100 < 12 || $i % 100 > 14 ) ) { return 'парковочных места'; }
		return 'парковочных мест';
	}
	if ( $lang === 'fr' ) { return $i < 2 ? 'place de parking' : 'places de parking'; }
	if ( $lang === 'en' ) { return $i < 2 ? 'parking space' : 'parking spaces'; }
	return 'חניות';
}

/** French ordinal floors: 1er, 2e. */
function nl_drop_fr_floor( $n ) {
	$n = (int) $n;
	return $n === 1 ? '1er' : $n . 'e';
}

function nl_drop_type_label( $t, $lang ) {
	static $L = array(
		'he' => array( 'apartment' => 'דירה', 'penthouse' => 'פנטהאוז', 'mini_penthouse' => 'מיני פנטהאוז', 'garden' => 'דירת גן', 'duplex' => 'דופלקס', 'villa' => 'וילה', 'cottage' => 'קוטג׳', 'studio' => 'סטודיו', 'other' => 'נכס' ),
		'en' => array( 'apartment' => 'Apartment', 'penthouse' => 'Penthouse', 'mini_penthouse' => 'Mini penthouse', 'garden' => 'Garden apartment', 'duplex' => 'Duplex', 'villa' => 'Villa', 'cottage' => 'Cottage', 'studio' => 'Studio', 'other' => 'Property' ),
		'ru' => array( 'apartment' => 'Квартира', 'penthouse' => 'Пентхаус', 'mini_penthouse' => 'Мини-пентхаус', 'garden' => 'Квартира с садом', 'duplex' => 'Дуплекс', 'villa' => 'Вилла', 'cottage' => 'Коттедж', 'studio' => 'Студия', 'other' => 'Объект' ),
		'fr' => array( 'apartment' => 'Appartement', 'penthouse' => 'Penthouse', 'mini_penthouse' => 'Mini-penthouse', 'garden' => 'Appartement avec jardin', 'duplex' => 'Duplex', 'villa' => 'Villa', 'cottage' => 'Maison', 'studio' => 'Studio', 'other' => 'Bien' ),
	);
	$t = isset( $L['en'][ (string) $t ] ) ? (string) $t : 'other';
	return $L[ nl_drop_L( $lang ) ][ $t ];
}

/** Russian and French group thousands with a no-break space and write decimals with a comma. */
function nl_drop_fmt_int( $n, $lang = 'he' ) {
	if ( $lang === 'ru' || $lang === 'fr' ) { return number_format( (float) $n, 0, ',', "\u{00A0}" ); }
	return number_format( (float) $n, 0, '.', ',' );
}

function nl_drop_fmt_num( $n, $lang = 'he' ) {
	$n   = (float) $n;
	$lat = ( $lang === 'ru' || $lang === 'fr' );
	$dec = $lat ? ',' : '.';
	$th  = $lat ? "\u{00A0}" : ',';
	if ( floor( $n ) == $n ) { return number_format( $n, 0, $dec, $th ); }
	return rtrim( rtrim( number_format( $n, 2, $dec, $th ), '0' ), $dec );
}

function nl_drop_money_html( $n, $lang ) {
	$num = '<span class="nlx-num">' . esc_html( nl_drop_fmt_int( $n, $lang ) ) . '</span>';
	if ( $lang === 'en' ) { return '<span class="nlx-money">NIS&nbsp;' . $num . '</span>'; }
	return '<span class="nlx-money">' . $num . '&nbsp;₪</span>';
}

function nl_drop_price_text( $n, $lang ) {
	if ( $lang === 'en' ) { return 'NIS ' . nl_drop_fmt_int( $n ); }
	if ( $lang === 'ru' || $lang === 'fr' ) { return nl_drop_fmt_int( $n, $lang ) . "\u{00A0}₪"; }
	return nl_drop_fmt_int( $n ) . ' ש״ח';
}

/** Every number a broker wrote, including "4.2 מיליון" as 4200000 and "15 אלף" as 15000. */
function nl_drop_nums_in_text( $text ) {
	$out = array();
	if ( preg_match_all( '/(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(\s*(?:מיליון|מליון|million|mil\b|M\b|אלף|thousand|K\b|k\b))?/u', (string) $text, $mm, PREG_SET_ORDER ) ) {
		foreach ( $mm as $x ) {
			$n     = (float) str_replace( ',', '', $x[1] );
			$out[] = $n;
			$mul   = isset( $x[2] ) ? trim( $x[2] ) : '';
			if ( $mul !== '' ) {
				$out[] = preg_match( '/^(מיליון|מליון|million|mil|M)$/u', $mul ) ? $n * 1000000 : $n * 1000;
			}
		}
	}
	return $out;
}

/** The day, month and year of a written date (1.10, 15/11/2026): each is a number the broker wrote. */
function nl_drop_date_parts( $s ) {
	$out = array();
	if ( preg_match_all( '/(?<![\d.])(\d{1,2})[.\/](\d{1,2})(?:[.\/](\d{2,4}))?(?![\d])/u', (string) $s, $m, PREG_SET_ORDER ) ) {
		foreach ( $m as $x ) {
			if ( (int) $x[1] >= 1 && (int) $x[1] <= 31 && (int) $x[2] >= 1 && (int) $x[2] <= 12 ) {
				$out[] = (float) $x[1];
				$out[] = (float) $x[2];
				if ( ! empty( $x[3] ) ) { $out[] = (float) $x[3]; }
			}
		}
	}
	return $out;
}

function nl_drop_nums_in_copy( $s, $lang = 'he' ) {
	$out = array();
	$s   = str_replace( '{{PRICE}}', ' ', (string) $s );
	if ( $lang === 'ru' || $lang === 'fr' ) {
		$s = preg_replace( '/(?<=\d)[\x{00A0}\x{202F}\x{2009} ](?=\d{3}(?!\d))/u', '', $s );
		$s = preg_replace( '/(?<=\d),(?=\d{1,2}(?!\d))/u', '.', $s );
	}
	if ( preg_match_all( '/\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?/u', $s, $m ) ) {
		foreach ( $m[0] as $x ) { $out[] = (float) str_replace( ',', '', $x ); }
	}
	return $out;
}


function nl_drop_num_ok( $n, $allowed ) {
	foreach ( (array) $allowed as $a ) {
		if ( abs( (float) $n - (float) $a ) <= max( 0.011, abs( (float) $a ) * 0.005 ) ) { return true; }
	}
	return false;
}

function nl_drop_norm( $s ) {
	$s = (string) $s;
	$s = str_replace( array( '״', '"', '׳', "'", '’', '`' ), array( '"', '"', "'", "'", "'", "'" ), $s );
	$s = preg_replace( '/\s+/u', ' ', $s );
	return function_exists( 'mb_strtolower' ) ? mb_strtolower( trim( $s ) ) : strtolower( trim( $s ) );
}

function nl_drop_icon( $k ) {
	static $p = array(
		'rooms'   => '<path d="M3.5 20V9.5L12 4l8.5 5.5V20M9.5 20v-5.5h5V20"/>',
		'area'    => '<rect x="4" y="4" width="16" height="16" rx="1.5"/><path d="M4 9h3M4 14h3M9 4v3M14 4v3"/>',
		'balcony' => '<path d="M7 11V5h10v6M4 11h16M6 11v8M10 11v8M14 11v8M18 11v8M4 19h16"/>',
		'floor'   => '<path d="M4 20h4v-4h4v-4h4V8h4"/>',
		'parking' => '<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M10 16.5v-9h3.2a2.7 2.7 0 010 5.4H10"/>',
		'storage' => '<path d="M4 8.2L12 4l8 4.2v7.6L12 20l-8-4.2z"/><path d="M4 8.2l8 4.2 8-4.2M12 12.4V20"/>',
		'shield'  => '<path d="M12 3.5l7 2.8v5.1c0 4.6-2.9 7.6-7 9.1-4.1-1.5-7-4.5-7-9.1V6.3z"/>',
		'lift'    => '<rect x="5.5" y="3.5" width="13" height="17" rx="1.5"/><path d="M9.5 9.5l2.5-2.5 2.5 2.5M9.5 14.5l2.5 2.5 2.5-2.5"/>',
		'key'     => '<circle cx="8" cy="12" r="3.6"/><path d="M11.6 12H20.5M17.5 12v3M20.5 12v2.4"/>',
		'sea'     => '<path d="M3 11c2.4 0 2.6-2 5-2s2.6 2 5 2 2.6-2 5-2 2.4 2 3 2M3 16c2.4 0 2.6-2 5-2s2.6 2 5 2 2.6-2 5-2 2.4 2 3 2"/>',
		'arrow'   => '<path d="M5 12h14M13 6l6 6-6 6"/>',
		'phone'   => '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2"/>',
		'wa'      => '<path fill="currentColor" stroke="none" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/>',
	);
	if ( ! isset( $p[ $k ] ) ) { return ''; }
	return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' . $p[ $k ] . '</svg>';
}

/* =====================================================================================================
 * The language gate (the same families the Meital runner refuses) and the no-invention check
 * ===================================================================================================== */
function nl_drop_banned( $lang ) {
	if ( $lang === 'en' ) {
		return array( 'madlan', 'yad2', 'instagram', 'not verified', 'unverified', 'according to the broker', 'per the listing', 'not published', 'not confirmed', 'the marketer',
			'once in a lifetime', 'dream', 'stunning', 'breathtaking', 'must see', "won't last", 'hurry', 'unique opportunity', 'luxury at its finest', '—', '–', '!' );
	}
	if ( $lang === 'ru' ) {
		return array( 'мадлан', 'яд2', 'яд 2', 'инстаграм', 'не проверено', 'не подтверждено', 'по словам риелтора', 'по словам маклера', 'не опубликовано',
			'уникальн*', 'мечт*', 'идеальн*', 'потрясающ*', 'шикарн*', 'невероятн*', 'сказочн*', 'не упустите', 'спешите', 'успейте', 'эксклюзивное предложение', '—', '–', '!' );
	}
	if ( $lang === 'fr' ) {
		return array( 'madlan', 'yad2', 'instagram', 'non vérifié', 'non confirmé', 'selon l’agent', 'selon l\'agent', 'non publié',
			'unique', 'uniques', 'rêve*', 'parfait*', 'exceptionnel*', 'magnifique*', 'sublime*', 'incroyable*', 'à ne pas manquer', 'coup de cœur', 'opportunité*', 'dépêchez', '—', '–', '!' );
	}
	return array( 'לפי המשווקת', 'המשווקת', 'לפי המתווכת', 'לפי המתווך', 'מדלן', 'יד2', 'יד 2', 'אינסטגרם', 'לא אומת', 'יש לאמת', 'לא פורסם', 'זמינות בבדיקה',
		'הזדמנות', 'חלום', 'מושלם', 'מדהים', 'פנטסטי', 'חוויה', 'לא תחזור', 'יוקרה במיטבה', 'בעידן', '—', '–', '!' );
}

/**
 * Hebrew and English match a banned string anywhere, as before. Russian and French match whole words, and a
 * trailing * matches every ending (уникальный, уникальная; parfait, parfaite), so "uniquement" never trips "unique".
 */
function nl_drop_banned_hits( $s, $lang ) {
	$hits = array();
	$low  = nl_drop_norm( $s );
	$word = ( $lang === 'ru' || $lang === 'fr' );
	$ws   = $word ? nl_drop_words( $s ) : array();
	foreach ( nl_drop_banned( $lang ) as $w ) {
		if ( $w === '' ) { continue; }
		$nw = nl_drop_norm( $w );
		if ( ! $word || strpos( $nw, ' ' ) !== false || ! preg_match( '/^[\p{L}\p{N}*-]+$/u', $nw ) ) {
			if ( strpos( $low, rtrim( $nw, '*' ) ) !== false ) { $hits[] = 'banned:' . $w; }
			continue;
		}
		$stem = substr( $nw, -1 ) === '*';
		$core = rtrim( $nw, '*' );
		foreach ( $ws as $x ) {
			if ( $stem ? strpos( $x, $core ) === 0 : $x === $core ) { $hits[] = 'banned:' . $w; break; }
		}
	}
	return $hits;
}

function nl_drop_gate_str( $s, $lang, $allowed, $stated = null, $names = array() ) {
	$issues = nl_drop_banned_hits( $s, $lang );
	foreach ( nl_drop_nums_in_copy( $s, $lang ) as $n ) {
		if ( ! nl_drop_num_ok( $n, $allowed ) ) { $issues[] = 'number:' . $n; }
	}
	if ( preg_match( '/https?:|www\./i', (string) $s ) ) { $issues[] = 'link'; }
	if ( is_array( $stated ) ) {
		$bare = (string) $s;
		foreach ( (array) $names as $nm ) {
			if ( $nm === '' || $nm === null ) { continue; }
			foreach ( array_unique( array( (string) $nm, nl_drop_he_typo( $nm ) ) ) as $v ) {
				$bare = (string) preg_replace( '/' . preg_quote( $v, '/' ) . '/iu', ' ', $bare );
			}
		}
		foreach ( nl_drop_claims_in( $bare ) as $g ) {
			if ( ! in_array( $g, $stated, true ) ) { $issues[] = 'claim:' . $g; }
		}
	}
	return $issues;
}

/** True when a copy field names the street the broker wrote (the address is never published). */
function nl_drop_has_street( $s, $f ) {
	foreach ( array( $f['street_he'] ?? '', $f['street_en'] ?? '' ) as $st ) {
		$st = trim( preg_replace( '/^(רחוב|רח׳|רח\'|שד׳|שדרות|st\.?|street|rehov|rechov|sderot|sd\.)\s+/iu', '', (string) $st ) );
		$st = trim( preg_replace( '/\s+\d+[a-zא-ת]?$/iu', '', $st ) );
		$st = trim( preg_replace( '/\s+(st\.?|street|blvd\.?|boulevard|ave\.?|avenue|rd\.?|road)$/iu', '', $st ) );
		if ( ( function_exists( 'mb_strlen' ) ? mb_strlen( $st ) : strlen( $st ) ) >= 3 && stripos( nl_drop_norm( $s ), nl_drop_norm( $st ) ) !== false ) { return true; }
	}
	return false;
}

/** Hebrew typography: מ"ר -> מ״ר, ג'קוזי -> ג׳קוזי. */
function nl_drop_he_typo( $s ) {
	$s = preg_replace( '/(?<=[\x{05D0}-\x{05EA}])"(?=[\x{05D0}-\x{05EA}])/u', '״', (string) $s );
	return preg_replace( "/(?<=[\\x{05D0}-\\x{05EA}])'/u", '׳', $s );
}

/** Descriptive claims a page may make only when the broker made them. A trailing * matches every ending. */
function nl_drop_claim_groups() {
	static $g = null;
	if ( $g !== null ) { return $g; }
	$g = array(
		'sea'      => array( 'ים', 'לים', 'הים', 'מהים', 'בים', 'וים', 'sea', 'seafront', 'beach', 'חוף', 'לחוף', 'החוף' ),
		'view'     => array( 'נוף', 'לנוף', 'הנוף', 'ונוף', 'נופים', 'view', 'views' ),
		'park'     => array( 'פארק', 'לפארק', 'הפארק', 'park' ),
		'quiet'    => array( 'שקט', 'שקטה', 'שקטים', 'בשקט', 'quiet', 'peaceful', 'calm' ),
		'bright'   => array( 'מואר', 'מוארת', 'מוארים', 'אור', 'bright', 'light-filled', 'sunlit' ),
		'new'      => array( 'חדש', 'חדשה', 'חדשים', 'חדשות', 'new', 'brand-new' ),
		'reno'     => array( 'משופץ', 'משופצת', 'שופץ', 'שופצה', 'renovated', 'refurbished' ),
		'boutique' => array( 'בוטיק', 'boutique' ),
		'design'   => array( 'מעצב', 'מעצבת', 'מעוצב', 'מעוצבת', 'designer', 'designed' ),
		'luxury'   => array( 'יוקרה', 'יוקרתי', 'יוקרתית', 'יוקרתיים', 'luxury', 'luxurious', 'prestigious' ),
		'spacious' => array( 'מרווח', 'מרווחת', 'מרווחים', 'spacious', 'generous', 'roomy' ),
		'garden'   => array( 'גינה', 'לגינה', 'הגינה', 'garden' ),
		'pool'     => array( 'בריכה', 'בריכת', 'pool' ),
		'gym'      => array( 'כושר', 'gym', 'fitness' ),
		'guard'    => array( 'שומר', 'שמירה', 'מאבטח', 'לובי', 'guard', 'security', 'concierge', 'lobby' ),
		'walk'     => array( 'הליכה', 'דקות', 'walk', 'minutes', 'minute' ),
		'school'   => array( 'בית ספר', 'בתי ספר', 'גן ילדים', 'school', 'schools', 'kindergarten' ),
		'transit'  => array( 'רכבת', 'הרכבת', 'אוטובוס', 'train', 'rail', 'metro', 'bus' ),
		'size'     => array( 'רחב', 'רחבה', 'רחבים', 'רחבות', 'ענק', 'ענקית', 'עצום', 'עצומה', 'גדול', 'גדולה', 'גדולים', 'expansive', 'wide', 'large', 'huge', 'vast', 'sweeping', 'ample' ),
		'quality'  => array( 'איכותי', 'איכותית', 'איכותיים', 'איכות', 'גימור', 'high-quality', 'quality', 'premium', 'high-end', 'fine' ),
		'advanced' => array( 'מתקדם', 'מתקדמת', 'מתקדמים', 'מתקדמות', 'חדשני', 'חדשנית', 'advanced', 'state-of-the-art', 'cutting-edge', 'modern' ),
		'living'   => array( 'סלון', 'מהסלון', 'לסלון', 'living', 'lounge' ),
		'control'  => array( 'שליטה', 'control', 'centralized' ),
		'family'   => array( 'משפחה', 'משפחות', 'family', 'families' ),
		'light'    => array( 'אור', 'שמש', 'sun', 'sunny', 'daylight' ),
	);
	$more = array(
		'sea'      => array( 'море', 'моря', 'морю', 'морем', 'морск*', 'пляж*', 'побережь*', 'mer', 'plage*', 'balnéaire*', 'littoral' ),
		'view'     => array( 'вид', 'вида', 'видом', 'виды', 'видами', 'панорам*', 'vue', 'vues', 'panoram*' ),
		'park'     => array( 'парк', 'парка', 'парку', 'парком', 'parc', 'parcs' ),
		'quiet'    => array( 'тих*', 'спокойн*', 'тишин*', 'calme*', 'tranquill*', 'paisible*' ),
		'bright'   => array( 'светл*', 'солнечн*', 'lumineu*', 'ensoleillé*' ),
		'new'      => array( 'новы*', 'нова*', 'ново*', 'neuf', 'neufs', 'neuve*', 'nouve*' ),
		'reno'     => array( 'отремонтирован*', 'ремонт*', 'rénov*', 'refait*' ),
		'boutique' => array( 'бутик*' ),
		'design'   => array( 'дизайн*', 'conçu*' ),
		'luxury'   => array( 'роскош*', 'люкс*', 'элитн*', 'престижн*', 'luxe', 'luxueu*', 'prestig*', 'haut de gamme' ),
		'spacious' => array( 'просторн*', 'spacieu*', 'vaste*', 'généreu*' ),
		'garden'   => array( 'сад', 'сада', 'саду', 'садом', 'jardin*' ),
		'pool'     => array( 'бассейн*', 'piscine*' ),
		'gym'      => array( 'тренаж*', 'фитнес*', 'salle de sport' ),
		'guard'    => array( 'охран*', 'консьерж*', 'лобби', 'gardien*', 'concierg*', 'vigile*' ),
		'walk'     => array( 'пешком', 'пешей', 'минут*', 'à pied' ),
		'school'   => array( 'школ*', 'детсад*', 'école*', 'crèche*', 'jardindenfants' ),
		'transit'  => array( 'поезд*', 'железнодорож*', 'метро', 'автобус*', 'трамва*', 'gare*', 'métro*', 'tram*' ),
		'size'     => array( 'больш*', 'огромн*', 'широк*', 'грандиозн*', 'grand', 'grande', 'grands', 'grandes', 'immense*', 'large*' ),
		'quality'  => array( 'качествен*', 'качеств*', 'отделк*', 'qualit*', 'finition*' ),
		'advanced' => array( 'современн*', 'передов*', 'продвинут*', 'инновацион*', 'moderne*', 'avancé*', 'innov*', 'dernier cri' ),
		'living'   => array( 'гостин*', 'салон*', 'salon*', 'séjour*' ),
		'control'  => array( 'управлен*', 'контрол*', 'централизован*', 'contrôl*', 'centralis*' ),
		'family'   => array( 'семья', 'семьи', 'семье', 'семью', 'семьёй', 'семьей', 'семей', 'семьям*', 'семейн*', 'famil*' ),
		'light'    => array( 'свет', 'света', 'светом', 'солнц*', 'lumière*', 'soleil*' ),
	);
	foreach ( $more as $k => $list ) { $g[ $k ] = array_merge( $g[ $k ], $list ); }
	return $g;
}


function nl_drop_words( $s ) {
	$s = nl_drop_norm( $s );
	$s = preg_replace( '/[^\p{L}\p{N}\s-]+/u', ' ', $s );
	return array_values( array_filter( preg_split( '/\s+/u', $s ) ) );
}

function nl_drop_claims_in( $s ) {
	// a kindergarten is a school claim, not a garden: детский сад, jardin d'enfants
	$s     = preg_replace( array( '/детск\p{L}*\s+сад\p{L}*/iu', "/jardins?\\s+d[’']\\s*enfants/iu" ), array( ' детсад ', ' jardindenfants ' ), (string) $s );
	$words = array();
	foreach ( nl_drop_words( $s ) as $w ) {
		$words[ $w ] = true;
		// Hebrew one- and two-letter prefixes: ושקטה, הים, לנוף, מהים
		if ( preg_match( '/^[\x{05D5}\x{05D4}\x{05D1}\x{05DC}\x{05DE}\x{05E9}\x{05DB}]{1,2}(?=\p{Hebrew}{2,})/u', $w ) ) {
			$words[ preg_replace( '/^[\x{05D5}\x{05D4}\x{05D1}\x{05DC}\x{05DE}\x{05E9}\x{05DB}]/u', '', $w ) ] = true;
			$words[ preg_replace( '/^[\x{05D5}\x{05D4}\x{05D1}\x{05DC}\x{05DE}\x{05E9}\x{05DB}]{2}/u', '', $w ) ] = true;
		}
	}
	$keys  = array_keys( $words );
	$low   = ' ' . implode( ' ', $keys ) . ' ';
	$found = array();
	foreach ( nl_drop_claim_groups() as $g => $list ) {
		foreach ( $list as $w ) {
			if ( strpos( $w, ' ' ) !== false ) {
				$hit = strpos( $low, ' ' . rtrim( $w, '*' ) . ' ' ) !== false;
			} elseif ( substr( $w, -1 ) === '*' ) {
				$core = substr( $w, 0, -1 );
				$hit  = false;
				foreach ( $keys as $k ) { if ( strpos( (string) $k, $core ) === 0 ) { $hit = true; break; } }
			} else {
				$hit = isset( $words[ $w ] );
			}
			if ( $hit ) { $found[ $g ] = true; break; }
		}
	}
	return array_keys( $found );
}

function nl_drop_allowed_numbers( $f, $text ) {
	$a = nl_drop_nums_in_text( $text );
	foreach ( array( 'rooms', 'size_sqm', 'balcony_sqm', 'garden_sqm', 'floor', 'total_floors', 'parking_count', 'price' ) as $k ) {
		if ( isset( $f[ $k ] ) && $f[ $k ] !== null && $f[ $k ] !== '' ) { $a[] = (float) $f[ $k ]; }
	}
	if ( ! empty( $f['price'] ) && ! empty( $f['size_sqm'] ) ) { $a[] = round( (float) $f['price'] / (float) $f['size_sqm'] ); }
	return array_merge( $a, nl_drop_date_parts( ( $f['entry_he'] ?? '' ) . ' ' . ( $f['entry_en'] ?? '' ) ) );
}

/* =====================================================================================================
 * The model call (JSON out). Uses the site's own keys; Claude when the site is set to Anthropic.
 * ===================================================================================================== */
function nl_drop_parse_json( $txt ) {
	$txt = trim( (string) $txt );
	$txt = preg_replace( '/^```(?:json)?\s*|\s*```$/m', '', $txt );
	$a   = strpos( $txt, '{' );
	$b   = strrpos( $txt, '}' );
	if ( $a === false || $b === false || $b < $a ) { return null; }
	$j = json_decode( substr( $txt, $a, $b - $a + 1 ), true );
	return is_array( $j ) ? $j : null;
}

function nl_drop_llm_json( $system, $user, $max_tokens, &$err = null ) {
	$user = function_exists( 'mb_substr' ) ? mb_substr( (string) $user, 0, 6000 ) : substr( (string) $user, 0, 6000 );
	if ( defined( 'NADLAN_DISABLE_AI' ) && NADLAN_DISABLE_AI ) { $err = 'disabled'; return null; }
	$cap  = (int) get_option( 'nadlan_ai_daily_token_cap_global', 200000 );
	$cap  = $cap < 10000 ? 200000 : $cap;
	$used = (int) get_option( 'nadlan_ai_tokens_today_' . gmdate( 'Ymd' ), 0 );
	if ( $used > $cap ) { $err = 'budget'; return null; }
	$prov = (string) get_option( 'nl_drop_provider', function_exists( 'nadlan_ai_provider' ) ? nadlan_ai_provider() : 'openai' );
	$akey = function_exists( 'nadlan_ai_anthropic_key' ) ? (string) nadlan_ai_anthropic_key() : '';
	$okey = function_exists( 'nadlan_ai_openai_key' ) ? (string) nadlan_ai_openai_key() : '';
	if ( $prov === 'anthropic' && $akey !== '' ) {
		$model = (string) get_option( 'nl_drop_anthropic_model', 'claude-sonnet-5' );
		$resp  = wp_remote_post( 'https://api.anthropic.com/v1/messages', array(
			'timeout' => 90,
			'headers' => array( 'x-api-key' => $akey, 'anthropic-version' => '2023-06-01', 'content-type' => 'application/json' ),
			'body'    => wp_json_encode( array(
				'model'      => $model,
				'max_tokens' => (int) $max_tokens,
				'system'     => (string) $system,
				'messages'   => array( array( 'role' => 'user', 'content' => (string) $user ) ),
			), JSON_UNESCAPED_UNICODE ),
		) );
		if ( is_wp_error( $resp ) ) { $err = $resp->get_error_message(); return null; }
		$code = (int) wp_remote_retrieve_response_code( $resp );
		$data = json_decode( wp_remote_retrieve_body( $resp ), true );
		if ( $code < 200 || $code >= 300 || ! is_array( $data ) ) { $err = 'http_' . $code; return null; }
		$txt = '';
		foreach ( (array) ( $data['content'] ?? array() ) as $blk ) {
			if ( ( $blk['type'] ?? '' ) === 'text' ) { $txt .= (string) $blk['text']; }
		}
		if ( function_exists( 'nadlan_ai_record_usage' ) ) { nadlan_ai_record_usage( 'anthropic', $model, (array) ( $data['usage'] ?? array() ), 0, 'ok' ); }
		nl_drop_usage_add( $model, $data['usage']['input_tokens'] ?? 0, $data['usage']['output_tokens'] ?? 0 );
		$j = nl_drop_parse_json( $txt );
		if ( ! is_array( $j ) ) { $err = 'badjson'; }
		return $j;
	}
	if ( $okey === '' ) { $err = 'nokey'; return null; }
	$models = array_values( array_unique( array( (string) get_option( 'nl_drop_openai_model', 'gpt-4.1' ), 'gpt-4o', 'gpt-4o-mini' ) ) );
	foreach ( $models as $model ) {
		$resp = wp_remote_post( 'https://api.openai.com/v1/chat/completions', array(
			'timeout' => 90,
			'headers' => array( 'Authorization' => 'Bearer ' . $okey, 'Content-Type' => 'application/json' ),
			'body'    => wp_json_encode( array(
				'model'           => $model,
				'store'           => false,
				'temperature'     => 0.2,
				'max_tokens'      => (int) $max_tokens,
				'response_format' => array( 'type' => 'json_object' ),
				'messages'        => array(
					array( 'role' => 'system', 'content' => (string) $system ),
					array( 'role' => 'user', 'content' => (string) $user ),
				),
			), JSON_UNESCAPED_UNICODE ),
		) );
		if ( is_wp_error( $resp ) ) { $err = $resp->get_error_message(); continue; }
		$code = (int) wp_remote_retrieve_response_code( $resp );
		$data = json_decode( wp_remote_retrieve_body( $resp ), true );
		if ( $code >= 200 && $code < 300 && is_array( $data ) ) {
			if ( function_exists( 'nadlan_ai_record_usage' ) ) { nadlan_ai_record_usage( 'openai', $model, (array) ( $data['usage'] ?? array() ), 0, 'ok' ); }
			nl_drop_usage_add( $model, $data['usage']['prompt_tokens'] ?? 0, $data['usage']['completion_tokens'] ?? 0 );
			$j = nl_drop_parse_json( (string) ( $data['choices'][0]['message']['content'] ?? '' ) );
			if ( is_array( $j ) ) { return $j; }
			$err = 'badjson';
			continue;
		}
		$err = 'http_' . $code . ':' . $model;
		if ( $code === 401 || $code === 429 ) { break; }
	}
	return null;
}

/* =====================================================================================================
 * Step 1: read the facts. Only what the broker wrote survives.
 * ===================================================================================================== */
function nl_drop_extract_prompt() {
	return <<<'NLPROMPT'
You read ONE message that an Israeli real-estate broker wrote about ONE property, in Hebrew or English, often informal. Return ONLY a JSON object with exactly these keys:
listing_type ("sale" or "rent" or null), property_type ("apartment", "penthouse", "mini_penthouse", "garden", "duplex", "villa", "cottage", "studio", "other" or null), exclusive (true or false),
city_he, city_en, area_he, area_en, street_he, street_en,
rooms, size_sqm, balcony_sqm, garden_sqm, floor, total_floors, price, parking_count,
parking, storage, elevator, protected_room, ac, furnished (each true, false or null),
condition ("new", "renovated", "good", "needs_renovation" or null),
entry_he, entry_en, view_he, view_en, features_he (array), features_en (array), notes_he, notes_en.

Rules, all strict:
1. Use null whenever the message does not say it. Never guess, never fill a typical value, never infer a number.
2. Every number you return must be written in the message. You may convert only units that are written: "4.2 מיליון" is 4200000, "15 אלף" is 15000, "4,650,000" is 4650000.
3. listing_type: "sale" when the message sells (למכירה, מחיר, מיליון, for sale); "rent" when it rents (להשכרה, לחודש, שכ"ד, for rent). null if neither is clear.
4. price: the asking price in NIS for a sale, or the monthly rent for a rental. Only if written.
5. floor: 0 for a ground floor only if the message says קרקע or ground. "5 מתוך 8" means floor 5 and total_floors 8.
6. exclusive: true only if the message says בלעדיות, בבלעדיות, בלעדי or exclusive.
7. area_he: the neighborhood or area exactly as written in the message. area_en: its usual English spelling (Tzukei Aviv, Nofei Yam, Kochav HaTzafon, Ramat Aviv HaHadasha, Herzliya Pituach, Sarona, Neve Tzedek, Old North, Bavli, Florentin). city_he and city_en: only if written, or if the neighborhood is unmistakably inside one city (נופי ים, צוקי אביב, כוכב הצפון, רמת אביב, שרונה, בבלי, יפו, פלורנטין, נווה צדק are areas in תל אביב-יפו / Tel Aviv-Yafo, so for them area_he is the area and city_he is תל אביב-יפו; הרצליה פיתוח is in הרצליה / Herzliya).
8. street_he: only if a street is written; street_en: the same street in English letters. Both are kept private and never published.
9. parking_count: only if a number of parking spaces is written. parking: true if parking is mentioned at all.
10. features_he: up to 8 short items taken from the message (materials, brands, systems, facilities, what the balcony faces), each under 40 characters, in Hebrew, with no praise words the message does not use. features_en: the same items in English, in the same order.
11. view_he and view_en: only if the message says what is seen (ים or sea, פארק or park, העיר or the city).
12. entry_he: as written (מיידית, 1.10, גמיש). entry_en: the same in English (Immediate, 1 October, Flexible).
13. notes_he and notes_en: other facts from the message that a buyer or tenant needs (a tenant in place, payment terms, building services), under 300 characters, or null.
Output JSON only.
NLPROMPT;
}

function nl_drop_extract( $text, $b, &$err = null ) {
	$sys = nl_drop_extract_prompt();
	if ( ! empty( $b['areas'] ) ) { $sys .= "\nThis broker usually works in: " . implode( ', ', $b['areas'] ) . '. Use this only to spell an area the message names, never to add one.'; }
	$j = nl_drop_llm_json( $sys, $text, 1100, $err );
	$f = is_array( $j ) ? $j : nl_drop_extract_basic( $text );
	return nl_drop_clean_facts( $f, $text );
}

/** Used only when no model is available: the plainest reading of the message. */
function nl_drop_extract_basic( $text ) {
	$t = (string) $text;
	$f = array();
	if ( preg_match( '/להשכרה|לחודש|שכ"ד|שכ״ד|for rent/iu', $t ) ) { $f['listing_type'] = 'rent'; }
	elseif ( preg_match( '/למכירה|מיליון|מליון|for sale/iu', $t ) ) { $f['listing_type'] = 'sale'; }
	if ( preg_match( '/(\d+(?:\.\d)?)\s*(?:חדרים|חד׳|חד\'|חד\b|rooms)/u', $t, $m ) ) { $f['rooms'] = (float) $m[1]; }
	if ( preg_match( '/(\d{2,4})\s*(?:מ״ר|מ"ר|מטר|sqm|m2)/u', $t, $m ) ) { $f['size_sqm'] = (int) $m[1]; }
	if ( preg_match( '/קומה\s*(\d+)(?:\s*(?:מתוך|מ-)\s*(\d+))?/u', $t, $m ) ) { $f['floor'] = (int) $m[1]; if ( ! empty( $m[2] ) ) { $f['total_floors'] = (int) $m[2]; } }
	if ( preg_match( '/מרפסת[^\d]{0,12}(\d{1,3})\s*(?:מ״ר|מ"ר|מטר)/u', $t, $m ) ) { $f['balcony_sqm'] = (int) $m[1]; }
	$max = 0;
	foreach ( nl_drop_nums_in_text( $t ) as $n ) { if ( $n >= 1000 && $n > $max ) { $max = $n; } }
	if ( $max ) { $f['price'] = (int) $max; }
	if ( preg_match( '/בלעדי/u', $t ) ) { $f['exclusive'] = true; }
	foreach ( array( 'חניה' => 'parking', 'חנייה' => 'parking', 'מחסן' => 'storage', 'מעלית' => 'elevator', 'ממ״ד' => 'protected_room', 'ממ"ד' => 'protected_room', 'מרוהט' => 'furnished' ) as $w => $k ) {
		if ( strpos( $t, $w ) !== false ) { $f[ $k ] = true; }
	}
	return $f;
}

function nl_drop_clean_facts( $j, $text ) {
	$nums = nl_drop_nums_in_text( $text );
	$norm = nl_drop_norm( $text );
	$str  = function ( $v, $max ) {
		if ( ! is_string( $v ) && ! is_numeric( $v ) ) { return null; }
		$v = trim( wp_strip_all_tags( (string) $v ) );
		if ( $v === '' || strtolower( $v ) === 'null' ) { return null; }
		return function_exists( 'mb_substr' ) ? mb_substr( $v, 0, $max ) : substr( $v, 0, $max );
	};
	$bool = function ( $v ) {
		if ( $v === true || $v === 'true' || $v === 1 || $v === '1' ) { return true; }
		if ( $v === false || $v === 'false' || $v === 0 || $v === '0' ) { return false; }
		return null;
	};
	$f = array();
	$f['listing_type']  = in_array( $j['listing_type'] ?? null, array( 'sale', 'rent' ), true ) ? $j['listing_type'] : null;
	$types              = array( 'apartment', 'penthouse', 'mini_penthouse', 'garden', 'duplex', 'villa', 'cottage', 'studio', 'other' );
	$f['property_type'] = in_array( $j['property_type'] ?? null, $types, true ) ? $j['property_type'] : null;
	$f['exclusive']     = $bool( $j['exclusive'] ?? false ) === true && preg_match( '/בלעדי|exclusive/iu', (string) $text );
	foreach ( array( 'rooms' => 30, 'size_sqm' => 5000, 'balcony_sqm' => 2000, 'garden_sqm' => 20000, 'floor' => 120, 'total_floors' => 120, 'price' => 500000000, 'parking_count' => 20 ) as $k => $max ) {
		$v = $j[ $k ] ?? null;
		if ( ! is_numeric( $v ) ) { $f[ $k ] = null; continue; }
		$v = (float) $v;
		if ( $v < 0 || $v > $max ) { $f[ $k ] = null; continue; }
		if ( $k === 'floor' && $v == 0 ) { $f[ $k ] = preg_match( '/קרקע|ground/iu', (string) $text ) ? 0 : null; continue; }
		$f[ $k ] = nl_drop_num_ok( $v, $nums ) ? ( in_array( $k, array( 'rooms' ), true ) ? $v : (int) round( $v ) ) : null;
	}
	if ( $f['total_floors'] !== null && $f['floor'] !== null && $f['total_floors'] < $f['floor'] ) { $f['total_floors'] = null; }
	foreach ( array( 'parking', 'storage', 'elevator', 'protected_room', 'ac', 'furnished' ) as $k ) { $f[ $k ] = $bool( $j[ $k ] ?? null ); }
	if ( $f['parking_count'] ) { $f['parking'] = true; }
	$f['condition'] = in_array( $j['condition'] ?? null, array( 'new', 'renovated', 'good', 'needs_renovation' ), true ) ? $j['condition'] : null;
	foreach ( array( 'city_he' => 60, 'city_en' => 60, 'area_he' => 60, 'area_en' => 60, 'street_he' => 80, 'street_en' => 80, 'entry_he' => 60, 'entry_en' => 60, 'view_he' => 60, 'view_en' => 60, 'notes_he' => 320, 'notes_en' => 320 ) as $k => $max ) {
		$f[ $k ] = $str( $j[ $k ] ?? null, $max );
	}
	foreach ( array( 'city_he', 'area_he', 'street_he', 'entry_he', 'view_he', 'notes_he' ) as $k ) {
		if ( $f[ $k ] !== null ) { $f[ $k ] = nl_drop_he_typo( $f[ $k ] ); }
	}
	// the area must be written in the message; a city may follow from a named neighborhood
	if ( $f['area_he'] !== null && strpos( $norm, nl_drop_norm( $f['area_he'] ) ) === false ) { $f['area_he'] = null; $f['area_en'] = null; }
	if ( $f['area_he'] === null && $f['area_en'] !== null && strpos( $norm, nl_drop_norm( $f['area_en'] ) ) === false ) { $f['area_en'] = null; }
	if ( $f['view_he'] !== null && strpos( $norm, nl_drop_norm( $f['view_he'] ) ) === false && ! preg_match( '/נוף|ים|view|sea/iu', (string) $text ) ) { $f['view_he'] = null; $f['view_en'] = null; }
	foreach ( array( 'features_he', 'features_en' ) as $k ) {
		$list = array();
		foreach ( (array) ( $j[ $k ] ?? array() ) as $item ) {
			$item = $str( $item, 60 );
			if ( $item === null ) { continue; }
			$ok = true;
			foreach ( nl_drop_nums_in_copy( $item ) as $n ) { if ( ! nl_drop_num_ok( $n, $nums ) ) { $ok = false; } }
			if ( $ok ) { $list[] = $k === 'features_he' ? nl_drop_he_typo( $item ) : $item; }
			if ( count( $list ) >= 8 ) { break; }
		}
		$f[ $k ] = $list;
	}
	$dates = array_merge( $nums, nl_drop_date_parts( (string) $f['entry_he'] ) );
	foreach ( array( 'notes_he', 'notes_en', 'entry_he', 'entry_en' ) as $k ) {
		if ( $f[ $k ] === null ) { continue; }
		foreach ( nl_drop_nums_in_copy( $f[ $k ] ) as $n ) { if ( ! nl_drop_num_ok( $n, strpos( $k, 'entry' ) === 0 ? $dates : $nums ) ) { $f[ $k ] = null; break; } }
	}
	return $f;
}

/** What still stops a page from being built. Hebrew, for the broker's screen. */
function nl_drop_missing( $f, $photos ) {
	$miss = array();
	if ( empty( $f['listing_type'] ) ) { $miss[] = 'למכירה או להשכרה'; }
	if ( empty( $f['area_he'] ) && empty( $f['city_he'] ) ) { $miss[] = 'שכונה או עיר'; }
	if ( empty( $f['rooms'] ) && empty( $f['size_sqm'] ) ) { $miss[] = 'מספר חדרים או שטח במ״ר'; }
	if ( empty( $photos ) ) { $miss[] = 'לפחות תמונה אחת'; }
	return $miss;
}

function nl_drop_summary( $f ) {
	$p = array();
	if ( ! empty( $f['listing_type'] ) ) { $p[] = nl_drop_t( 'he', $f['listing_type'] ); }
	if ( ! empty( $f['property_type'] ) && $f['property_type'] !== 'other' ) { $p[] = nl_drop_type_label( $f['property_type'], 'he' ); }
	if ( ! empty( $f['rooms'] ) ) { $p[] = sprintf( nl_drop_t( 'he', 'rooms_n' ), nl_drop_fmt_num( $f['rooms'] ) ); }
	if ( ! empty( $f['size_sqm'] ) ) { $p[] = sprintf( nl_drop_t( 'he', 'size_n' ), nl_drop_fmt_int( $f['size_sqm'] ) ); }
	$place = trim( implode( ', ', array_filter( array( $f['area_he'] ?? '', $f['city_he'] ?? '' ) ) ) );
	if ( $place !== '' ) { $p[] = $place; }
	$p[] = ! empty( $f['price'] ) ? nl_drop_price_text( $f['price'], 'he' ) : 'מחיר בפנייה';
	return implode( ' · ', $p );
}

/* =====================================================================================================
 * Step 2: write the page. Hebrew first, English as its faithful translation. Gated field by field.
 * ===================================================================================================== */
function nl_drop_write_prompt( $b ) {
	$p = <<<'NLPROMPT'
You write the listing page for ONE property on the website of an Israeli luxury real-estate broker. You receive FACTS (JSON, already checked against the broker's words) and the broker's own MESSAGE. Write in Hebrew and in English. Return ONLY a JSON object {"he": {...}, "en": {...}} where each has exactly these keys:
title, card_title, dek, story_h2, story, features, chips, card_hi, seo_title, seo_desc.

Hard rules. A field that breaks one is thrown away:
1. Use only what is in FACTS and MESSAGE. Do not add a view, a direction, a floor, a facility, a distance, a year, a building name, a material or a number that is not there. The examples below show the style only; never copy their facts.
2. Wherever you state the price or the rent, write the token {{PRICE}} exactly, never the number. If FACTS.price is null, do not mention the price at all.
3. Never mention the street or the address. Never mention the broker, a licence, a listing site, a portal or a source.
4. No exclamation marks. No long dashes; use a comma or a colon. No hype: no הזדמנות, חלום, מושלם, מדהים, חוויה, and no "once in a lifetime", "dream", "stunning", "breathtaking".
5. Specific details beat adjectives. Quiet, precise sentences, the way a top Tel Aviv broker writes to a private client.
6. Numbers as digits, exactly as in FACTS (110 מ״ר, 4.5 חדרים, קומה 5 מתוך 8; 110 sqm, 4.5 rooms, floor 5 of 8).

Fields (English is a faithful translation of the Hebrew):
- title: [type or rooms] [what is rare], [area]. Max 60 characters. Style: "3 חדרים עם מרפסת של 20 מ״ר ו-2 חניות, נופי ים" / "Three Rooms with a 20 sqm Balcony, Nofei Yam".
- card_title: a shorter title for a card, max 45 characters, without the area.
- dek: 25 to 45 words. Order: location, what is rare, two or three facts, then {{PRICE}} if there is a price. Style: "בקומה 5 בבניין בוטיק ברמת אביב: 4 חדרים על 110 מ״ר, מרפסת של 12 מ״ר, חניה ומחסן. {{PRICE}}."
- story_h2: a short heading for the home, max 50 characters.
- story: an array of 2 or 3 short paragraphs. First the home (layout, rooms, balcony, what it faces only if given). Then the finish and systems, only if given. Then the building and the surroundings, only if given. If there is little to say, write 2 short paragraphs, never padding.
- features: 4 to 6 pairs [short bold line, short second line], each from the facts.
- chips: 2 very short facts, max 28 characters each.
- card_hi: 3 short highlights for a card, max 40 characters each.
- seo_title: max 65 characters, holds the property type or rooms, the deal (למכירה or להשכרה; for Sale or for Rent) and the area.
- seo_desc: max 155 characters, the key facts, {{PRICE}} if there is a price.

Typography and words:
- Hebrew uses gershayim and geresh: מ״ר, ממ״ד, ש״ח, ג׳קוזי. Never a plain quote mark inside a Hebrew word.
- English: "lift" (not elevator), "safe room" (not protected room), "sqm", "floor 5 of 7".
- features: the bold line is the fact itself, the second line is its context from the MESSAGE. If the MESSAGE gives no context, the second line is "" (empty). Never pad: no "high-quality finish", "advanced systems", "access from the living room", "Yes", "כן".
- Descriptive words are claims. sea, view, quiet, bright, spacious, new, renovated, boutique, designer, luxury, and their Hebrew forms, may appear only if the MESSAGE says so.

A worked example about a DIFFERENT property. Copy the voice and the structure, never its facts:
MESSAGE: "להשכרה בבלעדיות: 3 חדרים 90 מ"ר, מרפסת 20 מ"ר לשטח פתוח, קומה 5 מתוך 7, בניין על עמודים עם מעלית, ממ"ד, 2 חניות נפרדות ומחסן גדול ליד החניה. 9,500 לחודש, כניסה 1.10 גמיש. נופי ים."
OUTPUT he: title "3 חדרים עם מרפסת של 20 מ״ר ו-2 חניות, נופי ים"; card_title "3 חדרים עם מרפסת של 20 מ״ר"; dek "בקומה 5 מתוך 7 בנופי ים: 3 חדרים על 90 מ״ר עם מרפסת של 20 מ״ר לשטח פתוח, ממ״ד, 2 חניות נפרדות ומחסן גדול. {{PRICE}} לחודש."; story_h2 "3 חדרים ומרפסת של 20 מ״ר בנופי ים"; story ["3 חדרים על 90 מ״ר, מרפסת של 20 מ״ר הפונה לשטח פתוח, וממ״ד, בקומה 5 בבניין בן 7 קומות על עמודים עם מעלית.", "לדירה 2 חניות נפרדות ומחסן גדול ליד החניה. שכר הדירה {{PRICE}} לחודש, והכניסה ב-1.10 בגמישות."]; features [["90 מ״ר ומרפסת של 20 מ״ר", "3 חדרים"], ["ממ״ד בתוך הדירה", "מרחב מוגן דירתי"], ["2 חניות נפרדות", "ומחסן גדול ליד החניה"], ["קומה 5 מתוך 7", "בניין על עמודים עם מעלית"]]; chips ["ממ״ד, 2 חניות ומחסן", "כניסה ב-1.10, גמיש"]; card_hi ["מרפסת לשטח פתוח", "מחסן גדול ליד החניה", "בניין על עמודים עם מעלית"]; seo_title "דירת 3 חדרים להשכרה בנופי ים, מרפסת 20 מ״ר ו-2 חניות".
OUTPUT en: title "Three Rooms with a 20 sqm Balcony and Two Parking Spaces, Nofei Yam"; dek "On floor 5 of 7 in Nofei Yam: three rooms on 90 sqm with a 20 sqm balcony facing an open area, a safe room, two separate parking spaces and a large storage room. {{PRICE}} a month."; features [["90 sqm plus a 20 sqm balcony", "Three rooms"], ["Safe room inside the unit", "An in-apartment protected room"], ["Two separate parking spaces", "And a large storage room by the parking"], ["Floor 5 of 7", "A building on pillars with a lift"]].
NLPROMPT;
	return $p;
}

function nl_drop_write( $f, $text, $b, &$err = null ) {
	$pub = $f;
	unset( $pub['street_he'], $pub['street_en'] );
	$user = wp_json_encode( array( 'FACTS' => $pub, 'MESSAGE' => (string) $text ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
	$j    = nl_drop_llm_json( nl_drop_write_prompt( $b ), $user, 2600, $err );
	return nl_drop_finish_copy( is_array( $j ) ? $j : array(), $f, $text );
}

function nl_drop_finish_copy( $j, $f, $text ) {
	$allowed = nl_drop_allowed_numbers( $f, $text );
	$names   = array_values( array_filter( array( $f['area_he'] ?? '', $f['area_en'] ?? '', $f['city_he'] ?? '', $f['city_en'] ?? '' ) ) );
	$stated  = nl_drop_stated( $f, $text );
	$out     = array();
	$caps    = array( 'title' => 90, 'card_title' => 70, 'dek' => 460, 'story_h2' => 80, 'seo_title' => 90, 'seo_desc' => 200 );
	foreach ( array( 'he', 'en' ) as $lang ) {
		$src = isset( $j[ $lang ] ) && is_array( $j[ $lang ] ) ? $j[ $lang ] : array();
		$tpl = nl_drop_tpl( $f, $lang );
		$c   = array();
		$fix = function ( $s ) use ( $f, $lang ) {
			$s = trim( wp_strip_all_tags( (string) $s ) );
			if ( ! empty( $f['price'] ) ) {
				$num = preg_quote( nl_drop_fmt_int( $f['price'] ), '/' );
				$raw = preg_quote( (string) (int) $f['price'], '/' );
				$s   = preg_replace( '/(?:NIS\s*|₪\s*)?(?<![\d,.])(?:' . $num . '|' . $raw . ')(?!\d|,\d|\.\d)(?:\s*(?:ש״ח|ש"ח|₪|שקלים|NIS))?/u', '{{PRICE}}', $s );
			}
			$s = preg_replace( '/\s+/u', ' ', $s );
			return $lang === 'he' ? nl_drop_he_typo( $s ) : $s;
		};
		$ok = function ( $s ) use ( $lang, $allowed, $stated, $names, $f ) { return $s !== '' && ! nl_drop_gate_str( $s, $lang, $allowed, $stated, $names ) && ! nl_drop_has_street( $s, $f ); };
		foreach ( $caps as $k => $max ) {
			$v   = $fix( $src[ $k ] ?? '' );
			$v   = function_exists( 'mb_substr' ) ? mb_substr( $v, 0, $max ) : substr( $v, 0, $max );
			$c[ $k ] = $ok( $v ) ? $v : $tpl[ $k ];
		}
		$story = array();
		foreach ( array_slice( (array) ( $src['story'] ?? array() ), 0, 3 ) as $para ) {
			$para = $fix( $para );
			if ( $ok( $para ) ) { $story[] = function_exists( 'mb_substr' ) ? mb_substr( $para, 0, 800 ) : $para; }
		}
		$c['story'] = count( $story ) >= 1 ? $story : $tpl['story'];
		$feat = array();
		foreach ( array_slice( (array) ( $src['features'] ?? array() ), 0, 6 ) as $pair ) {
			$pair = array_values( (array) $pair );
			$bo   = $fix( $pair[0] ?? '' );
			$sm   = $fix( $pair[1] ?? '' );
			if ( $sm !== '' && ( ! $ok( $sm ) || in_array( nl_drop_norm( $sm ), array( 'כן', 'yes', 'יש', 'included' ), true ) ) ) { $sm = ''; }
			if ( $ok( $bo ) ) { $feat[] = array( $bo, $sm ); }
		}
		$c['features'] = count( $feat ) >= 3 ? $feat : $tpl['features'];
		foreach ( array( 'chips' => array( 2, 40 ), 'card_hi' => array( 3, 60 ) ) as $k => $lim ) {
			$list = array();
			foreach ( array_slice( (array) ( $src[ $k ] ?? array() ), 0, $lim[0] ) as $s ) {
				$s = $fix( $s );
				if ( $ok( $s ) ) { $list[] = function_exists( 'mb_substr' ) ? mb_substr( $s, 0, $lim[1] ) : $s; }
			}
			$c[ $k ] = $list ? $list : $tpl[ $k ];
		}
		$out[ $lang ] = $c;
	}
	return $out;
}

/** The plain version: used field by field whenever the model is unavailable or a field fails the gate. */
function nl_drop_tpl( $f, $lang ) {
	$he    = $lang !== 'en';
	$deal  = ( $f['listing_type'] ?? '' ) === 'rent' ? 'rent' : 'sale';
	$area  = $he ? ( $f['area_he'] ?: ( $f['city_he'] ?: '' ) ) : ( $f['area_en'] ?: ( $f['city_en'] ?: '' ) );
	$city  = $he ? ( $f['city_he'] ?? '' ) : ( $f['city_en'] ?? '' );
	$type  = $f['property_type'] ?: '';
	$rooms = ! empty( $f['rooms'] ) ? nl_drop_fmt_num( $f['rooms'] ) : '';
	$plain = in_array( $type, array( '', 'apartment', 'other' ), true );
	if ( $he ) {
		$head = $rooms !== '' ? ( $plain ? $rooms . ' חדרים' : nl_drop_type_label( $type, 'he' ) . ' ' . $rooms . ' חדרים' ) : nl_drop_type_label( $type ?: 'other', 'he' );
		$rare = ! empty( $f['balcony_sqm'] ) ? ' עם מרפסת של ' . nl_drop_fmt_int( $f['balcony_sqm'] ) . ' מ״ר' : ( ! empty( $f['garden_sqm'] ) ? ' עם גינה של ' . nl_drop_fmt_int( $f['garden_sqm'] ) . ' מ״ר' : '' );
		$bits = array();
		if ( ! empty( $f['size_sqm'] ) ) { $bits[] = ( $rooms !== '' ? $rooms . ' חדרים על ' : '' ) . nl_drop_fmt_int( $f['size_sqm'] ) . ' מ״ר'; }
		elseif ( $rooms !== '' ) { $bits[] = $rooms . ' חדרים'; }
		if ( ! empty( $f['balcony_sqm'] ) ) { $bits[] = 'מרפסת של ' . nl_drop_fmt_int( $f['balcony_sqm'] ) . ' מ״ר'; }
		if ( isset( $f['floor'] ) && $f['floor'] !== null ) { $bits[] = $f['floor'] == 0 ? 'קומת קרקע' : 'קומה ' . (int) $f['floor'] . ( ! empty( $f['total_floors'] ) ? ' מתוך ' . (int) $f['total_floors'] : '' ); }
		if ( ! empty( $f['parking_count'] ) ) { $bits[] = $f['parking_count'] > 1 ? (int) $f['parking_count'] . ' חניות' : 'חניה'; }
		elseif ( ! empty( $f['parking'] ) ) { $bits[] = 'חניה'; }
		if ( ! empty( $f['storage'] ) ) { $bits[] = 'מחסן'; }
		if ( ! empty( $f['protected_room'] ) ) { $bits[] = 'ממ״ד'; }
		$place = trim( $area . ( $city && $city !== $area ? ', ' . $city : '' ) );
		$dek   = ( $place !== '' ? $place . ': ' : '' ) . implode( ', ', $bits ) . '.';
		if ( ! empty( $f['price'] ) ) { $dek .= ' {{PRICE}}' . ( $deal === 'rent' ? ' לחודש' : '' ) . '.'; }
		$story = array( rtrim( $dek, '.' ) . '.' );
		if ( ! empty( $f['features_he'] ) ) { $story[] = 'בנכס: ' . implode( ', ', array_slice( $f['features_he'], 0, 6 ) ) . '.'; }
		if ( ! empty( $f['notes_he'] ) ) { $story[] = rtrim( $f['notes_he'], '.' ) . '.'; }
		$feat = array();
		if ( ! empty( $f['size_sqm'] ) ) { $feat[] = array( nl_drop_fmt_int( $f['size_sqm'] ) . ' מ״ר', $rooms !== '' ? $rooms . ' חדרים' : '' ); }
		if ( ! empty( $f['balcony_sqm'] ) ) { $feat[] = array( 'מרפסת של ' . nl_drop_fmt_int( $f['balcony_sqm'] ) . ' מ״ר', $f['view_he'] ? 'נוף ל' . $f['view_he'] : '' ); }
		if ( isset( $f['floor'] ) && $f['floor'] !== null ) { $feat[] = array( $f['floor'] == 0 ? 'קומת קרקע' : 'קומה ' . (int) $f['floor'] . ( ! empty( $f['total_floors'] ) ? ' מתוך ' . (int) $f['total_floors'] : '' ), ! empty( $f['elevator'] ) ? 'עם מעלית' : '' ); }
		if ( ! empty( $f['parking'] ) || ! empty( $f['storage'] ) ) { $feat[] = array( trim( ( ! empty( $f['parking_count'] ) && $f['parking_count'] > 1 ? (int) $f['parking_count'] . ' חניות' : ( ! empty( $f['parking'] ) ? 'חניה' : '' ) ) . ( ! empty( $f['storage'] ) ? ( ! empty( $f['parking'] ) ? ' ומחסן' : 'מחסן' ) : '' ) ), 'צמודים לנכס' ); }
		if ( ! empty( $f['protected_room'] ) ) { $feat[] = array( 'ממ״ד', 'מרחב מוגן דירתי' ); }
		if ( ! empty( $f['entry_he'] ) ) { $feat[] = array( 'כניסה: ' . $f['entry_he'], '' ); }
		foreach ( array_slice( $f['features_he'] ?? array(), 0, max( 0, 6 - count( $feat ) ) ) as $x ) { $feat[] = array( $x, '' ); }
		$seo_head = $rooms !== '' ? ( $plain ? 'דירת ' . $rooms . ' חדרים' : nl_drop_type_label( $type, 'he' ) . ' ' . $rooms . ' חדרים' ) : nl_drop_type_label( $type ?: 'other', 'he' );
		return array(
			'title'      => $head . $rare . ( $area !== '' ? ', ' . $area : '' ),
			'card_title' => $head . $rare,
			'dek'        => $dek,
			'story_h2'   => $head . ( $area !== '' ? ' ב' . $area : '' ),
			'story'      => $story,
			'features'   => array_slice( $feat, 0, 6 ),
			'chips'      => array_slice( array_filter( array( ! empty( $f['size_sqm'] ) ? nl_drop_fmt_int( $f['size_sqm'] ) . ' מ״ר' : '', ! empty( $f['entry_he'] ) ? 'כניסה: ' . $f['entry_he'] : ( ! empty( $f['protected_room'] ) ? 'ממ״ד' : '' ) ) ), 0, 2 ),
			'card_hi'    => array_slice( array_merge( $f['features_he'] ?? array(), array_filter( array( ! empty( $f['storage'] ) ? 'מחסן' : '', ! empty( $f['elevator'] ) ? 'מעלית' : '' ) ) ), 0, 3 ),
			'seo_title'  => $seo_head . ' ' . nl_drop_t( 'he', $deal ) . ( $area !== '' ? ' ב' . $area : '' ),
			'seo_desc'   => function_exists( 'mb_substr' ) ? mb_substr( $dek, 0, 155 ) : $dek,
		);
	}
	$head = $rooms !== '' ? ( $plain ? $rooms . '-Room ' . ( $type === 'apartment' || $type === '' ? 'Apartment' : 'Home' ) : $rooms . '-Room ' . nl_drop_type_label( $type, 'en' ) ) : nl_drop_type_label( $type ?: 'other', 'en' );
	$rare = ! empty( $f['balcony_sqm'] ) ? ' with a ' . nl_drop_fmt_int( $f['balcony_sqm'] ) . ' sqm Balcony' : ( ! empty( $f['garden_sqm'] ) ? ' with a ' . nl_drop_fmt_int( $f['garden_sqm'] ) . ' sqm Garden' : '' );
	$bits = array();
	if ( ! empty( $f['size_sqm'] ) ) { $bits[] = ( $rooms !== '' ? $rooms . ' rooms on ' : '' ) . nl_drop_fmt_int( $f['size_sqm'] ) . ' sqm'; }
	elseif ( $rooms !== '' ) { $bits[] = $rooms . ' rooms'; }
	if ( ! empty( $f['balcony_sqm'] ) ) { $bits[] = 'a ' . nl_drop_fmt_int( $f['balcony_sqm'] ) . ' sqm balcony'; }
	if ( isset( $f['floor'] ) && $f['floor'] !== null ) { $bits[] = $f['floor'] == 0 ? 'ground floor' : 'floor ' . (int) $f['floor'] . ( ! empty( $f['total_floors'] ) ? ' of ' . (int) $f['total_floors'] : '' ); }
	if ( ! empty( $f['parking_count'] ) ) { $bits[] = $f['parking_count'] > 1 ? (int) $f['parking_count'] . ' parking spaces' : 'parking'; }
	elseif ( ! empty( $f['parking'] ) ) { $bits[] = 'parking'; }
	if ( ! empty( $f['storage'] ) ) { $bits[] = 'a storage room'; }
	if ( ! empty( $f['protected_room'] ) ) { $bits[] = 'a safe room'; }
	$place = trim( $area . ( $city && $city !== $area ? ', ' . $city : '' ) );
	$dek   = ( $place !== '' ? $place . ': ' : '' ) . implode( ', ', $bits ) . '.';
	if ( ! empty( $f['price'] ) ) { $dek .= ' {{PRICE}}' . ( $deal === 'rent' ? ' a month' : '' ) . '.'; }
	$story = array( $dek );
	if ( ! empty( $f['features_en'] ) ) { $story[] = 'The home includes ' . implode( ', ', array_slice( $f['features_en'], 0, 6 ) ) . '.'; }
	if ( ! empty( $f['notes_en'] ) ) { $story[] = rtrim( $f['notes_en'], '.' ) . '.'; }
	$feat = array();
	if ( ! empty( $f['size_sqm'] ) ) { $feat[] = array( nl_drop_fmt_int( $f['size_sqm'] ) . ' sqm', $rooms !== '' ? $rooms . ' rooms' : '' ); }
	if ( ! empty( $f['balcony_sqm'] ) ) { $feat[] = array( 'A ' . nl_drop_fmt_int( $f['balcony_sqm'] ) . ' sqm balcony', $f['view_en'] ? 'Facing the ' . $f['view_en'] : '' ); }
	if ( isset( $f['floor'] ) && $f['floor'] !== null ) { $feat[] = array( $f['floor'] == 0 ? 'Ground floor' : 'Floor ' . (int) $f['floor'] . ( ! empty( $f['total_floors'] ) ? ' of ' . (int) $f['total_floors'] : '' ), ! empty( $f['elevator'] ) ? 'With a lift' : '' ); }
	if ( ! empty( $f['parking'] ) || ! empty( $f['storage'] ) ) { $feat[] = array( trim( ( ! empty( $f['parking_count'] ) && $f['parking_count'] > 1 ? (int) $f['parking_count'] . ' parking spaces' : ( ! empty( $f['parking'] ) ? 'Parking' : '' ) ) . ( ! empty( $f['storage'] ) ? ( ! empty( $f['parking'] ) ? ' and storage' : 'Storage' ) : '' ) ), 'Attached to the unit' ); }
	if ( ! empty( $f['protected_room'] ) ) { $feat[] = array( 'Safe room', 'An in-apartment protected room' ); }
	if ( ! empty( $f['entry_en'] ) ) { $feat[] = array( 'Entry: ' . $f['entry_en'], '' ); }
	foreach ( array_slice( $f['features_en'] ?? array(), 0, max( 0, 6 - count( $feat ) ) ) as $x ) { $feat[] = array( $x, '' ); }
	return array(
		'title'      => $head . $rare . ( $area !== '' ? ', ' . $area : '' ),
		'card_title' => $head . $rare,
		'dek'        => $dek,
		'story_h2'   => $head . ( $area !== '' ? ' in ' . $area : '' ),
		'story'      => $story,
		'features'   => array_slice( $feat, 0, 6 ),
		'chips'      => array_slice( array_filter( array( ! empty( $f['size_sqm'] ) ? nl_drop_fmt_int( $f['size_sqm'] ) . ' sqm' : '', ! empty( $f['entry_en'] ) ? 'Entry: ' . $f['entry_en'] : ( ! empty( $f['protected_room'] ) ? 'Safe room' : '' ) ) ), 0, 2 ),
		'card_hi'    => array_slice( array_merge( $f['features_en'] ?? array(), array_filter( array( ! empty( $f['storage'] ) ? 'Storage' : '', ! empty( $f['elevator'] ) ? 'Lift' : '' ) ) ), 0, 3 ),
		'seo_title'  => $head . ' ' . ( $deal === 'rent' ? 'for Rent' : 'for Sale' ) . ( $area !== '' ? ', ' . $area : '' ),
		'seo_desc'   => substr( $dek, 0, 155 ),
	);
}

/* =====================================================================================================
 * Step 3 (brokers with Russian or French): the checked English page, translated, and checked again
 * ===================================================================================================== */

/** A per-language name or date the translation step added: area_ru, city_fr, entry_ru. English is the fallback. */
function nl_drop_fx( $f, $k, $lang ) {
	$lang = nl_drop_L( $lang );
	$v    = isset( $f[ $k . '_' . $lang ] ) ? (string) $f[ $k . '_' . $lang ] : '';
	if ( $v === '' && $lang !== 'he' ) { $v = isset( $f[ $k . '_en' ] ) ? (string) $f[ $k . '_en' ] : ''; }
	return $v;
}

/** The claims the broker made: in the message, the features, the view, the notes, and the condition. */
function nl_drop_stated( $f, $text ) {
	$msg = (string) $text;
	foreach ( array( $f['area_he'] ?? '', $f['area_en'] ?? '', $f['city_he'] ?? '', $f['city_en'] ?? '' ) as $nm ) {
		if ( $nm !== '' && $nm !== null ) { $msg = str_ireplace( (string) $nm, ' ', $msg ); }
	}
	$stated = nl_drop_claims_in( $msg . ' ' . implode( ' ', array_merge( (array) ( $f['features_he'] ?? array() ), (array) ( $f['features_en'] ?? array() ) ) ) . ' ' . ( $f['view_he'] ?? '' ) . ' ' . ( $f['view_en'] ?? '' ) . ' ' . ( $f['notes_he'] ?? '' ) . ' ' . ( $f['notes_en'] ?? '' ) );
	if ( ! empty( $f['garden_sqm'] ) ) { $stated[] = 'garden'; }
	if ( in_array( $f['condition'] ?? '', array( 'renovated', 'needs_renovation' ), true ) ) { $stated[] = 'reno'; }
	if ( ( $f['condition'] ?? '' ) === 'new' ) { $stated[] = 'new'; }
	return array_values( array_unique( $stated ) );
}

function nl_drop_translate_prompt() {
	return <<<'NLPROMPT'
You translate the listing page of ONE property on the website of an Israeli real-estate broker, for Russian-speaking and French-speaking buyers and tenants. You receive EN (the approved English page, already checked against the broker's words), FACTS, and LANGS (the languages to write). Return ONLY a JSON object with one key per language in LANGS ("ru", "fr"), each with exactly these keys:
title, card_title, dek, story_h2, story, features, chips, card_hi, seo_title, seo_desc, area, city, entry.

Hard rules. A field that breaks one is thrown away:
1. Translate faithfully. Add nothing: no view, direction, floor, facility, distance, year, material, adjective or number that is not in EN.
2. Keep the token {{PRICE}} exactly where EN has it. Never write a price or an amount of money.
3. No exclamation marks. No long dashes; use a comma or a colon. No hype. Russian: never уникальный, мечта, идеальный, потрясающий, шикарный, невероятный, сказочный. French: never unique, rêve, parfait, exceptionnel, magnifique, sublime, incroyable, coup de cœur, opportunité.
4. Numbers as digits, the same numbers as EN. Russian and French write decimals with a comma (4,5) and group thousands with a space (1 200).
5. Never mention the broker, a licence, a listing site, a portal or a source.
6. Same structure as EN: story is an array of the same paragraphs, features an array of [bold line, second line] pairs (keep "" where EN has ""), chips and card_hi arrays of the same length.
7. area and city: the usual name of FACTS.area_en and FACTS.city_en in that language (Russian: Тель-Авив, Герцлия-Питуах, Рамат-Авив, Нофей Ям, Цукей Авив; French: Tel Aviv, Herzliya Pituah, Ramat Aviv, Nofei Yam, Tsoukei Aviv), or "" when FACTS has none. entry: FACTS.entry_en in that language, or "".

Vocabulary:
- Russian: комнаты (the Israeli count, the living room included), м², этаж 5 из 8, балкон, мамад (защищённая комната), кладовая, парковка, лифт, въезд. Polite вы.
- French: pièces (the living room counts), m², 5e étage sur 8, balcon, mamad (pièce sécurisée), cave, parking, ascenseur, entrée dans les lieux. Vouvoiement.
- title: max 60 characters. card_title: max 45 characters, no area. seo_title: max 65 characters with the type or rooms, the deal (продажа / аренда; à vendre / à louer) and the area. seo_desc: max 155 characters.
Register: calm and precise, the way a top broker writes to a private client. Prefer the fact to the adjective.
NLPROMPT;
}

function nl_drop_translate( $copy, $f, $text, $langs, &$err = null ) {
	$langs = array_values( array_intersect( array( 'ru', 'fr' ), (array) $langs ) );
	if ( ! $langs ) { return array( 'copy' => array(), 'names' => array() ); }
	$src = array(
		'LANGS' => $langs,
		'FACTS' => array(
			'listing_type'  => $f['listing_type'] ?? null,
			'property_type' => $f['property_type'] ?? null,
			'area_en'       => $f['area_en'] ?? null,
			'city_en'       => $f['city_en'] ?? null,
			'entry_en'      => $f['entry_en'] ?? null,
		),
		'EN'    => isset( $copy['en'] ) ? $copy['en'] : array(),
	);
	$j = nl_drop_llm_json( nl_drop_translate_prompt(), wp_json_encode( $src, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ), 1800 * count( $langs ), $err );
	return nl_drop_finish_tr( is_array( $j ) ? $j : array(), $f, $text, $langs );
}

/** The price, however the model wrote it (4 200 000, 4,200,000, 4200000 ₪), becomes the live token. */
function nl_drop_price_token( $s, $f ) {
	if ( empty( $f['price'] ) ) { return $s; }
	$groups = explode( ',', number_format( (float) $f['price'], 0, '.', ',' ) );
	$num    = implode( '[\s\x{00A0}\x{202F},.]?', array_map( function ( $g ) { return preg_quote( $g, '/' ); }, $groups ) );
	return (string) preg_replace( '/(?:NIS\s*|₪\s*)?(?<![\d,.])' . $num . '(?![\d]|[,.]\d)(?:[\s\x{00A0}\x{202F}]*(?:ש״ח|ש"ח|₪|шекел\p{L}*|шек\.?|NIS|ILS|shekels?))?/u', '{{PRICE}}', (string) $s );
}

function nl_drop_finish_tr( $j, $f, $text, $langs ) {
	$allowed = nl_drop_allowed_numbers( $f, $text );
	$stated  = nl_drop_stated( $f, $text );
	$caps    = array( 'title' => 90, 'card_title' => 70, 'dek' => 460, 'story_h2' => 80, 'seo_title' => 90, 'seo_desc' => 200 );
	$cut     = function ( $s, $n ) { return function_exists( 'mb_substr' ) ? mb_substr( $s, 0, $n ) : substr( $s, 0, $n ); };
	$out     = array( 'copy' => array(), 'names' => array(), 'plain' => array() );
	foreach ( $langs as $lang ) {
		$src = isset( $j[ $lang ] ) && is_array( $j[ $lang ] ) ? $j[ $lang ] : array();
		// the names come first: they are kept out of the claim check (Парк Цамерет is a place, not a park claim)
		$nm = array();
		foreach ( array( 'area' => 60, 'city' => 60, 'entry' => 60 ) as $k => $max ) {
			$v    = $cut( trim( wp_strip_all_tags( (string) ( $src[ $k ] ?? '' ) ) ), $max );
			$base = (string) ( $f[ $k . '_en' ] ?? '' );
			if ( $v === '' || $base === '' || nl_drop_banned_hits( $v, $lang ) || preg_match( '/https?:|www\.|[{}]/i', $v ) ) {
				$v = '';
			} elseif ( $k !== 'entry' && preg_match( '/\d/', $v ) && ! preg_match( '/\d/', $base ) ) {
				$v = '';
			} elseif ( $k === 'entry' ) {
				foreach ( nl_drop_nums_in_copy( $v, $lang ) as $n ) { if ( ! nl_drop_num_ok( $n, $allowed ) ) { $v = ''; break; } }
			}
			$nm[ $k ] = $v;
		}
		$out['names'][ $lang ] = $nm;
		$fl = $f;
		foreach ( $nm as $k => $v ) { if ( $v !== '' ) { $fl[ $k . '_' . $lang ] = $v; } }
		$names = array_values( array_filter( array( $f['area_he'] ?? '', $f['area_en'] ?? '', $f['city_he'] ?? '', $f['city_en'] ?? '', $nm['area'], $nm['city'] ) ) );
		$tpl   = nl_drop_tpl_x( $fl, $lang );
		$fix   = function ( $s ) use ( $f ) {
			$s = nl_drop_price_token( trim( wp_strip_all_tags( (string) $s ) ), $f );
			return trim( (string) preg_replace( '/[ \t\r\n]+/u', ' ', $s ) );
		};
		$ok    = function ( $s ) use ( $lang, $allowed, $stated, $names, $f ) { return $s !== '' && ! nl_drop_gate_str( $s, $lang, $allowed, $stated, $names ) && ! nl_drop_has_street( $s, $f ); };
		$c     = array();
		$bad   = 0;
		foreach ( $caps as $k => $max ) {
			$v = $cut( $fix( $src[ $k ] ?? '' ), $max );
			if ( $ok( $v ) ) { $c[ $k ] = $v; } else { $c[ $k ] = $tpl[ $k ]; $bad++; }
		}
		$story = array();
		foreach ( array_slice( (array) ( $src['story'] ?? array() ), 0, 3 ) as $para ) {
			$para = $fix( $para );
			if ( $ok( $para ) ) { $story[] = $cut( $para, 800 ); }
		}
		$c['story'] = $story ? $story : $tpl['story'];
		$feat = array();
		foreach ( array_slice( (array) ( $src['features'] ?? array() ), 0, 6 ) as $pair ) {
			$pair = array_values( (array) $pair );
			$bo   = $fix( $pair[0] ?? '' );
			$sm   = $fix( $pair[1] ?? '' );
			if ( $sm !== '' && ! $ok( $sm ) ) { $sm = ''; }
			if ( $ok( $bo ) ) { $feat[] = array( $bo, $sm ); }
		}
		$c['features'] = count( $feat ) >= 3 ? $feat : $tpl['features'];
		foreach ( array( 'chips' => array( 2, 40 ), 'card_hi' => array( 3, 60 ) ) as $k => $lim ) {
			$list = array();
			foreach ( array_slice( (array) ( $src[ $k ] ?? array() ), 0, $lim[0] ) as $s ) {
				$s = $fix( $s );
				if ( $ok( $s ) ) { $list[] = $cut( $s, $lim[1] ); }
			}
			$c[ $k ] = $list ? $list : $tpl[ $k ];
		}
		if ( $bad >= 4 || ! $src ) { $c = $tpl; $out['plain'][] = $lang; }
		$out['copy'][ $lang ] = $c;
	}
	return $out;
}

/** The plain Russian or French page, from the structured facts only (the free-text features exist in Hebrew and English). */
function nl_drop_tpl_x( $f, $lang ) {
	$lang  = $lang === 'fr' ? 'fr' : 'ru';
	$ru    = $lang === 'ru';
	$deal  = ( $f['listing_type'] ?? '' ) === 'rent' ? 'rent' : 'sale';
	$area  = nl_drop_fx( $f, 'area', $lang );
	$city  = nl_drop_fx( $f, 'city', $lang );
	if ( $area === '' ) { $area = $city; }
	$type  = ! empty( $f['property_type'] ) ? $f['property_type'] : 'apartment';
	$rooms = ! empty( $f['rooms'] ) ? nl_drop_fmt_num( $f['rooms'], $lang ) : '';
	$rw    = ! empty( $f['rooms'] ) ? nl_drop_rooms_word( $f['rooms'], $lang ) : '';
	$tl    = nl_drop_type_label( $type, $lang );
	$sqm   = nl_drop_t( $lang, 'sqm' );
	$n     = function ( $x ) use ( $lang ) { return nl_drop_fmt_int( $x, $lang ); };
	$lc    = function ( $s ) { return function_exists( 'mb_strtolower' ) ? mb_strtolower( mb_substr( $s, 0, 1 ) ) . mb_substr( $s, 1 ) : $s; };
	if ( $rooms === '' ) { $head = $tl; }
	elseif ( $ru ) { $head = $type === 'apartment' ? $rooms . '-комнатная квартира' : $tl . ', ' . $rooms . ' ' . $rw; }
	else { $head = $tl . ' ' . $rooms . ' ' . $rw; }
	$rare  = '';
	if ( ! empty( $f['balcony_sqm'] ) ) { $rare = $ru ? ' с балконом ' . $n( $f['balcony_sqm'] ) . ' ' . $sqm : ' avec balcon de ' . $n( $f['balcony_sqm'] ) . ' ' . $sqm; }
	elseif ( ! empty( $f['garden_sqm'] ) && $type !== 'garden' ) { $rare = $ru ? ' с садом ' . $n( $f['garden_sqm'] ) . ' ' . $sqm : ' avec jardin de ' . $n( $f['garden_sqm'] ) . ' ' . $sqm; }
	$bits  = array();
	if ( ! empty( $f['size_sqm'] ) ) { $bits[] = $rooms !== '' ? ( $ru ? $rooms . ' ' . $rw . ', ' . $n( $f['size_sqm'] ) . ' ' . $sqm : $rooms . ' ' . $rw . ' sur ' . $n( $f['size_sqm'] ) . ' ' . $sqm ) : $n( $f['size_sqm'] ) . ' ' . $sqm; }
	elseif ( $rooms !== '' ) { $bits[] = $rooms . ' ' . $rw; }
	if ( ! empty( $f['balcony_sqm'] ) ) { $bits[] = $ru ? 'балкон ' . $n( $f['balcony_sqm'] ) . ' ' . $sqm : 'balcon de ' . $n( $f['balcony_sqm'] ) . ' ' . $sqm; }
	$floor = '';
	if ( isset( $f['floor'] ) && $f['floor'] !== null ) {
		if ( (int) $f['floor'] === 0 ) { $floor = $ru ? 'партер' : 'rez-de-chaussée'; }
		else { $floor = $ru ? 'этаж ' . (int) $f['floor'] . ( ! empty( $f['total_floors'] ) ? ' из ' . (int) $f['total_floors'] : '' ) : nl_drop_fr_floor( $f['floor'] ) . ' étage' . ( ! empty( $f['total_floors'] ) ? ' sur ' . (int) $f['total_floors'] : '' ); }
		$bits[] = $floor;
	}
	$park = '';
	if ( ! empty( $f['parking_count'] ) && $f['parking_count'] > 1 ) { $park = (int) $f['parking_count'] . ' ' . nl_drop_parking_word( $f['parking_count'], $lang ); }
	elseif ( ! empty( $f['parking'] ) || ! empty( $f['parking_count'] ) ) { $park = $ru ? 'парковка' : 'parking'; }
	if ( $park !== '' ) { $bits[] = $park; }
	if ( ! empty( $f['storage'] ) ) { $bits[] = $ru ? 'кладовая' : 'cave'; }
	if ( ! empty( $f['protected_room'] ) ) { $bits[] = 'мамад'; if ( ! $ru ) { array_pop( $bits ); $bits[] = 'mamad'; } }
	$place = trim( $area . ( $city !== '' && $city !== $area ? ', ' . $city : '' ) );
	$dek   = ( $place !== '' ? $place . ( $ru ? ': ' : ' : ' ) : '' ) . implode( ', ', $bits ) . '.';
	if ( ! empty( $f['price'] ) ) { $dek .= ' {{PRICE}}' . ( $deal === 'rent' ? ( $ru ? ' в месяц' : ' par mois' ) : '' ) . '.'; }
	$story = array( ( $place !== '' ? $place . ( $ru ? ': ' : ' : ' ) : '' ) . implode( ', ', $bits ) . '.' );
	$entry = nl_drop_fx( $f, 'entry', $lang );
	$more  = array();
	if ( ! empty( $f['condition'] ) ) { $more[] = nl_drop_t( $lang, 'f_condition' ) . ( $ru ? ': ' : ' : ' ) . $lc( nl_drop_t( $lang, 'c_' . $f['condition'] ) ); }
	if ( $entry !== '' ) { $more[] = nl_drop_t( $lang, 'f_entry' ) . ( $ru ? ': ' : ' : ' ) . $entry; }
	if ( ! empty( $f['price'] ) ) { $more[] = nl_drop_t( $lang, 'price_' . $deal ) . ( $ru ? ': ' : ' : ' ) . '{{PRICE}}'; }
	if ( $more ) { $story[] = implode( '. ', $more ) . '.'; }
	$feat = array();
	if ( ! empty( $f['size_sqm'] ) ) { $feat[] = array( $n( $f['size_sqm'] ) . ' ' . $sqm, $rooms !== '' ? $rooms . ' ' . $rw : '' ); }
	if ( ! empty( $f['balcony_sqm'] ) ) { $feat[] = array( $ru ? 'Балкон ' . $n( $f['balcony_sqm'] ) . ' ' . $sqm : 'Balcon de ' . $n( $f['balcony_sqm'] ) . ' ' . $sqm, '' ); }
	if ( $floor !== '' ) { $feat[] = array( function_exists( 'mb_strtoupper' ) ? mb_strtoupper( mb_substr( $floor, 0, 1 ) ) . mb_substr( $floor, 1 ) : $floor, ! empty( $f['elevator'] ) ? ( $ru ? 'с лифтом' : 'avec ascenseur' ) : '' ); }
	if ( $park !== '' || ! empty( $f['storage'] ) ) {
		$ps = trim( ( $park !== '' ? $park : '' ) . ( ! empty( $f['storage'] ) ? ( $park !== '' ? ( $ru ? ' и кладовая' : ' et cave' ) : ( $ru ? 'кладовая' : 'cave' ) ) : '' ) );
		$feat[] = array( function_exists( 'mb_strtoupper' ) ? mb_strtoupper( mb_substr( $ps, 0, 1 ) ) . mb_substr( $ps, 1 ) : $ps, '' );
	}
	if ( ! empty( $f['protected_room'] ) ) { $feat[] = array( $ru ? 'Мамад' : 'Mamad', $ru ? 'защищённая комната в квартире' : 'pièce sécurisée dans l’appartement' ); }
	if ( $entry !== '' ) { $feat[] = array( nl_drop_t( $lang, 'f_entry' ) . ( $ru ? ': ' : ' : ' ) . $entry, '' ); }
	$hi = array();
	if ( ! empty( $f['storage'] ) ) { $hi[] = $ru ? 'Кладовая' : 'Cave'; }
	if ( ! empty( $f['elevator'] ) ) { $hi[] = $ru ? 'Лифт' : 'Ascenseur'; }
	if ( $park !== '' ) { $hi[] = function_exists( 'mb_strtoupper' ) ? mb_strtoupper( mb_substr( $park, 0, 1 ) ) . mb_substr( $park, 1 ) : $park; }
	$chips = array_values( array_filter( array( ! empty( $f['size_sqm'] ) ? $n( $f['size_sqm'] ) . ' ' . $sqm : '', $entry !== '' ? nl_drop_t( $lang, 'f_entry' ) . ( $ru ? ': ' : ' : ' ) . $entry : ( ! empty( $f['protected_room'] ) ? ( $ru ? 'Мамад' : 'Mamad' ) : '' ) ) ) );
	$seo_t = $ru ? nl_drop_t( 'ru', $deal ) . ': ' . $lc( $head ) . ( $area !== '' ? ', ' . $area : '' ) : $head . ( $deal === 'rent' ? ' à louer' : ' à vendre' ) . ( $area !== '' ? ', ' . $area : '' );
	return array(
		'title'      => $head . $rare . ( $area !== '' ? ', ' . $area : '' ),
		'card_title' => $head . $rare,
		'dek'        => $dek,
		'story_h2'   => $head . ( $area !== '' ? ( $ru ? ', ' : ', ' ) . $area : '' ),
		'story'      => $story,
		'features'   => array_slice( $feat, 0, 6 ),
		'chips'      => array_slice( $chips, 0, 2 ),
		'card_hi'    => array_slice( $hi, 0, 3 ),
		'seo_title'  => $seo_t,
		'seo_desc'   => function_exists( 'mb_substr' ) ? mb_substr( $dek, 0, 155 ) : $dek,
	);
}

/* =====================================================================================================
 * Latin slug: area, type, rooms, deal. No word twice. Never Hebrew.
 * ===================================================================================================== */
function nl_drop_slug( $f, $b ) {
	$latin = function ( $s ) {
		$s = strtolower( remove_accents( (string) $s ) );
		$s = preg_replace( '/[^a-z0-9]+/', '-', $s );
		return trim( $s, '-' );
	};
	$area  = $latin( $f['area_en'] ?? '' );
	if ( $area === '' ) { $area = $latin( $f['city_en'] ?? '' ); }
	$words = array();
	if ( $area !== '' ) { $words[] = $area; }
	$type = array( 'penthouse' => 'penthouse', 'mini_penthouse' => 'mini-penthouse', 'garden' => 'garden-apartment', 'duplex' => 'duplex', 'villa' => 'villa', 'cottage' => 'cottage', 'studio' => 'studio' );
	if ( isset( $type[ $f['property_type'] ?? '' ] ) ) { $words[] = $type[ $f['property_type'] ]; }
	if ( ! empty( $f['rooms'] ) ) { $words[] = str_replace( '.', '-', nl_drop_fmt_num( $f['rooms'] ) ) . '-rooms'; }
	$words[] = ( $f['listing_type'] ?? '' ) === 'rent' ? 'for-rent' : 'for-sale';
	$seen = array();
	$out  = array();
	foreach ( explode( '-', implode( '-', $words ) ) as $w ) {
		if ( $w === '' ) { continue; }
		if ( ! ctype_digit( $w ) && isset( $seen[ $w ] ) ) { continue; }
		$seen[ $w ] = 1;
		$out[]      = $w;
	}
	$slug = implode( '-', $out );
	if ( count( $out ) < 3 ) { $slug = 'property-' . $slug; }
	$base = $slug;
	for ( $i = 2; $i < 60; $i++ ) {
		$taken = get_page_by_path( $slug, OBJECT, 'nadlan_property' );
		foreach ( array( 'en', 'ru', 'fr' ) as $l ) {
			if ( $taken ) { break; }
			$sid = (int) ( $b[ 'site_' . $l ] ?? 0 );
			if ( $sid ) { $taken = get_page_by_path( get_page_uri( $sid ) . '/' . $slug, OBJECT, 'page' ); }
		}
		if ( ! $taken ) { break; }
		$slug = $base . '-' . $i;
	}
	return $slug;
}

/* =====================================================================================================
 * The listing page (same design and classes as the approved broker listing pages)
 * 1.1.3 (24.9.2026, HAD-251): the lines that hid the portal's own layers (.nlps-*, .nlcard, everything after
 * article.nlx, the floating pills, the Yoast breadcrumb, the featured image) are gone. A listing with an owner
 * (nl_broker_id, or nl_owner=1 for private owners) no longer gets those layers printed at all:
 * plugins/nadlan-config/inc/property-owner.php, server side.
 * ===================================================================================================== */
function nl_drop_listing_css() {
	return <<<'NLXCSS'
.nlx{
  --nlx-paper:#F7F6F2; --nlx-surf:#FFFFFF; --nlx-ink:#14212B; --nlx-ink2:#3B4753; --nlx-mute:#6B7680;
  --nlx-line:#E3E1DA; --nlx-sea:#2F6F86; --nlx-seah:#255C70; --nlx-deep:#1F4B5C; --nlx-sand:#EEE9DD; --nlx-mist:#CFE3EA;
  --nlx-on-deep:#F7F6F2; --nlx-on-deep-2:rgba(247,246,242,.74); --nlx-on-deep-line:rgba(247,246,242,.18); --nlx-on-deep-fill:rgba(247,246,242,.08);
  --nlx-serif:'Noto Serif Hebrew','Noto Serif','David Libre',Georgia,serif;
  --nlx-sans:Assistant,'Segoe UI',Arial,sans-serif;
  --nlx-r:8px; --nlx-r-lg:22px;
  --nlx-shadow:0 8px 24px rgba(17,17,15,.07),0 2px 6px rgba(17,17,15,.04);
  color:var(--nlx-ink); font-family:var(--nlx-sans); font-size:17px; line-height:1.65;
  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;
}
.nlx *,.nlx *::before,.nlx *::after{box-sizing:border-box}
.nlx :where(h1,h2,h3,h4,p,ul,ol,dl,dd,figure,table){margin:0;padding:0}
.nlx :where(ul,ol){list-style:none}
.nlx img{max-width:100%;height:auto;display:block}
.nlx a{color:var(--nlx-sea);text-decoration-thickness:1px;text-underline-offset:3px}
.nlx a:hover{color:var(--nlx-seah)}
.nlx :focus-visible{outline:2px solid var(--nlx-sea);outline-offset:3px;border-radius:4px}
.nlx .nlx-num{font-variant-numeric:tabular-nums lining-nums;font-feature-settings:"tnum" 1,"lnum" 1;direction:ltr;unicode-bidi:isolate;display:inline-block}
.nlx .nlx-wrap{max-width:1240px;margin-inline:auto;padding-inline:clamp(16px,3vw,32px)}
.nlx .nlx-sr{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.nlx.nlx .nlx-title,.nlx.nlx .nlx-h2,.nlx.nlx .nlx-h3,.nlx.nlx .nlx-serif{font-family:var(--nlx-serif)!important;font-weight:600!important;color:var(--nlx-ink)!important;letter-spacing:-.005em;text-wrap:balance}
.nlx.nlx .nlx-title{font-size:clamp(34px,4.4vw,56px);line-height:1.12}
.nlx.nlx .nlx-h2{font-size:clamp(26px,2.6vw,34px);line-height:1.2}
.nlx.nlx .nlx-h3{font-size:21px;line-height:1.3}
.nlx .nlx-kicker,.nlx .nlx-eyebrow{font-family:var(--nlx-sans)!important;font-size:13px;font-weight:700;letter-spacing:.04em;color:var(--nlx-sea);margin:0}
.nlx[lang="en"] .nlx-kicker,.nlx[lang="en"] .nlx-eyebrow{text-transform:uppercase;letter-spacing:.09em;font-size:12px}
.nlx.nlx .nlx-dek{font-family:var(--nlx-serif)!important;font-weight:500;font-size:clamp(19px,1.7vw,23px);line-height:1.55;color:var(--nlx-ink2);max-width:40ch}
.nlx .nlx-muted{color:var(--nlx-mute)}
.nlx .nlx-small{font-size:14px;line-height:1.55}
.nlx .nlx-chips{display:flex;flex-wrap:wrap;gap:8px}
.nlx .nlx-chip{display:inline-flex;align-items:center;gap:6px;padding:5px 12px;border-radius:999px;background:var(--nlx-sand);border:1px solid var(--nlx-line);color:var(--nlx-deep);font-size:14px;font-weight:600;line-height:1.3}
.nlx .nlx-chip--sea{background:var(--nlx-surf);border-color:var(--nlx-sea);color:var(--nlx-sea)}
.nlx .nlx-tag{display:inline-block;padding:1px 7px;border-radius:999px;font-size:11.5px;font-weight:700;line-height:1.6;letter-spacing:.02em;white-space:nowrap;vertical-align:middle;border:1px solid var(--nlx-line);color:var(--nlx-mute);background:var(--nlx-surf)}
.nlx .nlx-tag--broker{color:#5C5347;background:#F4EFE6;border-color:#E2D8C6}
.nlx .nlx-tag--calc{color:var(--nlx-ink2);background:var(--nlx-paper)}
.nlx .nlx-tag--src{color:var(--nlx-sea);border-color:#BFD6DE;background:#F2F8FA}
.nlx .nlx-tag--tx{color:#FFFFFF;background:var(--nlx-deep);border-color:var(--nlx-deep)}
.nlx sup.nlx-fn{font-size:11px;font-weight:700;margin-inline-start:2px;vertical-align:super;line-height:0}
.nlx sup.nlx-fn a{text-decoration:none}
.nlx .nlx-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:46px;padding:10px 20px;border-radius:999px;background:var(--nlx-sea);color:#fff!important;font-weight:700;font-size:16px;text-decoration:none!important;border:1px solid var(--nlx-sea);transition:background .15s ease}
.nlx .nlx-btn:hover{background:var(--nlx-seah);border-color:var(--nlx-seah)}
.nlx .nlx-btn--ghost{background:var(--nlx-surf);color:var(--nlx-deep)!important;border-color:var(--nlx-line)}
.nlx .nlx-btn--ghost:hover{background:var(--nlx-sand);border-color:var(--nlx-line)}
.nlx .nlx-btn svg{width:18px;height:18px;flex:none}
.nlx .nlx-mast{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:clamp(24px,4vw,56px);align-items:end;padding-block:clamp(24px,4vw,48px) clamp(20px,3vw,36px)}
.nlx .nlx-mast-copy{display:grid;gap:18px;align-content:end}
.nlx .nlx-plate{position:relative;aspect-ratio:4/3;max-width:100%;border-radius:var(--nlx-r);overflow:hidden;background:var(--nlx-sand);border:1px solid var(--nlx-line)}
.nlx .nlx-plate--rent{background:#E4EEF1}
.nlx .nlx-plate svg{position:absolute;inset:0;width:100%;height:100%}
.nlx .nlx-plate figcaption{position:absolute;inset-inline:14px;bottom:12px;font-size:13px;color:var(--nlx-ink2);background:rgba(255,255,255,.82);padding:6px 10px;border-radius:6px;line-height:1.4;max-width:calc(100% - 28px)}
.nlx .nlx-plate-name{position:absolute;inset-inline-start:22px;top:18px;font-family:var(--nlx-serif)!important;font-weight:600;font-size:clamp(22px,2.4vw,30px);color:var(--nlx-deep);line-height:1.2;max-width:70%}
.nlx .nlx-facts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-block:1px solid var(--nlx-line)}
.nlx .nlx-fact{padding:18px 16px 16px;display:grid;gap:4px;align-content:start;border-inline-start:1px solid var(--nlx-line)}
.nlx .nlx-fact:first-child{border-inline-start:0}
.nlx .nlx-fact dt{font-size:13px;color:var(--nlx-mute);font-weight:600}
.nlx .nlx-fact dd{font-size:23px;font-weight:700;line-height:1.25;color:var(--nlx-ink)}
.nlx .nlx-fact dd .nlx-unit{font-size:15px;font-weight:600;color:var(--nlx-ink2);margin-inline-start:4px}
.nlx .nlx-fact .nlx-tag{justify-self:start}
.nlx .nlx-facts-note{display:flex;align-items:center;gap:8px;font-size:13.5px;color:var(--nlx-mute);padding-top:10px}
.nlx .nlx-money{white-space:nowrap}
.nlx .nlx-item-title{font-weight:600}
.nlx .nlx-spec-group h3 .nlx-tag{margin-inline-start:8px;letter-spacing:0}
.nlx .nlx-layout{display:grid;grid-template-columns:minmax(0,1fr) 352px;gap:clamp(32px,4.5vw,64px);align-items:start;padding-block:clamp(28px,4vw,48px)}
.nlx .nlx-main{min-width:0;display:grid;grid-template-columns:minmax(0,1fr);gap:0}
.nlx .nlx-main>*,.nlx .nlx-sec>*,.nlx .nlx-band>*,.nlx .nlx-band-grid>*,.nlx .nlx-two>*,.nlx .nlx-rail>*{min-width:0}
.nlx .nlx-rail{position:sticky;top:calc(var(--nlx-header-offset,96px) + env(safe-area-inset-top,0px));display:grid;gap:16px}
.nlx .nlx-card{background:var(--nlx-surf);border:1px solid var(--nlx-line);border-radius:var(--nlx-r);padding:22px}
.nlx .nlx-price-card{box-shadow:var(--nlx-shadow);display:grid;gap:14px}
.nlx .nlx-price-lbl{font-size:13px;font-weight:700;color:var(--nlx-mute);letter-spacing:.02em}
.nlx .nlx-price{font-size:clamp(30px,3vw,38px);font-weight:700;line-height:1.1;color:var(--nlx-ink)}
.nlx .nlx-price-sub{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:14px;color:var(--nlx-ink2)}
.nlx .nlx-price-rows{display:grid;gap:8px;border-top:1px solid var(--nlx-line);padding-top:14px}
.nlx .nlx-price-rows div{display:flex;justify-content:space-between;gap:12px;font-size:15px}
.nlx .nlx-price-rows dt{color:var(--nlx-mute)}
.nlx .nlx-price-rows dd{font-weight:700;text-align:end}
.nlx .nlx-cta{display:grid;gap:10px}
.nlx .nlx-agent-mini{display:grid;grid-template-columns:44px 1fr;gap:12px;align-items:center;font-size:14px;line-height:1.45}
.nlx .nlx-monogram{width:44px;height:44px;border-radius:50%;background:var(--nlx-deep);color:var(--nlx-on-deep);display:grid;place-items:center;font-family:var(--nlx-serif)!important;font-weight:600;font-size:18px}
.nlx .nlx-sec{padding-block:clamp(36px,4.5vw,56px);border-top:1px solid var(--nlx-line);display:grid;gap:22px;scroll-margin-top:96px}
.nlx .nlx-sec:first-child{border-top:0;padding-top:0}
.nlx .nlx-sec-head{display:grid;gap:8px;max-width:62ch}
.nlx .nlx-lead{font-size:18px;color:var(--nlx-ink2);max-width:64ch}
.nlx .nlx-prose{display:grid;gap:16px;max-width:66ch}
.nlx .nlx-prose p{font-size:18px;line-height:1.8;color:var(--nlx-ink)}
.nlx .nlx-toc{display:flex;flex-wrap:wrap;gap:8px 18px;font-size:14.5px;font-weight:600;padding-block:14px;border-bottom:1px solid var(--nlx-line)}
.nlx .nlx-toc a{color:var(--nlx-ink2);text-decoration:none}
.nlx .nlx-toc a:hover{color:var(--nlx-sea)}
.nlx .nlx-features{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 32px}
.nlx .nlx-features li{padding:14px 0;border-top:1px solid var(--nlx-line);display:grid;gap:2px}
.nlx .nlx-features b{font-weight:700;color:var(--nlx-ink)}
.nlx .nlx-features span{color:var(--nlx-ink2);font-size:16px}
.nlx .nlx-spec{display:grid;gap:28px}
.nlx .nlx-spec-group{display:grid;gap:0}
.nlx .nlx-spec-group h3{font-family:var(--nlx-sans)!important;font-size:14px!important;font-weight:700!important;color:var(--nlx-mute)!important;letter-spacing:.03em;padding-bottom:8px}
.nlx .nlx-rows{display:grid}
.nlx .nlx-row{display:grid;grid-template-columns:minmax(120px,.8fr) minmax(0,1.6fr) auto;gap:6px 18px;padding:12px 0;border-top:1px solid var(--nlx-line);align-items:baseline}
.nlx .nlx-row dt{color:var(--nlx-ink2);font-weight:600;font-size:15.5px}
.nlx .nlx-row dd{color:var(--nlx-ink);font-size:16px}
.nlx .nlx-row .nlx-row-tag{justify-self:end}
.nlx .nlx-dist{display:grid}
.nlx .nlx-dist li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 16px;padding:12px 0;border-top:1px solid var(--nlx-line);align-items:center}
.nlx .nlx-dist .nlx-dist-name{font-weight:600}
.nlx .nlx-dist .nlx-dist-val{font-weight:700;text-align:end}
.nlx .nlx-dist .nlx-meter{grid-column:1/-1;height:4px;border-radius:4px;background:var(--nlx-sand);overflow:hidden}
.nlx .nlx-dist .nlx-meter i{display:block;height:100%;background:var(--nlx-sea);border-radius:4px}
.nlx .nlx-dist .nlx-dist-note{grid-column:1/-1;font-size:13.5px;color:var(--nlx-mute)}
.nlx .nlx-items{display:grid}
.nlx .nlx-item{padding:14px 0;border-top:1px solid var(--nlx-line);display:grid;gap:5px}
.nlx .nlx-item-top{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:6px 14px}
.nlx .nlx-item-title{font-weight:700;color:var(--nlx-ink)}
.nlx .nlx-item p{font-size:15.5px;color:var(--nlx-ink2)}
.nlx .nlx-two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 40px}
.nlx .nlx-subhead{font-family:var(--nlx-sans)!important;font-size:15px!important;font-weight:700!important;color:var(--nlx-ink)!important;margin-bottom:4px}
.nlx .nlx-band{background:var(--nlx-deep);color:var(--nlx-on-deep);border-radius:var(--nlx-r-lg);padding:clamp(24px,4vw,48px);display:grid;gap:28px;margin-block:clamp(8px,2vw,16px)}
.nlx.nlx .nlx-band .nlx-h2,.nlx.nlx .nlx-band .nlx-h3,.nlx.nlx .nlx-band h2,.nlx.nlx .nlx-band h3{color:var(--nlx-on-deep)!important}
.nlx .nlx-band .nlx-eyebrow{color:var(--nlx-mist)}
.nlx .nlx-band p,.nlx .nlx-band li,.nlx .nlx-band dt,.nlx .nlx-band dd,.nlx .nlx-band span,.nlx .nlx-band td,.nlx .nlx-band th,.nlx .nlx-band small,.nlx .nlx-band label{color:var(--nlx-on-deep)}
.nlx .nlx-band .nlx-muted,.nlx .nlx-band .nlx-small{color:var(--nlx-on-deep-2)!important}
.nlx .nlx-band a{color:var(--nlx-mist)}
.nlx .nlx-band .nlx-tag{background:transparent;border-color:var(--nlx-on-deep-line);color:var(--nlx-on-deep-2)}
.nlx .nlx-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--nlx-on-deep-line);border:1px solid var(--nlx-on-deep-line);border-radius:var(--nlx-r);overflow:hidden}
.nlx .nlx-kpi{background:var(--nlx-deep);padding:18px;display:grid;gap:6px;align-content:start}
.nlx .nlx-kpi dt{font-size:13px;color:var(--nlx-on-deep-2)!important;font-weight:600}
.nlx .nlx-kpi dd{font-size:clamp(22px,2.2vw,28px);font-weight:700;line-height:1.15}
.nlx .nlx-kpi .nlx-small{font-size:13px}
.nlx .nlx-ledger{display:grid}
.nlx .nlx-ledger div{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 16px;padding:11px 0;border-top:1px solid var(--nlx-on-deep-line);align-items:baseline}
.nlx .nlx-ledger dt{font-size:15.5px}
.nlx .nlx-ledger dd{font-weight:700;text-align:end;font-size:16.5px}
.nlx .nlx-ledger .nlx-ledger-note{grid-column:1/-1;font-size:13px;color:var(--nlx-on-deep-2)!important}
.nlx .nlx-band-grid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:clamp(24px,4vw,48px)}
.nlx .nlx-seg{display:grid;gap:14px}
.nlx .nlx-seg > input{position:absolute;opacity:0;pointer-events:none}
.nlx .nlx-seg-labels{display:flex;flex-wrap:wrap;gap:8px}
.nlx .nlx-seg-labels label{cursor:pointer;padding:8px 14px;border-radius:999px;border:1px solid var(--nlx-on-deep-line);font-size:14.5px;font-weight:700;color:var(--nlx-on-deep);background:transparent;line-height:1.3}
.nlx .nlx-seg-panel{display:none}
.nlx .nlx-seg > input:nth-of-type(1):checked ~ .nlx-seg-labels label:nth-of-type(1),
.nlx .nlx-seg > input:nth-of-type(2):checked ~ .nlx-seg-labels label:nth-of-type(2),
.nlx .nlx-seg > input:nth-of-type(3):checked ~ .nlx-seg-labels label:nth-of-type(3),
.nlx .nlx-seg > input:nth-of-type(4):checked ~ .nlx-seg-labels label:nth-of-type(4){background:var(--nlx-on-deep);color:var(--nlx-deep);border-color:var(--nlx-on-deep)}
.nlx .nlx-seg > input:nth-of-type(1):checked ~ .nlx-seg-panels .nlx-seg-panel:nth-of-type(1),
.nlx .nlx-seg > input:nth-of-type(2):checked ~ .nlx-seg-panels .nlx-seg-panel:nth-of-type(2),
.nlx .nlx-seg > input:nth-of-type(3):checked ~ .nlx-seg-panels .nlx-seg-panel:nth-of-type(3),
.nlx .nlx-seg > input:nth-of-type(4):checked ~ .nlx-seg-panels .nlx-seg-panel:nth-of-type(4){display:grid}
.nlx .nlx-seg > input:focus-visible ~ .nlx-seg-labels label{outline:1px dashed var(--nlx-on-deep-line)}
.nlx .nlx-bars{display:grid;gap:12px;align-content:start}
.nlx .nlx-seg{align-content:start}
.nlx .nlx-kpis--1{grid-template-columns:minmax(0,1fr)}
.nlx .nlx-kpis--2{grid-template-columns:repeat(2,minmax(0,1fr))}
.nlx .nlx-kpis--3,.nlx .nlx-kpis--6{grid-template-columns:repeat(3,minmax(0,1fr))}
.nlx .nlx-kpis--wide{grid-template-columns:repeat(2,minmax(0,1fr))}
.nlx .nlx-bar{display:grid;gap:6px}
.nlx .nlx-bar-top{display:flex;justify-content:space-between;align-items:baseline;gap:12px;font-size:14.5px}
.nlx .nlx-bar-top>span:last-child{white-space:nowrap}
.nlx .nlx-bar-track{height:10px;border-radius:6px;background:var(--nlx-on-deep-fill);overflow:hidden}
.nlx .nlx-bar-track i{display:block;height:100%;border-radius:6px;background:var(--nlx-on-deep-2)}
.nlx .nlx-bar--this .nlx-bar-track i{background:var(--nlx-mist)}
.nlx .nlx-bar--this .nlx-bar-top{font-weight:700}
.nlx .nlx-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--nlx-line);border-radius:var(--nlx-r);background:var(--nlx-surf)}
.nlx table.nlx-table{width:100%;border-collapse:collapse;font-size:15px;min-width:640px}
.nlx .nlx-table th{font-size:12.5px;font-weight:700;color:var(--nlx-mute);text-align:start;padding:11px 14px;background:var(--nlx-paper);border-bottom:1px solid var(--nlx-line);white-space:nowrap}
.nlx .nlx-table td{padding:11px 14px;border-bottom:1px solid var(--nlx-line);vertical-align:top;color:var(--nlx-ink)}
.nlx .nlx-table tr:last-child td{border-bottom:0}
.nlx .nlx-table td.nlx-r{text-align:end;white-space:nowrap}
.nlx .nlx-table caption{caption-side:bottom;text-align:start;padding:10px 14px;font-size:13px;color:var(--nlx-mute)}
.nlx .nlx-stats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 32px}
.nlx .nlx-stats div{padding:12px 0;border-top:1px solid var(--nlx-line);display:grid;gap:2px}
.nlx .nlx-stats dt{font-size:14px;color:var(--nlx-mute)}
.nlx .nlx-stats dd{font-weight:600;line-height:1.5}
.nlx .nlx-checks{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 36px;counter-reset:nlxq}
.nlx .nlx-checks li{padding:12px 0;border-top:1px solid var(--nlx-line);display:grid;grid-template-columns:28px 1fr;gap:10px;font-size:15.5px;color:var(--nlx-ink2)}
.nlx .nlx-checks li::before{content:"";width:18px;height:18px;margin-top:3px;border:1.5px solid var(--nlx-sea);border-radius:4px}
.nlx .nlx-faq{display:grid}
.nlx .nlx-faq details{border-top:1px solid var(--nlx-line)}
.nlx .nlx-faq summary{cursor:pointer;list-style:none;padding:16px 0;font-weight:700;font-size:17px;display:flex;justify-content:space-between;gap:16px}
.nlx .nlx-faq summary::-webkit-details-marker{display:none}
.nlx .nlx-faq summary::after{content:"+";font-weight:400;color:var(--nlx-sea);font-size:22px;line-height:1}
.nlx .nlx-faq details[open] summary::after{content:"\2212"}
.nlx .nlx-faq .nlx-faq-a{padding:0 0 18px;color:var(--nlx-ink2);max-width:66ch}
.nlx .nlx-agent{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:18px 24px;align-items:center;background:var(--nlx-sand);border:1px solid var(--nlx-line);border-radius:var(--nlx-r-lg);padding:clamp(20px,3vw,32px)}
.nlx .nlx-agent .nlx-monogram{width:64px;height:64px;font-size:26px}
.nlx .nlx-agent-name{font-family:var(--nlx-serif)!important;font-weight:600;font-size:24px;line-height:1.25}
.nlx .nlx-agent .nlx-cta{grid-auto-flow:column}
.nlx .nlx-sources{display:grid;gap:10px;font-size:13.5px;color:var(--nlx-ink2)}
.nlx .nlx-sources ol{list-style:decimal;padding-inline-start:22px;display:grid;gap:6px}
.nlx .nlx-sources li{padding-inline-start:4px;overflow-wrap:anywhere}
.nlx .nlx-legend{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;font-size:13.5px;color:var(--nlx-mute)}
.nlx .nlx-disclaimer{font-size:13.5px;line-height:1.65;color:var(--nlx-mute);max-width:90ch}
.nlx .nlx-mbar{display:none}
@media (max-width:1080px){
  .nlx .nlx-layout{grid-template-columns:minmax(0,1fr)}
  .nlx .nlx-rail{position:static;order:-1;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
  .nlx .nlx-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}
  .nlx .nlx-band-grid{grid-template-columns:minmax(0,1fr)}
}
@media (max-width:760px){
  .nlx{font-size:16.5px}
  .nlx .nlx-mast{grid-template-columns:minmax(0,1fr);align-items:start}
  .nlx .nlx-plate{aspect-ratio:4/3}
  .nlx .nlx-facts{grid-template-columns:repeat(2,minmax(0,1fr))}
  .nlx .nlx-fact:nth-child(odd){border-inline-start:0}
  .nlx .nlx-fact{border-top:1px solid var(--nlx-line)}
  .nlx .nlx-fact:nth-child(-n+2){border-top:0}
  .nlx .nlx-features,.nlx .nlx-two,.nlx .nlx-checks,.nlx .nlx-stats{grid-template-columns:minmax(0,1fr)}
  .nlx .nlx-row{grid-template-columns:minmax(0,1fr) auto}
  .nlx .nlx-row dd{grid-column:1/-1;grid-row:2}
  .nlx .nlx-row .nlx-row-tag{grid-column:2;grid-row:1}
  .nlx .nlx-kpis{grid-template-columns:minmax(0,1fr)}
  .nlx .nlx-agent{grid-template-columns:auto minmax(0,1fr)}
  .nlx .nlx-agent .nlx-cta{grid-column:1/-1;grid-auto-flow:row}
  .nlx .nlx-prose p{font-size:17px}
  .nlx .nlx-mbar{display:grid;grid-template-columns:1fr 1fr;gap:10px;position:sticky;bottom:0;z-index:20;padding:10px 0 calc(10px + env(safe-area-inset-bottom,0px));background:linear-gradient(to top,var(--nlx-paper) 72%,rgba(247,246,242,0))}
}
@media (prefers-reduced-motion:reduce){.nlx *{transition:none!important;scroll-behavior:auto!important}}
@media print{.nlx .nlx-rail,.nlx .nlx-mbar,.nlx .nlx-cta{display:none!important}.nlx .nlx-band{background:#fff;color:#000;border:1px solid #999}}
.nlx.nlx-cat{padding-block:clamp(24px,4vw,48px)}
.nlx .nlx-cat-head{display:grid;gap:8px;margin-block-end:clamp(20px,3vw,32px);max-width:62ch}
.nlx.nlx .nlx-cat-title{font-family:var(--nlx-serif)!important;font-weight:600!important;font-size:clamp(28px,3.4vw,40px)!important;line-height:1.2!important;color:var(--nlx-ink)!important;margin:0!important;text-wrap:balance}
.nlx .nlx-cat-lead{margin:0;color:var(--nlx-ink2)}
.nlx .nlx-cat-group{margin-block:clamp(20px,3vw,32px) 12px;font-size:13px;font-weight:700;letter-spacing:.05em;color:var(--nlx-mute)}
.nlx .nlx-cat-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:18px}
.nlx a.nlx-card-l{display:grid;grid-template-rows:auto auto 1fr auto;gap:10px;background:var(--nlx-surf);border:1px solid var(--nlx-line);border-radius:var(--nlx-r);padding:20px 22px 16px;text-decoration:none!important;color:inherit!important;transition:border-color .2s ease,box-shadow .2s ease}
.nlx a.nlx-card-l:hover{border-color:var(--nlx-sea);box-shadow:var(--nlx-shadow)}
.nlx a.nlx-card-l:focus-visible{outline:2px solid var(--nlx-sea);outline-offset:3px}
.nlx .nlx-card-kicker{font-size:12.5px;font-weight:700;letter-spacing:.04em;color:var(--nlx-sea)}
.nlx.nlx .nlx-card-title{font-family:var(--nlx-serif)!important;font-weight:600!important;font-size:20px!important;line-height:1.35!important;color:var(--nlx-ink)!important;margin:0!important;text-wrap:balance}
.nlx .nlx-card-body{display:grid;gap:8px;align-content:start}
.nlx .nlx-card-price{font-size:22px;font-weight:700;line-height:1.2}
.nlx .nlx-card-price small{font-size:14px;font-weight:600;color:var(--nlx-mute)}
.nlx .nlx-card-specs{display:flex;flex-wrap:wrap;gap:2px 14px;margin:0;padding:0;list-style:none;font-size:14.5px;color:var(--nlx-ink2)}
.nlx .nlx-card-foot{display:flex;justify-content:space-between;gap:12px;border-top:1px solid var(--nlx-line);padding-top:10px;font-size:12.5px;color:var(--nlx-mute)}
.nlx .nlx-card-foot b{color:var(--nlx-sea);font-weight:700;white-space:nowrap}
.nlx .nlx-plate--photo{background:var(--nlx-deep)}
.nlx .nlx-plate--photo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;max-width:none}
.nlx .nlx-plate--photo .nlx-plate-name{color:#fff;text-shadow:0 1px 12px rgba(0,0,0,.45)}
.nlx .nlx-sec{scroll-margin-top:calc(var(--nlx-header-offset,96px) + 16px)}
.nlx .nlx-toc .nlx-home{font-weight:600;color:var(--nlx-sea,#2F6F86)}
.single-nadlan_property .entry-content.is-layout-constrained>*{max-width:none!important;margin-left:auto!important;margin-right:auto!important}
.nlx .nlx-wrap{max-width:1180px;margin-inline:auto;padding-inline:clamp(16px,3vw,28px)}
.nlx .nlx-plate--photo{background:var(--nlx-deep);aspect-ratio:var(--nlx-cover-ar,1.5);height:auto;max-height:78vh;position:relative;overflow:hidden}
.nlx .nlx-plate--photo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center;max-width:none}
.nlx .nlx-gallery{columns:3;column-gap:12px;margin:0}
.nlx .nlx-gallery figure{break-inside:avoid;margin:0 0 12px;border-radius:var(--nlx-r,8px);overflow:hidden;background:var(--nlx-sand,#EEE9DD)}
.nlx .nlx-gallery img{width:100%;height:auto;display:block}
.nlx .nlx-toc .nlx-lang{margin-inline-start:auto;font-weight:600}
@media (max-width:900px){.nlx .nlx-gallery{columns:2}}
@media (max-width:520px){.nlx .nlx-gallery{columns:1}}
NLXCSS;
}

function nl_drop_fill( $s, $f, $lang ) {
	$s = (string) $s;
	if ( strpos( $s, '{{PRICE}}' ) === false ) { return $s; }
	$deal = ( $f['listing_type'] ?? '' ) === 'rent' ? 'rent' : 'sale';
	$rep  = ! empty( $f['price'] ) ? nl_drop_price_text( $f['price'], $lang ) : nl_drop_t( $lang, 'ask_' . $deal );
	return str_replace( '{{PRICE}}', $rep, $s );
}

function nl_drop_nums_html( $s ) {
	return preg_replace_callback( '/(&#?[a-z0-9]+;)|(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)/iu', function ( $m ) {
		return $m[1] !== '' ? $m[1] : '<span class="nlx-num">' . $m[2] . '</span>';
	}, esc_html( (string) $s ) );
}

function nl_drop_wa_link( $b, $lang, $title ) {
	if ( empty( $b['wa'] ) ) { return ''; }
	$txt = sprintf( nl_drop_t( $lang, 'wa_text' ), nl_drop_name( $b, $lang ), $title );
	return 'https://wa.me/' . rawurlencode( $b['wa'] ) . '?text=' . rawurlencode( $txt );
}

/** Reg. 19(a): name, broker status and licence number on every marketing page. Owners are not brokers. */
function nl_drop_licence_line( $b, $lang ) {
	if ( ( $b['kind'] ?? 'broker' ) === 'owner' ) { return ''; }
	$brand = nl_drop_brand( $b, $lang );
	$lic   = $b['license'] !== '' ? nl_drop_t( $lang, $b['female'] ? 'lic_f' : 'lic_m' ) . ' ' . $b['license'] : '';
	return trim( implode( ' · ', array_filter( array( $brand, $lic ) ) ) );
}

/** A date each reader reads without the site's Hebrew month names. */
function nl_drop_date( $ts, $lang ) {
	$lang = nl_drop_L( $lang );
	if ( $lang === 'en' ) {
		$mon = array( 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' );
		return wp_date( 'j', $ts ) . ' ' . $mon[ (int) wp_date( 'n', $ts ) - 1 ] . ' ' . wp_date( 'Y', $ts );
	}
	if ( $lang === 'ru' ) { return wp_date( 'd.m.Y', $ts ); }
	if ( $lang === 'fr' ) { return wp_date( 'd/m/Y', $ts ); }
	return wp_date( 'j.n.Y', $ts );
}

/** Rooms, the floor and parking as the facts row and the cards print them, number first. */
function nl_drop_rooms_html( $n, $lang, $wrap ) {
	$lang = nl_drop_L( $lang );
	$num  = $wrap( nl_drop_fmt_num( $n, $lang ) );
	if ( $lang === 'he' || $lang === 'en' ) { return sprintf( esc_html( nl_drop_t( $lang, 'rooms_n' ) ), $num ); }
	return $num . ' ' . esc_html( nl_drop_rooms_word( $n, $lang ) );
}

function nl_drop_floor_html( $f, $lang, $wrap ) {
	$lang = nl_drop_L( $lang );
	if ( (int) $f['floor'] === 0 ) { return esc_html( nl_drop_t( $lang, 'ground' ) ); }
	if ( $lang === 'fr' ) {
		$fl = $wrap( nl_drop_fr_floor( $f['floor'] ) );
		return ! empty( $f['total_floors'] ) ? $fl . ' étage sur ' . $wrap( (int) $f['total_floors'] ) : $fl . ' étage';
	}
	return ! empty( $f['total_floors'] ) ? sprintf( esc_html( nl_drop_t( $lang, 'floor_of' ) ), $wrap( (int) $f['floor'] ), $wrap( (int) $f['total_floors'] ) ) : sprintf( esc_html( nl_drop_t( $lang, 'floor_n' ) ), $wrap( (int) $f['floor'] ) );
}

function nl_drop_parking_txt( $f, $lang ) {
	$lang = nl_drop_L( $lang );
	if ( ! empty( $f['parking_count'] ) && $f['parking_count'] > 1 ) {
		if ( $lang === 'he' || $lang === 'en' ) { return sprintf( nl_drop_t( $lang, 'parking_n' ), (int) $f['parking_count'] ); }
		return (int) $f['parking_count'] . ' ' . nl_drop_parking_word( $f['parking_count'], $lang );
	}
	return nl_drop_t( $lang, 'parking_1' );
}


/**
 * @param array $d id, facts, copy, photos[{id,url,w,h}], broker, url, alts (lang => url of the other versions), page_id, date
 */
function nl_drop_listing_html( $d, $lang ) {
	$lang  = nl_drop_L( $lang );
	$he    = $lang === 'he';
	$f     = $d['facts'];
	$c     = isset( $d['copy'][ $lang ] ) ? $d['copy'][ $lang ] : $d['copy']['en'];
	$b     = $d['broker'];
	$owner = ( $b['kind'] ?? 'broker' ) === 'owner';
	$uid   = 'd' . (int) $d['id'] . '-' . $lang;
	$deal  = ( $f['listing_type'] ?? '' ) === 'rent' ? 'rent' : 'sale';
	$area  = $he ? ( $f['area_he'] ?: ( $f['city_he'] ?? '' ) ) : ( nl_drop_fx( $f, 'area', $lang ) !== '' ? nl_drop_fx( $f, 'area', $lang ) : nl_drop_fx( $f, 'city', $lang ) );
	$city  = $he ? ( $f['city_he'] ?? '' ) : nl_drop_fx( $f, 'city', $lang );
	$name  = nl_drop_name( $b, $lang );
	$fill  = function ( $s ) use ( $f, $lang ) { return nl_drop_fill( $s, $f, $lang ); };
	$title = $fill( $c['title'] );
	$site  = nl_drop_site_url( $b, $lang );
	$wa    = nl_drop_wa_link( $b, $lang, $title );
	$tel   = $b['wa'] !== '' ? 'tel:+' . $b['wa'] : '';
	$photos = array_values( (array) $d['photos'] );
	$cover  = $photos ? $photos[0] : null;
	$kick   = array( nl_drop_t( $lang, $deal ) );
	$place  = trim( $area . ( $city && $city !== $area ? ', ' . $city : '' ) );
	if ( $place !== '' ) { $kick[] = $place; }
	$wrap   = function ( $x ) { return '<span class="nlx-num">' . esc_html( $x ) . '</span>'; };
	$alts   = isset( $d['alts'] ) && is_array( $d['alts'] ) ? $d['alts'] : array();
	if ( ! $alts && ! empty( $d['alt_url'] ) ) { $alts[ $he ? 'en' : 'he' ] = $d['alt_url']; }

	$h = '<article class="nlx" lang="' . $lang . '" dir="' . ( $he ? 'rtl' : 'ltr' ) . '" id="nlx-' . esc_attr( $uid ) . '" data-listing="' . esc_attr( $uid ) . '">' . "\n" . '<div class="nlx-wrap">' . "\n";
	$h .= '<header class="nlx-mast">' . "\n" . '<div class="nlx-mast-copy">' . "\n";
	$h .= '<p class="nlx-kicker">' . esc_html( implode( ' · ', $kick ) ) . '</p>' . "\n";
	$tag = $he ? 'h2' : 'h1';
	$h .= '<' . $tag . ' class="nlx-title">' . nl_drop_nums_html( $title ) . '</' . $tag . '>' . "\n";
	$h .= '<p class="nlx-dek">' . nl_drop_nums_html( $fill( $c['dek'] ) ) . '</p>' . "\n";
	$name_html = $site ? '<a href="' . esc_url( $site ) . '">' . esc_html( $name ) . '</a>' : esc_html( $name );
	if ( $owner ) {
		$chips = '<span class="nlx-chip nlx-chip--sea">' . esc_html( nl_drop_t( $lang, 'owner_chip' ) ) . '</span>';
	} else {
		$chips = '<span class="nlx-chip nlx-chip--sea">' . ( ! empty( $f['exclusive'] ) ? esc_html( nl_drop_t( $lang, 'exclusive' ) ) . ' · ' : '' ) . $name_html . '</span>';
	}
	foreach ( (array) $c['chips'] as $ch ) { $chips .= '<span class="nlx-chip">' . esc_html( $fill( $ch ) ) . '</span>'; }
	$h .= '<div class="nlx-chips">' . $chips . '</div>' . "\n" . '</div>' . "\n";
	if ( $cover ) {
		$ar = ( $cover['w'] > 0 && $cover['h'] > 0 ) ? $cover['w'] / $cover['h'] : 1.5;
		$ar = max( 0.56, min( 1.8, $ar ) );
		$h .= '<figure class="nlx-plate nlx-plate--photo" style="--nlx-cover-ar:' . esc_attr( sprintf( '%.3f', $ar ) ) . '"><img src="' . esc_url( $cover['url'] ) . '" alt="' . esc_attr( $title ) . '" width="' . (int) $cover['w'] . '" height="' . (int) $cover['h'] . '" loading="eager" decoding="async" fetchpriority="high">';
		$h .= $area !== '' ? '<span class="nlx-plate-name">' . esc_html( $area ) . '</span>' : '';
		$h .= '</figure>' . "\n";
	}
	$h .= '</header>' . "\n";

	// facts: only what the broker wrote
	$facts = array();
	$sq    = nl_drop_t( $lang, 'sqm' );
	if ( ! empty( $f['rooms'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_rooms' ), $wrap( nl_drop_fmt_num( $f['rooms'], $lang ) ) ); }
	if ( ! empty( $f['size_sqm'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_size' ), $wrap( nl_drop_fmt_int( $f['size_sqm'], $lang ) ) . ' ' . $sq ); }
	if ( ! empty( $f['balcony_sqm'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_balcony' ), $wrap( nl_drop_fmt_int( $f['balcony_sqm'], $lang ) ) . ' ' . $sq ); }
	if ( ! empty( $f['garden_sqm'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_garden' ), $wrap( nl_drop_fmt_int( $f['garden_sqm'], $lang ) ) . ' ' . $sq ); }
	if ( isset( $f['floor'] ) && $f['floor'] !== null ) {
		if ( (int) $f['floor'] === 0 ) { $fl = esc_html( nl_drop_t( $lang, 'ground' ) ); }
		else { $fl = $wrap( $lang === 'fr' ? nl_drop_fr_floor( $f['floor'] ) : (int) $f['floor'] ) . ( ! empty( $f['total_floors'] ) ? ' ' . nl_drop_t( $lang, 'of' ) . ' ' . $wrap( (int) $f['total_floors'] ) : '' ); }
		$facts[] = array( nl_drop_t( $lang, 'f_floor' ), $fl );
	}
	if ( ! empty( $f['parking'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_parking' ), ! empty( $f['parking_count'] ) ? $wrap( (int) $f['parking_count'] ) : nl_drop_t( $lang, 'yes' ) ); }
	if ( ! empty( $f['storage'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_storage' ), nl_drop_t( $lang, 'yes' ) ); }
	if ( ! empty( $f['protected_room'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_safe' ), nl_drop_t( $lang, 'yes' ) ); }
	if ( ! empty( $f['elevator'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_lift' ), nl_drop_t( $lang, 'yes' ) ); }
	if ( ! empty( $f['furnished'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_furnished' ), nl_drop_t( $lang, 'furnished' ) ); }
	if ( ! empty( $f['condition'] ) ) { $facts[] = array( nl_drop_t( $lang, 'f_condition' ), nl_drop_t( $lang, 'c_' . $f['condition'] ) ); }
	$entry = $he ? ( $f['entry_he'] ?? '' ) : nl_drop_fx( $f, 'entry', $lang );
	if ( $entry ) { $facts[] = array( nl_drop_t( $lang, 'f_entry' ), esc_html( $entry ) ); }
	if ( $facts ) {
		$h .= '<dl class="nlx-facts">' . "\n";
		foreach ( array_slice( $facts, 0, 8 ) as $x ) { $h .= '<div class="nlx-fact"><dt>' . esc_html( $x[0] ) . '</dt><dd>' . $x[1] . '</dd></div>' . "\n"; }
		$h .= '</dl>' . "\n";
	}

	$gallery = array_slice( $photos, 1 );
	$toc     = '';
	if ( $site ) { $toc .= '<a class="nlx-home" href="' . esc_url( $site ) . '">' . esc_html( nl_drop_tn( $lang, 'site', $name ) ) . '</a>'; }
	if ( $gallery ) { $toc .= '<a href="#photos-' . esc_attr( $uid ) . '">' . esc_html( nl_drop_t( $lang, 'photos' ) ) . '</a>'; }
	$toc .= '<a href="#home-' . esc_attr( $uid ) . '">' . esc_html( nl_drop_t( $lang, 'home' ) ) . '</a>';
	$toc .= '<a href="#broker-' . esc_attr( $uid ) . '">' . esc_html( $owner ? nl_drop_t( $lang, 'owner' ) : nl_drop_t( $lang, $b['female'] ? 'broker_tab_f' : 'broker_tab_m' ) ) . '</a>';
	$first = true;
	foreach ( nl_drop_langs() as $al ) {
		if ( $al === $lang || empty( $alts[ $al ] ) ) { continue; }
		$toc  .= '<a class="nlx-lang' . ( $first ? '' : ' nlx-lang--more' ) . '" href="' . esc_url( $alts[ $al ] ) . '" hreflang="' . $al . '" lang="' . $al . '">' . esc_html( nl_drop_lang_name( $al ) ) . '</a>';
		$first = false;
	}
	$h .= '<nav class="nlx-toc" aria-label="' . esc_attr( nl_drop_t( $lang, 'toc' ) ) . '">' . $toc . '</nav>' . "\n";

	$h .= '<div class="nlx-layout">' . "\n" . '<div class="nlx-main">' . "\n";
	if ( $gallery ) {
		$h .= '<section class="nlx-sec" id="photos-' . esc_attr( $uid ) . '"><div class="nlx-sec-head"><p class="nlx-eyebrow">' . esc_html( nl_drop_t( $lang, 'photos' ) ) . '</p><h2 class="nlx-h2">' . esc_html( nl_drop_t( $lang, 'photos_h2' ) ) . '</h2></div><div class="nlx-gallery">';
		foreach ( $gallery as $i => $g ) {
			$h .= '<figure><img src="' . esc_url( $g['url'] ) . '" alt="' . esc_attr( $title . ' · ' . ( $i + 2 ) ) . '" loading="lazy" decoding="async"' . ( $g['w'] ? ' width="' . (int) $g['w'] . '" height="' . (int) $g['h'] . '"' : '' ) . '></figure>';
		}
		$h .= '</div></section>' . "\n";
	}
	$h .= '<section class="nlx-sec" id="home-' . esc_attr( $uid ) . '">' . "\n";
	$h .= '<div class="nlx-sec-head"><p class="nlx-eyebrow">' . esc_html( nl_drop_t( $lang, 'home' ) ) . '</p><h2 class="nlx-h2">' . nl_drop_nums_html( $fill( $c['story_h2'] ) ) . '</h2></div>' . "\n";
	$h .= '<div class="nlx-prose">';
	foreach ( (array) $c['story'] as $para ) { $h .= '<p>' . nl_drop_nums_html( $fill( $para ) ) . '</p>'; }
	$h .= '</div>' . "\n";
	if ( ! empty( $c['features'] ) ) {
		$h .= '<ul class="nlx-features">';
		foreach ( (array) $c['features'] as $pair ) {
			$h .= '<li><b>' . nl_drop_nums_html( $fill( $pair[0] ?? '' ) ) . '</b>' . ( ! empty( $pair[1] ) ? '<span>' . nl_drop_nums_html( $fill( $pair[1] ) ) . '</span>' : '' ) . '</li>';
		}
		$h .= '</ul>' . "\n";
	}
	$h .= '</section>' . "\n";

	$eyebrow = $owner ? nl_drop_t( $lang, 'owner' ) : nl_drop_t( $lang, ( ! empty( $f['exclusive'] ) ? 'broker_ex_' : 'broker_' ) . ( $b['female'] ? 'f' : 'm' ) );
	$lic     = $owner ? nl_drop_t( $lang, 'owner_note' ) : nl_drop_licence_line( $b, $lang );
	$mono    = function_exists( 'mb_substr' ) ? mb_substr( $name, 0, 1 ) : substr( $name, 0, 1 );
	$btn_wa  = $wa ? '<a class="nlx-btn" href="' . esc_url( $wa ) . '" rel="noopener" target="_blank">' . nl_drop_icon( 'wa' ) . '<span>' . esc_html( nl_drop_t( $lang, 'cta' ) ) . '</span></a>' : '';
	$btn_tel = $tel ? '<a class="nlx-btn nlx-btn--ghost" href="' . esc_url( $tel ) . '">' . nl_drop_icon( 'phone' ) . '<span>' . esc_html( nl_drop_t( $lang, 'call' ) . ' ' . ( $he ? $b['phone'] : $b['phone_intl'] ) ) . '</span></a>' : '';
	$h .= '<section class="nlx-sec" id="broker-' . esc_attr( $uid ) . '">' . "\n" . '<div class="nlx-agent">' . "\n";
	$h .= '<span class="nlx-monogram" aria-hidden="true">' . esc_html( $mono ) . '</span>' . "\n";
	$h .= '<div><p class="nlx-eyebrow">' . esc_html( $eyebrow ) . '</p><p class="nlx-agent-name">' . $name_html . '</p>' . ( $lic !== '' ? '<p class="nlx-small">' . nl_drop_nums_html( $lic ) . '</p>' : '' ) . '</div>' . "\n";
	$h .= '<div class="nlx-cta">' . $btn_wa . $btn_tel . '</div>' . "\n" . '</div>' . "\n" . '</section>' . "\n";
	$h .= '</div>' . "\n";

	// the rail
	$h .= '<aside class="nlx-rail" aria-label="' . esc_attr( nl_drop_t( $lang, 'rail' ) ) . '">' . "\n" . '<div class="nlx-card nlx-price-card">' . "\n";
	$h .= '<span class="nlx-price-lbl">' . esc_html( nl_drop_t( $lang, 'price_' . $deal ) ) . '</span>' . "\n";
	if ( ! empty( $f['price'] ) ) {
		$h .= '<span class="nlx-price">' . nl_drop_money_html( $f['price'], $lang ) . '</span>' . "\n";
		$rows = '';
		if ( ! empty( $f['size_sqm'] ) ) { $rows .= '<div><dt>' . esc_html( nl_drop_t( $lang, 'psqm_' . $deal ) ) . '</dt><dd>' . nl_drop_money_html( round( $f['price'] / $f['size_sqm'] ), $lang ) . '</dd></div>'; }
		if ( $deal === 'rent' ) { $rows .= '<div><dt>' . esc_html( nl_drop_t( $lang, 'year' ) ) . '</dt><dd>' . nl_drop_money_html( $f['price'] * 12, $lang ) . '</dd></div>'; }
		if ( $entry ) { $rows .= '<div><dt>' . esc_html( nl_drop_t( $lang, 'f_entry' ) ) . '</dt><dd>' . esc_html( $entry ) . '</dd></div>'; }
		if ( $rows ) { $h .= '<dl class="nlx-price-rows">' . $rows . '</dl>' . "\n"; }
	} else {
		$h .= '<span class="nlx-price nlx-price--ask">' . esc_html( nl_drop_t( $lang, 'ask_' . $deal ) ) . '</span>' . "\n";
	}
	$h .= '<div class="nlx-cta">' . $btn_wa . ( $tel ? '<a class="nlx-btn nlx-btn--ghost" href="' . esc_url( $tel ) . '">' . nl_drop_icon( 'phone' ) . '<span>' . esc_html( nl_drop_t( $lang, 'call' ) ) . '</span></a>' : '' ) . '</div>' . "\n" . '</div>' . "\n";
	$h .= '<div class="nlx-card nlx-agent-mini"><span class="nlx-monogram" aria-hidden="true">' . esc_html( $mono ) . '</span><div><b>' . $name_html . '</b>' . ( $lic !== '' ? '<br><span class="nlx-muted">' . nl_drop_nums_html( $lic ) . '</span>' : '' ) . '</div></div>' . "\n";
	$h .= '</aside>' . "\n" . '</div>' . "\n";
	if ( $wa || $tel ) {
		$h .= '<div class="nlx-mbar">' . ( $wa ? '<a class="nlx-btn" href="' . esc_url( $wa ) . '" rel="noopener" target="_blank">' . nl_drop_icon( 'wa' ) . '<span>' . esc_html( nl_drop_t( $lang, 'wa' ) ) . '</span></a>' : '' ) . ( $tel ? '<a class="nlx-btn nlx-btn--ghost" href="' . esc_url( $tel ) . '">' . nl_drop_icon( 'phone' ) . '<span>' . esc_html( nl_drop_t( $lang, 'call' ) ) . '</span></a>' : '' ) . '</div>' . "\n";
	}
	$h .= '</div>' . "\n";

	if ( ! $he ) {
		$imgs = array();
		foreach ( $photos as $p ) { $imgs[] = $p['url']; }
		$node = array(
			'@type'       => 'RealEstateListing',
			'name'        => $title,
			'description' => $fill( $c['seo_desc'] ),
			'url'         => (string) $d['url'],
			'inLanguage'  => $lang,
			'datePosted'  => (string) $d['date'],
			'image'       => $imgs,
			'about'       => array_filter( array(
				'@type'         => in_array( $f['property_type'] ?? '', array( 'villa', 'cottage' ), true ) ? 'SingleFamilyResidence' : 'Apartment',
				'name'          => $title,
				'numberOfRooms' => ! empty( $f['rooms'] ) ? (float) $f['rooms'] : null,
				'floorSize'     => ! empty( $f['size_sqm'] ) ? array( '@type' => 'QuantitativeValue', 'value' => (int) $f['size_sqm'], 'unitCode' => 'MTK' ) : null,
				'address'       => array_filter( array( '@type' => 'PostalAddress', 'addressLocality' => $city !== '' ? $city : null, 'addressRegion' => $area !== '' ? $area : null, 'addressCountry' => 'IL' ) ),
			) ),
		);
		if ( ! empty( $f['price'] ) ) { $node['offers'] = array( '@type' => 'Offer', 'price' => (int) $f['price'], 'priceCurrency' => 'ILS', 'availability' => 'https://schema.org/InStock' ); }
		$h .= '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@graph' => array( $node ) ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
	}
	$h .= '</article>';

	$css = nl_drop_listing_css();
	if ( ! empty( $d['page_id'] ) ) {
		$pid  = (int) $d['page_id'];
		$css .= "\nbody.page-id-{$pid} .entry-content.is-layout-constrained>*{max-width:none!important;margin-left:auto!important;margin-right:auto!important}"
			. "\nbody.page-id-{$pid} .wp-block-post-featured-image,body.page-id-{$pid} .yoast-breadcrumbs,body.page-id-{$pid} .nlcta-start,body.page-id-{$pid} .nlcta-wa{display:none!important}";
	}
	$css .= "\n.nlx .nlx-price--ask{font-size:20px;line-height:1.35}\n.nlx .nlx-toc .nlx-lang--more{margin-inline-start:0}"
		. "\n.nlx:not([lang=\"he\"]) .nlx-agent{grid-template-columns:auto minmax(0,1fr)}\n.nlx:not([lang=\"he\"]) .nlx-agent .nlx-cta{grid-column:1/-1;justify-content:start}";
	return "<!-- wp:html -->\n<style>\n" . $css . "\n</style>\n" . $h . "\n<!-- /wp:html -->";
}

/* =====================================================================================================
 * Build: the Hebrew listing, the English twin, the photos, the language map, the caches
 * ===================================================================================================== */
function nl_drop_kses_off() {
	$had = has_filter( 'content_save_pre', 'wp_filter_post_kses' ) !== false;
	if ( $had ) { kses_remove_filters(); }
	return $had;
}

function nl_drop_kses_on( $had ) {
	if ( $had ) { kses_init_filters(); }
}

function nl_drop_photos( $ids, $title ) {
	$out = array();
	foreach ( array_values( (array) $ids ) as $i => $id ) {
		$id  = (int) $id;
		$url = wp_get_attachment_url( $id );
		if ( ! $url ) { continue; }
		$m     = wp_get_attachment_metadata( $id );
		$out[] = array( 'id' => $id, 'url' => $url, 'w' => (int) ( $m['width'] ?? 0 ), 'h' => (int) ( $m['height'] ?? 0 ) );
	}
	return $out;
}

function nl_drop_purge( $ids ) {
	foreach ( array_unique( array_filter( array_map( 'intval', (array) $ids ) ) ) as $id ) {
		clean_post_cache( $id );
		do_action( 'litespeed_purge_post', $id );
		$u = get_permalink( $id );
		if ( $u ) { do_action( 'litespeed_purge_url', $u ); }
	}
}

function nl_drop_data_for( $he_id, $b ) {
	$f      = json_decode( (string) get_post_meta( $he_id, 'nl_facts', true ), true );
	$c      = json_decode( (string) get_post_meta( $he_id, 'nl_copy', true ), true );
	$photos = json_decode( (string) get_post_meta( $he_id, 'nl_photos_json', true ), true );
	if ( ! is_array( $f ) || ! is_array( $c ) ) { return null; }
	return array( 'facts' => $f, 'copy' => $c, 'photos' => is_array( $photos ) ? $photos : array(), 'broker' => $b );
}

/** The language versions of a Hebrew listing: lang => page id. The first English twin predates the map. */
function nl_drop_twins( $he_id ) {
	$t = json_decode( (string) get_post_meta( $he_id, 'nl_twins', true ), true );
	$t = is_array( $t ) ? array_map( 'intval', $t ) : array();
	$en = (int) get_post_meta( $he_id, 'nl_twin', true );
	if ( $en && empty( $t['en'] ) ) { $t['en'] = $en; }
	$out = array();
	foreach ( $t as $l => $id ) {
		if ( $l !== 'he' && in_array( $l, nl_drop_langs(), true ) && $id > 0 ) { $out[ $l ] = $id; }
	}
	return $out;
}

/** Writes every language version from the stored facts and copy. Used on first build, and on every price change. */
function nl_drop_render_all( $he_id, $b ) {
	$data = nl_drop_data_for( $he_id, $b );
	if ( ! $data ) { return false; }
	$ids = array( 'he' => (int) $he_id );
	foreach ( nl_drop_twins( $he_id ) as $l => $id ) {
		if ( ! empty( $data['copy'][ $l ] ) && get_post( $id ) ) { $ids[ $l ] = $id; }
	}
	$urls = array();
	$live = array();
	foreach ( $ids as $l => $id ) {
		$urls[ $l ] = (string) get_permalink( $id );
		if ( get_post_status( $id ) === 'publish' ) { $live[ $l ] = $urls[ $l ]; }
	}
	$date = get_post_time( 'Y-m-d', false, $he_id );
	$had  = nl_drop_kses_off();
	foreach ( $ids as $l => $id ) {
		$alts = $live;
		unset( $alts[ $l ] );
		wp_update_post( array(
			'ID'           => $id,
			'post_excerpt' => nl_drop_fill( $data['copy'][ $l ]['dek'], $data['facts'], $l ),
			'post_content' => nl_drop_listing_html( array_merge( $data, array( 'id' => $he_id, 'url' => $urls[ $l ], 'alts' => $alts, 'page_id' => $l === 'he' ? 0 : $id, 'date' => $date ) ), $l ),
		) );
	}
	nl_drop_kses_on( $had );
	foreach ( $ids as $l => $id ) {
		update_post_meta( $id, '_yoast_wpseo_title', wp_slash( nl_drop_fill( $data['copy'][ $l ]['seo_title'], $data['facts'], $l ) ) );
		update_post_meta( $id, '_yoast_wpseo_metadesc', wp_slash( nl_drop_fill( $data['copy'][ $l ]['seo_desc'], $data['facts'], $l ) ) );
	}
	if ( count( $live ) > 1 ) {
		$map = wp_slash( wp_json_encode( $live, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) );
		foreach ( $live as $l => $u ) { update_post_meta( $ids[ $l ], 'nl_hreflang', $map ); }
	}
	return true;
}

/** Kept for callers of 1.0: the pair is now every language. */
function nl_drop_render_pair( $he_id, $en_id, $b ) {
	return nl_drop_render_all( $he_id, $b );
}

/* Token use and cost of the model calls in this request, kept on the submission. */
function nl_drop_usage_add( $model, $in, $out ) {
	$in    = (int) $in;
	$out   = (int) $out;
	$price = array( 'gpt-4.1' => array( 2.0, 8.0 ), 'gpt-4o' => array( 2.5, 10.0 ), 'gpt-4o-mini' => array( 0.15, 0.6 ), 'claude-sonnet-5' => array( 3.0, 15.0 ) );
	$p     = null;
	foreach ( $price as $k => $v ) { if ( strpos( (string) $model, $k ) === 0 ) { $p = $v; } }
	$usd = function_exists( 'nadlan_ai_estimated_cost_usd' ) ? (float) nadlan_ai_estimated_cost_usd( strpos( (string) $model, 'claude' ) === 0 ? 'anthropic' : 'openai', $model, $in, $out ) : 0.0;
	if ( $usd <= 0 && $p ) { $usd = ( $in * $p[0] + $out * $p[1] ) / 1000000; }
	$u = isset( $GLOBALS['nl_drop_usage'] ) && is_array( $GLOBALS['nl_drop_usage'] ) ? $GLOBALS['nl_drop_usage'] : array( 'calls' => 0, 'in' => 0, 'out' => 0, 'usd' => 0.0, 'models' => array() );
	$u['calls']++;
	$u['in']  += $in;
	$u['out'] += $out;
	$u['usd'] += $usd;
	$u['models'][ (string) $model ] = true;
	$GLOBALS['nl_drop_usage'] = $u;
}

function nl_drop_usage_save( $post_id ) {
	if ( empty( $GLOBALS['nl_drop_usage'] ) ) { return; }
	$prev = get_post_meta( $post_id, 'nl_usage', true );
	$u    = $GLOBALS['nl_drop_usage'];
	if ( is_array( $prev ) ) {
		foreach ( array( 'calls', 'in', 'out', 'usd' ) as $k ) { $u[ $k ] += $prev[ $k ] ?? 0; }
		$u['models'] = array_merge( (array) ( $prev['models'] ?? array() ), (array) $u['models'] );
	}
	$u['usd'] = round( (float) $u['usd'], 5 );
	update_post_meta( $post_id, 'nl_usage', $u );
	$GLOBALS['nl_drop_usage'] = null;
}

function nl_drop_build( $drop_id, $b ) {
	$prev = get_post_meta( $drop_id, 'nl_result', true );
	if ( is_array( $prev ) && ! empty( $prev['he_id'] ) ) { return $prev; }
	$f      = json_decode( (string) get_post_meta( $drop_id, 'nl_facts', true ), true );
	$text   = (string) get_post_meta( $drop_id, 'nl_text', true );
	$ids    = array_map( 'intval', (array) get_post_meta( $drop_id, 'nl_photos', true ) );
	if ( ! is_array( $f ) ) { return new WP_Error( 'nofacts', 'no facts' ); }
	$owner  = ( $b['kind'] ?? 'broker' ) === 'owner';
	$langs  = $owner ? array( 'he' ) : (array) ( $b['langs'] ?? array( 'he', 'en' ) );
	update_post_meta( $drop_id, 'nl_state', 'writing' );
	$err  = null;
	$copy = nl_drop_write( $f, $text, $b, $err );
	$xl   = array_values( array_intersect( array( 'ru', 'fr' ), $langs ) );
	if ( $xl ) {
		$terr = null;
		$tr   = nl_drop_translate( $copy, $f, $text, $xl, $terr );
		if ( $terr ) { $err = ( $err ? $err . '; ' : '' ) . 'translate:' . $terr; }
		foreach ( $tr['names'] as $l => $nm ) {
			foreach ( $nm as $k => $v ) { if ( $v !== '' ) { $f[ $k . '_' . $l ] = $v; } }
		}
		foreach ( $tr['copy'] as $l => $c ) { $copy[ $l ] = $c; }
		if ( ! empty( $tr['plain'] ) ) { update_post_meta( $drop_id, 'nl_plain', implode( ',', $tr['plain'] ) ); }
	}
	$slug = nl_drop_slug( $f, $b );
	$pub  = $f;
	unset( $pub['street_he'], $pub['street_en'] );
	$photos = nl_drop_photos( $ids, $copy['he']['title'] );
	$author = $owner && ! empty( $b['user_id'] ) ? (int) $b['user_id'] : nl_drop_author();
	$status = $b['auto'] ? 'publish' : 'draft';

	$had   = nl_drop_kses_off();
	$he_id = wp_insert_post( array(
		'post_type'    => 'nadlan_property',
		'post_status'  => $status,
		'post_title'   => nl_drop_fill( $copy['he']['title'], $f, 'he' ),
		'post_name'    => $slug,
		'post_excerpt' => nl_drop_fill( $copy['he']['dek'], $f, 'he' ),
		'post_content' => '',
		'post_author'  => $author,
	), true );
	nl_drop_kses_on( $had );
	if ( is_wp_error( $he_id ) ) { update_post_meta( $drop_id, 'nl_state', 'failed' ); return $he_id; }

	$type_map = array( 'mini_penthouse' => 'penthouse', 'villa' => 'cottage' );
	$ptype    = $f['property_type'] ? ( $type_map[ $f['property_type'] ] ?? $f['property_type'] ) : 'apartment';
	$meta     = array(
		'listing_type'   => $f['listing_type'],
		'property_type'  => $ptype,
		'price'          => $f['price'],
		'rooms'          => $f['rooms'],
		'floor'          => $f['floor'],
		'total_floors'   => $f['total_floors'],
		'size_sqm'       => $f['size_sqm'],
		'sqm'            => $f['size_sqm'],
		'balcony_sqm'    => $f['balcony_sqm'],
		'city'           => $f['city_he'],
		'neighborhood'   => $f['area_he'],
		'parking'        => $f['parking'],
		'elevator'       => $f['elevator'],
		'ac'             => $f['ac'],
		'protected_room' => $f['protected_room'],
		'storage'        => $f['storage'],
		'entry_date'     => $f['entry_he'],
		'condition'      => $f['condition'],
		'highlights_csv' => implode( '|', array_slice( $f['features_he'] ?? array(), 0, 6 ) ),
	);
	foreach ( $meta as $k => $v ) {
		if ( $v !== null && $v !== '' ) { update_post_meta( $he_id, $k, $v ); }
	}
	update_post_meta( $he_id, 'status', 'active' );
	update_post_meta( $he_id, 'claim_status', 'verified' );
	update_post_meta( $he_id, 'nl_status', 'active' );
	update_post_meta( $he_id, 'nl_drop_id', (string) $drop_id );
	if ( $owner ) {
		update_post_meta( $he_id, 'source', 'owner_wizard' );
		update_post_meta( $he_id, 'nl_owner', '1' );
		update_post_meta( $he_id, 'owner_user_id', (int) ( $b['user_id'] ?? 0 ) );
		update_post_meta( $he_id, 'nl_owner_contact', wp_slash( wp_json_encode( array( 'name' => $b['name_he'], 'phone' => $b['phone'] ), JSON_UNESCAPED_UNICODE ) ) );
	} else {
		update_post_meta( $he_id, 'source', 'broker_drop' );
		update_post_meta( $he_id, 'nl_broker_id', (string) $b['id'] );
	}
	update_post_meta( $he_id, 'nl_facts', wp_slash( wp_json_encode( $pub, JSON_UNESCAPED_UNICODE ) ) );
	update_post_meta( $he_id, 'nl_copy', wp_slash( wp_json_encode( $copy, JSON_UNESCAPED_UNICODE ) ) );
	update_post_meta( $he_id, 'nl_photos_json', wp_slash( wp_json_encode( $photos, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) ) );
	update_post_meta( $he_id, 'photos_csv', implode( ',', wp_list_pluck( $photos, 'url' ) ) );
	update_post_meta( $he_id, '_yoast_wpseo_title', nl_drop_fill( $copy['he']['seo_title'], $f, 'he' ) );
	update_post_meta( $he_id, '_yoast_wpseo_metadesc', nl_drop_fill( $copy['he']['seo_desc'], $f, 'he' ) );
	if ( $photos ) { set_post_thumbnail( $he_id, $photos[0]['id'] ); }
	foreach ( $photos as $i => $p ) {
		wp_update_post( array( 'ID' => $p['id'], 'post_parent' => $he_id ) );
		update_post_meta( $p['id'], '_wp_attachment_image_alt', wp_slash( nl_drop_fill( $copy['he']['title'], $f, 'he' ) . ( $i ? ' · ' . ( $i + 1 ) : '' ) ) );
	}

	// one page per language, under the broker's site in that language (created with the first listing that needs it)
	$twins = array();
	foreach ( array_diff( $langs, array( 'he' ) ) as $l ) {
		if ( empty( $copy[ $l ] ) ) { continue; }
		$site = nl_drop_site_ensure( $b, $l, $status );
		if ( ! $site ) { continue; }
		$had = nl_drop_kses_off();
		$tid = wp_insert_post( array(
			'post_type'    => 'page',
			'post_status'  => $status,
			'post_parent'  => $site,
			'post_title'   => nl_drop_fill( $copy[ $l ]['title'], $f, $l ),
			'post_name'    => $slug,
			'post_excerpt' => nl_drop_fill( $copy[ $l ]['dek'], $f, $l ),
			'post_content' => '',
			'post_author'  => $author,
		), true );
		nl_drop_kses_on( $had );
		if ( is_wp_error( $tid ) || ! $tid ) { continue; }
		update_post_meta( $tid, 'nl_broker_id', (string) $b['id'] );
		update_post_meta( $tid, 'nl_twin', (string) $he_id );
		update_post_meta( $tid, 'nl_lang', $l );
		update_post_meta( $tid, 'nl_status', 'active' );
		update_post_meta( $tid, 'source', 'broker_drop' );
		if ( $photos ) { set_post_thumbnail( $tid, $photos[0]['id'] ); }
		$twins[ $l ] = (int) $tid;
	}
	if ( ! empty( $twins['en'] ) ) { update_post_meta( $he_id, 'nl_twin', (string) $twins['en'] ); }
	if ( $twins ) { update_post_meta( $he_id, 'nl_twins', wp_slash( wp_json_encode( $twins ) ) ); }
	if ( ! $owner ) {
		$fresh = nl_drop_broker( $b['id'] );
		if ( $fresh ) { $b = $fresh; }
	}
	nl_drop_render_all( $he_id, $b );
	$urls = array( 'he' => (string) get_permalink( $he_id ) );
	foreach ( $twins as $l => $tid ) { $urls[ $l ] = (string) get_permalink( $tid ); }
	nl_drop_site_sync( $b );
	nl_drop_purge( array_merge( array( $he_id ), array_values( $twins ), array( $b['site_he'] ?? 0, $b['site_en'] ?? 0, $b['site_ru'] ?? 0, $b['site_fr'] ?? 0 ) ) );
	$res = array(
		'state'  => $status === 'publish' ? 'published' : 'draft',
		'he_id'  => (int) $he_id,
		'en_id'  => (int) ( $twins['en'] ?? 0 ),
		'url_he' => $urls['he'],
		'url_en' => $urls['en'] ?? '',
		'urls'   => $urls,
		'title'  => nl_drop_fill( $copy['he']['title'], $f, 'he' ),
		'ai'     => $err ? 'fallback:' . $err : 'ok',
	);
	update_post_meta( $drop_id, 'nl_result', $res );
	update_post_meta( $drop_id, 'nl_state', $res['state'] );
	nl_drop_usage_save( $drop_id );
	return $res;
}

/* =====================================================================================================
 * REST: the only doors. The token in the path is the identity; nothing works without a live broker.
 * ===================================================================================================== */
add_action( 'rest_api_init', function () {
	$t = '/drop/(?P<token>[a-z0-9]{24})';
	register_rest_route( 'nadlan/v1', $t . '/photo', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nl_drop_rest_photo' ) );
	register_rest_route( 'nadlan/v1', $t . '/submit', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nl_drop_rest_submit' ) );
	register_rest_route( 'nadlan/v1', $t . '/build/(?P<drop>\d+)', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nl_drop_rest_build' ) );
	register_rest_route( 'nadlan/v1', $t . '/listings', array( 'methods' => 'GET', 'permission_callback' => '__return_true', 'callback' => 'nl_drop_rest_listings' ) );
	register_rest_route( 'nadlan/v1', $t . '/update', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nl_drop_rest_update' ) );
} );

function nl_drop_rest_broker( $req ) {
	$b = nl_drop_broker_by_token( (string) $req['token'] );
	if ( ! $b ) { return new WP_Error( 'nl_drop_off', 'הקישור לא פעיל.', array( 'status' => 404 ) ); }
	return $b;
}

function nl_drop_strip_gps( $file, $type ) {
	if ( $type !== 'image/jpeg' || ! function_exists( 'exif_read_data' ) || ! function_exists( 'imagecreatefromjpeg' ) ) { return; }
	$ex = @exif_read_data( $file );
	if ( ! is_array( $ex ) || empty( $ex['GPSLatitude'] ) ) { return; }
	$im = @imagecreatefromjpeg( $file );
	if ( ! $im ) { return; }
	$o = (int) ( $ex['Orientation'] ?? 1 );
	if ( $o === 3 ) { $im = imagerotate( $im, 180, 0 ); }
	elseif ( $o === 6 ) { $im = imagerotate( $im, -90, 0 ); }
	elseif ( $o === 8 ) { $im = imagerotate( $im, 90, 0 ); }
	imagejpeg( $im, $file, 90 );
	imagedestroy( $im );
}

function nl_drop_rest_photo( WP_REST_Request $req ) {
	$b = nl_drop_rest_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	if ( nl_drop_rate( $b['id'], 'photo', 150, HOUR_IN_SECONDS ) ) { return new WP_Error( 'rate', 'הרבה תמונות בשעה האחרונה. אפשר להמשיך בעוד כמה דקות.', array( 'status' => 429 ) ); }
	$files = $req->get_file_params();
	$f     = $files['photo'] ?? null;
	if ( ! is_array( $f ) || empty( $f['tmp_name'] ) ) { return new WP_Error( 'nofile', 'לא התקבל קובץ.', array( 'status' => 400 ) ); }
	if ( (int) $f['size'] > NL_DROP_MAX_BYTES ) { return new WP_Error( 'big', 'התמונה גדולה מ-15MB.', array( 'status' => 400 ) ); }
	$mimes = array( 'jpg|jpeg|jpe' => 'image/jpeg', 'png' => 'image/png', 'webp' => 'image/webp', 'heic' => 'image/heic', 'heif' => 'image/heif' );
	$check = wp_check_filetype_and_ext( $f['tmp_name'], $f['name'], $mimes );
	if ( empty( $check['type'] ) || strpos( (string) $check['type'], 'image/' ) !== 0 ) { return new WP_Error( 'type', 'אפשר להעלות תמונות בלבד.', array( 'status' => 400 ) ); }
	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/image.php';
	require_once ABSPATH . 'wp-admin/includes/media.php';
	$f['name'] = 'nadlan-' . $b['id'] . '-' . gmdate( 'Ymd-His' ) . '-' . wp_rand( 100, 999 ) . '.' . ( $check['ext'] ?: 'jpg' );
	$moved     = wp_handle_upload( $f, array( 'test_form' => false, 'mimes' => $mimes ) );
	if ( isset( $moved['error'] ) ) { return new WP_Error( 'upload', 'ההעלאה נכשלה. אפשר לנסות שוב.', array( 'status' => 500 ) ); }
	nl_drop_strip_gps( $moved['file'], $moved['type'] );
	$att = wp_insert_attachment( array(
		'post_mime_type' => $moved['type'],
		'post_title'     => 'nadlan-drop-' . $b['id'],
		'post_status'    => 'inherit',
		'post_author'    => nl_drop_author(),
	), $moved['file'] );
	if ( is_wp_error( $att ) || ! $att ) { return new WP_Error( 'insert', 'ההעלאה נכשלה.', array( 'status' => 500 ) ); }
	wp_update_attachment_metadata( $att, wp_generate_attachment_metadata( $att, $moved['file'] ) );
	update_post_meta( $att, 'nl_drop_broker', (string) $b['id'] );
	$m = wp_get_attachment_metadata( $att );
	return array( 'id' => (int) $att, 'url' => (string) wp_get_attachment_url( $att ), 'w' => (int) ( $m['width'] ?? 0 ), 'h' => (int) ( $m['height'] ?? 0 ) );
}

function nl_drop_rest_submit( WP_REST_Request $req ) {
	$b = nl_drop_rest_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	if ( nl_drop_rate( $b['id'], 'submit', 40, DAY_IN_SECONDS ) ) { return new WP_Error( 'rate', 'הגעתם למכסת הנכסים להיום.', array( 'status' => 429 ) ); }
	$text = trim( sanitize_textarea_field( (string) $req->get_param( 'text' ) ) );
	$text = function_exists( 'mb_substr' ) ? mb_substr( $text, 0, 4000 ) : substr( $text, 0, 4000 );
	$ids  = array();
	foreach ( (array) $req->get_param( 'photos' ) as $id ) {
		$id = (int) $id;
		if ( $id && get_post_type( $id ) === 'attachment' && (string) get_post_meta( $id, 'nl_drop_broker', true ) === (string) $b['id'] && ! in_array( $id, $ids, true ) ) { $ids[] = $id; }
		if ( count( $ids ) >= NL_DROP_MAX_PHOTOS ) { break; }
	}
	if ( ( function_exists( 'mb_strlen' ) ? mb_strlen( $text ) : strlen( $text ) ) < 8 ) {
		return array( 'state' => 'held', 'missing' => array( 'כמה שורות על הנכס' ) );
	}
	@set_time_limit( 170 );
	$drop_id = wp_insert_post( array(
		'post_type'    => 'nadlan_drop',
		'post_status'  => 'private',
		'post_title'   => $b['name_he'] . ' · ' . wp_date( 'j.n.Y H:i' ),
		'post_content' => $text,
		'post_author'  => nl_drop_author(),
	), true );
	if ( is_wp_error( $drop_id ) ) { return new WP_Error( 'save', 'השמירה נכשלה. אפשר לנסות שוב.', array( 'status' => 500 ) ); }
	update_post_meta( $drop_id, 'nl_broker_id', (string) $b['id'] );
	update_post_meta( $drop_id, 'nl_text', wp_slash( $text ) );
	update_post_meta( $drop_id, 'nl_photos', $ids );
	update_post_meta( $drop_id, 'nl_door', 'link' );
	update_post_meta( $drop_id, 'nl_state', 'reading' );
	$err = null;
	$f   = nl_drop_extract( $text, $b, $err );
	nl_drop_usage_save( $drop_id );
	update_post_meta( $drop_id, 'nl_facts', wp_slash( wp_json_encode( $f, JSON_UNESCAPED_UNICODE ) ) );
	if ( $err ) { update_post_meta( $drop_id, 'nl_ai', 'fallback:' . $err ); }
	$miss = nl_drop_missing( $f, $ids );
	if ( $miss ) {
		update_post_meta( $drop_id, 'nl_state', 'held' );
		update_post_meta( $drop_id, 'nl_missing', $miss );
		return array( 'state' => 'held', 'drop' => (int) $drop_id, 'missing' => $miss, 'summary' => nl_drop_summary( $f ) );
	}
	update_post_meta( $drop_id, 'nl_state', 'ready' );
	return array( 'state' => 'ready', 'drop' => (int) $drop_id, 'summary' => nl_drop_summary( $f ) );
}

function nl_drop_rest_build( WP_REST_Request $req ) {
	$b = nl_drop_rest_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	$drop = (int) $req['drop'];
	if ( get_post_type( $drop ) !== 'nadlan_drop' || (string) get_post_meta( $drop, 'nl_broker_id', true ) !== (string) $b['id'] ) {
		return new WP_Error( 'nf', 'לא נמצא.', array( 'status' => 404 ) );
	}
	$state = (string) get_post_meta( $drop, 'nl_state', true );
	if ( ! in_array( $state, array( 'ready', 'writing', 'published', 'draft' ), true ) ) { return new WP_Error( 'state', 'חסרים פרטים.', array( 'status' => 409 ) ); }
	@set_time_limit( 170 );
	$res = nl_drop_build( $drop, $b );
	if ( is_wp_error( $res ) ) { return new WP_Error( 'build', 'בניית העמוד נכשלה. אפשר לנסות שוב.', array( 'status' => 500 ) ); }
	return $res;
}

function nl_drop_broker_listings( $bid, $lang = 'he', $only_live = true ) {
	$lang = nl_drop_L( $lang );
	$q    = get_posts( array(
		'post_type'        => 'nadlan_property',
		'post_status'      => $only_live ? array( 'publish' ) : array( 'publish', 'draft' ),
		'numberposts'      => 200,
		'orderby'          => 'date',
		'order'            => 'DESC',
		'suppress_filters' => true,
		'meta_query'       => array( array( 'key' => 'nl_broker_id', 'value' => (string) (int) $bid ) ),
	) );
	$out = array();
	foreach ( $q as $p ) {
		$twins = nl_drop_twins( $p->ID );
		$lid   = $lang === 'he' ? (int) $p->ID : (int) ( $twins[ $lang ] ?? 0 );
		if ( $lang !== 'he' && ( ! $lid || get_post_status( $lid ) !== 'publish' ) ) { continue; }
		$st = (string) get_post_meta( $p->ID, 'nl_status', true );
		$out[] = array(
			'id'       => (int) $p->ID,
			'twin'     => (int) ( $twins['en'] ?? 0 ),
			'twins'    => $twins,
			'url'      => (string) get_permalink( $lid ),
			'title'    => (string) get_the_title( $lid ),
			'deal'     => (string) get_post_meta( $p->ID, 'listing_type', true ) === 'rent' ? 'rent' : 'sale',
			'status'   => in_array( $st, array( 'sold', 'rented' ), true ) ? $st : 'active',
			'card_key' => (string) get_post_meta( $p->ID, 'nl_card_key', true ),
			'source'   => (string) get_post_meta( $p->ID, 'source', true ),
			'price'    => (int) get_post_meta( $p->ID, 'price', true ),
			'cover'    => (string) get_the_post_thumbnail_url( $p->ID, 'medium' ),
			'date'     => get_post_time( 'U', true, $p->ID ),
			'modified' => get_post_modified_time( 'U', true, $p->ID ),
		);
	}
	return $out;
}

function nl_drop_rest_listings( WP_REST_Request $req ) {
	$b = nl_drop_rest_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	$rows = array();
	foreach ( nl_drop_broker_listings( $b['id'], 'he', false ) as $L ) {
		$rows[] = array(
			'id'       => $L['id'],
			'title'    => html_entity_decode( $L['title'], ENT_QUOTES, 'UTF-8' ),
			'url'      => $L['url'],
			'cover'    => $L['cover'],
			'deal'     => $L['deal'],
			'status'   => $L['status'],
			'price'    => $L['price'] ? nl_drop_price_text( $L['price'], 'he' ) . ( $L['deal'] === 'rent' ? ' לחודש' : '' ) : '',
			'editable' => $L['source'] === 'broker_drop',
			'live'     => get_post_status( $L['id'] ) === 'publish',
			'langs'    => array_keys( $L['twins'] ),
		);
	}
	return array( 'name' => $b['name_he'], 'site' => nl_drop_site_url( $b, 'he' ), 'listings' => $rows );
}

/** Every page of a listing: the Hebrew one and its language versions (the first English twin may predate the map). */
function nl_drop_listing_ids( $id ) {
	$twins = nl_drop_twins( $id );
	if ( ! $twins ) {
		$tw = get_posts( array( 'post_type' => 'page', 'post_status' => 'any', 'numberposts' => 5, 'fields' => 'ids', 'meta_query' => array( array( 'key' => 'nl_twin', 'value' => (string) $id ) ) ) );
		foreach ( $tw as $t ) {
			$l = nl_drop_L( (string) get_post_meta( $t, 'nl_lang', true ) ?: 'en' );
			if ( $l !== 'he' ) { $twins[ $l ] = (int) $t; }
		}
	}
	return array_merge( array( (int) $id ), array_values( $twins ) );
}

/** Sold, let, back on the market, or a new price: every language, the broker's sites, the caches. */
function nl_drop_apply_update( $id, $b, $status, $price ) {
	$ids = nl_drop_listing_ids( $id );
	$sites = array( $b['site_he'] ?? 0, $b['site_en'] ?? 0, $b['site_ru'] ?? 0, $b['site_fr'] ?? 0 );
	if ( in_array( $status, array( 'sold', 'rented', 'active' ), true ) ) {
		foreach ( $ids as $pid ) {
			update_post_meta( $pid, 'nl_status', $status );
			update_post_meta( $pid, 'status', $status );
		}
		nl_drop_site_sync( $b );
		nl_drop_purge( array_merge( $ids, $sites ) );
		return array( 'ok' => true, 'status' => $status );
	}
	if ( $price !== null && $price !== '' ) {
		$src = (string) get_post_meta( $id, 'source', true );
		if ( $src !== 'broker_drop' && $src !== 'owner_wizard' ) { return new WP_Error( 'static', 'את המחיר של הנכס הזה מעדכנים מול nad-lan.', array( 'status' => 409 ) ); }
		$p = (int) preg_replace( '/\D+/', '', (string) $price );
		if ( $p < 500 || $p > 500000000 ) { return new WP_Error( 'price', 'המחיר לא נראה תקין.', array( 'status' => 400 ) ); }
		$f = json_decode( (string) get_post_meta( $id, 'nl_facts', true ), true );
		if ( ! is_array( $f ) ) { return new WP_Error( 'nofacts', 'לא ניתן לעדכן.', array( 'status' => 409 ) ); }
		$f['price'] = $p;
		update_post_meta( $id, 'nl_facts', wp_slash( wp_json_encode( $f, JSON_UNESCAPED_UNICODE ) ) );
		update_post_meta( $id, 'price', $p );
		nl_drop_render_all( $id, $b );
		nl_drop_site_sync( $b );
		nl_drop_purge( array_merge( $ids, $sites ) );
		return array( 'ok' => true, 'price' => nl_drop_price_text( $p, 'he' ) );
	}
	return new WP_Error( 'nothing', 'לא התקבל עדכון.', array( 'status' => 400 ) );
}

function nl_drop_rest_update( WP_REST_Request $req ) {
	$b = nl_drop_rest_broker( $req );
	if ( is_wp_error( $b ) ) { return $b; }
	if ( nl_drop_rate( $b['id'], 'update', 120, HOUR_IN_SECONDS ) ) { return new WP_Error( 'rate', 'יותר מדי עדכונים בשעה האחרונה.', array( 'status' => 429 ) ); }
	$id = (int) $req->get_param( 'id' );
	if ( get_post_type( $id ) !== 'nadlan_property' || (string) get_post_meta( $id, 'nl_broker_id', true ) !== (string) $b['id'] ) {
		return new WP_Error( 'nf', 'הנכס לא נמצא.', array( 'status' => 404 ) );
	}
	return nl_drop_apply_update( $id, $b, (string) $req->get_param( 'status' ), $req->get_param( 'price' ) );
}

/* =====================================================================================================
 * The broker's own site: new properties first, off-market cards out, the counters right
 * ===================================================================================================== */
function nl_drop_remove_li( $html, $id ) {
	$p = strpos( $html, 'id="' . $id . '"' );
	if ( $p === false ) { return $html; }
	$start = strrpos( substr( $html, 0, $p ), '<li' );
	if ( $start === false ) { return $html; }
	$depth = 0;
	$i     = $start;
	$len   = strlen( $html );
	while ( $i < $len ) {
		$o = strpos( $html, '<li', $i );
		$c = strpos( $html, '</li>', $i );
		if ( $c === false ) { return $html; }
		if ( $o !== false && $o < $c ) { $depth++; $i = $o + 3; continue; }
		$depth--;
		$i = $c + 5;
		if ( $depth === 0 ) { return substr( $html, 0, $start ) . substr( $html, $i ); }
	}
	return $html;
}

function nl_drop_card_html( $L, $lang, $b ) {
	$lang = nl_drop_L( $lang );
	$he   = $lang === 'he';
	$data = nl_drop_data_for( $L['id'], $b );
	if ( ! $data ) { return ''; }
	$f    = $data['facts'];
	$c    = isset( $data['copy'][ $lang ] ) ? $data['copy'][ $lang ] : $data['copy']['en'];
	$deal = $L['deal'];
	$ttl  = nl_drop_fill( $c['card_title'] ?? $c['title'], $f, $lang );
	$url  = $L['url'];
	$cov  = ! empty( $data['photos'][0]['url'] ) ? $data['photos'][0]['url'] : $L['cover'];
	$area = $he ? ( $f['area_he'] ?: ( $f['city_he'] ?? '' ) ) : ( nl_drop_fx( $f, 'area', $lang ) !== '' ? nl_drop_fx( $f, 'area', $lang ) : nl_drop_fx( $f, 'city', $lang ) );
	$kick = trim( nl_drop_type_label( $f['property_type'] ?: 'apartment', $lang ) . ( $area !== '' ? ' · ' . $area : '' ) );
	$num  = function ( $n ) { return '<span class="nlb-num">' . esc_html( $n ) . '</span>'; };
	$lc   = function ( $s ) use ( $he ) { return ( $he || ! function_exists( 'mb_strtolower' ) ) ? $s : mb_strtolower( mb_substr( $s, 0, 1 ) ) . mb_substr( $s, 1 ); };
	$h  = '<li class="nlb-lcard" data-deal="' . esc_attr( $deal ) . '" id="nlb-' . $lang . '-d' . (int) $L['id'] . '">' . "\n";
	$h .= '<a class="nlb-lcard-media" href="' . esc_url( $url ) . '" tabindex="-1" aria-hidden="true">' . ( $cov ? '<img src="' . esc_url( $cov ) . '" alt="" loading="lazy" decoding="async">' : '' );
	$h .= '<span class="nlb-badges"><span class="nlb-badge nlb-badge--' . esc_attr( $deal ) . '">' . esc_html( nl_drop_t( $lang, $deal ) ) . '</span></span></a>' . "\n";
	$h .= '<p class="nlb-lcard-kicker">' . esc_html( $kick ) . '</p>' . "\n";
	$h .= '<h3 class="nlb-lcard-title"><a href="' . esc_url( $url ) . '">' . esc_html( $ttl ) . '</a></h3>' . "\n";
	if ( ! empty( $f['price'] ) ) {
		$pn    = $num( nl_drop_fmt_int( $f['price'], $lang ) );
		$money = $lang === 'en' ? '<span>NIS&nbsp;' . $pn . '</span>' : '<span>' . $pn . '&nbsp;₪</span>';
		$sub   = '';
		if ( ! empty( $f['size_sqm'] ) ) {
			$ps  = $num( nl_drop_fmt_int( round( $f['price'] / $f['size_sqm'] ), $lang ) );
			$per = $lc( nl_drop_t( $lang, 'psqm_' . $deal ) );
			$sub = $lang === 'en' ? '<span>NIS&nbsp;' . $ps . ' ' . esc_html( $per ) . '</span>' : '<span>' . $ps . '&nbsp;₪ ' . esc_html( $per ) . '</span>';
		}
		$h .= '<div class="nlb-price"><strong>' . $money . ( $deal === 'rent' ? ' <small>' . esc_html( nl_drop_t( $lang, 'month' ) ) . '</small>' : '' ) . '</strong>' . $sub . '</div>' . "\n";
	} else {
		$h .= '<div class="nlb-price"><strong class="nlb-ask">' . esc_html( nl_drop_t( $lang, $deal === 'rent' ? 'ask_short_rent' : 'ask_short' ) ) . '</strong><span>' . esc_html( nl_drop_t( $lang, 'ask_sub' ) ) . '</span></div>' . "\n";
	}
	$specs = array();
	if ( ! empty( $f['rooms'] ) ) { $specs[] = array( 'rooms', nl_drop_rooms_html( $f['rooms'], $lang, $num ) ); }
	if ( ! empty( $f['size_sqm'] ) ) { $specs[] = array( 'area', sprintf( esc_html( nl_drop_t( $lang, 'size_n' ) ), $num( nl_drop_fmt_int( $f['size_sqm'], $lang ) ) ) ); }
	if ( ! empty( $f['balcony_sqm'] ) ) { $specs[] = array( 'balcony', sprintf( esc_html( nl_drop_t( $lang, 'balcony_n' ) ), $num( nl_drop_fmt_int( $f['balcony_sqm'], $lang ) ) ) ); }
	elseif ( ! empty( $f['garden_sqm'] ) ) { $specs[] = array( 'balcony', sprintf( esc_html( nl_drop_t( $lang, 'garden_n' ) ), $num( nl_drop_fmt_int( $f['garden_sqm'], $lang ) ) ) ); }
	if ( isset( $f['floor'] ) && $f['floor'] !== null && $f['floor'] > 0 ) { $specs[] = array( 'floor', nl_drop_floor_html( $f, $lang, $num ) ); }
	if ( $specs ) {
		$h .= '<ul class="nlb-specs">';
		foreach ( array_slice( $specs, 0, 4 ) as $s ) { $h .= '<li>' . nl_drop_icon( $s[0] ) . '<span>' . $s[1] . '</span></li>'; }
		$h .= '</ul>' . "\n";
	}
	$hi = array_slice( (array) ( $c['card_hi'] ?? array() ), 0, 3 );
	if ( $hi ) {
		$h .= '<ul class="nlb-hi">';
		foreach ( $hi as $x ) { $h .= '<li>' . esc_html( nl_drop_fill( $x, $f, $lang ) ) . '</li>'; }
		$h .= '</ul>' . "\n";
	}
	$amen = array();
	if ( ! empty( $f['parking'] ) ) { $amen[] = array( 'parking', nl_drop_parking_txt( $f, $lang ) ); }
	if ( ! empty( $f['storage'] ) ) { $amen[] = array( 'storage', nl_drop_t( $lang, 'f_storage' ) ); }
	if ( ! empty( $f['protected_room'] ) ) { $amen[] = array( 'shield', nl_drop_t( $lang, 'f_safe' ) ); }
	if ( ! empty( $f['elevator'] ) ) { $amen[] = array( 'lift', nl_drop_t( $lang, 'f_lift' ) ); }
	if ( $amen ) {
		$h .= '<div class="nlb-amen">';
		foreach ( array_slice( $amen, 0, 4 ) as $a ) { $h .= '<span>' . nl_drop_icon( $a[0] ) . esc_html( $a[1] ) . '</span>'; }
		$h .= '</div>' . "\n";
	}
	$entry = $he ? ( $f['entry_he'] ?? '' ) : nl_drop_fx( $f, 'entry', $lang );
	$h .= '<p class="nlb-lcard-meta">' . ( $entry ? '<span>' . nl_drop_icon( 'key' ) . esc_html( sprintf( nl_drop_t( $lang, 'entry_n' ), $entry ) ) . '</span>' : '<span></span>' ) . '<span class="nlb-num">' . esc_html( nl_drop_t( $lang, 'updated' ) . ' ' . nl_drop_date( $L['modified'], $lang ) ) . '</span></p>' . "\n";
	$wa = nl_drop_wa_link( $b, $lang, $ttl );
	$h .= '<div class="nlb-lcard-cta">';
	if ( $wa ) { $h .= '<a class="nlb-btn nlb-btn--sea" href="' . esc_url( $wa ) . '" target="_blank" rel="noopener" aria-label="' . esc_attr( nl_drop_t( $lang, 'wa' ) . ': ' . $ttl ) . '">' . nl_drop_icon( 'wa' ) . '<span>' . esc_html( nl_drop_t( $lang, 'wa' ) ) . '</span></a>'; }
	$h .= '<a class="nlb-btn nlb-btn--line" href="' . esc_url( $url ) . '" aria-label="' . esc_attr( nl_drop_t( $lang, 'card_view' ) . ': ' . $ttl ) . '"><span>' . esc_html( nl_drop_t( $lang, 'card_view' ) ) . '</span>' . nl_drop_icon( 'arrow' ) . '</a>';
	$h .= '</div>' . "\n" . '</li>' . "\n";
	return $h;
}

/* =====================================================================================================
 * The broker's own site, built by the engine (1.1). A broker who joined alone gets a Hebrew site at once;
 * the English, Russian and French sites appear with the first listing written in that language.
 * Hand-built sites (Meital's Hebrew and English) keep their own markup and get cards injected at view time.
 * ===================================================================================================== */

/** The "for brokers" page of a language: /brokers/, /en/brokers/, /ru/brokers/, /fr/brokers/. Published, or none. */
function nl_drop_lang_parent( $lang ) {
	$lang = nl_drop_L( $lang );
	$p    = get_page_by_path( $lang === 'he' ? 'brokers' : $lang . '/brokers', OBJECT, 'page' );
	return ( $p && $p->post_status === 'publish' ) ? (int) $p->ID : 0;
}

/** The broker's Latin slug: saved, or the Hebrew site's own slug, or the English name. */
function nl_drop_broker_slug( $b ) {
	if ( ! empty( $b['slug'] ) && preg_match( '/^[a-z0-9-]+$/', $b['slug'] ) ) { return $b['slug']; }
	if ( ! empty( $b['site_he'] ) ) {
		$s = (string) get_post_field( 'post_name', (int) $b['site_he'] );
		if ( preg_match( '/^[a-z0-9-]+$/', $s ) ) { return $s; }
	}
	$s = sanitize_title( remove_accents( (string) $b['name_en'] ) );
	return preg_match( '/^[a-z0-9-]+$/', $s ) ? $s : '';
}

function nl_drop_site_title( $b, $lang ) {
	$brand = nl_drop_brand( $b, $lang );
	return nl_drop_name( $b, $lang ) . ( $brand !== '' ? ' · ' . $brand : '' );
}

/** Returns the broker's site page in a language, creating it (engine-built) when it does not exist yet. */
function nl_drop_site_ensure( $b, $lang, $status = 'publish' ) {
	$lang = nl_drop_L( $lang );
	if ( ( $b['kind'] ?? 'broker' ) !== 'broker' || empty( $b['id'] ) ) { return 0; }
	$id = (int) ( $b[ 'site_' . $lang ] ?? 0 );
	if ( $id && get_post( $id ) && get_post_status( $id ) !== 'trash' ) { return $id; }
	$parent = nl_drop_lang_parent( $lang );
	$slug   = nl_drop_broker_slug( $b );
	if ( ! $parent || $slug === '' ) { return 0; }
	$there = get_page_by_path( get_page_uri( $parent ) . '/' . $slug, OBJECT, 'page' );
	if ( $there ) {
		$own = (string) get_post_meta( $there->ID, 'nl_broker_auto', true ) === (string) $b['id'] || (string) get_post_meta( $there->ID, 'nl_broker_site', true ) === (string) $b['id'];
		if ( ! $own ) { return 0; }
		update_post_meta( (int) $b['id'], 'nl_site_' . $lang, (string) $there->ID );
		return (int) $there->ID;
	}
	$had = nl_drop_kses_off();
	$pid = wp_insert_post( array(
		'post_type'    => 'page',
		'post_status'  => $status,
		'post_parent'  => $parent,
		'post_name'    => $slug,
		'post_title'   => nl_drop_site_title( $b, $lang ),
		'post_content' => '',
		'post_author'  => nl_drop_author(),
	), true );
	nl_drop_kses_on( $had );
	if ( is_wp_error( $pid ) || ! $pid ) { return 0; }
	update_post_meta( $pid, 'nl_broker_auto', (string) $b['id'] );
	update_post_meta( $pid, 'nl_lang', $lang );
	update_post_meta( (int) $b['id'], 'nl_site_' . $lang, (string) $pid );
	return (int) $pid;
}

/** Re-writes every engine-built site page of the broker (after a new listing, a sale, a price) and clears the caches. */
function nl_drop_site_sync( $b ) {
	if ( ( $b['kind'] ?? 'broker' ) !== 'broker' || empty( $b['id'] ) ) { return; }
	$b = nl_drop_broker( $b['id'] );
	if ( ! $b ) { return; }
	$touched = array();
	$sites   = array();
	foreach ( nl_drop_langs() as $l ) {
		$pid = (int) ( $b[ 'site_' . $l ] ?? 0 );
		if ( $pid && get_post( $pid ) ) { $sites[ $l ] = $pid; }
	}
	$live = array();
	foreach ( $sites as $l => $pid ) { if ( get_post_status( $pid ) === 'publish' ) { $live[ $l ] = (string) get_permalink( $pid ); } }
	foreach ( $sites as $l => $pid ) {
		$touched[] = $pid;
		if ( (string) get_post_meta( $pid, 'nl_broker_auto', true ) !== (string) $b['id'] ) { continue; }
		$alts = $live;
		unset( $alts[ $l ] );
		$html = nl_drop_site_html( $b, $l, $pid, $alts );
		$had  = nl_drop_kses_off();
		wp_update_post( array( 'ID' => $pid, 'post_content' => $html, 'post_title' => nl_drop_site_title( $b, $l ) ) );
		nl_drop_kses_on( $had );
		$seo = nl_drop_site_seo( $b, $l );
		update_post_meta( $pid, '_yoast_wpseo_title', wp_slash( $seo[0] ) );
		update_post_meta( $pid, '_yoast_wpseo_metadesc', wp_slash( $seo[1] ) );
		if ( count( $live ) > 1 ) { update_post_meta( $pid, 'nl_hreflang', wp_slash( wp_json_encode( $live, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) ) ); }
	}
	nl_drop_purge( $touched );
}

/** The areas the broker works in, in a language: the broker's own list in Hebrew, the saved translation elsewhere. */
function nl_drop_areas( $b, $lang ) {
	$lang = nl_drop_L( $lang );
	$a    = (array) ( $b['areas_l'][ $lang ] ?? array() );
	if ( ! $a && $lang !== 'he' ) { $a = (array) ( $b['areas_l']['en'] ?? array() ); }
	return array_values( array_filter( $a ) );
}

function nl_drop_areas_phrase( $b, $lang, $max = 3 ) {
	$a = array_slice( nl_drop_areas( $b, $lang ), 0, $max );
	if ( ! $a ) { return ''; }
	$j = nl_drop_join( $a, $lang );
	return nl_drop_L( $lang ) === 'he' ? nl_drop_he_in( $j ) : $j;
}

function nl_drop_site_seo( $b, $lang ) {
	$lang  = nl_drop_L( $lang );
	$name  = nl_drop_name( $b, $lang );
	$brand = nl_drop_brand( $b, $lang );
	$areas = nl_drop_areas_phrase( $b, $lang, 2 );
	$title = $areas !== '' ? sprintf( nl_drop_t( $lang, 'seo_site_t' ), $name, $areas ) : sprintf( nl_drop_t( $lang, 'seo_site_t0' ), $name );
	$who   = trim( $name . ( $brand !== '' ? ', ' . $brand : '' ) . ( $b['license'] !== '' ? ', ' . nl_drop_t( $lang, $b['female'] ? 'lic_f' : 'lic_m' ) . ' ' . $b['license'] : '' ) );
	$areas = nl_drop_areas_phrase( $b, $lang, 3 );
	$desc  = $areas !== '' ? sprintf( nl_drop_t( $lang, 'seo_site_d' ), $who, $areas ) : sprintf( nl_drop_t( $lang, 'seo_site_d0' ), $who );
	return array( nl_drop_cut_words( $title, 70 ), nl_drop_cut_words( $desc, 158 ) );
}

function nl_drop_site_css() {
	return <<<'NLBCSS'
.nlb{
  --paper:#F7F6F2; --surf:#FFFFFF; --ink:#14212B; --ink2:#3B4753; --mute:#5F6B75; --line:#E3E1DA;
  --sea:#2F6F86; --seah:#255C70; --deep:#1F4B5C; --abyss:#10262F; --sand:#EEE9DD; --mist:#CFE3EA; --foam:#E8F1F3;
  --serif:'Noto Serif Hebrew','Frank Ruhl Libre','Times New Roman',serif;
  --sans:Assistant,'Segoe UI','Arial Hebrew',sans-serif;
  --gutter:clamp(16px,5.6vw,80px); --max:1440px;
  background:var(--paper); color:var(--ink); font-family:var(--sans); font-size:17px; line-height:1.6;
  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility; overflow-x:clip;
}
.nlb[lang="en"]{--serif:'Noto Serif Display','Noto Serif',Georgia,serif}
.nlb *,.nlb *::before,.nlb *::after{box-sizing:border-box}
.nlb img{max-width:100%;display:block}
.nlb a{color:inherit}
.nlb p{margin:0}
.nlb .nlb-wrap{max-width:var(--max);margin-inline:auto;padding-inline:var(--gutter)}
.nlb .nlb-num{font-variant-numeric:tabular-nums lining-nums;font-feature-settings:"tnum" 1,"lnum" 1;direction:ltr;unicode-bidi:isolate}
.nlb .nlb-eyebrow{display:flex;align-items:center;gap:14px;font-size:14px;font-weight:700;letter-spacing:.03em;color:var(--sea)}
.nlb[lang="en"] .nlb-eyebrow{letter-spacing:.14em;text-transform:uppercase;font-size:13px}
.nlb .nlb-eyebrow--line::before{content:"";width:40px;height:1px;background:currentColor;flex:none}
.nlb.nlb h1,.nlb.nlb h2,.nlb.nlb h3{font-family:var(--serif)!important;font-weight:400!important;color:inherit!important;margin:0!important;letter-spacing:0;text-wrap:balance}
.nlb .nlb-h2{font-size:clamp(34px,4.2vw,56px)!important;line-height:1.08!important}
.nlb .nlb-h2--xl{font-size:clamp(40px,5vw,72px)!important;line-height:1.05!important}
.nlb .nlb-lead{color:var(--ink2);max-width:62ch;font-size:clamp(16px,1.35vw,19px);line-height:1.65}
.nlb .nlb-sec{padding-block:clamp(56px,7.8vw,112px)}
.nlb .nlb-btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:52px;padding:0 26px;border-radius:999px;font-family:var(--sans);font-weight:700;font-size:16px;line-height:1;text-decoration:none!important;border:1px solid transparent;transition:background .2s ease,color .2s ease,border-color .2s ease;white-space:nowrap}
.nlb .nlb-btn svg{width:19px;height:19px;flex:none}
.nlb .nlb-btn--paper{background:var(--paper);color:var(--abyss)!important;border-color:var(--paper)}
.nlb .nlb-btn--paper svg{color:var(--sea)}
.nlb .nlb-btn--paper:hover{background:#fff}
.nlb .nlb-btn--ghost{background:transparent;color:var(--paper)!important;border-color:rgba(247,246,242,.42)}
.nlb .nlb-btn--ghost:hover{background:rgba(247,246,242,.1);border-color:rgba(247,246,242,.7)}
.nlb .nlb-btn--sea{background:var(--sea);color:#fff!important;border-color:var(--sea)}
.nlb .nlb-btn--sea:hover{background:var(--seah);border-color:var(--seah)}
.nlb .nlb-btn--abyss{background:var(--abyss);color:var(--paper)!important;border-color:var(--abyss)}
.nlb .nlb-btn--abyss:hover{background:var(--deep);border-color:var(--deep)}
.nlb .nlb-btn--line{background:transparent;color:var(--ink)!important;border-color:var(--ink)}
.nlb .nlb-btn--line:hover{background:var(--ink);color:var(--paper)!important}
.nlb .nlb-btn--white{background:#fff;color:var(--ink)!important;border-color:var(--line)}
.nlb .nlb-btn:focus-visible,.nlb a:focus-visible,.nlb label:focus-visible{outline:2px solid var(--sea);outline-offset:3px}
.nlb .nlb-cta{display:flex;flex-wrap:wrap;gap:12px}
.nlb .nlb-hero{position:relative;isolation:isolate;display:grid;grid-template-rows:1fr auto;min-height:clamp(760px,61vw,1000px);background:var(--abyss);color:var(--paper);overflow:hidden}
.nlb .nlb-hero-media{position:absolute;inset:0;z-index:-1}
.nlb .nlb-hero-media img,.nlb .nlb-scene,.nlb .nlb-scene svg{width:100%;height:100%;object-fit:cover}
.nlb .nlb-scene--tall{display:none}
.nlb .nlb-hero-in{width:100%;display:flex;flex-direction:column;align-items:flex-start;padding-block:clamp(88px,11vw,168px) clamp(150px,15vw,230px)}
.nlb .nlb-hero .nlb-eyebrow{color:var(--mist);font-size:15px}
.nlb.nlb .nlb-name{margin-top:26px!important;font-size:clamp(64px,10.4vw,150px)!important;line-height:1!important;letter-spacing:-.01em;color:var(--paper)!important;white-space:nowrap}
.nlb[lang="en"] .nlb-name{font-size:clamp(52px,8.9vw,128px)!important}
.nlb .nlb-brand{margin-top:20px;font-family:var(--serif);font-size:clamp(24px,2.9vw,42px);line-height:1.15;font-weight:300;color:var(--mist)}
.nlb[lang="en"] .nlb-brand{font-style:italic}
.nlb .nlb-hero .nlb-lede{margin-top:28px;max-width:600px;font-size:clamp(17px,1.46vw,21px);line-height:1.6;color:rgba(247,246,242,.86)}
.nlb .nlb-hero .nlb-cta{margin-top:40px}
.nlb .nlb-hero .nlb-btn{min-height:56px;font-size:17px}
.nlb .nlb-hero-meta{border-top:1px solid rgba(207,227,234,.18)}
.nlb .nlb-hero-meta-in{display:flex;align-items:center;gap:24px;min-height:104px}
.nlb .nlb-hero-meta dl{margin:0;display:flex;flex-wrap:wrap;gap:12px 64px}
.nlb .nlb-hero-meta dl div{display:flex;flex-direction:column;gap:6px}
.nlb .nlb-hero-meta dt{font-size:13px;font-weight:600;letter-spacing:.03em;color:var(--mist)}
.nlb .nlb-hero-meta dd{margin:0;font-size:22px;font-weight:600;color:var(--paper)}
.nlb .nlb-coords{margin-inline-start:auto;font-size:13px;letter-spacing:.06em;color:rgba(207,227,234,.7)}
.nlb .nlb-feature{display:grid;grid-template-columns:minmax(0,480px) minmax(0,1fr);gap:40px;align-items:center}
.nlb .nlb-feature-copy{display:flex;flex-direction:column}
.nlb .nlb-feature-copy .nlb-h2{margin-top:18px!important}
.nlb .nlb-feature-copy .nlb-lead{margin-top:22px}
.nlb .nlb-feature-stats{margin:30px 0 0;padding-top:22px;border-top:1px solid var(--line);display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.nlb .nlb-feature-stats dt{font-size:clamp(34px,3.1vw,44px);line-height:1;font-weight:300;color:var(--ink)}
.nlb .nlb-feature-stats dd{margin:8px 0 0;font-size:14px;color:var(--mute)}
.nlb .nlb-feature-amen{margin-top:26px;font-size:16px;color:var(--ink2)}
.nlb .nlb-price-tag{margin-top:26px;display:flex;flex-direction:column;gap:4px}
.nlb .nlb-price-tag strong{font-size:24px;font-weight:800;color:var(--ink)}
.nlb .nlb-price-tag span{font-size:15px;color:var(--mute)}
.nlb .nlb-feature-copy .nlb-cta{margin-top:30px}
.nlb .nlb-feature-media{position:relative;margin:0;height:600px;border-radius:22px;overflow:hidden;background:var(--abyss)}
.nlb .nlb-feature-media img,.nlb .nlb-feature-media>svg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.nlb .nlb-code{position:absolute;display:inline-flex;align-items:center;height:26px;padding:0 10px;border-radius:7px;background:rgba(16,38,47,.62);color:var(--paper);font-size:12.5px;font-weight:700;letter-spacing:.06em}
.nlb .nlb-feature-media .nlb-code{top:20px;inset-inline-start:20px}
.nlb .nlb-illus{position:absolute;bottom:18px;inset-inline-end:20px;font-size:12px;font-weight:600;letter-spacing:.04em;color:rgba(207,227,234,.72)}
.nlb .nlb-numbers{background:var(--surf);border-block:1px solid var(--line)}
.nlb .nlb-numbers-in{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,456px);gap:64px;align-items:start}
.nlb .nlb-numbers-copy{display:flex;flex-direction:column}
.nlb .nlb-numbers-copy .nlb-h2{margin-top:18px!important;font-size:clamp(32px,3.6vw,52px)!important}
.nlb .nlb-numbers-copy .nlb-lead{margin-top:18px;font-size:clamp(16px,1.25vw,18px)}
.nlb .nlb-ladders{margin-top:48px;display:flex;flex-direction:column;gap:44px}
.nlb .nlb-ladder{display:flex;flex-direction:column;gap:12px}
.nlb .nlb-ladder-head{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:6px 16px}
.nlb .nlb-ladder-label{display:flex;align-items:baseline;gap:10px}
.nlb .nlb-ladder-label b{font-size:21px;font-weight:700}
.nlb .nlb-ladder-label span{font-size:15px;color:var(--mute)}
.nlb .nlb-ladder-range{display:flex;align-items:baseline;gap:8px}
.nlb .nlb-ladder-range .nlb-num{font-family:var(--serif);font-size:clamp(28px,2.4vw,34px);line-height:1.1}
.nlb .nlb-ladder-range small{font-size:15px;font-weight:600;color:var(--mute)}
.nlb .nlb-track svg{display:block;width:100%;height:auto;overflow:visible}
.nlb .nlb-track--narrow{display:none}
.nlb .nlb-chips{display:flex;flex-wrap:wrap;gap:8px}
.nlb .nlb-chip{display:inline-flex;align-items:center;gap:8px;min-height:32px;padding:0 12px;border-radius:999px;border:1px solid var(--line);background:var(--paper);font-size:14px;color:var(--ink2);text-decoration:none;white-space:nowrap}
.nlb .nlb-chip b{font-weight:800;color:var(--ink);letter-spacing:.04em}
.nlb .nlb-chip:hover{border-color:var(--sea)}
.nlb .nlb-chip--ask{background:transparent;border-style:dashed;border-color:#AEB8BF;color:var(--mute)}
.nlb .nlb-map{margin:0}
.nlb .nlb-map svg{display:block;width:100%;height:auto;border-radius:14px;border:1px solid var(--line)}
.nlb .nlb-map figcaption{margin-top:12px;font-size:13px;line-height:1.5;color:var(--mute)}
.nlb .nlb-listings-top{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:24px 40px;margin-bottom:48px}
.nlb .nlb-listings-head{max-width:720px;display:flex;flex-direction:column}
.nlb .nlb-listings-head .nlb-h2{margin-top:18px!important}
.nlb .nlb-listings-head .nlb-lead{margin-top:18px}
.nlb .nlb-f{position:absolute;opacity:0;pointer-events:none}
.nlb .nlb-filters{display:flex;gap:8px}
.nlb .nlb-filters label{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 20px;border-radius:999px;border:1px solid var(--line);font-weight:700;font-size:15px;color:var(--ink);cursor:pointer;user-select:none;transition:background .2s ease,color .2s ease,border-color .2s ease}
.nlb .nlb-filters label span{opacity:.72}
.nlb .nlb-f-all:checked ~ .nlb-listings-top label.nlb-l-all,
.nlb .nlb-f-sale:checked ~ .nlb-listings-top label.nlb-l-sale,
.nlb .nlb-f-rent:checked ~ .nlb-listings-top label.nlb-l-rent{background:var(--ink);border-color:var(--ink);color:var(--paper)}
.nlb .nlb-f:focus-visible ~ .nlb-listings-top .nlb-filters{outline:2px solid var(--sea);outline-offset:4px;border-radius:999px}
.nlb .nlb-f-sale:checked ~ .nlb-grid .nlb-lcard[data-deal="rent"],
.nlb .nlb-f-rent:checked ~ .nlb-grid .nlb-lcard[data-deal="sale"]{display:none}
.nlb .nlb-grid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));column-gap:32px;row-gap:36px}
.nlb .nlb-lcard{position:relative;display:flex;flex-direction:column;background:var(--surf);border:1px solid var(--line);border-radius:10px;overflow:hidden;transition:box-shadow .25s ease,border-color .25s ease}
@supports (grid-template-rows:subgrid){
  .nlb .nlb-lcard,.nlb .nlb-igtile{display:grid;grid-row:span 9;grid-template-rows:subgrid;row-gap:0}
}
.nlb .nlb-lcard:hover{box-shadow:0 18px 40px rgba(16,38,47,.10),0 3px 10px rgba(16,38,47,.05);border-color:#D6D3CA}
.nlb .nlb-lcard>*:not(.nlb-lcard-media){padding-inline:22px}
.nlb .nlb-lcard-media{position:relative;display:block;height:224px;background:var(--abyss);overflow:hidden}
.nlb .nlb-lcard-media img,.nlb .nlb-lcard-media>svg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .6s ease}
.nlb .nlb-lcard:hover .nlb-lcard-media img{transform:scale(1.03)}
.nlb .nlb-badges{position:absolute;top:14px;inset-inline-start:14px;inset-inline-end:64px;display:flex;flex-wrap:wrap;gap:6px}
.nlb .nlb-badge{display:inline-flex;align-items:center;height:28px;padding:0 12px;border-radius:999px;font-size:13px;font-weight:700;white-space:nowrap}
.nlb .nlb-badge--sale{background:var(--abyss);color:var(--paper)}
.nlb .nlb-badge--rent{background:var(--paper);color:var(--abyss)}
.nlb .nlb-badge--note{background:var(--mist);color:var(--abyss)}
.nlb .nlb-badge--review{background:var(--sand);color:var(--ink)}
.nlb .nlb-lcard-media .nlb-code{bottom:12px;inset-inline-end:12px;height:24px;padding:0 9px;font-size:12px}
.nlb .nlb-lcard-kicker{padding-top:22px;font-size:13px;line-height:1.3;font-weight:700;letter-spacing:.02em;color:var(--sea)}
.nlb[lang="en"] .nlb-lcard-kicker{letter-spacing:.06em}
.nlb.nlb .nlb-lcard-title{padding-top:8px!important;font-size:22px!important;line-height:1.3!important;font-weight:500!important}
.nlb[lang="en"] .nlb-lcard-title{font-size:21px!important}
.nlb .nlb-lcard-title a{text-decoration:none}
.nlb .nlb-lcard-title a::after{content:"";position:absolute;inset:0;z-index:0}
.nlb .nlb-lcard-title a:hover{color:var(--sea)}
.nlb .nlb-lcard-cta,.nlb .nlb-chip{position:relative;z-index:1}
.nlb .nlb-price{padding-top:12px;display:flex;flex-direction:column;justify-content:center;gap:4px;min-height:70px}
.nlb .nlb-price strong{display:flex;align-items:baseline;gap:8px;font-size:27px;line-height:1.15;font-weight:800;color:var(--ink);white-space:nowrap}
.nlb .nlb-price strong small{font-size:15px;font-weight:600;color:var(--mute)}
.nlb .nlb-price strong.nlb-ask{font-size:23px}
.nlb .nlb-price>span{font-size:14px;line-height:1.3;color:var(--mute)}
.nlb .nlb-specs{list-style:none;margin:16px 22px 0;padding:16px 0 0!important;border-top:1px solid var(--line);display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 14px;align-content:start}
.nlb .nlb-specs li{display:flex;align-items:center;gap:8px;min-width:0;font-size:15px;line-height:1.3;font-weight:600;color:var(--ink)}
.nlb[lang="en"] .nlb-specs li{font-size:14px}
.nlb .nlb-specs svg{width:18px;height:18px;flex:none;color:var(--sea)}
.nlb .nlb-hi{list-style:none;margin:0;padding-top:16px;display:flex;flex-direction:column;gap:5px}
.nlb .nlb-hi li{position:relative;padding-inline-start:15px;font-size:14.5px;line-height:1.45;color:var(--ink2)}
.nlb[lang="en"] .nlb-hi li{font-size:14px}
.nlb .nlb-hi li::before{content:"";position:absolute;inset-inline-start:0;top:.56em;width:5px;height:5px;border-radius:50%;background:var(--sea)}
.nlb .nlb-amen{padding-top:14px;display:flex;flex-wrap:wrap;align-content:flex-start;gap:6px}
.nlb .nlb-amen span{display:inline-flex;align-items:center;gap:6px;height:28px;padding:0 10px;border-radius:999px;background:var(--foam);color:var(--deep);font-size:13px;font-weight:600;white-space:nowrap}
.nlb .nlb-amen svg{width:14px;height:14px}
.nlb .nlb-lcard-meta{margin:16px 22px 0;padding:12px 0 0!important;border-top:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;gap:12px;font-size:13px;color:var(--mute)}
.nlb .nlb-lcard-meta span:first-child{display:flex;align-items:center;gap:7px;font-size:14px;font-weight:600;color:var(--ink)}
.nlb .nlb-lcard-meta svg{width:16px;height:16px;color:var(--sea);flex:none}
.nlb .nlb-lcard-cta{padding-block:14px 22px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;align-self:end}
.nlb .nlb-lcard-cta .nlb-btn{min-height:44px;padding:0 12px;font-size:15px;gap:8px}
.nlb .nlb-lcard-cta .nlb-btn svg{width:17px;height:17px}
.nlb .nlb-igtile{display:flex;flex-direction:column;justify-content:space-between;gap:28px;padding:32px;background:var(--abyss);color:var(--paper);border-radius:10px}
@supports (grid-template-rows:subgrid){.nlb .nlb-igtile{display:flex}}
.nlb .nlb-igtile-top{display:flex;flex-direction:column;gap:16px}
.nlb .nlb-igtile-top>svg{width:30px;height:30px;color:var(--mist)}
.nlb .nlb-igtile .nlb-eyebrow{color:var(--mist);font-size:13px}
.nlb .nlb-igtile-handle{font-family:'Noto Serif Display','Noto Serif',Georgia,serif;font-size:25px;line-height:1.25;overflow-wrap:anywhere;text-align:start}
.nlb[dir="rtl"] .nlb-igtile-handle{text-align:end}
.nlb .nlb-igtile-lead{font-size:16px;color:rgba(247,246,242,.8)}
.nlb .nlb-igtile-bottom{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:18px}
.nlb .nlb-igtile-qr{display:flex;flex-direction:column;gap:10px;font-size:13px;color:var(--mist)}
.nlb .nlb-igtile-qr svg{width:144px;height:144px;padding:12px;background:#fff;border-radius:8px}
.nlb .nlb-igtile .nlb-btn{min-height:44px;padding:0 18px;font-size:15px}
.nlb .nlb-sec-head{display:flex;flex-direction:column;gap:16px;margin-bottom:40px}
.nlb .nlb-strip{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(240px,300px);gap:12px;overflow-x:auto;padding-bottom:12px;scroll-snap-type:x mandatory}
.nlb .nlb-strip figure{margin:0;scroll-snap-align:start;display:grid;gap:8px}
.nlb .nlb-strip img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:10px;background:var(--sand)}
.nlb .nlb-strip figcaption{font-size:13px;color:var(--mute)}
.nlb .nlb-cardsec{background:var(--sand);padding-block:clamp(56px,6.7vw,96px)}
.nlb .nlb-cardsec-in{display:grid;grid-template-columns:minmax(0,360px) minmax(0,1fr);gap:56px;align-items:center}
.nlb .nlb-cardsec-head{display:flex;flex-direction:column}
.nlb .nlb-cardsec-head .nlb-h2{margin-top:18px!important;font-size:clamp(32px,2.9vw,42px)!important;line-height:1.12!important}
.nlb .nlb-cardsec-head .nlb-lead{margin-top:18px;font-size:17px}
.nlb .nlb-bcards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
.nlb .nlb-bcard{position:relative;container-type:inline-size;aspect-ratio:1050/600;border-radius:12px;overflow:hidden}
.nlb .nlb-bcard--front{background:var(--abyss);color:var(--paper);box-shadow:0 18px 40px rgba(16,38,47,.18)}
.nlb .nlb-bcard-scene,.nlb .nlb-bcard-scene svg{position:absolute;inset:0;width:100%;height:100%}
.nlb .nlb-bcard-in{position:absolute;inset:0;padding:6.1cqw;display:flex;flex-direction:column;justify-content:space-between}
.nlb .nlb-bcard-brand{display:flex;align-items:center;gap:1.7cqw;font-family:var(--serif);font-size:3.62cqw;line-height:1.2;font-weight:300;color:var(--mist)}
.nlb .nlb-bcard-brand::before{content:"";width:5.3cqw;height:1px;background:var(--mist)}
.nlb .nlb-bcard-name{font-family:var(--serif);font-size:9.9cqw;line-height:1;white-space:nowrap}
.nlb[lang="en"] .nlb-bcard-name{font-size:8.8cqw}
.nlb .nlb-bcard-role{margin-top:1.33cqw;font-size:2.48cqw;font-weight:600;letter-spacing:.02em;color:var(--mist)}
.nlb .nlb-bcard--back{background:#fff;color:var(--ink);box-shadow:0 18px 40px rgba(16,38,47,.12);padding:6.1cqw;display:flex;flex-direction:column;justify-content:space-between}
.nlb .nlb-bcard-back-in{display:flex;align-items:center;justify-content:space-between;gap:3.8cqw}
.nlb .nlb-bcard-rows{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:2.48cqw}
.nlb .nlb-bcard-rows li{display:flex;align-items:center;gap:1.9cqw;font-size:2.67cqw;line-height:1.25;font-weight:600}
.nlb .nlb-bcard-rows svg{width:2.67cqw;height:2.67cqw;min-width:10px;min-height:10px;color:var(--sea);flex:none}
.nlb .nlb-qr{display:flex;flex-direction:column;align-items:center;gap:1.14cqw;font-size:1.81cqw;font-weight:600;color:var(--mute)}
.nlb .nlb-qr svg{width:20cqw;height:20cqw}
.nlb .nlb-bcard-url{display:flex;align-items:center;gap:1.7cqw;font-size:1.71cqw;font-weight:600;letter-spacing:.02em;color:var(--mute)}
.nlb .nlb-bcard-url::before{content:"";flex:1;height:1px;background:var(--sea);opacity:.45}
.nlb .nlb-contact{background:var(--abyss);color:var(--paper);padding-block:clamp(56px,7.8vw,112px) clamp(40px,4.5vw,64px)}
.nlb .nlb-contact-top{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:32px 48px}
.nlb .nlb-contact-copy{max-width:760px;display:flex;flex-direction:column}
.nlb .nlb-contact .nlb-eyebrow{color:var(--mist)}
.nlb .nlb-contact .nlb-h2{margin-top:20px!important;color:var(--paper)!important}
.nlb .nlb-contact-copy p:last-child{margin-top:18px;font-size:clamp(16px,1.4vw,20px);color:rgba(207,227,234,.9)}
.nlb .nlb-contact .nlb-btn{min-height:56px;font-size:17px}
.nlb .nlb-method{margin-top:clamp(48px,5.6vw,80px);padding-top:40px;border-top:1px solid rgba(207,227,234,.18);display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:48px}
.nlb .nlb-method div{display:flex;flex-direction:column;gap:10px}
.nlb.nlb .nlb-method h3{font-family:var(--sans)!important;font-size:18px!important;font-weight:700!important;color:var(--paper)!important}
.nlb .nlb-method p{font-size:15px;color:rgba(207,227,234,.82)}
.nlb .nlb-legal{margin-top:48px;max-width:980px;font-size:13px;line-height:1.7;color:rgba(207,227,234,.66)}
.nlb .nlb-mbar{display:none}
@media (max-width:1180px){
  .nlb .nlb-grid{grid-template-columns:repeat(2,minmax(0,1fr));column-gap:24px}
  .nlb .nlb-feature{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
  .nlb .nlb-numbers-in{grid-template-columns:minmax(0,1fr) minmax(0,380px);gap:48px}
}
@media (max-width:1024px){
  .nlb .nlb-feature,.nlb .nlb-numbers-in,.nlb .nlb-cardsec-in{grid-template-columns:minmax(0,1fr)}
  .nlb .nlb-feature-media{order:-1;height:auto;aspect-ratio:4/3}
  .nlb .nlb-map{max-width:520px}
  .nlb .nlb-method{grid-template-columns:minmax(0,1fr);gap:24px}
  .nlb .nlb-coords{display:none}
}
@media (max-width:720px){
  .nlb{font-size:16px}
  .nlb .nlb-scene--wide{display:none}
  .nlb .nlb-scene--tall{display:block}
  .nlb .nlb-hero{min-height:0}
  .nlb .nlb-hero-in{padding-block:56px 150px;align-items:stretch}
  .nlb .nlb-hero .nlb-eyebrow{font-size:13px}
  .nlb.nlb .nlb-name{margin-top:18px!important;font-size:clamp(52px,17vw,68px)!important;white-space:normal}
  .nlb[lang="en"] .nlb-name{font-size:clamp(44px,14vw,56px)!important}
  .nlb .nlb-brand{margin-top:10px}
  .nlb .nlb-hero .nlb-lede{margin-top:18px}
  .nlb .nlb-hero .nlb-cta{margin-top:26px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
  .nlb .nlb-hero .nlb-cta .nlb-btn:first-child{grid-column:1/-1}
  .nlb .nlb-hero .nlb-btn{min-height:48px;font-size:15px;padding:0 10px}
  .nlb .nlb-hero .nlb-cta .nlb-btn:first-child{min-height:52px;font-size:16px}
  .nlb .nlb-hero-meta-in{min-height:76px}
  .nlb .nlb-hero-meta dl{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;width:100%}
  .nlb .nlb-hero-meta dt{font-size:11px}
  .nlb .nlb-hero-meta dd{font-size:15px}
  .nlb .nlb-feature-sec{padding-top:0}
  .nlb .nlb-feature{gap:36px}
  .nlb .nlb-feature-media{margin-inline:calc(var(--gutter) * -1);border-radius:0;aspect-ratio:auto;height:300px}
  .nlb .nlb-feature-stats{grid-template-columns:repeat(2,minmax(0,1fr));gap:0 20px;padding-top:0;border-top:0}
  .nlb .nlb-feature-stats div{padding-block:14px;border-top:1px solid var(--line)}
  .nlb .nlb-feature-copy .nlb-cta,.nlb .nlb-contact .nlb-cta{display:grid;grid-template-columns:minmax(0,1fr);width:100%}
  .nlb .nlb-track--wide{display:none}
  .nlb .nlb-track--narrow{display:block}
  .nlb .nlb-grid{grid-template-columns:minmax(0,1fr);row-gap:20px}
  .nlb .nlb-lcard,.nlb .nlb-igtile{grid-row:auto!important;display:flex!important;flex-direction:column}
  .nlb .nlb-lcard-media{height:214px}
  .nlb .nlb-lcard>*:not(.nlb-lcard-media){padding-inline:20px}
  .nlb .nlb-specs,.nlb .nlb-lcard-meta{margin-inline:20px}
  .nlb .nlb-filters{width:100%}
  .nlb .nlb-filters label{padding:0 16px;min-height:40px;font-size:14px}
  .nlb .nlb-contact-top{align-items:stretch}
  .nlb .nlb-contact{padding-bottom:112px}
  .nlb .nlb-mbar{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;position:sticky;bottom:0;z-index:30;padding:12px 16px calc(16px + env(safe-area-inset-bottom,0px));background:rgba(247,246,242,.97);border-top:1px solid var(--line)}
  .nlb .nlb-mbar .nlb-btn{min-height:48px;font-size:16px;padding:0 10px}
}
@media (max-width:400px){
  .nlb .nlb-lcard-cta .nlb-btn{font-size:14px}
}
@media (max-width:359px){
  .nlb .nlb-hero-meta dl{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (prefers-reduced-motion:reduce){.nlb *{transition:none!important}}
@media print{.nlb .nlb-mbar,.nlb .nlb-cta,.nlb .nlb-lcard-cta,.nlb .nlb-filters{display:none!important}}
.nlb-site-nav{position:sticky;top:var(--nlb-top,0px);z-index:40;background:rgba(247,246,242,.94);backdrop-filter:saturate(1.2) blur(8px);border-block-end:1px solid var(--line,#E3E1DA)}
.nlb-site-nav .nlb-wrap{display:flex;align-items:center;justify-content:space-between;gap:18px;min-height:58px;flex-wrap:wrap}
.nlb-site-brand{display:flex;flex-direction:column;line-height:1.15}
.nlb-site-brand b{font-family:var(--serif,'Noto Serif Hebrew',Georgia,serif);font-size:17px;font-weight:600;color:var(--ink,#14212B)}
.nlb-site-brand span{font-size:12.5px;color:var(--mute,#6B7680);letter-spacing:.02em}
.nlb-site-links{display:flex;gap:4px;flex-wrap:wrap;align-items:center}
.nlb-site-links a{font-size:14.5px;color:var(--ink-2,#3B4753)!important;text-decoration:none;padding:7px 12px;border-radius:999px;white-space:nowrap;display:inline-block;transition:background .18s ease,color .18s ease}
.nlb-site-links a:hover,.nlb-site-links a.is-active{background:var(--sand,#EEE9DD);color:var(--ink,#14212B)!important}
.nlb-site-links a.is-cta{background:var(--sea,#2F6F86);color:#fff!important;font-weight:600}
.nlb-site-links a.is-cta:hover{background:var(--sea-hover,#255C70);color:#fff!important}
.nlb-site-links a.is-lang{border:1px solid var(--line,#E3E1DA);font-weight:600;font-size:13.5px}
@media (max-width:760px){.nlb-site-nav{position:static}.nlb-site-links{width:100%;overflow-x:auto;flex-wrap:nowrap;padding-block-end:6px;-webkit-overflow-scrolling:touch;scrollbar-width:none}.nlb-site-links::-webkit-scrollbar{display:none}}
.nlb [id]{scroll-margin-top:calc(var(--nlb-top,0px) + 72px)}
.nlb .nlb-hero-media{position:absolute;inset:0;z-index:-1;overflow:hidden;background:#1F4B5C}
.nlb .nlb-hero-media img{width:100%;height:100%;object-fit:cover;object-position:center 58%;transform:scale(1.06);animation:nlb-settle 16s ease-out forwards}
@media (max-width:700px){.nlb .nlb-hero-media img{object-position:60% center}}
@keyframes nlb-settle{to{transform:scale(1)}}
@media (prefers-reduced-motion:reduce){.nlb .nlb-hero-media img{animation:none;transform:none}}
.nlb .nlb-hero-media::after{content:'';position:absolute;inset:0;background:linear-gradient(to top,rgba(16,38,47,.94) 0%,rgba(16,38,47,.58) 38%,rgba(16,38,47,.16) 72%,rgba(16,38,47,.02) 100%),linear-gradient(to left,rgba(16,38,47,.46) 0%,rgba(16,38,47,0) 55%)}
.nlb[dir="ltr"] .nlb-hero-media::after{background:linear-gradient(to top,rgba(16,38,47,.94) 0%,rgba(16,38,47,.58) 38%,rgba(16,38,47,.16) 72%,rgba(16,38,47,.02) 100%),linear-gradient(to right,rgba(16,38,47,.46) 0%,rgba(16,38,47,0) 55%)}
.nlb .nlb-coords{display:none!important}
.nlb-intro{background:var(--paper,#F7F6F2)}
.nlb-intro .nlb-wrap{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:clamp(24px,5vw,72px);align-items:center;padding-block:clamp(44px,6vw,84px)}
.nlb-intro h2{font-family:var(--serif,'Noto Serif Hebrew',Georgia,serif);font-size:clamp(26px,3.4vw,40px);font-weight:600;line-height:1.2;margin:0 0 18px;color:var(--ink,#14212B);text-wrap:balance}
.nlb-intro p{margin:0 0 14px;font-size:clamp(16px,1.6vw,18px);line-height:1.75;color:var(--ink-2,#3B4753);max-width:60ch}
.nlb-intro-portrait{aspect-ratio:4/5;border-radius:14px;overflow:hidden;background:var(--sand,#EEE9DD);max-width:440px;justify-self:start;margin:0}
.nlb-intro-portrait img{width:100%;height:100%;object-fit:cover;display:block}
@media (max-width:820px){.nlb-intro .nlb-wrap{grid-template-columns:minmax(0,1fr)}.nlb-intro-portrait{max-width:340px;justify-self:center}}
.nlb-areas{background:var(--surface,#fff);border-block:1px solid var(--line,#E3E1DA)}
.nlb-areas .nlb-wrap{padding-block:clamp(34px,4.5vw,64px)}
.nlb-areas h2{font-family:var(--serif,'Noto Serif Hebrew',Georgia,serif);font-size:clamp(24px,2.8vw,32px);font-weight:600;margin:0 0 6px;color:var(--ink,#14212B)}
.nlb-areas>.nlb-wrap>p{margin:0 0 22px;color:var(--mute,#6B7680);font-size:15.5px}
.nlb-areagrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:0;padding:0;list-style:none}
.nlb-areagrid li{margin:0}
.nlb-areagrid a{position:relative;display:block;aspect-ratio:4/3;border-radius:12px;overflow:hidden;background:var(--sand,#EEE9DD);color:#fff!important;text-decoration:none;isolation:isolate}
.nlb-areagrid img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .6s ease;z-index:-1}
.nlb-areagrid a::after{content:'';position:absolute;inset:0;background:linear-gradient(to top,rgba(16,38,47,.82) 0%,rgba(16,38,47,.25) 55%,rgba(16,38,47,.05) 100%);z-index:0}
.nlb-areagrid a:hover img{transform:scale(1.04)}
.nlb-areagrid .nlb-areaname{position:absolute;inset-inline:16px;inset-block-end:14px;z-index:1;display:flex;align-items:baseline;justify-content:space-between;gap:10px}
.nlb-areagrid .nlb-areaname b{font-family:var(--serif,'Noto Serif Hebrew',Georgia,serif);font-size:clamp(18px,2vw,23px);font-weight:600;letter-spacing:.005em}
.nlb-areagrid .nlb-areaname em{font-style:normal;font-size:13px;opacity:.9}
@media (max-width:700px){.nlb-areagrid{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.nlb-areagrid a{aspect-ratio:1/1}}
.nlb .nlb-lcard-media{aspect-ratio:4/5}
.nlb .nlb-lcard-media img{object-position:center}
.nlb .nlb-code{display:none!important}
.nlb .nlb-igtile .nlb-handle{direction:ltr;unicode-bidi:isolate;font-size:.84em;letter-spacing:-.01em;display:inline-block}
NLBCSS;
}

function nl_drop_site_js( $lang ) {
	return "<script>(function(){var nav=document.querySelector('.nlb-site-nav');if(!nav)return;var art=nav.closest('.nlb');function top(){var h=document.querySelector('header.wp-block-template-part,.header-luxury,.nlpc-site-header');var t=h?Math.round(h.getBoundingClientRect().height):0;if(art)art.style.setProperty('--nlb-top',t+'px');return t;}top();window.addEventListener('resize',top);var links=[].slice.call(nav.querySelectorAll('a[href^=\"#\"]'));var byId={};links.forEach(function(a){var id=a.getAttribute('href').slice(1);byId[id]=a;a.addEventListener('click',function(e){var t=document.getElementById(id);var f=(id==='sale'||id==='rent')?document.getElementById('nlb-f-" . nl_drop_L( $lang ) . "-'+id):null;if(f){f.checked=true;f.dispatchEvent(new Event('change',{bubbles:true}));t=document.getElementById('listings');}if(!t)return;e.preventDefault();var y=t.getBoundingClientRect().top+window.pageYOffset-top()-(nav.offsetHeight||58)-8;window.scrollTo({top:y,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});history.replaceState(null,'','#'+id);});});if(!('IntersectionObserver' in window))return;var io=new IntersectionObserver(function(es){es.forEach(function(en){if(!en.isIntersecting)return;links.forEach(function(a){a.classList.remove('is-active')});var a=byId[en.target.id];if(a)a.classList.add('is-active');});},{rootMargin:'-40% 0px -55% 0px'});['about','listings','contact'].forEach(function(id){var el=document.getElementById(id);if(el)io.observe(el);});})();</script>";
}

/**
 * The whole site page of a broker in one language: the same design and classes as the approved hand-built site.
 * @param array $alts lang => url of the broker's other published site pages
 */
function nl_drop_site_html( $b, $lang, $pid = 0, $alts = array() ) {
	$lang  = nl_drop_L( $lang );
	$he    = $lang === 'he';
	$name  = nl_drop_name( $b, $lang );
	$brand = nl_drop_brand( $b, $lang );
	$first = trim( (string) preg_split( '/\s+/u', $name )[0] );
	$aid   = 'nlb-' . ( $b['slug'] !== '' ? $b['slug'] : 'b' . (int) $b['id'] ) . '-' . $lang;
	$live  = array();
	foreach ( nl_drop_broker_listings( $b['id'], $lang ) as $L ) {
		if ( $L['source'] === 'broker_drop' && $L['status'] === 'active' ) { $live[] = $L; }
	}
	$cards = '';
	$n     = array( 'sale' => 0, 'rent' => 0 );
	foreach ( $live as $L ) {
		$card = nl_drop_card_html( $L, $lang, $b );
		if ( $card === '' ) { continue; }
		$cards .= $card;
		$n[ $L['deal'] ]++;
	}
	$total  = $n['sale'] + $n['rent'];
	$areas  = nl_drop_areas( $b, $lang );
	$bio    = trim( (string) ( $b['bio'][ $lang ] ?? '' ) );
	$wa     = $b['wa'] !== '' ? 'https://wa.me/' . rawurlencode( $b['wa'] ) . '?text=' . rawurlencode( sprintf( nl_drop_t( $lang, 'wa_site' ), $first ) ) : '';
	$tel    = $b['wa'] !== '' ? 'tel:+' . $b['wa'] : '';
	$phone  = $he ? $b['phone'] : $b['phone_intl'];
	$licln  = nl_drop_licence_line( $b, $lang );
	$hero   = '';
	if ( ! empty( $b['hero'] ) && wp_get_attachment_url( (int) $b['hero'] ) ) {
		$m    = wp_get_attachment_metadata( (int) $b['hero'] );
		$hero = '<img src="' . esc_url( wp_get_attachment_url( (int) $b['hero'] ) ) . '" alt="" width="' . (int) ( $m['width'] ?? 0 ) . '" height="' . (int) ( $m['height'] ?? 0 ) . '" loading="eager" decoding="async" fetchpriority="high">';
	} elseif ( $live ) {
		$d0 = nl_drop_data_for( $live[0]['id'], $b );
		$p0 = $d0 && ! empty( $d0['photos'][0] ) ? $d0['photos'][0] : null;
		if ( $p0 ) { $hero = '<img src="' . esc_url( $p0['url'] ) . '" alt="" width="' . (int) $p0['w'] . '" height="' . (int) $p0['h'] . '" loading="eager" decoding="async" fetchpriority="high">'; }
	}

	// navigation: the sections that exist, then the other languages
	$links = '<a href="#listings">' . esc_html( nl_drop_t( $lang, 'nav_listings' ) ) . '</a>';
	if ( $n['sale'] && $n['rent'] ) {
		$links .= '<a href="#sale">' . esc_html( nl_drop_t( $lang, 'nav_sale' ) ) . '</a><a href="#rent">' . esc_html( nl_drop_t( $lang, 'nav_rent' ) ) . '</a>';
	}
	if ( $bio !== '' ) { $links .= '<a href="#about">' . esc_html( nl_drop_t( $lang, 'nav_about' ) ) . '</a>'; }
	$links .= '<a href="#contact" class="is-cta">' . esc_html( nl_drop_t( $lang, 'nav_contact' ) ) . '</a>';
	foreach ( nl_drop_langs() as $al ) {
		if ( $al !== $lang && ! empty( $alts[ $al ] ) ) {
			$links .= '<a class="is-lang" href="' . esc_url( $alts[ $al ] ) . '" hreflang="' . $al . '" lang="' . $al . '">' . esc_html( nl_drop_lang_name( $al ) ) . '</a>';
		}
	}
	$btn_wa  = function ( $cls, $label ) use ( $wa ) { return $wa ? '<a class="nlb-btn ' . $cls . '" href="' . esc_url( $wa ) . '" target="_blank" rel="noopener">' . nl_drop_icon( 'wa' ) . '<span>' . esc_html( $label ) . '</span></a>' : ''; };
	$btn_tel = function ( $cls, $label ) use ( $tel ) { return $tel ? '<a class="nlb-btn ' . $cls . '" href="' . esc_url( $tel ) . '">' . nl_drop_icon( 'phone' ) . '<span class="nlb-num">' . esc_html( $label ) . '</span></a>' : ''; };

	$h  = '<article class="nlb" lang="' . $lang . '" dir="' . ( $he ? 'rtl' : 'ltr' ) . '" id="' . esc_attr( $aid ) . '">' . "\n";
	$h .= '<nav class="nlb-site-nav" aria-label="' . esc_attr( nl_drop_tn( $lang, 'nav_aria', $name ) ) . '"><div class="nlb-wrap"><span class="nlb-site-brand"><b>' . esc_html( $name ) . '</b>' . ( $brand !== '' ? '<span>' . esc_html( $brand ) . '</span>' : '' ) . '</span><span class="nlb-site-links">' . $links . '</span></div></nav>' . "\n";

	$lede = $areas ? sprintf( nl_drop_t( $lang, 'lede_areas' ), nl_drop_areas_phrase( $b, $lang, 4 ) ) : nl_drop_t( $lang, 'lede_plain' );
	$h .= '<header class="nlb-hero">' . "\n" . '<div class="nlb-hero-media" aria-hidden="true">' . $hero . '</div>' . "\n";
	$h .= '<div class="nlb-wrap nlb-hero-in">' . "\n" . '<p class="nlb-eyebrow nlb-eyebrow--line">' . esc_html( nl_drop_t( $lang, 'site_eyebrow' ) ) . '</p>' . "\n";
	$h .= '<h1 class="nlb-name">' . esc_html( $name ) . '</h1>' . "\n";
	if ( $brand !== '' ) { $h .= '<p class="nlb-brand">' . esc_html( $brand ) . '</p>' . "\n"; }
	$h .= '<p class="nlb-lede">' . esc_html( $lede ) . '</p>' . "\n";
	$h .= '<div class="nlb-cta">' . $btn_wa( 'nlb-btn--paper', nl_drop_t( $lang, 'wa' ) ) . $btn_tel( 'nlb-btn--ghost', $phone ) . '</div>' . "\n" . '</div>' . "\n";
	$stats = '';
	if ( $total ) { $stats .= '<div><dt>' . esc_html( nl_drop_t( $lang, 'stat_listings' ) ) . '</dt><dd><span class="nlb-num">' . (int) $total . '</span></dd></div>'; }
	if ( $areas ) { $stats .= '<div><dt>' . esc_html( nl_drop_t( $lang, 'stat_areas' ) ) . '</dt><dd>' . esc_html( nl_drop_join( array_slice( $areas, 0, 3 ), $lang ) ) . '</dd></div>'; }
	if ( $stats !== '' ) { $h .= '<div class="nlb-hero-meta"><div class="nlb-wrap nlb-hero-meta-in"><dl>' . $stats . '</dl></div></div>' . "\n"; }
	$h .= '</header>' . "\n";

	if ( $bio !== '' ) {
		$h .= '<section class="nlb-sec nlb-intro' . ( $b['portrait'] === '' ? ' nlb-intro--solo' : '' ) . '" id="about"><div class="nlb-wrap"><div><h2>' . esc_html( nl_drop_t( $lang, 'about_h2' ) ) . '</h2><p>' . esc_html( $bio ) . '</p></div>';
		if ( $b['portrait'] !== '' ) { $h .= '<figure class="nlb-intro-portrait"><img src="' . esc_url( $b['portrait'] ) . '" alt="' . esc_attr( $name ) . '" loading="lazy" decoding="async"></figure>'; }
		$h .= '</div></section>' . "\n";
	}

	$h .= '<section class="nlb-sec nlb-listings" id="listings">' . "\n" . '<div class="nlb-wrap">' . "\n";
	if ( $total && $n['sale'] && $n['rent'] ) {
		foreach ( array( 'all', 'sale', 'rent' ) as $k ) {
			$h .= '<input class="nlb-f nlb-f-' . $k . '" type="radio" name="nlb-f-' . $lang . '" id="nlb-f-' . $lang . '-' . $k . '"' . ( $k === 'all' ? ' checked' : '' ) . '>' . "\n";
		}
	}
	$h .= '<div class="nlb-listings-top">' . "\n" . '<div class="nlb-listings-head">' . "\n";
	$h .= '<p class="nlb-eyebrow nlb-eyebrow--line">' . esc_html( nl_drop_t( $lang, 'nav_listings' ) ) . '</p>' . "\n";
	$h .= '<h2 class="nlb-h2">' . esc_html( nl_drop_t( $lang, 'listings_h2' ) ) . '</h2>' . "\n";
	$h .= '<p class="nlb-lead">' . esc_html( $total ? nl_drop_t( $lang, 'listings_lead' ) : nl_drop_t( $lang, 'empty' ) ) . '</p>' . "\n" . '</div>' . "\n";
	if ( $total && $n['sale'] && $n['rent'] ) {
		$h .= '<div class="nlb-filters" role="group" aria-label="' . esc_attr( nl_drop_t( $lang, 'filter_aria' ) ) . '">';
		$h .= '<label class="nlb-l-all" for="nlb-f-' . $lang . '-all">' . esc_html( nl_drop_t( $lang, 'filter_all' ) ) . ' <span class="nlb-num">' . (int) $total . '</span></label>';
		$h .= '<label class="nlb-l-sale" for="nlb-f-' . $lang . '-sale">' . esc_html( nl_drop_t( $lang, 'nav_sale' ) ) . ' <span class="nlb-num">' . (int) $n['sale'] . '</span></label>';
		$h .= '<label class="nlb-l-rent" for="nlb-f-' . $lang . '-rent">' . esc_html( nl_drop_t( $lang, 'nav_rent' ) ) . ' <span class="nlb-num">' . (int) $n['rent'] . '</span></label>';
		$h .= '</div>' . "\n";
	}
	$h .= '</div>' . "\n";
	if ( $total ) { $h .= '<ul class="nlb-grid">' . "\n" . $cards . '</ul>' . "\n"; }
	$h .= '</div>' . "\n" . '</section>' . "\n";

	$h .= '<footer class="nlb-contact" id="contact">' . "\n" . '<div class="nlb-wrap">' . "\n" . '<div class="nlb-contact-top">' . "\n" . '<div class="nlb-contact-copy">' . "\n";
	$h .= '<p class="nlb-eyebrow nlb-eyebrow--line">' . esc_html( nl_drop_t( $lang, 'nav_contact' ) ) . '</p>' . "\n";
	$h .= '<h2 class="nlb-h2 nlb-h2--xl">' . esc_html( nl_drop_t( $lang, 'contact_h2' ) ) . '</h2>' . "\n";
	$h .= '<p>' . nl_drop_nums_html( trim( $name . ( $licln !== '' ? ', ' . $licln : '' ) ) ) . '.</p>' . "\n" . '</div>' . "\n";
	$h .= '<div class="nlb-cta">' . $btn_wa( 'nlb-btn--paper', nl_drop_t( $lang, 'wa' ) ) . $btn_tel( 'nlb-btn--ghost', $phone ) . '</div>' . "\n" . '</div>' . "\n";
	$h .= '<p class="nlb-legal">' . esc_html( nl_drop_tn( $lang, 'legal', $name ) ) . '</p>' . "\n" . '</div>' . "\n" . '</footer>' . "\n";
	if ( $wa || $tel ) {
		$h .= '<div class="nlb-mbar">' . $btn_wa( 'nlb-btn--sea', nl_drop_t( $lang, 'wa' ) ) . ( $tel ? '<a class="nlb-btn nlb-btn--white" href="' . esc_url( $tel ) . '">' . nl_drop_icon( 'phone' ) . '<span>' . esc_html( nl_drop_t( $lang, 'call' ) ) . '</span></a>' : '' ) . '</div>' . "\n";
	}
	$agent = array_filter( array(
		'@type'      => 'RealEstateAgent',
		'name'       => $name,
		'url'        => $pid ? (string) get_permalink( $pid ) : null,
		'telephone'  => $b['phone_intl'] !== '' ? $b['phone_intl'] : null,
		'areaServed' => $areas ? $areas : null,
		'image'      => $b['portrait'] !== '' ? $b['portrait'] : null,
		'address'    => array( '@type' => 'PostalAddress', 'addressCountry' => 'IL' ),
	) );
	if ( $brand !== '' ) { $agent['parentOrganization'] = array( '@type' => 'Organization', 'name' => $brand ); }
	$h .= '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@graph' => array( $agent ) ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
	$h .= nl_drop_site_js( $lang ) . "\n" . '</article>';

	$css = nl_drop_site_css();
	if ( $pid ) {
		$pid  = (int) $pid;
		$css .= "\nbody.page-id-{$pid} .entry-content.is-layout-constrained>*{max-width:none!important;margin-left:0!important;margin-right:0!important}"
			. "\nbody.page-id-{$pid} .entry-content{padding-left:0!important;padding-right:0!important}"
			. "\nbody.page-id-{$pid} .wp-block-post-featured-image,body.page-id-{$pid} .nlcta-start,body.page-id-{$pid} .nlcta-wa,body.page-id-{$pid} .yoast-breadcrumbs{display:none!important}";
	}
	$css .= "\n.nlb .nlb-hero-media:empty{background:linear-gradient(135deg,#1F4B5C 0%,#10262F 100%)}"
		. "\n.nlb .nlb-intro--solo{padding-block:clamp(36px,5vw,64px)}\n.nlb .nlb-intro--solo .nlb-wrap{grid-template-columns:minmax(0,1fr);padding-block:0}"
		. "\n.nlb .nlb-lcard-media{height:auto!important;width:100%}";
	return "<!-- wp:html -->\n<style>\n" . $css . "\n</style>\n" . $h . "\n<!-- /wp:html -->";
}

function nl_drop_is_current( $pid ) {
	return $pid && ! ( defined( 'REST_REQUEST' ) && REST_REQUEST ) && ! is_admin() && (int) $pid === (int) get_queried_object_id();
}

add_filter( 'the_content', function ( $html ) {
	$pid = (int) get_the_ID();
	if ( ! nl_drop_is_current( $pid ) ) { return $html; }
	$bid = (int) get_post_meta( $pid, 'nl_broker_site', true );
	if ( ! $bid || strpos( $html, '<ul class="nlb-grid">' ) === false ) { return $html; }
	$b = nl_drop_broker( $bid );
	if ( ! $b ) { return $html; }
	$lang = nl_drop_L( (string) get_post_meta( $pid, 'nl_lang', true ) ?: 'he' );
	$all  = nl_drop_broker_listings( $bid, $lang );
	foreach ( $all as $L ) {
		if ( $L['card_key'] !== '' && $L['status'] !== 'active' ) { $html = nl_drop_remove_li( $html, 'nlb-' . $lang . '-' . $L['card_key'] ); }
	}
	$cards = '';
	foreach ( $all as $L ) {
		if ( $L['source'] === 'broker_drop' && $L['status'] === 'active' ) { $cards .= nl_drop_card_html( $L, $lang, $b ); }
	}
	if ( $cards !== '' ) {
		$pos  = strpos( $html, '<ul class="nlb-grid">' ) + strlen( '<ul class="nlb-grid">' );
		$html = substr( $html, 0, $pos ) . "\n" . $cards . substr( $html, $pos );
	}
	$sale = substr_count( $html, 'class="nlb-lcard" data-deal="sale"' );
	$rent = substr_count( $html, 'class="nlb-lcard" data-deal="rent"' );
	$html = preg_replace_callback( '/(<label class="nlb-l-(all|sale|rent)"[^>]*>[^<]*<span class="nlb-num">)\d+(<\/span>)/u', function ( $m ) use ( $sale, $rent ) {
		$n = $m[2] === 'all' ? $sale + $rent : ( $m[2] === 'sale' ? $sale : $rent );
		return $m[1] . $n . $m[3];
	}, $html );
	$html = preg_replace_callback( '/(<dt>(?:נכסים|Listings)<\/dt><dd><span class="nlb-num">)\d+(<\/span>)/u', function ( $m ) use ( $sale, $rent ) {
		return $m[1] . ( $sale + $rent ) . $m[2];
	}, $html );
	return $html;
}, 26 );

/* A property that is off the market says so at the top, and stops asking for viewings (reg. 19(c)). */
add_filter( 'the_content', function ( $html ) {
	$pid = (int) get_the_ID();
	if ( ! nl_drop_is_current( $pid ) ) { return $html; }
	$st = (string) get_post_meta( $pid, 'nl_status', true );
	if ( $st !== 'sold' && $st !== 'rented' ) { return $html; }
	$at = strpos( $html, '<div class="nlx-wrap">' );
	if ( $at === false ) { return $html; }
	$lang = get_post_type( $pid ) === 'page' ? nl_drop_L( (string) get_post_meta( $pid, 'nl_lang', true ) ?: 'en' ) : 'he';
	$b    = nl_drop_broker( get_post_meta( $pid, 'nl_broker_id', true ) );
	$site = $b ? nl_drop_site_url( $b, $lang ) : '';
	$name = $b ? nl_drop_name( $b, $lang ) : '';
	$bar  = '<style>.nlx .nlx-soldbar{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;margin:16px 0 0;padding:12px 16px;border-radius:8px;background:#1F4B5C;color:#fff;font-weight:600}'
		. '.nlx .nlx-soldbar a{color:#fff!important;text-decoration:underline;font-weight:500}.nlx .nlx-rail .nlx-cta,.nlx .nlx-mbar,.nlx .nlx-agent .nlx-cta{display:none!important}</style>'
		. '<div class="nlx-soldbar" role="status"><span>' . esc_html( nl_drop_t( $lang, $st ) ) . '</span>'
		. ( $site ? '<a href="' . esc_url( $site ) . '">' . esc_html( nl_drop_tn( $lang, 'more', $name ) ) . '</a>' : '' ) . '</div>';
	$at += strlen( '<div class="nlx-wrap">' );
	return substr( $html, 0, $at ) . $bar . substr( $html, $at );
}, 25 );

/* =====================================================================================================
 * The address itself: /drop/<token>/  (a private tool page, never linked, never cached)
 * ===================================================================================================== */
add_action( 'parse_request', function () {
	$path = trim( (string) wp_parse_url( isset( $_SERVER['REQUEST_URI'] ) ? wp_unslash( $_SERVER['REQUEST_URI'] ) : '', PHP_URL_PATH ), '/' );
	if ( ! preg_match( '#^drop/([a-z0-9]{24})$#', $path, $m ) ) { return; }
	nl_drop_page( $m[1] );
	exit;
}, 0 );

function nl_drop_page( $token ) {
	do_action( 'litespeed_control_set_nocache', 'nadlan broker drop page' );
	nocache_headers();
	header( 'Cache-Control: no-store, private, max-age=0' );
	header( 'X-LiteSpeed-Cache-Control: no-cache' );
	header( 'Referrer-Policy: no-referrer' );
	header( 'X-Frame-Options: SAMEORIGIN' );
	header( 'Content-Type: text/html; charset=utf-8' );
	$b = nl_drop_broker_by_token( $token );
	if ( ! $b ) {
		status_header( 404 );
		echo '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>nad-lan</title></head><body style="font-family:Arial,sans-serif;padding:40px 16px;color:#14212B;background:#F7F6F2"><p>הקישור הזה לא פעיל.</p></body></html>';
		return;
	}
	status_header( 200 );
	$cfg = array(
		'api'  => esc_url_raw( rest_url( 'nadlan/v1/drop/' . $token ) ),
		'name' => $b['name_he'],
		'site' => nl_drop_site_url( $b, 'he' ),
	);
	$css = nl_drop_page_css();
	$js  = nl_drop_page_js();
	$ex  = 'למכירה, 4 חדרים, 110 מ״ר, קומה 5 מתוך 8, מרפסת 12 מ״ר, חניה ומחסן, ממ״ד. רמת אביב החדשה. 4,200,000 ש״ח. כניסה מיידית. בלעדיות.';
	echo '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">';
	echo '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="referrer" content="no-referrer">';
	echo '<meta name="theme-color" content="#1F4B5C"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="' . esc_attr( 'שליחת נכס' ) . '">';
	echo '<title>' . esc_html( 'שליחת נכס · ' . $b['name_he'] ) . '</title>';
	echo '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>';
	echo '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Noto+Serif+Hebrew:wght@500;600&display=swap">';
	echo '<style>' . $css . '</style></head><body>';
	echo '<header class="top"><div class="wrap"><div class="who"><b>' . esc_html( $b['name_he'] ) . '</b><span>' . esc_html( $b['brand_he'] ) . '</span></div>';
	if ( $cfg['site'] ) { echo '<a class="tosite" href="' . esc_url( $cfg['site'] ) . '" target="_blank" rel="noopener">לאתר שלכם</a>'; }
	echo '</div></header><main class="wrap">';
	echo '<section class="card" aria-labelledby="h-new"><h1 id="h-new">נכס חדש</h1>';
	echo '<p class="lead">בוחרים תמונות, כותבים כמה שורות על הנכס ושולחים. העמוד נבנה ועולה לאתר שלכם בתוך דקה. אפשר גם להכתיב: נוגעים במיקרופון שבמקלדת ומדברים.</p>';
	echo '<form id="f" novalidate>';
	echo '<div class="pick"><input type="file" id="files" accept="image/*" multiple><label for="files" class="btn btn--ghost" id="pickbtn">' . nl_drop_icon( 'area' ) . '<span>בחירת תמונות</span></label><span class="count" id="count" aria-live="polite"></span></div>';
	echo '<ul class="thumbs" id="thumbs" aria-label="התמונות שנבחרו"></ul>';
	echo '<p class="hint" id="hint" hidden>התמונה הראשונה היא התמונה הראשית של העמוד. נגיעה בתמונה אחרת הופכת אותה לראשית.</p>';
	echo '<label for="txt" class="lbl">פרטי הנכס</label>';
	echo '<textarea id="txt" rows="7" dir="rtl" placeholder="' . esc_attr( 'לדוגמה: ' . $ex ) . '"></textarea>';
	echo '<p class="hint">כדאי לכתוב: למכירה או להשכרה, שכונה, חדרים, מ״ר, קומה, מרפסת, חניה ומחסן, מחיר, מתי אפשר להיכנס, ומה מיוחד בנכס. מה שלא נכתב לא יופיע בעמוד.</p>';
	echo '<div class="bar"><button type="submit" class="btn" id="send">שליחה והעלאה לאתר</button></div>';
	echo '</form><div class="status" id="status" role="status" aria-live="polite" hidden></div></section>';
	echo '<section class="card" aria-labelledby="h-mine"><h2 id="h-mine">הנכסים שלי</h2><p class="lead small">נכס שנמכר או הושכר מסמנים כאן בנגיעה אחת. העמוד שלו נשאר עם הודעה מתאימה, והכרטיס יורד מהאתר.</p><ul class="mine" id="mine"><li class="muted">טוען…</li></ul></section>';
	echo '<p class="foot">הקישור הזה אישי. כל מי שמחזיק בו יכול להעלות נכסים לאתר שלכם, ולכן שומרים אותו לעצמכם.</p>';
	echo '</main>';
	echo '<div class="sheet" id="sheet" hidden><div class="sheet-in" role="dialog" aria-modal="true" aria-labelledby="sheet-t"><p id="sheet-t"></p><div class="sheet-f" id="sheet-f"></div><div class="sheet-b"><button type="button" class="btn" id="sheet-ok">אישור</button><button type="button" class="btn btn--ghost" id="sheet-no">ביטול</button></div></div></div>';
	echo '<script>window.NLDROP=' . wp_json_encode( $cfg, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . ';</script>';
	echo '<script>' . $js . '</script></body></html>';
}

function nl_drop_page_css() {
	return <<<'NLCSS'
:root{--paper:#F7F6F2;--surf:#FFFFFF;--ink:#14212B;--ink2:#3B4753;--mute:#6B7680;--line:#E3E1DA;--sea:#2F6F86;--seah:#255C70;--deep:#1F4B5C;--sand:#EEE9DD;--ok:#2E7D5B;--warn:#9A6A12;--bad:#B3261E;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--paper:#0F1A21;--surf:#16242D;--ink:#EEF2F4;--ink2:#C9D3D9;--mute:#93A2AC;--line:#2A3A44;--sea:#6FB3C9;--seah:#8CC4D6;--deep:#0B141A;--sand:#1E2E38;--ok:#6FC39A;--warn:#E0B35C;--bad:#F08A80;color-scheme:dark}}
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--paper);color:var(--ink);font:17px/1.6 Assistant,'Segoe UI',Arial,sans-serif;padding-bottom:env(safe-area-inset-bottom,0px)}
.wrap{max-width:600px;margin:0 auto;padding-inline:16px}
.top{background:var(--deep);color:#fff;padding-top:env(safe-area-inset-top,0px)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:60px}
.who{display:flex;flex-direction:column;line-height:1.2}
.who b{font-family:'Noto Serif Hebrew','Noto Serif',Georgia,serif;font-weight:600;font-size:18px}
.who span{font-size:13px;opacity:.8}
.tosite{color:#fff;font-size:14px;text-decoration:underline;text-underline-offset:3px}
main.wrap{padding-block:20px 40px;display:flex;flex-direction:column;gap:18px}
.card{background:var(--surf);border:1px solid var(--line);border-radius:14px;padding:22px 18px}
h1,h2{font-family:'Noto Serif Hebrew','Noto Serif',Georgia,serif;font-weight:600;margin:0 0 6px;line-height:1.25;text-wrap:balance}
h1{font-size:26px}
h2{font-size:21px}
.lead{margin:0 0 16px;color:var(--ink2)}
.lead.small{font-size:15px}
.pick{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.pick input{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none}
.count{font-size:15px;color:var(--mute);font-variant-numeric:tabular-nums}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:50px;padding:10px 20px;border-radius:999px;border:1px solid var(--sea);background:var(--sea);color:#fff;font:700 17px/1.2 Assistant,'Segoe UI',Arial,sans-serif;cursor:pointer;text-decoration:none}
.btn:hover{background:var(--seah);border-color:var(--seah)}
.btn:disabled{opacity:.55;cursor:default}
.btn svg{width:20px;height:20px}
.btn--ghost{background:transparent;color:var(--sea)}
.btn--ghost:hover{background:var(--sand);color:var(--ink)}
.btn--small{min-height:38px;padding:6px 14px;font-size:15px;font-weight:600}
:focus-visible{outline:3px solid var(--sea);outline-offset:2px}
.pick input:focus-visible+label{outline:3px solid var(--sea);outline-offset:2px}
.thumbs{list-style:none;margin:14px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.thumbs:empty{display:none}
.thumbs li{position:relative;aspect-ratio:1;border-radius:10px;overflow:hidden;background:var(--sand)}
.thumbs button.face{all:unset;display:block;width:100%;height:100%;cursor:pointer}
.thumbs img{width:100%;height:100%;object-fit:cover;display:block}
.thumbs .cover{position:absolute;top:6px;inset-inline-start:6px;background:var(--deep);color:#fff;font-size:12px;font-weight:700;padding:2px 8px;border-radius:999px}
.thumbs .x{position:absolute;top:4px;inset-inline-end:4px;width:30px;height:30px;border-radius:50%;border:0;background:rgba(20,33,43,.72);color:#fff;font-size:18px;line-height:30px;cursor:pointer}
.thumbs .st{position:absolute;inset-inline:0;bottom:0;height:4px;background:transparent}
.thumbs li[data-s="up"] .st{background:linear-gradient(90deg,var(--sea),var(--sand));animation:nlp 1.1s linear infinite;background-size:200% 100%}
.thumbs li[data-s="ok"] .st{background:var(--ok)}
.thumbs li[data-s="err"] .st{background:var(--bad)}
@keyframes nlp{to{background-position:-200% 0}}
@media (prefers-reduced-motion:reduce){.thumbs li[data-s="up"] .st{animation:none}}
.hint{font-size:14px;color:var(--mute);margin:8px 0 0}
.lbl{display:block;font-weight:700;margin:18px 0 6px}
textarea{width:100%;min-height:150px;border:1px solid var(--line);border-radius:12px;padding:12px 14px;font:17px/1.55 Assistant,'Segoe UI',Arial,sans-serif;background:var(--paper);color:var(--ink);resize:vertical}
textarea:focus{outline:3px solid var(--sea);outline-offset:1px;border-color:transparent}
.bar{margin-top:16px}
.bar .btn{width:100%}
@media (max-width:640px){.bar{position:sticky;bottom:0;margin-inline:-18px;padding:12px 18px calc(12px + env(safe-area-inset-bottom,0px));background:var(--surf);border-top:1px solid var(--line)}}
.status{margin-top:16px;padding:14px 16px;border-radius:12px;background:var(--sand);color:var(--ink)}
.status b{display:block;font-size:18px;margin-bottom:4px}
.status[data-k="ok"]{background:color-mix(in srgb,var(--ok) 14%,var(--surf));border:1px solid var(--ok)}
.status[data-k="warn"]{background:color-mix(in srgb,var(--warn) 14%,var(--surf));border:1px solid var(--warn)}
.status[data-k="bad"]{background:color-mix(in srgb,var(--bad) 12%,var(--surf));border:1px solid var(--bad)}
.status .row{display:flex;flex-wrap:wrap;gap:10px;margin-top:12px}
.status ul{margin:6px 0 0;padding-inline-start:20px}
.mine{list-style:none;margin:8px 0 0;padding:0;display:flex;flex-direction:column}
.mine li{display:grid;grid-template-columns:64px 1fr;gap:12px;padding:12px 0;border-top:1px solid var(--line)}
.mine li:first-child{border-top:0}
.mine li.muted{display:block;color:var(--mute)}
.mine img,.mine .ph{width:64px;height:64px;border-radius:10px;object-fit:cover;background:var(--sand);display:block}
.mine .t{font-weight:700;line-height:1.35}
.mine .t a{color:var(--ink);text-decoration:none}
.mine .t a:hover{text-decoration:underline}
.mine .m{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;font-size:14px;color:var(--mute);margin-top:2px}
.pill{display:inline-block;padding:1px 10px;border-radius:999px;font-size:13px;font-weight:700;border:1px solid var(--line)}
.pill--active{color:var(--ok);border-color:var(--ok)}
.pill--sold,.pill--rented{color:var(--warn);border-color:var(--warn)}
.pill--draft{color:var(--mute)}
.acts{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;grid-column:2}
.foot{font-size:13px;color:var(--mute);text-align:center;margin:4px 0 0}
.sheet{position:fixed;inset:0;background:rgba(15,26,33,.55);display:flex;align-items:flex-end;justify-content:center;z-index:9;padding:16px}
.sheet-in{background:var(--surf);color:var(--ink);border-radius:16px;padding:20px;width:100%;max-width:520px;margin-bottom:env(safe-area-inset-bottom,0px)}
.sheet-in p{margin:0 0 12px;font-weight:600}
.sheet-f input{width:100%;min-height:48px;border:1px solid var(--line);border-radius:10px;padding:8px 12px;font:18px Assistant,Arial,sans-serif;background:var(--paper);color:var(--ink);direction:ltr;text-align:right;font-variant-numeric:tabular-nums}
.sheet-b{display:flex;gap:10px;margin-top:14px}
.sheet-b .btn{flex:1}
[hidden]{display:none!important}
NLCSS;
}

function nl_drop_page_js() {
	return <<<'NLJS'
(function(){
'use strict';
var C=window.NLDROP||{},api=C.api||'';
var $=function(id){return document.getElementById(id);};
var items=[],seq=0,busy=false;
var files=$('files'),thumbs=$('thumbs'),count=$('count'),hint=$('hint'),txt=$('txt'),send=$('send'),statusEl=$('status'),mine=$('mine');
try{var d=localStorage.getItem('nldrop-draft');if(d&&!txt.value){txt.value=d;}}catch(e){}
txt.addEventListener('input',function(){try{localStorage.setItem('nldrop-draft',txt.value);}catch(e){}});
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function say(kind,html){statusEl.hidden=false;statusEl.setAttribute('data-k',kind||'');statusEl.innerHTML=html;}
function langBtns(j){var names={en:'באנגלית',ru:'ברוסית',fr:'בצרפתית'},u=j.urls||(j.url_en?{en:j.url_en}:{}),h='';['en','ru','fr'].forEach(function(l){if(u[l]){h+='<a class="btn btn--small btn--ghost" href="'+esc(u[l])+'" target="_blank" rel="noopener">'+names[l]+'</a>';}});return h;}
function shrink(file){
  return new Promise(function(res){
    var url=URL.createObjectURL(file),img=new Image();
    img.onload=function(){
      try{
        var max=2400,w=img.naturalWidth,h=img.naturalHeight,s=Math.min(1,max/Math.max(w,h));
        var c=document.createElement('canvas');c.width=Math.round(w*s);c.height=Math.round(h*s);
        c.getContext('2d').drawImage(img,0,0,c.width,c.height);
        c.toBlob(function(b){URL.revokeObjectURL(url);res(b||file);},'image/jpeg',0.86);
      }catch(e){URL.revokeObjectURL(url);res(file);}
    };
    img.onerror=function(){URL.revokeObjectURL(url);res(file);};
    img.src=url;
  });
}
function render(){
  thumbs.innerHTML='';
  items.forEach(function(it,i){
    var li=document.createElement('li');li.setAttribute('data-s',it.s);
    li.innerHTML='<button type="button" class="face" aria-label="'+(i?'הפיכה לתמונה הראשית':'התמונה הראשית')+'"><img alt="" src="'+it.preview+'"></button>'+(i===0?'<span class="cover">ראשית</span>':'')+'<button type="button" class="x" aria-label="הסרת התמונה">×</button><span class="st"></span>';
    li.querySelector('.face').addEventListener('click',function(){if(i>0){items.unshift(items.splice(i,1)[0]);render();}});
    li.querySelector('.x').addEventListener('click',function(){items.splice(i,1);render();});
    thumbs.appendChild(li);
  });
  var up=items.filter(function(x){return x.s==='up';}).length;
  count.textContent=items.length?(items.length+' תמונות'+(up?', מעלים '+up:'')):'';
  hint.hidden=items.length<2;
}
function upload(it){
  it.s='up';render();
  return shrink(it.file).then(function(blob){
    var fd=new FormData();fd.append('photo',blob,'photo.jpg');
    return fetch(api+'/photo',{method:'POST',body:fd,credentials:'omit'});
  }).then(function(r){return r.json().then(function(j){return {ok:r.ok,j:j};});})
  .then(function(x){if(x.ok&&x.j&&x.j.id){it.id=x.j.id;it.s='ok';}else{it.s='err';it.err=(x.j&&x.j.message)||'';}render();})
  .catch(function(){it.s='err';render();});
}
var queue=Promise.resolve();
files.addEventListener('change',function(){
  Array.prototype.forEach.call(files.files,function(f){
    if(!/^image\//.test(f.type)&&!/\.(heic|heif|jpe?g|png|webp)$/i.test(f.name)){return;}
    var it={k:++seq,file:f,preview:URL.createObjectURL(f),s:'wait',id:0};
    items.push(it);
    queue=queue.then(function(){return items.indexOf(it)>-1?upload(it):null;});
  });
  files.value='';render();
});
function post(path,body){
  return fetch(api+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body||{}),credentials:'omit'})
    .then(function(r){return r.json().then(function(j){return {ok:r.ok,j:j};});});
}
$('f').addEventListener('submit',function(e){
  e.preventDefault();if(busy){return;}
  var text=txt.value.trim();
  if(!items.length){say('warn','<b>חסרות תמונות</b>בוחרים לפחות תמונה אחת של הנכס.');return;}
  if(text.length<8){say('warn','<b>חסרים פרטים</b>כותבים כמה שורות על הנכס: חדרים, שטח, שכונה ומחיר.');txt.focus();return;}
  busy=true;send.disabled=true;
  say('','<b>מעלים את התמונות</b>עוד רגע.');
  queue.then(function(){
    var failed=items.filter(function(x){return x.s==='err';});
    if(failed.length){
      say('warn','<b>'+failed.length+' תמונות לא עלו</b>אפשר להסיר אותן בנגיעה ב-× ולשלוח שוב, או לבחור אותן מחדש.');
      throw 'stop';
    }
    say('','<b>קוראים את הפרטים</b>זה לוקח כמה שניות.');
    return post('/submit',{text:text,photos:items.map(function(x){return x.id;})});
  }).then(function(x){
    if(!x.ok){say('bad','<b>השליחה לא עברה</b>'+esc((x.j&&x.j.message)||'אפשר לנסות שוב בעוד רגע.'));throw 'stop';}
    if(x.j.state==='held'){
      say('warn','<b>חסרים כמה פרטים כדי לבנות עמוד</b>'+(x.j.summary?'<div>הבנו: '+esc(x.j.summary)+'</div>':'')+'<ul>'+(x.j.missing||[]).map(function(m){return '<li>'+esc(m)+'</li>';}).join('')+'</ul><div>מוסיפים אותם בטקסט ושולחים שוב. התמונות כבר למעלה.</div>');
      throw 'stop';
    }
    say('','<b>כותבים את העמוד</b>'+esc(x.j.summary||'')+'<div>עד דקה.</div>');
    var drop=x.j.drop;
    return post('/build/'+drop,{}).catch(function(){return post('/build/'+drop,{});});
  }).then(function(x){
    if(!x||!x.ok||!x.j||!x.j.url_he){say('bad','<b>בניית העמוד לא הושלמה</b>אפשר ללחוץ שוב על שליחה. שום דבר לא יוכפל.');throw 'stop';}
    var live=x.j.state==='published';
    say('ok','<b>'+(live?'הנכס עלה לאתר':'העמוד נשמר כטיוטה')+'</b>'+esc(x.j.title||'')+'<div class="row"><a class="btn btn--small" href="'+esc(x.j.url_he)+'" target="_blank" rel="noopener">לצפייה בעמוד</a>'+langBtns(x.j)+'<button type="button" class="btn btn--small btn--ghost" id="again">נכס נוסף</button></div>');
    var again=$('again');if(again){again.addEventListener('click',function(){items=[];render();txt.value='';try{localStorage.removeItem('nldrop-draft');}catch(e){}statusEl.hidden=true;window.scrollTo(0,0);});}
    try{localStorage.removeItem('nldrop-draft');}catch(e){}
    load();
  }).catch(function(err){if(err!=='stop'){say('bad','<b>אין חיבור</b>בודקים את האינטרנט ושולחים שוב.');}})
  .then(function(){busy=false;send.disabled=false;});
});
/* confirmations live in the page, never in browser pop-ups */
var sheet=$('sheet'),sheetT=$('sheet-t'),sheetF=$('sheet-f'),okB=$('sheet-ok'),noB=$('sheet-no'),onOk=null;
function ask(text,withInput,cb){sheetT.textContent=text;sheetF.innerHTML=withInput?'<input id="sheet-in" inputmode="numeric" autocomplete="off" aria-label="מחיר חדש בש״ח">':'';onOk=cb;sheet.hidden=false;var i=$('sheet-in');(i||okB).focus();}
okB.addEventListener('click',function(){var i=$('sheet-in'),v=i?i.value:'';sheet.hidden=true;if(onOk){onOk(v);}});
noB.addEventListener('click',function(){sheet.hidden=true;});
sheet.addEventListener('click',function(e){if(e.target===sheet){sheet.hidden=true;}});
function load(){
  fetch(api+'/listings',{credentials:'omit'}).then(function(r){return r.json();}).then(function(j){
    var L=(j&&j.listings)||[];
    if(!L.length){mine.innerHTML='<li class="muted">עוד אין נכסים. הנכס הראשון יופיע כאן.</li>';return;}
    mine.innerHTML='';
    L.forEach(function(x){
      var li=document.createElement('li');
      var st=x.live?x.status:'draft',lab={active:'באוויר',sold:'נמכר',rented:'הושכר',draft:'טיוטה'}[st];
      var off=x.deal==='rent'?'rented':'sold',offLab=x.deal==='rent'?'הושכר':'נמכר';
      li.innerHTML=(x.cover?'<img alt="" src="'+esc(x.cover)+'">':'<span class="ph"></span>')+
        '<div><div class="t"><a href="'+esc(x.url)+'" target="_blank" rel="noopener">'+esc(x.title)+'</a></div><div class="m"><span class="pill pill--'+st+'">'+lab+'</span>'+(x.price?'<span>'+esc(x.price)+'</span>':'')+'</div></div>'+
        '<div class="acts">'+(x.status==='active'?'<button type="button" class="btn btn--small btn--ghost" data-a="off">'+offLab+'</button>':'<button type="button" class="btn btn--small btn--ghost" data-a="on">החזרה לפרסום</button>')+(x.editable?'<button type="button" class="btn btn--small btn--ghost" data-a="price">עדכון מחיר</button>':'')+'</div>';
      var bOff=li.querySelector('[data-a="off"]'),bOn=li.querySelector('[data-a="on"]'),bP=li.querySelector('[data-a="price"]');
      if(bOff){bOff.addEventListener('click',function(){ask('לסמן את "'+x.title+'" כ'+offLab+'? העמוד יישאר עם הודעה, והכרטיס יירד מהאתר שלכם.',false,function(){post('/update',{id:x.id,status:off}).then(load);});});}
      if(bOn){bOn.addEventListener('click',function(){post('/update',{id:x.id,status:'active'}).then(load);});}
      if(bP){bP.addEventListener('click',function(){ask('מחיר חדש בש״ח ל"'+x.title+'"',true,function(v){if(!v){return;}post('/update',{id:x.id,price:v}).then(function(r){if(!r.ok){say('bad','<b>המחיר לא עודכן</b>'+esc((r.j&&r.j.message)||''));}load();});});});}
      mine.appendChild(li);
    });
  }).catch(function(){mine.innerHTML='<li class="muted">לא הצלחנו לטעון את הרשימה. מרעננים את העמוד.</li>';});
}
load();render();
})();
NLJS;
}

/* =====================================================================================================
 * Admin: the broker record gets its link; the log lists every submission
 * ===================================================================================================== */
add_action( 'add_meta_boxes_nadlan_professional', function () {
	add_meta_box( 'nl_drop_box', 'תיבת נכסים: קישור שליחה אישי', 'nl_drop_metabox', 'nadlan_professional', 'side', 'high' );
} );

function nl_drop_metabox( $post ) {
	$b = nl_drop_broker( $post->ID );
	wp_nonce_field( 'nl_drop_save', 'nl_drop_nonce' );
	$url = ( $b && $b['token'] !== '' ) ? home_url( '/drop/' . $b['token'] . '/' ) : '';
	echo '<p><label><input type="checkbox" name="nl_drop_on" value="1"' . checked( $b && $b['on'], true, false ) . '> פעילה</label></p>';
	if ( $url && $b['on'] ) {
		echo '<p style="margin:6px 0 2px">הקישור ששולחים למתווך:</p><input type="text" readonly value="' . esc_attr( $url ) . '" style="width:100%;direction:ltr" onclick="this.select()">';
		echo '<p><label><input type="checkbox" name="nl_drop_rotate" value="1"> קישור חדש (הקישור הקודם יפסיק לעבוד)</label></p>';
	}
	$langs = $b ? $b['langs'] : array( 'he' );
	echo '<p style="margin:10px 0 2px">שפות הנכסים</p><p style="margin:0">';
	foreach ( array( 'en' => 'אנגלית', 'ru' => 'רוסית', 'fr' => 'צרפתית' ) as $l => $lbl ) {
		echo '<label style="margin-inline-end:10px"><input type="checkbox" name="nl_langs[]" value="' . esc_attr( $l ) . '"' . checked( in_array( $l, $langs, true ), true, false ) . '> ' . esc_html( $lbl ) . '</label>';
	}
	echo '</p>';
	$tier = $b ? $b['tier'] : 'free';
	echo '<p style="margin:8px 0 2px">מסלול</p><select name="nl_tier">';
	foreach ( array( 'free' => 'בסיס (חינם)', 'pro' => 'מקצועי', 'studio' => 'בונים לכם' ) as $k => $lbl ) { echo '<option value="' . esc_attr( $k ) . '"' . selected( $tier, $k, false ) . '>' . esc_html( $lbl ) . '</option>'; }
	echo '</select>';
	$fields = array( 'nl_name_he' => 'שם בעברית', 'nl_name_en' => 'שם באנגלית', 'nl_name_ru' => 'שם ברוסית (לא חובה)', 'nl_brand_en' => 'שם העסק באנגלית', 'nl_site_he' => 'מזהה עמוד האתר בעברית', 'nl_site_en' => 'מזהה עמוד האתר באנגלית', 'nl_site_ru' => 'מזהה עמוד האתר ברוסית', 'nl_site_fr' => 'מזהה עמוד האתר בצרפתית' );
	foreach ( $fields as $k => $label ) {
		echo '<p style="margin:8px 0 2px">' . esc_html( $label ) . '</p><input type="text" name="' . esc_attr( $k ) . '" value="' . esc_attr( (string) get_post_meta( $post->ID, $k, true ) ) . '" style="width:100%">';
	}
	$g = (string) get_post_meta( $post->ID, 'nl_gender', true );
	echo '<p style="margin:8px 0 2px">לשון</p><select name="nl_gender"><option value="m"' . selected( $g !== 'f', true, false ) . '>מתווך</option><option value="f"' . selected( $g, 'f', false ) . '>מתווכת</option></select>';
	echo '<p><label><input type="checkbox" name="nl_auto_publish" value="1"' . checked( ! $b || $b['auto'], true, false ) . '> פרסום מיידי (בלי: נשמר כטיוטה)</label></p>';
	echo '<p class="description">רישיון ותיווך מגיעים מהשדות "מספר רישיון" ו"טלפון" של הכרטיס.</p>';
}

add_action( 'save_post_nadlan_professional', function ( $pid ) {
	if ( ! isset( $_POST['nl_drop_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nl_drop_nonce'] ) ), 'nl_drop_save' ) ) { return; }
	if ( ! current_user_can( 'edit_post', $pid ) || wp_is_post_revision( $pid ) ) { return; }
	$on = ! empty( $_POST['nl_drop_on'] );
	update_post_meta( $pid, 'nl_drop_on', $on ? '1' : '0' );
	if ( $on && ( (string) get_post_meta( $pid, '_nl_drop_token', true ) === '' || ! empty( $_POST['nl_drop_rotate'] ) ) ) {
		update_post_meta( $pid, '_nl_drop_token', nl_drop_new_token() );
		delete_post_meta( $pid, 'nl_drop_token' );
	}
	foreach ( array( 'nl_name_he', 'nl_name_en', 'nl_name_ru', 'nl_brand_en' ) as $k ) {
		if ( isset( $_POST[ $k ] ) ) { update_post_meta( $pid, $k, sanitize_text_field( wp_unslash( $_POST[ $k ] ) ) ); }
	}
	foreach ( array( 'nl_site_he', 'nl_site_en', 'nl_site_ru', 'nl_site_fr' ) as $k ) {
		if ( isset( $_POST[ $k ] ) ) { update_post_meta( $pid, $k, (string) absint( wp_unslash( $_POST[ $k ] ) ) ); }
	}
	update_post_meta( $pid, 'nl_gender', ( isset( $_POST['nl_gender'] ) && $_POST['nl_gender'] === 'f' ) ? 'f' : 'm' );
	update_post_meta( $pid, 'nl_auto_publish', ! empty( $_POST['nl_auto_publish'] ) ? '1' : '0' );
	$langs = array( 'he' );
	foreach ( (array) ( $_POST['nl_langs'] ?? array() ) as $l ) {
		$l = sanitize_key( wp_unslash( $l ) );
		if ( in_array( $l, array( 'en', 'ru', 'fr' ), true ) ) { $langs[] = $l; }
	}
	update_post_meta( $pid, 'nl_langs', implode( ',', array_unique( $langs ) ) );
	$tier = isset( $_POST['nl_tier'] ) ? sanitize_key( wp_unslash( $_POST['nl_tier'] ) ) : 'free';
	update_post_meta( $pid, 'nl_tier', in_array( $tier, array( 'free', 'pro', 'studio' ), true ) ? $tier : 'free' );
} );

add_filter( 'manage_nadlan_drop_posts_columns', function ( $cols ) {
	return array( 'cb' => $cols['cb'] ?? '', 'title' => 'שליחה', 'nl_state' => 'מצב', 'nl_page' => 'העמוד', 'date' => 'תאריך' );
} );

add_action( 'manage_nadlan_drop_posts_custom_column', function ( $col, $pid ) {
	if ( $col === 'nl_state' ) {
		$map = array( 'reading' => 'בקריאה', 'held' => 'חסרים פרטים', 'ready' => 'מוכן לבנייה', 'writing' => 'בכתיבה', 'published' => 'פורסם', 'draft' => 'טיוטה', 'failed' => 'נכשל' );
		$st  = (string) get_post_meta( $pid, 'nl_state', true );
		echo esc_html( $map[ $st ] ?? $st );
		$miss = (array) get_post_meta( $pid, 'nl_missing', true );
		if ( $st === 'held' && $miss ) { echo '<br><small>' . esc_html( implode( ', ', $miss ) ) . '</small>'; }
	}
	if ( $col === 'nl_page' ) {
		$r = get_post_meta( $pid, 'nl_result', true );
		if ( is_array( $r ) && ! empty( $r['url_he'] ) ) {
			echo '<a href="' . esc_url( $r['url_he'] ) . '" target="_blank" rel="noopener">עברית</a>';
			if ( ! empty( $r['url_en'] ) ) { echo ' · <a href="' . esc_url( $r['url_en'] ) . '" target="_blank" rel="noopener">English</a>'; }
		}
	}
}, 10, 2 );

/* =====================================================================================================
 * Health
 * ===================================================================================================== */
add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$since = gmdate( 'Y-m-d H:i:s', time() - 7 * DAY_IN_SECONDS );
	$q     = function ( $state = null ) use ( $since ) {
		$a = array( 'post_type' => 'nadlan_drop', 'post_status' => 'private', 'fields' => 'ids', 'numberposts' => 500, 'date_query' => array( array( 'after' => $since, 'column' => 'post_date_gmt' ) ), 'suppress_filters' => true );
		if ( $state ) { $a['meta_query'] = array( array( 'key' => 'nl_state', 'value' => $state ) ); }
		return count( get_posts( $a ) );
	};
	$out['broker_drop'] = array(
		'version'      => NL_DROP_VERSION,
		'brokers_on'   => count( get_posts( array( 'post_type' => 'nadlan_professional', 'fields' => 'ids', 'numberposts' => 200, 'meta_query' => array( array( 'key' => 'nl_drop_on', 'value' => '1' ) ), 'suppress_filters' => true ) ) ),
		'drops_7d'     => $q(),
		'published_7d' => $q( 'published' ),
		'held_7d'      => $q( 'held' ),
		'sites_auto'   => count( get_posts( array( 'post_type' => 'page', 'post_status' => 'publish', 'fields' => 'ids', 'numberposts' => 500, 'meta_query' => array( array( 'key' => 'nl_broker_auto', 'compare' => 'EXISTS' ) ), 'suppress_filters' => true ) ) ),
		'langs'        => nl_drop_langs(),
	);
	return $out;
} );
