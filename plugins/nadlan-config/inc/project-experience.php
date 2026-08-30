<?php
/**
 * nadlan-config - Project buying experience layer (v1.69.85)
 *
 * Owner mobile-QA 2026-07-01: projects felt stacked, un-unified, apartment
 * selection didn't work, map wasn't clickable, article buried. This module
 * adds a REPLICABLE experience layer to EVERY nadlan_project page:
 *   1. Sticky section nav (סיור ובחירת דירה / סביבה / עוד מידע)
 *   2. Apartment selection lives in the showroom engine only (design audit
 *      2026-07-02, D1/D2): this module must never render a second picker or
 *      standalone interior widget next to the engine.
 *   3. Live clickable surroundings map: streets/satellite, real OSM POIs
 *      (schools/kindergartens/transit/shops/health) AND a FUTURE-PLANS layer -
 *      nearby urban-renewal projects from our own 965-project gov.il dataset,
 *      each marker clickable to its project page (spoke wiring).
 *   4. "The world around the project" grid: contractor, professionals, city,
 *      calculators, guides, glossary - hub-spoke links.
 *   5. Compact factual SEO intro from real meta (no invented content).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---------------- helpers ---------------- */
if ( ! function_exists( 'nadlan_pjx_units' ) ) {
	function nadlan_pjx_units( $id ) {
		$raw = json_decode( (string) get_post_meta( $id, 'project_3d_units', true ), true );
		if ( ! is_array( $raw ) ) { return array(); }
		$units = array();
		foreach ( array_slice( $raw, 0, 60 ) as $u ) {
			if ( ! is_array( $u ) ) { continue; }
			$title = sanitize_text_field( (string) ( $u['title'] ?? '' ) );
			if ( ! $title ) { continue; }
			$floor = 0; $rooms = 0.0;
			if ( preg_match( '/קומה\s*(\d+)/u', $title, $m ) ) { $floor = (int) $m[1]; }
			if ( isset( $u['floor'] ) && (int) $u['floor'] > 0 ) { $floor = (int) $u['floor']; }
			if ( preg_match( '/([\d.]+)\s*חדרים/u', $title, $m ) ) { $rooms = (float) $m[1]; }
			$units[] = array(
				'title' => $title,
				'floor' => $floor,
				'rooms' => $rooms,
				'sqm'   => (int) ( $u['sqm'] ?? ( $u['size_sqm'] ?? 0 ) ),
				'price' => (int) ( $u['price'] ?? 0 ),
			);
		}
		return $units;
	}
}

if ( ! function_exists( 'nadlan_pjx_nearby_projects' ) ) {
	function nadlan_pjx_nearby_projects( $id, $lat, $lng, $limit = 12 ) {
		$key = 'nlpjx_near_v2_' . $id;
		$hit = get_transient( $key );
		if ( is_array( $hit ) ) { return $hit; }
		$q = new WP_Query( array(
			'post_type' => 'nadlan_project', 'post_status' => 'publish',
			'posts_per_page' => $limit + 1, 'post__not_in' => array( $id ),
			'no_found_rows' => true, 'fields' => 'ids',
			'nadlan_private_visibility_applied' => true,
			'meta_query' => nadlan_unit_journey_public_meta_query( array(
				array( 'key' => 'lat', 'value' => array( $lat - 0.016, $lat + 0.016 ), 'compare' => 'BETWEEN', 'type' => 'DECIMAL(10,6)' ),
				array( 'key' => 'lng', 'value' => array( $lng - 0.018, $lng + 0.018 ), 'compare' => 'BETWEEN', 'type' => 'DECIMAL(10,6)' ),
			) ),
		) );
		$out = array();
		foreach ( $q->posts as $pid ) {
			if ( count( $out ) >= $limit ) { break; }
			// name/url/coords only - raw enum fields (type/status) were unused by the
			// map JS and leaked machine values like new_build into the page (D3).
			$out[] = array(
				'name' => get_the_title( $pid ),
				'url'  => get_permalink( $pid ),
				'lat'  => (float) get_post_meta( $pid, 'lat', true ),
				'lng'  => (float) get_post_meta( $pid, 'lng', true ),
			);
		}
		set_transient( $key, $out, 12 * HOUR_IN_SECONDS );
		return $out;
	}
}

/* ---------------- comps: nearby projects WITH price data (R4) ---------------- */
if ( ! function_exists( 'nadlan_pjx_comps' ) ) {
	function nadlan_pjx_comps( $id, $lat, $lng, $limit = 6 ) {
		$key = 'nlpjx_comps_v2_' . $id;
		$hit = get_transient( $key );
		if ( is_array( $hit ) ) { return $hit; }
		$q = new WP_Query( array(
			'post_type' => 'nadlan_project', 'post_status' => 'publish',
			'posts_per_page' => 24, 'post__not_in' => array( $id ),
			'no_found_rows' => true, 'fields' => 'ids',
			'nadlan_private_visibility_applied' => true,
			'meta_query' => nadlan_unit_journey_public_meta_query( array(
				array( 'key' => 'lat', 'value' => array( $lat - 0.03, $lat + 0.03 ), 'compare' => 'BETWEEN', 'type' => 'DECIMAL(10,6)' ),
				array( 'key' => 'lng', 'value' => array( $lng - 0.035, $lng + 0.035 ), 'compare' => 'BETWEEN', 'type' => 'DECIMAL(10,6)' ),
				array( 'key' => 'project_3d_avg_price_per_sqm', 'value' => 1000, 'compare' => '>', 'type' => 'NUMERIC' ),
			) ),
		) );
		$out = array();
		foreach ( $q->posts as $pid ) {
			$plat = (float) get_post_meta( $pid, 'lat', true );
			$plng = (float) get_post_meta( $pid, 'lng', true );
			// language siblings never count as comps
			$p = get_post( $pid );
			if ( $p && preg_match( '/-(en|fr|ru|ar)$/', $p->post_name ) ) { continue; }
			$dist = (int) round( 111320 * sqrt( pow( $plat - $lat, 2 ) + pow( ( $plng - $lng ) * cos( deg2rad( $lat ) ), 2 ) ) );
			$out[] = array(
				'name'  => get_the_title( $pid ),
				'url'   => get_permalink( $pid ),
				'lat'   => $plat, 'lng' => $plng,
				'ppsqm' => (int) get_post_meta( $pid, 'project_3d_avg_price_per_sqm', true ),
				'city'  => (string) get_post_meta( $pid, 'city', true ),
				'dist_m'=> $dist,
			);
		}
		usort( $out, function ( $a, $b ) { return $a['dist_m'] <=> $b['dist_m']; } );
		$out = array_slice( $out, 0, $limit );
		set_transient( $key, $out, 12 * HOUR_IN_SECONDS );
		return $out;
	}
}

/* R4: comps as a public read API too. */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/comps', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function ( $req ) {
			$id = (int) $req->get_param( 'id' );
			$p  = get_post( $id );
			if ( ! $p || $p->post_type !== 'nadlan_project' || $p->post_status !== 'publish'
				|| ( function_exists( 'nadlan_unit_journey_is_private_lab' ) && nadlan_unit_journey_is_private_lab( $id ) ) ) {
				return new WP_Error( 'not_found', 'not_found', array( 'status' => 404 ) );
			}
			$lat = (float) get_post_meta( $id, 'lat', true ); $lng = (float) get_post_meta( $id, 'lng', true );
			if ( ! $lat || ! $lng ) { return array( 'comps' => array() ); }
			return array( 'comps' => nadlan_pjx_comps( $id, $lat, $lng ), 'note' => 'אומדנים לא מחייבים, מבוססים על קטלוג נדלן' );
		},
	) );
} );

/* ---------------- R4: price range + comps section (right after the engine) ---------------- */
if ( ! function_exists( 'nadlan_pjx_price_band' ) ) {
	function nadlan_pjx_price_band( $content ) {
		if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
		$id    = get_the_ID();
		if ( function_exists( 'nadlan_unit_journey_is_private_lab' ) && nadlan_unit_journey_is_private_lab( $id ) ) { return $content; }
		$ppsqm = (int) get_post_meta( $id, 'project_3d_avg_price_per_sqm', true );
		$lat   = (float) get_post_meta( $id, 'lat', true );
		$lng   = (float) get_post_meta( $id, 'lng', true );
		$units = nadlan_pjx_units( $id );
		$prices = array(); $sqms = array();
		foreach ( $units as $u ) {
			if ( ! empty( $u['price'] ) ) { $prices[] = (int) $u['price']; }
			if ( ! empty( $u['sqm'] ) ) { $sqms[] = (int) $u['sqm']; }
		}
		$comps = ( $lat && $lng ) ? nadlan_pjx_comps( $id, $lat, $lng ) : array();
		if ( ! $ppsqm && ! $prices && ! $comps ) { return $content; }
		$token = function_exists( 'nadlan_mapbox_token' ) ? nadlan_mapbox_token() : '';
		ob_start(); ?>
<section class="nlpjx-sec nlpjx-price" id="nlpjx-price" dir="rtl" aria-label="מחירים והשוואה">
	<h2>מחיר: איפה הפרויקט עומד מול הסביבה</h2>
	<div class="nlpjx-price-grid">
		<div class="nlpjx-price-cards">
			<?php if ( $prices ) : ?>
			<div class="nlpjx-price-card"><b><?php echo number_format( min( $prices ) ) . ' - ' . number_format( max( $prices ) ); ?> ₪</b><span>טווח מחירי הדירות המפורסמות בפרויקט. אומדן לא מחייב.</span></div>
			<?php endif; ?>
			<?php if ( $ppsqm ) : ?>
			<div class="nlpjx-price-card"><b>~<?php echo number_format( $ppsqm ); ?> ₪/מ״ר</b><span>מחיר ממוצע למ״ר בפרויקט<?php echo $sqms ? ', דירות ' . min( $sqms ) . '-' . max( $sqms ) . ' מ״ר' : ''; ?>. אומדן לא מחייב.</span></div>
			<?php endif; ?>
			<?php if ( $comps ) : ?>
			<table class="nlpjx-comps">
				<caption>פרויקטים סמוכים להשוואה · מבוסס על קטלוג נדלן</caption>
				<thead><tr><th>פרויקט</th><th>₪/מ״ר</th><th>מרחק</th></tr></thead>
				<tbody>
				<?php foreach ( $comps as $c ) : ?>
					<tr>
						<td><a href="<?php echo esc_url( $c['url'] ); ?>"><?php echo esc_html( $c['name'] ); ?></a></td>
						<td>~<?php echo number_format( $c['ppsqm'] ); ?></td>
						<td><?php echo $c['dist_m'] >= 1000 ? esc_html( number_format( $c['dist_m'] / 1000, 1 ) ) . ' ק״מ' : (int) $c['dist_m'] . ' מ׳'; ?></td>
					</tr>
				<?php endforeach; ?>
				</tbody>
			</table>
			<?php endif; ?>
		</div>
		<?php if ( $lat && $lng && $comps ) : ?>
		<div class="nlpjx-price-mapnote"><a href="#nlpjx-map">כל המחירים, המוסדות והתוכניות - על המפה החיה למטה ←</a></div>
		<script type="application/json" id="nlpjx-comps-data"><?php echo wp_json_encode( $comps ); // phpcs:ignore ?></script>
		<?php endif; ?>
	</div>
	<p class="nlpjx-cap">האומדנים מבוססים על נתונים גלויים בקטלוג נדלן ואינם מחייבים. יש לאמת מחירים מול היזם.</p>
</section>
<?php
		return $content . ob_get_clean();
	}
}
add_filter( 'the_content', 'nadlan_pjx_price_band', 9 );

/* ---------------- 1+2: sticky nav + intro + apartment selector (before engine) ---------------- */
if ( ! function_exists( 'nadlan_pjx_top' ) ) {
	function nadlan_pjx_top( $content ) {
		if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
		if ( function_exists( 'nadlan_unit_journey_is_private_lab' ) && nadlan_unit_journey_is_private_lab( get_the_ID() ) ) { return $content; }
		/* Owner evidence 2026-08-09: on engine pages this nav+intro was
		 * re-attached AFTER the theater together with the legacy profile
		 * header - the photographed mid-page "page restart". The theater
		 * panel already carries the lead and the project facts. */
		if ( function_exists( 'nadlan_showroom_engine_active_for' )
			&& nadlan_showroom_engine_active_for( get_the_ID() ) ) {
			return $content;
		}
		$id  = get_the_ID();
		$g   = function ( $k ) use ( $id ) { return get_post_meta( $id, $k, true ); };
		$dev = (string) $g( 'developer_name' );
		$city = (string) $g( 'city' );
		$floors = (int) $g( 'num_floors' );
		$units_n = (int) $g( 'num_units' );
		$status = (string) $g( 'project_status' );
		$status_he = array( 'planning' => 'בתכנון', 'marketing' => 'בשיווק', 'construction' => 'בבנייה', 'completed' => 'הושלם' );

		ob_start(); ?>
<nav class="nlpjx-nav" aria-label="ניווט בעמוד הפרויקט" dir="rtl">
	<a href="#nl-root">סיור ובחירת דירה</a>
	<a href="#nlpjx-map">מפה וסביבה</a>
	<a href="#nlpjx-world">עוד מידע</a>
</nav>
<div class="nlpjx-intro" dir="rtl">
	<?php
	$bits = array();
	if ( $dev ) { $bits[] = 'פרויקט של ' . esc_html( $dev ); }
	if ( $city ) { $bits[] = 'ב' . esc_html( $city ); }
	if ( $floors ) { $bits[] = $floors . ' קומות'; }
	if ( $units_n ) { $bits[] = number_format( $units_n ) . ' יחידות דיור'; }
	if ( $status && isset( $status_he[ $status ] ) ) { $bits[] = 'סטטוס: ' . $status_he[ $status ]; }
	if ( $bits ) { echo '<p>' . implode( ' · ', $bits ) . '. כל הנתונים, הדמיות, מפת הסביבה ותוכניות עתידיות - בעמוד אחד, כאילו ביקרתם בפרויקט.</p>'; }
	?>
</div>
<?php
		return ob_get_clean() . $content;
	}
}
add_filter( 'the_content', 'nadlan_pjx_top', 7 );

/* ---------------- 2+3+4: selector + map + world (after the engine + article) ---------------- */
if ( ! function_exists( 'nadlan_pjx_bottom' ) ) {
	function nadlan_pjx_bottom( $content ) {
		if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
		if ( function_exists( 'nadlan_unit_journey_is_private_lab' ) && nadlan_unit_journey_is_private_lab( get_the_ID() ) ) { return $content; }
		$id  = get_the_ID();
		$g   = function ( $k ) use ( $id ) { return get_post_meta( $id, $k, true ); };
		$ppsqm = (int) $g( 'project_3d_avg_price_per_sqm' );
		$lat = (float) $g( 'lat' ); $lng = (float) $g( 'lng' );
		$dev = (string) $g( 'developer_name' );
		$city = (string) $g( 'city' );

		ob_start(); ?>
<div class="nlpjx" dir="rtl">

	<section class="nlpjx-sec" id="nlpjx-finance" aria-label="מימון וליווי">
		<h2>מימון, ייעוץ ועיצוב - הכל במקום אחד</h2>
		<div class="nlpjx-fin">
			<?php if ( $ppsqm ) :
				$est = $ppsqm * 90 * 0.75 * ( 0.05 / 12 ) / ( 1 - pow( 1 + 0.05 / 12, -360 ) );
				$lo  = (int) round( $est * 0.9, -2 );
				$hi  = (int) round( $est * 1.1, -2 );
			?>
			<div class="nlpjx-fin-est"><b><?php echo number_format( $lo ) . '-' . number_format( $hi ); ?> ₪</b><span>סדר גודל של החזר חודשי לדירת ~90 מ״ר. אומדן לא מחייב, תלוי במסלול ובריבית.</span>
				<a href="<?php echo esc_url( home_url( '/mortgage-calculator/' ) ); ?>">לחישוב אישי במחשבון המשכנתא ←</a></div>
			<?php endif; ?>
			<?php
			$advisors = new WP_Query( array( 'post_type' => 'nadlan_professional', 'post_status' => 'publish', 'posts_per_page' => 3, 'no_found_rows' => true, 'fields' => 'ids',
				'meta_query' => array( array( 'key' => 'profession', 'value' => array( 'mashkanta', 'accountant', 'lawyer' ), 'compare' => 'IN' ), array( 'key' => 'paid_tier', 'value' => array( 'pro', 'premier' ), 'compare' => 'IN' ) ) ) );
			if ( $advisors->posts ) : ?>
			<div class="nlpjx-pros">
				<?php foreach ( $advisors->posts as $aid ) : $apm = function_exists( 'nadlan_prof_meta_of' ) ? nadlan_prof_meta_of( get_post_meta( $aid, 'profession', true ) ) : array( 'label' => '', 'color' => '#1B1A17' ); ?>
				<a class="nlpjx-pro" href="<?php echo esc_url( get_permalink( $aid ) ); ?>">
					<?php echo function_exists( 'nadlan_prof_monogram_svg' ) ? nadlan_prof_monogram_svg( get_the_title( $aid ), $apm['color'] ) : ''; // phpcs:ignore ?>
					<b><?php echo esc_html( get_the_title( $aid ) ); ?></b><span><?php echo esc_html( $apm['label'] ); ?> · מלווה רוכשים בפרויקטים</span>
				</a>
				<?php endforeach; ?>
			</div>
			<?php endif; ?>
		</div>
	</section>

	<?php
	$designers = new WP_Query( array( 'post_type' => 'nadlan_professional', 'post_status' => 'publish', 'posts_per_page' => 3, 'no_found_rows' => true, 'fields' => 'ids',
		'meta_query' => array( array( 'key' => 'profession', 'value' => 'interior_designer' ), array( 'key' => 'paid_tier', 'value' => array( 'pro', 'premier' ), 'compare' => 'IN' ) ) ) );
	if ( $designers->posts ) : ?>
	<section class="nlpjx-sec" id="nlpjx-design" aria-label="עיצוב פנים">
		<h2>קניתם? עצבו את הדירה עוד לפני הכניסה</h2>
		<p class="nlpjx-cap">מעצבי פנים מומלצים שעובדים עם דירות קבלן - מתוכנית המכר ועד דירה מוכנה.</p>
		<div class="nlpjx-pros">
			<?php foreach ( $designers->posts as $did ) : ?>
			<a class="nlpjx-pro" href="<?php echo esc_url( get_permalink( $did ) ); ?>">
				<?php echo function_exists( 'nadlan_prof_monogram_svg' ) ? nadlan_prof_monogram_svg( get_the_title( $did ), '#9F6F54' ) : ''; // phpcs:ignore ?>
				<b><?php echo esc_html( get_the_title( $did ) ); ?></b><span>מעצב/ת פנים · <?php echo esc_html( get_post_meta( $did, 'city', true ) ); ?></span>
			</a>
			<?php endforeach; ?>
		</div>
	</section>
	<?php endif; ?>

	<?php if ( $lat && $lng ) :
		$pois = function_exists( 'nadlan_poi_fetch' ) ? nadlan_poi_fetch( $lat, $lng, 1200 ) : array();
		$poi_json = wp_json_encode( array_map( function ( $grp ) {
			return array_values( array_filter( array_slice( (array) $grp, 0, 16 ), function ( $i ) { return ! empty( $i['lat'] ) && ! empty( $i['lng'] ); } ) );
		}, (array) $pois ) );
		$near = nadlan_pjx_nearby_projects( $id, $lat, $lng );
		// This section sits right under the 3D theater on every language sibling,
		// so its labels are localized by the page's own language (slug suffix).
		$mlang = 'he';
		foreach ( array( 'en', 'fr', 'ru', 'ar' ) as $ml ) {
			if ( substr( get_post_field( 'post_name', $id ), -3 ) === '-' . $ml ) { $mlang = $ml; }
		}
		$MT = array(
			'he' => array( 'aria' => 'מפה חיה של הסביבה', 'h' => 'הכל על מפה אחת: מחירים, סביבה, תוכניות עתידיות', 'layers' => 'שכבות מפה', 'comps' => '₪ מחירים בסביבה', 'schools' => '🏫 חינוך', 'parks' => '🌳 פארקים', 'food' => '☕ קפה ומסעדות', 'transit' => '🚌 תחבורה', 'shops' => '🛒 קניות', 'health' => '⚕️ בריאות', 'plans' => '◆ תוכניות עתידיות', 'd3' => '🏙️ תלת ממד', 'sat' => '🛰️ לוויין', 'cap' => 'לחצו על כל סימון לקבלת פרטים. תגי המחיר הם אומדן לא מחייב למ״ר בפרויקטים סמוכים.', 'purple' => '◆ סגול = תוכניות התחדשות ופרויקטים עתידיים' ),
			'en' => array( 'aria' => 'Live area map', 'h' => 'Everything on one map: prices, surroundings, future plans', 'layers' => 'Map layers', 'comps' => '₪ Nearby prices', 'schools' => '🏫 Education', 'parks' => '🌳 Parks', 'food' => '☕ Cafes', 'transit' => '🚌 Transit', 'shops' => '🛒 Shopping', 'health' => '⚕️ Health', 'plans' => '◆ Future plans', 'd3' => '🏙️ 3D', 'sat' => '🛰️ Satellite', 'cap' => 'Click any marker for details. Price tags are non-binding per-sqm estimates in nearby projects.', 'purple' => '◆ purple = urban renewal and future projects' ),
			'fr' => array( 'aria' => 'Carte interactive du quartier', 'h' => 'Tout sur une seule carte: prix, environnement, plans futurs', 'layers' => 'Couches de carte', 'comps' => '₪ Prix a proximite', 'schools' => '🏫 Education', 'parks' => '🌳 Parcs', 'food' => '☕ Cafes', 'transit' => '🚌 Transports', 'shops' => '🛒 Commerces', 'health' => '⚕️ Sante', 'plans' => '◆ Plans futurs', 'd3' => '🏙️ 3D', 'sat' => '🛰️ Satellite', 'cap' => 'Cliquez sur un marqueur pour les details. Les etiquettes de prix sont des estimations indicatives au m2 dans les projets voisins.', 'purple' => '◆ violet = renouvellement urbain et projets futurs' ),
			'ru' => array( 'aria' => 'Живая карта района', 'h' => 'Все на одной карте: цены, окружение, будущие проекты', 'layers' => 'Слои карты', 'comps' => '₪ Цены рядом', 'schools' => '🏫 Образование', 'parks' => '🌳 Парки', 'food' => '☕ Кафе', 'transit' => '🚌 Транспорт', 'shops' => '🛒 Магазины', 'health' => '⚕️ Здоровье', 'plans' => '◆ Будущие проекты', 'd3' => '🏙️ 3D', 'sat' => '🛰️ Спутник', 'cap' => 'Нажмите на любой маркер для подробностей. Ценовые метки - необязывающая оценка за кв.м в соседних проектах.', 'purple' => '◆ фиолетовый = городское обновление и будущие проекты' ),
			'ar' => array( 'aria' => 'خريطة حية للمنطقة', 'h' => 'كل شيء على خريطة واحدة: الأسعار والمحيط والخطط المستقبلية', 'layers' => 'طبقات الخريطة', 'comps' => '₪ الأسعار القريبة', 'schools' => '🏫 التعليم', 'parks' => '🌳 حدائق', 'food' => '☕ مقاهي', 'transit' => '🚌 المواصلات', 'shops' => '🛒 التسوق', 'health' => '⚕️ الصحة', 'plans' => '◆ الخطط المستقبلية', 'd3' => '🏙️ ثلاثي الأبعاد', 'sat' => '🛰️ قمر صناعي', 'cap' => 'انقر على أي علامة للتفاصيل. علامات الأسعار تقديرات غير ملزمة للمتر المربع في المشاريع المجاورة.', 'purple' => '◆ البنفسجي = التجديد الحضري والمشاريع المستقبلية' ),
		);
		$mt = $MT[ $mlang ];
	?>
	<?php $unimap = function_exists( 'nadlan_mapbox_token' ) ? nadlan_mapbox_token() : ''; ?>
	<section id="nlpjx-map" class="nlpjx-sec" aria-label="<?php echo esc_attr( $mt['aria'] ); ?>">
		<h2><?php echo esc_html( $mt['h'] ); ?></h2>
		<?php if ( $unimap ) : ?>
		<div class="nlpjx-maplayers" role="group" aria-label="<?php echo esc_attr( $mt['layers'] ); ?>">
			<button type="button" class="is-on" data-layer="comps"><?php echo esc_html( $mt['comps'] ); ?></button>
			<button type="button" class="is-on" data-layer="schools"><?php echo esc_html( $mt['schools'] ); ?></button>
			<button type="button" class="is-on" data-layer="parks"><?php echo esc_html( $mt['parks'] ); ?></button>
			<button type="button" data-layer="transit"><?php echo esc_html( $mt['transit'] ); ?></button>
			<button type="button" data-layer="shops"><?php echo esc_html( $mt['shops'] ); ?></button>
			<button type="button" data-layer="health"><?php echo esc_html( $mt['health'] ); ?></button>
			<button type="button" data-layer="food"><?php echo esc_html( $mt['food'] ); ?></button>
			<button type="button" class="is-on" data-layer="plans"><?php echo esc_html( $mt['plans'] ); ?></button>
			<button type="button" data-layer="3d"><?php echo esc_html( $mt['d3'] ); ?></button>
			<button type="button" data-layer="sat"><?php echo esc_html( $mt['sat'] ); ?></button>
		</div>
		<div id="nlpjx-unimap" data-token="<?php echo esc_attr( $unimap ); ?>" data-lat="<?php echo esc_attr( $lat ); ?>" data-lng="<?php echo esc_attr( $lng ); ?>" data-title="<?php echo esc_attr( get_the_title( $id ) ); ?>"></div>
		<?php else : ?>
		<div id="nlpjx-leaflet" data-lat="<?php echo esc_attr( $lat ); ?>" data-lng="<?php echo esc_attr( $lng ); ?>" data-title="<?php echo esc_attr( get_the_title( $id ) ); ?>"></div>
		<?php endif; ?>
		<script>window.NLPJX_POIS=<?php echo $poi_json ?: '{}'; // phpcs:ignore ?>;window.NLPJX_PLANS=<?php echo wp_json_encode( $near ); // phpcs:ignore ?>;</script>
		<p class="nlpjx-cap"><?php echo esc_html( $mt['cap'] ); ?> <b style="color:#6B4FA0"><?php echo esc_html( $mt['purple'] ); ?></b>.</p>
	</section>
	<?php endif; ?>

	<?php if ( function_exists( 'nadlan_sdedov_tour_band' ) && in_array( get_post_field( 'post_name', $id ), nadlan_sdedov_tour_slugs(), true ) ) :
		echo nadlan_sdedov_tour_band( 'project', nadlan_sdedov_tour_focus( get_post_field( 'post_name', $id ) ) ); // phpcs:ignore
	endif; ?>

	<section id="nlpjx-world" class="nlpjx-sec" aria-label="כל המידע סביב הפרויקט">
		<h2>כל מה שסביב הפרויקט</h2>
		<div class="nlpjx-world">
			<?php if ( $dev ) : ?><a href="<?php echo esc_url( home_url( '/professionals/?q=' . rawurlencode( $dev ) ) ); ?>"><b>היזם: <?php echo esc_html( $dev ); ?></b><span>פרופיל, רישום ופרויקטים נוספים ←</span></a><?php endif; ?>
			<a href="<?php echo esc_url( home_url( '/professionals/' . ( $city ? '?city=' . rawurlencode( $city ) : '' ) ) ); ?>"><b>בעלי מקצוע<?php echo $city ? ' ב' . esc_html( $city ) : ''; ?></b><span>עו״ד מקרקעין, שמאים, בדק בית ←</span></a>
			<a href="<?php echo esc_url( home_url( '/mortgage-calculator/' ) ); ?>"><b>מחשבון משכנתא</b><span>כמה תשלמו בחודש ←</span></a>
			<a href="<?php echo esc_url( home_url( '/purchase-tax-calculator/' ) ); ?>"><b>מס רכישה</b><span>מדרגות 2026 ומחשבון ←</span></a>
			<a href="<?php echo esc_url( home_url( '/buying-apartment/' ) ); ?>"><b>מדריך קנייה מקבלן</b><span>שלב-אחר-שלב, ערבויות חוק מכר ←</span></a>
			<a href="<?php echo esc_url( home_url( '/glossary/' ) ); ?>"><b>מילון מונחים</b><span>תמ״א, פינוי-בינוי, הערת אזהרה ←</span></a>
		</div>
	</section>
</div>
<?php
		return $content . ob_get_clean();
	}
}
add_filter( 'the_content', 'nadlan_pjx_bottom', 19 );

/* ---------------- assets ---------------- */
if ( ! function_exists( 'nadlan_pjx_assets' ) ) {
	function nadlan_pjx_assets() {
		if ( ! is_singular( 'nadlan_project' ) ) { return; }
		if ( function_exists( 'nadlan_unit_journey_is_private_lab' ) && nadlan_unit_journey_is_private_lab() ) { return; }
		$id = get_queried_object_id();
		$has_map = get_post_meta( $id, 'lat', true ) && get_post_meta( $id, 'lng', true );
		if ( $has_map ) {
			wp_enqueue_style( 'leaflet', 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css', array(), '1.9.4' );
			wp_enqueue_script( 'leaflet', 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js', array(), '1.9.4', true );
		}
		wp_register_style( 'nadlan-pjx', false );
		wp_enqueue_style( 'nadlan-pjx' );
		wp_add_inline_style( 'nadlan-pjx', '
.nlpjx-nav{position:sticky;top:0;z-index:60;display:flex;gap:6px;overflow-x:auto;-webkit-overflow-scrolling:touch;background:rgba(250,248,243,.96);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);border-bottom:1px solid #E2DCD0;padding:10px 14px;margin:0 -20px 14px;scrollbar-width:none}
.nlpjx-nav::-webkit-scrollbar{display:none}
.nlpjx-nav a{flex-shrink:0;font-size:13.5px;font-weight:600;color:#1B1A17;text-decoration:none;border:1px solid #E2DCD0;background:#fff;border-radius:999px;padding:8px 16px;min-height:38px;display:inline-flex;align-items:center}
.nlpjx-nav a:hover,.nlpjx-nav a:focus-visible{border-color:#9C7A3C;color:#9C7A3C}
.nlpjx-intro p{font-size:14.5px;color:#6D665C;margin:0 0 18px;line-height:1.6}
.nlpjx{font-family:var(--font-sans,Heebo,system-ui,sans-serif);color:#1B1A17}
.nlpjx-sec{border:1px solid #E2DCD0;border-radius:12px;background:#FFFDFC;padding:20px;margin:0 0 20px;box-shadow:0 1px 2px rgba(17,17,15,.04)}
.nlpjx-sec h2{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:1.35rem;margin:0 0 8px}
.nlpjx-cap{font-size:12.5px;color:#6D665C;margin:0 0 14px}
#nlpjx-leaflet{height:340px;border-radius:10px;border:1px solid #E2DCD0}
.nlpjx-price-grid{display:grid;grid-template-columns:1.1fr 1fr;gap:18px;align-items:start}
@media(max-width:760px){.nlpjx-price-grid{grid-template-columns:1fr}}
.nlpjx-price-cards{display:flex;flex-direction:column;gap:12px}
.nlpjx-price-card{border:1px solid #E2DCD0;border-radius:10px;background:#FAF8F3;padding:16px}
.nlpjx-price-card b{display:block;font-family:var(--font-serif,serif);font-size:1.5rem}
.nlpjx-price-card span{display:block;font-size:12px;color:#6D665C;margin-top:4px}
.nlpjx-comps{width:100%;border-collapse:collapse;font-size:13.5px;background:#fff;border:1px solid #E2DCD0;border-radius:10px;overflow:hidden}
.nlpjx-comps caption{caption-side:top;text-align:start;font-size:11.5px;color:#6D665C;padding:0 2px 6px}
.nlpjx-comps th,.nlpjx-comps td{text-align:start;padding:9px 12px;border-bottom:1px solid #EFE9DD}
.nlpjx-comps th{font-size:11.5px;color:#6D665C;font-weight:600;background:#FAF8F3}
.nlpjx-comps tr:last-child td{border-bottom:0}
.nlpjx-comps a{color:#1B1A17;text-decoration:none;font-weight:600}
.nlpjx-comps a:hover{color:#9C7A3C}
#nlpjx-unimap{height:440px;border-radius:12px;border:1px solid #E2DCD0;background:#F3EEE3}
#nlpjx-map.nl-adopted-map{max-width:1240px;margin:0 auto 20px;box-sizing:border-box}
.nlpjx-maplayers{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 10px}
.nlpjx-maplayers button{font:600 12.5px/1 Heebo,sans-serif;border:1px solid #E2DCD0;background:#fff;color:#6D665C;border-radius:999px;padding:8px 13px;cursor:pointer;min-height:34px}
.nlpjx-maplayers button.is-on{background:#1B1A17;border-color:#1B1A17;color:#F4EEDE}
.nlpjx-price-mapnote{margin-top:10px}
.nlpjx-price-mapnote a{font-size:13px;font-weight:700;color:#9C7A3C;text-decoration:none}
.nlpjx-world{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.nlpjx-world a{display:block;border:1px solid #E2DCD0;border-radius:10px;background:#FAF8F3;padding:14px 16px;text-decoration:none;color:#1B1A17;transition:border-color .2s,transform .2s;min-height:64px}
.nlpjx-world a:hover{border-color:#9C7A3C;transform:translateY(-2px)}
.nlpjx-world b{display:block;font-size:14px}
.nlpjx-fin{display:flex;flex-wrap:wrap;gap:14px;align-items:stretch}
.nlpjx-fin-est{flex:1;min-width:220px;border:1px solid #E2DCD0;border-radius:10px;background:#FAF8F3;padding:16px}
.nlpjx-fin-est b{display:block;font-family:var(--font-serif,serif);font-size:1.5rem}
.nlpjx-fin-est span{display:block;font-size:11.5px;color:#6D665C;margin:4px 0 8px}
.nlpjx-fin-est a{color:#9C7A3C;font-size:13px;font-weight:700;text-decoration:none}
.nlpjx-pros{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;flex:2}
.nlpjx-pro{display:flex;align-items:center;gap:10px;border:1px solid #E2DCD0;border-radius:10px;background:#FFFDFC;padding:10px 12px;text-decoration:none;color:#1B1A17;transition:border-color .2s}
.nlpjx-pro:hover{border-color:#9C7A3C}
.nlpjx-pro svg{width:44px;height:44px;flex-shrink:0}
.nlpjx-pro b{display:block;font-size:13.5px;line-height:1.2}
.nlpjx-pro span{font-size:11px;color:#6D665C}
.nlpjx-world span{font-size:12px;color:#6D665C}
' );
		wp_register_script( 'nadlan-pjx-js', false, $has_map ? array( 'leaflet' ) : array(), '1.69.85', true );
		wp_enqueue_script( 'nadlan-pjx-js' );
		wp_add_inline_script( 'nadlan-pjx-js', '
(function(){
document.addEventListener("DOMContentLoaded",function(){
	// LAYOUT (v1.72.0): the ENGINE adopts #nlpjx-map right under the theater and
	// hides its own plain map after it renders - moving/hiding from here raced
	// the engine (it renders after DOMContentLoaded) and left TWO maps live.
	// smooth section nav
	document.querySelectorAll(".nlpjx-nav a").forEach(function(a){
		a.addEventListener("click",function(e){
			var t=document.querySelector(a.getAttribute("href"));
			if(t){e.preventDefault();t.scrollIntoView({behavior:"smooth",block:"start"})}
		});
	});
	// UNIFIED MAP (owner 2026-07-02): one Mapbox map = price pills (Booking-style),
	// POI layers, future plans, satellite and 3D buildings. Lazy: GL loads only
	// when the map nears the viewport. Chips toggle marker groups/layers.
	var um=document.getElementById("nlpjx-unimap");
	if(um&&"IntersectionObserver" in window){
		var umDone=false;
		new IntersectionObserver(function(en,obs){
			if(!en[0].isIntersecting||umDone){return}
			umDone=true;obs.disconnect();
			function boot(){
				if(!window.mapboxgl){return}
				mapboxgl.accessToken=um.dataset.token;
				var lat=parseFloat(um.dataset.lat),lng=parseFloat(um.dataset.lng);
				var map=new mapboxgl.Map({container:um,style:"mapbox://styles/mapbox/light-v11",center:[lng,lat],zoom:14.4,pitch:0,attributionControl:true,cooperativeGestures:true,locale:{"CooperativeGesturesHandler.WindowsHelpText":"\u05dc\u05d7\u05e6\u05d5 Ctrl \u05d5\u05d2\u05dc\u05dc\u05d5 \u05db\u05d3\u05d9 \u05dc\u05d4\u05ea\u05e7\u05e8\u05d1 \u05d1\u05de\u05e4\u05d4","CooperativeGesturesHandler.MacHelpText":"\u05dc\u05d7\u05e6\u05d5 \u2318 \u05d5\u05d2\u05dc\u05dc\u05d5 \u05db\u05d3\u05d9 \u05dc\u05d4\u05ea\u05e7\u05e8\u05d1 \u05d1\u05de\u05e4\u05d4","TouchPanBlocker.Message":"\u05d4\u05d6\u05d9\u05d6\u05d5 \u05d0\u05ea \u05d4\u05de\u05e4\u05d4 \u05d1\u05e9\u05ea\u05d9 \u05d0\u05e6\u05d1\u05e2\u05d5\u05ea"}});
				map.on("style.load",function(){try{map.setPaintProperty("water","fill-color","#A9C6D0")}catch(e){}try{map.setPaintProperty("land","background-color","#F6F1E6")}catch(e){}});
				map.addControl(new mapboxgl.NavigationControl({visualizePitch:true}));
				window.NLPJX_MAP=map; // engine syncs model orbit -> map bearing through this handle
				try{document.dispatchEvent(new CustomEvent("nlpjx:map"))}catch(e){}
				var groups={comps:[],schools:[],parks:[],transit:[],shops:[],health:[],food:[],plans:[]};
				function pop(html){return new mapboxgl.Popup({offset:14,maxWidth:"260px"}).setHTML(html)}
				function dot(color){var e=document.createElement("div");e.style.cssText="width:15px;height:15px;border-radius:50%;background:"+color+";border:2.5px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.35);cursor:pointer";return e}
				// the project itself
				var home=document.createElement("div");home.style.cssText="width:20px;height:20px;border-radius:50%;background:#C2563A;border:3px solid #fff;box-shadow:0 2px 10px rgba(0,0,0,.4)";
				new mapboxgl.Marker({element:home}).setLngLat([lng,lat]).setPopup(pop("<b>"+um.dataset.title+"</b><br>הפרויקט שבעמוד")).addTo(map);
				// price pills for comparable projects
				var compsEl=document.getElementById("nlpjx-comps-data"),comps=[];
				try{comps=JSON.parse(compsEl?compsEl.textContent:"[]")}catch(e){}
				comps.forEach(function(c){
					if(!c.lat||!c.lng){return}
					var el=document.createElement("div");el.style.cssText="min-width:46px;padding:4px 8px;border-radius:8px;background:#1B1A17;color:#E6D4AE;font:700 11.5px/1.3 Heebo,sans-serif;text-align:center;border:1px solid #9C7A3C;cursor:pointer;box-shadow:0 3px 10px rgba(0,0,0,.3)";
					el.textContent="₪"+Math.round(c.ppsqm/1000)+"K";
					groups.comps.push(new mapboxgl.Marker({element:el}).setLngLat([c.lng,c.lat]).setPopup(pop("<b>"+c.name+"</b><br>אומדן ~"+Number(c.ppsqm).toLocaleString()+" ₪/מ\"ר · לא מחייב<br><a href=\""+c.url+"\">לעמוד הפרויקט ←</a>")));
				});
				// POIs by layer
				var P=window.NLPJX_POIS||{};
				var poiStyle={schools:["#334236","🏫 "],kindergartens:["#334236","🧒 "],parks:["#517048","🌳 "],transit:["#183C3C","🚌 "],shops:["#9F6F54","🛒 "],health:["#A93F2A","⚕️ "],food:["#8A6B3F","☕ "]};
				Object.keys(P).forEach(function(k){
					var g=(k==="kindergartens")?"schools":k;
					if(!groups[g]){return}
					(P[k]||[]).forEach(function(pt){
						if(!pt.lat||!pt.lng){return}
						var st=poiStyle[k]||["#666",""];
						var dtxt=pt.d?(pt.d>=1000?("<br><span style=\"color:#9C7A3C;font-size:12px\">כ-"+(Math.round(pt.d/100)/10)+" ק\"מ מהפרויקט</span>"):("<br><span style=\"color:#9C7A3C;font-size:12px\">כ-"+(Math.max(50,Math.round(pt.d/50)*50))+" מטר מהפרויקט</span>")):"";groups[g].push(new mapboxgl.Marker({element:dot(st[0])}).setLngLat([pt.lng,pt.lat]).setPopup(pop("<b>"+st[1]+(pt.name||"")+"</b>"+dtxt)));
					});
				});
				// future plans (purple)
				(window.NLPJX_PLANS||[]).forEach(function(pl){
					if(!pl.lat||!pl.lng){return}
					var e=dot("#6B4FA0");e.style.width="17px";e.style.height="17px";
					groups.plans.push(new mapboxgl.Marker({element:e}).setLngLat([pl.lng,pl.lat]).setPopup(pop("◆ <b>"+pl.name+"</b><br><a href=\""+pl.url+"\">לפרטי התוכנית ←</a>")));
				});
				var on={comps:true,schools:true,parks:true,transit:false,shops:false,health:false,food:false,plans:true};
				function apply(k){(groups[k]||[]).forEach(function(m){on[k]?m.addTo(map):m.remove()})}
				Object.keys(groups).forEach(apply);
				// live counts on every chip; a chip with nothing behind it says (0) and greys out
				document.querySelectorAll(".nlpjx-maplayers button").forEach(function(b){
					var k=b.dataset.layer;
					if(!(k in groups)){return}
					var n=groups[k].length;
					b.textContent=b.textContent.replace(/\s*\(\d+\)$/,"")+" ("+n+")";
					if(!n){b.style.opacity=".45";b.classList.remove("is-on")}
				});
				// 3D buildings + satellite, added after style load
				map.on("load",function(){
					map.addSource("nl-sat",{type:"raster",tiles:["https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.jpg90?access_token="+mapboxgl.accessToken],tileSize:256});
					map.addLayer({id:"nl-sat",type:"raster",source:"nl-sat",layout:{visibility:"none"}});
					var labelLayer;(map.getStyle().layers||[]).forEach(function(l){if(!labelLayer&&l.type==="symbol"&&l.layout&&l.layout["text-field"]){labelLayer=l.id}});
					map.addLayer({id:"nl-3d",source:"composite","source-layer":"building",filter:["==","extrude","true"],type:"fill-extrusion",minzoom:14,
						layout:{visibility:"none"},
						paint:{"fill-extrusion-color":"#d8d2c4","fill-extrusion-height":["get","height"],"fill-extrusion-base":["get","min_height"],"fill-extrusion-opacity":.75}},labelLayer);
				});
				document.querySelectorAll(".nlpjx-maplayers button").forEach(function(b){
					b.addEventListener("click",function(){
						var k=b.dataset.layer;
						if(k==="3d"){
							var v=map.getLayoutProperty("nl-3d","visibility")==="visible";
							map.setLayoutProperty("nl-3d","visibility",v?"none":"visible");
							map.easeTo({pitch:v?0:58,zoom:v?14.4:15.6,duration:900});
							b.classList.toggle("is-on",!v);return;
						}
						if(k==="sat"){
							var sv=map.getLayoutProperty("nl-sat","visibility")==="visible";
							map.setLayoutProperty("nl-sat","visibility",sv?"none":"visible");
							b.classList.toggle("is-on",!sv);return;
						}
						on[k]=!on[k];apply(k);b.classList.toggle("is-on",on[k]);
					});
				});
			}
			if(window.mapboxgl){boot();return}
			var l=document.createElement("link");l.rel="stylesheet";l.href="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css";document.head.appendChild(l);
			var s=document.createElement("script");s.src="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js";s.onload=boot;document.head.appendChild(s);
		},{rootMargin:"300px"}).observe(um);
	}
	// live map: streets/satellite, POIs, future-plans purple markers
	var m=document.getElementById("nlpjx-leaflet");
	if(m&&window.L){
		var lat=parseFloat(m.dataset.lat),lng=parseFloat(m.dataset.lng);
		var streets=L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png",{attribution:"&copy; OpenStreetMap"});
		var sat=L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",{attribution:"Esri"});
		var map=L.map(m,{scrollWheelZoom:false,layers:[streets]}).setView([lat,lng],15);
		L.control.layers({"מפה":streets,"לוויין":sat},null,{position:"topleft"}).addTo(map);
		L.marker([lat,lng]).addTo(map).bindPopup("<b>"+(m.dataset.title||"")+"</b>").openPopup();
		var P=window.NLPJX_POIS||{},style={schools:["#334236","🏫"],kindergartens:["#9C7A3C","🧒"],parks:["#517048","🌳"],transit:["#183C3C","🚌"],shops:["#9F6F54","🛒"],health:["#A93F2A","⚕️"],food:["#8A6B3F","☕"]};
		Object.keys(P).forEach(function(k){(P[k]||[]).forEach(function(p){
			if(!p.lat||!p.lng){return}
			L.circleMarker([p.lat,p.lng],{radius:6,color:(style[k]||["#666"])[0],weight:2,fillColor:"#fff",fillOpacity:.9}).addTo(map).bindPopup((style[k]?style[k][1]+" ":"")+(p.name||""));
		})});
		(window.NLPJX_PLANS||[]).forEach(function(p){
			if(!p.lat||!p.lng){return}
			L.circleMarker([p.lat,p.lng],{radius:8,color:"#6B4FA0",weight:2.5,fillColor:"#EBE4F5",fillOpacity:.95}).addTo(map)
				.bindPopup("◆ <b>"+p.name+"</b><br><a href=\""+p.url+"\">לפרטי הפרויקט ←</a>");
		});
	}
});
})();
' );
	}
}
add_action( 'wp_enqueue_scripts', 'nadlan_pjx_assets' );

/* ---------------- SEO: FAQPage JSON-LD + meta description for projects ---------------- */
if ( ! function_exists( 'nadlan_pjx_faq_jsonld' ) ) {
	function nadlan_pjx_faq_jsonld() {
		/* Source-audit 30.8.2026: retired. schema.php emits FAQPage from the real,
		 * visible project_faq_json; this synthetic invisible block doubled the
		 * schema on pages with a real FAQ and risks the rich-results policy. */
		return;
		if ( ! is_singular( 'nadlan_project' ) ) { return; }
		if ( function_exists( 'nadlan_unit_journey_is_private_lab' ) && nadlan_unit_journey_is_private_lab() ) { return; }
		$id = get_queried_object_id();
		$g  = function ( $k ) use ( $id ) { return get_post_meta( $id, $k, true ); };
		$name = get_the_title( $id ); $qa = array();
		if ( $g( 'developer_name' ) ) { $qa[] = array( 'מי היזם של ' . $name . '?', 'היזם הוא ' . $g( 'developer_name' ) . '. פרטי הרישום המלאים מופיעים בעמוד הפרויקט.' ); }
		if ( (int) $g( 'project_3d_avg_price_per_sqm' ) ) { $qa[] = array( 'מה מחיר למ״ר ב' . $name . '?', 'אומדן לא מחייב: כ-' . number_format( (int) $g( 'project_3d_avg_price_per_sqm' ) ) . ' ₪ למ״ר. יש לאמת מול היזם.' ); }
		if ( (int) $g( 'num_floors' ) || (int) $g( 'num_units' ) ) { $qa[] = array( 'כמה קומות ודירות יש בפרויקט?', trim( ( (int) $g( 'num_floors' ) ? (int) $g( 'num_floors' ) . ' קומות' : '' ) . ' ' . ( (int) $g( 'num_units' ) ? 'ו-' . (int) $g( 'num_units' ) . ' יחידות דיור' : '' ) ) . '.' ); }
		$qa[] = array( 'איך בוחרים דירה בפרויקט?', 'בעמוד זה: סיור בהדמיה, בחירת קומה ודירה, מפת סביבה חיה עם מוסדות חינוך ותחבורה, ופנייה ישירה בוואטסאפ או בטלפון.' );
		$items = array();
		foreach ( $qa as $x ) { $items[] = array( '@type' => 'Question', 'name' => $x[0], 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $x[1] ) ); }
		echo '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => $items ), JSON_UNESCAPED_UNICODE ) . '</script>' . "\n";
	}
}
add_action( 'wp_head', 'nadlan_pjx_faq_jsonld', 30 );

if ( ! function_exists( 'nadlan_pjx_meta_desc' ) ) {
	function nadlan_pjx_meta_desc( $desc ) {
		if ( ! is_singular( 'nadlan_project' ) ) { return $desc; }
		if ( function_exists( 'nadlan_unit_journey_is_private_lab' ) && nadlan_unit_journey_is_private_lab() ) { return ''; }
		if ( $desc ) { return $desc; }
		$id = get_queried_object_id();
		$g  = function ( $k ) use ( $id ) { return get_post_meta( $id, $k, true ); };
		$bits = array( 'דירות למכירה ב' . get_the_title( $id ) . ( $g( 'city' ) ? ', ' . $g( 'city' ) : '' ) . '.' );
		if ( (int) $g( 'project_3d_avg_price_per_sqm' ) ) { $bits[] = 'אומדן ' . number_format( (int) $g( 'project_3d_avg_price_per_sqm' ) ) . ' ₪ למ״ר.'; }
		$bits[] = 'הדמיה, בחירת דירה, מפת סביבה ותוכניות עתידיות - בנדלן.';
		return mb_substr( implode( ' ', $bits ), 0, 156 );
	}
}
add_filter( 'wpseo_metadesc', 'nadlan_pjx_meta_desc', 25 );
