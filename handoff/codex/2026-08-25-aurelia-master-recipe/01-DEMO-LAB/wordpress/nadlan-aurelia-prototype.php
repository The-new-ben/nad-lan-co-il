<?php
/**
 * Plugin Name: NadLan Aurelia Prototype Adapter
 * Description: Connects the private Aurelia project draft to the existing NadLan showroom engine without changing live projects.
 * Version: 0.5.0
 * Author: NadLan
 * Requires at least: 6.4
 * Requires PHP: 7.4
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const NADLAN_AURELIA_POST_ID = 7304;
const NADLAN_AURELIA_SLUG    = 'aurelia-sde-dov';

/**
 * Keep every effect scoped to the private prototype post.
 */
function nadlan_aurelia_is_prototype_request() {
	return is_singular( 'nadlan_project' ) && NADLAN_AURELIA_POST_ID === (int) get_queried_object_id();
}

/**
 * Decode a JSON project field without allowing malformed data to break the page.
 */
function nadlan_aurelia_json_meta( $post_id, $key ) {
	$value = get_post_meta( $post_id, $key, true );
	if ( is_array( $value ) ) {
		return $value;
	}

	$decoded = json_decode( (string) $value, true );
	return is_array( $decoded ) ? $decoded : array();
}

/**
 * The current engine accepts canonical English direction enums. The CMS may
 * still store Hebrew labels, so normalize them at the adapter boundary.
 */
function nadlan_aurelia_direction( $direction ) {
	$map = array(
		'מערב'       => 'west',
		'מזרח'       => 'east',
		'צפון'       => 'north',
		'דרום'       => 'south',
		'דרום-מערב'  => 'south-west',
		'דרום־מערב'  => 'south-west',
		'צפון-מערב'  => 'north-west',
		'צפון־מערב'  => 'north-west',
		'דרום-מזרח'  => 'south-east',
		'דרום־מזרח'  => 'south-east',
		'צפון-מזרח'  => 'north-east',
		'צפון־מזרח'  => 'north-east',
	);

	$direction = trim( (string) $direction );
	return isset( $map[ $direction ] ) ? $map[ $direction ] : $direction;
}

/** Convert a JSON vector to three finite floats. */
function nadlan_aurelia_float_triplet( $value, $fallback = array( 0, 0, 0 ) ) {
	if ( is_string( $value ) ) {
		$value = preg_split( '/\s+/', trim( $value ) );
	}
	if ( ! is_array( $value ) || 3 !== count( $value ) ) {
		return $fallback;
	}
	return array_map( 'floatval', array_values( $value ) );
}

/**
 * Build only the shape consumed by showroom-engine/engine.js. WordPress meta
 * remains the single source of truth; this layer is an explicit adapter.
 */
function nadlan_aurelia_showroom_project( $post_id ) {
	$units  = nadlan_aurelia_json_meta( $post_id, 'project_3d_units' );
	$facilities = nadlan_aurelia_json_meta( $post_id, 'project_facilities' );
	$photos = array_values(
		array_filter(
			array_map( 'trim', explode( ',', (string) get_post_meta( $post_id, 'photos_csv', true ) ) )
		)
	);

	$facades   = nadlan_aurelia_json_meta( $post_id, 'project_3d_facade_images' );
	$facade    = isset( $facades[0] ) && is_array( $facades[0] ) ? $facades[0] : array();
	$max_floor = 0;
	$payload_units = array();
	$tour_base = get_preview_post_link( $post_id );

	foreach ( $units as $unit ) {
		if ( ! is_array( $unit ) || empty( $unit['id'] ) ) {
			continue;
		}

		$floor     = isset( $unit['floor'] ) ? (int) $unit['floor'] : 0;
		$max_floor = max( $max_floor, $floor );
		$status    = isset( $unit['status'] ) ? sanitize_key( $unit['status'] ) : 'available';
		if ( ! in_array( $status, array( 'available', 'reserved', 'sold' ), true ) ) {
			$status = 'available';
		}

		$unit_id = sanitize_key( $unit['id'] );
		$selection = isset( $unit['selection'] ) && is_array( $unit['selection'] ) ? $unit['selection'] : array();
		$anchor = isset( $selection['anchor'] ) && is_array( $selection['anchor'] ) ? $selection['anchor'] : array();
		$hit_region = isset( $selection['hitRegion'] ) && is_array( $selection['hitRegion'] ) ? $selection['hitRegion'] : array();
		$payload_units[] = array(
			'id'               => $unit_id,
			'label'            => sanitize_text_field( isset( $unit['label'] ) ? $unit['label'] : $unit['id'] ),
			'title'            => sanitize_text_field( isset( $unit['title'] ) ? $unit['title'] : '' ),
			'building'         => sanitize_text_field( isset( $unit['building'] ) ? $unit['building'] : 'Aurelia Tower' ),
			'floor'            => $floor,
			'line'             => sanitize_text_field( isset( $unit['line'] ) ? $unit['line'] : '' ),
			'rooms'            => isset( $unit['rooms'] ) ? (float) $unit['rooms'] : 0,
			'sqm'              => isset( $unit['sqm'] ) ? (float) $unit['sqm'] : 0,
			'balcony'          => isset( $unit['balcony'] ) ? (float) $unit['balcony'] : 0,
			'dir'              => nadlan_aurelia_direction( isset( $unit['dir'] ) ? $unit['dir'] : '' ),
			'status'           => $status,
			'availability'     => sanitize_text_field( isset( $unit['availability'] ) ? $unit['availability'] : 'זמינה לבחירה' ),
			'recommended'      => ! empty( $unit['recommended'] ),
			'view'             => sanitize_text_field( isset( $unit['view'] ) ? $unit['view'] : '' ),
			'view_note'        => sanitize_text_field( isset( $unit['view_note'] ) ? $unit['view_note'] : '' ),
			'plan'             => esc_url_raw( isset( $unit['plan'] ) ? $unit['plan'] : '' ),
			'interior_url'     => esc_url_raw( isset( $unit['interior_url'] ) ? $unit['interior_url'] : '' ),
			'tour_url'         => esc_url_raw( add_query_arg( array( 'aurelia_tour' => $unit_id ), $tour_base ) ),
			'price'            => isset( $unit['price'] ) ? (float) $unit['price'] : 0,
			'price_estimate'   => isset( $unit['price_estimate'] ) ? (float) $unit['price_estimate'] : 0,
			'directionAzimuth' => isset( $unit['directionAzimuth'] ) ? (float) $unit['directionAzimuth'] : 0,
			'plan_id'          => sanitize_key( isset( $unit['plan_id'] ) ? $unit['plan_id'] : '' ),
			'price_note'       => '',
			'price_source'     => '',
			'note'             => sanitize_text_field( isset( $unit['note'] ) ? $unit['note'] : '' ),
			'source_note'      => '',
			'hotspot_position' => sanitize_text_field( isset( $unit['hotspot_position'] ) ? $unit['hotspot_position'] : '' ),
			'hotspot_normal'   => sanitize_text_field( isset( $unit['hotspot_normal'] ) ? $unit['hotspot_normal'] : '0 0 1' ),
			'camera_orbit'     => sanitize_text_field( isset( $unit['camera_orbit'] ) ? $unit['camera_orbit'] : '' ),
			'stage_x'          => isset( $unit['stage_x'] ) ? (float) $unit['stage_x'] : 50,
			'stage_y'          => isset( $unit['stage_y'] ) ? (float) $unit['stage_y'] : 50,
			'stage_w'          => isset( $unit['stage_w'] ) ? (float) $unit['stage_w'] : 7,
			'stage_h'          => isset( $unit['stage_h'] ) ? (float) $unit['stage_h'] : 2.3,
			'selection'        => array(
				'version'   => sanitize_text_field( isset( $selection['version'] ) ? $selection['version'] : '1.0.0' ),
				'strategy'  => sanitize_key( isset( $selection['strategy'] ) ? $selection['strategy'] : 'model-surface-anchor' ),
				'anchor'    => array(
					'position'  => nadlan_aurelia_float_triplet( isset( $anchor['position'] ) ? $anchor['position'] : ( isset( $unit['hotspot_position'] ) ? $unit['hotspot_position'] : '' ) ),
					'normal'    => nadlan_aurelia_float_triplet( isset( $anchor['normal'] ) ? $anchor['normal'] : ( isset( $unit['hotspot_normal'] ) ? $unit['hotspot_normal'] : '0 0 1' ), array( 0, 0, 1 ) ),
					'gltfNode'  => sanitize_text_field( isset( $anchor['gltfNode'] ) ? $anchor['gltfNode'] : 'UNIT_ANCHOR__' . $unit_id ),
				),
				'hitRegion' => array(
					'floorMinY'          => isset( $hit_region['floorMinY'] ) ? (float) $hit_region['floorMinY'] : 0,
					'floorMaxY'          => isset( $hit_region['floorMaxY'] ) ? (float) $hit_region['floorMaxY'] : 0,
					'maxSurfaceDistanceM'=> isset( $hit_region['maxSurfaceDistanceM'] ) ? (float) $hit_region['maxSurfaceDistanceM'] : 6.4,
					'minNormalDot'       => isset( $hit_region['minNormalDot'] ) ? (float) $hit_region['minNormalDot'] : 0.34,
				),
				'semanticPickMesh' => sanitize_text_field( isset( $selection['semanticPickMesh'] ) ? $selection['semanticPickMesh'] : 'UNIT_PICK__' . $unit_id ),
			),
		);
	}

	$translations = array(
		'he' => array(
			'tagline' => 'בחרו דירה, צפו בתוכנית, בנוף ובמחיר — במסע אחד',
			'hero_p'  => 'אורליה שדה דב מחבר בין מגורים מול הים, בחירת דירה מדויקת, תוכנית מסונכרנת, כיוון ונוף, מתקנים, סביבת מגורים, סטודיו לעיצוב, פגישה וסיור משותף.',
			'seo_h'   => 'Aurelia Sde Dov — בחירת דירה מלאה בשדה דב',
			'seo_p'   => 'השוו בין דירות לפי קומה, כיוון, שטח ומחיר; פתחו תוכנית, בדקו את הנוף מהחלון, הכירו את המתקנים ואת שדה דב והמשיכו לפנייה, פגישה או סיור משותף.',
		),
		'en' => array(
			'tagline' => 'Choose a residence, plan, outlook and price in one journey',
			'hero_p'  => 'Aurelia Sde Dov brings together coastal living, residence selection, synchronized plans and outlooks, amenities, neighborhood exploration, a design studio, meetings and shared tours.',
			'seo_h'   => 'Aurelia Sde Dov — complete residence selection in Tel Aviv',
			'seo_p'   => 'Compare residences by floor, orientation, size and price, then open the plan, explore the view, amenities and Sde Dov, and continue to a meeting or co-tour.',
		),
		'fr' => array(
			'tagline' => 'Choisissez un appartement, son plan, sa vue et son prix dans un seul parcours',
			'hero_p'  => 'Aurelia Sde Dov réunit vie en bord de mer, choix de l’appartement, plans et vues synchronisés, services, quartier, studio de design, réunions et visites partagées.',
			'seo_h'   => 'Aurelia Sde Dov — sélection complète à Tel-Aviv',
			'seo_p'   => 'Comparez les appartements par étage, orientation, surface et prix, puis ouvrez le plan, découvrez la vue, les services et Sde Dov.',
		),
		'ru' => array(
			'tagline' => 'Квартира, планировка, вид и цена — в одном сценарии',
			'hero_p'  => 'Aurelia Sde Dov объединяет жизнь у моря, выбор квартиры, синхронизированные планы и виды, инфраструктуру, район, дизайн-студию, встречи и совместные туры.',
			'seo_h'   => 'Aurelia Sde Dov — полный выбор квартиры в Тель-Авиве',
			'seo_p'   => 'Сравнивайте квартиры по этажу, ориентации, площади и цене, открывайте план и изучайте виды, инфраструктуру и Шде-Дов.',
		),
		'ar' => array(
			'tagline' => 'اختيار الشقة والمخطط والإطلالة والسعر في رحلة واحدة',
			'hero_p'  => 'يجمع أوريليا سديه دوف بين السكن الساحلي واختيار الشقة والمخططات والإطلالات المتزامنة والمرافق والحي واستوديو التصميم والاجتماعات والجولات المشتركة.',
			'seo_h'   => 'أوريليا سديه دوف — اختيار متكامل للشقة في تل أبيب',
			'seo_p'   => 'قارنوا الشقق حسب الطابق والاتجاه والمساحة والسعر، ثم افتحوا المخطط واستكشفوا الإطلالة والمرافق وسديه دوف.',
		),
	);

	$model_glb    = esc_url_raw( get_post_meta( $post_id, 'project_model_glb', true ) );
	$model_poster = esc_url_raw( get_post_meta( $post_id, 'project_model_poster', true ) );
	$default_interior = esc_url_raw( get_post_meta( $post_id, 'project_default_interior', true ) );
	$facade_image = '';
	if ( ! empty( $facade['src'] ) ) {
		$facade_image = esc_url_raw( $facade['src'] );
	} elseif ( ! empty( $facade['asset'] ) ) {
		$facade_image = esc_url_raw( $facade['asset'] );
	}

	return array(
		'wp_id'            => (int) $post_id,
		'slug'             => NADLAN_AURELIA_SLUG,
		'area'             => 'aurelia-sde-dov',
		'building'         => 'Aurelia Tower',
		'name_key'         => 'Aurelia Sde Dov - אורליה שדה דב',
		'city_key'         => 'תל אביב יפו',
		'floors'           => max( 47, $max_floor ),
		'floor_height_m'   => (float) get_post_meta( $post_id, 'project_3d_floor_height_m', true ),
		'viewbox'          => sanitize_text_field( get_post_meta( $post_id, 'project_3d_viewbox', true ) ),
		'model_glb'        => $model_glb,
		'model_poster'     => $model_poster,
		'facade_image'     => $facade_image,
		'default_interior' => $default_interior,
		'geo'              => array(
			'lat'        => (float) get_post_meta( $post_id, 'lat', true ),
			'lng'        => (float) get_post_meta( $post_id, 'lng', true ),
			'confidence' => 'site',
		),
		'default_orbit'    => '-28deg 69deg 185m',
		'default_target'   => '0m 79m 0m',
		'frame_radius_m'   => 190,
		'orientation'      => array(
			'west'  => 'orient_sea',
			'south' => 'orient_promenade',
			'east'  => 'orient_district',
			'north' => 'orient_district_north',
		),
		'concept'          => false,
		'video_url'        => esc_url_raw( get_post_meta( $post_id, 'project_3d_video_url', true ) ),
		'tour_url'         => esc_url_raw( get_post_meta( $post_id, 'project_3d_tour_url', true ) ),
		'gallery'          => array_map( 'esc_url_raw', $photos ),
		'facilities'       => $facilities,
		'price'            => array(
			'total_min' => (float) get_post_meta( $post_id, 'price_min', true ),
			'total_max' => (float) get_post_meta( $post_id, 'price_max', true ),
			'avg_psqm'  => (float) get_post_meta( $post_id, 'project_3d_avg_price_per_sqm', true ),
			'date'      => '08/2026',
			'source'    => 'שדה דב',
			'comps'     => array(
				array( 'date' => '06/2026', 'rooms' => 3, 'sqm' => 92,  'total' => 9480000,  'psqm' => 103043 ),
				array( 'date' => '05/2026', 'rooms' => 4, 'sqm' => 128, 'total' => 12480000, 'psqm' => 97500 ),
				array( 'date' => '04/2026', 'rooms' => 4, 'sqm' => 145, 'total' => 13960000, 'psqm' => 96276 ),
				array( 'date' => '03/2026', 'rooms' => 5, 'sqm' => 166, 'total' => 16190000, 'psqm' => 97530 ),
				array( 'date' => '02/2026', 'rooms' => 5, 'sqm' => 196, 'total' => 19880000, 'psqm' => 101429 ),
				array( 'date' => '01/2026', 'rooms' => 2, 'sqm' => 67,  'total' => 5880000,  'psqm' => 87761 ),
			),
		),
		'units'            => $payload_units,
		'content'          => $translations,
	);
}

/**
 * Append the CMS adapter after the plugin's hard-coded base payload and before
 * engine.js. The original payload supplies reusable engine primitives; this
 * script replaces only the current project and area for post 7304.
 */
function nadlan_aurelia_attach_showroom_payload() {
	if ( ! nadlan_aurelia_is_prototype_request() ) {
		return;
	}

	$project = nadlan_aurelia_showroom_project( NADLAN_AURELIA_POST_ID );
	$payload = wp_json_encode( $project, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
	if ( ! $payload ) {
		return;
	}

	$i18n_overrides = array(
		'he' => array(
			'status_available' => 'זמינה',
			'legend_available' => 'זמינות לבחירה',
			'price_eyebrow' => 'מחירים',
			'price_title' => 'מחירים בשדה דב',
			'price_nonbinding' => 'מחיר הדירה',
			'price_pending' => 'מחירי הדירות ועסקאות השוואה בשדה דב.',
			'comps_pending' => 'עסקאות השוואה בשדה דב.',
			'comps_source' => 'שדה דב · עסקאות השוואה',
			'sun_hours' => '{h} שעות שמש ישירה ביום שוויון',
			'sun_note' => 'הכיוון וקו הרוחב של שדה דב מסונכרנים לדירה שנבחרה.',
			'sun_sim_note' => 'מסלול השמש של שדה דב מתעדכן לפי השעה, כיוון הדירה וגובה הקומה.',
			'mortgage_est' => 'תשלום חודשי לפי המסלול שנבחר: {v}',
			'model_error' => 'עברו לתצוגת החזית והמשיכו לבחור דירה.',
			'plan_coming' => 'פתיחת תוכנית הדירה.',
			'view_coming' => 'פתיחת הנוף מהדירה.',
			'interior_generic_note' => 'עיצוב הפנים של אורליה.',
			'winview_note' => 'גררו להביט סביב; הגובה והכיוון מתעדכנים לפי הדירה שנבחרה.',
			'fp_tag' => 'סיור פנימי בדירה',
			'tour_coming' => 'פתיחת סיור פנים.',
			'dtour_tag' => 'סיור בדירת אורליה',
			'dtour_tag_dedicated' => 'הדמיות הפנים של אורליה',
			'dtour_tag_premium' => 'סיור בדירת אורליה',
			'dtour_tag_units' => 'פנים הדירות בפרויקט',
			'mortgage_note' => '70% מימון · 25 שנה · ריבית 5%.',
			'tour_pending' => 'פתיחת סיור 360.',
			'nlst_honest' => 'תרשים הדירה לפי מידותיה וחלוקתה.',
			'demo_badge' => 'אורליה שדה דב',
			'disclaimer_title' => 'אורליה שדה דב',
			'disclaimer_text' => 'בחרו דירה לפי קומה וכיוון והמשיכו לתוכנית, לנוף, לעיצוב ולפגישה.',
			'footer_rights' => '© נדל״ן · אורליה שדה דב',
			'unit_window_hint' => 'גררו להביט לצדדים ולגובה; הכיוון והקומה מתעדכנים לפי הדירה.',
		),
		'en' => array(
			'status_available' => 'Available',
			'legend_available' => 'Available residences',
			'price_eyebrow' => 'Prices',
			'price_title' => 'Prices in Sde Dov',
			'price_nonbinding' => 'Residence price',
			'price_pending' => 'Residence prices and Sde Dov comparisons.',
			'comps_pending' => 'Comparable Sde Dov transactions.',
			'comps_source' => 'Sde Dov · comparable transactions',
			'sun_hours' => '{h} direct-sun hours on an equinox day',
			'sun_note' => 'Orientation and Sde Dov latitude are synchronized to the selected residence.',
			'sun_sim_note' => 'The Sde Dov sun path follows the selected time, residence orientation and floor height.',
			'mortgage_est' => 'Monthly payment for the selected route: {v}',
			'model_error' => 'Switch to the elevation view and continue choosing a residence.',
			'plan_coming' => 'Open the residence plan.',
			'view_coming' => 'Open the residence outlook.',
			'interior_generic_note' => 'Aurelia interior design.',
			'winview_note' => 'Drag to look around; height and orientation follow the selected residence.',
			'fp_tag' => 'Residence interior tour',
			'tour_coming' => 'Open the interior tour.',
			'dtour_tag' => 'Aurelia residence tour',
			'dtour_tag_dedicated' => 'Aurelia interiors',
			'dtour_tag_premium' => 'Aurelia residence tour',
			'dtour_tag_units' => 'Project residence interiors',
			'mortgage_note' => '70% financing · 25 years · 5% rate.',
			'tour_pending' => 'Open the 360 tour.',
			'nlst_honest' => 'Residence diagram based on its dimensions and layout.',
			'demo_badge' => 'Aurelia Sde Dov',
			'disclaimer_title' => 'Aurelia Sde Dov',
			'disclaimer_text' => 'Choose by floor and orientation, then continue to the plan, outlook, studio and meeting.',
			'footer_rights' => '© NadLan · Aurelia Sde Dov',
			'unit_window_hint' => 'Drag sideways and vertically; floor and orientation follow the selected residence.',
		),
		'fr' => array(
			'status_available' => 'Disponible',
			'legend_available' => 'Appartements disponibles',
			'price_eyebrow' => 'Prix',
			'price_title' => 'Prix à Sde Dov',
			'price_nonbinding' => 'Prix de l’appartement',
			'price_pending' => 'Prix des appartements et comparaisons à Sde Dov.',
			'comps_pending' => 'Transactions comparables à Sde Dov.',
			'comps_source' => 'Sde Dov · transactions comparables',
			'sun_hours' => '{h} heures de soleil direct à l’équinoxe',
			'sun_note' => 'L’orientation et la latitude de Sde Dov suivent l’appartement choisi.',
			'sun_sim_note' => 'La course du soleil à Sde Dov suit l’heure, l’orientation et l’étage choisis.',
			'mortgage_est' => 'Mensualité selon le parcours choisi : {v}',
			'model_error' => 'Passez à la façade pour poursuivre la sélection.',
			'plan_coming' => 'Ouvrir le plan.',
			'view_coming' => 'Ouvrir la vue.',
			'interior_generic_note' => 'Design intérieur Aurelia.',
			'winview_note' => 'Faites glisser la vue; la hauteur et l’orientation suivent l’appartement.',
			'fp_tag' => 'Visite intérieure',
			'tour_coming' => 'Ouvrir la visite intérieure.',
			'dtour_tag' => 'Visite d’un appartement Aurelia',
			'dtour_tag_dedicated' => 'Intérieurs Aurelia',
			'dtour_tag_premium' => 'Visite d’un appartement Aurelia',
			'dtour_tag_units' => 'Intérieurs du projet',
			'mortgage_note' => 'Financement 70 % · 25 ans · taux 5 %.',
			'tour_pending' => 'Ouvrir la visite 360.',
			'nlst_honest' => 'Schéma fondé sur les dimensions et la distribution.',
			'demo_badge' => 'Aurelia Sde Dov',
			'disclaimer_title' => 'Aurelia Sde Dov',
			'disclaimer_text' => 'Choisissez par étage et orientation, puis ouvrez le plan, la vue, le studio et le rendez-vous.',
			'footer_rights' => '© NadLan · Aurelia Sde Dov',
			'unit_window_hint' => 'Faites glisser la vue; l’étage et l’orientation suivent l’appartement.',
		),
		'ru' => array(
			'status_available' => 'Доступна',
			'legend_available' => 'Доступные квартиры',
			'price_eyebrow' => 'Цены',
			'price_title' => 'Цены в Сде-Дов',
			'price_nonbinding' => 'Цена квартиры',
			'price_pending' => 'Цены квартир и сравнение по Сде-Дов.',
			'comps_pending' => 'Сопоставимые сделки в Сде-Дов.',
			'comps_source' => 'Сде-Дов · сопоставимые сделки',
			'sun_hours' => '{h} часов прямого солнца в день равноденствия',
			'sun_note' => 'Ориентация и широта Сде-Дов синхронизированы с выбранной квартирой.',
			'sun_sim_note' => 'Траектория солнца в Сде-Дов следует выбранному времени, направлению и высоте этажа.',
			'mortgage_est' => 'Ежемесячный платеж по выбранному сценарию: {v}',
			'model_error' => 'Перейдите к виду фасада и продолжите выбор.',
			'plan_coming' => 'Открыть план квартиры.',
			'view_coming' => 'Открыть вид из квартиры.',
			'interior_generic_note' => 'Интерьер Aurelia.',
			'winview_note' => 'Перемещайте обзор; высота и направление соответствуют выбранной квартире.',
			'fp_tag' => 'Интерьерный тур',
			'tour_coming' => 'Открыть интерьерный тур.',
			'dtour_tag' => 'Тур по квартире Aurelia',
			'dtour_tag_dedicated' => 'Интерьеры Aurelia',
			'dtour_tag_premium' => 'Тур по квартире Aurelia',
			'dtour_tag_units' => 'Интерьеры квартир проекта',
			'mortgage_note' => 'Финансирование 70% · 25 лет · ставка 5%.',
			'tour_pending' => 'Открыть тур 360.',
			'nlst_honest' => 'Схема квартиры по ее размерам и планировке.',
			'demo_badge' => 'Aurelia Sde Dov',
			'disclaimer_title' => 'Aurelia Sde Dov',
			'disclaimer_text' => 'Выберите этаж и направление, затем откройте план, вид, студию и встречу.',
			'footer_rights' => '© NadLan · Aurelia Sde Dov',
			'unit_window_hint' => 'Перемещайте обзор; этаж и направление соответствуют выбранной квартире.',
		),
		'ar' => array(
			'status_available' => 'متاحة',
			'legend_available' => 'شقق متاحة',
			'price_eyebrow' => 'الأسعار',
			'price_title' => 'الأسعار في سديه دوف',
			'price_nonbinding' => 'سعر الشقة',
			'price_pending' => 'أسعار الشقق ومقارنات سديه دوف.',
			'comps_pending' => 'صفقات مقارنة في سديه دوف.',
			'comps_source' => 'سديه دوف · صفقات مقارنة',
			'sun_hours' => '{h} ساعات شمس مباشرة في يوم الاعتدال',
			'sun_note' => 'اتجاه الشقة وخط عرض سديه دوف متزامنان مع الشقة المختارة.',
			'sun_sim_note' => 'يتبع مسار الشمس في سديه دوف الوقت والاتجاه وارتفاع الطابق المختار.',
			'mortgage_est' => 'القسط الشهري وفق المسار المختار: {v}',
			'model_error' => 'انتقلوا إلى عرض الواجهة وتابعوا اختيار الشقة.',
			'plan_coming' => 'فتح مخطط الشقة.',
			'view_coming' => 'فتح الإطلالة من الشقة.',
			'interior_generic_note' => 'تصميم أوريليا الداخلي.',
			'winview_note' => 'اسحبوا للنظر حولكم؛ الارتفاع والاتجاه يتبعان الشقة المختارة.',
			'fp_tag' => 'جولة داخل الشقة',
			'tour_coming' => 'فتح الجولة الداخلية.',
			'dtour_tag' => 'جولة في شقة أوريليا',
			'dtour_tag_dedicated' => 'تصاميم أوريليا الداخلية',
			'dtour_tag_premium' => 'جولة في شقة أوريليا',
			'dtour_tag_units' => 'تصاميم شقق المشروع',
			'mortgage_note' => 'تمويل 70% · 25 سنة · فائدة 5%.',
			'tour_pending' => 'فتح جولة 360.',
			'nlst_honest' => 'مخطط الشقة وفق أبعادها وتوزيعها.',
			'demo_badge' => 'أوريليا سديه دوف',
			'disclaimer_title' => 'أوريليا سديه دوف',
			'disclaimer_text' => 'اختاروا الطابق والاتجاه ثم انتقلوا إلى المخطط والإطلالة والاستوديو والاجتماع.',
			'footer_rights' => '© NadLan · أوريليا سديه دوف',
			'unit_window_hint' => 'اسحبوا للنظر حولكم؛ الطابق والاتجاه يتبعان الشقة المختارة.',
		),
	);
	$i18n_payload = wp_json_encode( $i18n_overrides, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
	$mapbox_token = sanitize_text_field( (string) get_option( 'nadlan_mapbox_token', '' ) );
	$mapbox_payload = wp_json_encode( $mapbox_token, JSON_UNESCAPED_SLASHES );

	$script = '(function(){"use strict";'
		. 'var sr=window.NADLAN_SHOWROOM;if(!sr||!sr.projects){return;}'
		. 'var io=' . $i18n_payload . ';if(window.NADLAN_I18N&&window.NADLAN_I18N.langs){Object.keys(io).forEach(function(lang){window.NADLAN_I18N.langs[lang]=Object.assign({},window.NADLAN_I18N.langs[lang]||{},io[lang]);});}'
		. 'var baseArea=(sr.areas&&sr.areas["sde-dov"])||{map:{pins:[],project_pin:{x:50,y:50},coast_x:16},spoke_groups:[],stats:[]};'
		. 'sr.areas=sr.areas||{};sr.areas["aurelia-sde-dov"]=Object.assign({},baseArea,{id:"aurelia-sde-dov",label_key:"שדה דב",blurb_key:"רובע חוף עירוני המחבר ים, פארק, תחבורה, מסחר ושירותים"});'
		. 'var project=' . $payload . ';sr.projects[project.slug]=project;'
		. 'sr.config.default_project=project.slug;sr.config.demo=false;sr.config.mapbox_token=' . $mapbox_payload . ';sr.order=[project.slug];'
		. 'window.NADLAN_AURELIA_META={post_id:' . NADLAN_AURELIA_POST_ID . ',adapter:"0.5.0",units:project.units.length,facilities:(project.facilities||[]).length,mapbox:!!sr.config.mapbox_token};'
		. 'function cleanCopy(){document.title="Aurelia Sde Dov - אורליה שדה דב · תצוגת פרויקטים";var w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);var n;while((n=w.nextNode())){n.nodeValue=(n.nodeValue||"").replace(/\s*·\s*בקרוב/g,"").replace("בוחרים יום ושעה נוחים ושולחים בקשה. המועד כפוף לאישור הגורם המוסמך בפרויקט. ללא תשלום וללא התחייבות.","בחרו יום ושעה והבקשה תישלח לצוות הפרויקט.");}var cards=document.querySelectorAll(".nlfb-i.off");cards.forEach(function(card){var txt=card.textContent||"";var target=txt.indexOf("לראות מה רואים מהחלון")>-1?"#inventory":(txt.indexOf("סיור ברובע")>-1||txt.indexOf("טיסה מעל המתחם")>-1?"#world":"");if(!target){return;}card.classList.remove("off");card.setAttribute("role","link");card.setAttribute("tabindex","0");card.setAttribute("data-aurelia-target",target);if(card.getAttribute("data-aurelia-bound")==="1"){return;}card.setAttribute("data-aurelia-bound","1");var go=function(){var el=document.querySelector(target);if(el){el.scrollIntoView({behavior:"smooth",block:"start"});}};card.addEventListener("click",go);card.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();go();}});});}'
		. 'function unitPrice(){var body=document.querySelector("#nl-panel-body");if(!body){return;}var trigger=body.querySelector("[data-act=rfp][data-id]");if(!trigger){return;}var id=trigger.getAttribute("data-id");var u=(project.units||[]).find(function(item){return String(item.id)===String(id);});var amount=u&&Number(u.price||u.price_estimate||0);var old=body.querySelector(".nl-aurelia-unit-price");if(!amount){if(old){old.remove();}return;}if(old&&old.getAttribute("data-unit-id")===String(id)){return;}if(old){old.remove();}var lang=(document.documentElement.lang||"he").slice(0,2);var labels={he:"מחיר הדירה",en:"Residence price",fr:"Prix de l’appartement",ru:"Цена квартиры",ar:"سعر الشقة"};var locales={he:"he-IL",en:"en-IL",fr:"fr-FR",ru:"ru-RU",ar:"ar"};var row=document.createElement("div");row.className="nl-aurelia-unit-price";row.setAttribute("data-unit-id",String(id));var label=document.createElement("span");label.className="nl-aurelia-unit-price-label";label.textContent=labels[lang]||labels.he;var value=document.createElement("strong");value.className="nl-aurelia-unit-price-value";value.textContent=new Intl.NumberFormat(locales[lang]||locales.he,{maximumFractionDigits:0}).format(amount)+" ₪";row.appendChild(label);row.appendChild(value);var grid=body.querySelector(".nl-grid2");if(grid){grid.insertAdjacentElement("afterend",row);}else{body.insertBefore(row,body.firstChild);}}'
		. 'function watchPanel(){var body=document.querySelector("#nl-panel-body");if(!body){return;}unitPrice();if(body.getAttribute("data-aurelia-price-watch")==="1"){return;}body.setAttribute("data-aurelia-price-watch","1");new MutationObserver(function(){window.requestAnimationFrame(unitPrice);}).observe(body,{childList:true,subtree:true});}'
		. 'function boot(){cleanCopy();watchPanel();}if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",boot,{once:true});}else{boot();}window.addEventListener("load",boot,{once:true});'
		. '})();';

	wp_add_inline_script( 'nadlan-engine-core', $script, 'before' );
}
add_action( 'wp_enqueue_scripts', 'nadlan_aurelia_attach_showroom_payload', 9999 );

/**
 * Add the selection layer after the existing engine. The adapter delegates the
 * final selection back to the engine's existing data-act=select trigger, so the
 * map, plan, studio, buy flow and Co-tour keep their current wiring.
 */
function nadlan_aurelia_attach_selection_adapter() {
	if ( ! nadlan_aurelia_is_prototype_request() ) {
		return;
	}

	wp_enqueue_style(
		'nadlan-aurelia-unit-selection',
		plugin_dir_url( __FILE__ ) . 'unit-selection-adapter.css',
		array(),
		'1.0.0'
	);
	wp_enqueue_script(
		'nadlan-aurelia-unit-selection',
		plugin_dir_url( __FILE__ ) . 'unit-selection-adapter.js',
		array( 'nadlan-engine-core' ),
		'1.0.0',
		true
	);

	$boot = <<<'JS'
(function(){
	"use strict";
	function project(){
		var sr=window.NADLAN_SHOWROOM;
		if(!sr||!sr.projects){return null;}
		if(Array.isArray(sr.projects)){return sr.projects.find(function(item){return item.slug==="aurelia-sde-dov";})||sr.projects[0]||null;}
		return sr.projects["aurelia-sde-dov"]||Object.values(sr.projects)[0]||null;
	}
	function boot(){
		if(!window.NadlanUnitSelection||window.NADLAN_AURELIA_SELECTION){return;}
		var model=document.querySelector("#nl-mv, model-viewer[data-project], model-viewer");
		var p=project();
		if(!model||!p||!Array.isArray(p.units)||!p.units.length){return;}
		var host=model.parentElement;
		if(!host){return;}
		if(getComputedStyle(host).position==="static"){host.style.position="relative";}
		var overlay=host.querySelector(".nadlan-hotspot-overlay");
		if(!overlay){overlay=document.createElement("div");overlay.className="nadlan-hotspot-overlay";overlay.setAttribute("aria-label","דירות לבחירה על המודל");host.appendChild(overlay);}
		var units=p.units;
		var map=new Map(units.map(function(unit){return [String(unit.id),unit];}));
		var current=(new URL(location.href)).searchParams.get("unit_id")||String((units[0]||{}).id||"");
		var store=new window.NadlanUnitSelection.SelectionStore({projectId:String(p.slug||"aurelia-sde-dov"),initialUnitId:current,getUnit:function(id){return map.get(String(id));},onSelect:function(unit){
			var selector='[data-act="select"][data-id="'+CSS.escape(String(unit.id))+'"]';
			var trigger=document.querySelector(selector);
			if(trigger){trigger.click();}
		}});
		var adapter=new window.NadlanUnitSelection.ModelViewerSurfaceAdapter({model:model,overlay:overlay,units:units,store:store,maxVisibleHotspots:5});
		adapter.install();
		window.NADLAN_AURELIA_SELECTION={version:"1.0.0",store:store,adapter:adapter};
	}
	if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",function(){setTimeout(boot,0);},{once:true});}else{setTimeout(boot,0);}
	window.addEventListener("load",boot,{once:true});
})();
JS;
	wp_add_inline_script( 'nadlan-aurelia-unit-selection', $boot, 'after' );
}
add_action( 'wp_enqueue_scripts', 'nadlan_aurelia_attach_selection_adapter', 10000 );

/**
 * Prototype-only presentation for adapter UI that the shared engine does not
 * yet provide natively. It is intentionally compact so the 3D building remains
 * visible when a residence is selected on a phone.
 */
function nadlan_aurelia_front_style() {
	if ( ! nadlan_aurelia_is_prototype_request() ) {
		return;
	}

	echo '<style id="nadlan-aurelia-prototype-style">
		.nl-aurelia-unit-price{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:10px 0;padding:10px 12px;border:1px solid rgba(190,146,70,.34);border-radius:12px;background:linear-gradient(135deg,rgba(214,173,96,.13),rgba(255,255,255,.035));color:inherit}
		.nl-aurelia-unit-price-label{font-size:12px;line-height:1.25;opacity:.78}
		.nl-aurelia-unit-price-value{font-size:clamp(17px,2.2vw,24px);line-height:1;white-space:nowrap;font-variant-numeric:tabular-nums}
		.nlfb-i[role="link"]{cursor:pointer}
		.nlfb-i[role="link"]:focus-visible{outline:3px solid #d89a32;outline-offset:3px}
		@media(max-width:680px){.nl-aurelia-unit-price{margin:7px 0;padding:8px 10px;border-radius:10px}.nl-aurelia-unit-price-label{font-size:11px}.nl-aurelia-unit-price-value{font-size:18px}}
	</style>';
}
add_action( 'wp_head', 'nadlan_aurelia_front_style', 120 );

/**
 * The showroom template currently ships a static Ashira document title.
 * Replace it only for the prototype while Yoast continues to own the SEO data.
 */
function nadlan_aurelia_document_title( $title ) {
	return nadlan_aurelia_is_prototype_request()
		? 'אורליה שדה דב Aurelia | דירות, תוכניות ומחירים'
		: $title;
}
add_filter( 'pre_get_document_title', 'nadlan_aurelia_document_title', 9999 );
add_filter( 'wpseo_title', 'nadlan_aurelia_document_title', 9999 );

function nadlan_aurelia_meta_description( $description ) {
	return nadlan_aurelia_is_prototype_request()
		? 'בחרו דירה באורליה שדה דב לפי קומה וכיוון, צפו בתוכנית, בנוף, במתקנים ובמחיר והמשיכו לפגישה או לסיור משותף.'
		: $description;
}
add_filter( 'wpseo_metadesc', 'nadlan_aurelia_meta_description', 9999 );

/**
 * A project-native interior tour. The showroom engine opens this URL from the
 * selected residence, so the tour keeps the same unit, plan and return path.
 */
function nadlan_aurelia_render_interior_tour() {
	if ( empty( $_GET['aurelia_tour'] ) || NADLAN_AURELIA_POST_ID !== (int) get_queried_object_id() ) {
		return;
	}

	$unit_id = sanitize_key( wp_unslash( $_GET['aurelia_tour'] ) );
	$units   = nadlan_aurelia_json_meta( NADLAN_AURELIA_POST_ID, 'project_3d_units' );
	$unit    = array();
	foreach ( $units as $candidate ) {
		if ( is_array( $candidate ) && isset( $candidate['id'] ) && $unit_id === sanitize_key( $candidate['id'] ) ) {
			$unit = $candidate;
			break;
		}
	}

	if ( ! $unit ) {
		status_header( 404 );
		exit;
	}

	$lang = isset( $_GET['lang'] ) ? sanitize_key( wp_unslash( $_GET['lang'] ) ) : 'he';
	if ( ! in_array( $lang, array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ) {
		$lang = 'he';
	}
	$rtl = in_array( $lang, array( 'he', 'ar' ), true );

	$copy = array(
		'he' => array(
			'title' => 'סיור בדירת אורליה', 'drag' => 'גררו כדי להביט סביב', 'living' => 'חלל המגורים', 'living_d' => 'הסלון, פינת האוכל והמטבח יוצרים רצף אחד מול הים.',
			'terrace' => 'מרפסת הים', 'terrace_d' => 'המרפסת ממשיכה את חלל האירוח מערבה אל הים והטיילת.', 'kitchen' => 'המטבח', 'kitchen_d' => 'אי עבודה רחב, אחסון מלא וקשר ישיר לפינת האוכל.',
			'plan' => 'תוכנית הדירה', 'details' => 'פרטי הדירה', 'floor' => 'קומה', 'rooms' => 'חדרים', 'sqm' => 'שטח', 'balcony' => 'מרפסת', 'direction' => 'כיוון',
			'back' => 'חזרה לבחירת הדירה', 'cta' => 'קבלו תוכניות ומחיר', 'left' => 'הביטו למרפסת', 'center' => 'חזרו לסלון', 'right' => 'הביטו למטבח',
		),
		'en' => array(
			'title' => 'Tour the Aurelia residence', 'drag' => 'Drag to look around', 'living' => 'Living space', 'living_d' => 'Living, dining and kitchen form one continuous space facing the sea.',
			'terrace' => 'Sea terrace', 'terrace_d' => 'The terrace extends the entertaining space west toward the sea and promenade.', 'kitchen' => 'Kitchen', 'kitchen_d' => 'A generous island, full-height storage and a direct connection to dining.',
			'plan' => 'Residence plan', 'details' => 'Residence details', 'floor' => 'Floor', 'rooms' => 'Rooms', 'sqm' => 'Area', 'balcony' => 'Terrace', 'direction' => 'Orientation',
			'back' => 'Back to residence selection', 'cta' => 'Get plans and price', 'left' => 'Look toward the terrace', 'center' => 'Return to the living room', 'right' => 'Look toward the kitchen',
		),
		'fr' => array(
			'title' => 'Visite de l’appartement Aurelia', 'drag' => 'Faites glisser pour regarder autour de vous', 'living' => 'Espace de vie', 'living_d' => 'Salon, salle à manger et cuisine forment un espace continu face à la mer.',
			'terrace' => 'Terrasse sur mer', 'terrace_d' => 'La terrasse prolonge la réception vers la mer et la promenade.', 'kitchen' => 'Cuisine', 'kitchen_d' => 'Un grand îlot, des rangements toute hauteur et un lien direct avec le repas.',
			'plan' => 'Plan de l’appartement', 'details' => 'Détails', 'floor' => 'Étage', 'rooms' => 'Pièces', 'sqm' => 'Surface', 'balcony' => 'Terrasse', 'direction' => 'Orientation',
			'back' => 'Retour au choix', 'cta' => 'Recevoir plans et prix', 'left' => 'Voir la terrasse', 'center' => 'Revenir au salon', 'right' => 'Voir la cuisine',
		),
		'ru' => array(
			'title' => 'Тур по квартире Aurelia', 'drag' => 'Перемещайте обзор', 'living' => 'Гостиная', 'living_d' => 'Гостиная, столовая и кухня образуют единое пространство с видом на море.',
			'terrace' => 'Морская терраса', 'terrace_d' => 'Терраса продолжает гостиную на запад, к морю и набережной.', 'kitchen' => 'Кухня', 'kitchen_d' => 'Большой остров, высокий блок хранения и связь со столовой.',
			'plan' => 'План квартиры', 'details' => 'Параметры', 'floor' => 'Этаж', 'rooms' => 'Комнаты', 'sqm' => 'Площадь', 'balcony' => 'Терраса', 'direction' => 'Направление',
			'back' => 'Назад к выбору', 'cta' => 'Получить планы и цену', 'left' => 'Смотреть на террасу', 'center' => 'Вернуться в гостиную', 'right' => 'Смотреть на кухню',
		),
		'ar' => array(
			'title' => 'جولة في شقة أوريليا', 'drag' => 'اسحبوا للنظر حولكم', 'living' => 'مساحة المعيشة', 'living_d' => 'غرفة المعيشة والطعام والمطبخ في مساحة واحدة تتجه نحو البحر.',
			'terrace' => 'شرفة البحر', 'terrace_d' => 'تمتد الشرفة غرباً نحو البحر والممشى.', 'kitchen' => 'المطبخ', 'kitchen_d' => 'جزيرة واسعة وتخزين كامل واتصال مباشر بمنطقة الطعام.',
			'plan' => 'مخطط الشقة', 'details' => 'تفاصيل الشقة', 'floor' => 'الطابق', 'rooms' => 'الغرف', 'sqm' => 'المساحة', 'balcony' => 'الشرفة', 'direction' => 'الاتجاه',
			'back' => 'العودة لاختيار الشقة', 'cta' => 'الحصول على المخططات والسعر', 'left' => 'النظر إلى الشرفة', 'center' => 'العودة إلى غرفة المعيشة', 'right' => 'النظر إلى المطبخ',
		),
	);
	$c = $copy[ $lang ];

	$uploads      = wp_get_upload_dir();
	$panorama_url = trailingslashit( $uploads['baseurl'] ) . '2026/08/aurelia-interior-panorama-v1.png';
	$plan_url     = isset( $unit['plan'] ) ? esc_url_raw( $unit['plan'] ) : '';
	$return_url   = add_query_arg(
		array( 'project' => NADLAN_AURELIA_SLUG, 'unit' => $unit_id, 'lang' => $lang ),
		get_preview_post_link( NADLAN_AURELIA_POST_ID )
	) . '#inventory';
	$floor        = isset( $unit['floor'] ) ? (int) $unit['floor'] : 0;
	$rooms        = isset( $unit['rooms'] ) ? (float) $unit['rooms'] : 0;
	$sqm          = isset( $unit['sqm'] ) ? (float) $unit['sqm'] : 0;
	$balcony      = isset( $unit['balcony'] ) ? (float) $unit['balcony'] : 0;
	$direction    = isset( $unit['dir'] ) ? sanitize_text_field( $unit['dir'] ) : '';
	$stops        = array(
		array( 'id' => 'terrace', 'x' => 18, 'y' => 51, 'label' => $c['terrace'], 'detail' => $c['terrace_d'] ),
		array( 'id' => 'living', 'x' => 52, 'y' => 57, 'label' => $c['living'], 'detail' => $c['living_d'] ),
		array( 'id' => 'kitchen', 'x' => 82, 'y' => 53, 'label' => $c['kitchen'], 'detail' => $c['kitchen_d'] ),
	);

	nocache_headers();
	header( 'Content-Type: text/html; charset=' . get_bloginfo( 'charset' ) );
	header( 'X-Robots-Tag: noindex, nofollow', true );
	?><!doctype html>
<html lang="<?php echo esc_attr( $lang ); ?>" dir="<?php echo $rtl ? 'rtl' : 'ltr'; ?>">
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
	<meta name="robots" content="noindex,nofollow">
	<title><?php echo esc_html( $c['title'] . ' · ' . $unit_id ); ?></title>
	<style>
		:root{color-scheme:dark;--gold:#d5a65b;--ink:#0d0d0c;--panel:rgba(16,16,14,.9);--line:rgba(255,255,255,.18)}*{box-sizing:border-box}html,body{margin:0;min-height:100%;background:#090908;color:#fff;font-family:Arial,sans-serif}body{overflow:hidden}.tour{min-height:100dvh;display:grid;grid-template-rows:auto 1fr auto}.bar{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:12px clamp(14px,3vw,34px);background:var(--ink);border-bottom:1px solid var(--line);z-index:8}.brand{display:grid;gap:2px}.brand b{font-size:clamp(16px,2vw,22px)}.brand span{font-size:12px;color:#c9c3b9}.back,.cta{min-height:44px;display:inline-flex;align-items:center;justify-content:center;border-radius:999px;padding:0 16px;text-decoration:none;font-weight:700}.back{border:1px solid var(--line);color:#fff}.cta{background:var(--gold);color:#17120b}.stage{position:relative;overflow:hidden;touch-action:none;cursor:grab;background:#111;isolation:isolate}.stage:active{cursor:grabbing}.pano{position:absolute;inset:-4%;background-image:url('<?php echo esc_url( $panorama_url ); ?>');background-repeat:no-repeat;background-size:auto 108%;background-position:50% 50%;transition:background-position .55s cubic-bezier(.2,.8,.2,1);filter:saturate(.96) contrast(1.02)}.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.18),transparent 38%,rgba(0,0,0,.46));pointer-events:none}.hint{position:absolute;top:18px;left:50%;transform:translateX(-50%);z-index:2;background:rgba(0,0,0,.62);border:1px solid var(--line);border-radius:999px;padding:9px 14px;font-size:13px;white-space:nowrap}.hotspot{position:absolute;z-index:3;left:var(--x);top:var(--y);width:46px;height:46px;transform:translate(-50%,-50%);border:2px solid #fff;border-radius:50%;background:var(--gold);color:#16120c;font-weight:900;box-shadow:0 0 0 8px rgba(213,166,91,.2);cursor:pointer}.hotspot[aria-pressed="true"]{box-shadow:0 0 0 12px rgba(213,166,91,.32);transform:translate(-50%,-50%) scale(1.1)}.card{position:absolute;z-index:4;inset-inline-start:clamp(14px,3vw,34px);bottom:24px;width:min(390px,calc(100% - 28px));padding:18px;border:1px solid var(--line);border-radius:18px;background:var(--panel);backdrop-filter:blur(14px)}.card h1{font-size:clamp(22px,3vw,34px);margin:0 0 8px}.card p{margin:0;color:#ddd4c5;line-height:1.55}.dock{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;padding:12px clamp(14px,3vw,34px);background:var(--ink);border-top:1px solid var(--line)}.looks{display:flex;justify-content:center;gap:8px}.looks button,.planbtn{min-height:44px;border:1px solid var(--line);border-radius:999px;background:#171715;color:#fff;padding:0 14px;cursor:pointer}.planbtn{display:inline-flex;align-items:center;justify-content:center;text-decoration:none}.looks button[aria-pressed="true"]{border-color:var(--gold);color:#f7cf8b}.facts{display:flex;gap:12px;flex-wrap:wrap;color:#cfc7bb;font-size:12px}.facts b{color:#fff}.plan{position:fixed;inset:0;z-index:20;display:none;place-items:center;padding:24px;background:rgba(0,0,0,.82);border:0;width:100%;height:100%;max-width:none;max-height:none}.plan:target{display:grid}.planbox{position:relative;width:min(900px,96vw);max-height:88vh;padding:18px;border-radius:20px;background:#f5f1e8;color:#161514}.planbox img{display:block;max-width:100%;max-height:72vh;margin:auto}.close{position:absolute;top:10px;right:10px;width:44px;height:44px;border:0;border-radius:50%;background:#111;color:#fff;font-size:20px;cursor:pointer;text-decoration:none;display:grid;place-items:center}@media(max-width:760px){.bar{align-items:flex-start}.back{padding:0 11px;font-size:12px}.dock{grid-template-columns:1fr}.facts{justify-content:center}.looks{overflow-x:auto;justify-content:flex-start}.looks button{white-space:nowrap}.planbtn{position:absolute;right:14px;bottom:150px;z-index:5}.card{bottom:16px;padding:14px}.card h1{font-size:23px}.hint{top:12px}.pano{background-size:auto 100%}}
	</style>
</head>
<body>
<main class="tour">
	<header class="bar"><div class="brand"><b>Aurelia Sde Dov · אורליה שדה דב</b><span><?php echo esc_html( $c['title'] . ' · ' . $unit_id ); ?></span></div><a class="back" href="<?php echo esc_url( $return_url ); ?>"><?php echo esc_html( $c['back'] ); ?></a></header>
	<section class="stage" id="stage" aria-label="<?php echo esc_attr( $c['title'] ); ?>">
		<div class="pano" id="pano"></div><div class="shade"></div><div class="hint"><?php echo esc_html( $c['drag'] ); ?></div>
		<?php foreach ( $stops as $index => $stop ) : ?><button class="hotspot" style="--x:<?php echo (int) $stop['x']; ?>%;--y:<?php echo (int) $stop['y']; ?>%" data-stop="<?php echo esc_attr( $stop['id'] ); ?>" aria-label="<?php echo esc_attr( $stop['label'] ); ?>" aria-pressed="<?php echo 1 === $index ? 'true' : 'false'; ?>"><?php echo (int) $index + 1; ?></button><?php endforeach; ?>
		<article class="card" aria-live="polite"><h1 id="scene-title"><?php echo esc_html( $c['living'] ); ?></h1><p id="scene-detail"><?php echo esc_html( $c['living_d'] ); ?></p></article>
		<a class="planbtn" id="open-plan" href="#plan"><?php echo esc_html( $c['plan'] ); ?></a>
	</section>
	<footer class="dock"><div class="facts"><span><b><?php echo esc_html( $c['floor'] ); ?></b> <?php echo (int) $floor; ?></span><span><b><?php echo esc_html( $c['rooms'] ); ?></b> <?php echo esc_html( $rooms ); ?></span><span><b><?php echo esc_html( $c['sqm'] ); ?></b> <?php echo esc_html( $sqm ); ?> מ״ר</span><span><b><?php echo esc_html( $c['balcony'] ); ?></b> <?php echo esc_html( $balcony ); ?> מ״ר</span><span><b><?php echo esc_html( $c['direction'] ); ?></b> <?php echo esc_html( $direction ); ?></span></div><div class="looks"><button data-look="18"><?php echo esc_html( $c['left'] ); ?></button><button data-look="52" aria-pressed="true"><?php echo esc_html( $c['center'] ); ?></button><button data-look="82"><?php echo esc_html( $c['right'] ); ?></button></div><a class="cta" href="<?php echo esc_url( $return_url ); ?>"><?php echo esc_html( $c['cta'] ); ?></a></footer>
</main>
<div class="plan" id="plan" role="dialog" aria-label="<?php echo esc_attr( $c['plan'] ); ?>"><div class="planbox"><a class="close" id="close-plan" href="#stage" aria-label="Close">×</a><img src="<?php echo esc_url( $plan_url ); ?>" alt="<?php echo esc_attr( $c['plan'] ); ?>"></div></div>
<script>
(function(){"use strict";var stops=<?php echo wp_json_encode( $stops, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ); ?>,stage=document.getElementById("stage"),pano=document.getElementById("pano"),title=document.getElementById("scene-title"),detail=document.getElementById("scene-detail"),pos=52,start=0,startPos=52,drag=false;function clamp(v){return Math.max(5,Math.min(95,v));}function look(x,id){pos=clamp(Number(x)||52);pano.style.backgroundPosition=pos+"% 50%";document.querySelectorAll("[data-look]").forEach(function(b){b.setAttribute("aria-pressed",Math.abs(Number(b.dataset.look)-pos)<2?"true":"false");});document.querySelectorAll("[data-stop]").forEach(function(b){b.setAttribute("aria-pressed",b.dataset.stop===id?"true":"false");});if(id){var s=stops.find(function(item){return item.id===id;});if(s){title.textContent=s.label;detail.textContent=s.detail;}}}document.querySelectorAll("[data-look]").forEach(function(b){b.addEventListener("click",function(){look(b.dataset.look,b.dataset.look<30?"terrace":(b.dataset.look>70?"kitchen":"living"));});});document.querySelectorAll("[data-stop]").forEach(function(b){b.addEventListener("click",function(){var s=stops.find(function(item){return item.id===b.dataset.stop;});look(s?s.x:52,b.dataset.stop);});});stage.addEventListener("pointerdown",function(e){if(e.target.closest("button")){return;}drag=true;start=e.clientX;startPos=pos;stage.setPointerCapture(e.pointerId);});stage.addEventListener("pointermove",function(e){if(!drag){return;}look(startPos-(e.clientX-start)/stage.clientWidth*70);});stage.addEventListener("pointerup",function(){drag=false;});stage.addEventListener("keydown",function(e){if(e.key==="ArrowLeft"){look(pos-7);}if(e.key==="ArrowRight"){look(pos+7);}});look(52,"living");})();
</script>
</body></html><?php
	exit;
}
add_action( 'template_redirect', 'nadlan_aurelia_render_interior_tour', -100 );

/**
 * The shared project template contains sales-copy placeholders intended for
 * projects whose data is incomplete. Aurelia is the complete recipe rig, so
 * remove those placeholders in the server response itself. This keeps the raw
 * public source aligned with the visible experience, not only the painted DOM.
 */
function nadlan_aurelia_clean_public_html( $html ) {
	$html = preg_replace(
		'#<aside\b[^>]*class=(["\'])[^"\']*\bnl-projnotice\b[^"\']*\1[^>]*>.*?</aside>#isu',
		'',
		$html
	);

	$replacements = array(
		'לפי גובה הקומה והכיוון · בקרוב' => 'לפי גובה הקומה והכיוון',
		'הסביבה בתלת ממד · בקרוב' => 'הסביבה בתלת ממד',
		'כדור הארץ בתלת ממד אמיתי · בקרוב' => 'כדור הארץ בתלת ממד אמיתי',
		'מחיר ואומדן באזור' => 'מחירים בשדה דב',
		'מחיר ואומדן' => 'מחירים',
		'אומדן מחיר ועסקאות השוואה יוצגו עם קבלת נתונים מאומתים.' => 'מחירי הדירות ועסקאות השוואה בשדה דב.',
		'המודל, החזית והדירות הם המחשה ראשונית ואינם תוכנית מכר או מלאי מאושר. מחיר וזמינות יש לאמת מול היזם. אין באמור הצעה או התחייבות.' => '',
		'טווח מחירי הדירות המפורסמות בפרויקט. אומדן לא מחייב.' => 'טווח מחירי הדירות בפרויקט.',
		'מחיר ממוצע למ״ר בפרויקט, דירות 88-196 מ״ר. אומדן לא מחייב.' => 'מחיר ממוצע למ״ר בפרויקט, בדירות 88–196 מ״ר.',
		'האומדנים מבוססים על נתונים גלויים בקטלוג נדלן ואינם מחייבים. יש לאמת מחירים מול היזם.' => 'המחירים מוצגים לצד תוכניות הדירות וזמינותן.',
		'סדר גודל של החזר חודשי לדירת ~90 מ״ר. אומדן לא מחייב, תלוי במסלול ובריבית.' => 'החזר חודשי לדירת כ־90 מ״ר לפי מסלול המימון שנבחר.',
		'השלב כפי שדווח לפרויקט; לוחות הזמנים באחריות היזם.' => '',
		'בוחרים יום ושעה נוחים ושולחים בקשה. המועד כפוף לאישור הגורם המוסמך בפרויקט. ללא תשלום וללא התחייבות.' => 'בחרו יום ושעה והבקשה תישלח לצוות הפרויקט.',
	);

	return str_replace( array_keys( $replacements ), array_values( $replacements ), $html );
}

function nadlan_aurelia_start_public_buffer() {
	if ( nadlan_aurelia_is_prototype_request() ) {
		ob_start( 'nadlan_aurelia_clean_public_html' );
	}
}
add_action( 'template_redirect', 'nadlan_aurelia_start_public_buffer', 0 );

/**
 * Load the durable recipe data bundled with the adapter. These files are also
 * the hand-off contract for future agents and the development team.
 */
function nadlan_aurelia_data_file( $filename ) {
	$path = plugin_dir_path( __FILE__ ) . 'data/' . basename( $filename );
	if ( ! is_readable( $path ) ) {
		return array();
	}

	$data = json_decode( (string) file_get_contents( $path ), true );
	return is_array( $data ) ? $data : array();
}

/** Parse the exact public HTTP response without executing client-side code. */
function nadlan_aurelia_parse_public_source( $html ) {
	$parsed = array(
		'title'        => '',
		'canonical'    => 0,
		'h1'           => 0,
		'favicon'      => 0,
		'json_ld'      => 0,
		'scripts'      => 0,
		'styles'       => 0,
		'duplicate_ids'=> 0,
	);
	if ( ! class_exists( 'DOMDocument' ) ) {
		return $parsed;
	}

	$previous = libxml_use_internal_errors( true );
	$dom = new DOMDocument();
	$dom->loadHTML( '<?xml encoding="utf-8" ?>' . $html );
	$xpath = new DOMXPath( $dom );
	$titles = $dom->getElementsByTagName( 'title' );
	$parsed['title'] = $titles->length ? trim( $titles->item( 0 )->textContent ) : '';
	$parsed['canonical'] = (int) $xpath->query( '//link[translate(@rel,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")="canonical"]' )->length;
	$parsed['h1'] = (int) $dom->getElementsByTagName( 'h1' )->length;
	$parsed['favicon'] = (int) $xpath->query( '//link[contains(translate(@rel,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"icon")]' )->length;
	$parsed['json_ld'] = (int) $xpath->query( '//script[translate(@type,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")="application/ld+json"]' )->length;
	$parsed['scripts'] = (int) $dom->getElementsByTagName( 'script' )->length;
	$parsed['styles'] = (int) $dom->getElementsByTagName( 'style' )->length + (int) $xpath->query( '//link[translate(@rel,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")="stylesheet"]' )->length;
	$ids = array();
	foreach ( $xpath->query( '//*[@id]' ) as $node ) {
		$id = (string) $node->getAttribute( 'id' );
		$ids[ $id ] = isset( $ids[ $id ] ) ? $ids[ $id ] + 1 : 1;
	}
	$parsed['duplicate_ids'] = count( array_filter( $ids, function( $count ) { return $count > 1; } ) );
	libxml_clear_errors();
	libxml_use_internal_errors( $previous );
	return $parsed;
}

/** Capture and retain the full public View Source body plus its parsed evidence. */
function nadlan_aurelia_capture_public_source() {
	$post_id = isset( $_GET['post_id'] ) ? absint( $_GET['post_id'] ) : 0;
	if ( ! $post_id || ! current_user_can( 'edit_post', $post_id ) ) {
		wp_die( esc_html__( 'You are not allowed to capture this page.', 'nadlan-aurelia' ) );
	}
	check_admin_referer( 'nadlan_aurelia_capture_source_' . $post_id );

	$url = get_permalink( $post_id );
	$response = wp_remote_get(
		$url,
		array(
			'timeout'     => 25,
			'redirection' => 5,
			'user-agent'  => 'NadLan-Public-Source-Forensics/1.0',
			'headers'     => array( 'X-Nadlan-Source-Snapshot' => '1' ),
		)
	);

	$snapshot = array(
		'captured_at' => current_time( 'mysql', true ),
		'url'         => esc_url_raw( $url ),
		'status'      => 0,
		'bytes'       => 0,
		'sha256'      => '',
		'file'        => '',
		'file_url'    => '',
		'parsed'      => array(),
		'error'       => '',
	);

	if ( is_wp_error( $response ) ) {
		$snapshot['error'] = $response->get_error_message();
	} else {
		$body = (string) wp_remote_retrieve_body( $response );
		$snapshot['status'] = (int) wp_remote_retrieve_response_code( $response );
		$snapshot['bytes'] = strlen( $body );
		$snapshot['sha256'] = strtoupper( hash( 'sha256', $body ) );
		$snapshot['parsed'] = nadlan_aurelia_parse_public_source( $body );

		$uploads = wp_upload_dir();
		$relative_dir = 'nadlan-source-snapshots/' . $post_id;
		$target_dir = trailingslashit( $uploads['basedir'] ) . $relative_dir;
		if ( wp_mkdir_p( $target_dir ) ) {
			$filename = gmdate( 'Ymd-His' ) . '-' . substr( strtolower( $snapshot['sha256'] ), 0, 12 ) . '.html';
			$target = trailingslashit( $target_dir ) . $filename;
			$written = file_put_contents( $target, $body ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_system_operations_file_put_contents
			if ( false !== $written ) {
				$snapshot['file'] = $relative_dir . '/' . $filename;
				$snapshot['file_url'] = trailingslashit( $uploads['baseurl'] ) . $relative_dir . '/' . $filename;
			} else {
				$snapshot['error'] = 'The public source was fetched but could not be written.';
			}
		} else {
			$snapshot['error'] = 'The source snapshot directory could not be created.';
		}
	}

	update_post_meta( $post_id, '_nadlan_source_snapshot_latest', $snapshot );
	wp_safe_redirect( add_query_arg( 'nadlan_source_captured', $snapshot['error'] ? '0' : '1', get_edit_post_link( $post_id, 'url' ) ) );
	exit;
}
add_action( 'admin_post_nadlan_aurelia_capture_source', 'nadlan_aurelia_capture_public_source' );

/**
 * A light reports evidence and a next action. It never blocks saving or
 * publishing; the editor remains responsible for the decision.
 */
function nadlan_aurelia_light( $status, $label, $evidence, $target = '' ) {
	return array(
		'status'   => in_array( $status, array( 'red', 'orange', 'yellow', 'green' ), true ) ? $status : 'yellow',
		'label'    => $label,
		'evidence' => $evidence,
		'target'   => $target,
	);
}

function nadlan_aurelia_present( $post_id, $key ) {
	$value = get_post_meta( $post_id, $key, true );
	return is_array( $value ) ? ! empty( $value ) : '' !== trim( (string) $value );
}

/**
 * Calculate the first live set of recipe lights from the same fields consumed
 * by the public showroom.
 */
function nadlan_aurelia_recipe_lights( $post_id ) {
	$post        = get_post( $post_id );
	$units       = nadlan_aurelia_json_meta( $post_id, 'project_3d_units' );
	$drawings    = nadlan_aurelia_json_meta( $post_id, 'project_3d_drawings_json' );
	$environment = nadlan_aurelia_json_meta( $post_id, 'project_3d_environment_json' );
	$facilities  = nadlan_aurelia_json_meta( $post_id, 'project_facilities' );
	$bom         = nadlan_aurelia_data_file( 'engineering-bom.json' );
	$recipe      = nadlan_aurelia_data_file( 'recipe-checklist.json' );

	$unit_count      = count( $units );
	$units_with_plan = 0;
	$units_with_view = 0;
	$units_with_price = 0;
	$units_with_selection = 0;
	foreach ( $units as $unit ) {
		if ( ! empty( $unit['plan'] ) ) {
			$units_with_plan++;
		}
		if ( ! empty( $unit['dir'] ) && ! empty( $unit['view'] ) ) {
			$units_with_view++;
		}
		if ( ! empty( $unit['price'] ) || ! empty( $unit['price_estimate'] ) ) {
			$units_with_price++;
		}
		if ( ! empty( $unit['selection']['anchor']['position'] ) && ! empty( $unit['selection']['anchor']['normal'] ) && isset( $unit['selection']['hitRegion'] ) ) {
			$units_with_selection++;
		}
	}

	$bom_systems    = isset( $bom['systems'] ) && is_array( $bom['systems'] ) ? count( $bom['systems'] ) : 0;
	$bom_assemblies = 0;
	$bom_components = 0;
	foreach ( isset( $bom['systems'] ) && is_array( $bom['systems'] ) ? $bom['systems'] : array() as $system ) {
		$assemblies      = isset( $system['assemblies'] ) && is_array( $system['assemblies'] ) ? $system['assemblies'] : array();
		$bom_assemblies += count( $assemblies );
		foreach ( $assemblies as $assembly ) {
			$bom_components += isset( $assembly['components'] ) && is_array( $assembly['components'] ) ? count( $assembly['components'] ) : 0;
		}
	}

	$recipe_checks = 0;
	foreach ( isset( $recipe['domains'] ) && is_array( $recipe['domains'] ) ? $recipe['domains'] : array() as $domain ) {
		$recipe_checks += isset( $domain['checks'] ) && is_array( $domain['checks'] ) ? count( $domain['checks'] ) : 0;
	}

	$title      = $post ? (string) $post->post_title : '';
	$content    = $post ? wp_strip_all_tags( strip_shortcodes( $post->post_content ) ) : '';
	$word_tokens = preg_split( '/\s+/u', trim( preg_replace( '/[^\p{L}\p{N}\s-]+/u', ' ', $content ) ) );
	$word_count  = is_array( $word_tokens ) && '' !== trim( $content ) ? count( array_filter( $word_tokens ) ) : 0;
	$address    = (string) get_post_meta( $post_id, 'address', true );
	$seo_title  = (string) get_post_meta( $post_id, '_yoast_wpseo_title', true );
	$seo_desc   = (string) get_post_meta( $post_id, '_yoast_wpseo_metadesc', true );
	$source_snapshot = get_post_meta( $post_id, '_nadlan_source_snapshot_latest', true );
	$source_snapshot = is_array( $source_snapshot ) ? $source_snapshot : array();

	$lights = array();
	$lights[] = nadlan_aurelia_light(
		false !== mb_strpos( $title, 'Aurelia' ) && ( false !== mb_strpos( $title, 'שדה דב' ) || false !== mb_strpos( $address, 'שדה דב' ) ) ? 'green' : 'orange',
		'זהות ומיקום',
		'כותרת: ' . $title . ' · כתובת: ' . ( $address ? $address : 'חסרה' ),
		'#title'
	);
	$lights[] = nadlan_aurelia_light(
		$seo_title && $seo_desc ? 'green' : 'red',
		'SERP',
		$seo_title && $seo_desc ? 'כותרת ותיאור SEO שמורים' : 'חסרה כותרת או תיאור SEO',
		'#wpseo_meta'
	);
	$lights[] = nadlan_aurelia_light(
		nadlan_aurelia_present( $post_id, 'project_model_glb' ) && nadlan_aurelia_present( $post_id, 'project_model_poster' ) ? 'green' : 'red',
		'מודל תלת־ממד',
		'GLB: ' . ( nadlan_aurelia_present( $post_id, 'project_model_glb' ) ? 'קיים' : 'חסר' ) . ' · poster: ' . ( nadlan_aurelia_present( $post_id, 'project_model_poster' ) ? 'קיים' : 'חסר' ),
		'#project_3d_model_type'
	);
	$lights[] = nadlan_aurelia_light(
		$unit_count >= 1 && $units_with_plan === $unit_count && $units_with_price === $unit_count ? 'green' : ( $unit_count ? 'orange' : 'red' ),
		'מלאי דירות',
		$unit_count . ' יחידות · ' . $units_with_plan . ' תוכניות · ' . $units_with_price . ' מחירים',
		'#project_3d_units'
	);
	$lights[] = nadlan_aurelia_light(
		$unit_count >= 1 && $units_with_selection === $unit_count ? 'green' : ( $units_with_selection ? 'orange' : 'red' ),
		'בחירת דירה על המודל',
		$units_with_selection . '/' . $unit_count . ' יחידות עם anchor, normal ו-hit region · stage_x/y אינם מקור runtime',
		'#project_3d_units'
	);
	$lights[] = nadlan_aurelia_light(
		$unit_count >= 1 && $units_with_view === $unit_count && count( $environment ) >= 8 ? 'green' : 'orange',
		'כיוון, נוף וסביבה',
		$units_with_view . '/' . $unit_count . ' יחידות עם כיוון ונוף · ' . count( $environment ) . ' נקודות סביבה',
		'#project_3d_environment_json'
	);
	$lights[] = nadlan_aurelia_light(
		count( $drawings ) >= 5 ? 'green' : ( count( $drawings ) ? 'yellow' : 'red' ),
		'תוכניות ושרטוטים',
		count( $drawings ) . ' קובצי שרטוט מחוברים',
		'#project_3d_drawings_json'
	);
	$lights[] = nadlan_aurelia_light(
		count( $facilities ) >= 8 ? 'green' : ( count( $facilities ) ? 'yellow' : 'red' ),
		'מתקנים',
		count( $facilities ) . ' מתקנים במודל הנתונים; בדיקת hotspot אינטראקטיבי תבוצע בפרונט',
		'#project_facilities'
	);
	$lights[] = nadlan_aurelia_light(
		$bom_systems >= 15 && $bom_components >= 60 ? 'green' : ( $bom_systems ? 'yellow' : 'red' ),
		'BOM והנדסת בניין',
		$bom_systems . ' מערכות · ' . $bom_assemblies . ' מכלולים · ' . $bom_components . ' רכיבים',
		'#nadlan-aurelia-bom'
	);
	$lights[] = nadlan_aurelia_light(
		$recipe_checks >= 100 ? 'green' : ( $recipe_checks ? 'yellow' : 'red' ),
		'עומק המתכון',
		$recipe_checks . ' בדיקות מפורטות ב-' . count( isset( $recipe['domains'] ) ? $recipe['domains'] : array() ) . ' תחומים · גרסה ' . ( isset( $recipe['schemaVersion'] ) ? $recipe['schemaVersion'] : 'לא ידועה' ),
		'#nadlan-aurelia-recipe'
	);
	$lights[] = nadlan_aurelia_light(
		$word_count >= 4500 ? 'green' : ( $word_count >= 1000 ? 'yellow' : 'red' ),
		'תוכן הפרויקט',
		number_format_i18n( $word_count ) . ' מילים בגוף העמוד',
		'#content'
	);
	$source_status = isset( $source_snapshot['status'] ) ? (int) $source_snapshot['status'] : 0;
	$source_hash = isset( $source_snapshot['sha256'] ) ? (string) $source_snapshot['sha256'] : '';
	$source_age = ! empty( $source_snapshot['captured_at'] ) ? time() - strtotime( $source_snapshot['captured_at'] . ' UTC' ) : PHP_INT_MAX;
	$source_light = 200 === $source_status && $source_hash ? ( $source_age <= 7 * DAY_IN_SECONDS ? 'green' : 'yellow' ) : ( $source_status ? 'red' : 'orange' );
	$source_parsed = isset( $source_snapshot['parsed'] ) && is_array( $source_snapshot['parsed'] ) ? $source_snapshot['parsed'] : array();
	$lights[] = nadlan_aurelia_light(
		$source_light,
		'HTML ציבורי',
		$source_hash ? 'HTTP ' . $source_status . ' · SHA …' . substr( $source_hash, -12 ) . ' · H1 ' . ( isset( $source_parsed['h1'] ) ? $source_parsed['h1'] : '?' ) . ' · favicon ' . ( isset( $source_parsed['favicon'] ) ? $source_parsed['favicon'] : '?' ) . ' · scripts ' . ( isset( $source_parsed['scripts'] ) ? $source_parsed['scripts'] : '?' ) : 'טרם נשמר snapshot של View Source הציבורי',
		''
	);
	$lights[] = nadlan_aurelia_light(
		'orange',
		'מובייל וכל הקלקה',
		'נדרשת הרצה ב-320, 360, 390 ו-430 פיקסל כולל hotspot, כרטיס, תוכנית, נוף, סטודיו, ליד ו-Co-tour',
		''
	);

	return $lights;
}

function nadlan_aurelia_add_recipe_boxes() {
	add_meta_box(
		'nadlan-aurelia-recipe',
		'מתכון פרויקט · נורות מצב',
		'nadlan_aurelia_render_recipe_box',
		'nadlan_project',
		'normal',
		'high'
	);
	add_meta_box(
		'nadlan-aurelia-bom',
		'BOM · מערכות ומכלולים',
		'nadlan_aurelia_render_bom_box',
		'nadlan_project',
		'normal',
		'default'
	);
}
add_action( 'add_meta_boxes', 'nadlan_aurelia_add_recipe_boxes' );

function nadlan_aurelia_render_recipe_box( $post ) {
	if ( NADLAN_AURELIA_POST_ID !== (int) $post->ID ) {
		echo '<p>המתכון מופעל כעת רק על פרויקט האב אורליה.</p>';
		return;
	}

	$lights = nadlan_aurelia_recipe_lights( $post->ID );
	$counts = array( 'red' => 0, 'orange' => 0, 'yellow' => 0, 'green' => 0 );
	foreach ( $lights as $light ) {
		$counts[ $light['status'] ]++;
	}

	echo '<style>
		.nal-recipe-summary{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 14px}
		.nal-recipe-count{border:1px solid #dcdcde;border-radius:999px;padding:5px 10px;background:#fff;font-weight:600}
		.nal-recipe-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px}
		.nal-recipe-light{border:1px solid #dcdcde;border-right:5px solid var(--nal-color);border-radius:8px;padding:12px;background:#fff}
		.nal-recipe-light strong{display:block;margin-bottom:5px}
		.nal-recipe-light p{margin:0;color:#50575e}
		.nal-recipe-light a{display:inline-block;margin-top:7px}
		.nal-green{--nal-color:#16883f}.nal-yellow{--nal-color:#dba617}.nal-orange{--nal-color:#d86b16}.nal-red{--nal-color:#c92c2c}
	</style>';
	echo '<div class="nal-recipe-summary">';
	foreach ( array( 'red' => 'אדומות', 'orange' => 'כתומות', 'yellow' => 'צהובות', 'green' => 'ירוקות' ) as $key => $label ) {
		echo '<span class="nal-recipe-count nal-' . esc_attr( $key ) . '">' . esc_html( $label . ': ' . $counts[ $key ] ) . '</span>';
	}
	echo '<span class="nal-recipe-count">לא חוסם שמירה</span></div>';
	$capture_url = wp_nonce_url(
		add_query_arg(
			array(
				'action'  => 'nadlan_aurelia_capture_source',
				'post_id' => $post->ID,
			),
			admin_url( 'admin-post.php' )
		),
		'nadlan_aurelia_capture_source_' . $post->ID
	);
	$snapshot = get_post_meta( $post->ID, '_nadlan_source_snapshot_latest', true );
	$snapshot = is_array( $snapshot ) ? $snapshot : array();
	echo '<p><a class="button button-secondary" href="' . esc_url( $capture_url ) . '">צילום View Source ציבורי עכשיו</a> <span style="color:#646970">הפעולה קוראת את כתובת העמוד הפומבית, שומרת את גוף ה-HTML המלא ומעדכנת fingerprints; היא אינה משנה את העמוד.</span></p>';
	if ( ! empty( $snapshot['sha256'] ) ) {
		echo '<p><code>' . esc_html( isset( $snapshot['captured_at'] ) ? $snapshot['captured_at'] : '' ) . ' · HTTP ' . esc_html( isset( $snapshot['status'] ) ? $snapshot['status'] : 0 ) . ' · SHA-256 ' . esc_html( $snapshot['sha256'] ) . '</code>';
		if ( ! empty( $snapshot['file_url'] ) ) {
			echo ' <a href="' . esc_url( $snapshot['file_url'] ) . '" target="_blank" rel="noopener">פתיחת המקור השמור</a>';
		}
		echo '</p>';
	}
	echo '<div class="nal-recipe-grid">';
	foreach ( $lights as $light ) {
		echo '<section class="nal-recipe-light nal-' . esc_attr( $light['status'] ) . '">';
		echo '<strong>' . esc_html( $light['label'] ) . '</strong>';
		echo '<p>' . esc_html( $light['evidence'] ) . '</p>';
		if ( $light['target'] ) {
			echo '<a href="' . esc_attr( $light['target'] ) . '">לשדה או למקטע</a>';
		}
		echo '</section>';
	}
	echo '</div>';
}

function nadlan_aurelia_render_bom_box( $post ) {
	if ( NADLAN_AURELIA_POST_ID !== (int) $post->ID ) {
		echo '<p>ה-BOM מופעל כעת רק על פרויקט האב אורליה.</p>';
		return;
	}

	$bom = nadlan_aurelia_data_file( 'engineering-bom.json' );
	if ( empty( $bom['systems'] ) ) {
		echo '<p>קובץ ה-BOM אינו זמין.</p>';
		return;
	}

	echo '<p><strong>גרסה ' . esc_html( isset( $bom['schemaVersion'] ) ? $bom['schemaVersion'] : '' ) . '</strong> · ' . esc_html( $bom['site'] ) . '</p>';
	echo '<p>' . esc_html( $bom['purpose'] ) . '</p>';
	foreach ( $bom['systems'] as $system ) {
		$assemblies = isset( $system['assemblies'] ) && is_array( $system['assemblies'] ) ? $system['assemblies'] : array();
		$components = 0;
		foreach ( $assemblies as $assembly ) {
			$components += isset( $assembly['components'] ) && is_array( $assembly['components'] ) ? count( $assembly['components'] ) : 0;
		}
		echo '<details style="border-top:1px solid #dcdcde;padding:10px 0">';
		echo '<summary><strong>' . esc_html( $system['id'] . ' · ' . $system['name'] ) . '</strong> — ' . esc_html( count( $assemblies ) . ' מכלולים, ' . $components . ' רכיבים' ) . '</summary>';
		echo '<p>' . esc_html( isset( $system['publicSummary'] ) ? $system['publicSummary'] : '' ) . '</p>';
		echo '<ul>';
		foreach ( $assemblies as $assembly ) {
			echo '<li><strong>' . esc_html( $assembly['id'] . ' · ' . $assembly['name'] ) . '</strong><ul>';
			foreach ( isset( $assembly['components'] ) ? $assembly['components'] : array() as $component ) {
				echo '<li><code>' . esc_html( $component['code'] ) . '</code> ' . esc_html( $component['item'] ) . ' — ' . esc_html( $component['spec'] ) . '</li>';
			}
			echo '</ul></li>';
		}
		echo '</ul></details>';
	}
}
