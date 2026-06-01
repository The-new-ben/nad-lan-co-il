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
