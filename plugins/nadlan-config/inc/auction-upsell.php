<?php
/**
 * Auction upsell inside the listing flow.
 *
 * Owner call: the sale-by-offers product must be offered where sellers
 * already are - "when someone wants to open a listing, offer him: why don't
 * you sell in auction". The property wizard is that moment. This appends a
 * quiet aside under the wizard rather than editing the wizard itself:
 * additive, zero risk to the flow, and it links the offers landing plus the
 * michraz pillar (internal-link equity flows both ways).
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_filter( 'the_content', function ( $content ) {
	/* the wizard (or its signup gate) is on this page */
	if ( false === strpos( $content, 'id="nlpw' ) || false !== strpos( $content, 'nl-auction-upsell' ) ) {
		return $content;
	}
	$html = '<aside class="nl-auction-upsell" dir="rtl">'
		. '<b>יש גם דרך אחרת למכור: מכירה בהצעות</b>'
		. '<span>במקום לנקוב מחיר סגור, הקונים מגישים הצעות ואתם בוחרים את הטובה שבהן, או אף אחת. '
		. 'ההצעות אינן מחייבות, התהליך שקוף, ומתאים במיוחד לנכסים עם ביקוש.</span>'
		. '<span class="nl-auction-upsell__links">'
		. '<a href="' . esc_url( home_url( '/sell-by-auction/' ) ) . '">איך זה עובד</a>'
		. '<a href="' . esc_url( home_url( '/michraz-dirot/' ) ) . '" class="ghost">המדריך המלא למכרזי דירות</a>'
		. '</span></aside>';
	return $content . $html;
}, 30 );

add_action( 'wp_enqueue_scripts', function () {
	wp_register_style( 'nadlan-auction-upsell', false, array(), NADLAN_CONFIG_VERSION );
	wp_enqueue_style( 'nadlan-auction-upsell' );
	wp_add_inline_style(
		'nadlan-auction-upsell',
		'.nl-auction-upsell{display:block;background:#FBF7EC;border:1px solid #E2DCD0;' .
		'border-inline-start:4px solid #9C7A3C;border-radius:12px;padding:16px 18px;margin:22px 0 0;' .
		'font-family:Heebo,system-ui,sans-serif}' .
		'.nl-auction-upsell b{display:block;font-size:15px;color:#1B1A17;margin-bottom:6px}' .
		'.nl-auction-upsell span{display:block;font-size:13.5px;line-height:1.65;color:#4B4639}' .
		'.nl-auction-upsell__links{margin-top:10px}' .
		'.nl-auction-upsell__links a{display:inline-block;background:#B85410;color:#fff;text-decoration:none;' .
		'font-weight:700;font-size:13px;border-radius:8px;padding:8px 14px;margin-inline-end:8px}' .
		'.nl-auction-upsell__links a.ghost{background:transparent;border:1px solid #C9BFA9;color:#6D5A2E}'
	);
}, 22 );
