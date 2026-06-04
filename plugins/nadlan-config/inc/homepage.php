<?php
/**
 * nadlan-config — Homepage below-the-fold sections (v1.27.0)
 *
 * Owner direction + Lovable blueprint §5 agree: the HERO stays for real-estate-user
 * intent (search / decisions), and the discovery / directory / authority content
 * goes BELOW THE FOLD, designed clean (quiet gradient, serif headings, gold accents,
 * no heavy images — LCP target ≤2s).
 *
 * Appended (priority 50, AFTER the page's own content) on the front page only:
 *   1. השוק לפי עיר   — 12 city cards (real professional counts) → city hubs
 *   2. בעלי מקצוע      — verified directory teaser (gov.il רשם הקבלנים)
 *   3. מדריכי החלטה   — 4 decision-guide pillar cards
 *
 * Everything is real-estate-buyer/seller facing. No internal "stats with arrows" in
 * the hero. Each card is a destination a real estate user actually wants.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_home_sections_render' ) ) {
	function nadlan_home_sections_render() {
		$out  = '<div class="nlhome" dir="rtl">';
		$out .= nadlan_home_cities_block();
		$out .= nadlan_home_pros_block();
		$out .= nadlan_home_guides_block();
		$out .= '</div>' . nadlan_home_css();
		return $out;
	}
}

/* ---- 1. Cities grid (real-estate-user intent: "השוק לפי עיר") ---- */
if ( ! function_exists( 'nadlan_home_cities_block' ) ) {
	function nadlan_home_cities_block() {
		$idx = function_exists( 'nadlan_cities_index' ) ? nadlan_cities_index() : array();
		// Keep cities that have a meaningful number of records (hubs need ≥5).
		$idx = array_values( array_filter( $idx, function ( $r ) { return ( $r['count'] ?? 0 ) >= 5 && mb_strlen( $r['name'] ) > 1; } ) );
		$idx = array_slice( $idx, 0, 12 );
		if ( ! $idx ) { return ''; }
		$h  = '<section class="nlhome-sec"><div class="nlhome-head"><p class="nlhome-eyebrow">השוק לפי עיר</p><h2>בעלי מקצוע ופרויקטים, לפי עיר</h2><p class="nlhome-sub">בחרו עיר כדי לראות קבלנים רשומים, פרויקטים והתחדשות עירונית באזור.</p></div>';
		$h .= '<div class="nlhome-cities">';
		foreach ( $idx as $row ) {
			$name = (string) $row['name'];
			$url  = home_url( '/city/' . rawurlencode( $name ) . '/contractors/' );
			$h   .= '<a class="nlhome-city" href="' . esc_url( $url ) . '"><span class="nlhome-city-n">' . esc_html( $name ) . '</span><span class="nlhome-city-c">' . number_format( (int) $row['count'] ) . ' רשומות</span></a>';
		}
		$h .= '</div></section>';
		return $h;
	}
}

/* ---- 2. Professional directory teaser ---- */
if ( ! function_exists( 'nadlan_home_pros_block' ) ) {
	function nadlan_home_pros_block() {
		$total = (int) wp_count_posts( 'nadlan_professional' )->publish;
		if ( $total < 1 ) { return ''; }
		$pros = get_posts( array(
			'post_type' => 'nadlan_professional', 'post_status' => 'publish',
			'posts_per_page' => 6, 'orderby' => 'rand',
			'meta_query' => array(
				array( 'key' => 'classification', 'value' => '', 'compare' => '!=' ),
				array( 'key' => 'city', 'value' => '', 'compare' => '!=' ),
			),
		) );
		if ( ! $pros ) { return ''; }
		$h  = '<section class="nlhome-sec"><div class="nlhome-head"><p class="nlhome-eyebrow">מאגר מאומת</p><h2>בעלי מקצוע שאפשר לסמוך עליהם</h2><p class="nlhome-sub">' . number_format( $total ) . ' קבלנים רשומים, ממקור רשמי — פנקס הקבלנים הרשומים (gov.il).</p></div>';
		$h .= '<div class="nlhome-pros">';
		foreach ( $pros as $p ) {
			$city = trim( (string) get_post_meta( $p->ID, 'city', true ) );
			$cls  = trim( (string) get_post_meta( $p->ID, 'classification', true ) );
			$cls  = mb_strlen( $cls ) > 42 ? mb_substr( $cls, 0, 42 ) . '…' : $cls;
			$h   .= '<a class="nlhome-pro" href="' . esc_url( get_permalink( $p ) ) . '"><span class="nlhome-pro-badge">קבלן רשום</span><span class="nlhome-pro-n">' . esc_html( get_the_title( $p ) ) . '</span>'
				 . ( $city ? '<span class="nlhome-pro-city">' . esc_html( $city ) . '</span>' : '' )
				 . ( $cls ? '<span class="nlhome-pro-c">' . esc_html( $cls ) . '</span>' : '' ) . '</a>';
		}
		$h .= '</div><div class="nlhome-cta"><a class="nlhome-btn" href="' . esc_url( home_url( '/professionals/' ) ) . '">לכל בעלי המקצוע ←</a></div></section>';
		return $h;
	}
}

/* ---- 3. Decision guides (links to existing money-pillar guide pages) ---- */
if ( ! function_exists( 'nadlan_home_guides_block' ) ) {
	function nadlan_home_guides_block() {
		// Curated, high-intent guides that already exist on the site.
		$guides = array(
			array( 'slug' => 'buying-apartment-step-by-step', 'title' => 'קונים דירה', 'desc' => 'מדריך מלא לרוכש — שלב אחר שלב, מהחיפוש ועד המסירה.' ),
			array( 'slug' => 'selling-without-broker',         'title' => 'מוכרים דירה', 'desc' => 'תמחור, פרסום, משא ומתן וחוזה. בלי מתווך.' ),
			array( 'slug' => 'real-estate-leverage',           'title' => 'משקיעים', 'desc' => 'מינוף, יחס מימון ותשואה על ההון. בלי טעויות יקרות.' ),
			array( 'slug' => 'when-real-estate-lawyer-required','title' => 'ליווי משפטי', 'desc' => 'מתי חייבים עורך דין מקרקעין, ומה הוא בודק בשבילכם.' ),
		);
		$cards = '';
		foreach ( $guides as $g ) {
			$page = get_page_by_path( $g['slug'] );
			$url  = $page ? get_permalink( $page ) : home_url( '/' . $g['slug'] . '/' );
			$cards .= '<a class="nlhome-guide" href="' . esc_url( $url ) . '"><h3>' . esc_html( $g['title'] ) . '</h3><p>' . esc_html( $g['desc'] ) . '</p><span class="nlhome-go">התחל ←</span></a>';
		}
		return '<section class="nlhome-sec"><div class="nlhome-head"><p class="nlhome-eyebrow">ידע שמגן על העסקה</p><h2>מדריכי החלטה</h2></div><div class="nlhome-guides">' . $cards . '</div></section>';
	}
}

/* ---- scoped CSS (quiet, Lovable-clean, gold/ink/serif) ---- */
if ( ! function_exists( 'nadlan_home_css' ) ) {
	function nadlan_home_css() {
		return '<style>
.nlhome{font-family:var(--font-sans,Heebo,sans-serif);max-width:1240px;margin:8px auto 0;padding:0 24px;direction:rtl}
.nlhome-sec{margin:44px 0}
.nlhome-head{text-align:center;margin-bottom:26px}
.nlhome-eyebrow{font-size:11px;letter-spacing:.18em;color:#9C7A3C;font-weight:600;margin:0 0 6px;text-transform:uppercase}
.nlhome-head h2{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-weight:500;font-size:32px;color:#1B1A17;margin:0 0 8px;letter-spacing:-.015em}
.nlhome-sub{font-size:14.5px;color:#6b6b6b;margin:0;max-width:640px;margin-inline:auto;line-height:1.6}
/* cities */
.nlhome-cities{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}
.nlhome-city{display:flex;flex-direction:column;gap:4px;background:#fff;border:1px solid rgba(27,26,23,.1);border-radius:12px;padding:16px 18px;text-decoration:none;color:inherit;transition:transform .2s,box-shadow .2s,border-color .2s}
.nlhome-city:hover{transform:translateY(-3px);box-shadow:0 10px 24px rgba(27,26,23,.08);border-color:rgba(156,122,60,.4)}
.nlhome-city-n{font-family:var(--font-serif,serif);font-size:18px;color:#1B1A17;font-weight:500}
.nlhome-city-c{font-size:12px;color:#9C7A3C;font-weight:600}
/* pros */
.nlhome-pros{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px}
.nlhome-pro{position:relative;display:flex;flex-direction:column;gap:6px;background:linear-gradient(135deg,#fff,#FBF9F5);border:1px solid rgba(27,26,23,.1);border-radius:14px;padding:20px;text-decoration:none;color:inherit;transition:transform .22s,box-shadow .22s,border-color .22s;min-height:150px}
.nlhome-pro:hover{transform:translateY(-4px);box-shadow:0 14px 30px rgba(27,26,23,.1);border-color:rgba(156,122,60,.45)}
.nlhome-pro-badge{align-self:flex-start;background:linear-gradient(135deg,#9C7A3C,#B89254);color:#fff;font-size:10px;letter-spacing:.1em;font-weight:600;padding:4px 10px;border-radius:20px}
.nlhome-pro-n{font-family:var(--font-serif,serif);font-size:17px;color:#1B1A17;font-weight:500;margin-top:4px}
.nlhome-pro-city{font-size:12px;letter-spacing:.08em;color:#9C7A3C;font-weight:600}
.nlhome-pro-c{font-size:12.5px;color:#5a5a5a;line-height:1.5;margin-top:auto}
/* guides */
.nlhome-guides{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px}
.nlhome-guide{background:linear-gradient(135deg,#fff,#FBF9F5);border:1px solid rgba(27,26,23,.1);border-radius:16px;padding:26px 24px;text-decoration:none;color:inherit;transition:transform .25s,box-shadow .25s,border-color .25s;display:flex;flex-direction:column;min-height:170px}
.nlhome-guide:hover{transform:translateY(-5px);box-shadow:0 16px 34px rgba(27,26,23,.1);border-color:rgba(156,122,60,.5)}
.nlhome-guide h3{font-family:var(--font-serif,serif);font-weight:500;font-size:21px;color:#1B1A17;margin:0 0 10px}
.nlhome-guide p{font-size:13.5px;color:#5a5a5a;margin:0 0 16px;line-height:1.6}
.nlhome-go,.nlhome-btn{color:#9C7A3C;font-weight:600;font-size:13.5px}
.nlhome-go{margin-top:auto;transition:transform .2s}
.nlhome-guide:hover .nlhome-go{transform:translateX(-4px)}
.nlhome-cta{text-align:center;margin-top:24px}
.nlhome-btn{display:inline-block;background:#1B1A17;color:#FAF7F1;padding:13px 30px;border-radius:8px;text-decoration:none;transition:background .2s,color .2s,transform .2s}
.nlhome-btn:hover{background:#9C7A3C;color:#fff;transform:translateY(-2px)}
@media(max-width:600px){.nlhome-head h2{font-size:25px}.nlhome-cities{grid-template-columns:repeat(2,1fr)}}
</style>';
	}
}

/* Append BELOW the page content on the front page only (priority 50 = under the fold).
 * DISABLED per owner request (2026-06-01): "don't touch the homepage and the menus".
 * The shortcodes below still work, so the owner can place these blocks anywhere later.
 */
// add_filter( 'the_content', function ( $content ) {
//	if ( ! is_front_page() || ! in_the_loop() || ! is_main_query() ) { return $content; }
//	return $content . nadlan_home_sections_render();
// }, 50 );

/* Also expose as a shortcode so the owner can place it anywhere in the page builder. */
add_shortcode( 'nadlan_home_sections', 'nadlan_home_sections_render' );

/* ---- v1.28.0: Lovable-style HERO SEARCH (drop-in shortcode) ----
 * [nadlan_hero_search] — the real-estate-user-intent search module for the hero,
 * per Lovable §5. Three tabs (למכירה / להשכרה / פרויקטים), city field (gets the
 * sitewide autocomplete free via name="city"), rooms + max price, search button.
 * Submits GET to the matching archive so the existing facets engine handles it.
 * The owner can place this in their hero block without us overwriting the hero. */
if ( ! function_exists( 'nadlan_hero_search_render' ) ) {
	function nadlan_hero_search_render() {
		$prop_url = get_post_type_archive_link( 'nadlan_property' ) ?: home_url( '/properties/' );
		$proj_url = get_post_type_archive_link( 'nadlan_project' ) ?: home_url( '/urban-renewal/' );
		ob_start(); ?>
<div class="nlhs" dir="rtl">
	<div class="nlhs-tabs" role="tablist">
		<button type="button" class="nlhs-tab is-on" data-mode="sale">למכירה</button>
		<button type="button" class="nlhs-tab" data-mode="rent">להשכרה</button>
		<button type="button" class="nlhs-tab" data-mode="project">פרויקטים</button>
	</div>
	<form class="nlhs-form" method="get" action="<?php echo esc_url( $prop_url ); ?>"
		  data-prop="<?php echo esc_url( $prop_url ); ?>" data-proj="<?php echo esc_url( $proj_url ); ?>">
		<input type="hidden" name="listing_type" value="sale" class="nlhs-lt">
		<div class="nlhs-field nlhs-city">
			<label>עיר או שכונה</label>
			<input type="text" name="city" autocomplete="off" placeholder="לדוגמה: ירושלים, רמת גן">
		</div>
		<div class="nlhs-field nlhs-rooms">
			<label>חדרים (מינ׳)</label>
			<select name="rooms_min">
				<option value="">הכל</option>
				<option value="2">2+</option><option value="3">3+</option>
				<option value="4">4+</option><option value="5">5+</option>
			</select>
		</div>
		<div class="nlhs-field nlhs-price">
			<label>מחיר עד</label>
			<select name="price_max">
				<option value="">ללא הגבלה</option>
				<option value="1500000">1.5M ₪</option><option value="2500000">2.5M ₪</option>
				<option value="3500000">3.5M ₪</option><option value="5000000">5M ₪</option>
			</select>
		</div>
		<button type="submit" class="nlhs-go">חיפוש</button>
	</form>
	<?php $val = get_page_by_path( 'pricing-apartment-for-sale' ); $val_url = $val ? get_permalink( $val ) : home_url( '/pricing-apartment-for-sale/' ); ?>
	<a class="nlhs-micro" href="<?php echo esc_url( $val_url ); ?>">או בדקו שווי דירה ←</a>
</div>
<style>
.nlhs{font-family:var(--font-sans,Heebo,sans-serif);max-width:880px;margin:0 auto;direction:rtl}
.nlhs-tabs{display:flex;gap:4px;margin-bottom:-1px}
.nlhs-tab{background:rgba(255,255,255,.6);border:1px solid rgba(27,26,23,.12);border-bottom:0;border-radius:12px 12px 0 0;padding:11px 22px;font:inherit;font-weight:600;color:#5a5a5a;cursor:pointer}
.nlhs-tab.is-on{background:#fff;color:#1B1A17}
.nlhs-form{display:flex;gap:10px;align-items:flex-end;background:#fff;border:1px solid rgba(27,26,23,.12);border-radius:0 14px 14px 14px;padding:16px;box-shadow:0 10px 30px rgba(27,26,23,.08)}
.nlhs-field{display:flex;flex-direction:column;gap:5px;flex:1}
.nlhs-field label{font-size:11px;letter-spacing:.06em;color:#9C7A3C;font-weight:600}
.nlhs-field input,.nlhs-field select{padding:12px;border:1px solid rgba(27,26,23,.16);border-radius:9px;font:inherit;background:#fff}
.nlhs-city{flex:2}
.nlhs-go{background:#1B1A17;color:#FAF7F1;border:0;border-radius:9px;padding:13px 30px;font:inherit;font-weight:600;cursor:pointer;transition:background .2s,color .2s;height:46px}
.nlhs-go:hover{background:#9C7A3C;color:#fff}
.nlhs-micro{display:inline-block;margin-top:12px;color:#9C7A3C;text-decoration:none;font-size:13.5px;font-weight:600}
@media(max-width:680px){.nlhs-form{flex-wrap:wrap}.nlhs-field{flex:1 1 100%}.nlhs-go{width:100%}}
</style>
<script>
(function(){
	var box=document.currentScript.closest('.nlhs')||document.querySelector('.nlhs');
	if(!box)return;
	var form=box.querySelector('.nlhs-form'),lt=box.querySelector('.nlhs-lt');
	box.querySelectorAll('.nlhs-tab').forEach(function(t){
		t.addEventListener('click',function(){
			box.querySelectorAll('.nlhs-tab').forEach(function(x){x.classList.remove('is-on');});
			t.classList.add('is-on');
			var m=t.dataset.mode;
			if(m==='project'){form.action=form.dataset.proj;lt.disabled=true;}
			else{form.action=form.dataset.prop;lt.disabled=false;lt.value=m;}
		});
	});
})();
</script>
		<?php
		return ob_get_clean();
	}
}
add_shortcode( 'nadlan_hero_search', 'nadlan_hero_search_render' );
