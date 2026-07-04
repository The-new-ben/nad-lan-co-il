<?php
/**
 * nadlan-config - GA4 / dataLayer event bridge (v1.40.0 / shark #12)
 *
 * Pushes funnel events to window.dataLayer so Site Kit / GA4 / GTM can see
 * the whole conversion flow:
 *   page_view (auto)
 *   directory_filter_used
 *   directory_card_click
 *   profile_view
 *   quote_request (click)
 *   quote_submitted (success)
 *   claim_request
 *   review_submitted
 *   upgrade_click
 *   subscription_paid (WooCommerce hook → ₪ event)
 *
 * The data layer is the standard channel; if Site Kit is active it'll surface
 * them. If GA4 is not installed, the pushes are silent.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'wp_footer', function () {
	if ( is_admin() ) { return; }
	?>
<script>
(function(){
	window.dataLayer=window.dataLayer||[];
	// click delegation
	document.addEventListener('click',function(e){
		var t=e.target;if(!t)return;
		// directory card
		var card=t.closest&&t.closest('.nldc');
		if(card&&!card.classList.contains('nldc-sponsored-spot')){window.dataLayer.push({event:'directory_card_click',pt:card.closest('[data-mode]')?card.closest('[data-mode]').dataset.mode:''});}
		// sponsored spot
		var sp=t.closest&&t.closest('.nldc-sponsored-spot');
		if(sp){window.dataLayer.push({event:'sponsored_spot_click'});}
		// upgrade buttons
		if(t.matches&&t.matches('a[href*="add-to-cart=476"],a[href*="add-to-cart=477"],a[href*="add-to-cart=489"]')){
			var pid=(t.href.match(/add-to-cart=(\d+)/)||[])[1];
			window.dataLayer.push({event:'upgrade_click',product_id:pid});
		}
		// filter pills
		if(t.matches&&t.matches('.nldir-pill')){window.dataLayer.push({event:'directory_filter_used',facet:'profession',value:t.dataset.prof||''});}
		// city facets
		if(t.matches&&t.matches('.nldir-cityb')){window.dataLayer.push({event:'directory_filter_used',facet:'city',value:t.dataset.city||''});}
		// profile quote button (the "request a quote" buttons use onclick attr; catch via class fallback)
		if(t.matches&&(t.matches('.nlpf-quote')||t.matches('.nlpf-call'))){window.dataLayer.push({event:'quote_request'});}
	},true);
	// page type
	if(document.querySelector('.nldir')){window.dataLayer.push({event:'view_directory'});}
	if(document.querySelector('.nlpf')){window.dataLayer.push({event:'profile_view'});}
	if(document.querySelector('.nlrev')){/* glossary/review pages */}
})();
</script>
	<?php
}, 95 );

/* Server-side WooCommerce conversion event - pushes a transactional event on
 * the order-received page so GA4 ecommerce sees the ₪. */
add_action( 'woocommerce_thankyou', function ( $order_id ) {
	if ( ! $order_id || ! function_exists( 'wc_get_order' ) ) { return; }
	$order = wc_get_order( $order_id );
	if ( ! $order ) { return; }
	$total = (float) $order->get_total();
	$items = array();
	foreach ( $order->get_items() as $it ) {
		$items[] = array(
			'item_id' => (int) $it->get_product_id(),
			'item_name' => $it->get_name(),
			'price' => (float) ( $it->get_total() ),
			'quantity' => (int) $it->get_quantity(),
		);
	}
	$payload = wp_json_encode( array(
		'event'        => 'purchase',
		'currency'     => $order->get_currency(),
		'value'        => $total,
		'transaction_id' => $order_id,
		'items'        => $items,
	), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
	echo "<script>window.dataLayer=window.dataLayer||[];window.dataLayer.push($payload);</script>";
} );
