<?php
/**
 * nadlan-config - Sde Dov quarter-tour teaser band (v1.72.120)
 *
 * One light band, three surfaces: the homepage (after the flagship strip),
 * the Sde Dov area page, and under the live map on every project page that
 * belongs to the quarter (Sde Dov + Einstein). Pure HTML/CSS with one lazy
 * poster image - the band never delays page load; the heavy 3D experience
 * lives on its own page and opens in a new tab.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

function nadlan_sdedov_tour_url() {
	return apply_filters( 'nadlan_sdedov_tour_url', 'https://nad-lan.co.il/wp-content/uploads/2026/07/sde-dov-tour.html' );
}

function nadlan_sdedov_tour_poster() {
	return apply_filters( 'nadlan_sdedov_tour_poster', 'https://nad-lan.co.il/wp-content/uploads/2026/07/sdedov-tour-poster.jpg' );
}

/* Every catalog project that belongs to the quarter. Filterable so new
 * projects join with one line and future compounds can reuse the module. */
function nadlan_sdedov_tour_slugs() {
	return apply_filters( 'nadlan_sdedov_tour_slugs', array(
		'rainbow-tel-aviv', 'ashira-sde-dov', 'dimri-yama-sde-dov',
		'utopia-sde-dov', 'first-sde-dov', 'zohi-sde-dov', 'gindi-vogue-sde-dov',
		'migdalei-hayam-sde-dov', 'shikun-binui-sde-dov',
		'einstein-tower', 'einstein-19', 'ashdar-einstein',
	) );
}

/* Flagships that have a named node inside the tour - deep link straight to them. */
function nadlan_sdedov_tour_focus( $slug ) {
	$map = array( 'rainbow-tel-aviv' => 'rainbow', 'ashira-sde-dov' => 'ashira', 'dimri-yama-sde-dov' => 'dimri' );
	return isset( $map[ $slug ] ) ? $map[ $slug ] : '';
}

function nadlan_sdedov_tour_css() {
	static $done = false;
	if ( $done ) { return ''; }
	$done = true;
	return '<style id="nlsdt-css">'
		. '.nlsdt{position:relative;overflow:hidden;border-radius:18px;margin:26px auto;max-width:1240px;background:#101826;color:#fff;direction:rtl}'
		. '.nlsdt-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55}'
		. '.nlsdt-in{position:relative;z-index:2;padding:34px 30px;background:linear-gradient(90deg,rgba(10,15,26,.88) 0%,rgba(10,15,26,.55) 55%,rgba(10,15,26,.15) 100%)}'
		. '.nlsdt-kick{font:700 13px/1 Heebo,sans-serif;letter-spacing:.12em;color:#F2C14E;margin:0 0 8px}'
		. '.nlsdt h2,.nlsdt-title{font:900 clamp(22px,3vw,32px)/1.2 Heebo,sans-serif;margin:0 0 8px;color:#fff}'
		. '.nlsdt-sub{font:400 15.5px/1.6 Heebo,sans-serif;color:#D9E0EC;max-width:34em;margin:0 0 14px}'
		. '.nlsdt-chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 18px;padding:0;list-style:none}'
		. '.nlsdt-chips li{font:600 12.5px/1 Heebo,sans-serif;color:#EFE3C8;border:1px solid rgba(242,193,78,.45);border-radius:999px;padding:7px 12px}'
		. '.nlsdt-cta{display:inline-block;background:#E2701F;color:#fff;font:800 16px/1 Heebo,sans-serif;border-radius:10px;padding:13px 26px;text-decoration:none}'
		. '.nlsdt-cta:hover{background:#C05A12;color:#fff}'
		. '.nlsdt-cta2{display:inline-block;margin-inline-start:12px;color:#F2C14E;font:700 14px/1 Heebo,sans-serif;text-decoration:none}'
		. '.nlsdt-note{font:400 11.5px/1.5 Heebo,sans-serif;color:#94A0B4;margin:12px 0 0}'
		. '@media(max-width:640px){.nlsdt-in{padding:24px 18px;background:linear-gradient(180deg,rgba(10,15,26,.35) 0%,rgba(10,15,26,.9) 60%)}.nlsdt-cta{display:block;text-align:center}.nlsdt-cta2{display:block;margin:10px 0 0;text-align:center}}'
		. '</style>';
}

/**
 * The band itself.
 *
 * @param string $variant 'home' | 'project' | 'page'
 * @param string $focus   optional tour node key (rainbow|ashira|dimri)
 */
function nadlan_sdedov_tour_band( $variant = 'home', $focus = '' ) {
	$url  = nadlan_sdedov_tour_url();
	$link = $focus ? $url . '?focus=' . rawurlencode( $focus ) . '&mode=explore' : $url;
	$html = nadlan_sdedov_tour_css();
	$html .= '<section class="nlsdt" aria-label="סיור תלת ממדי ברובע שדה דב">'
		. '<img class="nlsdt-img" src="' . esc_url( nadlan_sdedov_tour_poster() ) . '" alt="" loading="lazy" decoding="async">'
		. '<div class="nlsdt-in">'
		. '<p class="nlsdt-kick">חדש · סיור תלת ממדי חי</p>'
		. '<p class="nlsdt-title">נכנסים לעתיד של רובע שדה דב</p>'
		. '<p class="nlsdt-sub">' . ( 'project' === $variant
			? 'הפרויקט הזה הוא חלק מרובע שלם שקם על קו החוף. מסתובבים ברחובות של 2035, עוברים בין המגדלים, ורואים איך הכול מתחבר.'
			: 'מסתובבים ברחובות הרובע של 2035, עוברים בין המגדלים, יורדים לטיילת, ובוחרים דירה מתוך הבניין. הדמיה חיה בדפדפן, בלי להוריד כלום.' )
		. '</p>'
		. '<ul class="nlsdt-chips"><li>מכונת זמן 2026 ⇄ 2035</li><li>סיור חופשי עם חצים</li><li>כל בניין לחיץ</li></ul>'
		. '<a class="nlsdt-cta" href="' . esc_url( $link ) . '" target="_blank" rel="noopener">כניסה לסיור</a>'
		. ( ( 'project' === $variant && $focus ) ? '<a class="nlsdt-cta2" href="' . esc_url( $url ) . '" target="_blank" rel="noopener">או מתחילים מתצפית על כל הרובע ←</a>' : '' )
		. '<p class="nlsdt-note">הדמיה להמחשה על פי תכנית רובע שדה דב. אינה מטעם היזמים או גורם רשמי.</p>'
		. '</div></section>';
	return $html;
}

/* Surface 3: the Sde Dov area page gets the full band appended to its content. */
function nadlan_sdedov_tour_page_append( $content ) {
	if ( is_page( 'sde-dov' ) && in_the_loop() && is_main_query() ) {
		$content .= nadlan_sdedov_tour_band( 'page' );
	}
	return $content;
}
add_filter( 'the_content', 'nadlan_sdedov_tour_page_append', 21 );
