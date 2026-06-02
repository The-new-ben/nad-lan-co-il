<?php
/**
 * nadlan-config — Pricing page schema + meta (v1.40.0 / shark #10)
 *
 * Adds Product + Offer JSON-LD on /join-pro/ so Google's rich results show
 * the price + "free trial" + ratings (once we have any). Also sets a clean
 * Yoast-friendly meta title/description. Pure SEO play: rich snippets get
 * +20-35% CTR vs. plain results.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_pricing_is_page' ) ) {
	function nadlan_pricing_is_page() {
		if ( ! is_page() ) { return false; }
		$slug = get_post_field( 'post_name', get_queried_object_id() );
		return in_array( $slug, array( 'join-pro', 'pricing' ), true );
	}
}

add_action( 'wp_head', function () {
	if ( ! nadlan_pricing_is_page() ) { return; }
	$products = array(
		array(
			'name' => 'Pro — אנשי מקצוע (חודש ראשון חינם)',
			'description' => 'תוכנית Pro למאגר נדל"ן חכם: פרסום מקודם של הכרטיס, חשיפה של פרטי קשר, גלריית תמונות, קבלת לידים חמים.',
			'sku'  => 'NL-PRO-476',
			'price' => '349.00',
			'url' => home_url( '/?add-to-cart=476' ),
		),
		array(
			'name' => 'Premier — חשיפה מוגברת',
			'description' => 'תוכנית Premier: כל יתרונות Pro + תג מאומת + מיקום בלעדי באזור + קמפיין מיקרו-תוכן.',
			'sku'  => 'NL-PREMIER-477',
			'price' => '749.00',
			'url' => home_url( '/?add-to-cart=477' ),
		),
		array(
			'name' => 'קמפיין פרויקט — יזמים וקבלנים',
			'description' => 'קמפיין מקודם של פרויקט נדל"ן (תמ"א 38, פינוי בינוי, בנייה חדשה) במאגר נדל"ן חכם.',
			'sku'  => 'NL-PROJECT-489',
			'price' => '3990.00',
			'url' => home_url( '/?add-to-cart=489' ),
		),
	);
	foreach ( $products as $pr ) {
		$ld = array(
			'@context' => 'https://schema.org',
			'@type'    => 'Product',
			'name'     => $pr['name'],
			'description' => $pr['description'],
			'sku'      => $pr['sku'],
			'brand'    => array( '@type' => 'Brand', 'name' => 'נדל"ן חכם' ),
			'offers'   => array(
				'@type' => 'Offer',
				'priceCurrency' => 'ILS',
				'price' => $pr['price'],
				'availability' => 'https://schema.org/InStock',
				'url' => $pr['url'],
			),
		);
		echo "\n<script type=\"application/ld+json\">" . wp_json_encode( $ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
	}
}, 25 );

add_filter( 'pre_get_document_title', function ( $t ) {
	if ( nadlan_pricing_is_page() ) {
		return 'הצטרפו כמקצוען — Pro / Premier / קמפיין פרויקט | נדל"ן חכם';
	}
	return $t;
}, 25 );

add_filter( 'wpseo_metadesc', function ( $d ) {
	if ( nadlan_pricing_is_page() ) {
		return 'הצטרפו למאגר נדל"ן חכם — Pro ₪349/חודש, Premier ₪749/חודש, קמפיין פרויקט ₪3,990. חודש ראשון חינם. חשיפה לאלפי קונים פוטנציאליים בחודש.';
	}
	return $d;
} );
