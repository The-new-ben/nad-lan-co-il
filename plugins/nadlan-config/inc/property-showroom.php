<?php
/**
 * nadlan-config - Property showroom layer (v1.69.70)
 *
 * The differentiator block on single nadlan_property pages, on top of the
 * existing stack (cards-render facts/gallery, listings-ux similar/favorites/
 * mortgage, nearby-poi real schools/transit via OSM, avm-deals, media tabs,
 * schema JSON-LD):
 *   1. Key-facts hero strip (price, rooms, floor, sqm, ₪/sqm, listing type)
 *   2. Sketch-first SELECTABLE FACADE - parametric SVG building generated from
 *      total_floors / floor / units_per_floor / unit_position meta; the listed
 *      apartment is highlighted; hover/click floors; toggle to a parametric
 *      schematic floor plan (rooms/mamad/balcony) - the "inside view".
 *   3. Monthly costs panel (arnona + vaad bayit + mortgage estimate).
 *   4. Single-listing Leaflet map (OSM tiles, no key) with the asset marker.
 *   5. Honest "לדוגמה" badge on is_demo listings.
 *
 * Registers the extra Israeli listing meta Yad2/Madlan-parity requires:
 * arnona_monthly, vaad_bayit_monthly, entry_date, condition, storage,
 * renovated_year, direction, units_per_floor, unit_position.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---------------- extra listing meta ---------------- */
if ( ! function_exists( 'nadlan_pshow_register_meta' ) ) {
	function nadlan_pshow_register_meta() {
		$fields = array(
			'city'               => 'string',   // queried by listings-ux similar-SQL; was never registered for properties
			'neighborhood'       => 'string',
			'highlights_csv'     => 'string',   // "What's special" bullets, pipe-separated (Zillow-parity)
			'arnona_monthly'     => 'integer',
			'vaad_bayit_monthly' => 'integer',
			'entry_date'         => 'string',   // free text: מיידי / 01/2027
			'condition'          => 'string',   // new|renovated|good|needs_renovation
			'storage'            => 'boolean',  // מחסן
			'renovated_year'     => 'integer',
			'direction'          => 'string',   // כיווני אוויר
			'units_per_floor'    => 'integer',  // for the facade
			'unit_position'      => 'integer',  // 1..units_per_floor (from the right)
		);
		foreach ( $fields as $k => $type ) {
			register_post_meta( 'nadlan_property', $k, array(
				'show_in_rest' => true, 'single' => true, 'type' => $type,
				'auth_callback' => function ( $allowed, $meta_key, $post_id ) { return current_user_can( 'edit_post', (int) $post_id ); },
			) );
		}
	}
}
add_action( 'init', 'nadlan_pshow_register_meta', 14 );

/* ---------------- helpers ---------------- */
if ( ! function_exists( 'nadlan_pshow_condition_label' ) ) {
	function nadlan_pshow_condition_label( $c ) {
		$map = array( 'new' => 'חדש מקבלן', 'renovated' => 'משופץ', 'good' => 'במצב טוב', 'needs_renovation' => 'דורש שיפוץ' );
		return isset( $map[ $c ] ) ? $map[ $c ] : $c;
	}
}

/* ---------------- parametric facade SVG ---------------- */
if ( ! function_exists( 'nadlan_pshow_facade_svg' ) ) {
	function nadlan_pshow_facade_svg( $total_floors, $listing_floor, $units_per_floor, $unit_position ) {
		$total_floors    = max( 1, min( 40, (int) $total_floors ) );
		$listing_floor   = max( 0, min( $total_floors, (int) $listing_floor ) );
		$units_per_floor = max( 1, min( 6, (int) $units_per_floor ?: 2 ) );
		$unit_position   = max( 1, min( $units_per_floor, (int) $unit_position ?: 1 ) );

		$fh = 34;                                   // floor height px
		$bw = 260;                                  // building width
		$bx = 30;                                   // building x
		$h  = ( $total_floors + 1 ) * $fh + 70;     // + ground + roof margin
		$w  = 320;
		$ground_y = $h - 30;

		$uw  = ( $bw - 24 ) / $units_per_floor;     // unit cell width
		$svg = '<svg class="nlps-facade-svg" viewBox="0 0 ' . $w . ' ' . $h . '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="חזית הבניין - הדירה המוצעת בקומה ' . esc_attr( $listing_floor ) . '">';
		$svg .= '<style>.nlps-f-fl{cursor:pointer}.nlps-f-fl:hover .nlps-f-bg{fill:#F3EEE3}.nlps-f-win{fill:#FAF8F3;stroke:#2E2B26;stroke-width:1.1}.nlps-f-sel .nlps-f-win{fill:#E6D4AE}.nlps-f-unit{fill:#C2563A;fill-opacity:.85;stroke:#9C3F28;stroke-width:1.4}</style>';
		// ground line + trees (sketch feel)
		$svg .= '<line x1="6" y1="' . $ground_y . '" x2="' . ( $w - 6 ) . '" y2="' . $ground_y . '" stroke="#2E2B26" stroke-width="1.6"/>';
		$svg .= '<path d="M14 ' . $ground_y . ' q4 -22 8 0 M10 ' . ( $ground_y - 10 ) . ' q8 -14 16 0" fill="none" stroke="#6D665C" stroke-width="1.1"/>';
		$svg .= '<path d="M' . ( $w - 22 ) . ' ' . $ground_y . ' q4 -26 8 0 M' . ( $w - 26 ) . ' ' . ( $ground_y - 12 ) . ' q8 -16 16 0" fill="none" stroke="#6D665C" stroke-width="1.1"/>';
		// building outline + roof
		$top_y = $ground_y - ( $total_floors + 1 ) * $fh;
		$svg .= '<rect x="' . $bx . '" y="' . $top_y . '" width="' . $bw . '" height="' . ( ( $total_floors + 1 ) * $fh ) . '" fill="#FFFDFC" stroke="#1B1A17" stroke-width="2"/>';
		$svg .= '<line x1="' . ( $bx - 8 ) . '" y1="' . $top_y . '" x2="' . ( $bx + $bw + 8 ) . '" y2="' . $top_y . '" stroke="#1B1A17" stroke-width="2.4"/>';
		// floors, top floor first
		for ( $f = $total_floors; $f >= 1; $f-- ) {
			$fy = $ground_y - ( $f + 1 ) * $fh + $fh; // top y of this floor row
			$is_sel = ( $f === $listing_floor );
			$svg .= '<g class="nlps-f-fl' . ( $is_sel ? ' nlps-f-sel' : '' ) . '" data-floor="' . $f . '">';
			$svg .= '<rect class="nlps-f-bg" x="' . $bx . '" y="' . $fy . '" width="' . $bw . '" height="' . $fh . '" fill="' . ( $is_sel ? '#F8F0EA' : '#FFFDFC' ) . '" stroke="#C9C0AE" stroke-width="0.7"/>';
			for ( $u = 1; $u <= $units_per_floor; $u++ ) {
				// RTL: unit 1 is rightmost
				$ux = $bx + 12 + $bw - 24 - $u * $uw + ( $uw - min( $uw - 8, 34 ) ) / 2;
				$wgw = min( $uw - 8, 34 );
				$is_unit = ( $is_sel && $u === $unit_position );
				$svg .= '<rect class="' . ( $is_unit ? 'nlps-f-unit' : 'nlps-f-win' ) . '" x="' . round( $ux, 1 ) . '" y="' . ( $fy + 7 ) . '" width="' . round( $wgw, 1 ) . '" height="' . ( $fh - 14 ) . '" rx="1.5"/>';
			}
			// floor number (right side, RTL)
			$svg .= '<text x="' . ( $bx + $bw + 12 ) . '" y="' . ( $fy + $fh / 2 + 4 ) . '" font-size="10" fill="' . ( $is_sel ? '#C2563A' : '#B7AE9E' ) . '" font-weight="' . ( $is_sel ? '700' : '400' ) . '">' . $f . '</text>';
			$svg .= '</g>';
		}
		// ground floor: entrance
		$gy = $ground_y - $fh;
		$svg .= '<rect x="' . $bx . '" y="' . $gy . '" width="' . $bw . '" height="' . $fh . '" fill="#F3EEE3" stroke="#C9C0AE" stroke-width="0.7"/>';
		$svg .= '<rect x="' . ( $bx + $bw / 2 - 14 ) . '" y="' . ( $gy + 8 ) . '" width="28" height="' . ( $fh - 8 ) . '" fill="#2E2B26"/>';
		$svg .= '</svg>';
		return $svg;
	}
}

/* ---------------- parametric floor-plan SVG (inside view) ---------------- */
if ( ! function_exists( 'nadlan_pshow_plan_svg' ) ) {
	function nadlan_pshow_plan_svg( $rooms, $has_mamad, $balcony_sqm, $size_sqm ) {
		$rooms    = max( 1, min( 8, (float) $rooms ) );
		$bedrooms = max( 0, (int) ceil( $rooms ) - 1 );
		$w = 340; $h = 250;
		$s = '<svg class="nlps-plan-svg" viewBox="0 0 ' . $w . ' ' . $h . '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="תוכנית דירה סכמטית">';
		$s .= '<style>.nlps-p-r{fill:#FFFDFC;stroke:#1B1A17;stroke-width:1.6}.nlps-p-t{font-size:10px;fill:#2E2B26;font-weight:600}.nlps-p-s{font-size:8px;fill:#6D665C}</style>';
		$s .= '<rect x="8" y="8" width="' . ( $w - 16 ) . '" height="' . ( $h - 16 ) . '" fill="none" stroke="#1B1A17" stroke-width="2.4"/>';
		// salon+kitchen block (right half, RTL)
		$s .= '<rect class="nlps-p-r" x="' . ( $w / 2 ) . '" y="8" width="' . ( $w / 2 - 8 ) . '" height="' . ( $h * 0.62 ) . '"/>';
		$s .= '<text class="nlps-p-t" x="' . ( $w * 0.75 - 20 ) . '" y="' . ( $h * 0.3 ) . '">סלון ומטבח</text>';
		// bedrooms stacked on left half
		$bh = $bedrooms > 0 ? ( $h - 16 ) / max( $bedrooms, 1 ) : 0;
		for ( $i = 0; $i < $bedrooms; $i++ ) {
			$label = ( $has_mamad && $i === $bedrooms - 1 ) ? 'ממ״ד' : 'חדר שינה';
			$s .= '<rect class="nlps-p-r" x="8" y="' . ( 8 + $i * $bh ) . '" width="' . ( $w / 2 - 8 ) . '" height="' . $bh . '"/>';
			$s .= '<text class="nlps-p-t" x="' . ( $w / 4 - 24 ) . '" y="' . ( 8 + $i * $bh + $bh / 2 + 4 ) . '">' . $label . '</text>';
		}
		// bathroom bottom-right
		$s .= '<rect class="nlps-p-r" x="' . ( $w / 2 ) . '" y="' . ( $h * 0.62 + 8 ) . '" width="' . ( $w / 4 - 4 ) . '" height="' . ( $h - 24 - $h * 0.62 ) . '"/>';
		$s .= '<text class="nlps-p-t" x="' . ( $w * 0.56 ) . '" y="' . ( $h * 0.82 ) . '">רחצה</text>';
		// balcony (dashed, outside bottom)
		if ( (int) $balcony_sqm > 0 ) {
			$s .= '<rect x="' . ( $w * 0.75 ) . '" y="' . ( $h * 0.62 + 8 ) . '" width="' . ( $w / 4 - 12 ) . '" height="' . ( $h - 24 - $h * 0.62 ) . '" fill="#F3EEE3" stroke="#9C7A3C" stroke-width="1.4" stroke-dasharray="5 3"/>';
			$s .= '<text class="nlps-p-t" x="' . ( $w * 0.79 ) . '" y="' . ( $h * 0.82 ) . '">מרפסת</text>';
		}
		if ( (int) $size_sqm > 0 ) {
			$s .= '<text class="nlps-p-s" x="14" y="' . ( $h - 2 ) . '">שטח בנוי כ־' . (int) $size_sqm . ' מ״ר · תוכנית להמחשה בלבד</text>';
		}
		$s .= '</svg>';
		return $s;
	}
}

/* ---------------- the content block ---------------- */
if ( ! function_exists( 'nadlan_pshow_render' ) ) {
	function nadlan_pshow_render( $content ) {
		if ( ! is_singular( 'nadlan_property' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
		$id = get_the_ID();
		$g  = function ( $k ) use ( $id ) { return get_post_meta( $id, $k, true ); };

		$price   = (int) $g( 'price' );
		$rooms   = (float) $g( 'rooms' );
		$floor   = (int) $g( 'floor' );
		$tfloors = (int) $g( 'total_floors' );
		$sqm     = (int) $g( 'size_sqm' );
		$ltype   = (string) $g( 'listing_type' ); // sale|rent
		$is_rent = ( $ltype === 'rent' );
		$ppsqm   = ( $price && $sqm && ! $is_rent ) ? (int) round( $price / $sqm ) : 0;
		$lat     = (float) $g( 'lat' ); $lng = (float) $g( 'lng' );
		$demo    = (bool) $g( 'is_demo' );

		ob_start(); ?>
<div class="nlps" dir="rtl">
	<?php if ( $demo ) : ?><div class="nlps-demo">נכס לדוגמה - להמחשת חוויית המודעה. <a href="<?php echo esc_url( home_url( '/post-listing/' ) ); ?>">פרסמו נכס אמיתי חינם ←</a></div><?php endif; ?>

	<h1 class="nlps-title"><?php echo esc_html( get_the_title( $id ) ); ?></h1>

	<?php /* the listing 3D theater (owner 2026-07-07: a listing without 3D
	   "looks broken"): the generic flagship tower, spinnable, honest chip,
	   day/dusk/night light. The floor badge states the REAL floor - no
	   invented hotspot positions on a generic model. */
	$glb = function_exists( 'nadlan_showroom_engine_base_url' ) ? nadlan_showroom_engine_base_url() . 'models/standard-residential.glb' : '';
	if ( $glb ) : ?>
	<div class="nlps-3d" id="nlps-3d" style="background-image:linear-gradient(180deg,rgba(237,242,245,.15),rgba(246,241,230,.35)),url('<?php echo esc_url( content_url( 'uploads/2026/07/nadlan-poster-standard-building.jpg' ) ); ?>');background-size:cover;background-position:center">
		<model-viewer id="nlps-mv" src="<?php echo esc_url( $glb ); ?>" loading="lazy" reveal="auto" camera-controls auto-rotate auto-rotate-delay="700" rotation-per-second="13deg" interaction-prompt="basic" environment-image="neutral" exposure="1.02" shadow-intensity="0.55" camera-target="0 13 0" camera-orbit="-28deg 76deg 46m" min-camera-orbit="auto 48deg 26m" max-camera-orbit="auto 86deg 80m" min-field-of-view="16deg" max-field-of-view="68deg" touch-action="pan-y"></model-viewer>
		<span class="nlps-3d__chip">המחשה כללית של מגורים בבניין - לא הבניין של הנכס</span>
		<?php if ( $floor ) : ?><span class="nlps-3d__floor">קומה <?php echo (int) $floor; ?><?php echo $tfloors ? ' מתוך ' . (int) $tfloors : ''; ?></span><?php endif; ?>
		<span class="nlps-3d__hint">הקישו על הבניין לסיבוב בתלת ממד</span>
		<div class="nlps-3d__light" role="group" aria-label="תאורה">
			<button type="button" data-l="day" aria-pressed="true">יום</button>
			<button type="button" data-l="dusk" aria-pressed="false">שקיעה</button>
			<button type="button" data-l="night" aria-pressed="false">לילה</button>
		</div>
	</div>
	<script>
	(function(){
		var box=document.getElementById("nlps-3d");if(!box)return;
		var mv=document.getElementById("nlps-mv"),exp={day:"1.02",dusk:"0.5",night:"0.25"};
		box.querySelectorAll("[data-l]").forEach(function(b){
			b.addEventListener("click",function(){
				var m=b.dataset.l;
				box.classList.toggle("is-dusk",m==="dusk");box.classList.toggle("is-night",m==="night");
				if(mv)mv.setAttribute("exposure",exp[m]||"1.02");
				box.querySelectorAll("[data-l]").forEach(function(x){x.setAttribute("aria-pressed",String(x===b))});
			});
		});
	})();
	</script>
	<?php endif; ?>

	<div class="nlps-hero">
		<div class="nlps-price">
			<?php if ( $price ) : ?><b><?php echo esc_html( number_format( $price ) ); ?> ₪</b><?php if ( $is_rent ) : ?><span>/ חודש</span><?php endif; ?><?php endif; ?>
			<em><?php echo $is_rent ? 'להשכרה' : 'למכירה'; ?></em>
		</div>
		<dl class="nlps-facts">
			<?php if ( $rooms ) : ?><div><dt>חדרים</dt><dd><?php echo esc_html( rtrim( rtrim( number_format( $rooms, 1 ), '0' ), '.' ) ); ?></dd></div><?php endif; ?>
			<?php if ( $floor || $tfloors ) : ?><div><dt>קומה</dt><dd><?php echo (int) $floor; ?><?php if ( $tfloors ) : ?><span class="nlps-of"> מתוך <?php echo (int) $tfloors; ?></span><?php endif; ?></dd></div><?php endif; ?>
			<?php if ( $sqm ) : ?><div><dt>מ״ר</dt><dd><?php echo (int) $sqm; ?></dd></div><?php endif; ?>
			<?php if ( $ppsqm ) : ?><div><dt>₪ למ״ר</dt><dd><?php echo esc_html( number_format( $ppsqm ) ); ?></dd></div><?php endif; ?>
			<?php if ( $g( 'entry_date' ) ) : ?><div><dt>כניסה</dt><dd><?php echo esc_html( $g( 'entry_date' ) ); ?></dd></div><?php endif; ?>
		</dl>
		<div class="nlps-chips">
			<?php
			$chips = array();
			if ( $g( 'protected_room' ) ) { $chips[] = 'ממ״ד'; }
			if ( $g( 'elevator' ) ) { $chips[] = 'מעלית'; }
			if ( $g( 'parking' ) ) { $chips[] = 'חניה'; }
			if ( $g( 'storage' ) ) { $chips[] = 'מחסן'; }
			if ( $g( 'ac' ) ) { $chips[] = 'מיזוג'; }
			if ( (int) $g( 'balcony_sqm' ) > 0 ) { $chips[] = 'מרפסת ' . (int) $g( 'balcony_sqm' ) . ' מ״ר'; }
			if ( $g( 'condition' ) ) { $chips[] = nadlan_pshow_condition_label( $g( 'condition' ) ); }
			if ( $g( 'direction' ) ) { $chips[] = 'כיוונים: ' . $g( 'direction' ); }
			foreach ( $chips as $c ) { echo '<span class="nlps-chip">' . esc_html( $c ) . '</span>'; }
			?>
		</div>
		<div class="nlps-trust">
			<span>עודכן: <?php echo esc_html( get_the_modified_date( 'j.n.Y', $id ) ); ?></span>
			<button type="button" class="nlps-share" data-url="<?php echo esc_attr( get_permalink( $id ) ); ?>">↗ שיתוף</button>
			<a class="nlps-report" href="mailto:<?php echo esc_attr( get_option( 'admin_email' ) ); ?>?subject=<?php echo rawurlencode( 'דיווח על מודעה: ' . get_the_title( $id ) . ' #' . $id ); ?>">דווחו על טעות</a>
		</div>
	</div>

	<?php
	$hl = array_filter( array_map( 'trim', explode( '|', (string) $g( 'highlights_csv' ) ) ) );
	if ( $hl ) : ?>
	<section class="nlps-hl" aria-label="מה מיוחד בנכס">
		<h2>מה מיוחד כאן?</h2>
		<ul>
			<?php foreach ( array_slice( $hl, 0, 6 ) as $h ) : ?><li><?php echo esc_html( $h ); ?></li><?php endforeach; ?>
		</ul>
	</section>
	<?php endif; ?>

	<?php
	// Default model for EVERY listing: when building data wasn't fed, render a
	// sensible schematic default (4 floors, or enough to contain the listing floor).
	$f_tfloors = $tfloors > 0 ? $tfloors : max( 4, $floor + 1 );
	$f_floor   = ( $floor > 0 || $tfloors > 0 ) ? $floor : 2;
	?>
	<section class="nlps-facade" aria-label="חזית הבניין ותוכנית הדירה">
		<header class="nlps-sec-head">
			<h2>איפה הדירה בבניין?</h2>
			<div class="nlps-toggle" role="tablist">
				<button type="button" class="is-on" data-view="out" role="tab" aria-selected="true">מבט חוץ</button>
				<button type="button" data-view="in" role="tab" aria-selected="false">תוכנית הדירה</button>
				<button type="button" data-view="fp" role="tab" aria-selected="false">🚶 סיור פנימי</button>
			</div>
		</header>
		<div class="nlps-facade-stage">
			<div class="nlps-view nlps-view-out is-on">
				<?php echo nadlan_pshow_facade_svg( $f_tfloors, $f_floor, (int) $g( 'units_per_floor' ), (int) $g( 'unit_position' ) ); // phpcs:ignore ?>
				<p class="nlps-cap">הדירה המוצעת מסומנת בקומה <?php echo (int) $f_floor; ?>. לחצו עליה כדי להיכנס פנימה לתוכנית הדירה. הדמיה סכמטית להמחשה.</p>
			</div>
			<div class="nlps-view nlps-view-in">
				<p class="nlps-plan-title">תוכנית הדירה · קומה <?php echo (int) $f_floor; ?></p>
				<?php echo nadlan_pshow_plan_svg( $rooms, (bool) $g( 'protected_room' ), (int) $g( 'balcony_sqm' ), $sqm ); // phpcs:ignore ?>
				<p class="nlps-cap"><button type="button" class="nlps-backout">← חזרה למבט על הבניין</button></p>
			</div>
			<div class="nlps-view nlps-view-fp">
				<?php if ( function_exists( 'nadlan_interior_fp_html' ) ) { echo nadlan_interior_fp_html( array( 'rooms' => $rooms, 'size_sqm' => $sqm, 'protected_room' => (bool) $g( 'protected_room' ), 'balcony_sqm' => (int) $g( 'balcony_sqm' ), 'direction' => (string) $g( 'direction' ) ) ); } // phpcs:ignore ?>
			</div>
			<div class="nlps-floor-tip" hidden></div>
		</div>
	</section>

	<?php if ( (int) $g( 'arnona_monthly' ) || (int) $g( 'vaad_bayit_monthly' ) || ( $price && ! $is_rent ) ) : ?>
	<section class="nlps-costs" aria-label="עלויות חודשיות">
		<h2>כמה זה עולה בחודש?</h2>
		<div class="nlps-cost-grid">
			<?php if ( $price && ! $is_rent ) :
				// 30y, 5% annual, 75% LTV quick estimate
				$loan = $price * 0.75; $r = 0.05 / 12; $n = 360;
				$pmt  = (int) round( $loan * $r / ( 1 - pow( 1 + $r, -$n ) ) );
			?><div><dt>משכנתא משוערת*</dt><dd><?php echo esc_html( number_format( $pmt ) ); ?> ₪</dd></div><?php endif; ?>
			<?php if ( (int) $g( 'arnona_monthly' ) ) : ?><div><dt>ארנונה</dt><dd><?php echo esc_html( number_format( (int) $g( 'arnona_monthly' ) ) ); ?> ₪</dd></div><?php endif; ?>
			<?php if ( (int) $g( 'vaad_bayit_monthly' ) ) : ?><div><dt>ועד בית</dt><dd><?php echo esc_html( number_format( (int) $g( 'vaad_bayit_monthly' ) ) ); ?> ₪</dd></div><?php endif; ?>
		</div>
		<?php if ( $price && ! $is_rent ) : ?><p class="nlps-cap">* הערכה בלבד: 75% מימון, 30 שנה, 5% ריבית. <a href="<?php echo esc_url( home_url( '/mortgage-calculator/' ) ); ?>">למחשבון המלא ←</a></p><?php endif; ?>
	</section>
	<?php endif; ?>

	<?php if ( $lat && $lng ) :
		$pois = function_exists( 'nadlan_poi_fetch' ) ? nadlan_poi_fetch( $lat, $lng, 1000 ) : array();
		$poi_json = wp_json_encode( array_map( function ( $grp ) {
			return array_values( array_filter( array_slice( (array) $grp, 0, 12 ), function ( $i ) { return ! empty( $i['lat'] ) && ! empty( $i['lng'] ); } ) );
		}, (array) $pois ) );
	?>
	<section class="nlps-map-sec" aria-label="מיקום">
		<h2>מיקום וסביבה - מפה חיה</h2>
		<div class="nlps-poichips" role="group" aria-label="סינון נקודות עניין">
			<button type="button" class="is-on" data-poi="schools">🏫 חינוך</button>
			<button type="button" class="is-on" data-poi="kindergartens">🧒 גנים</button>
			<button type="button" class="is-on" data-poi="parks">🌳 פארקים</button>
			<button type="button" data-poi="transit">🚌 תחבורה</button>
			<button type="button" data-poi="shops">🛒 קניות</button>
			<button type="button" data-poi="health">⚕️ בריאות</button>
			<button type="button" data-poi="food">☕ קפה ואוכל</button>
		</div>
		<div id="nlps-map" data-lat="<?php echo esc_attr( $lat ); ?>" data-lng="<?php echo esc_attr( $lng ); ?>" data-title="<?php echo esc_attr( get_the_title( $id ) ); ?>"></div>
		<script>window.NLPS_POIS = <?php echo $poi_json ? $poi_json : '{}'; // phpcs:ignore ?>;</script>
		<p class="nlps-cap">הקישו על קטגוריה כדי להציג או להסתיר אותה במפה. נתונים חיים מ-OpenStreetMap, מרחקים אוויריים בקירוב. תצוגת לוויין בכפתור השכבות שבמפה.</p>
	</section>
	<?php endif; ?>
</div>
<?php
		return ob_get_clean() . $content;
	}
}
add_filter( 'the_content', 'nadlan_pshow_render', 6 );

/* ---------------- assets ---------------- */
if ( ! function_exists( 'nadlan_pshow_assets' ) ) {
	function nadlan_pshow_assets() {
		if ( ! is_singular( 'nadlan_property' ) ) { return; }
		$id  = get_queried_object_id();
		$has_map = get_post_meta( $id, 'lat', true ) && get_post_meta( $id, 'lng', true );
		if ( $has_map ) {
			wp_enqueue_style( 'leaflet', 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css', array(), '1.9.4' );
			wp_enqueue_script( 'leaflet', 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js', array(), '1.9.4', true );
		}
		wp_register_style( 'nadlan-pshow', false );
		wp_enqueue_style( 'nadlan-pshow' );
		wp_add_inline_style( 'nadlan-pshow', '
.nlps{--ink:#1B1A17;--warm:#6D665C;--gold:#9C7A3C;--terra:#C2563A;--line:#E2DCD0;--band:#F3EEE3;font-family:var(--font-sans,Heebo,system-ui,sans-serif);color:var(--ink);margin:0 0 28px}
.nlps h2{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:1.3rem;margin:0 0 12px}
.nlps-demo{background:var(--band);border:1px solid var(--line);border-inline-start:3px solid var(--gold);border-radius:8px;padding:10px 14px;font-size:13.5px;margin-bottom:16px}
.nlps-demo a{color:var(--gold);font-weight:600;text-decoration:none}
.nlps-hero{border:1px solid var(--line);border-radius:10px;background:#FFFDFC;padding:18px 20px;margin-bottom:18px;box-shadow:0 1px 2px rgba(17,17,15,.04)}
.nlps-title{font-family:"Frank Ruhl Libre",serif;font-size:clamp(1.5rem,3.2vw,2.2rem);line-height:1.25;color:#1B1A17;margin:4px 0 14px}
.nlps-3d{position:relative;height:min(58vh,520px);border-radius:14px;overflow:hidden;background:linear-gradient(180deg,#EDF2F5,#F6F1E6 78%);border:1px solid var(--line,#E2DCD0);margin-bottom:18px;transition:background .6s}
.nlps-3d.is-dusk{background:linear-gradient(180deg,#3E2E33,#1E1A1B 75%)}
.nlps-3d.is-night{background:linear-gradient(180deg,#0C0F16,#14130F 75%)}
.nlps-3d model-viewer{width:100%;height:100%;transition:filter .6s;--poster-color:transparent;background-color:transparent}
.nlps-3d.is-dusk model-viewer{filter:sepia(.35) saturate(.85) brightness(.8) contrast(1.04)}
.nlps-3d.is-night model-viewer{filter:brightness(.5) saturate(.6) contrast(1.08)}
.nlps-3d__chip{position:absolute;top:12px;inset-inline-start:12px;background:rgba(20,19,15,.82);color:#E9D9A8;font:600 11.5px/1 Heebo,sans-serif;padding:7px 11px;border-radius:999px;border:1px solid rgba(233,217,168,.4);pointer-events:none}
.nlps-3d__floor{position:absolute;bottom:12px;inset-inline-start:12px;background:#FAF7F1;color:#1B1A17;font:700 12.5px/1 Heebo,sans-serif;padding:8px 12px;border-radius:999px;border:1px solid #D6C189}
.nlps-3d__light{position:absolute;top:12px;inset-inline-end:12px;display:inline-flex;gap:4px;background:rgba(250,247,241,.92);border:1px solid #E2DCD0;border-radius:11px;padding:4px}
.nlps-3d__light button{font:600 12px/1 Heebo,sans-serif;color:#51483A;background:transparent;border:0;border-radius:8px;padding:7px 11px;cursor:pointer}
.nlps-3d__light button[aria-pressed="true"]{background:#1B1A17;color:#FAF7F1}
.nlps-3d__hint{position:absolute;bottom:12px;inset-inline-end:12px;background:rgba(20,19,15,.75);color:#F5EFE2;font:600 11.5px/1 Heebo,sans-serif;padding:8px 12px;border-radius:999px;pointer-events:none}
.nlps-3d model-viewer::part(default-progress-bar){display:none}
.nlps-price{display:flex;align-items:baseline;gap:10px;margin-bottom:12px}
.nlps-price b{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:2rem;letter-spacing:-.01em}
.nlps-price span{color:var(--warm);font-size:.95rem}
.nlps-price em{font-style:normal;font-size:11px;font-weight:700;letter-spacing:.08em;background:var(--ink);color:#fff;border-radius:4px;padding:3px 9px;margin-inline-start:auto}
.nlps-facts{display:flex;flex-wrap:wrap;gap:22px;margin:0;padding:12px 0 0;border-top:1px solid var(--line)}
.nlps-facts dt{font-size:11px;color:var(--warm);margin:0}
.nlps-facts dd{font-size:17px;font-weight:700;margin:2px 0 0}
.nlps-of{font-size:12px;color:var(--warm);font-weight:400}
.nlps-chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:14px}
.nlps-chip{font-size:12px;border:1px solid var(--line);background:var(--band);border-radius:999px;padding:4px 11px}
.nlps-facade,.nlps-costs,.nlps-map-sec{border:1px solid var(--line);border-radius:10px;background:#FFFDFC;padding:18px 20px;margin-bottom:18px}
.nlps-sec-head{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.nlps-toggle{display:flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.nlps-toggle button{font:inherit;font-size:12.5px;border:0;background:#fff;color:var(--warm);padding:7px 14px;cursor:pointer}
.nlps-toggle button.is-on{background:var(--ink);color:#fff}
.nlps-facade-stage{position:relative;margin-top:8px}
.nlps-view{display:none}.nlps-view.is-on{display:block}
.nlps-facade-svg{display:block;max-width:340px;margin:0 auto;max-height:460px}
.nlps-plan-svg{display:block;max-width:360px;margin:0 auto}
.nlps-cap{font-size:11.5px;color:var(--warm);text-align:center;margin:10px 0 0}
.nlps-cap a{color:var(--gold)}
.nlps-floor-tip{position:absolute;top:8px;inset-inline-start:8px;background:var(--ink);color:#fff;font-size:12px;border-radius:6px;padding:5px 10px;pointer-events:none}
.nlps-cost-grid{display:flex;flex-wrap:wrap;gap:26px}
.nlps-cost-grid dt{font-size:11.5px;color:var(--warm)}
.nlps-cost-grid dd{font-size:18px;font-weight:700;margin:2px 0 0}
#nlps-map{height:320px;border-radius:8px;border:1px solid var(--line)}
.nlps-poichips{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 10px}
.nlps-poichips button{font:600 12.5px/1 Heebo,sans-serif;border:1px solid var(--line);background:#fff;color:#6D665C;border-radius:999px;padding:8px 13px;cursor:pointer;min-height:34px}
.nlps-poichips button.is-on{background:#1B1A17;border-color:#1B1A17;color:#F4EEDE}
.nlps-trust{display:flex;align-items:center;gap:16px;margin-top:12px;padding-top:10px;border-top:1px solid var(--line);font-size:12px;color:var(--warm)}
.nlps-share{font:inherit;font-size:12px;border:1px solid var(--line);background:#fff;border-radius:999px;padding:4px 12px;cursor:pointer;color:var(--ink)}
.nlps-report{color:var(--warm);margin-inline-start:auto}
.nlps-hl{border:1px solid var(--line);border-radius:10px;background:#FFFDFC;padding:18px 20px;margin-bottom:18px}
.nlps-hl ul{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:8px 18px}
.nlps-hl li{position:relative;padding-inline-start:20px;font-size:14px}
.nlps-hl li::before{content:"◆";position:absolute;inset-inline-start:0;color:var(--gold);font-size:11px;top:3px}
.nlps-plan-title{text-align:center;font-weight:700;font-size:14px;margin:0 0 6px}
.nlps-backout{font:inherit;font-size:12.5px;border:0;background:none;color:var(--gold);cursor:pointer;text-decoration:underline}
.nlps-f-sel{cursor:zoom-in}
@media(max-width:560px){.nlps-price b{font-size:1.5rem}.nlps-facts{gap:16px}}
' );
		wp_register_script( 'nadlan-pshow-js', false, $has_map ? array( 'leaflet' ) : array(), '1.69.70', true );
		wp_enqueue_script( 'nadlan-pshow-js' );
		wp_add_inline_script( 'nadlan-pshow-js', '
(function(){
	document.addEventListener("DOMContentLoaded",function(){
		var root=document.querySelector(".nlps");if(!root){return}
		// facade / plan toggle
		root.querySelectorAll(".nlps-toggle button").forEach(function(b){
			b.addEventListener("click",function(){
				root.querySelectorAll(".nlps-toggle button").forEach(function(x){x.classList.toggle("is-on",x===b);x.setAttribute("aria-selected",x===b?"true":"false")});
				root.querySelectorAll(".nlps-view").forEach(function(v){v.classList.remove("is-on")});
				var t=root.querySelector(".nlps-view-"+b.dataset.view);if(t){t.classList.add("is-on");if(b.dataset.view==="fp"&&window.nadlanInitFP){window.nadlanInitFP()}}
			});
		});
		// floor click: selected floor = enter the apartment (slice inspect); others = tooltip
		var tip=root.querySelector(".nlps-floor-tip");
		function setView(v){
			root.querySelectorAll(".nlps-toggle button").forEach(function(x){x.classList.toggle("is-on",x.dataset.view===v);x.setAttribute("aria-selected",x.dataset.view===v?"true":"false")});
			root.querySelectorAll(".nlps-view").forEach(function(x){x.classList.remove("is-on")});
			var t=root.querySelector(".nlps-view-"+v);if(t){t.classList.add("is-on")}
		}
		root.querySelectorAll(".nlps-f-fl").forEach(function(fl){
			fl.addEventListener("click",function(){
				var f=fl.dataset.floor,sel=fl.classList.contains("nlps-f-sel");
				if(sel){setView("in");return}
				if(!tip){return}
				tip.textContent="קומה "+f;
				tip.hidden=false;clearTimeout(tip._t);tip._t=setTimeout(function(){tip.hidden=true},2200);
			});
		});
		var back=root.querySelector(".nlps-backout");
		if(back){back.addEventListener("click",function(){setView("out")});}
		// share
		var sh=root.querySelector(".nlps-share");
		if(sh){sh.addEventListener("click",function(){
			var u=sh.dataset.url;
			if(navigator.share){navigator.share({title:document.title,url:u}).catch(function(){})}
			else{navigator.clipboard&&navigator.clipboard.writeText(u);sh.textContent="✓ הקישור הועתק";setTimeout(function(){sh.textContent="↗ שיתוף"},2000)}
		});}
		// single-listing map: streets + satellite layers, listing marker, live POI markers
		var m=document.getElementById("nlps-map");
		if(m&&window.L){
			var lat=parseFloat(m.dataset.lat),lng=parseFloat(m.dataset.lng);
			var streets=L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png",{attribution:"&copy; OpenStreetMap"});
			var sat=L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",{attribution:"Esri World Imagery"});
			var map=L.map(m,{scrollWheelZoom:false,layers:[streets]}).setView([lat,lng],15);
			L.control.layers({"מפה":streets,"לוויין":sat},null,{position:"topleft"}).addTo(map);
			L.marker([lat,lng]).addTo(map).bindPopup("<b>"+(m.dataset.title||"")+"</b>").openPopup();
			var P=window.NLPS_POIS||{},style={schools:["#334236","🏫"],kindergartens:["#9C7A3C","🧒"],parks:["#517048","🌳"],transit:["#183C3C","🚌"],shops:["#9F6F54","🛒"],health:["#A93F2A","⚕️"],food:["#8A6B3F","☕"]};
			// REAL category filtering: one layerGroup per category, chips toggle them
			var poiLayers={};
			function dlab(d){if(!d){return ""}if(d>=1000){return "<br><span style=\"color:#9C7A3C;font-size:12px\">כ-"+(Math.round(d/100)/10)+" ק\"מ מהנכס</span>"}return "<br><span style=\"color:#9C7A3C;font-size:12px\">כ-"+(Math.max(50,Math.round(d/50)*50))+" מטר מהנכס</span>"}
			Object.keys(P).forEach(function(k){
				var grp=L.layerGroup();
				(P[k]||[]).forEach(function(p){
					if(!p.lat||!p.lng){return}
					L.circleMarker([p.lat,p.lng],{radius:6,color:(style[k]||["#666"])[0],weight:2,fillColor:"#fff",fillOpacity:.9})
						.bindPopup("<b>"+(style[k]?style[k][1]+" ":"")+(p.name||"")+"</b>"+dlab(p.d)).addTo(grp);
				});
				poiLayers[k]=grp;
			});
			var chips=document.querySelectorAll(".nlps-poichips button");
			chips.forEach(function(b){
				var k=b.dataset.poi,grp=poiLayers[k],n=grp?grp.getLayers().length:0;
				b.textContent=b.textContent+" ("+n+")";
				if(!n){b.style.opacity=".45";b.classList.remove("is-on");return}
				if(b.classList.contains("is-on")){grp.addTo(map)}
				b.addEventListener("click",function(){
					var on=b.classList.toggle("is-on");
					if(on){grp.addTo(map)}else{map.removeLayer(grp)}
				});
			});
		}
	});
})();
' );
	}
}
add_action( 'wp_enqueue_scripts', 'nadlan_pshow_assets' );

/* the listing 3D theater needs the model-viewer runtime (same version the engine pins) */
add_action( 'wp_enqueue_scripts', function () {
	if ( ! is_singular( 'nadlan_property' ) ) { return; }
	wp_enqueue_script( 'nadlan-model-viewer', 'https://ajax.googleapis.com/ajax/libs/model-viewer/4.3.1/model-viewer.min.js', array(), '4.3.1', true );
	wp_script_add_data( 'nadlan-model-viewer', 'type', 'module' );
} );

/* Demo listings are showcase-only: keep them out of Google regardless of body length. */
if ( ! function_exists( 'nadlan_pshow_demo_noindex' ) ) {
	function nadlan_pshow_demo_noindex( $robots ) {
		if ( is_singular( 'nadlan_property' ) && get_post_meta( get_queried_object_id(), 'is_demo', true ) ) {
			$robots['noindex'] = true; $robots['follow'] = true;
		}
		return $robots;
	}
}
add_filter( 'wp_robots', 'nadlan_pshow_demo_noindex', 20 );

/* ---------------- SEO: archive title + listing meta description ---------------- */
if ( ! function_exists( 'nadlan_pshow_archive_title' ) ) {
	function nadlan_pshow_archive_title( $title ) {
		if ( is_post_type_archive( 'nadlan_property' ) ) { return 'דירות למכירה ולהשכרה בישראל - לוח נדל"ן | נדלן'; }
		return $title;
	}
}
add_filter( 'wpseo_title', 'nadlan_pshow_archive_title', 20 );
add_filter( 'document_title_parts', function ( $parts ) {
	if ( is_post_type_archive( 'nadlan_property' ) ) { $parts['title'] = 'דירות למכירה ולהשכרה בישראל - לוח נדל"ן'; }
	return $parts;
}, 20 );

if ( ! function_exists( 'nadlan_pshow_meta_desc' ) ) {
	function nadlan_pshow_meta_desc( $desc ) {
		if ( ! is_singular( 'nadlan_property' ) || $desc ) { return $desc; }
		$id = get_queried_object_id();
		$g  = function ( $k ) use ( $id ) { return get_post_meta( $id, $k, true ); };
		$bits  = array();
		$rooms = (float) $g( 'rooms' );
		$deal  = $g( 'listing_type' ) === 'rent' ? 'להשכרה' : 'למכירה';
		$bits[] = 'דירת ' . ( $rooms ? rtrim( rtrim( number_format( $rooms, 1 ), '0' ), '.' ) . ' חדרים ' : '' ) . $deal
			. ( $g( 'city' ) ? ' ב' . $g( 'city' ) : '' ) . ( $g( 'street' ) ? ', רחוב ' . $g( 'street' ) : '' ) . '.';
		if ( (int) $g( 'size_sqm' ) ) { $bits[] = (int) $g( 'size_sqm' ) . ' מ"ר, קומה ' . (int) $g( 'floor' ) . '.'; }
		if ( (int) $g( 'price' ) ) { $bits[] = number_format( (int) $g( 'price' ) ) . ' ₪' . ( $g( 'listing_type' ) === 'rent' ? ' לחודש' : '' ) . '.'; }
		$bits[] = 'כל הפרטים, מפה חיה וסביבת מגורים - בנדלן.';
		return mb_substr( implode( ' ', $bits ), 0, 156 );
	}
}
add_filter( 'wpseo_metadesc', 'nadlan_pshow_meta_desc', 20 );
