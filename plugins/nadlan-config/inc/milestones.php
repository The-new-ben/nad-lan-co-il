<?php
/**
 * nadlan-config - PROJECT MILESTONE TRACKER (2026-07-07, world-scan cycle).
 *
 * The Amazon/Lennar/Buildertrend pattern Israeli buyers never get: where the
 * project stands on the road from planning to keys. Rendered ONLY from real
 * data - the project's own project_status meta (already curated in the CMS)
 * mapped onto the canonical Israeli lifecycle. No status = no band (collapse
 * law). Language siblings (slug-en/-fr/-ru/-ar) inherit the base project's
 * status so the ladder is never duplicated by hand.
 *
 *  Stages: תכנון -> היתר בנייה -> שיווק ומכירות -> בנייה -> טופס 4 ומסירה
 *
 * Token order matters: 'בהיתר בנייה' must match permit before construction.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ms_stage_of' ) ) {
	function nadlan_ms_stage_of( $status ) {
		$s = trim( (string) $status );
		if ( '' === $s ) { return -1; }
		// ordered token => stage index checks (first hit wins)
		$checks = array(
			array( array( 'טופס 4', 'מסירה', 'אכלוס', 'הושלם' ), 4 ),
			array( array( 'היתר' ), 1 ),
			array( array( 'בנייה', 'בביצוע', 'שלד' ), 3 ),
			array( array( 'שיווק', 'מכירה', 'מכירות' ), 2 ),
			array( array( 'תכנון', 'תכנית', 'סטטוטורי', 'מימוש' ), 0 ),
		);
		foreach ( $checks as $c ) {
			foreach ( $c[0] as $tk ) {
				if ( false !== mb_stripos( $s, $tk ) ) { return $c[1]; }
			}
		}
		return -1;
	}
}

if ( ! function_exists( 'nadlan_ms_status_for' ) ) {
	/* the post's own status, or the base project's when this is a lang sibling */
	function nadlan_ms_status_for( $post ) {
		$st = (string) get_post_meta( $post->ID, 'project_status', true );
		if ( trim( $st ) !== '' ) { return $st; }
		if ( preg_match( '/^(.*)-(en|fr|ru|ar)$/', $post->post_name, $m ) ) {
			$base = get_page_by_path( $m[1], OBJECT, 'nadlan_project' );
			if ( $base ) { return (string) get_post_meta( $base->ID, 'project_status', true ); }
		}
		return '';
	}
}

add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
	$post   = get_post();
	$status = nadlan_ms_status_for( $post );
	$stage  = nadlan_ms_stage_of( $status );
	if ( $stage < 0 ) { return $content; }
	$en = (bool) preg_match( '/-en$/', $post->post_name );
	$labels = $en
		? array( 'Planning', 'Building permit', 'Sales', 'Construction', 'Form 4 + delivery' )
		: array( 'תכנון', 'היתר בנייה', 'שיווק ומכירות', 'בנייה', 'טופס 4 ומסירה' );
	$title  = $en ? 'Where the project stands' : 'איפה הפרויקט עומד';
	$note   = $en
		? 'Stage as reported for the project; timelines are the developer\'s responsibility.'
		: 'השלב כפי שדווח לפרויקט; לוחות הזמנים באחריות היזם.';
	$steps = '';
	foreach ( $labels as $i => $l ) {
		$cls = $i < $stage ? 'is-done' : ( $i === $stage ? 'is-now' : '' );
		$steps .= '<li class="' . $cls . '"><i></i><span>' . esc_html( $l ) . '</span></li>';
	}
	$band = '<section class="nlms" dir="' . ( $en ? 'ltr' : 'rtl' ) . '" aria-label="' . esc_attr( $title ) . '">' .
		'<div class="nlms-head"><span class="nlms-eyebrow">' . esc_html( $title ) . '</span>' .
		'<b class="nlms-status">' . esc_html( trim( $status ) ) . '</b></div>' .
		'<ol class="nlms-steps" style="--nlms-p:' . ( $stage / ( count( $labels ) - 1 ) * 100 ) . '%">' . $steps . '</ol>' .
		'<p class="nlms-note">' . esc_html( $note ) . '</p></section>';
	return $band . $content;
}, 12 );

/* The band's css used to travel INSIDE the content as a <style> block. Found
   live 2026-08-05: the raw css surfaced as readable TEXT near the top of the
   page, so Google's first impression of a project page included
   ".nlms{background:#fff..." as content. Styles belong in the style pipeline,
   never in the content stream. */
add_action( 'wp_enqueue_scripts', function () {
	if ( ! is_singular( 'nadlan_project' ) ) {
		return;
	}
	$css = '.nlms{background:#fff;border:1px solid #E2DCD0;border-radius:16px;padding:20px 22px 14px;margin:6px 0 26px;font-family:Heebo,system-ui,sans-serif}'
		. '.nlms-head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:16px}'
		. '.nlms-eyebrow{font:700 11.5px/1 Heebo,sans-serif;letter-spacing:.12em;color:#9C7A3C}'
		. '.nlms-status{font-family:"Frank Ruhl Libre",serif;font-size:1.15rem;color:#1B1A17}'
		. '.nlms-steps{list-style:none;display:flex;margin:0;padding:0;position:relative}'
		. '.nlms-steps::before{content:"";position:absolute;top:8px;inset-inline:9%;height:2px;background:#E2DCD0}'
		. '.nlms-steps::after{content:"";position:absolute;top:8px;inset-inline-start:9%;width:calc(var(--nlms-p) * .82);height:2px;background:#9C7A3C}'
		. '.nlms-steps li{flex:1;text-align:center;position:relative;z-index:1}'
		. '.nlms-steps i{display:block;width:18px;height:18px;border-radius:50%;background:#fff;border:2px solid #D8D2C6;margin:0 auto 7px}'
		. '.nlms-steps li.is-done i{background:#9C7A3C;border-color:#9C7A3C}'
		. '.nlms-steps li.is-now i{background:#C2563A;border-color:#C2563A;box-shadow:0 0 0 4px rgba(194,86,58,.18)}'
		. '.nlms-steps span{font:600 11.5px/1.35 Heebo,sans-serif;color:#6D665C;display:block;padding:0 3px}'
		. '.nlms-steps li.is-now span{color:#1B1A17;font-weight:700}'
		. '.nlms-note{font:400 11.5px/1.5 Heebo,sans-serif;color:#6D665C;margin:14px 0 0}'
		. '@media(max-width:560px){.nlms-steps span{font-size:10px}}'
		/* the promoted lead paragraph reads as the page opener; give it lead weight */
		/* max-width + auto margins + padding: the FIRST REAL SCREENSHOT (owner's
		   Chrome, 2026-08-08) showed the lead running full-bleed at desktop with
		   "Rainbow" clipped off both edges - the guide templates give the entry
		   no column, so the lead must carry its own. unicode-bidi:plaintext keeps
		   a mixed Hebrew/English first line from exploding the direction. */
		/* min() with a vw guard: the guide wrapper can sit slightly off-canvas, so
		   1240px alone still clipped a letter at the right edge. Standard bidi
		   reordering handles the English-first opening; plaintext made it worse. */
		. '.nl-lead{font-size:1.06em;line-height:1.75;margin:0 auto 14px;max-width:min(1240px,92vw);'
		. 'padding:0 clamp(14px,3vw,26px);box-sizing:border-box;overflow-wrap:break-word}'
		. '@media(max-width:560px){.nl-lead{font-size:1.02em}}';
	wp_register_style( 'nadlan-milestones', false, array(), NADLAN_CONFIG_VERSION );
	wp_enqueue_style( 'nadlan-milestones' );
	wp_add_inline_style( 'nadlan-milestones', $css );
}, 21 );
