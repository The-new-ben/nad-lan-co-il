<?php
/**
 * nadlan-config - CITY PROJECTS (HAD-642 loop L3a, 1.11.2026; Claude Design v105.4 CityProjects). [nadlan_city_projects
 * city="<registry spelling>"] on the page that already owns the city (its price page): the city's developer projects and its
 * urban-renewal compounds by stage, each a card linking to its page, with the registry's city numbers. It gives the owner page
 * "פרויקטים חדשים ב<city>" without a new URL (the URL word law). Unknown values are omitted, never shown as 0.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

add_shortcode( 'nadlan_city_projects', function ( $atts ) {
	$a    = shortcode_atts( array( 'city' => '', 'limit' => 12 ), $atts );
	$city = trim( (string) $a['city'] );
	if ( '' === $city ) { return ''; }
	$disp = preg_replace( '/^קרית /u', 'קריית ', str_replace( array( 'תל אביב יפו', 'תל אביב-יפו', 'גבעתים', 'פתח תקוה' ), array( 'תל אביב', 'תל אביב', 'גבעתיים', 'פתח תקווה' ), $city ) );
	$ck   = 'nlcp_' . md5( $city . '|' . (int) $a['limit'] . '|v2' );
	$out  = get_transient( $ck );
	if ( is_string( $out ) && '' !== $out ) { return $out; }
	$ids = get_posts( array( 'post_type' => 'nadlan_project', 'post_status' => 'publish', 'posts_per_page' => 400, 'fields' => 'ids', 'no_found_rows' => true,
		'meta_query' => array( array( 'key' => 'city', 'value' => $city ) ) ) );
	$dev = array(); $comp = array();
	foreach ( $ids as $id ) {
		$slug = (string) get_post_field( 'post_name', $id );
		if ( preg_match( '/-(en|fr|ru|ar)$/', $slug ) ) { continue; }
		if ( 'urban_renewal' === (string) get_post_meta( $id, 'source', true ) ) {
			$st = preg_replace( '/\s+[-–]\s+/u', ' · ', preg_replace( '/\s+/u', ' ', trim( (string) get_post_meta( $id, 'project_status', true ) ) ) );
			$rk = false !== mb_strpos( $st, 'במימוש' ) || false !== mb_strpos( $st, 'אחרי רישוי' ) ? 0 : ( false !== mb_strpos( $st, 'לפני מימוש' ) ? 1 : ( false !== mb_strpos( $st, 'סטטוטורי' ) ? 2 : 3 ) );
			$comp[] = array( 'id' => $id, 'st' => $st, 'rk' => $rk, 'u' => (int) get_post_meta( $id, 'num_units', true ) );
		} else {
			$dev[] = array( 'id' => $id, 'd' => trim( (string) get_post_meta( $id, 'developer_name', true ) ) );
		}
	}
	usort( $comp, function ( $x, $y ) { return $x['rk'] === $y['rk'] ? $y['u'] <=> $x['u'] : $x['rk'] <=> $y['rk']; } );
	$GLOBALS['nlcpj_disp'] = $disp; $GLOBALS['nlcpj_city'] = $city;
	$name = function ( $id ) {
		$t = trim( wp_strip_all_tags( html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ) ) );
		$t = preg_replace( '/:\s*פינוי בינוי.*$/u', '', $t );
		$t = preg_replace( '/,\s*(?:' . preg_quote( $GLOBALS['nlcpj_disp'] ?? '', '/' ) . '|' . preg_quote( $GLOBALS['nlcpj_city'] ?? '', '/' ) . ')\s*$/u', '', $t ); // the block names its city once
		$p = preg_split( '/\s+[-–|]\s+/u', $t );
		return trim( (string) $p[0] );
	};
	$cs = function_exists( 'nadlan_cv2_city' ) ? nadlan_cv2_city( $city, 0, 0 ) : array();
	$h  = '<section class="nlcpj" id="nlcpj" dir="rtl" aria-labelledby="nlcpj-h"><p class="nlcpj-k">' . esc_html( $disp ) . ' · פרויקטים</p>';
	$h .= '<h2 class="nlcpj-h2" id="nlcpj-h">פרויקטים חדשים והתחדשות עירונית ב' . esc_html( $disp ) . '</h2>';
	if ( ! empty( $cs['n'] ) ) {
		$h .= '<p class="nlcpj-p">במאגר הרשות הממשלתית להתחדשות עירונית רשומים ב' . esc_html( $disp ) . ' ' . number_format( (int) $cs['n'] ) . ' מתחמי פינוי בינוי'
			. ( ! empty( $cs['approved'] ) ? ', ל-' . number_format( (int) $cs['approved'] ) . ' מהם תכנית מאושרת' : '' )
			. ( ! empty( $cs['permits'] ) ? ', ו-' . number_format( (int) $cs['permits'] ) . ' דירות כבר קיבלו היתר' : '' ) . '.</p>';
	}
	if ( $dev ) {
		$h .= '<h3 class="nlcpj-h3">פרויקטים של יזמים ב' . esc_html( $disp ) . '</h3><div class="nlcpj-grid">';
		foreach ( $dev as $d ) {
			$h .= '<a class="nlcpj-card" href="' . esc_url( get_permalink( $d['id'] ) ) . '"><b>' . esc_html( $name( $d['id'] ) ) . '</b>' . ( '' !== $d['d'] ? '<span>' . esc_html( $d['d'] ) . '</span>' : '' ) . '</a>';
		}
		$h .= '</div>';
	}
	if ( $comp ) {
		$h .= '<h3 class="nlcpj-h3">מתחמי פינוי בינוי ב' . esc_html( $disp ) . ', לפי שלב</h3><div class="nlcpj-grid">';
		foreach ( array_slice( $comp, 0, max( 1, (int) $a['limit'] ) ) as $c ) {
			$h .= '<a class="nlcpj-card" href="' . esc_url( get_permalink( $c['id'] ) ) . '"><b>' . esc_html( $name( $c['id'] ) ) . '</b>'
				. ( '' !== $c['st'] ? '<i>' . esc_html( $c['st'] ) . '</i>' : '' )
				. ( $c['u'] > 0 ? '<span><span class="nlcpj-n">' . number_format( $c['u'] ) . '</span> דירות בתכנית</span>' : '' ) . '</a>';
		}
		$h .= '</div><a class="nlcpj-all" href="' . esc_url( home_url( '/projects/?city=' . rawurlencode( $city ) ) ) . '">לכל ' . number_format( count( $comp ) ) . ' המתחמים ב' . esc_html( $disp ) . ' ←</a>';
	}
	if ( ! empty( $cs['file_date'] ) && preg_match( '/^(\d{4})-(\d{2})-(\d{2})/', $cs['file_date'], $m ) ) {
		$h .= '<p class="nlcpj-src">לפי מאגר הרשות הממשלתית להתחדשות עירונית (data.gov.il), עדכון הקובץ ' . (int) $m[3] . '.' . (int) $m[2] . '.' . $m[1] . '.</p>';
	}
	$h .= '</section>';
	if ( ! $dev && ! $comp ) { $h = ''; }
	set_transient( $ck, $h, 6 * HOUR_IN_SECONDS );
	return $h;
} );

add_action( 'wp_head', function () {
	if ( ! is_singular() ) { return; }
	$p = get_post();
	if ( ! $p || false === strpos( (string) $p->post_content, '[nadlan_city_projects' ) ) { return; }
	echo '<style id="nadlan-cpj-css">'
		. '.nlcpj{--ink:#14212b;--ink2:#3b4753;--line:#e3e1da;--sea:#2f6f86;--sand:#eee9dd;font-family:Assistant,Heebo,"Segoe UI",Arial,sans-serif;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:22px;padding:18px;margin:28px 0;display:grid;gap:12px;max-width:900px}'
		. 'html body .nlcpj p{margin:0!important}html body .nlcpj p.nlcpj-k{font:700 12.5px/1.3 Assistant,Heebo,sans-serif!important;color:var(--sea)!important}'
		. 'html body .nlcpj h2.nlcpj-h2{margin:0!important;padding:0!important;border:0!important;font:600 clamp(21px,4.6vw,26px)/1.25 "Noto Serif Hebrew","Frank Ruhl Libre",Georgia,serif!important;color:var(--ink)!important;text-align:start!important}'
		. 'html body .nlcpj h2.nlcpj-h2::before,html body .nlcpj h2.nlcpj-h2::after,html body .nlcpj h3.nlcpj-h3::before{content:none!important;display:none!important}'
		. 'html body .nlcpj h3.nlcpj-h3{margin:6px 0 0!important;padding:0!important;border:0!important;font:600 17px/1.3 "Noto Serif Hebrew",Georgia,serif!important;color:var(--ink)!important}'
		. 'html body .nlcpj p.nlcpj-p{font-size:15px!important;line-height:1.6!important;color:var(--ink2)!important}'
		. '.nlcpj .nlcpj-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px}'
		. 'html body .nlcpj a.nlcpj-card{display:grid;gap:4px;padding:11px 13px;border:1px solid var(--line);border-radius:14px;background:#fff;text-decoration:none!important;color:var(--ink)!important}'
		. 'html body .nlcpj a.nlcpj-card:hover{border-color:var(--sea)}'
		. '.nlcpj a.nlcpj-card b{font:600 15.5px/1.3 "Noto Serif Hebrew",Georgia,serif}.nlcpj a.nlcpj-card i{justify-self:start;font-style:normal;font:700 12px/1.3 Assistant,sans-serif;padding:3px 9px;border-radius:999px;background:var(--sand);color:var(--ink)}'
		. '.nlcpj a.nlcpj-card>span{font-size:13px;color:var(--ink2)}.nlcpj .nlcpj-n{direction:ltr;unicode-bidi:isolate;font-variant-numeric:tabular-nums}'
		. 'html body .nlcpj a.nlcpj-all{justify-self:start;font:700 14.5px/1.3 Assistant,sans-serif;color:var(--sea)!important;text-decoration:none!important}'
		. 'html body .nlcpj p.nlcpj-src{font-size:12.5px!important;color:var(--ink2)!important}'
		. '</style>';
}, 30 );
