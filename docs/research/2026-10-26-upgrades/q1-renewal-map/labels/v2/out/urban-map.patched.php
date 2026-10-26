<?php
/**
 * nadlan-config - URBAN RENEWAL MAP + advisor wiring (L5, 2026-07-12).
 *
 * 1. Adds the renewal advisor kinds to the RFP matcher (filter added in
 *    rfp.php): shamai / mefakeach / organizer, so the wizard and the
 *    project space can request quotes from the real directory.
 * 2. /urban-renewal/map/: city-cluster map over the ~938 imported gov.il
 *    compounds. HONEST V1: the import carries no lat/lng, so the map shows
 *    CITY AGGREGATES with counts by track (never fake per-building pins);
 *    per-compound pins arrive after a geocoding enrichment pass.
 *
 * Feature gate: option nadlan_feature_renewal_map ('1' = on).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_filter( 'nadlan_rfp_advisor_map', function ( $map ) {
	$map['shamai']    = array( 'shamai', 'appraiser' );
	$map['mefakeach'] = array( 'mefakeach', 'inspector', 'bedek_bait' );
	$map['organizer'] = array( 'organizer', 'urban_renewal_manager' );
	return $map;
} );

if ( ! function_exists( 'nadlan_ur_map_on' ) ) {
	function nadlan_ur_map_on() { return get_option( 'nadlan_feature_renewal_map', '1' ) === '1'; }
}

/* filterable He city -> [lng, lat] centroids for the aggregate map */
if ( ! function_exists( 'nadlan_ur_city_centroids' ) ) {
	function nadlan_ur_city_centroids() {
		return apply_filters( 'nadlan_ur_city_centroids', array(
			'תל אביב'      => array( 34.7818, 32.0853 ), 'תל אביב-יפו' => array( 34.7818, 32.0853 ),
			'ירושלים'      => array( 35.2137, 31.7683 ), 'חיפה' => array( 34.9896, 32.7940 ),
			'ראשון לציון'  => array( 34.7894, 31.9730 ), 'פתח תקווה' => array( 34.8878, 32.0871 ),
			'אשדוד'        => array( 34.6553, 31.8014 ), 'נתניה' => array( 34.8532, 32.3215 ),
			'באר שבע'      => array( 34.7913, 31.2530 ), 'בני ברק' => array( 34.8338, 32.0807 ),
			'חולון'        => array( 34.7722, 32.0158 ), 'רמת גן' => array( 34.8114, 32.0684 ),
			'בת ים'        => array( 34.7519, 32.0171 ), 'רחובות' => array( 34.8113, 31.8928 ),
			'הרצליה'       => array( 34.8434, 32.1663 ), 'כפר סבא' => array( 34.9068, 32.1750 ),
			'חדרה'         => array( 34.9196, 32.4340 ), 'לוד' => array( 34.8903, 31.9514 ),
			'רמלה'         => array( 34.8722, 31.9293 ), 'גבעתיים' => array( 34.8100, 32.0723 ),
			'קרית אונו'    => array( 34.8555, 32.0636 ), 'רעננה' => array( 34.8708, 32.1836 ),
			'קרית ים'      => array( 35.0691, 32.8497 ), 'קרית ביאליק' => array( 35.0856, 32.8275 ),
			'קרית מוצקין'  => array( 35.0777, 32.8369 ), 'עכו' => array( 35.0818, 32.9281 ),
			'נהריה'        => array( 35.0925, 33.0058 ), 'טבריה' => array( 35.5312, 32.7922 ),
			'אשקלון'       => array( 34.5715, 31.6688 ), 'דימונה' => array( 35.0320, 31.0658 ),
			'אילת'         => array( 34.9482, 29.5581 ), 'בית שמש' => array( 34.9886, 31.7304 ),
			'הוד השרון'    => array( 34.8878, 32.1556 ), 'רמת השרון' => array( 34.8395, 32.1461 ),
			'יהוד'         => array( 34.8907, 32.0331 ), 'אור יהודה' => array( 34.8500, 32.0292 ),
			'גבעת שמואל'   => array( 34.8480, 32.0781 ), 'קרית גת' => array( 34.7642, 31.6100 ),
			'נצרת'         => array( 35.2985, 32.7021 ), 'עפולה' => array( 35.2908, 32.6078 ),
			// registry spelling variants + the rest of the towns in the register
			'גבעתים'       => array( 34.8100, 32.0723 ), 'פתח תקוה' => array( 34.8878, 32.0871 ),
			'אבן יהודה'    => array( 34.8870, 32.2630 ), 'אור עקיבא' => array( 34.9170, 32.5060 ),
			'אזור'         => array( 34.8060, 32.0240 ), 'אריאל' => array( 35.1870, 32.1060 ),
			'באר יעקב'     => array( 34.8310, 31.9450 ), 'בית דגן' => array( 34.8300, 32.0020 ),
			'בית שאן'      => array( 35.4970, 32.4970 ), 'בנימינה גבעת עדה' => array( 34.9490, 32.5140 ),
			'גדרה'         => array( 34.7790, 31.8140 ), 'זכרון יעקב' => array( 34.9520, 32.5730 ),
			'חצור הגלילית' => array( 35.5430, 32.9810 ), 'טירה' => array( 34.9500, 32.2330 ),
			'טירת כרמל'    => array( 34.9720, 32.7600 ), 'יבנה' => array( 34.7400, 31.8780 ),
			'יקנעם עילית'  => array( 35.0890, 32.6590 ), 'כפר יונה' => array( 34.9350, 32.3170 ),
			'כפר קאסם'     => array( 34.9770, 32.1140 ), 'כרמיאל' => array( 35.2950, 32.9190 ),
			'מבשרת ציון'   => array( 35.1500, 31.8010 ), 'מגדל העמק' => array( 35.2400, 32.6750 ),
			'מזכרת בתיה'   => array( 34.8370, 31.8530 ), 'מעלה אדומים' => array( 35.2980, 31.7770 ),
			'נוף הגליל'    => array( 35.3200, 32.7020 ), 'נס ציונה' => array( 34.8000, 31.9300 ),
			'נשר'          => array( 35.0450, 32.7660 ), 'נתיבות' => array( 34.5880, 31.4220 ),
			'סחנין'        => array( 35.2970, 32.8640 ), 'עתלית' => array( 34.9400, 32.6880 ),
			'פרדס חנה כרכור' => array( 34.9770, 32.4740 ), 'צורן קדימה' => array( 34.9360, 32.2840 ),
			'צפת'          => array( 35.4950, 32.9650 ), 'קרית אתא' => array( 35.1060, 32.8110 ),
			'קרית טבעון'   => array( 35.1270, 32.7160 ), 'קרית מלאכי' => array( 34.7480, 31.7290 ),
			'קרית עקרון'   => array( 34.8210, 31.8600 ), 'קרית שמונה' => array( 35.5700, 33.2070 ),
			'שדרות'        => array( 34.5960, 31.5250 ), 'שלומי' => array( 35.1440, 33.0750 ),
			'תל מונד'      => array( 34.9170, 32.2500 ),
			'ערד'          => array( 35.2126, 31.2589 ), // v2 labels (26.10.2026): on the authority map from its 20.10.2026 check, not in our import
		) );
	}
}

/* v2 labels (proposal 26.10.2026): the centroids and the official apartment price medians the site already shows
   (assets/instruments/data/value.json: Tax Authority closed deals by room count, from the public summary files of nadlan.gov.il),
   printed once into the map script so the tags can say a price range without a new request. Unknown = omitted: a city without a
   median gets no price. */
if ( ! function_exists( 'nadlan_ur_map_v2_boot' ) ) {
	function nadlan_ur_map_v2_boot() {
		static $out = null;
		if ( null !== $out ) { return $out; }
		$px   = array();
		$src  = array();
		$path = dirname( __DIR__ ) . '/assets/instruments/data/value.json';
		$v    = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
		if ( is_array( $v ) && ! empty( $v['cities'] ) && is_array( $v['cities'] ) ) {
			foreach ( $v['cities'] as $name => $c ) {
				$row = array();
				foreach ( array( 'r3', 'r4', 'r5' ) as $k ) {
					if ( ! empty( $c[ $k ] ) ) {
						$row[ $k ] = array( (int) $c[ $k ], (string) ( $c[ 'q' . substr( $k, 1 ) ] ?? ( $c['q'] ?? '' ) ) );
					}
				}
				if ( $row ) {
					$row['page'] = (string) ( $c['page'] ?? '' );
					$px[ (string) $name ] = $row;
				}
			}
			$src = array( 'source' => (string) ( $v['source'] ?? '' ), 'url' => (string) ( $v['url'] ?? '' ), 'file' => (string) ( $v['file'] ?? '' ) );
		}
		$cent = array();
		foreach ( nadlan_ur_city_centroids() as $k => $ll ) { $cent[ (string) $k ] = array( (float) $ll[0], (float) $ll[1] ); }
		$out = wp_json_encode( array(
			'px'     => (object) $px,
			'pxsrc'  => (object) $src,
			'cent'   => (object) $cent,
			'pulled' => function_exists( 'nadlan_ur_source_pulled' ) ? (string) nadlan_ur_source_pulled() : '13.7.2026',
		), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG | JSON_HEX_AMP );
		if ( ! is_string( $out ) || '' === $out ) { $out = '{}'; }
		return $out;
	}
}

/* city aggregates - one computation feeding BOTH the map REST payload and the
   server-rendered (crawlable) city directory on the page */
if ( ! function_exists( 'nadlan_ur_map_cities' ) ) {
	function nadlan_ur_map_cities() {
		$hit = get_transient( 'nadlan_ur_mapdata_v4' );
		if ( is_array( $hit ) ) { return $hit; }
		global $wpdb;
		$rows = $wpdb->get_results( "
			SELECT c.meta_value AS city, t.meta_value AS track, COUNT(*) AS n
			FROM {$wpdb->posts} p
			JOIN {$wpdb->postmeta} s ON s.post_id = p.ID AND s.meta_key = 'source' AND s.meta_value = 'urban_renewal'
			JOIN {$wpdb->postmeta} c ON c.post_id = p.ID AND c.meta_key = 'city'
			LEFT JOIN {$wpdb->postmeta} t ON t.post_id = p.ID AND t.meta_key = 'renewal_track'
			WHERE p.post_type = 'nadlan_project' AND p.post_status = 'publish'
			AND NOT EXISTS (SELECT 1 FROM {$wpdb->postmeta} private_v2
				WHERE private_v2.post_id=p.ID AND private_v2.meta_key='_nadlan_private_unit_journey' AND private_v2.meta_value='private-unit-journey-v2')
			GROUP BY c.meta_value, t.meta_value
		", ARRAY_A );
		$cities = array();
		$cent = nadlan_ur_city_centroids();
		// normalize: gov.il city names vary in hyphenation ("תל אביב יפו" vs "תל אביב-יפו")
		$cent_norm = array();
		foreach ( $cent as $k => $v ) { $cent_norm[ str_replace( array( '-', '  ' ), ' ', $k ) ] = $v; }
		foreach ( (array) $rows as $r ) {
			$city = trim( (string) $r['city'] );
			if ( '' === $city ) { continue; }
			if ( ! isset( $cities[ $city ] ) ) {
				$cities[ $city ] = array( 'city' => $city, 'count' => 0, 'misui' => 0, 'rashuyot' => 0,
					'lnglat' => $cent[ $city ] ?? ( $cent_norm[ str_replace( array( '-', '  ' ), ' ', $city ) ] ?? null ) );
			}
			$cities[ $city ]['count'] += (int) $r['n'];
			if ( 'misui' === $r['track'] ) { $cities[ $city ]['misui'] += (int) $r['n']; }
			if ( 'rashuyot' === $r['track'] ) { $cities[ $city ]['rashuyot'] += (int) $r['n']; }
		}
		$out = array( 'total' => array_sum( wp_list_pluck( $cities, 'count' ) ), 'cities' => array_values( $cities ) );
		set_transient( 'nadlan_ur_mapdata_v4', $out, 6 * HOUR_IN_SECONDS );
		return $out;
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/renewal-map-data', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function () {
			if ( ! nadlan_ur_map_on() ) { return array( 'cities' => array() ); }
			return nadlan_ur_map_cities();
		},
	) );
} );

/* server-rendered SEO layer for the map page: crawlable city directory with
   direct compound links, guide copy with internal links, FAQ + Dataset +
   ItemList schema. The interactive map is JS (invisible to crawlers) - THIS
   is what search engines read. Cached whole for 6h. */
if ( ! function_exists( 'nadlan_ur_map_seo_html' ) ) {
	function nadlan_ur_map_seo_html() {
		$hit = get_transient( 'nadlan_ur_mapseo_v6' ); // v4: the honest copy of HAD-396 (no "מוכרזים" on every compound, the real pull date)
		// the FAQ / Dataset / ItemList schema is cached with the copy: before, a cache hit returned early and the schema never printed
		$sch = get_transient( 'nadlan_ur_mapschema_v6' );
		if ( is_string( $hit ) && '' !== $hit && is_array( $sch ) ) { $GLOBALS['nadlan_ur_map_schemas'] = $sch; return $hit; }
		$data = nadlan_ur_map_cities();
		$cities = $data['cities'];
		usort( $cities, function ( $a, $b ) { return $b['count'] - $a['count']; } );
		$top = array_slice( $cities, 0, 12 );
		$total = (int) $data['total'];
		$cards = '';
		$schema_cities = array();
		foreach ( $top as $c ) {
			$q = new WP_Query( array(
				'post_type' => 'nadlan_project', 'post_status' => 'publish', 'posts_per_page' => 4,
				'no_found_rows' => true, 'meta_query' => array(
					array( 'key' => 'source', 'value' => 'urban_renewal' ),
					array( 'key' => 'city', 'value' => $c['city'] ),
				),
			) );
			$links = '';
			foreach ( $q->posts as $pp ) {
				$links .= '<li><a href="' . esc_url( get_permalink( $pp ) ) . '">' . esc_html( get_the_title( $pp ) ) . '</a></li>';
			}
			$more = max( 0, $c['count'] - count( $q->posts ) );
			$cards .= '<div class="nlurm-city"><h3>' . esc_html( $c['city'] ) . '</h3>'
				. '<p class="nlurm-cn">' . (int) $c['count'] . ' מתחמי פינוי בינוי במאגר'
				. ( $c['misui'] ? ' · מוכרזים במסלול מיסוי: ' . (int) $c['misui'] : '' )
				. ( $c['rashuyot'] ? ' · מוכרזים במסלול רשויות: ' . (int) $c['rashuyot'] : '' ) . '</p>'
				. ( $links ? '<ul>' . $links . '</ul>' : '' )
				. ( $more > 0 ? '<p class="nlurm-more">ועוד ' . $more . ' מתחמים בעיר (הקישו על העיר במפה לרשימה המלאה)</p>' : '' )
				. '</div>';
			$schema_cities[] = array( '@type' => 'ListItem', 'position' => count( $schema_cities ) + 1, 'name' => $c['city'] . ' - ' . $c['count'] . ' מתחמי פינוי בינוי' );
		}
		$home = home_url();
		// "מוכרז" belongs to the two declared tracks only (misui, rashuyot); the rest of the registry is not declared yet (HAD-396)
		$declared = 0;
		foreach ( $cities as $c ) { $declared += (int) $c['misui'] + (int) $c['rashuyot']; }
		$pulled = function_exists( 'nadlan_ur_source_pulled' ) ? nadlan_ur_source_pulled() : '13.7.2026';
		$copy = '<section class="nlurm-seo">'
			. '<h2>מתחמי התחדשות עירונית בישראל לפי עיר</h2>'
			. '<p>המפה מציגה <b>' . $total . ' מתחמי פינוי בינוי</b> מתוך מאגר המתחמים של הרשות הממשלתית להתחדשות עירונית (data.gov.il). מהם ' . $declared . ' מוכרזים, במסלול מיסוי או במסלול רשויות, והשאר מתחמים שטרם הוכרזו או שהמסלול שלהם לא צוין במאגר. לכל מתחם עמוד ייעודי עם מספר התכנית, המסלול והסטטוס. הנתונים נמשכו מהמאגר ב-' . esc_html( $pulled ) . '. המפה מרכזת אותם לפי עיר, והטבלאות מטה מציגות את כל המתחמים בקובץ הרשמי העדכני לפי שלב, מחוז ועיר, עם התאריך של כל מקור.</p>'
			. '<p>גרים בבניין שנמצא במתחם התחדשות? התחילו ב<a href="' . esc_url( $home . '/urban-renewal/' ) . '">מדריך ההתחדשות העירונית המלא</a>, בדקו את הבניין שלכם ב<a href="' . esc_url( $home . '/urban-renewal/check/' ) . '">בדיקת בניין חינמית</a>, או קראו על המסלולים: <a href="' . esc_url( $home . '/urban-renewal/pinui-binui/' ) . '">פינוי בינוי</a> ו<a href="' . esc_url( $home . '/urban-renewal/tama-38/' ) . '">תמא 38 והחלופות</a>. נציגות בניין יכולה לפתוח <a href="' . esc_url( $home . '/my-renewal/' ) . '">חדר פרויקט פרטי</a> לניהול ההסכמות והמסמכים.</p>'
			. '<div class="nlurm-cities">' . $cards . '</div>'
			. '</section>';
		$faq = array(
			'@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => array(
				array( '@type' => 'Question', 'name' => 'מה זה מתחם התחדשות עירונית מוכרז?',
					'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'מתחם שהוכרז רשמית במסלול מיסוי או במסלול רשויות. ההכרזה פותחת הטבות מס ותהליכי תכנון ייעודיים. במפה מופיעים גם מתחמים שטרם הוכרזו, וליד כל עיר כתוב כמה מתחמים בה מוכרזים בכל מסלול. מקור הנתונים: המאגר הרשמי ב-data.gov.il.' ) ),
				array( '@type' => 'Question', 'name' => 'איך בודקים אם הבניין שלי נמצא במתחם התחדשות?',
					'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'הקישו על העיר שלכם במפה לרשימת המתחמים בה, או השתמשו בבדיקת הבניין החינמית באתר, שמחפשת את העיר והרחוב במאגר.' ) ),
				array( '@type' => 'Question', 'name' => 'מה ההבדל בין פינוי בינוי לתמא 38?',
					'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'פינוי בינוי הוא הריסת מתחם שלם ובנייה חדשה, בדרך כלל ביוזמת הרשות או יזם ובהיקף גדול. תמא 38 (והחלופות שהחליפו אותה) היא חיזוק או הריסה ובנייה של בניין בודד. לכל מסלול רף הסכמות שונה של בעלי הדירות.' ) ),
			),
		);
		$dataset = array(
			'@context' => 'https://schema.org', '@type' => 'Dataset',
			'name' => 'מתחמי פינוי בינוי במאגר ההתחדשות העירונית בישראל',
			'description' => 'ריכוז מתחמי ההתחדשות העירונית בישראל לפי עיר ומסלול, מוכרזים ושטרם הוכרזו, מתוך המאגר הרשמי של הרשות הממשלתית להתחדשות עירונית, כפי שנמשך ב-' . $pulled . '.',
			'creator' => array( '@type' => 'Organization', 'name' => 'הרשות הממשלתית להתחדשות עירונית (data.gov.il)' ),
			'license' => 'https://data.gov.il/terms',
			'url' => home_url( '/urban-renewal/map/' ),
		);
		$list = array( '@context' => 'https://schema.org', '@type' => 'ItemList', 'name' => 'ערים מובילות בהתחדשות עירונית', 'itemListElement' => $schema_cities );
		if ( function_exists( 'nadlan_urd_faq_schema' ) ) { // 1.72.520: the 20 visible questions of the data block are the FAQPage
			$faq = nadlan_urd_faq_schema();
			$ud  = nadlan_urd();
			if ( ! empty( $ud['file']['last_modified'] ) ) { $dataset['dateModified'] = $ud['file']['last_modified']; $dataset['isBasedOn'] = $ud['file']['url']; }
		}
		$GLOBALS['nadlan_ur_map_schemas'] = array( $faq, $dataset, $list );
		set_transient( 'nadlan_ur_mapschema_v6', $GLOBALS['nadlan_ur_map_schemas'], 6 * HOUR_IN_SECONDS );
		$html = $copy
			. '<style>.nlurm-seo{margin-top:34px}.nlurm-seo h2{font-family:"Frank Ruhl Libre",Georgia,serif;font-size:clamp(1.25rem,2.6vw,1.6rem);margin:0 0 12px}.nlurm-seo>p{font:400 15px/1.75 Heebo,sans-serif;color:#3E382F;max-width:70ch}.nlurm-cities{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;margin-top:20px}.nlurm-city{background:#fff;border:1px solid #E2DCD0;border-radius:14px;padding:16px 18px}.nlurm-city h3{font:700 16px Heebo,sans-serif;margin:0 0 4px}.nlurm-cn{font:400 12.5px/1.6 Heebo,sans-serif;color:#6D665C;margin:0 0 8px}.nlurm-city ul{margin:0;padding:0 18px 0 0;font:400 13.5px/1.9 Heebo,sans-serif}.nlurm-city a{color:#9C7A3C}.nlurm-more{font:400 12px/1.5 Heebo,sans-serif;color:#A79E8D;margin:6px 0 0}</style>';
		set_transient( 'nadlan_ur_mapseo_v6', $html, 6 * HOUR_IN_SECONDS ); // the key read above (v4): main's code review, 3.10
		return $html;
	}
}

add_shortcode( 'nadlan_ur_map', function () {
	if ( ! nadlan_ur_map_on() ) { return ''; }
	$token = '';
	if ( function_exists( 'nadlan_cmpmap_token' ) ) { $token = nadlan_cmpmap_token(); }
	if ( ! $token && function_exists( 'nadlan_drone_token' ) ) { $token = nadlan_drone_token(); }
	if ( ! $token ) { $token = (string) get_option( 'nadlan_mapbox_token', '' ); }
	if ( '' === $token ) { return '<p>המפה תוצג לאחר הגדרת מפתח מפות.</p>'; }
	$rest = esc_url( rest_url( 'nadlan/v1/renewal-map-data' ) );
	$v2   = nadlan_ur_map_v2_boot(); // v2 labels: centroids + price medians as JSON, printed into the map script
	ob_start(); ?>
<div class="nlurm" dir="rtl">
	<div id="nlurm-map"></div>
	<p class="nlurm-note">התוויות במפה מראות לכל עיר את מתחמי ההתחדשות ושלביהם לפי מפת הרשות הממשלתית להתחדשות עירונית, ואת מחירי הדירות לפי עסקאות שדווחו לרשות המסים. בפרטי כל עיר כתובים המקור והתאריך של כל מספר. עמודי המתחמים באתר נבנו מהקובץ הרשמי (data.gov.il) כפי שנמשך ב-<?php echo esc_html( function_exists( 'nadlan_ur_source_pulled' ) ? nadlan_ur_source_pulled() : '13.7.2026' ); ?>. הקישו על עיר לפרטים ולרשימת המתחמים בה.</p>
	<div id="nlurm-list" aria-live="polite"></div>
	<?php
	echo nadlan_ur_map_seo_html(); // phpcs:ignore -- built from escaped parts
	if ( function_exists( 'nadlan_urd_html' ) ) { echo nadlan_urd_html(); } // phpcs:ignore -- 1.72.520 data block, escaped parts
	add_action( 'wp_footer', function () {
		foreach ( (array) ( $GLOBALS['nadlan_ur_map_schemas'] ?? array() ) as $sc ) {
			echo '<script type="application/ld+json">' . wp_json_encode( $sc, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n"; // phpcs:ignore
		}
	} );
	?>
</div>
<style>
/* renewal map v2 (proposal of 26.10.2026): survey tags that carry the facts, a city panel in step with the map, chips that re-label
   the map. Colours of the page's data block (.nlur2): ink #12202A, ink2 #3E4C58, sea #2F6F86, deep #1F4B5C, line #D3DCE2; red only
   for warnings. IBM Plex Sans Hebrew for words, IBM Plex Mono for numbers (the faces the page already loads). The site skin forces
   another face on span, button and p with !important, so the faces are pinned here with scoped !important rules. */
#nlurm-map{height:520px;border-radius:10px;overflow:hidden;border:1px solid #D3DCE2;background:#E9EEF1}
.nlurm-note{font:400 12.5px/1.6 "IBM Plex Sans Hebrew",Heebo,sans-serif;color:#3E4C58;margin:10px 0}
#nlurm-list .nlur-hit{background:#fff;border:1px solid #D3DCE2;border-radius:6px;padding:12px 14px;margin-top:8px;font:400 13.5px/1.6 "IBM Plex Sans Hebrew",Heebo,sans-serif;color:#12202A}
.nlurm-v2{--ink:#12202A;--ink2:#3E4C58;--sea:#2F6F86;--deep:#1F4B5C;--line:#D3DCE2;--wash:#EEF3F5;--red:#C42550;position:relative;display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:hidden;color:var(--ink);text-align:right}
.nlurm-v2 *{box-sizing:border-box}
html body .nlurm-v2 :is(div,span,button,p,a,b,i,small,input,select,option,label,li,ul,ol,h3,h4,strong,em,dl,dt,dd){font-family:"IBM Plex Sans Hebrew",system-ui,sans-serif!important;letter-spacing:0!important;text-transform:none!important}
html body .nlurm-v2 :is(.n,.n *){font-family:"IBM Plex Mono",ui-monospace,monospace!important;font-variant-numeric:tabular-nums}
html body .nlurm-v2 :focus-visible{outline:2px solid var(--deep)!important;outline-offset:2px!important;box-shadow:none!important}
.nlurm-v2 #nlurm-map{height:500px;border:0;border-radius:0;background:#E9EEF1}
.nlurm-v2.is-wide{display:grid;grid-template-columns:340px minmax(0,1fr);grid-template-rows:auto minmax(0,1fr);grid-template-areas:"bar map" "side map";height:600px}
.nlurm-v2.is-wide .nlurm-bar{grid-area:bar}
.nlurm-v2.is-wide .nlurm-side{grid-area:side;overflow:auto;border-top:0}
.nlurm-v2.is-wide #nlurm-map{grid-area:map;height:100%;border-inline-start:1px solid var(--line)}
/* the bar: search and the chips that choose what the tags say */
.nlurm-bar{position:relative;z-index:6;display:flex;flex-direction:column;gap:10px;padding:12px 12px 10px;background:#fff;border-bottom:1px solid var(--line)}
.nlurm-q{position:relative}
html body .nlurm-v2 .nlurm-q input{width:100%;height:44px;margin:0;border:1px solid #8C99A4!important;border-radius:4px!important;padding:0 40px 0 12px!important;background:#fff!important;color:var(--ink)!important;font-size:15px!important;font-weight:500!important;line-height:44px;box-shadow:none;-webkit-appearance:none;appearance:none}
.nlurm-q input::placeholder{color:#3E4C58;opacity:1}
.nlurm-q svg{position:absolute;right:12px;top:13px;width:18px;height:18px;stroke:var(--ink2);fill:none;stroke-width:2;pointer-events:none}
.nlurm-res{position:absolute;inset-inline:0;top:48px;max-height:340px;overflow:auto;background:#fff;border:1px solid var(--line);border-radius:4px;box-shadow:0 10px 28px rgba(18,32,42,.18);z-index:9}
html body .nlurm-v2 .nlurm-res button{display:block;width:100%;min-height:44px;margin:0;padding:8px 12px;border:0;border-bottom:1px solid var(--wash);background:#fff;color:var(--ink);text-align:right;cursor:pointer;font-size:14.5px!important;font-weight:600!important;line-height:1.35}
html body .nlurm-v2 .nlurm-res button small{display:block;color:var(--ink2);font-size:12.5px!important;font-weight:400!important}
.nlurm-res button:hover,.nlurm-res button:focus-visible{background:var(--wash)}
.nlurm-res p{margin:0;padding:12px;color:var(--ink2);font-size:13.5px}
.nlurm-chips{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;margin:0 -12px;padding:0 12px 2px}
.nlurm-chips::-webkit-scrollbar{display:none}
.nlurm-v2.is-wide .nlurm-bar .nlurm-chips{flex-wrap:wrap;overflow:visible;margin:0;padding:0}
html body .nlurm-v2:not(.is-touch) .nlurm-bar .nlurm-chip{min-height:36px;padding:0 11px}
html body .nlurm-v2 .nlurm-chip{flex:none;min-height:44px;margin:0;padding:0 13px;border:1px solid #8C99A4;border-radius:4px;background:#fff;color:var(--ink);cursor:pointer;font-size:14px!important;font-weight:500!important;line-height:1;white-space:nowrap}
html body .nlurm-v2 .nlurm-chip[aria-pressed="true"]{background:var(--deep);border-color:var(--deep);color:#fff;font-weight:600!important}
.nlurm-chip:hover{border-color:var(--deep)}
/* the tags: a zero-size anchor at the city point, a small dot, and the tag beside it (a survey tag: square corners, a stage strip) */
.nlurm-v2 .mapboxgl-canvas-container{isolation:isolate} /* the tags stack among themselves, under the map's buttons, the preview and the peek card */
.nlurm-lb{width:0;height:0;pointer-events:none}
.nlurm-lb .dt{position:absolute;left:-4px;top:-4px;width:8px;height:8px;border-radius:50%;background:var(--deep,#1F4B5C);box-shadow:0 0 0 1.5px #fff,0 1px 3px rgba(18,32,42,.35)}
.nlurm-lb .ld{position:absolute;left:0;top:0;display:none;height:1px;background:#3E4C58;transform-origin:0 50%}
.nlurm-lb .tg.is-c::after{display:none}
.nlurm-lb.is-hd .dt{display:none}
.nlurm-lb.is-zero .dt{background:#8C99A4;width:6px;height:6px;left:-3px;top:-3px}
html body .nlurm-v2 .nlurm-lb .tg{position:absolute;display:block;margin:0;padding:5px 8px 8px;background:#fff;border:1px solid rgba(18,32,42,.28);border-radius:3px;box-shadow:0 1px 3px rgba(18,32,42,.22);color:var(--ink);text-align:right;white-space:nowrap;cursor:pointer;pointer-events:auto;line-height:1;overflow:visible;-webkit-tap-highlight-color:transparent;transition:box-shadow .12s ease,border-color .12s ease}
html body .nlurm-v2 .nlurm-lb .tg .nm{display:block;color:var(--ink);font-size:14px!important;font-weight:600!important;line-height:18px}
html body .nlurm-v2 .nlurm-lb .tg .f{display:block;color:var(--ink2);font-size:12px!important;font-weight:500!important;line-height:16px}
html body .nlurm-v2 .nlurm-lb .tg .f b{color:var(--deep);font-size:12px!important;font-weight:500!important}
.nlurm-lb .tg .sb{position:absolute;left:0;right:0;bottom:0;height:4px;display:flex;overflow:hidden;border-radius:0 0 2px 2px;background:#D3DCE2}
.nlurm-lb .tg .sb i{display:block;height:100%}
.nlurm-lb .tg::after{content:"";position:absolute;width:7px;height:7px;background:#fff;border:solid rgba(18,32,42,.28);border-width:0 1px 1px 0;pointer-events:none}
.nlurm-lb .tg.is-n::after{left:calc(50% - 4px);bottom:-5px;transform:rotate(45deg)}
.nlurm-lb .tg.is-s::after{left:calc(50% - 4px);top:-5px;transform:rotate(-135deg)}
.nlurm-lb .tg.is-w::after{right:-5px;top:calc(50% - 4px);transform:rotate(-45deg)}
.nlurm-lb .tg.is-e::after{left:-5px;top:calc(50% - 4px);transform:rotate(135deg)}
.nlurm-lb .tg.is-n .sb,.nlurm-lb .tg.is-e .sb,.nlurm-lb .tg.is-w .sb{border-radius:0 0 2px 2px}
/* name only: no plate, a cartographer's white halo */
html body .nlurm-v2 .nlurm-lb .tg.tS{padding:2px 3px;background:none;border:0;box-shadow:none}
.nlurm-lb .tg.tS::after{display:none}
html body .nlurm-v2 .nlurm-lb .tg.tS .nm{font-size:13px!important;line-height:16px;text-shadow:0 0 1px #fff,0 0 2px #fff,0 0 3px #fff,0 0 4px #fff,1px 1px 2px #fff,-1px -1px 2px #fff,1px -1px 2px #fff,-1px 1px 2px #fff}
html body .nlurm-v2:not(.is-touch) .nlurm-lb .tg.tS{padding:4px 4px}
html body .nlurm-v2.is-touch .nlurm-lb .tg.tS{pointer-events:none} /* a phone opens a name through the map's own tap test (22 px around the point, or the name) */
html body .nlurm-v2.is-touch .nlurm-lb .tg:is(.tM,.tL){min-width:44px}
html body .nlurm-v2.is-touch .nlurm-lb .tg.tM{min-height:44px}
/* states */
.nlurm-lb .tg:hover,.nlurm-lb .tg.is-hi{border-color:var(--deep);box-shadow:0 0 0 1px var(--deep),0 4px 12px rgba(18,32,42,.25)}
html body .nlurm-v2 .nlurm-lb .tg.tS:hover .nm,html body .nlurm-v2 .nlurm-lb .tg.tS.is-hi .nm{text-decoration:underline;text-underline-offset:3px}
.nlurm-lb .tg:active{transform:translateY(1px)}
html body .nlurm-v2 .nlurm-lb .tg.is-on{background:var(--deep);border-color:var(--deep);box-shadow:0 0 0 2px #fff,0 4px 14px rgba(18,32,42,.35)}
html body .nlurm-v2 .nlurm-lb .tg.is-on .nm,html body .nlurm-v2 .nlurm-lb .tg.is-on .f,html body .nlurm-v2 .nlurm-lb .tg.is-on .f b{color:#fff;text-shadow:none}
.nlurm-lb .tg.is-on::after{background:var(--deep);border-color:var(--deep)}
.nlurm-lb .tg.is-on .sb{box-shadow:0 -1px 0 #fff}
/* hover preview (mouse) and the peek card (touch) */
.nlurm-pop{position:absolute;z-index:50;width:300px;max-width:calc(100% - 16px);padding:12px 14px 10px;background:#fff;border:1px solid rgba(18,32,42,.28);border-radius:4px;box-shadow:0 10px 28px rgba(18,32,42,.22);pointer-events:none}
.nlurm-peek{position:absolute;z-index:50;left:8px;right:8px;bottom:8px;padding:12px 14px 12px;background:#fff;border:1px solid rgba(18,32,42,.28);border-radius:6px;box-shadow:0 -2px 18px rgba(18,32,42,.2)}
html body .nlurm-v2 :is(.nlurm-pop,.nlurm-peek,.nlurm-side) .ct{display:block;color:var(--ink);font-size:17px!important;font-weight:600!important;line-height:22px;margin:0 0 2px}
html body .nlurm-v2 :is(.nlurm-pop,.nlurm-peek,.nlurm-side) .k{display:block;color:var(--ink2);font-size:13px!important;font-weight:400!important;line-height:19px}
html body .nlurm-v2 :is(.nlurm-pop,.nlurm-peek,.nlurm-side) .k b{color:var(--ink);font-weight:500!important}
.nlurm-big{display:flex;height:8px;margin:8px 0 4px;border-radius:1px;overflow:hidden;background:#D3DCE2}
.nlurm-big i{display:block;height:100%}
.nlurm-leg{display:flex;flex-wrap:wrap;gap:2px 10px;margin:0 0 6px}
html body .nlurm-v2 .nlurm-leg span{display:inline-flex;align-items:center;gap:5px;color:var(--ink2);font-size:12.5px!important;font-weight:400!important;line-height:18px}
.nlurm-leg span::before{content:"";width:9px;height:9px;border-radius:1px;background:var(--c)}
html body .nlurm-v2 .nlurm-leg span b{color:var(--ink);font-weight:500!important}
.nlurm-top3{margin:6px 0 0;padding:6px 0 0;border-top:1px solid var(--wash);list-style:none}
html body .nlurm-v2 .nlurm-top3 li{color:var(--ink);font-size:13px!important;font-weight:500!important;line-height:19px;margin:0;padding:0}
html body .nlurm-v2 .nlurm-top3 li small{color:var(--ink2);font-size:12px!important;font-weight:400!important}
html body .nlurm-v2 .nlurm-pop .hint{display:block;margin-top:6px;color:var(--ink2);font-size:12px!important}
.nlurm-acts{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
html body .nlurm-v2 .nlurm-acts :is(button,a){display:inline-flex;align-items:center;justify-content:center;min-height:44px;margin:0;padding:0 14px;border:1px solid var(--deep);border-radius:4px;background:#fff;color:var(--deep);text-decoration:none;cursor:pointer;font-size:14px!important;font-weight:600!important;line-height:1.2}
html body .nlurm-v2 .nlurm-acts :is(button,a).pri{background:var(--deep);color:#fff}
html body .nlurm-v2 .nlurm-x{position:absolute;top:2px;left:2px;width:44px;height:44px;margin:0;padding:0;border:0;background:none;color:var(--ink);font-size:24px!important;font-weight:400!important;line-height:44px;text-align:center;cursor:pointer}
/* the side panel (beside the map on a wide screen, under it on a phone) */
.nlurm-side{position:relative;padding:12px 14px 16px;background:#fff;border-top:1px solid var(--line)}
html body .nlurm-v2 .nlurm-side h3{margin:0 0 4px;color:var(--ink);font-size:15px!important;font-weight:600!important;line-height:22px}
html body .nlurm-v2 .nlurm-side .lede{margin:0 0 8px;color:var(--ink2);font-size:13px!important;line-height:19px}
.nlurm-rows{list-style:none;margin:0;padding:0}
html body .nlurm-v2 .nlurm-rows .ctr{position:relative;display:block;width:100%;min-height:52px;margin:0;padding:7px 4px 11px;border:0;border-bottom:1px solid var(--wash);background:none;color:var(--ink);text-align:right;cursor:pointer}
.nlurm-rows .ctr:hover,.nlurm-rows .ctr.is-hi{background:var(--wash)}
html body .nlurm-v2 .nlurm-rows .ctr .nm{display:block;font-size:14.5px!important;font-weight:600!important;line-height:20px;color:var(--ink)}
html body .nlurm-v2 .nlurm-rows .ctr .f{display:block;font-size:12.5px!important;font-weight:400!important;line-height:18px;color:var(--ink2)}
html body .nlurm-v2 .nlurm-rows .ctr .f b{color:var(--deep);font-weight:500!important}
.nlurm-rows .ctr .sb{position:absolute;right:4px;left:4px;bottom:5px;height:3px;display:flex;overflow:hidden;background:#D3DCE2}
.nlurm-rows .ctr .sb i{display:block;height:100%}
html body .nlurm-v2 .nlurm-more{display:block;width:100%;min-height:44px;margin:8px 0 0;padding:0 12px;border:1px solid #8C99A4;border-radius:4px;background:#fff;color:var(--ink);cursor:pointer;font-size:14px!important;font-weight:500!important}
html body .nlurm-v2 .nlurm-back{display:inline-flex;align-items:center;min-height:44px;margin:-6px 0 4px;padding:0 4px;border:0;background:none;color:var(--deep);cursor:pointer;font-size:14px!important;font-weight:600!important}
.nlurm-dl{margin:8px 0 0;padding:0}
.nlurm-dl>div{display:flex;justify-content:space-between;gap:10px;padding:6px 0;border-top:1px solid var(--wash)}
html body .nlurm-v2 .nlurm-dl dt{margin:0;color:var(--ink2);font-size:13px!important;font-weight:400!important;line-height:19px}
html body .nlurm-v2 .nlurm-dl dd{margin:0;color:var(--ink);font-size:13px!important;font-weight:500!important;line-height:19px;text-align:left;white-space:nowrap}
html body .nlurm-v2 .nlurm-dl dt small{display:block;color:var(--ink2);font-size:11.5px!important}
.nlurm-cxh{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:14px 0 6px}
html body .nlurm-v2 .nlurm-cxh select{height:44px;margin:0;padding:0 10px;border:1px solid #8C99A4;border-radius:4px;background:#fff;color:var(--ink);font-size:14px!important}
.nlurm-cxh .nlurm-chips{margin:0;padding:0;flex-wrap:wrap;overflow:visible}
html body .nlurm-v2 .nlurm-cxh .nlurm-chip{min-height:36px;padding:0 10px;font-size:13px!important}
html body .nlurm-v2.is-touch .nlurm-cxh .nlurm-chip{min-height:44px}
.nlurm-cx{list-style:none;margin:0;padding:0}
.nlurm-cx li{display:flex;align-items:stretch;gap:8px;border-bottom:1px solid var(--wash)}
.nlurm-cx .sq{flex:none;width:4px;margin:8px 0;border-radius:1px}
html body .nlurm-v2 .nlurm-cx .cxm{flex:1;display:block;min-height:44px;padding:7px 0;color:var(--ink);text-decoration:none}
html body .nlurm-v2 .nlurm-cx .cxm b{display:block;color:var(--ink);font-size:14px!important;font-weight:600!important;line-height:20px}
html body .nlurm-v2 .nlurm-cx a.cxm b{text-decoration:underline;text-decoration-color:#8C99A4;text-underline-offset:3px}
html body .nlurm-v2 .nlurm-cx .cxm span{display:block;color:var(--ink2);font-size:12.5px!important;font-weight:400!important;line-height:18px}
html body .nlurm-v2 .nlurm-cx li.is-hi{background:var(--wash)}
html body .nlurm-v2 .nlurm-cx .cxt{flex:none;align-self:center;min-height:44px;min-width:56px;margin:0;padding:0 10px;border:1px solid var(--line);border-radius:4px;background:#fff;color:var(--deep);cursor:pointer;font-size:13px!important;font-weight:600!important}
html body .nlurm-v2 .nlurm-src{margin:12px 0 0;color:var(--ink2);font-size:12px!important;line-height:18px}
html body .nlurm-v2 .nlurm-src a{color:var(--deep)}
.nlurm-msg{margin:8px 0;color:var(--ink2);font-size:13.5px}
.nlurm-sr{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.nlurm-home{display:block}
html body .nlurm-v2 .nlurm-home button{width:auto!important;padding:0 8px!important;font-size:12.5px!important;font-weight:600!important;color:var(--ink)!important;white-space:nowrap}
@media (prefers-reduced-motion:reduce){.nlurm-lb .tg{transition:none}}
</style>
<script>
/* renewal map v2 (proposal of 26.10.2026). Every city gets a tag that says something: its name and, where there is room, the facts
   the chips choose (complexes and approved plans, homes added, apartment prices, what moved), with a strip of its stages along the
   bottom. Tags never overlap: the most important cities get the richest tags, the rest a name or a dot until you zoom in. A mouse
   over a tag previews the city, a tap or click opens it in the panel beside the map (under it on a phone) with every number's
   source and date and the full list of its complexes, each with a link to its page and to "יומן המתחמים". Data: the tracker file
   the page already loads (stages, units, moves on the authority's map), the price medians the site already shows (value.json,
   printed by PHP), the city list of /renewal-map-data. Without the tracker file the map falls back to today's counts and today's
   list (renewal-lookup), with an honest message when its hourly limit answers. One finger still scrolls the page over the map. */
(function(){
	var host=document.getElementById("nlurm-map");if(!host||host.dataset.wired)return;host.dataset.wired="1";
	var BOOT=<?php echo $v2; // phpcs:ignore ?>||{};
	var REST="<?php echo $rest; // phpcs:ignore ?>",LOOK="<?php echo esc_url( rest_url( 'nadlan/v1/renewal-lookup' ) ); // phpcs:ignore ?>";
	var ST=["ללא שלב","תכנון ראשוני","תכנון סטטוטורי","תכנית מאושרת","במימוש","אחרי רישוי"],SC=["#D3DCE2","#9DB7C3","#5C93A8","#2F6F86","#1F4B5C","#12202A"];
	var KIND={"new":"נוסף","up":"עלה שלב","down":"ירד שלב","chg":"השלב השתנה","gone":"ירד מהרשימה","back":"חזר לרשימה","trk":"המסלול השתנה","renum":"מספר מתחם חדש"};
	var ORD={up:0,"new":1,down:2,chg:3,trk:4,renum:5,back:6,gone:7};
	var MODES=[["all","מתחמים"],["ap","תכניות מאושרות"],["un","דירות חדשות"],["px","מחירי דירות"],["mv","מה זז"]];
	var GUIDE={"תל אביב יפו":"/urban-renewal/pinui-binui-tel-aviv/"};
	var touch=!!(window.matchMedia&&matchMedia("(hover: none), (pointer: coarse)").matches);
	function fail(){
		// no WebGL / blocked script: never leave a black box - the crawlable city directory below carries the same data
		var box=(host.closest&&host.closest(".nlurm-v2"))||host;box.style.display="none";
		var n=document.createElement("p");n.className="nlurm-note";
		n.textContent="המפה לא נטענה בדפדפן הזה. רשימת הערים והמתחמים המלאה מוצגת מטה.";
		box.parentNode.insertBefore(n,box.nextSibling);
	}
	function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})}
	function fold(s){return String(s||"").replace(/־/g," ").replace(/[֑-ׇ]/g,"").replace(/[-‐-―,.;:!?"'׳״()\[\]\/\\+]/g," ").replace(/\s+/g," ").trim().replace(/יי/g,"י").replace(/וו/g,"ו")}
	function n0(x){return String(Math.round(x||0)).replace(/\B(?=(\d{3})+(?!\d))/g,",")}
	function mil(v,dg){var s=(v/1e6).toFixed(dg==null?2:dg);if(s.indexOf(".")>-1)s=s.replace(/0+$/,"").replace(/\.$/,"");return s}
	function dd(iso){var p=String(iso||"").split("-");return p.length===3?(+p[2])+"."+(+p[1])+"."+p[0]:String(iso||"")}
	function N(x){return '<b class="n">'+n0(x)+'</b>'}
	function Q(q){return '<bdi class="n">'+esc(q)+'</bdi>'} // a quarter like 1-3.2026 keeps its order inside a Hebrew line
	function pl(x,one,many){return N(x)+" "+(x===1?one:many)}
	function txt(h){var d=document.createElement("div");d.innerHTML=h;return d.textContent.replace(/\s+/g," ").trim()}
	function slug(s){return encodeURIComponent(s).replace(/%[0-9A-F]{2}/g,function(x){return x.toLowerCase()})}
	/* ---------- the layout around the map: bar (search + chips), map, side panel ---------- */
	var wrap=document.createElement("div");wrap.className="nlurm-v2"+(touch?" is-touch":"");wrap.setAttribute("dir","rtl");
	host.parentNode.insertBefore(wrap,host);
	var bar=document.createElement("div");bar.className="nlurm-bar";
	bar.innerHTML='<div class="nlurm-q"><label class="nlurm-sr" for="nlurm-qi">חיפוש עיר, מתחם או מספר תכנית</label><input id="nlurm-qi" type="search" autocomplete="off" enterkeyhint="search" placeholder="חפשו עיר, מתחם או מספר תכנית"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/></svg><div class="nlurm-res" hidden></div></div><div class="nlurm-chips" role="group" aria-label="מה התוויות במפה מציגות"></div>';
	wrap.appendChild(bar);wrap.appendChild(host);
	var side=document.createElement("div");side.className="nlurm-side";side.setAttribute("role","region");side.setAttribute("aria-label","הערים והמתחמים");wrap.appendChild(side);
	var live=document.createElement("p");live.className="nlurm-sr";live.setAttribute("aria-live","polite");wrap.appendChild(live);
	function isWide(){return wrap.classList.contains("is-wide")}
	function wide(){var w=wrap.clientWidth>=820;if(isWide()!==w){wrap.classList.toggle("is-wide",w);if(map){map.resize();if(CITY.length&&CITY[0].el)measure();if(S.sel)peek(w?null:S.sel)}}}
	wide();if(window.ResizeObserver){new ResizeObserver(function(){wide();soon()}).observe(wrap)}else{window.addEventListener("resize",function(){wide();soon()})}
	var map=null,D=null,LM=-1,MAPD="",CITY=[],BYF={},S={mode:"all",sel:null,hi:null,sort:"st",grp:"*",more:0,list:0},raf=0;
	/* ---------- data ---------- */
	function trackerUrl(){var t=document.querySelector('[data-nli="urtrack"]'),a=t&&t.getAttribute("data-nli-data");if(!a)return "";var u=a.split(",").filter(function(x){return x.indexOf("renewal-track")>-1})[0];return u||""}
	function getJSON(u){return u?fetch(u,{credentials:"omit",cache:"force-cache"}).then(function(r){if(!r.ok)throw 0;return r.json()}).catch(function(){return null}):Promise.resolve(null)}
	function build(md,T){
		var cent={},px={},k;for(k in(BOOT.cent||{}))cent[fold(k)]=BOOT.cent[k];for(k in(BOOT.px||{}))px[fold(k)]=BOOT.px[k];
		var C={},list=[];
		function get(name){var f=fold(name);if(!C[f]){C[f]={name:name,f:f,ll:cent[f]||null,n:0,off:0,st:[0,0,0,0,0,0],ap:0,im:0,e:0,p:0,un:0,add:0,up:0,gone:0,down:0,chg:0,renum:0,mv:0,last:null,px:px[f]||null,recs:[],c0:0};list.push(C[f])}return C[f]}
		((md&&md.cities)||[]).forEach(function(c){var x=get(c.city);x.c0=c.count;if(!x.ll&&c.lnglat)x.ll=c.lnglat});
		if(T&&T.recs&&T.snaps){
			for(var i=T.snaps.length-1;i>=0;i--){if(T.snaps[i].k==="map"){LM=i;break}}
			MAPD=LM>-1?T.snaps[LM].d:"";
			T.recs.forEach(function(r){
				var x=get(r.c),s=LM>-1?r.s[LM]:-1;x.recs.push(r);
				(r.ch||[]).forEach(function(c){if(!x.last||c[0]>x.last.c[0]||(c[0]===x.last.c[0]&&(ORD[c[1]]||9)<(ORD[x.last.c[1]]||9)))x.last={r:r,c:c}});
				if(s==null||s<0){x.off++;return}
				x.n++;x.st[s]++;if(s>=3)x.ap++;if(s>=4)x.im++;
				if(r.u===LM&&r.e&&r.p){x.e+=r.e;x.p+=r.p;x.un++} // homes today and after: only the authority map's own figures, one source and one date
			});
			var A=(T.agg&&T.agg.cities)||{};for(k in A){var y=get(k),a=A[k];y.add=a.add||0;y.up=a.up||0;y.gone=a.gone||0;y.down=a.down||0;y.chg=a.chg||0;y.renum=a.renum||0;y.mv=y.add+y.up+y.gone+y.down+y.chg+y.renum}
			D=T;
		}
		list=list.filter(function(x){return x.ll&&(D?x.n>0:x.c0>0)});
		list.forEach(function(x){BYF[x.f]=x});
		return list;
	}
	function cnt(x){return D?x.n:x.c0}
	function metric(x,m){m=m||S.mode;if(m==="ap")return x.ap;if(m==="un")return Math.max(0,x.p-x.e);if(m==="px")return x.px?cnt(x)+1:0;if(m==="mv")return x.mv;return cnt(x)}
	function rooms(x){var k=["r3","r4","r5"].filter(function(r){return x.px&&x.px[r]}),a=k.map(function(r){return x.px[r][0]});if(!k.length)return null;var lo=Math.min.apply(0,a),hi=Math.max.apply(0,a);
		return{rl:k.length>1?k[0].slice(1)+"-"+k[k.length-1].slice(1)+" חד׳":k[0].slice(1)+" חד׳",rg:lo===hi?mil(lo,1):mil(lo,1)+"-"+mil(hi,1)}}
	function moved(x,max){var p=[];if(x.add)p.push(pl(x.add,"נוסף","נוספו"));if(x.up)p.push(pl(x.up,"עלה שלב","עלו שלב"));if(x.down)p.push(pl(x.down,"ירד שלב","ירדו שלב"));if(x.chg)p.push(pl(x.chg,"שינה שלב","שינו שלב"));if(x.gone)p.push(pl(x.gone,"ירד מהרשימה","ירדו מהרשימה"));if(x.renum)p.push(pl(x.renum,"קיבל מספר חדש","קיבלו מספר חדש"));return max?p.slice(0,max):p}
	function lines(x,m){
		var c=cnt(x),r=rooms(x);m=m||S.mode;
		if(m==="ap")return[pl(x.ap,"תכנית מאושרת","תכניות מאושרות"),x.im?N(x.im)+" במימוש · מתוך "+pl(c,"מתחם","מתחמים"):"מתוך "+pl(c,"מתחם","מתחמים")];
		if(m==="un")return x.un?['<b class="n" dir="ltr">+'+n0(x.p-x.e)+'</b> דירות אחרי הבנייה',"היום "+N(x.e)+" ← "+N(x.p)]:["",""];
		if(m==="px")return r?['<b class="n">'+r.rg+'</b> מיליון ₪',r.rl+" · חציון עסקאות"]:["",""];
		if(m==="mv")return x.mv?[moved(x,2).join(" · "),x.last?esc(KIND[x.last.c[1]]||"")+": "+esc(x.last.r.n):""]:["",""];
		return[pl(c,"מתחם","מתחמים")+(D&&x.ap?" · "+pl(x.ap,"מאושרת","מאושרות"):""),r?r.rl+" · "+'<b class="n">'+r.rg+'</b> מיליון ₪':(x.un&&x.p>x.e?'<b class="n" dir="ltr">+'+n0(x.p-x.e)+'</b> דירות חדשות':"")];
	}
	function strip(x,cls){if(!D||!x.n)return "";var h="";[5,4,3,2,1,0].forEach(function(s){if(x.st[s])h+='<i style="flex:'+x.st[s]+' 0 0;background:'+SC[s]+'"></i>'});return'<span class="'+(cls||"sb")+'" aria-hidden="true">'+h+'</span>'}
	function short(x,l){var m=S.mode,c=cnt(x);if(m==="all")return pl(c,"מתחם","מתחמים");if(m==="un"&&x.un)return'<b class="n" dir="ltr">+'+n0(x.p-x.e)+'</b> דירות';if(m==="mv"&&x.mv)return moved(x,1)[0];if(m==="ap")return pl(x.ap,"מאושרת","מאושרות");return l[0]}
	function tagHTML(x){var l=lines(x),nm='<span class="nm">'+esc(x.name)+'</span>',sb=strip(x),o={S:nm},m1=isWide()?l[0]:(l[0]?short(x,l):"");
		o.M=m1?nm+'<span class="f">'+m1+'</span>'+sb:null;o.L=l[0]&&l[1]?nm+'<span class="f">'+l[0]+'</span><span class="f">'+l[1]+'</span>'+sb:null;
		o.aria=x.name+(l[0]?": "+txt(l[0])+(l[1]?", "+txt(l[1]):""):"")+". פתיחת פרטי העיר";return o}
	/* ---------- the tags on the map ---------- */
	function makeTags(){
		CITY.forEach(function(x){
			var el=document.createElement("div");el.className="nlurm-lb";
			el.innerHTML='<i class="ld"></i><span class="dt"></span><button type="button" class="tg" style="display:none"></button>';
			x.el=el;x.btn=el.lastChild;x.ld=el.firstChild;
			x.btn.addEventListener("click",function(e){e.stopPropagation();select(x,{from:"tag"})});
			if(!touch){x.btn.addEventListener("mouseenter",function(){S.hov=x;hiRow(x,1);pop(x)});x.btn.addEventListener("mouseleave",function(){S.hov=null;hiRow(x,0);pop(null)})}
			x.btn.addEventListener("focus",function(){if(!touch)pop(x)});x.btn.addEventListener("blur",function(){pop(null)});
			x.mk=new mapboxgl.Marker({element:el,anchor:"center"}).setLngLat(x.ll).addTo(map);
		});
		measure();
	}
	function measure(){
		var box=document.createElement("div");box.className="nlurm-lb";box.style.cssText="position:absolute;left:-9999px;top:0;visibility:hidden";host.appendChild(box);
		var probes=[];
		CITY.forEach(function(x){x.html=tagHTML(x);x.sz={};["L","M","S"].forEach(function(t){if(!x.html[t])return;var b=document.createElement("button");b.type="button";b.className="tg t"+t+" is-n";b.innerHTML=x.html[t];box.appendChild(b);probes.push([x,t,b])})});
		probes.forEach(function(p){var r=p[2].getBoundingClientRect();p[0].sz[p[1]]=[Math.ceil(r.width),Math.ceil(r.height)]});
		host.removeChild(box);
		CITY.forEach(function(x){x.el._k="";x.btn.setAttribute("aria-label",x.html.aria)});
	}
	function hit(a,b){return a[0]<b[2]&&a[2]>b[0]&&a[1]<b[3]&&a[3]>b[1]}
	/* the sea as the margin: every dense renewal city is on the coast, so a tag that has no room by its city may float over the sea
	   to the west, joined to the city by a thin line. The coastline here is coarse on purpose (the bay of Haifa counts as land). */
	var COAST=[[33.30,35.19],[33.10,35.105],[33.00,35.087],[32.92,35.068],[32.83,34.955],[32.70,34.938],[32.61,34.915],[32.50,34.888],[32.45,34.872],[32.33,34.848],[32.17,34.800],[32.10,34.770],[32.05,34.748],[32.00,34.733],[31.93,34.692],[31.80,34.630],[31.67,34.548],[31.59,34.490],[31.50,34.420],[31.32,34.220]];
	function coast(lat){for(var i=1;i<COAST.length;i++){var a=COAST[i-1],b=COAST[i];if(lat<=a[0]&&lat>=b[0])return b[1]+(a[1]-b[1])*(lat-b[0])/(a[0]-b[0])}return null}
	var seaRow={};  // per layout: the screen x of the coastline for each 4 px row (one unproject per row, not per corner)
	function sea(px,py){var k=Math.round(py/4),cx=seaRow[k];if(cx===undefined){var lat=map.unproject([0,k*4]).lat,c=coast(lat);cx=seaRow[k]=c===null?-1e9:map.project([c-0.008,lat]).x}return px<cx}
	var COFF=[];[26,44,64,86,110,136,164,196].forEach(function(d){[0,-22,22,-44,44,-66,66,-92,92,-120,120].forEach(function(dy){COFF.push([d,dy,d+1.4*Math.abs(dy)])})});COFF.sort(function(a,b){return a[2]-b[2]});
	function cands(x,t){
		var w=x.sz[t][0],h=x.sz[t][1],X=x.qx,Y=x.qy,g=t==="S"?7:11;
		function mk(sd,l,tp,ld){var b=[X+l,Y+tp,X+l+w,Y+tp+h];if(t!=="S"&&sd!=="c"){if(sd==="n")b[3]+=6;else if(sd==="s")b[1]-=6;else if(sd==="w")b[2]+=6;else b[0]-=6}return{sd:sd,l:l,t:tp,ld:ld||null,bx:b}} // the box keeps the tick: no tag covers another tag's pointer
		var n=mk("n",-w/2,-g-h),s=mk("s",-w/2,g),W=mk("w",-g-w,-h/2),E=mk("e",g,-h/2),o=t==="S"?[W,E,n,s]:[n,s,W,E];
		if(t!=="S"&&x.coastal)COFF.forEach(function(q){var d=q[0],dy=q[1];o.push(mk("c",-d-w,dy-h/2,[-d,Math.max(dy-h/2+6,Math.min(dy+h/2-6,0))]))});
		return o;
	}
	var lastLay=0,lastZ=0,zt=0,geo=null;
	/* the map's size and the boxes of its buttons and of the peek card, read once and kept until a resize or the peek changes:
	   reading them on every placement would force the browser to lay the whole page out again while the map zooms */
	function geom(){if(geo)return geo;var cr=host.getBoundingClientRect(),pad=4,block=[];
		[].forEach.call(host.querySelectorAll(".mapboxgl-ctrl-top-right .mapboxgl-ctrl,.mapboxgl-ctrl-top-left .mapboxgl-ctrl,.mapboxgl-ctrl-bottom-left .mapboxgl-ctrl,.mapboxgl-ctrl-bottom-right .mapboxgl-ctrl,.nlurm-peek"),function(c){if(c.hidden||c.style.display==="none")return;var b=c.getBoundingClientRect();if(b.width&&b.height)block.push([b.left-cr.left-pad,b.top-cr.top-pad,b.right-cr.left+pad,b.bottom-cr.top+pad])});
		return(geo={W:host.clientWidth,H:host.clientHeight,block:block})}
	function soon(){if(!raf&&map)raf=requestAnimationFrame(layout)}
	/* while zooming in, points only move apart, so the placement stays valid and is redone when the zoom ends; while zooming out,
	   at most one placement every 110 ms keeps tags from meeting (the markers themselves move every frame either way) */
	var quick=false;
	function soonZoom(){if(map.getZoom()>=lastZ-0.001)return;quick=true;var d=performance.now()-lastLay;if(d>=110)soon();else if(!zt)zt=setTimeout(function(){zt=0;soon()},110-d)}
	function layout(){
		raf=0;if(!CITY.length||!map)return;lastLay=performance.now();lastZ=map.getZoom();seaRow={};
		var G=geom(),W=G.W,H=G.H,pad=4,placed=[],block=G.block,isQuick=quick&&map.isZooming();quick=false;
		var order=CITY.slice().sort(function(a,b){return(metric(b)-metric(a))||(cnt(b)-cnt(a))});
		if(isQuick){  // zooming out: each tag keeps its place beside its point, a tag that now meets a more important one hides; the full placement follows when the zoom ends
			var qb=[];order.forEach(function(x){var q=map.project(x.ll);x.qx=q.x;x.qy=q.y;x.vis=q.x>-60&&q.y>-60&&q.x<W+60&&q.y<H+60;if(!x.t||!x.cd||!x.vis){x.t=null;return}
				var sz=x.sz[x.t],bx=[x.qx+x.cd.l,x.qy+x.cd.t,x.qx+x.cd.l+sz[0],x.qy+x.cd.t+sz[1]];
				if(qb.some(function(b){return hit(bx,b)})){x.t=null;return}qb.push(bx)});
			CITY.forEach(paint);return;
		}
		order.forEach(function(x,i){var q=map.project(x.ll),c=coast(x.ll[1]);x.qx=q.x;x.qy=q.y;x.vis=q.x>-60&&q.y>-60&&q.x<W+60&&q.y<H+60;x.t=null;x.cd=null;x.pi=-1;x.rank=i;x.coastal=c!==null&&x.ll[0]-c<0.3});
		var lines=[];  // the leader lines of sea tags, by the same index as placed: a later tag may not cover an earlier line
		function segIn(s,bx){if(Math.max(s[0],s[2])<bx[0]-4||Math.min(s[0],s[2])>bx[2]+4||Math.max(s[1],s[3])<bx[1]-4||Math.min(s[1],s[3])>bx[3]+4)return false;var L=Math.hypot(s[2]-s[0],s[3]-s[1]),k,px,py;for(k=5;k<L-1;k+=2){px=s[0]+(s[2]-s[0])*k/L;py=s[1]+(s[3]-s[1])*k/L;if(px>bx[0]-4&&px<bx[2]+4&&py>bx[1]-4&&py<bx[3]+4)return true}return false}
		var guard=0,dots=order.filter(function(x){return x.vis&&metric(x)>0});  // a tag never hides the point of a more important city (the chosen one: of the top 20)
		function fits(bx,skip,me){if(bx[0]<pad||bx[1]<pad||bx[2]>W-pad||bx[3]>H-pad)return false;var i;for(i=0;i<block.length;i++)if(hit(bx,block[i]))return false;for(i=0;i<placed.length;i++){if(i===skip)continue;if(placed[i]&&hit(bx,placed[i]))return false;if(lines[i]&&segIn(lines[i],bx))return false}
			if(me){var lim=guard?20:me.rank;for(i=0;i<dots.length&&dots[i].rank<lim;i++){var d=dots[i];if(d!==me&&d.qx>bx[0]-4&&d.qx<bx[2]+4&&d.qy>bx[1]-4&&d.qy<bx[3]+4)return false}}return true}
		function cross(a,b){function o(p,q,r){return(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])}var p1=[a[0],a[1]],p2=[a[2],a[3]],q1=[b[0],b[1]],q2=[b[2],b[3]];return o(p1,p2,q1)*o(p1,p2,q2)<0&&o(q1,q2,p1)*o(q1,q2,p2)<0}
		function lineFree(x,c,skip){if(Math.hypot(c.ld[0],c.ld[1])>170)return false;var me=[x.qx,x.qy,x.qx+c.ld[0],x.qy+c.ld[1]];for(var j=0;j<lines.length;j++){if(j!==skip&&lines[j]&&cross(me,lines[j]))return false}return lineFree0(x,c,skip)}
		function lineFree0(x,c,skip){var x2=x.qx+c.ld[0],y2=x.qy+c.ld[1],L=Math.hypot(x2-x.qx,y2-x.qy),k,i,px,py;for(k=5;k<L-2;k+=2){px=x.qx+(x2-x.qx)*k/L;py=x.qy+(y2-x.qy)*k/L;for(i=0;i<placed.length;i++){var b=placed[i];if(i!==skip&&b&&px>b[0]-4&&px<b[2]+4&&py>b[1]-4&&py<b[3]+4)return false}}return true}
		function seaBox(bx){return sea(bx[0],bx[1])&&sea(bx[2],bx[1])&&sea(bx[0],bx[3])&&sea(bx[2],bx[3])}
		function put(x,t,c){if(x.pi<0){x.pi=placed.length;placed.push(null);tagged.push(x)}placed[x.pi]=c.bx;lines[x.pi]=c.ld?[x.qx,x.qy,x.qx+c.ld[0],x.qy+c.ld[1]]:null;x.t=t;x.cd=c;return true}
		/* one tag, one point: a tag never sits nearer to another tagged city's point than to its own, and its own point is never
		   crowded by another tag; the bare point of a city without a tag that sits right against a tag steps aside at this zoom */
		var tagged=[];
		function dist(d,bx){var dx=Math.max(bx[0]-d.qx,0,d.qx-bx[2]),dy=Math.max(bx[1]-d.qy,0,d.qy-bx[3]);return Math.sqrt(dx*dx+dy*dy)}
		function near(bx,me,g){for(var i=0;i<tagged.length;i++){var d=tagged[i];if(d!==me&&dist(d,bx)<g-1)return true}
			for(i=0;i<order.length&&order[i].rank<16;i++){var q=order[i];if(q!==me&&q.vis&&!q.t&&Math.hypot(q.qx-me.qx,q.qy-me.qy)>=9&&dist(q,bx)<g-1)return true} /* nor nearer to an important city's point that is still bare */
			for(i=0;i<placed.length;i++){if(i!==me.pi&&placed[i]&&dist(me,placed[i])<10)return true}return false}
		// leave room: among the places that fit, a tag takes the one that crowds the fewest points of the next important cities still
		// waiting for a tag (a city sitting on top of this one does not count: it can never have its own tag here)
		function crowd(bx,me){var n=0;for(var i=0;i<order.length&&order[i].rank<16;i++){var d=order[i];if(d.rank>me.rank&&!d.t&&d.vis&&metric(d)>0&&Math.hypot(d.qx-me.qx,d.qy-me.qy)>=24&&dist(d,bx)<16)n+=16-d.rank}return n}
		function tryT(x,t,force){if(!x.sz[t])return false;var c=cands(x,t),g=t==="S"?7:11,best=null,bp=1e9,i,pn;
			for(i=0;i<c.length;i++){if(fits(c[i].bx,x.pi,x)&&!near(c[i].bx,x,g)&&(c[i].sd!=="c"||(seaBox(c[i].bx)&&lineFree(x,c[i],x.pi)))){pn=crowd(c[i].bx,x);if(pn<bp){bp=pn;best=c[i];if(!pn)break}}}
			if(best)return put(x,t,best);
			return force?put(x,t,c[0]):false}
		var lead=order.filter(function(x){return x===S.sel||x===S.hi}),rest=order.filter(function(x){return x!==S.sel&&x!==S.hi});
		lead.forEach(function(x){if(!x.vis)return;guard=1;var ok=tryT(x,"L")||tryT(x,"M");guard=0;ok||tryT(x,"L")||tryT(x,"M")||tryT(x,x.sz.M?"M":"S",true)});
		rest.forEach(function(x){if(x.vis&&metric(x)>0)tryT(x,"M")});                        // 1. a named tag with one fact for as many cities as fit
		rest.forEach(function(x){if(x.t==="M"){var keep=placed[x.pi],kl=lines[x.pi],kc=x.cd;placed[x.pi]=null;lines[x.pi]=null;if(!tryT(x,"L")){placed[x.pi]=keep;lines[x.pi]=kl;x.t="M";x.cd=kc}}}); // 2. a second fact where there is room
		rest.forEach(function(x){if(x.vis&&!x.t&&(metric(x)>0||S.mode==="all"))tryT(x,"S")});  // 3. the name alone
		order.forEach(function(x){x.hd=false;if(!x.vis||x.t)return;for(var j=0;j<tagged.length;j++){if(Math.hypot(tagged[j].qx-x.qx,tagged[j].qy-x.qy)<9){x.hd=true;return}}if(x.rank<16)return;for(var i=0;i<placed.length;i++){if(placed[i]&&dist(x,placed[i])<12){x.hd=true;break}}}); // 4. bare points against a tag wait for the zoom
		CITY.forEach(paint);
		clearTimeout(layout.dt);layout.dt=setTimeout(dedupe,250);
	}
	function paint(x){
		var b=x.btn,t=x.vis?x.t:null,c=x.cd,on=x===S.sel,hi=x===S.hi,key=t?t+c.sd+Math.round(c.l)+","+Math.round(c.t)+S.mode+on+hi:"-";
		var zi=String(on?3000:hi?2990:t?(t==="S"?1200:2000)+Math.max(0,700-x.rank):Math.max(0,700-x.rank));if(x.el._z!==zi){x.el._z=zi;x.el.style.zIndex=zi}
		x.el.classList.toggle("is-zero",!metric(x)&&!on);x.el.classList.toggle("is-hd",!!x.hd&&!t);
		if(x.el._k===key)return;x.el._k=key;
		if(!t){b.style.display="none";x.ld.style.display="none";return}
		var sz=x.sz[t];
		b.className="tg t"+t+" is-"+c.sd+(on?" is-on":"")+(hi?" is-hi":"");b.innerHTML=x.html[t];
		b.style.cssText="display:block;left:"+Math.round(c.l)+"px;top:"+Math.round(c.t)+"px;width:"+sz[0]+"px;height:"+sz[1]+"px";
		b.setAttribute("aria-pressed",on?"true":"false");
		if(c.ld){var L=Math.hypot(c.ld[0],c.ld[1]);x.ld.style.cssText="display:block;width:"+L.toFixed(1)+"px;transform:rotate("+Math.atan2(c.ld[1],c.ld[0]).toFixed(4)+"rad)"}else x.ld.style.display="none";
	}
	/* one name per place: the base map's own label for a city that has a tag here steps aside (checked when the map rests) */
	var baseF={},hidden="";
	function dedupe(){
		if(!map||!map.isStyleLoaded())return;
		if(map.isMoving()){clearTimeout(layout.dt);layout.dt=setTimeout(dedupe,300);return} // a base-map restyle waits until the map rests
		try{
			if(!dedupe.m){dedupe.m=1;["country-label","state-label","settlement-major-label","settlement-minor-label","settlement-subdivision-label"].forEach(function(id){if(map.getLayer(id)&&map.getPaintProperty(id,"text-opacity")==null)map.setPaintProperty(id,"text-opacity",.6)})}
			var own={};CITY.forEach(function(x){if(x.vis&&x.t)own[x.f]=1});
			var names=[];map.querySourceFeatures("composite",{sourceLayer:"place_label"}).forEach(function(f){var p=f.properties||{};[p.name,p.name_he,p["name_he"]].forEach(function(n){if(n&&own[fold(n)]&&names.indexOf(n)<0)names.push(n)})});
			var key=names.sort().join("|");if(key===hidden)return;hidden=key;
			var flt=names.length?["!",["any",["in",["coalesce",["get","name"],""],["literal",names]],["in",["coalesce",["get","name_he"],""],["literal",names]]]]:null;
			["settlement-major-label","settlement-minor-label","settlement-subdivision-label"].forEach(function(id){if(!map.getLayer(id))return;if(!(id in baseF))baseF[id]=map.getFilter(id)||null;var f0=baseF[id];map.setFilter(id,flt?(f0?["all",f0,flt]:flt):f0)});
		}catch(e){}
	}
	/* ---------- preview (mouse) and peek (touch) ---------- */
	var popEl=null,peekEl=null;
	function top3(x){return x.recs.filter(function(r){return LM>-1&&r.s[LM]>=0}).sort(function(a,b){return(b.s[LM]-a.s[LM])||((b.p||0)-(a.p||0))}).slice(0,3)}
	function legend(x){if(!D||!x.n)return "";var h="";[4,3,2,1,0,5].forEach(function(s){if(x.st[s])h+='<span style="--c:'+SC[s]+'">'+esc(s===3?"מאושרת":ST[s])+' <b class="n">'+x.st[s]+'</b></span>'});return'<div class="nlurm-big" aria-hidden="true">'+strip(x,"x").replace(/^<span class="x" aria-hidden="true">|<\/span>$/g,"")+'</div><div class="nlurm-leg">'+h+'</div>'}
	function summary(x){
		var r=rooms(x),h='<span class="ct">'+esc(x.name)+'</span>';
		h+=D?'<span class="k">'+pl(x.n,"מתחם","מתחמים")+' במפת הרשות, '+esc(dd(MAPD))+'</span>':'<span class="k">'+pl(x.c0,"מתחם","מתחמים")+' במאגר, '+esc(BOOT.pulled||"")+'</span>';
		h+=legend(x);
		if(x.un)h+='<span class="k">דירות: היום '+N(x.e)+' ← אחרי הבנייה '+N(x.p)+'</span>';
		if(r)h+='<span class="k">'+r.rl+': חציון עסקאות <b class="n">'+r.rg+'</b> מיליון ₪, רבעון '+Q(x.px.r4?x.px.r4[1]:x.px[Object.keys(x.px).filter(function(k){return k[0]==="r"})[0]][1])+'</span>';
		if(D&&x.mv)h+='<span class="k">מאז '+esc(dd(D.agg.since))+': '+moved(x).join(", ")+'</span>';
		return h;
	}
	function pop(x){
		if(!x||touch){if(popEl)popEl.style.display="none";return}
		if(!popEl){popEl=document.createElement("div");popEl.className="nlurm-pop";popEl.setAttribute("aria-hidden","true");host.appendChild(popEl)}
		var t3=top3(x);
		popEl.innerHTML=summary(x)+(t3.length?'<ul class="nlurm-top3">'+t3.map(function(r){return'<li>'+esc(r.n)+' <small>· '+esc(ST[r.s[LM]]||"")+(r.p?' · '+n0(r.p)+' דירות אחרי הבנייה':'')+'</small></li>'}).join("")+'</ul>':"")+'<span class="hint">לחיצה פותחת את העיר ואת רשימת המתחמים שלה</span>';
		popEl.style.display="block";
		var W=host.clientWidth,H=host.clientHeight,pw=popEl.offsetWidth,ph=popEl.offsetHeight,b=x.btn.getBoundingClientRect(),cr=host.getBoundingClientRect();
		var bx=[b.left-cr.left,b.top-cr.top,b.right-cr.left,b.bottom-cr.top],left=(bx[0]+bx[2])/2-pw/2,top=bx[1]-ph-8;
		if(top<8)top=bx[3]+8;if(top+ph>H-8){top=Math.max(8,(bx[1]+bx[3])/2-ph/2);left=bx[0]-pw-10<8?bx[2]+10:bx[0]-pw-10}
		popEl.style.left=Math.round(Math.max(8,Math.min(W-pw-8,left)))+"px";popEl.style.top=Math.round(Math.max(8,Math.min(H-ph-8,top)))+"px";
	}
	function peek(x){
		if(!x||isWide()){if(peekEl&&peekEl.style.display!=="none"){peekEl.style.display="none";geo=null;soon()}return}
		if(!peekEl){peekEl=document.createElement("div");peekEl.className="nlurm-peek";peekEl.setAttribute("role","dialog");host.appendChild(peekEl)}
		var l=lines(x,"all"),acts='<div class="nlurm-acts"><button type="button" class="pri go-list">המתחמים בעיר</button>'+(document.querySelector('#nlur2-track select[id$="-city"]')?'<button type="button" class="go-trk">יומן המתחמים</button>':'')+'</div>';
		peekEl.setAttribute("aria-label",x.name);
		peekEl.innerHTML='<button type="button" class="nlurm-x" aria-label="סגירה">×</button><span class="ct">'+esc(x.name)+'</span><span class="k">'+l[0]+'</span>'+(l[1]?'<span class="k">'+l[1]+'</span>':'')+(D&&x.n?'<div class="nlurm-big" aria-hidden="true">'+strip(x,"x").replace(/^<span class="x" aria-hidden="true">|<\/span>$/g,"")+'</div>':'')+acts;
		peekEl.style.display="block";geo=null;
		peekEl.querySelector(".nlurm-x").addEventListener("click",function(){select(null)});
		peekEl.querySelector(".go-list").addEventListener("click",function(){to(side,90)});
		var gt=peekEl.querySelector(".go-trk");if(gt)gt.addEventListener("click",function(){toTracker(x.name)});
		soon();
	}
	/* ---------- the side panel ---------- */
	function to(el,padTop){window.scrollTo({top:el.getBoundingClientRect().top+window.pageYOffset-padTop,behavior:"smooth"})} // clear of the sticky site header
	function toTracker(city,cx){
		var box=document.getElementById("nlur2-track");if(!box)return false;
		var seg=[].filter.call(box.querySelectorAll(".nli__seg button"),function(b){return b.textContent.trim()==="מתחם אחד"})[0];
		if(cx&&seg&&seg.getAttribute("aria-pressed")!=="true")seg.click();
		var sel=box.querySelector('select[id$="-city"]');if(!sel)return false;
		var f=fold(city),o=[].filter.call(sel.options,function(q){return fold(q.value)===f})[0];
		if(o&&sel.value!==o.value){sel.value=o.value;sel.dispatchEvent(new Event("change",{bubbles:true}))}
		if(cx){var s2=box.querySelector('select[id$="-cx"]');if(s2&&[].some.call(s2.options,function(q){return q.value===cx})){s2.value=cx;s2.dispatchEvent(new Event("change",{bubbles:true}))}}
		to(sel,140);return true;
	}
	function inView(){if(!map)return CITY;var b=map.getBounds();return CITY.filter(function(x){return b.contains(x.ll)})}
	function rowHTML(x){var l=lines(x);return'<li><button type="button" class="ctr" data-f="'+esc(x.f)+'"><span class="nm">'+esc(x.name)+'</span><span class="f">'+(l[0]||lines(x,"all")[0])+'</span>'+strip(x)+'</button></li>'}
	function listView(){
		var v=inView().sort(function(a,b){return(metric(b)-metric(a))||(cnt(b)-cnt(a))}),all=v.length===CITY.length,max=touch&&!S.list?8:999;
		var tot=0;CITY.forEach(function(x){tot+=cnt(x)});
		var h='<h3>'+(all?"כל הערים במפה":"ערים בתצוגה: "+v.length+" מתוך "+CITY.length)+'</h3>';
		h+='<p class="lede">'+(D?pl(tot,"מתחם","מתחמים")+" ב-"+N(CITY.length)+" ערים במפת הרשות הממשלתית להתחדשות עירונית, "+esc(dd(MAPD))+". ":"")+(all?"התקרבו במפה כדי לצמצם את הרשימה לאזור.":"הרשימה מתעדכנת כשמזיזים את המפה.")+'</p>';
		if(D)h+='<div class="nlurm-leg" aria-label="פס השלבים בתחתית כל תווית">'+[4,3,2,1,0].map(function(s){return'<span style="--c:'+SC[s]+'">'+esc(s===3?"מאושרת":ST[s])+'</span>'}).join("")+'</div>';
		h+=v.length?'<ul class="nlurm-rows">'+v.slice(0,max).map(rowHTML).join("")+'</ul>':'<p class="nlurm-msg">אין ערים עם מתחמים באזור הזה. הזיזו את המפה או לחצו על כל הארץ.</p>';
		if(v.length>max)h+='<button type="button" class="nlurm-more" data-a="list">כל '+v.length+' הערים בתצוגה</button>';
		h+=srcLine();
		side.innerHTML=h;
	}
	function srcLine(){var s=[];if(D)s.push('<a href="https://www.gov.il/he/departments/topics/mapa-renewal" target="_blank" rel="noopener">מפת הרשות הממשלתית להתחדשות עירונית</a> ('+esc(dd(MAPD))+')','<a href="https://data.gov.il/dataset/urban_renewal" target="_blank" rel="noopener">קובץ המתחמים ב-data.gov.il</a> ('+esc(dd(D.agg.since))+')');
		if(BOOT.pxsrc&&BOOT.pxsrc.source)s.push('<a href="'+esc(BOOT.pxsrc.url||"https://www.nadlan.gov.il/")+'" target="_blank" rel="noopener">רשות המסים, אתר נדל״ן הממשלתי</a> (קובץ '+esc(BOOT.pxsrc.file||"")+')');
		return s.length?'<p class="nlurm-src">מקורות: '+s.join(" · ")+'</p>':""}
	function cxRows(x){
		var R=x.recs.slice(),lm=LM;
		var g=S.grp;R=R.filter(function(r){var s=lm>-1?r.s[lm]:-1;return g==="*"||(g==="ap"&&s>=3)||(g==="pl"&&(s===1||s===2))||(g==="no"&&s===0)||(g==="off"&&s<0)});
		var sc=function(r){return lm>-1?r.s[lm]:-1},lc=function(r){var c=r.ch&&r.ch[r.ch.length-1];return c?c[0]:""};
		R.sort(S.sort==="un"?function(a,b){return((b.p||0)-(b.e||0))-((a.p||0)-(a.e||0))||a.n.localeCompare(b.n,"he")}:S.sort==="nm"?function(a,b){return a.n.localeCompare(b.n,"he")}:S.sort==="ch"?function(a,b){return lc(b)<lc(a)?-1:lc(b)>lc(a)?1:a.n.localeCompare(b.n,"he")}:function(a,b){return(sc(b)-sc(a))||((b.p||0)-(a.p||0))||a.n.localeCompare(b.n,"he")});
		return R;
	}
	function cityView(x,focusKey){
		var r=rooms(x),h='<button type="button" class="nlurm-back" data-a="back">→ כל הערים</button>';
		h+='<span class="ct" tabindex="-1">'+esc(x.name)+'</span>';
		h+=D?'<span class="k">'+pl(x.n,"מתחם","מתחמים")+' במפת הרשות, '+esc(dd(MAPD))+(x.off?' · ועוד '+N(x.off)+' שלא מופיעים בה היום':'')+'</span>':'<span class="k">'+pl(x.c0,"מתחם","מתחמים")+' במאגר, כפי שנמשך ב-'+esc(BOOT.pulled||"")+'</span>';
		h+=legend(x);
		h+='<dl class="nlurm-dl">';
		if(D){
			h+='<div><dt>תכניות מאושרות ובמימוש<small>מפת הרשות, '+esc(dd(MAPD))+'</small></dt><dd>'+N(x.ap)+(x.im?' (במימוש '+N(x.im)+')':'')+'</dd></div>';
			if(x.un)h+='<div><dt>דירות היום ← אחרי הבנייה<small>מפת הרשות, '+esc(dd(MAPD))+', '+pl(x.un,"מתחם","מתחמים")+' עם שני הנתונים</small></dt><dd>'+N(x.e)+' ← '+N(x.p)+'</dd></div>';
			h+='<div><dt>מה זז מאז '+esc(dd(D.agg.since))+'<small>קובץ data.gov.il מול מפת הרשות של '+esc(dd(D.agg.to))+'</small></dt><dd>'+(x.mv?moved(x).join(", "):"לא נמצא שינוי")+'</dd></div>';
			if(x.last)h+='<div><dt>השינוי האחרון<small>'+esc(x.last.r.n)+'</small></dt><dd>'+esc(KIND[x.last.c[1]]||"")+' '+esc(dd(x.last.c[0]))+'</dd></div>';
		}
		if(r)["r3","r4","r5"].forEach(function(k){if(x.px[k])h+='<div><dt>דירת '+k.slice(1)+' חדרים, חציון מחיר עסקה<small>רשות המסים, רבעון '+Q(x.px[k][1])+'</small></dt><dd>'+N(x.px[k][0])+' ₪</dd></div>'});
		if(x.c0)h+='<div><dt>עמודי מתחמים באתר<small>מהקובץ הרשמי, כפי שנמשך ב-'+esc(BOOT.pulled||"")+'</small></dt><dd>'+N(x.c0)+'</dd></div>';
		h+='</dl>';
		var trk=!!document.querySelector('#nlur2-track select[id$="-city"]');
		h+='<div class="nlurm-acts">'+(trk?'<button type="button" class="pri" data-a="trk">יומן המתחמים ב'+esc(x.name)+'</button>':'')+(x.px&&x.px.page?'<a href="'+esc(x.px.page)+'">מחירי הדירות ב'+esc(x.name)+'</a>':'')+(GUIDE[x.name]?'<a href="'+esc(GUIDE[x.name])+'">פינוי בינוי ב'+esc(x.name)+'</a>':'')+'</div>';
		if(D){
			var cn=function(f){return x.recs.filter(function(q){var s=LM>-1?q.s[LM]:-1;return f(s)}).length},gs=[["*","הכול",x.recs.length],["ap","מאושרות ובמימוש",cn(function(s){return s>=3})],["pl","בתכנון",cn(function(s){return s===1||s===2})],["no","ללא שלב",cn(function(s){return s===0})],["off","לא במפה היום",cn(function(s){return s<0})]].filter(function(q){return q[2]>0});
			if(!gs.some(function(q){return q[0]===S.grp}))S.grp="*";
			var R=cxRows(x),max=S.more?9999:(touch?12:40);if(focusKey){for(var fi=0;fi<R.length;fi++){if(R[fi].k===focusKey){if(fi>=max)max=fi+1;break}}}
			h+='<div class="nlurm-cxh"><h3>המתחמים ב'+esc(x.name)+'</h3><select data-a="sort" aria-label="סדר הרשימה"><option value="st"'+(S.sort==="st"?" selected":"")+'>לפי שלב</option><option value="un"'+(S.sort==="un"?" selected":"")+'>לפי דירות שיתווספו</option><option value="ch"'+(S.sort==="ch"?" selected":"")+'>לפי שינוי אחרון</option><option value="nm"'+(S.sort==="nm"?" selected":"")+'>לפי שם</option></select>'
				+'<div class="nlurm-chips" role="group" aria-label="סינון לפי שלב">'+gs.map(function(q){return'<button type="button" class="nlurm-chip" data-a="grp" data-g="'+q[0]+'" aria-pressed="'+(S.grp===q[0])+'">'+esc(q[1])+' <span class="n">'+q[2]+'</span></button>'}).join("")+'</div></div>';
			h+='<ul class="nlurm-cx">'+R.slice(0,max).map(function(q){
				var s=LM>-1?q.s[LM]:-1,c=q.ch&&q.ch[q.ch.length-1],meta=[s<0?"לא במפת הרשות היום":ST[s]];
				if(q.p)meta.push(q.e?"היום "+n0(q.e)+" ← "+n0(q.p)+" דירות":n0(q.p)+" דירות אחרי הבנייה");if(c)meta.push((KIND[c[1]]||"")+" "+dd(c[0]));
				var inner='<b>'+esc(q.n)+'</b><span>'+esc(meta.join(" · "))+'</span>';
				return'<li data-k="'+esc(q.k)+'"'+(q.k===focusKey?' class="is-hi"':'')+'><span class="sq" style="background:'+(s<0?"#fff;box-shadow:inset 0 0 0 1px #C42550":SC[s])+'"></span>'+(q.w?'<a class="cxm" href="/projects/'+esc(slug(q.w))+'/">'+inner+'</a>':'<div class="cxm">'+inner+'</div>')+(trk?'<button type="button" class="cxt" data-a="cx" data-k="'+esc(q.k)+'" aria-label="'+esc(q.n)+' ביומן המתחמים">ביומן</button>':'')+'</li>'}).join("")+'</ul>';
			if(R.length>max)h+='<button type="button" class="nlurm-more" data-a="more">הציגו את כל '+R.length+' המתחמים</button>';
		}else{h+='<div class="nlurm-look"></div>'}
		h+='<div class="nlurm-acts"><button type="button" data-a="link">העתיקו קישור לעיר</button></div>'+srcLine();
		side.innerHTML=h;
		if(!D)lookup(x,side.querySelector(".nlurm-look"));
		if(focusKey){var li=side.querySelector('li[data-k="'+focusKey.replace(/"/g,"")+'"]');if(li)li.scrollIntoView({block:"nearest"})}
	}
	function lookup(x,box){ // the fallback when the tracker file is not on the page: today's list, with an honest message at the hourly limit
		box.innerHTML='<p class="nlurm-msg">טוענים את מתחמי '+esc(x.name)+'...</p>';
		fetch(LOOK+"?city="+encodeURIComponent(x.name)).then(function(r){if(r.status===429)throw{lim:1};if(!r.ok)throw{};return r.json()}).then(function(j){
			box.innerHTML=(j.matches||[]).map(function(m){var t=m.project_type==="pinui_binui"?"פינוי בינוי":(m.project_type==="tama38"?"תמא 38":"התחדשות");return'<div class="nlur-hit"><b>'+esc(m.title)+'</b> · '+t+(m.plan_number?' · תכנית '+esc(m.plan_number):'')+' · <a href="'+esc(m.url)+'">לעמוד המתחם</a></div>'}).join("")||'<p class="nlurm-msg">לא נמצאו מתחמים לעיר הזו ברשימה.</p>';
		}).catch(function(e){box.innerHTML='<p class="nlurm-msg">'+(e&&e.lim?"הגעתם למספר הבדיקות המרבי לשעה מהחיבור הזה. נסו שוב בעוד כמה דקות; רשימת הערים והמתחמים המלאה מוצגת גם מטה בעמוד.":"הרשימה לא נטענה כרגע. נסו שוב בעוד רגע.")+'</p>'})}
	function panel(focusKey){if(S.sel)cityView(S.sel,focusKey);else listView()}
	function hiRow(x,on){var b=side.querySelector('.ctr[data-f="'+x.f+'"]');if(b)b.classList.toggle("is-hi",!!on)}
	side.addEventListener("click",function(e){
		var t=e.target.closest("[data-a],.ctr");if(!t)return;var a=t.getAttribute("data-a");
		if(t.classList.contains("ctr")){var x=BYF[t.getAttribute("data-f")];if(x)select(x,{fly:true,from:"list"});return}
		if(a==="back")select(null);else if(a==="list"){S.list=1;listView()}else if(a==="more"){S.more=1;panel()}
		else if(a==="grp"){S.grp=t.getAttribute("data-g");S.more=0;panel()}
		else if(a==="trk"&&S.sel)toTracker(S.sel.name);else if(a==="cx"&&S.sel)toTracker(S.sel.name,t.getAttribute("data-k"));
		else if(a==="link"&&S.sel){var u=location.origin+location.pathname+"#nlurm="+encodeURIComponent(S.sel.name);var done=function(){t.textContent="הקישור הועתק"};if(navigator.clipboard)navigator.clipboard.writeText(u).then(done,function(){window.prompt("העתיקו את הקישור",u)});else window.prompt("העתיקו את הקישור",u)}
	});
	side.addEventListener("change",function(e){if(e.target.getAttribute("data-a")==="sort"){S.sort=e.target.value;S.more=0;panel()}});
	if(!touch){side.addEventListener("mouseover",function(e){var t=e.target.closest(".ctr");var x=t&&BYF[t.getAttribute("data-f")];if(x!==S.hi){S.hi=x||null;soon()}});side.addEventListener("mouseleave",function(){if(S.hi){S.hi=null;soon()}})}
	/* ---------- choosing a city ---------- */
	function select(x,o){
		o=o||{};S.sel=x;S.more=0;S.grp="*";S.hi=null;pop(null);
		if(x){
			var b=map.getBounds(),z=map.getZoom();
			if(o.fly||!b.contains(x.ll))map.easeTo({center:x.ll,zoom:Math.max(z,o.zoom||(z<9?9.5:z)),duration:600});
			live.textContent="נבחרה "+x.name+": "+txt(lines(x,"all")[0]);
		}else live.textContent="";
		panel(o.cx);peek(x);soon();
		if(x&&o.from==="list"&&!touch){var ct=side.querySelector(".ct");if(ct)ct.focus({preventScroll:true})}
		if(x&&o.from==="search"&&!isWide())to(host,100);
	}
	/* ---------- chips and search ---------- */
	function chips(){var c=bar.querySelector(".nlurm-chips");c.innerHTML=MODES.filter(function(m){return D||m[0]==="all"||m[0]==="px"}).map(function(m){return'<button type="button" class="nlurm-chip" data-m="'+m[0]+'" aria-pressed="'+(S.mode===m[0])+'">'+esc(m[1])+'</button>'}).join("")}
	bar.querySelector(".nlurm-chips").addEventListener("click",function(e){var b=e.target.closest(".nlurm-chip");if(!b||!CITY.length)return;S.mode=b.getAttribute("data-m");chips();measure();soon();panel()});
	var qi=bar.querySelector("input"),res=bar.querySelector(".nlurm-res");
	function search(q){
		var f=fold(q),out=[];if(f.replace(/ /g,"").length<2){res.hidden=true;return}
		CITY.forEach(function(x){if(x.f.indexOf(f)>-1)out.push({t:"c",x:x})});
		if(D){var toks=f.split(" "),qc=f.replace(/ /g,"");D.recs.forEach(function(r){if(out.length>=14)return;var hs=r.__h||(r.__h=fold(r.n+" "+r.c+" "+(r.pl||""))),pp=r.__p||(r.__p=fold(r.pl||"").replace(/ /g,""));if(toks.every(function(w){return hs.indexOf(w)>-1})||(qc.length>=4&&pp.indexOf(qc)>-1)){var x=BYF[fold(r.c)];if(x)out.push({t:"x",x:x,r:r})}})}
		res.innerHTML=out.length?out.slice(0,14).map(function(o,i){return o.t==="c"?'<button type="button" role="option" data-i="'+i+'">'+esc(o.x.name)+'<small>עיר · '+txt(lines(o.x,"all")[0])+'</small></button>':'<button type="button" role="option" data-i="'+i+'">'+esc(o.r.n)+'<small>'+esc(o.x.name)+(o.r.pl?' · תכנית '+esc(o.r.pl):'')+(LM>-1&&o.r.s[LM]>=0?' · '+esc(ST[o.r.s[LM]]):' · לא במפת הרשות היום')+'</small></button>'}).join(""):'<p>לא מצאנו עיר או מתחם בשם הזה. נסו שם רחוב, שם מתחם או מספר תכנית.</p>';
		res.hidden=false;res._o=out;
	}
	function pick(o){res.hidden=true;qi.value=o.t==="c"?o.x.name:o.r.n;if(o.t==="x"&&o.r.s[LM]<0)S.grp="*";select(o.x,{fly:true,zoom:10.5,cx:o.t==="x"?o.r.k:null,from:"search"})}
	qi.addEventListener("input",function(){search(qi.value)});
	qi.addEventListener("keydown",function(e){if(e.key==="Enter"&&res._o&&res._o.length&&!res.hidden){e.preventDefault();pick(res._o[0])}else if(e.key==="ArrowDown"){var f=res.querySelector("button");if(f){e.preventDefault();f.focus()}}else if(e.key==="Escape"){res.hidden=true}});
	res.addEventListener("click",function(e){var b=e.target.closest("button");if(b&&res._o)pick(res._o[+b.getAttribute("data-i")])});
	res.addEventListener("keydown",function(e){var b=e.target.closest("button");if(!b)return;if(e.key==="ArrowDown"&&b.nextElementSibling){e.preventDefault();b.nextElementSibling.focus()}else if(e.key==="ArrowUp"){e.preventDefault();(b.previousElementSibling||qi).focus()}else if(e.key==="Escape"){res.hidden=true;qi.focus()}});
	document.addEventListener("click",function(e){if(!bar.contains(e.target))res.hidden=true});
	document.addEventListener("keydown",function(e){if(e.key==="Escape"&&S.sel&&!bar.contains(e.target)){var x=S.sel;select(null);if(x.btn&&x.btn.style.display!=="none")x.btn.focus({preventScroll:true})}});
	/* ---------- the map ---------- */
	function boot(){
		try{
			/* Hebrew base-map labels: the RTL text plugin (fetched only when Hebrew text appears) + the map language */
			try{if(mapboxgl.getRTLTextPluginStatus()==="unavailable"){mapboxgl.setRTLTextPlugin("https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.3.0/mapbox-gl-rtl-text.js",null,true)}}catch(e){}
			mapboxgl.accessToken="<?php echo esc_js( $token ); ?>";
			map=new mapboxgl.Map({container:"nlurm-map",style:"mapbox://styles/mapbox/light-v11",language:"he",center:[34.9,31.9],zoom:7,attributionControl:true,cooperativeGestures:true,
				locale:{"CooperativeGesturesHandler.WindowsHelpText":"לחצו Ctrl וגללו כדי להתקרב במפה","CooperativeGesturesHandler.MacHelpText":"לחצו ⌘ וגללו כדי להתקרב במפה","TouchPanBlocker.Message":"הזיזו את המפה בשתי אצבעות"}});
		}catch(e){fail();return}
		map.addControl(new mapboxgl.NavigationControl());
		map.addControl({onAdd:function(){var d=document.createElement("div");d.className="mapboxgl-ctrl mapboxgl-ctrl-group nlurm-home";d.innerHTML='<button type="button" aria-label="הצגת כל הארץ">כל הארץ</button>';
			d.firstChild.addEventListener("click",function(){var b=new mapboxgl.LngLatBounds();CITY.forEach(function(x){b.extend(x.ll)});if(CITY.length)map.fitBounds(b,{padding:30,duration:600})});return d},onRemove:function(){}},"top-right");
		map.on("click",function(e){
			var p=e.point,best=null,bd=1e9;
			CITY.forEach(function(x){if(!x.vis||x.hd)return;var d=Math.hypot(x.qx-p.x,x.qy-p.y);if(x.t==="S"&&x.cd){var b=x.cd.bx,dx=Math.max(b[0]-p.x,0,p.x-b[2]),dy=Math.max(b[1]-p.y,0,p.y-b[3]);if(dx<=6&&dy<=14)d=Math.min(d,Math.hypot(dx,dy))}if(d<bd){bd=d;best=x}});
			if(best&&bd<=22){select(best,{from:"map"});return} // forgiving taps on names and points, without buttons that overlap
			if(S.sel&&!isWide())select(null);
		});
		var ready=Promise.all([getJSON(REST),getJSON(trackerUrl())]);
		map.on("load",function(){ready.then(function(v){
			CITY=build(v[0],v[1]);if(!CITY.length)return;
			chips();makeTags();panel();
			var h=decodeURIComponent((location.hash.match(/nlurm=([^&]+)/)||[])[1]||""),hx=h&&BYF[fold(h)];if(hx)select(hx,{fly:true,zoom:10});
			map.on("zoom",soonZoom);map.on("zoomend",soon);var lvT=0;map.on("moveend",function(){soon();clearTimeout(lvT);lvT=setTimeout(function(){if(!S.sel&&!map.isMoving())listView()},180)});map.on("idle",function(){if(!dedupe.m)dedupe()});map.on("resize",function(){geo=null;soon()});map.on("movestart",function(){pop(null)});
			if(document.fonts&&document.fonts.load){Promise.all([document.fonts.load('600 14px "IBM Plex Sans Hebrew"',"רמת גן"),document.fonts.load('500 12px "IBM Plex Mono"',"0123")]).then(function(){measure();soon()},function(){})}
			soon();
		})});
	}
	if(window.mapboxgl){boot();return}
	var l=document.createElement("link");l.rel="stylesheet";l.href="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css";document.head.appendChild(l);
	var s=document.createElement("script");s.src="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js";s.onload=boot;s.onerror=fail;document.head.appendChild(s);
})();
</script>
	<?php
	return ob_get_clean();
} );

/* 1.72.520: the data layer (stats, tables, charts, 20 questions) from data/renewal-stats.json; loaded only if present (the 25.10 rule) */
if ( file_exists( __DIR__ . '/urban-map-data.php' ) ) { require_once __DIR__ . '/urban-map-data.php'; }
