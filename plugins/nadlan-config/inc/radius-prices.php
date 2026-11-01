<?php
/**
 * nadlan-config - RADIUS PRICES (HAD-654 radius loop, 1.11.2026; Claude Design v105.5 RadiusPrices). [nadlan_radius_prices]
 * at the end of a developer project's article, before the ProjectToolkit: the price list around the project.
 *   1. The apartment deals reported to the Tax Authority within 500 m (median per m², by rooms, by year, the latest deals).
 *   2. The official median deal price in the neighbourhood, as nadlan.gov.il publishes it, with its quarter.
 *   3. The developer projects within 1.5 km, nearest first, each linking to its page.
 * Data: data/radius-prices.json (tools/deals/build_radius_prices.py + build_radius_data.py). Every number carries its period;
 * a median needs 5 deals; nothing is extrapolated; unknown values are omitted, never shown as 0. Ben (1.11): "tools, price
 * lists around, a lot of data and numbers, everything that attracts ChatGPT".
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

function nadlan_rp_data() {
	static $d = null;
	if ( null === $d ) {
		$f = dirname( __DIR__ ) . '/data/radius-prices.json';
		$d = file_exists( $f ) ? json_decode( (string) file_get_contents( $f ), true ) : array();
		if ( ! is_array( $d ) ) { $d = array(); }
	}
	return $d;
}

function nadlan_rp_name( $id ) {
	$k = trim( (string) get_post_meta( $id, 'nadlan_kit_name', true ) );
	if ( '' !== $k ) { return $k; }
	$t = trim( wp_strip_all_tags( html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ) ) );
	$t = preg_replace( '/,\s*(?:תל אביב(?:[ -]יפו)?|הרצליה)\s*$/u', '', $t );
	$p = preg_split( '/\s+[-–|]\s+/u', $t );
	return trim( (string) $p[0] );
}

function nadlan_rp_month( $m ) { // "09.2024" -> "9.2024"
	return preg_replace( '/^0/', '', (string) $m );
}

function nadlan_rp_stage( $s ) {
	$s = trim( (string) $s );
	$map = array( 'construction' => 'בבנייה', 'permits' => 'בהיתר', 'marketing' => 'בשיווק', 'planning' => 'בתכנון' );
	if ( isset( $map[ $s ] ) ) { return $map[ $s ]; }
	return ( '' !== $s && mb_strlen( $s ) <= 14 ) ? $s : '';
}

function nadlan_rp_rooms( $r ) {
	$r = (float) $r;
	if ( $r <= 0 ) { return ''; }
	if ( 1.0 === $r ) { return 'חדר אחד'; }
	return ( floor( $r ) == $r ? (int) $r : rtrim( rtrim( number_format( $r, 1 ), '0' ), '.' ) ) . ' חדרים';
}

function nadlan_rp_floor( $f ) {
	$f = trim( (string) $f );
	if ( '' === $f ) { return ''; }
	if ( 0 === mb_strpos( $f, 'קומ' ) ) { return $f; }
	if ( 0 === mb_strpos( $f, 'קרקע' ) ) { return 'קומת קרקע'; }
	return 'קומה ' . $f;
}

function nadlan_rp_km( $a, $b ) {
	$la1 = deg2rad( $a[0] ); $la2 = deg2rad( $b[0] ); $dl = deg2rad( $b[1] - $a[1] );
	$h = pow( sin( ( $la2 - $la1 ) / 2 ), 2 ) + cos( $la1 ) * cos( $la2 ) * pow( sin( $dl / 2 ), 2 );
	return 2 * 6371000 * asin( min( 1, sqrt( $h ) ) );
}

function nadlan_rp_around( $id ) {
	$lat = (float) get_post_meta( $id, 'lat', true ); $lng = (float) get_post_meta( $id, 'lng', true );
	if ( ! $lat || ! $lng ) { return array(); }
	$ids = get_posts( array( 'post_type' => 'nadlan_project', 'post_status' => 'publish', 'posts_per_page' => 1500, 'fields' => 'ids', 'no_found_rows' => true ) );
	update_meta_cache( 'post', $ids ); // one query for every project's coordinates, not one per project
	$skip = (array) apply_filters( 'nadlan_cpj_not_homes', array( 'toha2-tel-aviv', 'the-park-bnei-brak', 'shikun-binui-sde-dov', 'migdalei-hayam-sde-dov', 'aurelia', 'hamedina' ) );
	$out = array();
	foreach ( $ids as $o ) {
		if ( (int) $o === (int) $id ) { continue; }
		$slug = (string) get_post_field( 'post_name', $o );
		if ( preg_match( '/-(en|fr|ru|ar)$/', $slug ) || in_array( $slug, $skip, true ) || 'urban_renewal' === (string) get_post_meta( $o, 'source', true ) ) { continue; }
		$a = (float) get_post_meta( $o, 'lat', true ); $b = (float) get_post_meta( $o, 'lng', true );
		if ( ! $a || ! $b ) { continue; }
		$m = nadlan_rp_km( array( $lat, $lng ), array( $a, $b ) );
		if ( $m > 1500 ) { continue; }
		$out[] = array( 'id' => $o, 'm' => $m );
	}
	usort( $out, function ( $x, $y ) { return $x['m'] <=> $y['m']; } );
	return array_slice( $out, 0, 6 );
}

add_shortcode( 'nadlan_radius_prices', function ( $atts ) {
	$a  = shortcode_atts( array( 'id' => 0 ), $atts );
	$id = (int) $a['id'] ? (int) $a['id'] : (int) get_the_ID();
	if ( ! $id ) { return ''; }
	$f  = dirname( __DIR__ ) . '/data/radius-prices.json';
	$ck = 'nlrp_' . $id . '_' . ( file_exists( $f ) ? filemtime( $f ) : 0 ) . '_v2';
	$c  = get_transient( $ck );
	if ( is_string( $c ) ) { return $c; }
	$d  = nadlan_rp_data();
	$p  = $d['projects'][ (string) $id ] ?? null;
	$n  = (int) ( $p['n'] ?? 0 );
	$of = $p['official'] ?? null;
	if ( ! $p || ( $n < 5 && ! $of ) ) { set_transient( $ck, '', 12 * HOUR_IN_SECONDS ); return ''; }
	$name = nadlan_rp_name( $id );
	$num  = function ( $v ) { return '<span class="nlrp-n">' . number_format( (int) $v ) . '</span>'; };
	$abt  = function ( $v ) use ( $num ) { return 'כ־' . $num( round( (int) $v / 100 ) * 100 ); };
	$qw   = array( 1 => 'הראשון', 2 => 'השני', 3 => 'השלישי', 4 => 'הרביעי' );
	$h  = '<section class="nlrp" id="nlrp" dir="rtl" aria-labelledby="nlrp-h">';
	$h .= '<p class="nlrp-k">' . esc_html( $name ) . ' · מחירים מסביב</p>';
	$h .= '<h2 class="nlrp-h2" id="nlrp-h">מחירי הדירות סביב ' . esc_html( $name ) . '</h2>';
	$h .= '<p class="nlrp-in">' . ( $n >= 5 ? 'העסקאות שדווחו לרשות המסים ברדיוס 500 מטר מהפרויקט' . ( $of ? ', והמחיר הרשמי בשכונה.' : '.' ) : 'המחיר הרשמי בשכונה, לפי רשות המסים.' ) . '</p>';
	$h .= '<ul class="nlrp-sum">';
	if ( $n >= 5 && ! empty( $p['ppsqm'] ) ) {
		$h .= '<li><b>' . $abt( $p['ppsqm'] ) . ' ₪ למ״ר</b><span>חציון ' . $num( $n ) . ' עסקאות דירה ברדיוס 500 מטר, ' . esc_html( nadlan_rp_month( $p['first_deal'] ?? '' ) ) . ' עד ' . esc_html( nadlan_rp_month( $p['last_deal'] ?? '' ) ) . '</span></li>';
	}
	if ( $of && ! empty( $of['all']['ils'] ) ) {
		$q = (int) $of['all']['q'];
		$h .= '<li><b>' . $num( $of['all']['ils'] ) . ' ₪</b><span>המחיר החציוני הרשמי לדירה ' . ( ! empty( $of['near'] ) ? 'בשכונה הסמוכה, ' . esc_html( $of['name'] ) : 'ב' . esc_html( 0 === mb_strpos( (string) $of['name'], 'ה' ) ? mb_substr( (string) $of['name'], 1 ) : (string) $of['name'] ) ) . ', ברבעון ' . esc_html( $qw[ $q ] ?? '' ) . ' של ' . (int) $of['all']['y'] . '</span></li>';
	}
	$top = null;
	foreach ( (array) ( $p['rooms'] ?? array() ) as $k => $r ) {
		if ( ! empty( $r['ppsqm'] ) && ( ! $top || $r['n'] > $top[1]['n'] ) ) { $top = array( $k, $r ); }
	}
	if ( $top ) {
		$h .= '<li><b>' . $abt( $top[1]['ppsqm'] ) . ' ₪ למ״ר</b><span>חציון דירות ' . ( '5' === (string) $top[0] ? '5 חדרים ומעלה' : (int) $top[0] . ' חדרים' ) . ' ברדיוס, ' . $num( $top[1]['n'] ) . ' עסקאות</span></li>';
	}
	$h .= '</ul>';
	if ( $n >= 5 ) {
		$h .= '<div class="nlrp-part"><h3 class="nlrp-h3">לפי מספר חדרים</h3><div class="nlrp-grid" role="table" aria-label="חציון המחיר למ״ר לפי מספר חדרים">';
		$h .= '<div class="nlrp-th" role="row"><span role="columnheader">חדרים</span><span role="columnheader">חציון למ״ר</span><span role="columnheader">עסקאות</span></div>';
		foreach ( array( '2' => '2', '3' => '3', '4' => '4', '5' => '5 ומעלה' ) as $k => $lab ) {
			$r = $p['rooms'][ $k ] ?? array( 'n' => 0 );
			if ( empty( $r['n'] ) ) { continue; }
			$h .= '<div class="nlrp-tr" role="row"><span role="cell">' . esc_html( $lab ) . '</span><span role="cell">' . ( ! empty( $r['ppsqm'] ) ? $num( $r['ppsqm'] ) . ' ₪' : '<i>פחות מ־5 עסקאות</i>' ) . '</span><span role="cell">' . $num( $r['n'] ) . '</span></div>';
		}
		$h .= '</div></div>';
		$ys = array_filter( (array) ( $p['years'] ?? array() ), function ( $y ) { return ! empty( $y['ppsqm'] ); } );
		if ( count( $ys ) >= 2 ) {
			$mx = max( array_map( function ( $y ) { return (int) $y['ppsqm']; }, $ys ) );
			$al = array();
			$bars = '';
			foreach ( $ys as $yr => $y ) {
				$al[] = (int) $yr . ' כ־' . number_format( round( $y['ppsqm'] / 100 ) * 100 ) . ' ₪';
				$bars .= '<div class="nlrp-bar"><b>' . number_format( $y['ppsqm'] / 1000, 1 ) . '</b><i style="height:' . max( 8, (int) round( 104 * $y['ppsqm'] / $mx ) ) . 'px"></i><span>' . (int) $yr . '</span><span class="nlrp-n">' . (int) $y['n'] . '</span></div>';
			}
			$h .= '<div class="nlrp-part"><h3 class="nlrp-h3">המחיר למ״ר ברדיוס, לפי שנה</h3><div class="nlrp-bars" role="img" aria-label="' . esc_attr( 'חציון המחיר למ״ר ברדיוס 500 מטר: ' . implode( ', ', $al ) ) . '">' . $bars . '</div><p class="nlrp-mut">באלפי ₪ למ״ר; מתחת לכל שנה, מספר העסקאות.</p></div>';
		}
		$ls = array_slice( (array) ( $p['latest'] ?? array() ), 0, 6 );
		if ( $ls ) {
			$h .= '<div class="nlrp-part"><h3 class="nlrp-h3">העסקאות האחרונות ברדיוס</h3>';
			foreach ( $ls as $x ) {
				$bits = array_filter( array( nadlan_rp_rooms( $x['rooms'] ?? 0 ), ! empty( $x['sqm'] ) ? number_format( (int) $x['sqm'] ) . ' מ״ר' : '', nadlan_rp_floor( $x['floor'] ?? '' ), nadlan_rp_month( $x['month'] ?? '' ) ) );
				$h .= '<div class="nlrp-deal"><b>' . esc_html( $x['street'] ?? '' ) . ( ! empty( $x['new'] ) ? ' <span class="nlrp-chip">דירה חדשה</span>' : '' ) . '</b><span class="nlrp-p">' . $num( $x['price'] ) . ' ₪</span>'
					. '<span class="nlrp-d">' . esc_html( implode( ' · ', $bits ) ) . '</span><span class="nlrp-d">' . $num( $x['ppsqm'] ) . ' ₪ למ״ר</span></div>';
			}
			$h .= '</div>';
		}
	}
	$ar = nadlan_rp_around( $id );
	if ( $ar ) {
		$h .= '<div class="nlrp-part"><h3 class="nlrp-h3">הפרויקטים מסביב</h3><div class="nlrp-pjs">';
		foreach ( $ar as $o ) {
			$dev = trim( (string) get_post_meta( $o['id'], 'developer_name', true ) );
			$st  = nadlan_rp_stage( get_post_meta( $o['id'], 'project_status', true ) );
			$u   = (int) get_post_meta( $o['id'], 'num_units', true ); $fl = (int) get_post_meta( $o['id'], 'num_floors', true );
			$bits = array_filter( array( '' !== $dev ? esc_html( $dev ) : '', '' !== $st ? '<span class="nlrp-chip">' . esc_html( $st ) . '</span>' : '', $fl > 0 ? $num( $fl ) . ' קומות' : '', $u > 0 ? $num( $u ) . ' דירות' : '' ) );
			$dist = $o['m'] < 950 ? $num( round( $o['m'] / 10 ) * 10 ) . ' מ׳' : '<span class="nlrp-n">' . number_format( $o['m'] / 1000, 1 ) . '</span> ק״מ';
			$h .= '<a class="nlrp-pj" href="' . esc_url( get_permalink( $o['id'] ) ) . '"><b>' . esc_html( nadlan_rp_name( $o['id'] ) ) . '</b><span class="nlrp-row"><span>' . implode( ' · ', $bits ) . '</span><span>' . $dist . '</span></span></a>';
		}
		$h .= '</div></div>';
	}
	$ver = $of && preg_match( '/^(\d{2})-(\d{2})-(\d{4})$/', (string) ( $of['version'] ?? '' ), $mm ) ? (int) $mm[1] . '.' . (int) $mm[2] . '.' . $mm[3] : '';
	$h .= '<p class="nlrp-src">מקורות: עסקאות שדווחו לרשות המסים כפי שפורסמו באתר nadlan.gov.il, ומאגר הכתובות של עיריית תל אביב-יפו. המחיר למ״ר הוא מחיר העסקה חלקי השטח הרשום. חציון מוצג רק כשיש 5 עסקאות לפחות.'
		. ( '' !== $ver ? ' המחיר הרשמי בשכונה: קובץ השכונה של רשות המסים מ־' . esc_html( $ver ) . '.' : '' ) . '</p>';
	$h .= '</section>';
	set_transient( $ck, $h, 12 * HOUR_IN_SECONDS );
	return $h;
} );

add_action( 'wp_head', function () {
	if ( ! is_singular() ) { return; }
	$p = get_post();
	if ( ! $p || false === strpos( (string) $p->post_content, '[nadlan_radius_prices' ) ) { return; }
	$t = 'color-mix(in srgb,var(--sa-sea,#2f6f86) 9%,#fff)';
	echo '<style id="nadlan-rp-css">'
		. '.nlrp{--ink:#14212b;--ink2:#3b4753;--line:#e3e1da;--sea:#2f6f86;font-family:Assistant,Heebo,"Segoe UI",Arial,sans-serif;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:22px;padding:18px;margin:28px 0;display:grid;gap:14px;max-width:900px}'
		. 'html body .nlrp p{margin:0!important}html body .nlrp p.nlrp-k{font:700 12.5px/1.3 Assistant,Heebo,sans-serif!important;color:var(--sea)!important}'
		. 'html body .nlrp h2.nlrp-h2{margin:0!important;padding:0!important;border:0!important;font:600 clamp(21px,4.6vw,26px)/1.25 "Noto Serif Hebrew","Frank Ruhl Libre",Georgia,serif!important;color:var(--ink)!important;text-align:start!important;text-wrap:balance}'
		. 'html body .nlrp h2.nlrp-h2::before,html body .nlrp h2.nlrp-h2::after,html body .nlrp h3.nlrp-h3::before,html body .nlrp h3.nlrp-h3::after{content:none!important;display:none!important}'
		. 'html body .nlrp h3.nlrp-h3{margin:0!important;padding:0!important;border:0!important;font:600 17px/1.3 "Noto Serif Hebrew",Georgia,serif!important;color:var(--ink)!important}'
		. 'html body .nlrp p.nlrp-in{font-size:15px!important;line-height:1.6!important;color:var(--ink2)!important}'
		. '.nlrp .nlrp-n{font-family:"IBM Plex Mono",ui-monospace,monospace;direction:ltr;unicode-bidi:isolate;font-variant-numeric:tabular-nums}'
		. 'html body .nlrp ul.nlrp-sum{list-style:none!important;margin:0!important;padding:0!important;display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}'
		. 'html body .nlrp ul.nlrp-sum li{display:grid;gap:3px;margin:0!important;padding:11px 13px!important;border-radius:14px;background:' . $t . '}html body .nlrp ul.nlrp-sum li::before{content:none!important}'
		. '.nlrp .nlrp-sum b{font:600 21px/1.2 "Noto Serif Hebrew",Georgia,serif;color:var(--ink)}.nlrp .nlrp-sum span{font-size:13px;line-height:1.45;color:var(--ink2)}'
		. '.nlrp .nlrp-part{display:grid;gap:8px;border-top:1px solid var(--line);padding-top:12px}'
		. '.nlrp .nlrp-grid{display:grid;font-size:14.5px}.nlrp .nlrp-th,.nlrp .nlrp-tr{display:grid;grid-template-columns:1fr 1.4fr .7fr;gap:8px;padding:7px 0;border-bottom:1px solid var(--line)}'
		. '.nlrp .nlrp-th{font:700 12px/1.3 Assistant,sans-serif;color:var(--ink2)}.nlrp .nlrp-tr i{font-style:normal;font-size:13px;color:var(--ink2)}'
		. '.nlrp .nlrp-bars{direction:ltr;display:grid;grid-auto-flow:column;grid-auto-columns:1fr;gap:8px;align-items:end;min-height:150px;max-width:520px}'
		. '.nlrp .nlrp-bar{display:grid;gap:4px;justify-items:center;align-self:end}.nlrp .nlrp-bar i{display:block;width:100%;border-radius:8px 8px 3px 3px;background:var(--sea)}'
		. '.nlrp .nlrp-bar b{font:500 11.5px/1 "IBM Plex Mono",ui-monospace,monospace;color:var(--ink)}.nlrp .nlrp-bar span{font-size:12px;color:var(--ink2)}'
		. 'html body .nlrp p.nlrp-mut{font-size:12.5px!important;color:var(--ink2)!important}'
		. '.nlrp .nlrp-deal{display:grid;grid-template-columns:1fr auto;gap:2px 10px;padding:9px 0;border-bottom:1px solid var(--line)}'
		. '.nlrp .nlrp-deal b{font:600 15px/1.3 "Noto Serif Hebrew",Georgia,serif}.nlrp .nlrp-p{font:500 15px/1.3 "IBM Plex Mono",ui-monospace,monospace;text-align:left}.nlrp .nlrp-d{font-size:13px;color:var(--ink2)}'
		. '.nlrp .nlrp-chip{display:inline-block;font:700 11.5px/1.3 Assistant,sans-serif;padding:2px 8px;border-radius:999px;background:' . $t . ';color:var(--ink)}'
		. '.nlrp .nlrp-pjs{display:grid;gap:8px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}'
		. 'html body .nlrp a.nlrp-pj{display:grid;gap:4px;padding:11px 13px;border:1px solid var(--line);border-radius:14px;background:#fff;text-decoration:none!important;color:var(--ink)!important}html body .nlrp a.nlrp-pj:hover{border-color:var(--sea)}'
		. '.nlrp .nlrp-pj b{font:600 15.5px/1.3 "Noto Serif Hebrew",Georgia,serif}.nlrp .nlrp-row{display:flex;justify-content:space-between;gap:8px;font-size:13px;color:var(--ink2)}.nlrp .nlrp-row>span:last-child{white-space:nowrap}'
		. 'html body .nlrp p.nlrp-src{font-size:12.5px!important;line-height:1.5!important;color:var(--ink2)!important}'
		. '</style>';
}, 30 );
