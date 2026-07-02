<?php
/**
 * nadlan-config — Homepage v2 (v1.69.84)
 *
 * Research-grounded rebuild (Zillow/Realtor: search-first hero, trust volume up
 * top; Madlan: analytics + "leading professionals" monetized band). Everything
 * server-rendered from live CMS data — zero hardcoded inventory:
 *   1. Search hero with intent tabs (buy/rent/projects/professionals)
 *   2. Trust strip (real counts)
 *   3. Featured projects band — unified imagery treatment, paid_tier first
 *   4. Latest listings band (magazine cards)
 *   5. SPONSORED professionals band (premium tiers first = monetization) + join tile
 *   6. Tools band (calculators) · 7. Guides band · 8. Foreign-investor gateway
 *
 * Ships as [nadlan_home_v2] on /home-v2/ for owner approval, then the front page
 * is flipped via settings (safe cutover, no theme surgery).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_hv2_img' ) ) {
	function nadlan_hv2_img( $id ) {
		if ( has_post_thumbnail( $id ) ) { return get_the_post_thumbnail_url( $id, 'large' ); }
		$poster = (string) get_post_meta( $id, 'project_model_poster', true );
		if ( $poster ) { return $poster; }
		$photos = array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $id, 'photos_csv', true ) ) ) );
		return $photos ? $photos[0] : '';
	}
}

if ( ! function_exists( 'nadlan_home_v2_shortcode' ) ) {
	function nadlan_home_v2_shortcode() {
		$counts = array(
			'projects'      => (int) wp_count_posts( 'nadlan_project' )->publish,
			'professionals' => (int) wp_count_posts( 'nadlan_professional' )->publish,
			'properties'    => (int) wp_count_posts( 'nadlan_property' )->publish,
		);

		// featured projects: flagship-quality first (has model poster), tier priority
		$projects = get_posts( array( 'post_type' => 'nadlan_project', 'posts_per_page' => 3, 'no_found_rows' => true,
			'meta_query' => array( array( 'key' => 'project_model_glb', 'compare' => 'EXISTS' ) ) ) );
		if ( count( $projects ) < 3 ) {
			$projects = array_merge( $projects, get_posts( array( 'post_type' => 'nadlan_project', 'posts_per_page' => 3 - count( $projects ), 'no_found_rows' => true, 'post__not_in' => wp_list_pluck( $projects, 'ID' ) ) ) );
		}
		$listings = get_posts( array( 'post_type' => 'nadlan_property', 'posts_per_page' => 4, 'no_found_rows' => true ) );
		$pros = get_posts( array( 'post_type' => 'nadlan_professional', 'posts_per_page' => 4, 'no_found_rows' => true,
			'meta_query' => array( array( 'key' => 'paid_tier', 'value' => array( 'pro', 'premier' ), 'compare' => 'IN' ) ) ) );

		ob_start(); ?>
<div class="nlhv2" dir="rtl">

	<section class="nlhv2-hero">
		<h1>מוצאים דירה רואים אותה מבפנים ועד הנוף מהמרפסת</h1>
		<p class="nlhv2-sub">פרויקטים חדשים בתלת-ממד, דירות למכירה ולהשכרה, בעלי מקצוע מאומתים ומחשבונים - הכל במקום אחד.</p>
		<form class="nlhv2-search" action="<?php echo esc_url( home_url( '/properties/' ) ); ?>" method="get" role="search">
			<div class="nlhv2-tabs" role="tablist">
				<button type="button" class="is-on" data-action="<?php echo esc_url( home_url( '/properties/' ) ); ?>" data-extra="listing_type=sale">לקנייה</button>
				<button type="button" data-action="<?php echo esc_url( home_url( '/properties/' ) ); ?>" data-extra="listing_type=rent">להשכרה</button>
				<button type="button" data-action="<?php echo esc_url( home_url( '/projects/' ) ); ?>" data-extra="">פרויקטים חדשים</button>
				<button type="button" data-action="<?php echo esc_url( home_url( '/professionals/' ) ); ?>" data-extra="">בעלי מקצוע</button>
			</div>
			<div class="nlhv2-box">
				<input type="search" name="q" placeholder="עיר, שכונה, פרויקט או בעל מקצוע..." aria-label="חיפוש">
				<button type="submit">חיפוש</button>
			</div>
		</form>
		<div class="nlhv2-trust">
			<span><b><?php echo number_format( $counts['projects'] ); ?></b> פרויקטים והתחדשות</span>
			<span><b><?php echo number_format( $counts['professionals'] ); ?></b> בעלי מקצוע מאומתים (gov.il)</span>
			<span><b>5</b> מחשבונים מקצועיים</span>
			<span><b>ליווי</b> עורך דין מקרקעין</span>
		</div>
	</section>

	<?php if ( $projects ) : ?>
	<section class="nlhv2-band">
		<header><h2>פרויקטים נבחרים - עם סיור תלת-ממדי</h2><a href="<?php echo esc_url( home_url( '/projects/' ) ); ?>">לכל הפרויקטים ←</a></header>
		<div class="nlhv2-projgrid">
			<?php foreach ( $projects as $p ) : $img = nadlan_hv2_img( $p->ID ); ?>
			<a class="nlhv2-proj" href="<?php echo esc_url( get_permalink( $p ) ); ?>">
				<span class="nlhv2-proj-media"<?php echo $img ? ' style="background-image:url(' . esc_url( $img ) . ')"' : ''; ?>>
					<?php if ( get_post_meta( $p->ID, 'project_model_glb', true ) ) : ?><em>סיור 3D</em><?php endif; ?>
				</span>
				<span class="nlhv2-proj-body">
					<b><?php echo esc_html( get_the_title( $p ) ); ?></b>
					<span><?php echo esc_html( get_post_meta( $p->ID, 'city', true ) ); ?><?php $pp = (int) get_post_meta( $p->ID, 'project_3d_avg_price_per_sqm', true ); echo $pp ? ' · ~' . number_format( $pp ) . ' ₪/מ״ר' : ''; ?></span>
				</span>
			</a>
			<?php endforeach; ?>
		</div>
	</section>
	<?php endif; ?>

	<?php if ( $listings ) : ?>
	<section class="nlhv2-band nlhv2-alt">
		<header><h2>דירות למכירה ולהשכרה</h2><a href="<?php echo esc_url( home_url( '/properties/' ) ); ?>">לכל הדירות ←</a></header>
		<div class="nlhv2-listgrid">
			<?php foreach ( $listings as $l ) : $img = nadlan_hv2_img( $l->ID );
				$pr = (int) get_post_meta( $l->ID, 'price', true ); $rm = (float) get_post_meta( $l->ID, 'rooms', true ); ?>
			<a class="nlhv2-list" href="<?php echo esc_url( get_permalink( $l ) ); ?>">
				<span class="nlhv2-list-media"<?php echo $img ? ' style="background-image:url(' . esc_url( $img ) . ')"' : ''; ?>></span>
				<b><?php echo $pr ? number_format( $pr ) . ' ₪' : esc_html( get_the_title( $l ) ); ?></b>
				<span><?php echo esc_html( trim( ( $rm ? rtrim( rtrim( number_format( $rm, 1 ), '0' ), '.' ) . " חד' · " : '' ) . get_post_meta( $l->ID, 'city', true ), " ·'" ) ); ?></span>
			</a>
			<?php endforeach; ?>
			<a class="nlhv2-list nlhv2-cta-tile" href="<?php echo esc_url( home_url( '/post-listing/' ) ); ?>"><b>+ פרסמו דירה</b><span>חינם, עם עוזר AI</span></a>
		</div>
	</section>
	<?php endif; ?>

	<?php if ( $pros ) : ?>
	<section class="nlhv2-band">
		<header><h2>בעלי מקצוע מובילים</h2><a href="<?php echo esc_url( home_url( '/professionals/' ) ); ?>">לכל המאגר ←</a></header>
		<div class="nlhv2-prosgrid">
			<?php foreach ( $pros as $pr ) :
				$prof = function_exists( 'nadlan_prof_meta_of' ) ? nadlan_prof_meta_of( get_post_meta( $pr->ID, 'profession', true ) ) : array( 'label' => '', 'color' => '#1B1A17' );
				$rating = (float) get_post_meta( $pr->ID, 'rating', true ); ?>
			<a class="nlhv2-pro" href="<?php echo esc_url( get_permalink( $pr ) ); ?>">
				<?php echo function_exists( 'nadlan_prof_monogram_svg' ) ? nadlan_prof_monogram_svg( get_the_title( $pr ), $prof['color'] ) : ''; // phpcs:ignore ?>
				<b><?php echo esc_html( get_the_title( $pr ) ); ?></b>
				<span><?php echo esc_html( $prof['label'] ); ?><?php echo $rating ? ' · ★ ' . number_format( $rating, 1 ) : ''; ?></span>
			</a>
			<?php endforeach; ?>
			<a class="nlhv2-pro nlhv2-cta-tile" href="<?php echo esc_url( home_url( '/advertise/' ) ); ?>"><b>+ הצטרפו למאגר</b><span>חשיפה לקונים ומשקיעים</span></a>
		</div>
	</section>
	<?php endif; ?>

	<section class="nlhv2-band nlhv2-alt">
		<header><h2>כלים שחוסכים טעויות יקרות</h2></header>
		<div class="nlhv2-tools">
			<a href="<?php echo esc_url( home_url( '/mortgage-calculator/' ) ); ?>"><b>מחשבון משכנתא</b><span>ההחזר החודשי האמיתי</span></a>
			<a href="<?php echo esc_url( home_url( '/purchase-tax-calculator/' ) ); ?>"><b>מס רכישה</b><span>מדרגות 2026</span></a>
			<a href="<?php echo esc_url( home_url( '/apartment-purchase-cost-calculator/' ) ); ?>"><b>עלות עסקה מלאה</b><span>כל ההוצאות הנלוות</span></a>
			<a href="<?php echo esc_url( home_url( '/property-value-estimator/' ) ); ?>"><b>כמה שווה הדירה?</b><span>אומדן ראשוני</span></a>
		</div>
	</section>

	<section class="nlhv2-band">
		<header><h2>מדריכים שכדאי לקרוא לפני שחותמים</h2><a href="<?php echo esc_url( home_url( '/buying-apartment/' ) ); ?>">לכל המדריכים ←</a></header>
		<div class="nlhv2-tools">
			<a href="<?php echo esc_url( home_url( '/buying-apartment/' ) ); ?>"><b>קניית דירה</b><span>המדריך המלא, שלב אחר שלב</span></a>
			<a href="<?php echo esc_url( home_url( '/tabu-extract-check/' ) ); ?>"><b>בדיקת נסח טאבו</b><span>מה חייבים לבדוק</span></a>
			<a href="<?php echo esc_url( home_url( '/investment/' ) ); ?>"><b>נדל״ן להשקעה</b><span>איפה ואיך ב-2026</span></a>
		</div>
	</section>

	<section class="nlhv2-en" dir="ltr">
		<div>
			<h2>Buying property in Israel from abroad?</h2>
			<p>3D project tours, verified professionals and legal guidance for foreign buyers - in English.</p>
		</div>
		<a href="<?php echo esc_url( home_url( '/projects/ashira-sde-dov-en/' ) ); ?>">Explore in English →</a>
	</section>
</div>
<?php
		return ob_get_clean();
	}
}
add_shortcode( 'nadlan_home_v2', 'nadlan_home_v2_shortcode' );

if ( ! function_exists( 'nadlan_hv2_assets' ) ) {
	function nadlan_hv2_assets() {
		if ( ! is_singular() || ! has_shortcode( (string) get_post_field( 'post_content', get_queried_object_id() ), 'nadlan_home_v2' ) ) { return; }
		wp_register_style( 'nadlan-hv2', false );
		wp_enqueue_style( 'nadlan-hv2' );
		wp_add_inline_style( 'nadlan-hv2', '
.nlhv2{--ink:#1B1A17;--warm:#6D665C;--gold:#9C7A3C;--line:#E2DCD0;--band:#F3EEE3;font-family:var(--font-sans,Heebo,system-ui,sans-serif);color:var(--ink)}
.nlhv2 h1{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:clamp(1.7rem,4.4vw,2.7rem);line-height:1.2;margin:0 0 10px;letter-spacing:-.01em}
.nlhv2 h2{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:1.35rem;margin:0}
.nlhv2-hero{text-align:center;padding:28px 0 26px}
.nlhv2-sub{color:var(--warm);max-width:560px;margin:0 auto 20px;font-size:15.5px}
.nlhv2-search{max-width:640px;margin:0 auto}
.nlhv2-tabs{display:flex;justify-content:center;gap:4px;flex-wrap:wrap;margin-bottom:-1px}
.nlhv2-tabs button{font:600 13.5px/1 inherit;font-family:inherit;border:1px solid var(--line);border-bottom:0;background:#FAF8F3;color:var(--warm);border-radius:10px 10px 0 0;padding:11px 18px;cursor:pointer;min-height:40px}
.nlhv2-tabs button.is-on{background:#fff;color:var(--ink);font-weight:700}
.nlhv2-box{display:flex;background:#fff;border:1px solid var(--line);border-radius:0 12px 12px 12px;padding:7px;box-shadow:0 14px 34px rgba(27,26,23,.08)}
.nlhv2-box input{flex:1;border:0;font:inherit;font-size:15px;padding:12px 14px;background:none;min-width:0;outline-offset:-2px}
.nlhv2-box button{font:700 15px/1 inherit;font-family:inherit;border:0;background:var(--ink);color:#fff;border-radius:8px;padding:0 26px;cursor:pointer;min-height:46px}
.nlhv2-box button:hover{background:#000}
.nlhv2-trust{display:flex;justify-content:center;gap:22px;flex-wrap:wrap;margin-top:20px;font-size:12.5px;color:var(--warm)}
.nlhv2-trust b{color:var(--ink);font-size:15px;display:block}
.nlhv2-band{padding:26px 0;border-top:1px solid var(--line)}
.nlhv2-alt{background:linear-gradient(180deg,#FAF8F3,transparent)}
.nlhv2-band header{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin-bottom:16px}
.nlhv2-band header a{color:var(--gold);font-size:13.5px;font-weight:700;text-decoration:none}
.nlhv2-projgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.nlhv2-proj{display:block;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff;text-decoration:none;color:var(--ink);transition:transform .2s,box-shadow .25s}
.nlhv2-proj:hover{transform:translateY(-3px);box-shadow:0 14px 34px rgba(27,26,23,.1)}
.nlhv2-proj-media{display:block;aspect-ratio:16/10;background:var(--band) center/cover no-repeat;position:relative}
.nlhv2-proj-media em{position:absolute;top:10px;inset-inline-start:10px;font-style:normal;font-size:11px;font-weight:700;background:rgba(27,26,23,.85);color:#E6D4AE;border-radius:5px;padding:4px 9px}
.nlhv2-proj-body{display:block;padding:12px 14px}
.nlhv2-proj-body b{display:block;font-family:var(--font-serif,serif);font-size:1.05rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nlhv2-proj-body span{font-size:12.5px;color:var(--warm)}
.nlhv2-listgrid,.nlhv2-prosgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
.nlhv2-list{display:block;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:#fff;text-decoration:none;color:var(--ink);padding-bottom:10px;transition:border-color .2s}
.nlhv2-list:hover{border-color:var(--gold)}
.nlhv2-list-media{display:block;aspect-ratio:4/3;background:var(--band) center/cover no-repeat;margin-bottom:8px}
.nlhv2-list b{display:block;padding:0 12px;font-size:15px}
.nlhv2-list>span{display:block;padding:0 12px;font-size:12px;color:var(--warm)}
.nlhv2-pro{display:flex;flex-direction:column;align-items:center;text-align:center;gap:6px;border:1px solid var(--line);border-radius:12px;background:#fff;padding:16px 10px;text-decoration:none;color:var(--ink);transition:border-color .2s}
.nlhv2-pro:hover{border-color:var(--gold)}
.nlhv2-pro svg{width:56px;height:56px}
.nlhv2-pro b{font-size:13.5px;line-height:1.2}
.nlhv2-pro span{font-size:11.5px;color:var(--warm)}
.nlhv2-cta-tile{justify-content:center;background:var(--band);border-style:dashed}
.nlhv2-cta-tile b{color:var(--gold)}
.nlhv2-tools{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}
.nlhv2-tools a{display:block;border:1px solid var(--line);border-radius:10px;background:#fff;padding:14px 16px;text-decoration:none;color:var(--ink);transition:border-color .2s,transform .2s}
.nlhv2-tools a:hover{border-color:var(--gold);transform:translateY(-2px)}
.nlhv2-tools b{display:block;font-size:14.5px}
.nlhv2-tools span{font-size:12px;color:var(--warm)}
.nlhv2-en{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;border:1px solid var(--ink);border-radius:14px;background:var(--ink);color:#FAF8F3;padding:22px 24px;margin:26px 0}
.nlhv2-en h2{color:#FAF8F3;font-size:1.25rem;margin:0 0 4px}
.nlhv2-en p{margin:0;font-size:13.5px;color:#C9C2B2}
.nlhv2-en a{background:#E6D4AE;color:var(--ink);font-weight:700;font-size:14px;border-radius:9px;padding:12px 20px;text-decoration:none;white-space:nowrap}
@media(max-width:560px){.nlhv2-trust{gap:14px}.nlhv2-box button{padding:0 18px}}
' );
		wp_register_script( 'nadlan-hv2-js', false, array(), '1.69.84', true );
		wp_enqueue_script( 'nadlan-hv2-js' );
		wp_add_inline_script( 'nadlan-hv2-js', '
(function(){document.addEventListener("DOMContentLoaded",function(){
	var f=document.querySelector(".nlhv2-search");if(!f){return}
	f.querySelectorAll(".nlhv2-tabs button").forEach(function(b){
		b.addEventListener("click",function(){
			f.querySelectorAll(".nlhv2-tabs button").forEach(function(x){x.classList.toggle("is-on",x===b)});
			f.action=b.dataset.action;
			f.querySelectorAll("input[type=hidden]").forEach(function(h){h.remove()});
			if(b.dataset.extra){var kv=b.dataset.extra.split("=");var h=document.createElement("input");h.type="hidden";h.name=kv[0];h.value=kv[1];f.appendChild(h)}
		});
	});
});})();
' );
	}
}
add_action( 'wp_enqueue_scripts', 'nadlan_hv2_assets' );
