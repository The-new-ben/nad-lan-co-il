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
		) );
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
	ob_start(); ?>
<div class="nlurm" dir="rtl">
	<div id="nlurm-map"></div>
	<p class="nlurm-note">המפה מציגה ריכוזי מתחמי התחדשות לפי עיר, מתוך המאגר הרשמי (data.gov.il) כפי שנמשך ב-<?php echo esc_html( function_exists( 'nadlan_ur_source_pulled' ) ? nadlan_ur_source_pulled() : '13.7.2026' ); ?>. הקישו על עיר לרשימת המתחמים בה.</p>
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
#nlurm-map{height:520px;border-radius:16px;overflow:hidden;border:1px solid #D3DCE2;background:#14130F}
.nlurm-note{font:400 12.5px/1.6 Heebo,sans-serif;color:#6D665C;margin:10px 0}
/* city labels (26.10.2026 proposal): a circle sized by the count, the count in white mono, the city name in ink with a white halo; colours of .nlur2 (deep #1F4B5C, ink #12202A, sea #2F6F86) */
.nlurm-pin{--r:12px;--h:22px;width:calc(var(--h)*2);height:calc(var(--h)*2);margin:0;padding:0;border:0;background:none;cursor:pointer;-webkit-tap-highlight-color:transparent}
.nlurm-dot{position:absolute;left:50%;top:50%;width:calc(var(--r)*2);height:calc(var(--r)*2);transform:translate(-50%,-50%);box-sizing:border-box;border-radius:50%;background:#1F4B5C;border:2px solid #fff;box-shadow:0 1px 4px rgba(18,32,42,.38);color:#fff;font:500 12px/1 "IBM Plex Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums;display:flex;align-items:center;justify-content:center;direction:ltr;transition:transform .12s ease,box-shadow .12s ease}
.nlurm-name{position:absolute;top:50%;white-space:nowrap;font:600 13px/18px "IBM Plex Sans Hebrew",system-ui,sans-serif;color:#12202A;text-shadow:0 0 1px #fff,0 0 2px #fff,0 0 3px #fff,0 0 4px #fff,1px 1px 0 #fff,-1px -1px 0 #fff,1px -1px 0 #fff,-1px 1px 0 #fff;visibility:hidden;text-underline-offset:3px;text-decoration-thickness:1px}
.nlurm-pin .nlurm-name{font-family:"IBM Plex Sans Hebrew",system-ui,sans-serif!important}.nlurm-pin .nlurm-dot{font-family:"IBM Plex Mono",ui-monospace,monospace!important} /* the skin forces Assistant on every span with !important (body.nl-skin-a span) */
.nlurm-pin.is-big .nlurm-name{font-size:15px;line-height:20px}
.nlurm-pin.is-e .nlurm-name{visibility:visible;left:calc(50% + var(--r) + 4px);transform:translateY(-50%)}
.nlurm-pin.is-w .nlurm-name{visibility:visible;right:calc(50% + var(--r) + 4px);transform:translateY(-50%)}
.nlurm-pin.is-n .nlurm-name,.nlurm-pin.is-q .nlurm-name{top:auto;bottom:calc(50% + var(--r) + 3px);left:50%;transform:translateX(-50%)}
.nlurm-pin.is-n .nlurm-name{visibility:visible}
.nlurm-pin.is-s .nlurm-name{visibility:visible;top:calc(50% + var(--r) + 3px);left:50%;transform:translateX(-50%)}
.nlurm-pin.is-ne .nlurm-name,.nlurm-pin.is-se .nlurm-name{visibility:visible;left:calc(50% + var(--r)*.72 + 2px)}.nlurm-pin.is-nw .nlurm-name,.nlurm-pin.is-sw .nlurm-name{visibility:visible;right:calc(50% + var(--r)*.72 + 2px)}
.nlurm-pin.is-ne .nlurm-name,.nlurm-pin.is-nw .nlurm-name{top:auto;bottom:calc(50% + var(--r)*.72)}.nlurm-pin.is-se .nlurm-name,.nlurm-pin.is-sw .nlurm-name{top:calc(50% + var(--r)*.72)}
.nlurm-grp .nlurm-dot{box-shadow:inset 0 0 0 3px #1F4B5C,inset 0 0 0 4.5px rgba(255,255,255,.75),0 1px 4px rgba(18,32,42,.38)}
.nlurm-pin:hover,.nlurm-pin:focus-visible,.nlurm-pin.is-on{z-index:3}
.nlurm-pin:hover .nlurm-dot{transform:translate(-50%,-50%) scale(1.08);box-shadow:0 0 0 4px rgba(47,111,134,.3),0 2px 6px rgba(18,32,42,.4)}
.nlurm-grp:hover .nlurm-dot{box-shadow:inset 0 0 0 3px #1F4B5C,inset 0 0 0 4.5px rgba(255,255,255,.75),0 0 0 4px rgba(47,111,134,.3),0 2px 6px rgba(18,32,42,.4)}
.nlurm-pin:hover .nlurm-name{visibility:visible;text-decoration-line:underline}
.nlurm-pin:active .nlurm-dot{transform:translate(-50%,-50%) scale(.94)}
.nlurm-pin:focus{outline:none}.nlurm-pin:focus-visible .nlurm-dot{outline:2px solid #2F6F86;outline-offset:3px}.nlurm-pin:focus-visible .nlurm-name{visibility:visible}
.nlurm-pin.is-q:hover .nlurm-name,.nlurm-pin.is-q:focus-visible .nlurm-name{background:#fff;border:1px solid #D3DCE2;border-radius:4px;padding:0 6px;text-shadow:none}
.nlurm-pin.is-on .nlurm-dot{background:#12202A;color:#fff;border-color:#fff;box-shadow:0 0 0 3px #2F6F86,0 2px 8px rgba(18,32,42,.45)}
.nlurm-pin.is-on .nlurm-name{visibility:visible;color:#fff;background:#12202A;border:0;border-radius:4px;padding:0 6px;text-shadow:none;text-decoration-line:none}
#nlurm-list .nlur-hit{background:#fff;border:1px solid #E2DCD0;border-radius:10px;padding:12px 14px;margin-top:8px;font:400 13.5px/1.6 Heebo,sans-serif}
</style>
<script>
(function(){
	var host=document.getElementById("nlurm-map");if(!host||host.dataset.wired)return;host.dataset.wired="1";
	function fail(){
		// no WebGL / blocked script: never leave a black box - the crawlable
		// city directory below carries the same data
		host.style.display="none";
		var n=document.createElement("p");
		n.className="nlurm-note";
		n.textContent="המפה האינטראקטיבית דורשת דפדפן עם תמיכה גרפית (WebGL). רשימת הערים והמתחמים המלאה מוצגת מטה.";
		host.parentNode.insertBefore(n,host.nextSibling);
	}
	/* city labels: biggest counts first; cities whose tap areas (44px) would touch share one circle with the summed count,
	   a tap on it zooms in; a name shows only where it fits with no overlap, the rest wait for a closer zoom, a hover or a tap */
	function nlurmFold(s){return String(s||"").replace(/[\u0591-\u05C7]/g,"").replace(/[-\u2010-\u2015,.;:!?"'\u05F3\u05F4()\/]/g," ").replace(/\s+/g," ").trim().replace(/יי/g,"י").replace(/וו/g,"ו")}
	function nlurmLabels(map,pins){
		var pool=[],last=-1,raf=0,cv=document.createElement("canvas").getContext("2d"),wd={},own={},seen={},hide=[],base={};
		pins.forEach(function(p){var f=nlurmFold(p.c.city),w=f.split(" ");own[f]=1;if(w.length>2)own[w[0]+" "+w[1]]=1}); // also the short form (תל אביב)
		var fine=!!(window.matchMedia&&matchMedia("(pointer:fine)").matches); // mouse: 24px targets (WCAG 2.5.8); touch: 44px
		function rad(n){return Math.min(fine?30:26,9+1.5*Math.sqrt(n))}
		function tw(t,big){var k=t+big;if(!wd[k]){cv.font="600 "+(big?15:13)+'px "IBM Plex Sans Hebrew"';wd[k]=Math.ceil(cv.measureText(t).width)+4}return wd[k]}
		function hits(a,b){return a[0]<b[2]&&b[0]<a[2]&&a[1]<b[3]&&b[1]<a[3]}
		function hk(k){return Math.max(rad(k.n),fine?12:22)} // half the tap square
		function paint(el,n,name,side,big,h){
			var r=rad(n);el.style.setProperty("--r",r.toFixed(1)+"px");el.style.setProperty("--h",h.toFixed(1)+"px");
			el.firstChild.style.fontSize=(r<15?11:r<22?12:13)+"px";el.firstChild.textContent=n;el.lastChild.textContent=name;
			el.className=el.className.replace(/ is-(ne|nw|se|sw|e|w|n|s|q|big)\b/g,"")+" is-"+(side||"q")+(big?" is-big":"");
			el.title=side?"":name;
		}
		function grp(i){
			if(!pool[i]){
				var el=document.createElement("button");el.type="button";el.className="nlurm-pin nlurm-grp";
				el.innerHTML='<span class="nlurm-dot"></span><span class="nlurm-name"></span>';
				el.addEventListener("click",function(){var b=new mapboxgl.LngLatBounds();el._m.forEach(function(p){b.extend(p.c.lnglat)});map.fitBounds(b,{padding:80,maxZoom:13,duration:700})});
				pool[i]={el:el,mk:new mapboxgl.Marker({element:el,anchor:"center"}).setLngLat([34.9,31.9]).addTo(map)};
			}
			return pool[i];
		}
		function near(a,b){return Math.max(Math.abs(a.x-b.x),Math.abs(a.y-b.y))<hk(a)+hk(b)+2} // the square tap areas would touch
		function gap(bx,k){var x=Math.max(bx[0],Math.min(k.x,bx[2])),y=Math.max(bx[1],Math.min(k.y,bx[3]));return Math.hypot(x-k.x,y-k.y)-rad(k.n)}
		function mine(bx,g,ix){var d=gap(bx,g[ix]);for(var q=0;q<g.length;q++){if(q!==ix&&gap(bx,g[q])<d+8)return false}return true} // a name sits clearly nearest its own circle
		function lay(){
			raf=0;last=map.getZoom();
			var cont=map.getContainer(),W=cont.clientWidth,H=cont.clientHeight,cr=cont.getBoundingClientRect(),placed=[],used=0,g=[];
			// biggest first: a city joins the nearest group whose tap area it would touch, else it opens its own (the group sits on its biggest city)
			pins.map(function(p){var q=map.project(p.c.lnglat);return{m:[p],n:+p.c.count,x:q.x,y:q.y}}).sort(function(a,b){return b.n-a.n}).forEach(function(c){
				var best=null,bd=1e9;g.forEach(function(k){var d=Math.max(Math.abs(c.x-k.x),Math.abs(c.y-k.y));if(near(c,k)&&d<bd){bd=d;best=k}});
				if(best){best.m.push(c.m[0]);best.n+=c.n}else g.push(c);
			});
			// a group that grew may now touch another one: the smaller joins the bigger
			for(var pass=0,moved=true;moved&&pass<30;pass++){moved=false;g.sort(function(a,b){return b.n-a.n});
				for(var i=0;i<g.length&&!moved;i++){for(var j=i+1;j<g.length;j++){if(near(g[i],g[j])){g[i].m=g[i].m.concat(g[j].m);g[i].n+=g[j].n;g.splice(j,1);moved=true;break}}}
			}
			g.forEach(function(k){k.m.sort(function(a,b){return b.c.count-a.c.count})});
			var block=g.map(function(k){var h=hk(k)+1;return[k.x-h,k.y-h,k.x+h,k.y+h]});
			[].forEach.call(cont.querySelectorAll(".mapboxgl-ctrl"),function(c){var b=c.getBoundingClientRect();if(b.width)block.push([b.left-cr.left-4,b.top-cr.top-4,b.right-cr.left+4,b.bottom-cr.top+4])});
			g.forEach(function(k,ix){
				var r=rad(k.n),x=k.x,y=k.y,big=k.m.length===1&&k.n>=40,h=big?20:18,t=k.m.length>1?k.m[0].c.city+" ועוד "+(k.m.length-1):k.m[0].c.city,w=tw(t,big),d=r*0.72;
				var c=[["e",[x+r+3,y-h/2,x+r+5+w,y+h/2]],["w",[x-r-5-w,y-h/2,x-r-3,y+h/2]],["ne",[x+d+2,y-d-h,x+d+4+w,y-d]],["nw",[x-d-4-w,y-d-h,x-d-2,y-d]],
					["se",[x+d+2,y+d,x+d+4+w,y+d+h]],["sw",[x-d-4-w,y+d,x-d-2,y+d+h]],["n",[x-w/2,y-r-4-h,x+w/2,y-r-2]],["s",[x-w/2,y+r+2,x+w/2,y+r+4+h]]],side=null;
				for(var s=0;s<c.length&&!side;s++){var bx=c[s][1],ok=bx[0]>2&&bx[1]>2&&bx[2]<W-2&&bx[3]<H-2,q;
					for(q=0;ok&&q<block.length;q++){if(q!==ix&&hits(bx,block[q]))ok=false}
					for(q=0;ok&&q<placed.length;q++){if(hits(bx,placed[q]))ok=false}
					if(ok&&mine(bx,g,ix)){side=c[s][0];placed.push(bx)}}
				if(k.m.length===1){k.m[0].el.style.display="";paint(k.m[0].el,k.n,t,side,big,hk(k))}
				else{
					k.m.forEach(function(p){p.el.style.display="none";p.el.classList.remove("is-on")});
					var o=grp(used++);o.el._m=k.m;o.el.style.display="";o.mk.setLngLat(map.unproject([x,y]));paint(o.el,k.n,t,side,false,hk(k));
					o.el.setAttribute("aria-label",k.m[0].c.city+" ועוד "+(k.m.length-1)+" ערים: "+k.n+" מתחמים. הקשה מקרבת את המפה");
				}
			});
			for(var u=used;u<pool.length;u++){pool[u].el.style.display="none"}
		}
		var muted=0;
		function dedupe(){ // the base map's own label for a city these labels already name is hidden: one name per place
			try{var add=0,f;
				if(!muted){muted=1;["country-label","state-label","settlement-major-label","settlement-minor-label","settlement-subdivision-label"].forEach(function(id){if(map.getLayer(id)&&map.getPaintProperty(id,"text-opacity")==null)map.setPaintProperty(id,"text-opacity",.6)})} // the base map's words step back
				map.querySourceFeatures("composite",{sourceLayer:"place_label"}).forEach(function(x){var n=x.properties.name;if(n&&!seen[n]){seen[n]=1;if(own[nlurmFold(n)]){hide.push(n);add=1}}});
				if(!add)return;f=["!",["in",["get","name"],["literal",hide]]];
				["settlement-major-label","settlement-minor-label","settlement-subdivision-label"].forEach(function(id){if(!map.getLayer(id))return;if(!(id in base))base[id]=map.getFilter(id)||null;map.setFilter(id,base[id]?["all",base[id],f]:f)});
			}catch(e){}
		}
		function soon(){if(!raf)raf=requestAnimationFrame(lay)}
		pins.forEach(function(p){p.el.addEventListener("click",function(){pins.forEach(function(o){if(o!==p)o.el.classList.remove("is-on")});p.el.classList.add("is-on")})});
		map.on("move",function(){if(Math.abs(map.getZoom()-last)>0.2)soon()});
		map.on("moveend",soon);map.on("resize",soon);map.on("idle",dedupe);
		if(document.fonts&&document.fonts.load){document.fonts.load('600 13px "IBM Plex Sans Hebrew"',"רמת גן").then(function(){wd={};soon()},soon)}
		soon();
	}
	function boot(){
		var map;
		try{
			mapboxgl.accessToken="<?php echo esc_js( $token ); ?>";
			/* Hebrew base-map labels: the RTL text plugin (fetched only when Hebrew text appears) + the map language */
			try{if(mapboxgl.getRTLTextPluginStatus()==="unavailable"){mapboxgl.setRTLTextPlugin("https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.3.0/mapbox-gl-rtl-text.js",null,true)}}catch(e){}
			map=new mapboxgl.Map({container:"nlurm-map",style:"mapbox://styles/mapbox/light-v11",language:"he",center:[34.9,31.9],zoom:7,attributionControl:true,cooperativeGestures:true,
				locale:{"CooperativeGesturesHandler.WindowsHelpText":"לחצו Ctrl וגללו כדי להתקרב במפה","CooperativeGesturesHandler.MacHelpText":"לחצו ⌘ וגללו כדי להתקרב במפה","TouchPanBlocker.Message":"הזיזו את המפה בשתי אצבעות"}});
		}catch(e){fail();return}
		map.addControl(new mapboxgl.NavigationControl());
		fetch("<?php echo $rest; // phpcs:ignore ?>").then(function(r){return r.json()}).then(function(d){
			var pins=[];
			(d.cities||[]).forEach(function(c){
				if(!c.lnglat)return;
				var el=document.createElement("button");el.className="nlurm-pin";el.type="button";
				el.innerHTML='<span class="nlurm-dot"></span><span class="nlurm-name"></span>';el.firstChild.textContent=c.count;el.lastChild.textContent=c.city;
				el.setAttribute("aria-label",c.city+": "+c.count+" מתחמים");
				el.addEventListener("click",function(){
					var list=document.getElementById("nlurm-list");
					list.innerHTML='<div class="nlur-hit">טוענים את מתחמי '+c.city+'...</div>';
					fetch("<?php echo esc_url( rest_url( 'nadlan/v1/renewal-lookup' ) ); // phpcs:ignore ?>?city="+encodeURIComponent(c.city))
						.then(function(r){return r.json()}).then(function(x){
							list.innerHTML=(x.matches||[]).map(function(m){
								var t=m.project_type==="pinui_binui"?"פינוי בינוי":(m.project_type==="tama38"?"תמא 38":"התחדשות");
								return '<div class="nlur-hit"><b>'+m.title+'</b> · '+t+(m.plan_number?' · תכנית '+m.plan_number:'')+' · <a href="'+m.url+'">לעמוד המתחם</a></div>';
							}).join("")||'<div class="nlur-hit">אין מתחמים להצגה</div>';
						});
				});
				new mapboxgl.Marker({element:el,anchor:"center"}).setLngLat(c.lnglat).addTo(map);
				pins.push({c:c,el:el});
			});
			nlurmLabels(map,pins);
		});
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
