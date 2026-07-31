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
		$hit = get_transient( 'nadlan_ur_mapdata_v3' );
		if ( is_array( $hit ) ) { return $hit; }
		global $wpdb;
		$rows = $wpdb->get_results( "
			SELECT c.meta_value AS city, t.meta_value AS track, COUNT(*) AS n
			FROM {$wpdb->posts} p
			JOIN {$wpdb->postmeta} s ON s.post_id = p.ID AND s.meta_key = 'source' AND s.meta_value = 'urban_renewal'
			JOIN {$wpdb->postmeta} c ON c.post_id = p.ID AND c.meta_key = 'city'
			LEFT JOIN {$wpdb->postmeta} t ON t.post_id = p.ID AND t.meta_key = 'renewal_track'
			WHERE p.post_type = 'nadlan_project' AND p.post_status = 'publish'
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
		set_transient( 'nadlan_ur_mapdata_v3', $out, 6 * HOUR_IN_SECONDS );
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
		$hit = get_transient( 'nadlan_ur_mapseo_v3' );
		if ( is_string( $hit ) && '' !== $hit ) { return $hit; }
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
				. '<p class="nlurm-cn">' . (int) $c['count'] . ' מתחמי פינוי בינוי בפנקס'
				. ( $c['misui'] ? ' · מסלול מיסוי: ' . (int) $c['misui'] : '' )
				. ( $c['rashuyot'] ? ' · מסלול רשויות: ' . (int) $c['rashuyot'] : '' ) . '</p>'
				. ( $links ? '<ul>' . $links . '</ul>' : '' )
				. ( $more > 0 ? '<p class="nlurm-more">ועוד ' . $more . ' מתחמים בעיר (הקישו על העיר במפה לרשימה המלאה)</p>' : '' )
				. '</div>';
			$schema_cities[] = array( '@type' => 'ListItem', 'position' => count( $schema_cities ) + 1, 'name' => $c['city'] . ' - ' . $c['count'] . ' מתחמי פינוי בינוי' );
		}
		$home = home_url();
		$copy = '<section class="nlurm-seo">'
			. '<h2>מתחמי התחדשות עירונית מוכרזים בישראל - לפי עיר</h2>'
			. '<p>המפה מציגה <b>' . $total . ' מתחמי פינוי בינוי</b> מתוך המאגר הרשמי של הרשות הממשלתית להתחדשות עירונית (data.gov.il). לכל מתחם עמוד ייעודי עם מספר התכנית, המסלול והסטטוס. הנתונים מתעדכנים מהמאגר; מיקום מדויק לכל מתחם יתווסף בהמשך ולכן המפה מציגה ריכוזים לפי עיר.</p>'
			. '<p>גרים בבניין שנמצא במתחם מוכרז? התחילו ב<a href="' . esc_url( $home . '/urban-renewal/' ) . '">מדריך ההתחדשות העירונית המלא</a>, בדקו את הבניין שלכם ב<a href="' . esc_url( $home . '/urban-renewal/check/' ) . '">בדיקת בניין חינמית</a>, או קראו על המסלולים: <a href="' . esc_url( $home . '/urban-renewal/pinui-binui/' ) . '">פינוי בינוי</a> ו<a href="' . esc_url( $home . '/urban-renewal/tama-38/' ) . '">תמא 38 והחלופות</a>. נציגות בניין יכולה לפתוח <a href="' . esc_url( $home . '/my-renewal/' ) . '">חדר פרויקט פרטי</a> לניהול ההסכמות והמסמכים.</p>'
			. '<div class="nlurm-cities">' . $cards . '</div>'
			. '</section>';
		$faq = array(
			'@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => array(
				array( '@type' => 'Question', 'name' => 'מה זה מתחם התחדשות עירונית מוכרז?',
					'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'מתחם שהוכרז רשמית על ידי הרשות הממשלתית להתחדשות עירונית או ועדה מוסמכת, במסלול פינוי בינוי או מסלול אחר. ההכרזה פותחת הטבות מס ותהליכי תכנון ייעודיים. הנתונים במפה מגיעים מהמאגר הרשמי בdata.gov.il.' ) ),
				array( '@type' => 'Question', 'name' => 'איך בודקים אם הבניין שלי נמצא במתחם מוכרז?',
					'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'הקישו על העיר שלכם במפה לרשימת המתחמים המוכרזים בה, או השתמשו בבדיקת הבניין החינמית באתר שמצליבה את הכתובת מול המאגר.' ) ),
				array( '@type' => 'Question', 'name' => 'מה ההבדל בין פינוי בינוי לתמא 38?',
					'acceptedAnswer' => array( '@type' => 'Answer', 'text' => 'פינוי בינוי הוא הריסת מתחם שלם ובנייה חדשה, בדרך כלל ביוזמת הרשות או יזם ובהיקף גדול. תמא 38 (והחלופות שהחליפו אותה) היא חיזוק או הריסה ובנייה של בניין בודד. לכל מסלול רף הסכמות שונה של בעלי הדירות.' ) ),
			),
		);
		$dataset = array(
			'@context' => 'https://schema.org', '@type' => 'Dataset',
			'name' => 'מתחמי פינוי בינוי במאגר ההתחדשות העירונית בישראל',
			'description' => 'ריכוז מתחמי ההתחדשות העירונית המוכרזים בישראל לפי עיר ומסלול, מתוך המאגר הרשמי של הרשות הממשלתית להתחדשות עירונית.',
			'creator' => array( '@type' => 'Organization', 'name' => 'הרשות הממשלתית להתחדשות עירונית (data.gov.il)' ),
			'license' => 'https://data.gov.il/terms',
			'url' => home_url( '/urban-renewal/map/' ),
		);
		$list = array( '@context' => 'https://schema.org', '@type' => 'ItemList', 'name' => 'ערים מובילות בהתחדשות עירונית', 'itemListElement' => $schema_cities );
		$GLOBALS['nadlan_ur_map_schemas'] = array( $faq, $dataset, $list );
		$html = $copy
			. '<style>.nlurm-seo{margin-top:34px}.nlurm-seo h2{font-family:"Frank Ruhl Libre",Georgia,serif;font-size:clamp(1.25rem,2.6vw,1.6rem);margin:0 0 12px}.nlurm-seo>p{font:400 15px/1.75 Heebo,sans-serif;color:#3E382F;max-width:70ch}.nlurm-cities{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;margin-top:20px}.nlurm-city{background:#fff;border:1px solid #E2DCD0;border-radius:14px;padding:16px 18px}.nlurm-city h3{font:700 16px Heebo,sans-serif;margin:0 0 4px}.nlurm-cn{font:400 12.5px/1.6 Heebo,sans-serif;color:#6D665C;margin:0 0 8px}.nlurm-city ul{margin:0;padding:0 18px 0 0;font:400 13.5px/1.9 Heebo,sans-serif}.nlurm-city a{color:#9C7A3C}.nlurm-more{font:400 12px/1.5 Heebo,sans-serif;color:#A79E8D;margin:6px 0 0}</style>';
		set_transient( 'nadlan_ur_mapseo_v3', $html, 6 * HOUR_IN_SECONDS );
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
	<p class="nlurm-note">המפה מציגה ריכוזי מתחמים מוכרזים לפי עיר, מתוך המאגר הרשמי (data.gov.il). מיקום מדויק לכל מתחם יתווסף בהמשך; הקישו על עיר לרשימת המתחמים בה.</p>
	<div id="nlurm-list" aria-live="polite"></div>
	<?php
	echo nadlan_ur_map_seo_html(); // phpcs:ignore -- built from escaped parts
	add_action( 'wp_footer', function () {
		foreach ( (array) ( $GLOBALS['nadlan_ur_map_schemas'] ?? array() ) as $sc ) {
			echo '<script type="application/ld+json">' . wp_json_encode( $sc, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n"; // phpcs:ignore
		}
	} );
	?>
</div>
<style>
#nlurm-map{height:520px;border-radius:16px;overflow:hidden;border:1px solid #E2DCD0;background:#14130F}
.nlurm-note{font:400 12.5px/1.6 Heebo,sans-serif;color:#6D665C;margin:10px 0}
.nlurm-pin{background:#9C7A3C;color:#FAF7F1;border:2px solid #FAF7F1;border-radius:999px;padding:6px 11px;font:700 12px Heebo,sans-serif;cursor:pointer;white-space:nowrap;box-shadow:0 6px 16px rgba(0,0,0,.35)}
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
	function boot(){
		var map;
		try{
			mapboxgl.accessToken="<?php echo esc_js( $token ); ?>";
			map=new mapboxgl.Map({container:"nlurm-map",style:"mapbox://styles/mapbox/light-v11",center:[34.9,31.9],zoom:7,attributionControl:true,cooperativeGestures:true,
				locale:{"CooperativeGesturesHandler.WindowsHelpText":"לחצו Ctrl וגללו כדי להתקרב במפה","CooperativeGesturesHandler.MacHelpText":"לחצו ⌘ וגללו כדי להתקרב במפה","TouchPanBlocker.Message":"הזיזו את המפה בשתי אצבעות"}});
		}catch(e){fail();return}
		map.addControl(new mapboxgl.NavigationControl());
		fetch("<?php echo $rest; // phpcs:ignore ?>").then(function(r){return r.json()}).then(function(d){
			(d.cities||[]).forEach(function(c){
				if(!c.lnglat)return;
				var el=document.createElement("button");el.className="nlurm-pin";el.type="button";
				el.textContent=c.city+" · "+c.count;
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
				new mapboxgl.Marker({element:el,anchor:"bottom"}).setLngLat(c.lnglat).addTo(map);
			});
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
