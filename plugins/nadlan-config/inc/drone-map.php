<?php
/**
 * nadlan-config - The projects map (design system ProjectMap v52, 28.9.2026; first built 2026-07-06).
 *
 * A Mapbox view of every located project. The country view is flat and legible: one circle
 * per city with its number of projects, and where cities touch at that scale one circle for
 * them all, named after the largest ("תל אביב יפו ועוד 11 ערים"). A tap dives in with pitch;
 * in the city every dot is a project with its name and its units. The projects with a 3D
 * model fly a pill on a stem; pills that would cover each other merge into one
 * ("4 פרויקטים בתלת־ממד") until the zoom separates them.
 *
 * HONESTY: only projects with real lat/lng meta appear (language siblings and private lab
 * projects excluded). A project located only at city level is counted in its city's circle
 * and is not drawn as a dot: a dot on the city centre would claim a location. No price on
 * the map: the per-m² figures are estimates. Lazy: Mapbox GL loads only when the band comes
 * near the viewport (or opens). No token -> no band.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_drone_map_data' ) ) {
	/** The map's payload, cached six hours: the REST route and the band's lead share it. */
	function nadlan_drone_map_data() {
		/* The cache key is part of the privacy boundary: an older aggregate
		 * may contain a lab project even after the query itself is hardened. */
		$cache = get_transient( 'nadlan_project_map_v3_public' );
		if ( is_array( $cache ) ) { return $cache; }
		$public_meta = function_exists( 'nadlan_unit_journey_public_meta_query' )
			? nadlan_unit_journey_public_meta_query()
			: array(
				'relation' => 'OR',
				array( 'key' => '_nadlan_private_unit_journey', 'compare' => 'NOT EXISTS' ),
				array(
					'key'     => '_nadlan_private_unit_journey',
					'value'   => 'private-unit-journey-v2',
					'compare' => '!=',
				),
			);
		$q = new WP_Query( array(
			'post_type' => 'nadlan_project', 'post_status' => 'publish',
			'posts_per_page' => -1, 'fields' => 'ids', 'no_found_rows' => true,
			'nadlan_no_lang_siblings' => true,
			'nadlan_private_visibility_applied' => true,
			'meta_query' => array( 'relation' => 'AND',
				array( 'key' => 'lat', 'compare' => 'EXISTS' ),
				array( 'key' => 'lng', 'compare' => 'EXISTS' ),
				$public_meta,
			),
		) );
		$items = array();
		foreach ( $q->posts as $id ) {
			$lat = (float) get_post_meta( $id, 'lat', true );
			$lng = (float) get_post_meta( $id, 'lng', true );
			if ( ! $lat || ! $lng ) { continue; }
			$items[] = array(
				'id' => $id, 'lat' => $lat, 'lng' => $lng,
				'title' => get_the_title( $id ),
				'url'   => get_permalink( $id ),
				'city'  => (string) get_post_meta( $id, 'city', true ),
				'conf'  => (string) get_post_meta( $id, 'geo_confidence', true ),
				'featured' => (bool) get_post_meta( $id, 'project_featured', true ),
				'poster'   => esc_url_raw( (string) get_post_meta( $id, 'project_model_poster', true ) ),
				'img'   => esc_url_raw( (string) get_post_meta( $id, 'project_3d_image', true ) ),
				// data-tag fuel (owner 2026-07-12): the map must shout data, not dots
				'units'  => (int) get_post_meta( $id, 'num_units', true ),
				'psqm'   => (float) get_post_meta( $id, 'project_3d_avg_price_per_sqm', true ),
				'status' => nadlan_drone_map_status_enum( $id ),
			);
		}
		$out = array( 'ok' => true, 'count' => count( $items ), 'items' => $items );
		set_transient( 'nadlan_project_map_v3_public', $out, 6 * HOUR_IN_SECONDS );
		return $out;
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/project-map', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function () {
			return new WP_REST_Response( nadlan_drone_map_data(), 200 );
		},
	) );
} );
add_action( 'save_post_nadlan_project', function () {
	delete_transient( 'nadlan_project_map_v2' );
	delete_transient( 'nadlan_project_map_v3_public' );
} );

if ( ! function_exists( 'nadlan_drone_map_status_enum' ) ) {
	// Normalize project_status (enum or gov.il Hebrew) to a known enum; fail open (empty).
	function nadlan_drone_map_status_enum( $id ) {
		$raw = trim( (string) get_post_meta( $id, 'project_status', true ) );
		if ( '' === $raw ) { return ''; }
		$map = array(
			'marketing' => 'marketing', 'construction' => 'construction', 'planning' => 'planning', 'completed' => 'completed',
			'בשיווק' => 'marketing', 'שיווק' => 'marketing',
			'בביצוע' => 'construction', 'בבנייה' => 'construction', 'ביצוע' => 'construction',
			'בתכנון' => 'planning', 'תכנון' => 'planning', 'מאושר' => 'planning',
			'הסתיים' => 'completed', 'אוכלס' => 'completed', 'הושלם' => 'completed',
		);
		return isset( $map[ $raw ] ) ? $map[ $raw ] : '';
	}
}

if ( ! function_exists( 'nadlan_drone_map_i18n' ) ) {
	function nadlan_drone_map_i18n( $lang ) {
		$T = array(
			'he' => array(
				'eyebrow' => 'על המפה', 'title' => 'מפת הפרויקטים',
				'lead' => '{n} מתוך {t} הפרויקטים בקטלוג מסומנים על המפה, ב־{c} ערים. כל עיגול הוא עיר, והמספר שבו הוא מספר הפרויקטים בה; לחיצה מקרבת, ושם כל נקודה היא פרויקט.',
				'lead_nt' => '{n} פרויקטים מסומנים על המפה, ב־{c} ערים. כל עיגול הוא עיר, והמספר שבו הוא מספר הפרויקטים בה; לחיצה מקרבת, ושם כל נקודה היא פרויקט.',
				'lg_city' => 'עיר ומספר הפרויקטים בה', 'lg_pt' => 'פרויקט, במיקום המתחם או החלקה', 'lg_3d' => 'פרויקט עם דגם תלת־ממד',
				'note' => 'פרויקט שמיקומו ידוע רק ברמת העיר נספר בעיגול של העיר ולא מסומן כנקודה.',
				'near' => 'פרויקטים לידי', 'toggle' => 'כל הקטלוג על המפה, עם הבניינים בתלת־ממד',
				'to_project' => 'לעמוד הפרויקט ←', 'city_level' => 'מיקום ברמת העיר',
				'group' => '{n} פרויקטים בתלת־ממד', 'city_k' => 'עיר', 'city_n' => '{n} פרויקטים בעיר', 'city_n1' => 'פרויקט אחד בעיר',
				'city_cl' => 'מתוכם {n} במיקום ברמת העיר בלבד', 'to_city' => 'לפרויקטים ב{city} ←',
				'more' => 'ועוד {k} ערים', 'more1' => 'ועוד עיר אחת',
			),
			'en' => array(
				'eyebrow' => 'On the map', 'title' => 'Project map',
				'lead' => '{n} of the {t} projects in the catalogue are on the map, in {c} cities. Each circle is a city with its number of projects; tap to zoom in, where each dot is a project.',
				'lead_nt' => '{n} projects are on the map, in {c} cities. Each circle is a city with its number of projects; tap to zoom in, where each dot is a project.',
				'lg_city' => 'A city and its number of projects', 'lg_pt' => 'A project, at its compound or parcel', 'lg_3d' => 'A project with a 3D model',
				'note' => 'A project located only at city level is counted in its city circle and is not shown as a dot.',
				'near' => 'Projects near me', 'toggle' => 'The whole catalogue on the map, with 3D buildings',
				'to_project' => 'To the project page →', 'city_level' => 'city-level location',
				'group' => '{n} projects in 3D', 'city_k' => 'City', 'city_n' => '{n} projects in the city', 'city_n1' => 'One project in the city',
				'city_cl' => '{n} of them located at city level only', 'to_city' => 'Projects in {city} →',
				'more' => '+{k} cities', 'more1' => '+1 city',
			),
			'fr' => array(
				'eyebrow' => 'Sur la carte', 'title' => 'La carte des projets',
				'lead' => '{n} des {t} projets du catalogue sont sur la carte, dans {c} villes. Chaque cercle est une ville avec son nombre de projets ; touchez pour zoomer, chaque point est alors un projet.',
				'lead_nt' => '{n} projets sont sur la carte, dans {c} villes. Chaque cercle est une ville avec son nombre de projets ; touchez pour zoomer, chaque point est alors un projet.',
				'lg_city' => 'Une ville et son nombre de projets', 'lg_pt' => 'Un projet, sur son îlot ou sa parcelle', 'lg_3d' => 'Un projet avec maquette 3D',
				'note' => 'Un projet localisé seulement au niveau de la ville est compté dans le cercle de la ville, sans point.',
				'near' => 'Projets près de moi', 'toggle' => 'Tout le catalogue sur la carte, avec les bâtiments en 3D',
				'to_project' => 'Vers la page du projet →', 'city_level' => 'localisation au niveau de la ville',
				'group' => '{n} projets en 3D', 'city_k' => 'Ville', 'city_n' => '{n} projets dans la ville', 'city_n1' => 'Un projet dans la ville',
				'city_cl' => 'dont {n} localisés au niveau de la ville', 'to_city' => 'Les projets à {city} →',
				'more' => '+{k} villes', 'more1' => '+1 ville',
			),
			'ru' => array(
				'eyebrow' => 'На карте', 'title' => 'Карта проектов',
				'lead' => '{n} из {t} проектов каталога отмечены на карте, в {c} городах. Каждый круг — город и число проектов в нём; нажмите, чтобы приблизить: там каждая точка — проект.',
				'lead_nt' => 'На карте {n} проектов, в {c} городах. Каждый круг — город и число проектов в нём; нажмите, чтобы приблизить: там каждая точка — проект.',
				'lg_city' => 'Город и число проектов в нём', 'lg_pt' => 'Проект, по участку или кварталу', 'lg_3d' => 'Проект с 3D-моделью',
				'note' => 'Проект, известный только с точностью до города, учтён в круге города и не показан точкой.',
				'near' => 'Проекты рядом со мной', 'toggle' => 'Весь каталог на карте, с 3D-зданиями',
				'to_project' => 'На страницу проекта →', 'city_level' => 'с точностью до города',
				'group' => '3D-проекты: {n}', 'city_k' => 'Город', 'city_n' => 'Проектов в городе: {n}', 'city_n1' => 'Один проект в городе',
				'city_cl' => 'из них {n} — с точностью до города', 'to_city' => 'Проекты: {city} →',
				'more' => '+{k} гор.', 'more1' => '+1 гор.',
			),
			'ar' => array(
				'eyebrow' => 'على الخريطة', 'title' => 'خريطة المشاريع',
				'lead' => '{n} من أصل {t} مشروعا في الدليل على الخريطة، في {c} مدينة. كل دائرة مدينة وعدد مشاريعها؛ اضغطوا للتقريب، وهناك كل نقطة مشروع.',
				'lead_nt' => '{n} مشروعا على الخريطة، في {c} مدينة. كل دائرة مدينة وعدد مشاريعها؛ اضغطوا للتقريب، وهناك كل نقطة مشروع.',
				'lg_city' => 'مدينة وعدد مشاريعها', 'lg_pt' => 'مشروع، في موقع المجمّع أو القسيمة', 'lg_3d' => 'مشروع بنموذج ثلاثي الأبعاد',
				'note' => 'المشروع المعروف موقعه على مستوى المدينة فقط يُحسب في دائرة المدينة ولا يظهر كنقطة.',
				'near' => 'مشاريع بالقرب مني', 'toggle' => 'الدليل كله على الخريطة، مع المباني ثلاثية الأبعاد',
				'to_project' => 'إلى صفحة المشروع ←', 'city_level' => 'موقع على مستوى المدينة',
				'group' => 'مشاريع ثلاثية الأبعاد: {n}', 'city_k' => 'مدينة', 'city_n' => 'مشاريع في المدينة: {n}', 'city_n1' => 'مشروع واحد في المدينة',
				'city_cl' => 'منها {n} على مستوى المدينة فقط', 'to_city' => 'المشاريع في {city} ←',
				'more' => 'و{k} أخرى', 'more1' => 'وواحدة أخرى',
			),
		);
		return isset( $T[ $lang ] ) ? $T[ $lang ] : $T['he'];
	}
}

if ( ! function_exists( 'nadlan_drone_map_tag_labels' ) ) {
	// Labels for the Google-style data tags on the pins (owner 2026-07-12).
	function nadlan_drone_map_tag_labels( $lang ) {
		$T = array(
			'he' => array( 'u' => 'יח״ד', 'sqm' => 'למ״ר', 'st' => array( 'marketing' => 'בשיווק', 'construction' => 'בבנייה', 'planning' => 'בתכנון', 'completed' => 'הושלם' ) ),
			'en' => array( 'u' => 'units', 'sqm' => '/sqm', 'st' => array( 'marketing' => 'Selling', 'construction' => 'Under construction', 'planning' => 'Planning', 'completed' => 'Completed' ) ),
			'fr' => array( 'u' => 'logements', 'sqm' => '/m2', 'st' => array( 'marketing' => 'Commercialisation', 'construction' => 'En construction', 'planning' => 'En planification', 'completed' => 'Livré' ) ),
			'ru' => array( 'u' => 'квартир', 'sqm' => 'за м2', 'st' => array( 'marketing' => 'Продажи', 'construction' => 'Строится', 'planning' => 'Проектируется', 'completed' => 'Сдан' ) ),
			'ar' => array( 'u' => 'وحدات', 'sqm' => 'للمتر', 'st' => array( 'marketing' => 'في التسويق', 'construction' => 'قيد البناء', 'planning' => 'في التخطيط', 'completed' => 'مكتمل' ) ),
		);
		return isset( $T[ $lang ] ) ? $T[ $lang ] : $T['he'];
	}
}

if ( ! function_exists( 'nadlan_drone_map_lead' ) ) {
	/** The band's lead with the real counts (the map's own payload and the catalogue's total); '' when the map is empty. */
	function nadlan_drone_map_lead( $lang = 'he' ) {
		$d = nadlan_drone_map_data();
		$items = isset( $d['items'] ) ? (array) $d['items'] : array();
		if ( ! $items ) { return ''; }
		$cities = array();
		foreach ( $items as $p ) {
			// one city, one count: a hyphen does not make a second city ("תל אביב-יפו" / "תל אביב יפו")
			$k = trim( preg_replace( '/\s+/u', ' ', str_replace( array( '-', '־', '–' ), ' ', (string) $p['city'] ) ) );
			if ( '' !== $k ) { $cities[ $k ] = 1; }
		}
		$f = function_exists( 'nadlan_dir_project_facets' ) ? nadlan_dir_project_facets() : array();
		$t = isset( $f['total'] ) ? (int) $f['total'] : 0;
		$L = nadlan_drone_map_i18n( $lang );
		return strtr( $t >= count( $items ) ? $L['lead'] : $L['lead_nt'], array(
			'{n}' => number_format( count( $items ) ), '{t}' => number_format( $t ), '{c}' => number_format( count( $cities ) ),
		) );
	}
}

if ( ! function_exists( 'nadlan_drone_map_band' ) ) {
	/**
	 * $mode 'toggle'   - collapsible band (projects catalog).
	 * $mode 'showcase' - always-visible designed band that boots itself when
	 *                    scrolled into view (homepage / premium). Same map.
	 * $args['head']    - false: the caller prints its own head (the Hebrew home's band head).
	 */
	function nadlan_drone_map_band( $mode = 'toggle', $lang = 'he', $args = array() ) {
		$token = trim( (string) get_option( 'nadlan_mapbox_token', '' ) );
		if ( $token === '' ) { return ''; }
		$rest = esc_url( rest_url( 'nadlan/v1/project-map' ) );
		$L    = nadlan_drone_map_i18n( $lang );
		$head = 'showcase' === $mode && ( ! isset( $args['head'] ) || false !== $args['head'] );
		$js   = array(
			'top' => $L['to_project'], 'city' => $L['city_level'], 'group' => $L['group'], 'cityK' => $L['city_k'],
			'cityN' => $L['city_n'], 'cityN1' => $L['city_n1'], 'cityCl' => $L['city_cl'], 'toCity' => $L['to_city'],
			'more' => $L['more'], 'more1' => $L['more1'], 'catalog' => home_url( '/projects/' ),
		);
		$lead = $head ? nadlan_drone_map_lead( $lang ) : '';
		ob_start(); ?>
<section class="nldrone nldrone--<?php echo esc_attr( $mode ); ?>" id="nldrone" data-mode="<?php echo esc_attr( $mode ); ?>" data-token="<?php echo esc_attr( $token ); ?>" data-rest="<?php echo esc_attr( $rest ); ?>" data-l="<?php echo esc_attr( wp_json_encode( $js, JSON_UNESCAPED_UNICODE ) ); ?>" data-l-x="<?php echo esc_attr( wp_json_encode( nadlan_drone_map_tag_labels( $lang ), JSON_UNESCAPED_UNICODE ) ); ?>">
	<?php if ( $head ) : ?>
	<div class="nldrone-head">
		<p class="nldrone-head__kicker"><?php echo esc_html( $L['eyebrow'] ); ?></p>
		<h2 class="nldrone-head__title"><?php echo esc_html( $L['title'] ); ?></h2>
		<?php if ( '' !== $lead ) : ?><p class="nldrone-head__sub"><?php echo esc_html( $lead ); ?></p><?php endif; ?>
	</div>
	<?php elseif ( 'toggle' === $mode ) : ?>
	<button type="button" class="nldrone-toggle" id="nldrone-toggle" aria-expanded="false" aria-controls="nldrone-stage">
		<span class="nldrone-toggle__ic" aria-hidden="true"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M9 4 3 6.5v13.5l6-2.5 6 2.5 6-2.5V4l-6 2.5z"/><path d="M9 4v13.5M15 6.5V20"/></svg></span>
		<span><?php echo esc_html( $L['toggle'] ); ?></span>
		<span class="nldrone-toggle__arrow" aria-hidden="true">▾</span>
	</button>
	<?php endif; ?>
	<div class="nldrone-stage" id="nldrone-stage" <?php echo 'toggle' === $mode ? 'hidden' : ''; ?>>
		<div class="nldrone-map" id="nldrone-map" role="region" aria-label="<?php echo esc_attr( $L['title'] ); ?>">
			<button type="button" class="nldrone-near" id="nldrone-near" hidden><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="3.2"/><path d="M12 2.5v3.2M12 18.3v3.2M2.5 12h3.2M18.3 12h3.2"/><circle cx="12" cy="12" r="7.2"/></svg><span><?php echo esc_html( $L['near'] ); ?></span></button>
		</div>
		<?php if ( 'hero' === $mode ) : ?>
		<p class="nldrone-note"><?php echo esc_html( $L['note'] ); ?></p>
		<?php else : ?>
		<div class="nldrone-key">
			<ul class="nldrone-legend">
				<li><i class="nldrone-lg nldrone-lg--city" aria-hidden="true">12</i><?php echo esc_html( $L['lg_city'] ); ?></li>
				<li><i class="nldrone-lg nldrone-lg--pt" aria-hidden="true"></i><?php echo esc_html( $L['lg_pt'] ); ?></li>
				<li><i class="nldrone-lg nldrone-lg--3d" aria-hidden="true">3D</i><?php echo esc_html( $L['lg_3d'] ); ?></li>
			</ul>
			<p class="nldrone-note"><?php echo esc_html( $L['note'] ); ?></p>
		</div>
		<?php endif; ?>
	</div>
</section>
<style>
/* ProjectMap v52 (design system, 28.9.2026): the Skin A palette - sea circles, ink dots, white halos on a quiet ground */
.nldrone{max-width:1240px;margin:6px auto 22px;padding:0 4px}
.nldrone--showcase{margin:34px auto 40px;padding:0 clamp(14px,3vw,28px)}
.nlhp-mapband .nldrone--showcase{max-width:none;margin:0;padding:0}
.nlhp-mapband .nlhp-maplead{margin:-6px 0 18px;max-width:780px;color:#3B4753;font:400 16px/1.65 Assistant,Heebo,Arial,sans-serif}
html body .nldrone .nldrone-head{background:transparent!important;border:0!important;border-radius:0!important;padding:0;margin:0 0 18px}
:root body .nldrone .nldrone-head__kicker{font:700 12.5px/1 Assistant,Heebo,Arial,sans-serif;letter-spacing:.07em;color:#2F6F86!important;margin:0 0 9px}
:root body .nldrone .nldrone-head__title{font:600 32px/1.15 "Noto Serif Hebrew","Frank Ruhl Libre",Georgia,serif!important;color:#14212B!important;margin:0 0 10px!important;text-wrap:balance}
.nldrone-head__sub{margin:0;max-width:780px;color:#3B4753;font:400 16px/1.65 Assistant,Heebo,Arial,sans-serif}
.nldrone-stage{margin-top:10px}
.nlhp-mapband .nldrone-stage,.nldrone--showcase .nldrone-stage{margin-top:0}
.nldrone-map{position:relative;height:520px;border-radius:16px;border:1px solid #DDE2E6;background:#EEF0EE;overflow:hidden}
.nldrone--showcase .nldrone-map{height:600px;border-radius:18px;box-shadow:0 18px 44px -30px rgba(20,33,43,.45)}
.nldrone-toggle{display:flex;align-items:center;gap:12px;width:100%;min-height:48px;text-align:start;font:600 14.5px/1.3 Assistant,Heebo,Arial,sans-serif;color:#14212B;background:#fff;border:1px solid #DDE2E6;border-radius:14px;padding:12px 18px;cursor:pointer;transition:border-color .2s}
.nldrone-toggle:hover{border-color:#2F6F86}
.nldrone-toggle__ic{color:#2F6F86;display:flex}
.nldrone-toggle__arrow{margin-inline-start:auto;color:#2F6F86;transition:transform .25s}
.nldrone.is-open .nldrone-toggle__arrow{transform:rotate(180deg)}
.nldrone-near{position:absolute;z-index:5;top:12px;left:12px;display:inline-flex;align-items:center;gap:7px;min-height:40px;font:700 13px/1 Assistant,Heebo,Arial,sans-serif;color:#14212B;background:#fff;border:1px solid #D5DBE0;border-radius:999px;padding:0 14px;cursor:pointer;box-shadow:0 4px 14px rgba(20,33,43,.16);transition:border-color .2s}
.nldrone-near svg{color:#2F6F86}
.nldrone-near:hover{border-color:#2F6F86}
.nldrone-key{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px 24px;margin:12px 2px 0}
.nldrone-legend{display:flex;flex-wrap:wrap;gap:8px 18px;list-style:none;margin:0!important;padding:0!important}
.nldrone-legend li{display:flex;align-items:center;gap:8px;margin:0!important;padding:0;color:#3B4753;font:600 13px/1.3 Assistant,Heebo,Arial,sans-serif;list-style:none}
.nldrone-legend li::before{content:none!important}
.nldrone-lg{flex:none;display:inline-grid;place-items:center;font-style:normal}
.nldrone-lg--city{width:26px;height:26px;border-radius:50%;background:#2F6F86;color:#fff;font:700 10.5px/1 Assistant,Arial,sans-serif;border:2px solid #fff;box-shadow:0 0 0 1px rgba(20,33,43,.14)}
.nldrone-lg--pt{width:9px;height:9px;border-radius:50%;background:#14212B;box-shadow:0 0 0 1.5px #fff,0 0 0 2.5px rgba(20,33,43,.18)}
.nldrone-lg--3d{height:20px;padding:0 7px;border-radius:999px;background:#14212B;color:#fff;font:800 10px/1 Assistant,Arial,sans-serif}
.nldrone-note{margin:0;max-width:560px;color:#5B6670;font:400 12.5px/1.5 Assistant,Heebo,Arial,sans-serif}
.nldrone-flag{display:flex;flex-direction:column;align-items:center;text-decoration:none!important;cursor:pointer;background:none;border:0;padding:0;margin:0;font:inherit;color:inherit}
.nldrone-flag__card{display:flex;align-items:center;gap:8px;white-space:nowrap;background:rgba(20,33,43,.94);border-radius:999px;padding-block:4px;padding-inline:4px 12px;box-shadow:0 8px 20px -6px rgba(20,33,43,.5);transition:background-color .2s}
.nldrone-flag__av{display:flex}
.nldrone-flag__av img,.nldrone-flag__av span{display:block;width:28px;height:28px;border-radius:50%;object-fit:cover;border:2px solid #fff;background:#2F6F86}
.nldrone-flag__av>*+*{margin-inline-start:-11px}
.nldrone-flag__card b{color:#fff;font:700 12.5px/1.2 Assistant,Heebo,Arial,sans-serif;max-width:170px;overflow:hidden;text-overflow:ellipsis}
.nldrone-flag__card i{font:800 10px/1 Assistant,Arial,sans-serif;font-style:normal;color:#14212B;background:#fff;border-radius:999px;padding:4px 6px}
.nldrone-flag__pole{display:block;width:2px;height:28px;background:#14212B;opacity:.75;transition:height .25s}
.nldrone.is-far .nldrone-flag{flex-direction:row;direction:ltr}
html[dir=rtl] .nldrone.is-far .nldrone-flag__card{direction:rtl}
.nldrone.is-far .nldrone-flag__pole{width:26px;height:2px}
.nldrone.is-far .nldrone-flag__foot{margin:0 0 0 -1px}
.nldrone-flag__s{display:none}
.nldrone.is-far.is-phone .nldrone-flag__av,.nldrone.is-far.is-phone .nldrone-flag__l{display:none}
.nldrone.is-far.is-phone .nldrone-flag__s{display:inline}
.nldrone.is-far.is-phone .nldrone-flag__card{padding-inline:10px 5px}
.nldrone.is-far.is-phone .nldrone-flag__pole{width:18px}
.nldrone-flag__foot{display:block;width:10px;height:10px;border-radius:50%;background:#14212B;border:2px solid #fff;margin-top:-1px}
.nldrone-flag:hover .nldrone-flag__card,.nldrone-flag:focus-visible .nldrone-flag__card{background:#2F6F86}
.nldrone-flag:focus-visible{outline:none}
.nldrone .mapboxgl-popup-content{border-radius:12px;padding:12px 14px 8px;background:#fff;box-shadow:0 14px 34px -12px rgba(20,33,43,.4);font-family:Assistant,Heebo,Arial,sans-serif}
.nldrone .mapboxgl-popup-close-button{width:36px;height:36px;font-size:20px;line-height:1;color:#3B4753;border-radius:0 12px 0 10px}
html[dir=rtl] .nldrone .mapboxgl-popup-close-button{right:auto;left:0;border-radius:12px 0 10px 0}
.nldrone-pop{min-width:190px;max-width:240px;color:#14212B;text-align:start}
.nldrone-pop__k{display:block;margin:0 0 6px;padding-inline-end:30px;font:700 11.5px/1 Assistant,Arial,sans-serif;letter-spacing:.05em;color:#2F6F86}
.nldrone-pop b{display:block;font:700 15px/1.3 Assistant,Heebo,Arial,sans-serif;padding-inline-end:26px}
.nldrone-pop img{display:block;width:100%;height:92px;object-fit:cover;border-radius:8px;margin:8px 0 2px}
.nldrone-pop__row{display:block;margin-top:5px;font:600 13px/1.4 Assistant,Heebo,Arial,sans-serif;color:#3B4753}
.nldrone-pop__note{display:block;margin-top:3px;font:400 12px/1.4 Assistant,Heebo,Arial,sans-serif;color:#5B6670}
.nldrone-pop a{display:flex;align-items:center;min-height:40px;margin-top:4px;font:700 13.5px/1.2 Assistant,Heebo,Arial,sans-serif;color:#2F6F86!important;text-decoration:none!important}
.nldrone-pop__list{list-style:none;margin:2px 0 0!important;padding:0!important}
.nldrone-pop__list li{margin:0!important;padding:0;border-top:1px solid #E9ECEF;list-style:none}
.nldrone-pop__list li:first-child{border-top:0}
.nldrone-pop__list li::before{content:none!important}
.nldrone-pop .nldrone-pop__list a{gap:10px;min-height:50px;margin:0;color:#14212B!important}
.nldrone-pop__list img,.nldrone-pop__list a>span{flex:none;display:block;width:34px;height:34px;margin:0;border-radius:50%;object-fit:cover;background:#2F6F86}
.nldrone-pop .nldrone-pop__list b{flex:1;padding:0;font:700 14px/1.3 Assistant,Heebo,Arial,sans-serif}
.nldrone-pop__list i{flex:none;font:800 10px/1 Assistant,Arial,sans-serif;font-style:normal;color:#fff;background:#14212B;border-radius:999px;padding:4px 6px}
.nldrone-pop .nldrone-pop__list a:hover b{color:#2F6F86}
@media(max-width:600px){
:root body .nldrone .nldrone-head__title{font-size:25px!important}
.nldrone-head__sub,.nlhp-mapband .nlhp-maplead{font-size:15px}
.nldrone-map,.nldrone--showcase .nldrone-map{height:480px;border-radius:14px}
.nldrone-near{min-height:44px}
.nldrone-key{margin-top:10px}
.nldrone-legend{gap:6px 14px}
.nldrone-legend li{font-size:12.5px}
}
.nldrone--hero{max-width:none;margin:0;padding:0;position:absolute;inset:0}
.nldrone--hero .nldrone-stage{margin:0;height:100%}
.nldrone--hero .nldrone-map{height:100%;border-radius:0;border:0;box-shadow:none}
.nldrone--hero .nldrone-note{position:absolute;bottom:8px;inset-inline-end:14px;z-index:5;color:#CDC5B4;margin:0;text-shadow:0 1px 3px rgba(0,0,0,.6)}
.nldrone--hero .nldrone-near{top:auto;bottom:46px;left:auto;right:14px}
@media(prefers-reduced-motion:reduce){.nldrone-flag__pole,.nldrone-flag__card,.nldrone-toggle__arrow{transition:none}}
</style>
<script>
(function(){
	var band=document.getElementById("nldrone"),btn=document.getElementById("nldrone-toggle"),stage=document.getElementById("nldrone-stage");
	if(!band)return;
	var L={},X={u:"",sqm:"",st:{}};
	try{L=JSON.parse(band.dataset.l||"{}")||{}}catch(e){}
	try{X=JSON.parse(band.dataset.lX||"{}")||X}catch(e){}
	function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})}
	function fmt(n){return String(Math.round(+n||0)).replace(/\B(?=(\d{3})+(?!\d))/g,",")}
	function tpl(s,o){return String(s||"").replace(/\{(\w+)\}/g,function(m,k){return o[k]!=null?o[k]:m})}
	function short(t){return String(t||"").split("|")[0].split(/\s[-–·]\s/)[0].trim()}
	var booted=false;
	function boot(){
		if(booted)return;booted=true;
		function go(){
			if(!window.mapboxgl)return;
			mapboxgl.accessToken=band.dataset.token;
			/* Hebrew renders REVERSED without the RTL text plugin (caught on the live hero) */
			try{if(mapboxgl.getRTLTextPluginStatus&&mapboxgl.getRTLTextPluginStatus()==="unavailable"){mapboxgl.setRTLTextPlugin("https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.3.0/mapbox-gl-rtl-text.js",null,false)}}catch(e){}
			var isHero=band.dataset.mode==="hero";
			var phone=!!(window.matchMedia&&window.matchMedia("(max-width:600px)").matches);
			/* ProjectMap v52: the country view is FLAT (legible circles and names); a tap dives in with pitch.
			   The night palette stays for the hero fallback only. cooperativeGestures (owner 2026-07-11):
			   page scroll must never zoom the map. */
			var PAL=isHero
				?{city:"#C9B37A",cityTxt:"#14130F",ring:"#14130F",pt:"#E9D9A8",ptStroke:"#14130F",label:"#E9E2D2",halo:"#14130F",tag:"#E9D9A8",land:"#17150F",water:"#0E1A20",bld:"#3A342A"}
				:{city:"#2F6F86",cityTxt:"#FFFFFF",ring:"#FFFFFF",pt:"#14212B",ptStroke:"#FFFFFF",label:"#14212B",halo:"#FFFFFF",tag:"#2F6F86",land:"#F1F0EB",water:"#C3D5DB",bld:"#D8DDE1"};
			var map=new mapboxgl.Map({container:"nldrone-map",style:isHero?"mapbox://styles/mapbox/dark-v11":"mapbox://styles/mapbox/light-v11",center:[34.95,32.05],zoom:phone?6.9:7.6,pitch:isHero?55:0,bearing:0,attributionControl:true,cooperativeGestures:true,locale:{"CooperativeGesturesHandler.WindowsHelpText":"לחצו Ctrl וגללו כדי להתקרב במפה","CooperativeGesturesHandler.MacHelpText":"לחצו ⌘ וגללו כדי להתקרב במפה","TouchPanBlocker.Message":"הזיזו את המפה בשתי אצבעות"}});
			map.addControl(new mapboxgl.NavigationControl({visualizePitch:true}),"top-right");
			var OUT=12.2,IN=11.3;
			band.classList.toggle("is-phone",phone);
			/* the style's own "load" is the only reliable signal: isStyleLoaded() is false again while the terrain loads,
			   and a data reply landing in that gap waited for a "load" that had passed (seen live 28.9.2026: no circles) */
			var styleReady=false;
			map.on("load",function(){
				styleReady=true;
				try{map.setPaintProperty("water","fill-color",PAL.water)}catch(e){}
				try{map.setPaintProperty("land","background-color",PAL.land)}catch(e){}
				if(isHero){try{map.setFog({color:"#14130F","horizon-blend":0.06,"star-intensity":0.25})}catch(e){}}
				try{map.getStyle().layers.forEach(function(l){if(l.type==="symbol"&&l.layout&&l.layout["text-field"]){map.setLayoutProperty(l.id,"text-field",["coalesce",["get","name_he"],["get","name:he"],["get","name"]])}})}catch(e){}
				/* the country view speaks only in our circles: the base map's country, region and town names wait for the dive */
				try{map.getStyle().layers.forEach(function(l){if(/^(country|state|settlement-major|settlement-minor)-label/.test(l.id)){map.setLayerZoomRange(l.id,9.5,24)}})}catch(e){}
				var layers=map.getStyle().layers,lab;
				for(var i=0;i<layers.length;i++){if(layers[i].type==="symbol"&&layers[i].layout&&layers[i].layout["text-field"]){lab=layers[i].id;break}}
				try{map.addLayer({id:"nl-3d",source:"composite","source-layer":"building",filter:["==","extrude","true"],type:"fill-extrusion",minzoom:13,paint:{"fill-extrusion-color":PAL.bld,"fill-extrusion-height":["get","height"],"fill-extrusion-base":["get","min_height"],"fill-extrusion-opacity":.72}},lab)}catch(e){}
				try{map.addSource("nl-dem",{type:"raster-dem",url:"mapbox://mapbox.mapbox-terrain-dem-v1",tileSize:512,maxzoom:14});map.setTerrain({source:"nl-dem",exaggeration:1.35})}catch(e){}
				if(isHero){try{map.addLayer({id:"nl-sky",type:"sky",paint:{"sky-type":"atmosphere","sky-atmosphere-sun-intensity":6}})}catch(e){}}
			});
			fetch(band.dataset.rest).then(function(r){return r.json()}).then(function(d){
				var all=(d&&d.items)||[]; if(!all.length)return;
				function exact(p){return p.conf!=="city"}
				/* a project located only at city level is counted in its city's circle, never drawn as a dot */
				var flags=all.filter(function(p){return p.featured&&exact(p)});
				var pts=all.filter(function(p){return exact(p)&&!p.featured});
				/* the data tag (owner 2026-07-12): units, else the status. No price on the map (v52): the per-m2 figures are estimates. */
				function tagOf(p){
					if(p.units>0){return fmt(p.units)+" "+(X.u||"")}
					if(p.status&&X.st&&X.st[p.status]){return X.st[p.status]}
					return ""
				}
				var gj={type:"FeatureCollection",features:pts.map(function(p){
					return {type:"Feature",geometry:{type:"Point",coordinates:[p.lng,p.lat]},
						properties:{id:p.id,title:p.title,short:short(p.title),url:p.url,city:p.city||"",img:p.img||"",conf:p.conf||"",tag:tagOf(p)}};
				})};
				/* the city circle: every located project counts, at the mean of the city's exact points */
				/* one city, one circle: "תל אביב-יפו" and "תל אביב יפו" are the same city (a hyphen split one project off, seen
				   live 28.9.2026); the circle wears the most common spelling */
				function ckey(c){return String(c).replace(/[-־–]/g," ").replace(/\s+/g," ").trim()}
				var C={};
				all.forEach(function(p){
					var raw=p.city||"";if(!raw)return;
					var c=ckey(raw),v=C[c]||(C[c]={n:0,m:0,x:0,y:0,cl:0,cx:0,cy:0,sp:{}});
					v.sp[raw]=(v.sp[raw]||0)+1;
					v.n++;if(exact(p)){v.m++;v.x+=p.lng;v.y+=p.lat}else{v.cl++;v.cx+=p.lng;v.cy+=p.lat}
				});
				function spell(v){var b="",k=-1;for(var s in v.sp){if(v.sp[s]>k){k=v.sp[s];b=s}}return b}
				var keys=Object.keys(C).sort(function(a,b){return C[b].n-C[a].n}),names=keys.map(function(c){return spell(C[c])});
				var cityGj={type:"FeatureCollection",features:keys.map(function(c,i){
					var v=C[c];
					return {type:"Feature",geometry:{type:"Point",coordinates:v.m?[v.x/v.m,v.y/v.m]:[v.cx/v.cl,v.cy/v.cl]},properties:{city:names[i],n:v.n,cl:v.cl,rank:i}};
				})};
				/* the first frame: the whole country from the Negev's edge to the Galilee, flat */
				var bb=new mapboxgl.LngLatBounds();
				cityGj.features.forEach(function(f){if(f.geometry.coordinates[1]>30.8){bb.extend(f.geometry.coordinates)}});
				if(!isHero&&!bb.isEmpty()){try{map.fitBounds(bb,{padding:phone?{top:64,bottom:26,left:22,right:50}:{top:56,bottom:34,left:60,right:60},duration:0})}catch(e){}}
				var N=["coalesce",["get","sum"],["get","n"]];
				var R=["interpolate",["linear"],["sqrt",N],1,phone?8:9,4,phone?12:14,9,phone?19:22,16,phone?26:31,24,phone?32:39];
				var TS=["interpolate",["linear"],["sqrt",N],1,11.5,9,13,24,14.5];
				/* the name sits under its circle, or above it, or inland beside it (the 3D callout lives over the sea) when a
				   neighbour is in the way: (radius + 4px) in ems of its own size. The bigger city is placed first (the sort key
				   stays positive). */
				var RO=["+",["/",["+",R,4],TS],0.05];
				function fade(a){return ["interpolate",["linear"],["zoom"],IN,a,OUT,0]}
				var nameOf=["at",["coalesce",["get","best"],["get","rank"]],["literal",names]];
				var more=String(L.more||"+{k}").split("{k}"),k=["-",["get","point_count"],1];
				/* the city names are Hebrew: on a left-to-right page the "+12 cities" goes on its own line, or the two
				   directions reorder each other ("cities 12+ חיפה", seen on the English home 28.9.2026) */
				var sep=window.getComputedStyle(band).direction==="rtl"?" ":"\n";
				var label=["case",["has","point_count"],["concat",nameOf,sep,["case",["==",k,1],String(L.more1||"+1"),["concat",more[0],["to-string",k],more[1]||""]]],["get","city"]];
				var pop=null;
				function popup(ll,html){if(pop){pop.remove()}pop=new mapboxgl.Popup({offset:14,maxWidth:"270px",focusAfterOpen:false}).setLngLat(ll).setHTML(html).addTo(map)}
				var addData=function(){
					if(map.getSource("nlprojects"))return;
					map.addSource("nlprojects",{type:"geojson",data:gj});
					/* cities that touch at this scale share one circle, named after the largest */
					map.addSource("nlcities",{type:"geojson",data:cityGj,cluster:true,clusterRadius:phone?40:46,clusterMaxZoom:11,clusterProperties:{sum:["+",["get","n"]],best:["min",["get","rank"]]}});
					/* dots: quiet under the circles, full in the city */
					map.addLayer({id:"nl-points",type:"circle",source:"nlprojects",
						paint:{"circle-color":PAL.pt,"circle-radius":["interpolate",["linear"],["zoom"],6,1.5,9,2.4,IN,3.6,13,6,15,7.5],"circle-stroke-width":["interpolate",["linear"],["zoom"],6,0.3,IN,1,13,1.6],"circle-stroke-color":PAL.ptStroke,"circle-opacity":["interpolate",["linear"],["zoom"],7,0.3,IN,0.45,OUT,0.95]}});
					map.addLayer({id:"nl-point-tags",type:"symbol",source:"nlprojects",minzoom:OUT-0.4,
						layout:{"text-field":["get","tag"],"text-size":["interpolate",["linear"],["zoom"],12,11,15,12.5],"text-font":["DIN Pro Bold","Arial Unicode MS Bold"],"text-anchor":"bottom","text-offset":[0,-0.6],"text-optional":true,"text-allow-overlap":false,"text-padding":4},
						paint:{"text-color":PAL.tag,"text-halo-color":PAL.halo,"text-halo-width":1.6}});
					map.addLayer({id:"nl-point-labels",type:"symbol",source:"nlprojects",minzoom:OUT-0.4,
						layout:{"text-field":["get","short"],"text-size":11.5,"text-font":["DIN Pro Medium","Arial Unicode MS Regular"],"text-anchor":"top","text-offset":[0,0.7],"text-optional":true,"text-allow-overlap":false,"text-max-width":9},
						paint:{"text-color":PAL.label,"text-halo-color":PAL.halo,"text-halo-width":1.4}});
					/* the city circles; a circle of several cities wears a second ring */
					map.addLayer({id:"nl-city-ring",type:"circle",source:"nlcities",maxzoom:OUT,filter:["has","point_count"],
						paint:{"circle-radius":["+",R,4],"circle-color":"rgba(0,0,0,0)","circle-stroke-width":1.5,"circle-stroke-color":PAL.city,"circle-stroke-opacity":fade(0.75)}});
					map.addLayer({id:"nl-city",type:"circle",source:"nlcities",maxzoom:OUT,
						paint:{"circle-radius":R,"circle-color":PAL.city,"circle-opacity":fade(0.94),"circle-stroke-width":2,"circle-stroke-color":PAL.ring,"circle-stroke-opacity":fade(1)}});
					map.addLayer({id:"nl-city-n",type:"symbol",source:"nlcities",maxzoom:OUT,
						layout:{"text-field":["number-format",N,{"locale":"en-US"}],"text-size":["interpolate",["linear"],["sqrt",N],1,10.5,9,13,24,16],"text-font":["DIN Pro Bold","Arial Unicode MS Bold"],"text-allow-overlap":true,"text-ignore-placement":true},
						paint:{"text-color":PAL.cityTxt,"text-opacity":fade(1)}});
					/* the circles are obstacles for the names: an invisible square of the circle's size, placed before them */
					if(!map.hasImage("nl-blk")){map.addImage("nl-blk",{width:32,height:32,data:new Uint8Array(32*32*4)})}
					map.addLayer({id:"nl-city-name",type:"symbol",source:"nlcities",maxzoom:OUT,
						layout:{"text-field":label,"text-size":TS,"text-font":["DIN Pro Bold","Arial Unicode MS Bold"],"text-variable-anchor":["top","bottom","left","right"],"text-radial-offset":RO,"symbol-sort-key":["-",100000,N],"text-padding":1,"text-max-width":14},
						paint:{"text-color":PAL.label,"text-halo-color":PAL.halo,"text-halo-width":1.8,"text-opacity":fade(1)}});
					map.addLayer({id:"nl-city-blk",type:"symbol",source:"nlcities",maxzoom:OUT,
						layout:{"icon-image":"nl-blk","icon-size":["/",["*",R,2],32],"icon-padding":0,"icon-allow-overlap":true,"icon-ignore-placement":false}});
					function projHtml(p){
						return '<div class="nldrone-pop" dir="auto">'+(p.city?'<span class="nldrone-pop__k">'+esc(p.city)+"</span>":"")+"<b>"+esc(p.title)+"</b>"
							+(p.img?'<img src="'+esc(p.img)+'" alt="" loading="lazy">':"")+(p.tag?'<span class="nldrone-pop__row">'+esc(p.tag)+"</span>":"")
							+(p.conf==="city"?'<span class="nldrone-pop__note">'+esc(L.city)+"</span>":"")+'<a href="'+esc(p.url)+'">'+esc(L.top)+"</a></div>";
					}
					function cityHtml(p){
						var url=String(L.catalog||"/projects/")+"?city="+encodeURIComponent(p.city);
						return '<div class="nldrone-pop" dir="auto"><span class="nldrone-pop__k">'+esc(L.cityK||"")+"</span><b>"+esc(p.city)+"</b>"
							+'<span class="nldrone-pop__row">'+esc(+p.n===1?(L.cityN1||""):tpl(L.cityN,{n:fmt(p.n)}))+"</span>"
							+(+p.cl>0?'<span class="nldrone-pop__note">'+esc(tpl(L.cityCl,{n:fmt(p.cl)}))+"</span>":"")
							+'<a href="'+esc(url)+'">'+esc(tpl(L.toCity,{city:p.city}))+"</a></div>";
					}
					/* one click handler: a city circle first (cluster: open it up; city: dive in with its card), then a project */
					var CITY=["nl-city","nl-city-n","nl-city-name"],PTS=["nl-points","nl-point-labels","nl-point-tags"];
					map.on("click",function(e){
						var b=[[e.point.x-4,e.point.y-4],[e.point.x+4,e.point.y+4]];
						var cf=map.getZoom()<OUT?map.queryRenderedFeatures(b,{layers:CITY}):[];
						if(cf.length){
							var f=cf[0],p=f.properties,c=f.geometry.coordinates;
							if(p.cluster){
								map.getSource("nlcities").getClusterExpansionZoom(p.cluster_id,function(err,z){if(err)return;map.easeTo({center:c,zoom:Math.min(z+0.4,OUT-0.4),duration:900})});
								return;
							}
							map.easeTo({center:c,zoom:OUT+0.5,pitch:isHero?55:45,bearing:-8,duration:1200});
							popup(c,cityHtml(p));
							return;
						}
						var pf=map.queryRenderedFeatures(b,{layers:PTS});
						if(pf.length){popup(pf[0].geometry.coordinates,projHtml(pf[0].properties))}
					});
					CITY.concat(PTS).forEach(function(l){
						map.on("mouseenter",l,function(){map.getCanvas().style.cursor="pointer"});
						map.on("mouseleave",l,function(){map.getCanvas().style.cursor=""});
					});
				};
				if(styleReady){addData()}else{map.once("load",addData)}
				/* the city names laid out before the right-to-left text plugin was ready were dropped at the country view
				   (seen 28.9.2026): once it is ready, the circles are laid out again */
				(function relayout(n){
					var st=mapboxgl.getRTLTextPluginStatus?mapboxgl.getRTLTextPluginStatus():"loaded";
					if(st==="loaded"&&map.getSource("nlcities")){map.once("idle",function(){try{if(map.getZoom()<OUT&&map.queryRenderedFeatures({layers:["nl-city"]}).length&&!map.queryRenderedFeatures({layers:["nl-city-name"]}).length){map.getSource("nlcities").setData(cityGj)}}catch(e){}});return}
					if(n<60){setTimeout(function(){relayout(n+1)},250)}
				})(0);
				/* the projects with a 3D model fly a pill on a stem; pills that would cover each other merge into one
				   ("4 projects in 3D") until the zoom separates them. One click opens the group; one more, the page. */
				var marks=[];
				function flagEl(list,label,group){
					var el=document.createElement(group?"button":"a");
					if(group){el.type="button"}else{el.href=list[0].url}
					el.className="nldrone-flag"+(group?" nldrone-flag--group":"");
					el.setAttribute("aria-label",label);
					el.innerHTML='<span class="nldrone-flag__card"><span class="nldrone-flag__av">'+list.slice(0,3).map(function(q){return q.poster?'<img src="'+esc(q.poster)+'" alt="" loading="lazy">':"<span></span>"}).join("")+'</span><b><span class="nldrone-flag__l">'+esc(label)+"</span>"+(group?'<span class="nldrone-flag__s">'+list.length+"</span>":"")+'</b><i>3D</i></span><span class="nldrone-flag__pole"></span><span class="nldrone-flag__foot"></span>';
					return el;
				}
				/* far (the country view): a callout to the west, over the sea, so it never covers a city circle;
				   near: a pill on a stem above its building */
				function listHtml(list){
					return '<div class="nldrone-pop" dir="auto"><span class="nldrone-pop__k">'+esc(tpl(L.group,{n:list.length}))+'</span><ul class="nldrone-pop__list">'
						+list.map(function(q){return '<li><a href="'+esc(q.url)+'">'+(q.poster?'<img src="'+esc(q.poster)+'" alt="" loading="lazy">':"<span></span>")+"<b>"+esc(short(q.title))+"</b><i>3D</i></a></li>"}).join("")+"</ul></div>";
				}
				function regroup(){
					marks.forEach(function(m){m.remove()});marks=[];
					var farz=map.getZoom()<IN; /* the callout over the sea until the circles fade; then the pill on its stem */
					band.classList.toggle("is-far",farz);
					if(!flags.length)return;
					var gap=farz?(phone?90:130):(phone?120:160),P=flags.map(function(q){return map.project([q.lng,q.lat])}),up=flags.map(function(q,i){return i});
					function root(i){while(up[i]!==i){i=up[i]}return i}
					for(var i=0;i<flags.length;i++){for(var j=i+1;j<flags.length;j++){var dx=P[i].x-P[j].x,dy=P[i].y-P[j].y;if(dx*dx+dy*dy<gap*gap){up[root(j)]=root(i)}}}
					var sets={};flags.forEach(function(q,i){var r=root(i);(sets[r]=sets[r]||[]).push(q)});
					Object.keys(sets).forEach(function(r){
						var list=sets[r],group=list.length>1;
						var el=flagEl(list,group?tpl(L.group,{n:list.length}):short(list[0].title),group);
						var lng=0,lat=0,bx=new mapboxgl.LngLatBounds();
						list.forEach(function(q){lng+=q.lng;lat+=q.lat;bx.extend([q.lng,q.lat])});
						if(group){el.addEventListener("click",function(ev){
							ev.preventDefault();ev.stopPropagation();
							/* too close to part even at the closest zoom (Dimri Yama and Rainbow stand 130 m apart): a list card */
							if(map.getZoom()>=15.2){var at=[lng/list.length,lat/list.length];map.easeTo({center:at,offset:[0,phone?90:60],duration:500});popup(at,listHtml(list));return}
							map.fitBounds(bx,{padding:phone?80:140,maxZoom:15.8,pitch:45,duration:1200});
						})}
						marks.push(new mapboxgl.Marker({element:el,anchor:farz?"right":"bottom",offset:farz?[5,0]:[0,5]}).setLngLat([lng/list.length,lat/list.length]).addTo(map));
					});
				}
				map.on("moveend",regroup);regroup();
				/* least-effort locality: silent IP-level approximation opens the map
				   near the visitor (no permission prompt); the button uses precise
				   browser geolocation only when the user asks. */
				var near=document.getElementById("nldrone-near");
				if(near&&navigator.geolocation){
					near.hidden=false;
					near.addEventListener("click",function(){
						navigator.geolocation.getCurrentPosition(function(pos){
							map.easeTo({center:[pos.coords.longitude,pos.coords.latitude],zoom:OUT+0.5,pitch:45,duration:1400});
						},function(){},{ enableHighAccuracy:false, timeout:6000, maximumAge:600000 });
					});
				}
				try{
					fetch("https://ipwho.is/").then(function(r){return r.json()}).then(function(g){
						if(g&&g.success&&g.country_code==="IL"&&g.latitude){
							map.easeTo({center:[g.longitude,g.latitude],zoom:10.2,duration:1600});
						}
					}).catch(function(){});
				}catch(e){}
			}).catch(function(){});
		}
		if(window.mapboxgl){go();return}
		var l=document.createElement("link");l.rel="stylesheet";l.href="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css";document.head.appendChild(l);
		var sc=document.createElement("script");sc.src="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js";sc.onload=go;document.head.appendChild(sc);
	}
	if(band.dataset.mode==="hero"){
		// the hero map is the site opener - boot when the browser breathes
		if("requestIdleCallback" in window){requestIdleCallback(boot,{timeout:1800})}else{setTimeout(boot,400)}
	} else if(band.dataset.mode==="showcase"){
		// present itself: boot when the band approaches the viewport
		if("IntersectionObserver" in window){
			var io=new IntersectionObserver(function(es){
				es.forEach(function(e){ if(e.isIntersecting){ io.disconnect(); boot(); } });
			},{rootMargin:"260px"});
			io.observe(band);
		} else { boot(); }
	} else if(btn){
		btn.addEventListener("click",function(){
			var open=stage.hidden;
			stage.hidden=!open;
			band.classList.toggle("is-open",open);
			btn.setAttribute("aria-expanded",open?"true":"false");
			if(open)boot();
		});
	}
})();
</script>
<?php
		return ob_get_clean();
	}
}
