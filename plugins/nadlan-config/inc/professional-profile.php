<?php
/**
 * nadlan-config — World-class professional profile layer (v1.69.82)
 *
 * Owner directive 2026-07-02: single professional pages were "very basic".
 * This module adds a Zillow-agent/Houzz-class rich profile on top of the
 * existing directory (2,711 gov.il-verified records, ratings, tiers, claim):
 *   1. Profile hero: brand monogram portrait (parametric SVG — elegant, honest,
 *      no fake photos), name, profession pill, city, gov.il verified badge,
 *      rating, years/projects stats, tier-aware contact CTAs.
 *   2. Expertise band: specialties + languages chips, service areas.
 *   3. WIRED TO EVERYTHING: their projects (developer/contractor name match),
 *      colleagues nearby (same profession/city), profession-matched guides,
 *      calculators — hub-spoke in both directions.
 *   4. Extends the profession taxonomy: designers, engineers, accountants,
 *      surveyors, property managers, urban planners (the "go for all" ask).
 *   5. Demo premium profiles supported: is_demo flag → visible "לדוגמה" tag +
 *      noindex (same honest pattern as demo listings).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---------------- extra professions (merge into the directory taxonomy) ---------------- */
add_filter( 'nadlan_dir_professions', function ( $p ) { return $p; } ); // future-proof hook
if ( ! function_exists( 'nadlan_prof_extra_professions' ) ) {
	function nadlan_prof_extra_professions() {
		return array(
			'interior_designer' => array( 'label' => 'מעצב/ת פנים',      'color' => '#9F6F54', 'soft' => '#F8F0EA', 'icon' => 'profession-architect' ),
			'engineer'          => array( 'label' => 'מהנדס/ת בניין',    'color' => '#183C3C', 'soft' => '#EFF4F4', 'icon' => 'profession-inspector' ),
			'accountant'        => array( 'label' => 'רו״ח מיסוי נדל״ן', 'color' => '#11110F', 'soft' => '#EFEDE7', 'icon' => 'profession-lawyer' ),
			'surveyor'          => array( 'label' => 'מודד/ת מוסמך',     'color' => '#334236', 'soft' => '#F1F4EE', 'icon' => 'profession-appraiser' ),
			'property_manager'  => array( 'label' => 'ניהול נכסים',      'color' => '#9C7A3C', 'soft' => '#FBF6EE', 'icon' => 'profession-broker' ),
			'urban_planner'     => array( 'label' => 'מתכנן/ת ערים',     'color' => '#2E2B26', 'soft' => '#F3EEE3', 'icon' => 'profession-architect' ),
		);
	}
}

if ( ! function_exists( 'nadlan_prof_meta_of' ) ) {
	function nadlan_prof_meta_of( $key ) {
		$all = function_exists( 'nadlan_dir_professions' ) ? nadlan_dir_professions() : array();
		$all = array_merge( $all, nadlan_prof_extra_professions() );
		return isset( $all[ $key ] ) ? $all[ $key ] : array( 'label' => $key ?: 'בעל/ת מקצוע', 'color' => '#1B1A17', 'soft' => '#F3EEE3', 'icon' => 'profession-contractor' );
	}
}

/* ---------------- extra profile meta ---------------- */
if ( ! function_exists( 'nadlan_prof_register_meta' ) ) {
	function nadlan_prof_register_meta() {
		foreach ( array( 'specialties_csv' => 'string', 'languages_csv' => 'string', 'bio' => 'string', 'response_time' => 'string', 'meeting_url' => 'string', 'lat' => 'number', 'lng' => 'number', 'profile_views' => 'integer' ) as $k => $t ) {
			register_post_meta( 'nadlan_professional', $k, array(
				'show_in_rest' => true, 'single' => true, 'type' => $t,
				'auth_callback' => function ( $a, $m, $pid ) { return current_user_can( 'edit_post', (int) $pid ); },
			) );
		}
	}
}
add_action( 'init', 'nadlan_prof_register_meta', 15 );

/* ---------------- brand monogram portrait (design-consistent "generic picture") ---------------- */
if ( ! function_exists( 'nadlan_prof_monogram_svg' ) ) {
	function nadlan_prof_monogram_svg( $name, $color ) {
		$parts = preg_split( '/\s+/u', trim( (string) $name ) );
		$ini   = mb_substr( $parts[0] ?? '', 0, 1 ) . ( isset( $parts[1] ) ? '.' . mb_substr( $parts[1], 0, 1 ) : '' );
		return '<svg class="nlpp-avatar" viewBox="0 0 96 96" role="img" aria-label="' . esc_attr( $name ) . '">'
			. '<circle cx="48" cy="48" r="46" fill="#FFFDFC" stroke="' . esc_attr( $color ) . '" stroke-width="2"/>'
			. '<circle cx="48" cy="48" r="40" fill="' . esc_attr( $color ) . '"/>'
			. '<path d="M20 14 A46 46 0 0 1 76 14" fill="none" stroke="#9C7A3C" stroke-width="2.4" stroke-linecap="round"/>'
			. '<text x="48" y="58" text-anchor="middle" font-family="\'Frank Ruhl Libre\',serif" font-size="30" font-weight="700" fill="#FAF8F3">' . esc_html( $ini ) . '</text>'
			. '</svg>';
	}
}

/* ---------------- profession → guide/calculator wiring map ---------------- */
if ( ! function_exists( 'nadlan_prof_related_links' ) ) {
	function nadlan_prof_related_links( $prof ) {
		$map = array(
			'lawyer'     => array( array( '/real-estate-lawyer/', 'מתי חובה עורך דין בעסקה' ), array( '/purchase-tax-calculator/', 'מחשבון מס רכישה' ) ),
			'shamai'     => array( array( '/real-estate-appraiser/', 'מה שמאי בודק ולמה' ), array( '/property-value/', 'איך מעריכים שווי דירה' ) ),
			'mashkanta'  => array( array( '/mortgage-calculator/', 'מחשבון משכנתא' ), array( '/mortgage-advisor/', 'האם צריך יועץ משכנתאות' ) ),
			'bedek_bait' => array( array( '/home-inspection/', 'בדק בית — המדריך' ), array( '/buying-apartment/', 'מדריך קניית דירה' ) ),
			'kablan'     => array( array( '/projects/', 'פרויקטים חדשים' ), array( '/buying-apartment/', 'קנייה מקבלן — הזכויות שלכם' ) ),
			'metavech'   => array( array( '/real-estate-broker/', 'עבודה נכונה עם מתווך' ), array( '/properties/', 'דירות למכירה ולהשכרה' ) ),
		);
		$base = isset( $map[ $prof ] ) ? $map[ $prof ] : array( array( '/buying-apartment/', 'מדריך קניית דירה' ), array( '/glossary/', 'מילון מונחי נדל״ן' ) );
		return $base;
	}
}

/* ---------------- the rich profile (renders ABOVE the legacy facts card) ---------------- */
if ( ! function_exists( 'nadlan_prof_render' ) ) {
	function nadlan_prof_render( $content ) {
		if ( ! is_singular( 'nadlan_professional' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
		$id = get_the_ID();
		$g  = function ( $k ) use ( $id ) { return get_post_meta( $id, $k, true ); };
		$pm   = nadlan_prof_meta_of( (string) $g( 'profession' ) );
		$name = get_the_title( $id );
		$city = (string) $g( 'city' );
		$rating = (float) $g( 'rating' ); $reviews = (int) $g( 'reviews_count' );
		$years  = (int) $g( 'years_active' ); $projects_n = (int) $g( 'project_count' );
		$demo   = (bool) $g( 'is_demo' );
		$show_contact = function_exists( 'nadlan_tier_can_show' ) ? nadlan_tier_can_show( $id, 'phone' ) : false;
		$phone  = $show_contact ? (string) $g( 'phone' ) : '';
		$wa     = preg_replace( '/\D+/', '', (string) get_option( 'nadlan_whatsapp_e164', '' ) );

		// their projects: developer/contractor name match (real wiring, cached)
		$their = get_transient( 'nlpp_projects_' . $id );
		if ( ! is_array( $their ) ) {
			$their = array();
			if ( mb_strlen( $name ) > 3 ) {
				$q = new WP_Query( array(
					'post_type' => 'nadlan_project', 'post_status' => 'publish', 'posts_per_page' => 4,
					'no_found_rows' => true, 'fields' => 'ids',
					'meta_query' => array( 'relation' => 'OR',
						array( 'key' => 'developer_name', 'value' => $name, 'compare' => 'LIKE' ),
						array( 'key' => 'contractor_name', 'value' => $name, 'compare' => 'LIKE' ),
					),
				) );
				foreach ( $q->posts as $pid ) { $their[] = array( 'title' => get_the_title( $pid ), 'url' => get_permalink( $pid ) ); }
			}
			set_transient( 'nlpp_projects_' . $id, $their, 12 * HOUR_IN_SECONDS );
		}

		// live view counter (debounced per IP, real FOMO surface)
		$ipk = 'nlppv_' . md5( ( $_SERVER['REMOTE_ADDR'] ?? 'x' ) . $id );
		if ( ! get_transient( $ipk ) ) {
			set_transient( $ipk, 1, 6 * HOUR_IN_SECONDS );
			update_post_meta( $id, 'profile_views', (int) $g( 'profile_views' ) + 1 );
		}
		$views   = (int) $g( 'profile_views' );
		$tier    = (string) $g( 'paid_tier' );
		$premium = in_array( $tier, array( 'pro', 'premier' ), true ) || $demo;
		$meeting = (string) $g( 'meeting_url' );
		$plat = (float) $g( 'lat' ); $plng = (float) $g( 'lng' );
		$ai_on = function_exists( 'nadlan_ai_enabled' ) && nadlan_ai_enabled();
		$specialties = array_filter( array_map( 'trim', explode( ',', (string) $g( 'specialties_csv' ) ) ) );
		$langs       = array_filter( array_map( 'trim', explode( ',', (string) $g( 'languages_csv' ) ) ) );
		$areas       = array_filter( array_map( 'trim', explode( ',', (string) $g( 'areas_served' ) ) ) );
		$links       = nadlan_prof_related_links( (string) $g( 'profession' ) );

		ob_start(); ?>
<div class="nlpp" dir="rtl" style="--pc:<?php echo esc_attr( $pm['color'] ); ?>;--ps:<?php echo esc_attr( $pm['soft'] ); ?>">
	<?php if ( $demo ) : ?><div class="nlpp-demo">פרופיל לדוגמה — כך נראה פרופיל פרימיום. <a href="<?php echo esc_url( home_url( '/advertise/' ) ); ?>">בעלי מקצוע: הצטרפו ←</a></div><?php endif; ?>

	<header class="nlpp-hero">
		<?php echo nadlan_prof_monogram_svg( $name, $pm['color'] ); // phpcs:ignore ?>
		<div class="nlpp-id">
			<span class="nlpp-pill"><?php echo esc_html( $pm['label'] ); ?></span>
			<h2 class="nlpp-name"><?php echo esc_html( $name ); ?></h2>
			<div class="nlpp-sub">
				<?php if ( $city ) : ?><span><?php echo esc_html( $city ); ?></span><?php endif; ?>
				<?php if ( $g( 'registry_number' ) || $g( 'license_number' ) ) : ?><span class="nlpp-ver">✓ מאומת ברשם (gov.il)</span><?php endif; ?>
				<?php if ( $rating > 0 ) : ?><span class="nlpp-stars" aria-label="דירוג <?php echo esc_attr( $rating ); ?>">★ <?php echo esc_html( number_format( $rating, 1 ) ); ?><?php echo $reviews ? ' (' . (int) $reviews . ')' : ''; ?></span><?php endif; ?>
			</div>
		</div>
		<div class="nlpp-ctas">
			<?php if ( $wa ) : ?><a class="nlpp-btn nlpp-wa" target="_blank" rel="noopener" href="https://wa.me/<?php echo esc_attr( $wa ); ?>?text=<?php echo rawurlencode( 'היי, אשמח לחיבור אל ' . $name . ' דרך האתר' ); ?>">פנייה בוואטסאפ</a><?php endif; ?>
			<?php if ( $phone ) : ?><a class="nlpp-btn nlpp-tel" href="tel:<?php echo esc_attr( preg_replace( '/[^0-9+]/', '', $phone ) ); ?>">התקשרו</a>
			<?php else : ?><a class="nlpp-btn nlpp-tel" href="#nlcard-claim">קבלו הצעת מחיר</a><?php endif; ?>
			<?php if ( $premium ) : ?>
				<?php if ( $meeting ) : ?><a class="nlpp-btn nlpp-vid" target="_blank" rel="noopener" href="<?php echo esc_url( $meeting ); ?>">🎥 פגישת וידאו</a>
				<?php else : ?><button type="button" class="nlpp-btn nlpp-vid" data-nlpp-meet>🎥 תיאום שיחת וידאו</button><?php endif; ?>
			<?php endif; ?>
		</div>
	</header>

	<div class="nlpp-stats">
		<?php if ( $years ) : ?><div><b><?php echo (int) $years; ?>+</b><span>שנות ניסיון</span></div><?php endif; ?>
		<?php if ( $projects_n ) : ?><div><b><?php echo number_format( $projects_n ); ?></b><span>פרויקטים</span></div><?php endif; ?>
		<?php if ( $g( 'classification' ) ) : ?><div><b><?php echo esc_html( $g( 'classification' ) ); ?></b><span>סיווג רשמי</span></div><?php endif; ?>
		<?php if ( $g( 'response_time' ) ) : ?><div><b><?php echo esc_html( $g( 'response_time' ) ); ?></b><span>זמן מענה ממוצע</span></div><?php endif; ?>
	</div>

	<?php if ( $g( 'bio' ) ) : ?><p class="nlpp-bio"><?php echo esc_html( $g( 'bio' ) ); ?></p><?php endif; ?>

	<?php if ( $specialties || $langs || $areas ) : ?>
	<div class="nlpp-chips">
		<?php foreach ( $specialties as $sp ) : ?><a class="nlpp-chip" href="<?php echo esc_url( home_url( '/professionals/?q=' . rawurlencode( $sp ) ) ); ?>"><?php echo esc_html( $sp ); ?></a><?php endforeach; ?>
		<?php foreach ( $langs as $l ) : ?><span class="nlpp-chip nlpp-lang">🌐 <?php echo esc_html( $l ); ?></span><?php endforeach; ?>
		<?php foreach ( array_slice( $areas, 0, 6 ) as $a ) : ?><span class="nlpp-chip nlpp-area">📍 <?php echo esc_html( $a ); ?></span><?php endforeach; ?>
	</div>
	<?php endif; ?>

	<?php if ( $views >= 5 ) : ?><p class="nlpp-fomo">👁 <?php echo number_format( $views ); ?> צפיות בפרופיל · <?php echo $g( 'response_time' ) ? 'מענה ' . esc_html( $g( 'response_time' ) ) : 'זמינות גבוהה'; ?></p><?php endif; ?>

	<?php if ( $premium && ! $meeting ) : ?>
	<form class="nlpp-meet" id="nlpp-meet" hidden data-rest="<?php echo esc_attr( rest_url( 'nadlan/v1/lead' ) ); ?>" data-prof="<?php echo esc_attr( $name ); ?>">
		<b>תיאום שיחת וידאו עם <?php echo esc_html( $name ); ?></b>
		<div class="nlpp-meet-row">
			<input type="text" name="name" placeholder="שם" required>
			<input type="tel" name="phone" placeholder="טלפון" required>
			<input type="text" name="slot" placeholder="מועד מועדף (למשל: מחר 17:00)">
		</div>
		<input type="text" name="company" class="nlpp-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
		<button type="submit" class="nlpp-btn nlpp-vid">שלחו בקשה</button>
		<span class="nlpp-meet-msg" aria-live="polite"></span>
	</form>
	<?php endif; ?>

	<?php if ( $plat && $plng ) : ?>
	<section class="nlpp-sec"><h3>אזור פעילות</h3>
		<div id="nlpp-map" data-lat="<?php echo esc_attr( $plat ); ?>" data-lng="<?php echo esc_attr( $plng ); ?>" data-title="<?php echo esc_attr( $name ); ?>"></div>
	</section>
	<?php endif; ?>

	<?php if ( $premium && $ai_on ) : ?>
	<section class="nlpp-sec nlpp-ai" data-rest="<?php echo esc_attr( rest_url( 'nadlan/v1/concierge' ) ); ?>" data-prof="<?php echo esc_attr( $pm['label'] ); ?>">
		<h3>✨ שאלו את ה-AI על <?php echo esc_html( $pm['label'] ); ?></h3>
		<p class="nlpp-ai-hint">למשל: מה בודקים לפני שסוגרים עם <?php echo esc_html( $pm['label'] ); ?>? כמה זה עולה בדרך כלל?</p>
		<div class="nlpp-ai-row"><input type="text" id="nlpp-ai-q" placeholder="שאלה חופשית..."><button type="button" class="nlpp-btn nlpp-tel" id="nlpp-ai-send">שאלו</button></div>
		<div class="nlpp-ai-a" id="nlpp-ai-a" hidden aria-live="polite"></div>
	</section>
	<?php endif; ?>

	<?php if ( $their ) : ?>
	<section class="nlpp-sec"><h3>פרויקטים באתר</h3>
		<ul class="nlpp-list"><?php foreach ( $their as $t ) : ?><li><a href="<?php echo esc_url( $t['url'] ); ?>"><?php echo esc_html( $t['title'] ); ?> ←</a></li><?php endforeach; ?></ul>
	</section>
	<?php endif; ?>

	<section class="nlpp-sec"><h3>כלים ומדריכים רלוונטיים</h3>
		<ul class="nlpp-list"><?php foreach ( $links as $l ) : ?><li><a href="<?php echo esc_url( home_url( $l[0] ) ); ?>"><?php echo esc_html( $l[1] ); ?> ←</a></li><?php endforeach; ?></ul>
	</section>
</div>
<?php
		return ob_get_clean() . $content;
	}
}
add_filter( 'the_content', 'nadlan_prof_render', 6 );

/* demo profiles: honest tag above + keep out of Google (extends the listings pattern) */
add_filter( 'wp_robots', function ( $robots ) {
	if ( is_singular( 'nadlan_professional' ) && get_post_meta( get_queried_object_id(), 'is_demo', true ) ) {
		$robots['noindex'] = true; $robots['follow'] = true;
	}
	return $robots;
}, 20 );

/* ---------------- styles ---------------- */
if ( ! function_exists( 'nadlan_prof_assets' ) ) {
	function nadlan_prof_assets() {
		if ( ! is_singular( 'nadlan_professional' ) ) { return; }
		$pid = get_queried_object_id();
		if ( get_post_meta( $pid, 'lat', true ) && get_post_meta( $pid, 'lng', true ) ) {
			wp_enqueue_style( 'leaflet', 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css', array(), '1.9.4' );
			wp_enqueue_script( 'leaflet', 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js', array(), '1.9.4', true );
		}
		wp_register_style( 'nadlan-nlpp', false );
		wp_enqueue_style( 'nadlan-nlpp' );
		wp_add_inline_style( 'nadlan-nlpp', '
.nlpp{--ink:#1B1A17;--warm:#6D665C;--gold:#9C7A3C;--line:#E2DCD0;font-family:var(--font-sans,Heebo,system-ui,sans-serif);color:var(--ink);margin-bottom:26px}
.nlpp-demo{background:#F3EEE3;border:1px solid var(--line);border-inline-start:3px solid var(--gold);border-radius:8px;padding:10px 14px;font-size:13.5px;margin-bottom:16px}
.nlpp-demo a{color:var(--gold);font-weight:700;text-decoration:none}
.nlpp-hero{display:flex;align-items:center;gap:18px;flex-wrap:wrap;border:1px solid var(--line);border-radius:14px;background:#FFFDFC;padding:22px;box-shadow:0 1px 2px rgba(17,17,15,.04)}
.nlpp-avatar{width:88px;height:88px;flex-shrink:0}
.nlpp-id{flex:1;min-width:200px}
.nlpp-pill{display:inline-block;font-size:11.5px;font-weight:700;color:#fff;background:var(--pc,var(--ink));border-radius:999px;padding:4px 12px}
.nlpp-name{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:1.7rem;margin:8px 0 6px;line-height:1.15}
.nlpp-sub{display:flex;flex-wrap:wrap;gap:12px;font-size:13px;color:var(--warm)}
.nlpp-ver{color:#334236;font-weight:700}
.nlpp-stars{color:var(--gold);font-weight:700}
.nlpp-ctas{display:flex;gap:8px;flex-wrap:wrap}
.nlpp-btn{font-size:13.5px;font-weight:700;border-radius:10px;padding:11px 18px;text-decoration:none;min-height:44px;display:inline-flex;align-items:center}
.nlpp-wa{background:#1f8a4c;color:#fff}.nlpp-tel{background:var(--ink);color:#fff}
.nlpp-vid{background:var(--pc,#183C3C);color:#fff;border:0;cursor:pointer;font-family:inherit}
.nlpp-fomo{font-size:12.5px;color:var(--warm);margin:0 0 14px}
.nlpp-meet{border:1px solid var(--line);border-radius:12px;background:#FAF8F3;padding:16px;margin-bottom:14px}
.nlpp-meet-row{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}
.nlpp-meet input{flex:1;min-width:130px;font:inherit;font-size:14px;border:1px solid var(--line);border-radius:8px;padding:10px 12px;background:#fff}
.nlpp-hp{position:absolute!important;left:-9999px}
.nlpp-meet-msg{display:block;margin-top:8px;font-size:13px;color:#334236}
#nlpp-map{height:200px;border-radius:10px;border:1px solid var(--line)}
.nlpp-ai-row{display:flex;gap:8px}
.nlpp-ai-row input{flex:1;font:inherit;font-size:14px;border:1px solid var(--line);border-radius:8px;padding:10px 12px;background:#fff}
.nlpp-ai-hint{font-size:12.5px;color:var(--warm);margin:0 0 10px}
.nlpp-ai-a{margin-top:12px;background:#FAF8F3;border:1px solid var(--line);border-radius:10px;padding:12px 14px;font-size:14px;line-height:1.65}
a.nlpp-chip{text-decoration:none;color:var(--ink)}a.nlpp-chip:hover{border-color:var(--gold);color:var(--gold)}
.nlpp-stats{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0}
.nlpp-stats>div{flex:1;min-width:120px;text-align:center;border:1px solid var(--line);border-radius:10px;background:#FAF8F3;padding:12px 8px}
.nlpp-stats b{display:block;font-size:1.25rem;font-family:var(--font-serif,serif)}
.nlpp-stats span{font-size:11.5px;color:var(--warm)}
.nlpp-bio{font-size:15px;line-height:1.7;background:#FFFDFC;border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:0 0 14px}
.nlpp-chips{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:16px}
.nlpp-chip{font-size:12.5px;border:1px solid var(--line);background:#FFFDFC;border-radius:999px;padding:5px 12px}
.nlpp-sec{border:1px solid var(--line);border-radius:12px;background:#FFFDFC;padding:16px 18px;margin-bottom:14px}
.nlpp-sec h3{font-family:var(--font-serif,serif);font-size:1.1rem;margin:0 0 10px}
.nlpp-list{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px}
.nlpp-list a{color:var(--ink);text-decoration:none;font-size:14px}
.nlpp-list a:hover{color:var(--gold)}
@media(max-width:560px){.nlpp-hero{padding:16px}.nlpp-name{font-size:1.4rem}.nlpp-ctas{width:100%}.nlpp-btn{flex:1;justify-content:center}}
' );
		wp_register_script( 'nadlan-nlpp-js', false, array(), '1.69.83', true );
		wp_enqueue_script( 'nadlan-nlpp-js' );
		wp_add_inline_script( 'nadlan-nlpp-js', '
(function(){document.addEventListener("DOMContentLoaded",function(){
	var mb=document.querySelector("[data-nlpp-meet]"),mf=document.getElementById("nlpp-meet");
	if(mb&&mf){mb.addEventListener("click",function(){mf.hidden=!mf.hidden;if(!mf.hidden){mf.querySelector("input").focus()}});
		mf.addEventListener("submit",function(e){e.preventDefault();
			var msg=mf.querySelector(".nlpp-meet-msg"),fd=new FormData(mf);
			if(fd.get("company")){return}
			fetch(mf.dataset.rest,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({
				name:fd.get("name"),phone:fd.get("phone"),topic:"video-meeting",source:"professional-profile",
				message:"בקשת שיחת וידאו עם "+mf.dataset.prof+(fd.get("slot")?" | מועד: "+fd.get("slot"):"")
			})}).then(function(r){msg.textContent=r.ok?"✓ הבקשה נשלחה - נחזור אליכם לתיאום":"שגיאה, נסו שוב";})
			.catch(function(){msg.textContent="שגיאה, נסו שוב"});
		});}
	var m=document.getElementById("nlpp-map");
	if(m&&window.L){var la=parseFloat(m.dataset.lat),ln=parseFloat(m.dataset.lng);
		var map=L.map(m,{scrollWheelZoom:false,zoomControl:false}).setView([la,ln],13);
		L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png",{attribution:"&copy; OSM"}).addTo(map);
		L.circle([la,ln],{radius:2200,color:"#9C7A3C",weight:1.5,fillColor:"#E6D4AE",fillOpacity:.25}).addTo(map);
		L.marker([la,ln]).addTo(map).bindPopup(m.dataset.title||"");}
	var ai=document.querySelector(".nlpp-ai");
	if(ai){var send=document.getElementById("nlpp-ai-send"),q=document.getElementById("nlpp-ai-q"),a=document.getElementById("nlpp-ai-a");
		function ask(){var t=q.value.trim();if(t.length<4){return}
			send.disabled=true;send.textContent="חושב...";a.hidden=false;a.textContent="";
			fetch(ai.dataset.rest,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({
				messages:[{role:"user",content:"בהקשר של "+ai.dataset.prof+" בנדל\"ן בישראל: "+t}]
			})}).then(function(r){return r.json()}).then(function(j){
				a.textContent=(j.answer||j.reply||j.message||"לא הצלחתי לענות כרגע, נסו לנסח אחרת.");
			}).catch(function(){a.textContent="השירות לא זמין כרגע."})
			.finally(function(){send.disabled=false;send.textContent="שאלו"});}
		send.addEventListener("click",ask);q.addEventListener("keydown",function(e){if(e.key==="Enter"){ask()}});}
});})();
' );
	}
}
add_action( 'wp_enqueue_scripts', 'nadlan_prof_assets' );
