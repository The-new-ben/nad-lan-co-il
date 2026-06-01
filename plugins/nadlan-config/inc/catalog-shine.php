<?php
/**
 * nadlan-config — Catalog / WooCommerce premium skin (v1.22.0)
 *
 * The owner's catalog is a WooCommerce store (/catalog/, /shop, product archives).
 * Default Woo styling looks generic ("lame"). This module ships a SCOPED, brand-
 * matched skin (gold #9C7A3C, ink #1B1A17, cream #FAF7F1, Heebo) that only loads on
 * Woo surfaces — no global CSS bleed, no theme edit, no extra HTTP request (inline).
 *
 * What it restyles, modern-store grade:
 *   - product grid cards: white, rounded, soft shadow, hover lift + image zoom
 *   - price in brand gold, sale badge as a gold pill, rating stars
 *   - add-to-cart / buttons: ink → gold hover, full-width on cards
 *   - single product: cleaner gallery, sticky-feel summary, polished tabs
 *   - store notices / messages on-brand
 *   - RTL-correct throughout (Hebrew store)
 *
 * Guarded: does nothing if WooCommerce is not active.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* Only act when WooCommerce exists. */
if ( ! function_exists( 'nadlan_catalog_is_woo_active' ) ) {
	function nadlan_catalog_is_woo_active() {
		return class_exists( 'WooCommerce' );
	}
}

/* Should the skin load on the current view? */
if ( ! function_exists( 'nadlan_catalog_is_woo_view' ) ) {
	function nadlan_catalog_is_woo_view() {
		if ( ! nadlan_catalog_is_woo_active() ) { return false; }
		if ( function_exists( 'is_woocommerce' ) && is_woocommerce() ) { return true; }
		if ( function_exists( 'is_shop' ) && is_shop() ) { return true; }
		if ( function_exists( 'is_product_taxonomy' ) && is_product_taxonomy() ) { return true; }
		if ( function_exists( 'is_cart' ) && is_cart() ) { return true; }
		if ( function_exists( 'is_checkout' ) && is_checkout() ) { return true; }
		if ( function_exists( 'is_account_page' ) && is_account_page() ) { return true; }
		// The owner's catalog lives at /catalog/ — cover it even if it embeds Woo via shortcode.
		if ( is_page() ) {
			$slug = get_post_field( 'post_name', get_queried_object_id() );
			if ( in_array( $slug, array( 'catalog', 'store', 'shop' ), true ) ) { return true; }
		}
		return false;
	}
}

if ( ! function_exists( 'nadlan_catalog_skin' ) ) {
	function nadlan_catalog_skin() {
		if ( ! nadlan_catalog_is_woo_view() ) { return; }
		?>
<style id="nadlan-catalog-skin">
:root{--nl-ink:#1B1A17;--nl-gold:#9C7A3C;--nl-cream:#FAF7F1;--nl-line:rgba(27,26,23,.10)}
.woocommerce,.woocommerce-page{font-family:var(--font-sans,Heebo,sans-serif)}

/* ---- grid + cards ---- */
.woocommerce ul.products,.woocommerce-page ul.products{display:grid !important;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:22px;margin:0 0 30px;padding:0}
.woocommerce ul.products li.product,.woocommerce-page ul.products li.product{width:auto !important;margin:0 !important;float:none !important;background:#fff;border:1px solid var(--nl-line);border-radius:14px;padding:0 0 16px;overflow:hidden;transition:transform .22s ease,box-shadow .22s ease;display:flex;flex-direction:column;position:relative}
.woocommerce ul.products li.product:hover{transform:translateY(-6px);box-shadow:0 16px 34px rgba(27,26,23,.13)}
.woocommerce ul.products li.product a img{margin:0 0 12px;border-radius:0;aspect-ratio:4/3;object-fit:cover;width:100%;transition:transform .4s ease}
.woocommerce ul.products li.product:hover a img{transform:scale(1.06)}
.woocommerce ul.products li.product .woocommerce-loop-product__link{display:block;overflow:hidden}
.woocommerce ul.products li.product .woocommerce-loop-product__title,.woocommerce ul.products li.product h2{font-size:16px !important;font-weight:600;color:var(--nl-ink);padding:0 16px !important;margin:0 0 6px;line-height:1.4}
.woocommerce ul.products li.product .price{color:var(--nl-gold) !important;font-weight:700;font-size:18px;padding:0 16px;margin-bottom:10px}
.woocommerce ul.products li.product .price del{color:#b9b2a6 !important;font-weight:400;font-size:14px;margin-inline-end:6px}
.woocommerce ul.products li.product .price ins{text-decoration:none}
.woocommerce ul.products li.product .star-rating{margin:0 16px 8px;font-size:13px;color:var(--nl-gold)}

/* ---- sale badge as a gold pill ---- */
.woocommerce span.onsale,.woocommerce ul.products li.product .onsale{position:absolute;top:12px;inset-inline-start:12px;background:var(--nl-gold);color:#fff;min-height:0;min-width:0;line-height:1;padding:7px 13px;border-radius:20px;font-size:12px;font-weight:600;margin:0;box-shadow:0 4px 12px rgba(156,122,60,.35)}

/* ---- buttons ---- */
.woocommerce a.button,.woocommerce button.button,.woocommerce input.button,.woocommerce .button.alt,.woocommerce #respond input#submit{background:var(--nl-ink);color:var(--nl-cream);border-radius:8px;font-weight:600;padding:11px 20px;transition:background .2s ease,color .2s ease;border:0;text-shadow:none}
.woocommerce a.button:hover,.woocommerce button.button:hover,.woocommerce .button.alt:hover,.woocommerce #respond input#submit:hover{background:var(--nl-gold);color:#fff}
.woocommerce ul.products li.product .button{margin:auto 16px 0;display:block;text-align:center}
.woocommerce ul.products li.product .added_to_cart{display:block;text-align:center;margin:8px 16px 0;color:var(--nl-gold);font-weight:600}

/* ---- result count + ordering ---- */
.woocommerce .woocommerce-result-count{color:#6b6b6b}
.woocommerce .woocommerce-ordering select{padding:9px 12px;border:1px solid var(--nl-line);border-radius:8px;font:inherit;background:#fff}

/* ---- single product ---- */
.woocommerce div.product .product_title{font-size:30px;font-weight:700;color:var(--nl-ink)}
.woocommerce div.product p.price,.woocommerce div.product span.price{color:var(--nl-gold);font-weight:700;font-size:26px}
.woocommerce div.product .woocommerce-product-gallery{border-radius:14px;overflow:hidden}
.woocommerce div.product form.cart .button{padding:13px 30px;font-size:16px}
.woocommerce div.product .quantity .qty{padding:11px;border:1px solid var(--nl-line);border-radius:8px;width:64px}
.woocommerce-tabs ul.tabs li{border-radius:8px 8px 0 0}
.woocommerce-tabs ul.tabs li.active{background:#fff;border-bottom-color:#fff}
.woocommerce div.product .woocommerce-tabs ul.tabs li a{font-weight:600;color:var(--nl-ink)}

/* ---- on-brand notices ---- */
.woocommerce-message,.woocommerce-info,.woocommerce-noreviews,.woocommerce-error{border-top-color:var(--nl-gold);border-radius:8px}
.woocommerce-message .button,.woocommerce-info .button{background:var(--nl-gold);color:#fff}

/* ---- cart / checkout polish ---- */
.woocommerce table.shop_table{border-radius:12px;overflow:hidden;border:1px solid var(--nl-line)}
.woocommerce .cart-collaterals .cart_totals h2,.woocommerce-checkout h3{color:var(--nl-ink)}
.woocommerce form .form-row input.input-text,.woocommerce form .form-row textarea,.select2-container .select2-selection{border:1px solid var(--nl-line) !important;border-radius:8px !important;padding:11px !important}

/* ---- empty-store nudge ---- */
.woocommerce-info.woocommerce-no-products-found,.woocommerce-info{background:var(--nl-cream)}

@media(max-width:600px){
.woocommerce ul.products,.woocommerce-page ul.products{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px}
.woocommerce div.product .product_title{font-size:23px}
}
</style>
		<?php
	}
}
add_action( 'wp_head', 'nadlan_catalog_skin', 50 );

/* Make the loop add-to-cart use AJAX add (nicer than full reload) — Woo already
 * supports this on archives; ensure the theme didn't disable it. Harmless if on. */
add_filter( 'woocommerce_loop_add_to_cart_args', function ( $args ) {
	if ( is_array( $args ) ) {
		$args['class'] = trim( ( $args['class'] ?? '' ) . ' add_to_cart_button ajax_add_to_cart' );
	}
	return $args;
}, 10 );

/* Show 12 products per page on the catalog grid (cleaner than the theme default). */
add_filter( 'loop_shop_per_page', function ( $n ) {
	return 12;
}, 5 );

/* ---- v1.25.0: Featured professionals showcase ----
 * /catalog/ used to render 5 empty demo properties (no photos, ₪0). After unpublishing
 * those, the page would be blank. Inject a premium "מומחי נדל\"ן רשומים" block at the
 * top of the catalog page that surfaces the actively-importing contractor directory
 * (749+ cards from gov.il רשם הקבלנים). Real data, real cards, immediate shine.
 *
 * Also exposes [nadlan_featured_pros count=12] for use anywhere.
 */
if ( ! function_exists( 'nadlan_featured_pros_render' ) ) {
	function nadlan_featured_pros_render( $atts = array() ) {
		$a = shortcode_atts( array( 'count' => 12, 'city' => '' ), $atts );
		$args = array(
			'post_type'      => 'nadlan_professional',
			'post_status'    => 'publish',
			'posts_per_page' => max( 4, min( 24, (int) $a['count'] ) ),
			'orderby'        => 'rand',
			'meta_query'     => array(
				'relation' => 'AND',
				array( 'key' => 'classification', 'value' => '', 'compare' => '!=' ),
				array( 'key' => 'city', 'value' => '', 'compare' => '!=' ),
			),
		);
		if ( $a['city'] ) {
			$args['meta_query'][] = array( 'key' => 'city', 'value' => sanitize_text_field( $a['city'] ) );
		}
		$pros = get_posts( $args );
		if ( ! $pros ) { return ''; }
		$total = (int) wp_count_posts( 'nadlan_professional' )->publish;
		ob_start(); ?>
<section class="nlfp" dir="rtl">
	<div class="nlfp-head">
		<p class="nlfp-eyebrow">מאגר מקצועי</p>
		<h2>מומחי נדל"ן רשומים</h2>
		<p class="nlfp-sub"><?php echo number_format( $total ); ?> בעלי מקצוע מאומתים, מקור: פנקס הקבלנים הרשומים (gov.il)</p>
	</div>
	<div class="nlfp-grid">
		<?php foreach ( $pros as $p ) :
			$city  = trim( (string) get_post_meta( $p->ID, 'city', true ) );
			$cls   = trim( (string) get_post_meta( $p->ID, 'classification', true ) );
			$reg   = trim( (string) get_post_meta( $p->ID, 'registry_number', true ) );
			$cls_short = mb_strlen( $cls ) > 50 ? mb_substr( $cls, 0, 50 ) . '…' : $cls; ?>
		<a class="nlfp-card" href="<?php echo esc_url( get_permalink( $p ) ); ?>">
			<div class="nlfp-badge">קבלן רשום</div>
			<h3><?php echo esc_html( get_the_title( $p ) ); ?></h3>
			<?php if ( $city ) : ?><p class="nlfp-city"><?php echo esc_html( $city ); ?></p><?php endif; ?>
			<?php if ( $cls_short ) : ?><p class="nlfp-spec"><?php echo esc_html( $cls_short ); ?></p><?php endif; ?>
			<?php if ( $reg ) : ?><p class="nlfp-reg">רשם הקבלנים #<?php echo esc_html( $reg ); ?></p><?php endif; ?>
			<span class="nlfp-arrow">לצפייה בכרטיס →</span>
		</a>
		<?php endforeach; ?>
	</div>
	<div class="nlfp-cta">
		<a href="<?php echo esc_url( home_url( '/professionals/' ) ); ?>" class="nlfp-btn">צפו בכל <?php echo number_format( $total ); ?> בעלי המקצוע</a>
	</div>
</section>
<style>
.nlfp{font-family:var(--font-sans,Heebo,sans-serif);max-width:1240px;margin:0 auto;padding:32px 24px 16px;direction:rtl}
.nlfp-head{text-align:center;margin-bottom:28px}
.nlfp-eyebrow{font-size:11px;letter-spacing:.18em;color:#9C7A3C;font-weight:600;margin:0 0 6px;text-transform:uppercase}
.nlfp-head h2{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-weight:500;font-size:36px;color:#1B1A17;margin:0 0 8px;letter-spacing:-.015em}
.nlfp-sub{font-size:14px;color:#6b6b6b;margin:0}
.nlfp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
.nlfp-card{position:relative;background:#fff;border:1px solid rgba(27,26,23,.1);border-radius:14px;padding:22px 20px 18px;text-decoration:none;color:inherit;transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease;display:flex;flex-direction:column;min-height:200px}
.nlfp-card:hover{transform:translateY(-5px);box-shadow:0 14px 32px rgba(27,26,23,.12);border-color:rgba(156,122,60,.4)}
.nlfp-badge{display:inline-block;background:linear-gradient(135deg,#9C7A3C,#B89254);color:#fff;font-size:10px;letter-spacing:.12em;font-weight:600;padding:5px 11px;border-radius:20px;margin-bottom:14px;align-self:flex-start;box-shadow:0 3px 8px rgba(156,122,60,.25)}
.nlfp-card h3{font-family:var(--font-serif,serif);font-weight:500;font-size:18px;color:#1B1A17;margin:0 0 10px;line-height:1.35}
.nlfp-city{font-size:12px;letter-spacing:.1em;color:#9C7A3C;font-weight:600;margin:0 0 6px;text-transform:uppercase}
.nlfp-spec{font-size:13px;color:#5a5a5a;margin:0 0 8px;line-height:1.5}
.nlfp-reg{font-size:11px;color:#999;margin:0 0 14px;font-family:var(--font-mono,monospace)}
.nlfp-arrow{margin-top:auto;font-size:13px;color:#9C7A3C;font-weight:600;transition:transform .2s}
.nlfp-card:hover .nlfp-arrow{transform:translateX(-4px)}
.nlfp-cta{text-align:center;margin:32px 0 8px}
.nlfp-btn{display:inline-block;background:#1B1A17;color:#FAF7F1;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:600;font-size:15px;transition:background .2s,color .2s,transform .2s}
.nlfp-btn:hover{background:#9C7A3C;color:#fff;transform:translateY(-2px)}
@media(max-width:600px){.nlfp-head h2{font-size:26px}.nlfp-grid{grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}.nlfp-card{padding:18px 16px;min-height:170px}}
</style>
</section>
		<?php
		return ob_get_clean();
	}
}
add_shortcode( 'nadlan_featured_pros', 'nadlan_featured_pros_render' );

/* ---- v1.26.0: /catalog/ as a DIRECTORY HUB ----
 * Owner decision: /catalog/ becomes a landing page linking to all three branches of
 * the directory — properties, registered professionals (live gov.il import), and
 * urban-renewal projects — each as a premium category card with a live count. The
 * old hardcoded empty property grid is replaced by this hub. Featured contractors
 * render below so there is always real content on the page.
 */
if ( ! function_exists( 'nadlan_directory_hub_render' ) ) {
	function nadlan_directory_hub_render() {
		$prop = (int) wp_count_posts( 'nadlan_property' )->publish;
		$pros = (int) wp_count_posts( 'nadlan_professional' )->publish;
		$proj = (int) wp_count_posts( 'nadlan_project' )->publish;
		$cards = array(
			array(
				'url'   => home_url( '/professionals/' ),
				'count' => $pros,
				'label' => 'בעלי מקצוע רשומים',
				'desc'  => 'קבלנים, שמאים ומפקחים מאומתים — מתוך פנקס הקבלנים הרשומים (gov.il).',
				'cta'   => 'לאינדקס המקצועי',
				'live'  => true,
			),
			array(
				'url'   => home_url( '/urban-renewal/' ),
				'count' => $proj,
				'label' => 'פרויקטים והתחדשות עירונית',
				'desc'  => 'תמ״א 38, פינוי-בינוי ובנייה חדשה — עם מספר תוכנית, יזם וסטטוס.',
				'cta'   => 'לפרויקטים',
				'live'  => false,
			),
			array(
				'url'   => home_url( '/properties/' ),
				'count' => $prop,
				'label' => 'נכסים למכירה והשקעה',
				'desc'  => 'דירות ובתים עם בדיקה משפטית מקדימה — מחיר, חדרים, מ״ר ושכונה.',
				'cta'   => $prop > 0 ? 'לנכסים' : 'בקרוב נכסים חדשים',
				'live'  => false,
			),
		);
		ob_start(); ?>
<section class="nldh" dir="rtl">
	<div class="nldh-head">
		<p class="nldh-eyebrow">מאגר נדל״ן חכם</p>
		<h2>קטלוג נכסים, פרויקטים ובעלי מקצוע</h2>
		<p class="nldh-sub">כל מה שצריך לבדוק לפני עסקה — במקום אחד, ממקורות רשמיים.</p>
	</div>
	<div class="nldh-grid">
		<?php foreach ( $cards as $c ) : ?>
		<a class="nldh-card" href="<?php echo esc_url( $c['url'] ); ?>">
			<?php if ( $c['live'] ) : ?><span class="nldh-livedot">מתעדכן עכשיו</span><?php endif; ?>
			<div class="nldh-count"><?php echo $c['count'] > 0 ? number_format( $c['count'] ) : '—'; ?></div>
			<h3><?php echo esc_html( $c['label'] ); ?></h3>
			<p><?php echo esc_html( $c['desc'] ); ?></p>
			<span class="nldh-go"><?php echo esc_html( $c['cta'] ); ?> ←</span>
		</a>
		<?php endforeach; ?>
	</div>
</section>
<style>
.nldh{font-family:var(--font-sans,Heebo,sans-serif);max-width:1240px;margin:24px auto 8px;padding:0 24px;direction:rtl}
.nldh-head{text-align:center;margin-bottom:30px}
.nldh-eyebrow{font-size:11px;letter-spacing:.18em;color:#9C7A3C;font-weight:600;margin:0 0 6px;text-transform:uppercase}
.nldh-head h2{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-weight:500;font-size:36px;color:#1B1A17;margin:0 0 8px;letter-spacing:-.015em}
.nldh-sub{font-size:15px;color:#6b6b6b;margin:0}
.nldh-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}
.nldh-card{position:relative;background:linear-gradient(135deg,#fff,#FBF9F5);border:1px solid rgba(27,26,23,.1);border-radius:18px;padding:32px 28px;text-decoration:none;color:inherit;transition:transform .25s,box-shadow .25s,border-color .25s;display:flex;flex-direction:column;min-height:250px;overflow:hidden}
.nldh-card:hover{transform:translateY(-6px);box-shadow:0 20px 40px rgba(27,26,23,.12);border-color:rgba(156,122,60,.5)}
.nldh-livedot{position:absolute;inset-block-start:18px;inset-inline-start:18px;font-size:10px;letter-spacing:.1em;color:#2e7d32;font-weight:600;background:rgba(46,125,50,.1);padding:5px 11px;border-radius:20px}
.nldh-livedot::before{content:"●";margin-inline-end:5px;animation:nldhpulse 1.6s infinite}
@keyframes nldhpulse{0%,100%{opacity:1}50%{opacity:.3}}
.nldh-count{font-family:var(--font-serif,serif);font-size:48px;font-weight:600;color:#9C7A3C;line-height:1;margin:12px 0 14px;font-variant-numeric:tabular-nums}
.nldh-card h3{font-family:var(--font-serif,serif);font-weight:500;font-size:22px;color:#1B1A17;margin:0 0 10px;line-height:1.3}
.nldh-card p{font-size:14px;color:#5a5a5a;margin:0 0 18px;line-height:1.6}
.nldh-go{margin-top:auto;color:#9C7A3C;font-weight:600;font-size:14px;transition:transform .2s}
.nldh-card:hover .nldh-go{transform:translateX(-5px)}
@media(max-width:600px){.nldh-head h2{font-size:27px}.nldh-card{padding:26px 22px;min-height:210px}.nldh-count{font-size:38px}}
</style>
		<?php
		return ob_get_clean();
	}
}

/* Replace the /catalog/ page body with: directory hub + featured contractors. */
add_filter( 'the_content', function ( $content ) {
	if ( ! is_page() || ! in_the_loop() || ! is_main_query() ) { return $content; }
	$slug = get_post_field( 'post_name', get_queried_object_id() );
	if ( ! in_array( $slug, array( 'catalog', 'store', 'shop' ), true ) ) { return $content; }
	$prop = (int) wp_count_posts( 'nadlan_property' )->publish;
	$hub  = nadlan_directory_hub_render();
	$featured = nadlan_featured_pros_render( array( 'count' => 12 ) );
	// If real properties exist, keep the original property grid below the hub;
	// if not, replace the empty grid entirely with hub + featured pros.
	return $prop > 0 ? ( $hub . $content . $featured ) : ( $hub . $featured );
}, 15 );
