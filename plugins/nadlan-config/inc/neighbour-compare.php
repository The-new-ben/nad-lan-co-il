<?php
/**
 * nadlan-config - NEIGHBOURS SPOTLIGHT (HAD-654 R10c, 1.72.570; Claude Design v106.6 NeighbourCompare). Ben, 2.11.2026: "marketing,
 * something that promotes the project itself; price ranges according to public sources; commit to nothing; nothing that puts
 * people off". Printed right after the facts table ([nadlan_project_facts], inc/project-facts.php) of a page listed in
 * data/neighbour-spotlight.json: the page's project as the hero (rounded pills, one price range), up to three nearby projects as
 * link cards with no price, and one quiet line. Every figure is written by hand in the JSON from the sourced facts; nothing is
 * computed here. Loaded by inc/project-facts.php.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

function nadlan_nbc_data() {
	static $d = null;
	if ( null === $d ) {
		$f = dirname( __DIR__ ) . '/data/neighbour-spotlight.json';
		$d = file_exists( $f ) ? json_decode( (string) file_get_contents( $f ), true ) : array();
		if ( ! is_array( $d ) ) { $d = array(); }
	}
	return $d;
}

function nadlan_nbc_html( $id ) {
	$d = nadlan_nbc_data();
	$k = (string) (int) $id;
	if ( empty( $d['pages'][ $k ] ) || empty( $d['projects'][ $k ]['name'] ) ) { return ''; }
	$me   = $d['projects'][ $k ];
	$name = (string) $me['name'];
	$sn   = ! empty( $me['subname'] ) ? (string) $me['subname'] : $name;
	$and  = preg_match( '/^[A-Za-z0-9]/', $sn ) ? 'ו-' : 'ו';
	$h  = '<section class="nlnb" id="nlnb" dir="rtl" aria-labelledby="nlnb-h">';
	$h .= '<h2 class="nlnb-h2" id="nlnb-h">' . esc_html( ! empty( $me['h'] ) ? (string) $me['h'] : $name . ' והרובע שנבנה סביבו' ) . '</h2>';
	$h .= '<p class="nlnb-sub">' . esc_html( (string) ( $d['area'] ?? 'הרובע' ) . ' נבנה עכשיו, ' . $and . $sn . ' הוא אחד הפרויקטים החדשים בו. אלה הפרויקטים החדשים בסביבה הקרובה.' ) . '</p>';
	$h .= '<div class="nlnb-body"><div class="nlnb-hero"><span class="nlnb-tag">הפרויקט בעמוד</span>';
	$h .= '<p class="nlnb-name">' . esc_html( $name ) . ( ! empty( $me['dev'] ) ? '<small>' . esc_html( (string) $me['dev'] ) . '</small>' : '' ) . '</p>';
	if ( ! empty( $me['stats'] ) ) {
		$h .= '<ul class="nlnb-stats">';
		foreach ( (array) $me['stats'] as $s ) { $h .= '<li>' . esc_html( (string) $s ) . '</li>'; }
		$h .= '</ul>';
	}
	if ( ! empty( $me['price'] ) ) {
		$h .= '<div class="nlnb-price"><span>טווח מחירים, לפי פרסומים גלויים</span><b>' . esc_html( (string) $me['price'] ) . '</b></div>';
	}
	$h .= '</div><div class="nlnb-side"><p class="nlnb-around">גם ברובע</p><div class="nlnb-scroll"><div class="nlnb-cards">';
	foreach ( array_slice( (array) $d['pages'][ $k ], 0, 3 ) as $nid ) {
		$n = $d['projects'][ (string) $nid ] ?? null;
		if ( ! $n || empty( $n['name'] ) || empty( $n['url'] ) ) { continue; }
		$line = implode( ' · ', array_slice( (array) ( $n['stats'] ?? array() ), 0, 2 ) );
		$h .= '<a class="nlnb-card" href="' . esc_url( home_url( (string) $n['url'] ) ) . '"><b>' . esc_html( (string) $n['name'] ) . '</b>'
			. ( ! empty( $n['dev'] ) ? '<i>' . esc_html( (string) $n['dev'] ) . '</i>' : '' )
			. ( '' !== $line ? '<span>' . esc_html( $line ) . '</span>' : '' ) . '<em>לעמוד הפרויקט ←</em></a>';
	}
	$subj = rawurlencode( 'טעות בנתונים: ' . wp_strip_all_tags( get_the_title( (int) $id ) ) );
	$h .= '</div></div></div></div><p class="nlnb-note">הנתונים בקירוב, לפי פרסומים גלויים, ואינם הצעת מחיר. מצאתם טעות? <a href="mailto:info@nad-lan.co.il?subject=' . $subj . '">כתבו לנו</a></p></section>';
	return $h;
}

add_action( 'wp_head', function () {
	if ( ! is_singular() ) { return; }
	$d = nadlan_nbc_data();
	if ( empty( $d['pages'][ (string) (int) get_queried_object_id() ] ) ) { return; }
	$t = 'color-mix(in srgb,#2f6f86 6%,#fff)';
	echo '<style id="nadlan-nbc-css">'
		. '.nlnb{--ink:#14212b;--ink2:#3b4753;--muted:#5b6670;--line:#e3e1da;--sea:#2f6f86;font-family:Assistant,Heebo,"Segoe UI",Arial,sans-serif;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:22px;padding:18px;margin:24px 0;display:grid;gap:14px;max-width:900px}'
		. '.nlnb>*,.nlnb .nlnb-body>*{min-width:0}'
		. 'html body .nlnb p{margin:0!important}'
		. 'html body .nlnb h2.nlnb-h2{margin:0!important;padding:0!important;border:0!important;font:600 clamp(21px,4.6vw,26px)/1.25 "Noto Serif Hebrew","Frank Ruhl Libre",Georgia,serif!important;color:var(--ink)!important;text-align:start!important;text-wrap:balance}'
		. 'html body .nlnb h2.nlnb-h2::before,html body .nlnb h2.nlnb-h2::after{content:none!important;display:none!important}'
		. 'html body .nlnb p.nlnb-sub{font-size:14px!important;line-height:1.5!important;color:var(--ink2)!important}'
		. '.nlnb .nlnb-hero{background:' . $t . ';border-radius:16px;border-top:3px solid var(--sea);padding:16px;display:grid;gap:10px}'
		. '.nlnb .nlnb-tag{font:700 11.5px/1 Assistant,sans-serif;color:var(--sea)}'
		. 'html body .nlnb p.nlnb-name{font:600 22px/1.2 "Noto Serif Hebrew",Georgia,serif!important;color:var(--ink)!important}'
		. '.nlnb .nlnb-name small{display:block;font:600 13px/1.4 Assistant,sans-serif;color:var(--ink2);margin-top:2px}'
		. 'html body .nlnb ul.nlnb-stats{display:flex;flex-wrap:wrap;gap:8px;margin:0!important;padding:0!important;list-style:none!important}'
		. 'html body .nlnb ul.nlnb-stats li{margin:0!important;background:#fff;border:1px solid var(--line);border-radius:999px;padding:5px 12px;font:600 13.5px/1.3 Assistant,sans-serif;list-style:none!important}'
		. 'html body .nlnb ul.nlnb-stats li::before,html body .nlnb ul.nlnb-stats li::marker{content:none!important}'
		. '.nlnb .nlnb-price{display:grid;gap:2px;padding-top:10px;border-top:1px solid color-mix(in srgb,#2f6f86 20%,#fff)}'
		. '.nlnb .nlnb-price span{font:700 12px/1.3 Assistant,sans-serif;color:var(--muted)}'
		. '.nlnb .nlnb-price b{font:600 19px/1.3 "Noto Serif Hebrew",Georgia,serif;color:var(--ink)}'
		. 'html body .nlnb p.nlnb-around{font:700 13px/1.3 Assistant,sans-serif!important;color:var(--ink2)!important;margin:2px 0 8px!important}'
		. '.nlnb .nlnb-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;scroll-snap-type:x mandatory;margin:0 -18px;padding:0 18px 4px}'
		. '.nlnb .nlnb-cards{display:grid;grid-auto-flow:column;grid-auto-columns:220px;gap:10px}'
		. 'html body .nlnb a.nlnb-card{scroll-snap-align:start;border:1px solid var(--line);border-radius:14px;padding:12px;display:grid;gap:6px;align-content:start;text-decoration:none!important;color:var(--ink)!important;background:#fff}'
		. '.nlnb .nlnb-card b{font:700 15px/1.25 Assistant,sans-serif}'
		. '.nlnb .nlnb-card i{font-style:normal;font:600 12.5px/1.3 Assistant,sans-serif;color:var(--ink2)}'
		. '.nlnb .nlnb-card span{font:600 13px/1.4 Assistant,sans-serif}'
		. '.nlnb .nlnb-card em{font-style:normal;font:700 12.5px/1 Assistant,sans-serif;color:var(--sea);margin-top:4px}'
		. 'html body .nlnb p.nlnb-note{font-size:12.5px!important;line-height:1.5!important;color:var(--ink2)!important}html body .nlnb p.nlnb-note a{color:var(--sea)!important;text-decoration:underline!important;text-underline-offset:2px}'
		. '@media (min-width:760px){.nlnb .nlnb-body{display:grid;grid-template-columns:1.1fr 1.9fr;gap:16px;align-items:start}.nlnb .nlnb-scroll{margin:0;padding:0;overflow:visible}.nlnb .nlnb-cards{grid-auto-flow:row;grid-template-columns:repeat(3,1fr)}}'
		. '</style>';
}, 30 );
