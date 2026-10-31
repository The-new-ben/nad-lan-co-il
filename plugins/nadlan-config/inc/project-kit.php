<?php
/**
 * nadlan-config - PROJECT KIT (HAD-642 loop, Ben 31.10.2026: "tools on every project, the center and luxury first, the big
 * developers"). Claude Design v105.3, component ProjectToolkit.
 *
 * [nadlan_project_kit] at the end of a developer project's article: the site's own instruments (HAD-527), pre-set for this
 * project, under one heading that leads with the project's name ("<project>: כמה זה עולה באמת"), so the kit never competes
 * with the tool pages for their own words (the instruments' headings become h3 inside it). Four tabs: all the costs (pcost,
 * new from a contractor), the construction input index (indexation), the purchase tax (ptax), a late delivery (delay).
 * The project's published price range opens it when the project has one (meta price_min / price_max); a price is never
 * invented. Additive: it is appended to the content, below everything the page already has; never inside a stage.
 * Never on Ashira (Ben). The short name comes from the meta nadlan_kit_name, else the title before " - ".
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_kit_tools' ) ) {
	function nadlan_kit_tools() {
		return array(
			'pcost'      => 'כל העלויות',
			'indexation' => 'הצמדה למדד',
			'ptax'       => 'מס רכישה',
			'delay'      => 'איחור במסירה',
		);
	}
}

add_action( 'init', function () {
	register_post_meta( 'nadlan_project', 'nadlan_kit_name', array(
		'show_in_rest'  => true,
		'single'        => true,
		'type'          => 'string',
		'auth_callback' => function ( $allowed, $meta_key, $post_id ) { return current_user_can( 'edit_post', (int) $post_id ); },
	) );
}, 20 );

/* the instruments load their engine only on pages that name their tools: the kit names its four */
add_filter( 'nadlan_nli_page_ids', function ( $ids ) {
	if ( is_singular( 'nadlan_project' ) ) {
		$p = get_post();
		if ( $p && false !== strpos( (string) $p->post_content, '[nadlan_project_kit' ) && 0 !== strpos( (string) $p->post_name, 'ashira' ) ) {
			$ids = array_values( array_unique( array_merge( (array) $ids, array_keys( nadlan_kit_tools() ) ) ) );
		}
	}
	return $ids;
} );

if ( ! function_exists( 'nadlan_kit_name' ) ) {
	function nadlan_kit_name( $id ) {
		$n = trim( (string) get_post_meta( $id, 'nadlan_kit_name', true ) );
		if ( '' !== $n ) { return $n; }
		$t = trim( wp_strip_all_tags( html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ) ) );
		$parts = preg_split( '/\s+[-–|]\s+/u', $t );
		return trim( (string) $parts[0] );
	}
}

add_shortcode( 'nadlan_project_kit', function () {
	$id = (int) get_the_ID();
	if ( ! $id || 'nadlan_project' !== get_post_type( $id ) || 0 === strpos( (string) get_post_field( 'post_name', $id ), 'ashira' ) ) { return ''; }
	if ( ! shortcode_exists( 'nadlan_tool' ) ) { return ''; }
	$name  = nadlan_kit_name( $id );
	$pmin  = (int) get_post_meta( $id, 'price_min', true );
	$pmax  = (int) get_post_meta( $id, 'price_max', true );
	$city  = trim( (string) get_post_meta( $id, 'city', true ) );
	$cityd = str_replace( array( 'תל אביב יפו', 'תל אביב-יפו' ), 'תל אביב', $city );
	$price = $pmin > 0 ? ' price="' . $pmin . '"' : '';
	$tabs = ''; $panes = ''; $i = 0;
	foreach ( nadlan_kit_tools() as $tid => $label ) {
		$extra = 'pcost' === $tid ? ' kind="new"' : '';
		$inst  = do_shortcode( '[nadlan_tool id="' . $tid . '"' . ( 'delay' === $tid ? '' : $price ) . $extra . ']' );
		if ( '' === trim( $inst ) ) { continue; }
		$inst  = preg_replace( '#<h2 class="nli__title">(.*?)</h2>#su', '<h3 class="nli__title">$1</h3>', $inst, 1 );
		$on    = 0 === $i;
		$tabs .= '<button type="button" class="nlkit-tab" role="tab" id="nlkit-t' . $i . '" aria-controls="nlkit-p' . $i . '" aria-selected="' . ( $on ? 'true' : 'false' ) . '"' . ( $on ? '' : ' tabindex="-1"' ) . '>' . esc_html( $label ) . '</button>';
		$panes .= '<div class="nlkit-pane" id="nlkit-p' . $i . '" role="tabpanel" aria-labelledby="nlkit-t' . $i . '"' . ( $on ? '' : ' hidden' ) . '>' . $inst . '</div>';
		$i++;
	}
	if ( ! $i ) { return ''; }
	$nm = '<span class="nlkit-nm">' . esc_html( $name ) . '</span>';
	$h  = '<section class="nlkit" id="nlkit" dir="rtl" aria-labelledby="nlkit-h">';
	$h .= '<p class="nlkit-k">' . esc_html( $name ) . ' · הכלים</p>';
	$h .= '<h2 class="nlkit-h2" id="nlkit-h">' . $nm . ': כמה זה עולה באמת</h2>';
	$h .= '<p class="nlkit-p">המחיר בחוזה הוא רק חלק מהסיפור. כאן רואים את כל מה שמסביבו, מכוון לפרויקט: עלויות העסקה, ההצמדה למדד תשומות הבנייה, מס הרכישה והפיצוי אם המסירה מתאחרת.</p>';
	if ( $pmin > 0 ) {
		$h .= '<div class="nlkit-price"><span>המחירים שפורסמו בפרויקט:</span><b><span class="nlkit-n">' . esc_html( number_format( $pmin ) ) . '</span>' . ( $pmax > $pmin ? ' עד <span class="nlkit-n">' . esc_html( number_format( $pmax ) ) . '</span>' : '' ) . ' ₪</b></div>';
	} else {
		$h .= '<div class="nlkit-price"><span>הכניסו בכלים את המחיר שקיבלתם מהיזם, והכול מתחשב לפיו.</span></div>';
	}
	$h .= '<div class="nlkit-tabs" role="tablist" aria-label="' . esc_attr( 'הכלים של ' . $name ) . '">' . $tabs . '</div>' . $panes;
	$h .= '<div class="nlkit-links">';
	if ( '' !== $city ) { $h .= '<a href="' . esc_url( home_url( '/projects/?city=' . rawurlencode( $city ) ) ) . '">כל הפרויקטים ב' . esc_html( $cityd ) . ' <span>←</span></a>'; }
	$h .= '<a href="' . esc_url( home_url( '/mortgage-calculator/' ) ) . '">מחשבון משכנתא <span>←</span></a>';
	$h .= '<a href="' . esc_url( home_url( '/home-inspection/' ) ) . '">בדק בית לפני מסירה <span>←</span></a></div></section>';
	$h .= '<script>(function(){var r=document.getElementById("nlkit");if(!r||r.getAttribute("data-on"))return;r.setAttribute("data-on","1");var t=[].slice.call(r.querySelectorAll(".nlkit-tab"));function s(x){t.forEach(function(b){var on=b===x;b.setAttribute("aria-selected",on?"true":"false");b.tabIndex=on?0:-1;document.getElementById(b.getAttribute("aria-controls")).hidden=!on;});}t.forEach(function(b,i){b.addEventListener("click",function(){s(b)});b.addEventListener("keydown",function(e){var j=-1;if(e.key==="ArrowLeft")j=(i+1)%t.length;else if(e.key==="ArrowRight")j=(i-1+t.length)%t.length;if(j>-1){e.preventDefault();s(t[j]);t[j].focus();}});});})();</script>';
	return $h;
} );

add_action( 'wp_head', function () {
	if ( ! is_singular( 'nadlan_project' ) ) { return; }
	$p = get_post();
	if ( ! $p || false === strpos( (string) $p->post_content, '[nadlan_project_kit' ) ) { return; }
	echo '<style id="nadlan-kit-css">'
		. '.nlkit{--ink:#14212b;--ink2:#3b4753;--line:#e3e1da;--sea:#2f6f86;--sand:#eee9dd;--paper:#f7f6f2;font-family:Assistant,Heebo,"Segoe UI",Arial,sans-serif;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:22px;padding:18px;margin:28px 0;display:grid;gap:14px;max-width:820px}'
		. '.nlkit .nlkit-n{direction:ltr;unicode-bidi:isolate;font-variant-numeric:tabular-nums}.nlkit .nlkit-nm{white-space:nowrap;unicode-bidi:isolate}'
		. 'html body .nlkit p{margin:0!important}html body .nlkit p.nlkit-k{font:700 12.5px/1.3 Assistant,Heebo,sans-serif!important;color:var(--sea)!important}'
		. 'html body .nlkit h2.nlkit-h2{margin:0!important;padding:0!important;border:0!important;font:600 clamp(21px,4.6vw,26px)/1.25 "Noto Serif Hebrew","Frank Ruhl Libre",Georgia,serif!important;color:var(--ink)!important;text-align:start!important}'
		. 'html body .nlkit h2.nlkit-h2::before,html body .nlkit h2.nlkit-h2::after{content:none!important;display:none!important}'
		. 'html body .nlkit p.nlkit-p{font-size:15px!important;line-height:1.6!important;color:var(--ink2)!important}'
		. '.nlkit .nlkit-price{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap;padding:11px 13px;border-radius:14px;background:var(--sand);font-size:14px;color:var(--ink2)}'
		. 'html body .nlkit .nlkit-price b{font:600 20px/1.25 "Noto Serif Hebrew",Georgia,serif!important;color:var(--ink)!important}'
		. '.nlkit .nlkit-tabs{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;padding:4px;border-radius:999px;background:var(--sand)}'
		. '@media(max-width:560px){.nlkit .nlkit-tabs{grid-template-columns:repeat(2,1fr);border-radius:18px}}'
		. '.nlkit .nlkit-tab{min-height:42px;border:0;border-radius:999px;background:transparent;font:700 14px/1.15 Assistant,Heebo,sans-serif;color:var(--ink2);cursor:pointer;padding:0 6px}'
		. '.nlkit .nlkit-tab[aria-selected=true]{background:#fff;color:var(--ink);box-shadow:0 1px 2px rgba(20,33,43,.08)}'
		. '.nlkit .nlkit-tab:focus-visible{outline:2px solid var(--sea);outline-offset:3px}'
		. '.nlkit .nlkit-pane[hidden]{display:none}.nlkit .nlkit-pane .nli{margin:0!important}'
		. '.nlkit .nlkit-links{display:grid;gap:6px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}'
		. 'html body .nlkit .nlkit-links a{display:flex;justify-content:space-between;align-items:center;gap:10px;min-height:46px;padding:0 14px;border:1px solid var(--line);border-radius:14px;background:#fff;color:var(--ink)!important;text-decoration:none!important;font:600 14.5px/1.3 Assistant,Heebo,sans-serif}'
		. 'html body .nlkit .nlkit-links a span{color:var(--sea)}'
		. '@media(max-width:520px){.nlkit{padding:14px;border-radius:18px}}'
		. '</style>';
}, 30 );
