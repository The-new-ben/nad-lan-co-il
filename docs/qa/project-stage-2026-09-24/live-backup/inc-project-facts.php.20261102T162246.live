<?php
/**
 * nadlan-config - PROJECT FACTS (HAD-654 radius loop R2b, 1.11.2026; Claude Design v105.5 ProjectFacts). [nadlan_project_facts]
 * at the top of a developer project's article: the project's facts in one place, each with its source as a link, under a line
 * that says when they were checked. It is the part of Rainbow's page that ChatGPT quotes (GA4: 246 ChatGPT visits in 5 months,
 * Rainbow first), now on the pages that had the facts only inside their prose. The stage pages already carry their own facts
 * panel (.nlpf) and do not get this one. Data: data/project-facts.json, written by hand from named, dated sources; a row
 * without a source is never drawn.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

function nadlan_pfx_data() {
	static $d = null;
	if ( null === $d ) {
		$f = dirname( __DIR__ ) . '/data/project-facts.json';
		$d = file_exists( $f ) ? json_decode( (string) file_get_contents( $f ), true ) : array();
		if ( ! is_array( $d ) ) { $d = array(); }
	}
	return $d;
}

add_shortcode( 'nadlan_project_facts', function ( $atts ) {
	$a  = shortcode_atts( array( 'id' => 0 ), $atts );
	$id = (int) $a['id'] ? (int) $a['id'] : (int) get_the_ID();
	$d  = nadlan_pfx_data();
	$p  = $d[ (string) $id ] ?? null;
	if ( ! $p || empty( $p['rows'] ) ) { return ''; }
	$rows = array_filter( (array) $p['rows'], function ( $r ) { return ! empty( $r['k'] ) && ! empty( $r['v'] ) && ! empty( $r['src'] ); } );
	if ( ! $rows ) { return ''; }
	$names = array();
	foreach ( $rows as $r ) {
		$n = trim( preg_replace( '/,.*$/u', '', (string) $r['src'] ) );
		if ( '' !== $n && ! in_array( $n, $names, true ) ) { $names[] = $n; }
	}
	$h  = '<section class="nlfx" id="nlfx" dir="rtl" aria-labelledby="nlfx-h">';
	$h .= '<p class="nlfx-upd">עודכן ב' . esc_html( (string) ( $p['checked'] ?? '' ) ) . ' · מקורות: ' . esc_html( implode( ', ', $names ) ) . '</p>';
	$h .= '<h2 class="nlfx-h2" id="nlfx-h">' . esc_html( (string) ( $p['title'] ?? '' ) ) . '</h2><dl class="nlfx-dl">';
	foreach ( $rows as $r ) {
		$src = esc_html( (string) $r['src'] );
		$h  .= '<dt>' . esc_html( (string) $r['k'] ) . '</dt><dd><b>' . esc_html( (string) $r['v'] ) . '</b>'
			. ( ! empty( $r['url'] ) ? '<a class="nlfx-s" href="' . esc_url( (string) $r['url'] ) . '" target="_blank" rel="noopener">' . $src . '</a>' : '<span class="nlfx-s">' . $src . '</span>' ) . '</dd>';
	}
	$h .= '</dl></section>';
	return $h;
} );

add_action( 'wp_head', function () {
	if ( ! is_singular() ) { return; }
	$p = get_post();
	if ( ! $p || false === strpos( (string) $p->post_content, '[nadlan_project_facts' ) ) { return; }
	$t = 'color-mix(in srgb,var(--sa-sea,#2f6f86) 9%,#fff)';
	echo '<style id="nadlan-pfx-css">'
		. '.nlfx{--ink:#14212b;--ink2:#3b4753;--line:#e3e1da;--sea:#2f6f86;font-family:Assistant,Heebo,"Segoe UI",Arial,sans-serif;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:22px;padding:18px;margin:24px 0;display:grid;gap:10px;max-width:900px}'
		. 'html body .nlfx p{margin:0!important}html body .nlfx p.nlfx-upd{font-size:13px!important;line-height:1.45!important;color:var(--ink2)!important}'
		. 'html body .nlfx h2.nlfx-h2{margin:0!important;padding:0!important;border:0!important;font:600 clamp(21px,4.6vw,26px)/1.25 "Noto Serif Hebrew","Frank Ruhl Libre",Georgia,serif!important;color:var(--ink)!important;text-align:start!important;text-wrap:balance}'
		. 'html body .nlfx h2.nlfx-h2::before,html body .nlfx h2.nlfx-h2::after{content:none!important;display:none!important}'
		. 'html body .nlfx dl.nlfx-dl{margin:0!important;display:grid;grid-template-columns:minmax(92px,auto) 1fr;gap:0}'
		. 'html body .nlfx dl.nlfx-dl dt,html body .nlfx dl.nlfx-dl dd{margin:0!important;padding:9px 0!important;border-bottom:1px solid var(--line)}'
		. 'html body .nlfx dl.nlfx-dl dt{font:700 13px/1.4 Assistant,sans-serif!important;color:var(--ink2)!important;padding-inline-end:12px!important}'
		. 'html body .nlfx dl.nlfx-dl dd{display:grid;gap:4px;justify-items:start}'
		. '.nlfx dd b{font:600 15.5px/1.4 "Noto Serif Hebrew",Georgia,serif;color:var(--ink)}'
		. 'html body .nlfx .nlfx-s{font:600 11.5px/1.3 Assistant,sans-serif!important;padding:2px 8px;border-radius:999px;background:' . $t . ';color:var(--ink)!important;text-decoration:none!important}'
		. '</style>';
}, 30 );
