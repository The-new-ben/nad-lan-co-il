<?php
/**
 * nadlan-config · the /projects/ hub in English, Russian and French (1.72.514, Ben 25.10.2026: "highest level ... they
 * strengthen each other ... English, Russian, French ... per language the nuances of what people search ... tools,
 * infographics, something nobody can copy").
 *
 * /en/projects/, /ru/projects/ and /fr/projects/ are WordPress pages under the language roots whose content is
 * [nadlan_projects_hub lang="xx"]. They are the same page as /projects/ in another language: one hreflang group with the
 * Hebrew archive (x-default /projects/), kept apart from the buyer-guide group /xx/new-projects/. Copy per language lives in
 * data/hub-lang/{en,ru,fr}.json (written natively for that language's searchers, docs/research/2026-10-25-projects-hub/
 * lang-dna-*.md), names in data/hub-lang/names.json; the numbers come from the same files as the Hebrew hub.
 * Loaded by inc/projects-hub.php only when this file exists (release rule of 25.10: no new required file).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_phl_dict' ) ) {
	function nadlan_phl_dict( $lang ) {
		return in_array( $lang, array( 'en', 'ru', 'fr' ), true ) ? nadlan_ph_json( 'data/hub-lang/' . $lang . '.json' ) : array();
	}
	function nadlan_phl_names() { return nadlan_ph_json( 'data/hub-lang/names.json' ); }
	function nadlan_phl_t( $s, $v = array() ) { foreach ( (array) $v as $k => $x ) { $s = str_replace( '{' . $k . '}', (string) $x, (string) $s ); } return (string) $s; }
	/** 3215000 -> "3,215,000" (en) or "3 215 000" (ru, fr; narrow no-break space) */
	function nadlan_phl_num( $n, $d ) { return number_format( (float) $n, 0, '.', ',' === ( $d['num_sep'] ?? ',' ) ? ',' : "\u{202F}" ); }
	/** 3.4844 -> "3,4844" where the language writes a decimal comma (ru, fr) */
	function nadlan_phl_dec( $n, $d ) { return str_replace( '.', (string) ( $d['dec'] ?? '.' ), (string) $n ); }
	function nadlan_phl_fx( $d ) {
		$fx = nadlan_ph_json( 'assets/instruments/data/boi-fx.json' ); $c = $d['cur'] ?? 'USD';
		return array( (float) ( $fx['fx'][ $c ]['rate'] ?? 0 ), (string) ( $fx['fx'][ $c ]['date'] ?? '' ) );
	}
	function nadlan_phl_date( $ymd, $d ) { $t = strtotime( (string) $ymd ); return $t ? date( 'j.n.Y', $t ) : ''; }
	/** "₪3,215,000 ≈ $1,040,000" with the foreign amount rounded to the thousand */
	function nadlan_phl_money( $nis, $d, $small = true ) {
		list( $r ) = nadlan_phl_fx( $d );
		$s = esc_html( '₪' . nadlan_phl_num( $nis, $d ) );
		if ( $r > 0 ) {
			$f = nadlan_phl_num( round( $nis / $r, -3 ), $d );
			$f = ! empty( $d['cur_after'] ) ? $f . "\u{00A0}" . $d['cur_sign'] : $d['cur_sign'] . $f;
			$s .= $small ? '<small>≈ ' . esc_html( $f ) . '</small>' : ' (≈ ' . esc_html( $f ) . ')';
		}
		return $s;
	}
	function nadlan_phl_city( $he, $d ) {
		$n = nadlan_phl_names(); $i = (int) ( $d['names_i'] ?? 0 ); $k = trim( (string) $he );
		foreach ( array( $k, str_replace( '-', ' ', $k ), str_replace( ' ', '-', $k ) ) as $x ) { if ( isset( $n['cities'][ $x ][ $i ] ) ) { return $n['cities'][ $x ][ $i ]; } }
		return '';
	}
	function nadlan_phl_dev( $he ) {
		$n = nadlan_phl_names(); $k = trim( (string) $he );
		if ( isset( $n['developers'][ $k ] ) ) { return $n['developers'][ $k ]; }
		return preg_match( '/^[A-Za-z0-9 .&\'-]+$/', $k ) ? $k : '';
	}
	/** The Latin part of a project name ("VOGUE גינדי שדה דב" -> "VOGUE"), '' when there is none */
	/** "ZOHI Sde Dov Tel Aviv apartments for sale - prices, plans" -> "ZOHI Sde Dov Tel Aviv" (the card name) */
	function nadlan_phl_short( $t ) {
		$s = preg_split( '/\s+(?:-|\x{2013}|\||:)\s+|:\s|\s+(?:long-term|apartments?|квартир[а-я]*|appartements?|аренда|location|à vendre)(?![\w])/iu', (string) $t, 2 );
		$s = trim( (string) ( $s[0] ?? $t ), " ,-" );
		return mb_strlen( $s ) >= 3 ? $s : (string) $t;
	}
	function nadlan_phl_pname( $name ) {
		$s = trim( preg_replace( '/\s+/u', ' ', preg_replace( '/[\x{0590}-\x{05FF}״׳"]+/u', ' ', (string) $name ) ), " -|,()" );
		return preg_match( '/[A-Za-z]{2,}/', $s ) ? $s : '';
	}
}

/* ------------------------------------------------------------------------------------------------ sections */
if ( ! function_exists( 'nadlan_phl_featured_html' ) ) {
	function nadlan_phl_featured_html( $d, $lang ) {
		global $wpdb;
		$ids = $wpdb->get_col( $wpdb->prepare( "SELECT ID FROM {$wpdb->posts} WHERE post_type='nadlan_project' AND post_status='publish' AND post_name LIKE %s AND post_name NOT LIKE %s AND post_name NOT LIKE %s ORDER BY menu_order ASC, post_date DESC", '%-' . $wpdb->esc_like( $lang ), '%toha2%', '%the-park%' ) );
		if ( ! $ids ) { return ''; }
		$cards = ''; $items = array();
		foreach ( $ids as $i => $id ) {
			$t = nadlan_phl_short( wp_strip_all_tags( get_the_title( $id ) ) ); $u = get_permalink( $id );
			$img = get_the_post_thumbnail_url( $id, 'medium_large' );
			if ( ! $img ) { $he = get_page_by_path( preg_replace( '/-(?:en|ru|fr|ar)$/', '', (string) get_post_field( 'post_name', $id ) ), OBJECT, 'nadlan_project' ); $img = $he ? get_the_post_thumbnail_url( $he->ID, 'medium_large' ) : ''; } /* the Hebrew project's picture */
			$city = nadlan_phl_city( (string) get_post_meta( $id, 'city', true ), $d ); // the city in the page's language, or nothing
			$cards .= '<a class="nlphl-card" href="' . esc_url( $u ) . '">' . ( $img ? '<img src="' . esc_url( $img ) . '" alt="' . esc_attr( $t ) . '" loading="lazy" width="640" height="400">' : '' )
				. '<h3 class="nlphl-card__t">' . esc_html( $t ) . '</h3>' . ( $city ? '<small>' . esc_html( $city ) . '</small>' : '' ) . '<span>' . esc_html( $d['featured_more'] ?? '' ) . ' &rsaquo;</span></a>';
			$items[] = array( '@type' => 'ListItem', 'position' => $i + 1, 'url' => $u, 'name' => $t );
		}
		$GLOBALS['nadlan_phl_items'] = $items;
		return '<section class="nlph-sec" id="nlph-featured"><p class="nlph-kick">' . esc_html( $d['featured_kick'] ?? '' ) . '</p><h2>' . esc_html( $d['featured_h'] ?? '' ) . '</h2><p class="nlph-lede">' . esc_html( $d['featured_lede'] ?? '' ) . '</p><div class="nlphl-cards">' . $cards . '</div></section>';
	}
}

if ( ! function_exists( 'nadlan_phl_market_html' ) ) {
	function nadlan_phl_market_html( $d, $lang ) {
		$m = nadlan_ph_market(); $all = count( $m['projects'] ); $rows = array();
		foreach ( $m['projects'] as $p ) { $pn = nadlan_phl_pname( $p['name'] ?? '' ); if ( '' !== $pn ) { $p['_n'] = $pn; $rows[] = $p; } }
		if ( ! $rows ) { return ''; }
		usort( $rows, function ( $a, $b ) { $pa = (int) ( $a['price_from'] ?? 0 ); $pb = (int) ( $b['price_from'] ?? 0 ); if ( ! $pa !== ! $pb ) { return $pa ? -1 : 1; } return $pa - $pb; } );
		list( $fx, $fxd ) = nadlan_phl_fx( $d ); $tlv = 0; $count = array(); $tr = '';
		$stl = (array) ( $d['stage'] ?? array() ); $home = untrailingslashit( home_url( '/' ) );
		foreach ( $rows as $i => $p ) {
			$reg = nadlan_ph_region( $p['city'] ?? '' ); $count[ $reg ] = ( $count[ $reg ] ?? 0 ) + 1; if ( 'tlv' === $reg ) { $tlv++; }
			$name = esc_html( $p['_n'] );
			if ( ! empty( $p['url'] ) ) {
				$sib = rtrim( $p['url'], '/' ) . '-' . $lang . '/'; $sp = get_page_by_path( trim( basename( $sib ), '/' ), OBJECT, 'nadlan_project' );
				$name = '<a href="' . esc_url( $sp ? get_permalink( $sp ) : $home . $p['url'] ) . '">' . $name . '</a>';
			}
			$price = (int) ( $p['price_from'] ?? 0 );
			$pc = $price ? '<b>' . nadlan_phl_money( $price, $d ) . '</b>' : '<span class="nlph-na">' . esc_html( $d['price_ask'] ?? '' ) . '</span>';
			preg_match( '/^[\d.\s\-]+/', (string) ( $p['rooms'] ?? '' ), $rm );
			preg_match( '/\b(\d{1,2}\s*\/\s*\d{2})\b/', (string) ( $p['deal'] ?? '' ), $dl );
			$st = (string) ( $p['status'] ?? '' ); $del = (string) ( $p['delivery'] ?? '' );
			$del = preg_match( '/\d{4}|Q\d/i', $del ) ? preg_replace( '/[\x{0590}-\x{05FF}]+/u', '', $del ) : '';
			$tr .= '<tr data-reg="' . esc_attr( $reg ) . '"' . ( $i >= 20 ? ' class="nlph-more"' : '' ) . '><th scope="row">' . $name . '<small>' . esc_html( nadlan_phl_city( $p['city'] ?? '', $d ) ) . '</small></th>'
				. '<td data-l="' . esc_attr( $d['col_dev'] ?? '' ) . '">' . esc_html( nadlan_phl_dev( $p['developer'] ?? '' ) ) . '</td>'
				. '<td data-l="' . esc_attr( $d['col_rooms'] ?? '' ) . '">' . esc_html( trim( $rm[0] ?? '' ) ) . '</td>'
				. '<td data-l="' . esc_attr( $d['col_from'] ?? '' ) . '" class="nlph-p">' . $pc . '</td>'
				. '<td data-l="' . esc_attr( $d['col_terms'] ?? '' ) . '">' . esc_html( isset( $dl[1] ) ? str_replace( ' ', '', $dl[1] ) : '' ) . '</td>'
				. '<td data-l="' . esc_attr( $d['col_stage'] ?? '' ) . '">' . ( isset( $stl[ $st ] ) ? '<span class="nlph-st nlph-st--' . esc_attr( $st ) . '">' . esc_html( $stl[ $st ] ) . '</span>' : '' ) . ( $del ? '<small>' . esc_html( ( $d['delivery'] ?? '' ) . ': ' . trim( $del ) ) . '</small>' : '' ) . '</td></tr>';
		}
		$chips = '';
		foreach ( (array) ( $d['regions'] ?? array() ) as $k => $label ) {
			if ( '' !== $k && empty( $count[ $k ] ) ) { continue; }
			$chips .= '<button type="button"' . ( '' === $k ? ' class="is-on"' : '' ) . ' data-reg="' . esc_attr( $k ) . '">' . esc_html( $label ) . ' <i>' . ( '' === $k ? count( $rows ) : (int) $count[ $k ] ) . '</i></button>';
		}
		$cols = ''; foreach ( array( 'col_project', 'col_dev', 'col_rooms', 'col_from', 'col_terms', 'col_stage' ) as $c ) { $cols .= '<th scope="col">' . esc_html( $d[ $c ] ?? '' ) . '</th>'; }
		$date = nadlan_phl_date( $m['read'] ?? '', $d );
		return '<section class="nlph-sec" id="nlph-market"><p class="nlph-kick">' . esc_html( $d['market_kick'] ?? '' ) . '</p><h2>' . esc_html( $d['market_h'] ?? '' ) . '</h2>'
			. '<p class="nlph-lede">' . esc_html( nadlan_phl_t( $d['market_lede'] ?? '', array( 'n' => count( $rows ), 'tlv' => $tlv ) ) ) . '</p>'
			. '<div class="nlph-chips nlphl-chips" role="group">' . $chips . '</div>'
			. '<div class="nlph-tw"><table class="nlphl-mt"><thead><tr>' . $cols . '</tr></thead><tbody>' . $tr . '</tbody></table></div>'
			. '<button type="button" class="nlph-btn nlph-btn--ghost" id="nlphl-more">' . esc_html( nadlan_phl_t( $d['market_more'] ?? '', array( 'n' => count( $rows ) ) ) ) . '</button>'
			. '<p class="nlph-src">' . esc_html( nadlan_phl_t( $d['market_note'] ?? '', array( 'date' => $date, 'fxdate' => nadlan_phl_date( $fxd, $d ), 'fx' => nadlan_phl_dec( $fx, $d ), 'all' => $all ) ) ) . ' <a href="' . esc_url( home_url( '/projects/#nlph-market' ) ) . '">' . esc_html( nadlan_phl_t( $d['market_all'] ?? '', array( 'all' => $all ) ) ) . '</a></p></section>';
	}
}

if ( ! function_exists( 'nadlan_phl_tlv_html' ) ) {
	function nadlan_phl_tlv_html( $d, $lang ) {
		$v = nadlan_ph_value(); $t = $v['תל אביב יפו'] ?? array(); $hood = array();
		foreach ( (array) ( $t['hoods'] ?? array() ) as $h ) { $hood[ $h['n'] ] = $h; }
		$hp = function ( $name, $room ) use ( $hood ) { foreach ( $hood as $k => $h ) { if ( 0 === mb_strpos( $k, $name ) && ! empty( $h[ $room ][0] ) ) { return (int) $h[ $room ][0]; } } return 0; };
		$pick = array( 'north' => array( 'בבלי', 'הצפון החדש החלק הצפ', 'נאות אפקה א', 'הדר יוסף' ), 'centre' => array( 'לב העיר', 'גני שרונה', 'כרם התימנים' ), 'east' => array( 'נחלת יצחק', 'ביצרון', 'יד אליהו' ), 'south' => array( 'קרית שלום', 'דקר', 'נוה חן' ), 'jaffa' => array( 'צפון יפו', 'יפו ד' ) );
		$areas = array(); foreach ( nadlan_ph_market()['projects'] as $p ) { if ( 'tlv' !== nadlan_ph_region( $p['city'] ?? '' ) ) { continue; } $a = nadlan_ph_tlv_area( ( $p['neighbourhood'] ?? '' ) . ' ' . ( $p['street'] ?? '' ) ); if ( $a ) { $areas[ $a ][] = $p; } }
		$cards = '';
		foreach ( (array) ( $d['tlv_areas'] ?? array() ) as $k => $a ) {
			$med = '';
			foreach ( $pick[ $k ] ?? array() as $hn ) { $room = in_array( $hn, array( 'צפון יפו', 'יפו ד' ), true ) ? 'r3' : 'r4'; $x = $hp( $hn, $room ); if ( $x && ! empty( $d['hoods'][ $hn ] ) ) { $med .= '<li><span>' . esc_html( $d['hoods'][ $hn ] ) . '</span><b>' . esc_html( '₪' . nadlan_phl_num( $x, $d ) ) . '</b><small>' . esc_html( 'r3' === $room ? ( $d['rooms3'] ?? '' ) : ( $d['rooms4'] ?? '' ) ) . '</small></li>'; } }
			$ps = $areas[ $k ] ?? array(); $lo = 0; foreach ( $ps as $p ) { $pr = (int) ( $p['price_from'] ?? 0 ); if ( $pr ) { $lo = $lo ? min( $lo, $pr ) : $pr; } }
			$cards .= '<article class="nlph-area"><h3>' . esc_html( $a[0] ) . '</h3><p class="nlph-area__n">' . esc_html( $a[1] ) . '</p><p>' . esc_html( $a[2] ) . '</p>'
				. ( $ps && $lo ? '<p class="nlph-area__m">' . esc_html( nadlan_phl_t( $d['tlv_on_market'] ?? '', array( 'n' => count( $ps ), 'lo' => '₪' . nadlan_phl_num( $lo, $d ) ) ) ) . '</p>' : '' )
				. ( $med ? '<p class="nlph-area__k">' . esc_html( nadlan_phl_t( $d['tlv_median'] ?? '', array( 'q' => '1-3.2026' ) ) ) . '</p><ul class="nlph-area__med">' . $med . '</ul>' : '' ) . '</article>';
		}
		$stats = ''; foreach ( (array) ( $d['tlv_stats'] ?? array() ) as $s ) { $stats .= '<li><b>' . esc_html( $s[0] ) . '</b><span>' . esc_html( $s[1] ) . '</span></li>'; }
		if ( ! empty( $t['r4'] ) ) { $stats .= '<li><b>' . esc_html( '₪' . nadlan_phl_num( $t['r4'], $d ) ) . '</b><span>' . esc_html( nadlan_phl_t( $d['tlv_median'] ?? '', array( 'q' => $t['q4'] ?? '' ) ) ) . '</span></li>'; }
		$pl = ''; foreach ( (array) ( $d['plans'] ?? array() ) as $r ) { $nm = $r[3] ? '<a href="' . esc_url( home_url( $r[3] ) ) . '">' . esc_html( $r[0] ) . '</a>' : esc_html( $r[0] ); $pl .= '<tr><th scope="row">' . $nm . '</th><td data-l="' . esc_attr( $d['plans_cols'][1] ?? '' ) . '">' . esc_html( $r[1] ) . '</td><td data-l="' . esc_attr( $d['plans_cols'][2] ?? '' ) . '">' . esc_html( $r[2] ) . '</td></tr>'; }
		$pc = ''; foreach ( (array) ( $d['plans_cols'] ?? array() ) as $c ) { $pc .= '<th scope="col">' . esc_html( $c ) . '</th>'; }
		return '<section class="nlph-sec" id="nlph-tlv"><p class="nlph-kick">' . esc_html( $d['tlv_kick'] ?? '' ) . '</p><h2>' . esc_html( $d['tlv_h'] ?? '' ) . '</h2><p class="nlph-lede">' . esc_html( $d['tlv_lede'] ?? '' ) . '</p>'
			. '<ul class="nlph-stats">' . $stats . '</ul><div class="nlph-areas">' . $cards . '</div><h3>' . esc_html( $d['plans_h'] ?? '' ) . '</h3>'
			. '<div class="nlph-tw"><table class="nlph-plans"><thead><tr>' . $pc . '</tr></thead><tbody>' . $pl . '</tbody></table></div></section>';
	}
}

if ( ! function_exists( 'nadlan_phl_prices_html' ) ) {
	function nadlan_phl_prices_html( $d, $lang ) {
		$v = nadlan_ph_value(); if ( ! $v ) { return ''; }
		$mk = array(); foreach ( nadlan_ph_market()['projects'] as $p ) { $pr = (int) ( $p['price_from'] ?? 0 ); if ( ! $pr ) { continue; } $k = str_replace( '-', ' ', (string) ( $p['city'] ?? '' ) ); $mk[ $k ] = isset( $mk[ $k ] ) ? min( $mk[ $k ], $pr ) : $pr; }
		$rows = array(); $max = 0; foreach ( $v as $city => $x ) { if ( ! empty( $x['r4'] ) ) { $rows[] = array( $city, $x ); $max = max( $max, (int) $x['r4'] ); } }
		usort( $rows, function ( $a, $b ) { return (int) $b[1]['r4'] - (int) $a[1]['r4']; } );
		$bars = ''; $tr = ''; list( $fx, $fxd ) = nadlan_phl_fx( $d );
		$alias = array( 'פתח תקווה' => 'פתח תקוה', 'קריית אונו' => 'קרית אונו', 'גבעתיים' => 'גבעתים' );
		foreach ( $rows as $r ) {
			list( $city, $x ) = $r; $cn = nadlan_phl_city( $city, $d ); if ( '' === $cn ) { continue; }
			$from = $mk[ $city ] ?? ( $mk[ $alias[ $city ] ?? '' ] ?? 0 );
			$yoy = isset( $x['yoy4'] ) ? nadlan_phl_t( $x['yoy4'] < 0 ? ( $d['yoy_down'] ?? '' ) : ( $d['yoy_up'] ?? '' ), array( 'x' => nadlan_phl_dec( abs( (float) $x['yoy4'] ), $d ) ) ) : '';
			$bars .= '<li style="--w:' . round( 100 * (int) $x['r4'] / max( 1, $max ), 1 ) . '%"' . ( 'תל אביב יפו' === $city ? ' class="is-tlv"' : '' ) . '><span>' . esc_html( $cn ) . '</span><i></i><b>' . esc_html( '₪' . nadlan_phl_num( $x['r4'], $d ) ) . '</b></li>';
			$tr .= '<tr><th scope="row">' . esc_html( $cn ) . '</th><td data-l="' . esc_attr( $d['prices_cols'][1] ?? '' ) . '">' . ( ! empty( $x['r3'] ) ? esc_html( '₪' . nadlan_phl_num( $x['r3'], $d ) ) : '' ) . '</td>'
				. '<td data-l="' . esc_attr( $d['prices_cols'][2] ?? '' ) . '"><b>' . nadlan_phl_money( $x['r4'], $d ) . '</b>' . ( $yoy ? '<small>' . esc_html( $yoy ) . '</small>' : '' ) . '</td>'
				. '<td data-l="' . esc_attr( $d['prices_cols'][3] ?? '' ) . '">' . ( ! empty( $x['r5'] ) ? esc_html( '₪' . nadlan_phl_num( $x['r5'], $d ) ) : '' ) . '</td>'
				. '<td data-l="' . esc_attr( $d['prices_cols'][4] ?? '' ) . '">' . ( $from ? esc_html( '₪' . nadlan_phl_num( $from, $d ) ) : '' ) . '</td></tr>';
		}
		$pc = ''; foreach ( (array) ( $d['prices_cols'] ?? array() ) as $c ) { $pc .= '<th scope="col">' . esc_html( $c ) . '</th>'; }
		return '<section class="nlph-sec" id="nlph-prices"><p class="nlph-kick">' . esc_html( $d['prices_kick'] ?? '' ) . '</p><h2>' . esc_html( $d['prices_h'] ?? '' ) . '</h2><p class="nlph-lede">' . esc_html( $d['prices_lede'] ?? '' ) . '</p>'
			. '<ol class="nlph-bars">' . $bars . '</ol><div class="nlph-tw"><table class="nlph-pt"><thead><tr>' . $pc . '</tr></thead><tbody>' . $tr . '</tbody></table></div>'
			. '<p class="nlph-src">' . esc_html( nadlan_phl_t( $d['prices_note'] ?? '', array( 'fx' => nadlan_phl_dec( $fx, $d ), 'fxdate' => nadlan_phl_date( $fxd, $d ) ) ) ) . '</p></section>';
	}
}

if ( ! function_exists( 'nadlan_phl_abroad_html' ) ) {
	function nadlan_phl_abroad_html( $d, $lang ) {
		$pt = nadlan_ph_json( 'assets/instruments/data/ptax.json' ); $tr = $pt['tracks'] ?? array(); if ( ! $tr ) { return ''; }
		$rate = function ( $track, $x ) use ( $tr ) { foreach ( (array) ( $tr[ $track ] ?? array() ) as $b ) { if ( null === $b[0] || $x <= $b[0] ) { return (float) $b[1]; } } return 0.0; };
		$cuts = array( 0, 1978745, 2347040, 6055070, 20183565 ); $rows = '';
		foreach ( $cuts as $i => $lo ) {
			$hi = $cuts[ $i + 1 ] ?? null; $mid = null === $hi ? $lo + 1 : ( $lo + $hi ) / 2;
			$band = null === $hi ? '> ' . nadlan_phl_num( $lo, $d ) : nadlan_phl_num( $lo, $d ) . ' - ' . nadlan_phl_num( $hi, $d );
			$f = function ( $r ) use ( $d ) { return nadlan_phl_dec( rtrim( rtrim( number_format( 100 * $r, 1 ), '0' ), '.' ), $d ) . ( $d['pct'] ?? '%' ); };
			$rows .= '<tr><th scope="row">' . esc_html( $band ) . '</th><td data-l="' . esc_attr( $d['tax_cols'][1] ?? '' ) . '">' . $f( $rate( 'single', $mid ) ) . '</td><td data-l="' . esc_attr( $d['tax_cols'][2] ?? '' ) . '">' . $f( $rate( 'oleh', $mid ) ) . '</td><td data-l="' . esc_attr( $d['tax_cols'][3] ?? '' ) . '">' . $f( $rate( 'foreign', $mid ) ) . '</td></tr>';
		}
		$tc = ''; foreach ( (array) ( $d['tax_cols'] ?? array() ) as $c ) { $tc .= '<th scope="col">' . esc_html( $c ) . '</th>'; }
		$fx = nadlan_ph_json( 'assets/instruments/data/boi-fx.json' );
		$opt = ''; foreach ( (array) ( $d['calc_buyers'] ?? array() ) as $k => $l ) { $opt .= '<option value="' . esc_attr( $k ) . '"' . ( 'foreign' === $k ? ' selected' : '' ) . '>' . esc_html( $l ) . '</option>'; }
		$cur = ''; foreach ( array( 'ILS' => '₪ ILS', 'USD' => '$ USD', 'EUR' => '€ EUR', 'GBP' => '£ GBP' ) as $k => $l ) { $cur .= '<option value="' . $k . '"' . ( ( $d['cur'] ?? 'USD' ) === $k ? ' selected' : '' ) . '>' . $l . '</option>'; }
		$out = ''; foreach ( (array) ( $d['calc_rows'] ?? array() ) as $k => $l ) { $out .= '<div class="nlphl-r nlphl-r--' . esc_attr( $k ) . '"><span>' . esc_html( $l ) . '</span><b data-o="' . esc_attr( $k ) . '"></b></div>'; }
		$steps = ''; foreach ( (array) ( $d['steps'] ?? array() ) as $s ) { $steps .= '<li><b>' . esc_html( $s[0] ) . '</b><span>' . esc_html( $s[1] ) . '</span></li>'; }
		$links = ''; foreach ( (array) ( $d['abroad_links'] ?? array() ) as $l ) { $links .= '<a href="' . esc_url( home_url( $l[0] ) ) . '">' . esc_html( $l[1] ) . '</a>'; }
		$cfg = array( 'tracks' => $tr, 'fx' => array( 'USD' => (float) ( $fx['fx']['USD']['rate'] ?? 0 ), 'EUR' => (float) ( $fx['fx']['EUR']['rate'] ?? 0 ), 'GBP' => (float) ( $fx['fx']['GBP']['rate'] ?? 0 ) ), 'ltv' => array( 'single' => 0.75, 'oleh' => 0.75, 'foreign' => 0.5, 'extra' => 0.5 ), 'sep' => ',' === ( $d['num_sep'] ?? ',' ) ? ',' : "\u{202F}" );
		$tool = 'en' === $lang ? do_shortcode( '[nadlan_tool id="nrm"]' ) : '';
		return '<section class="nlph-sec" id="nlph-abroad"><p class="nlph-kick">' . esc_html( $d['abroad_kick'] ?? '' ) . '</p><h2>' . esc_html( $d['abroad_h'] ?? '' ) . '</h2><p class="nlph-lede">' . esc_html( $d['abroad_lede'] ?? '' ) . '</p>'
			. '<h3>' . esc_html( $d['tax_h'] ?? '' ) . '</h3><div class="nlph-tw"><table class="nlph-pt nlphl-tax"><thead><tr>' . $tc . '</tr></thead><tbody>' . $rows . '</tbody></table></div><p class="nlph-src">' . esc_html( $d['tax_note'] ?? '' ) . '</p>'
			. '<h3>' . esc_html( $d['calc_h'] ?? '' ) . '</h3><form class="nlphl-calc" action="#" data-cfg="' . esc_attr( wp_json_encode( $cfg ) ) . '"><div class="nlphl-in"><label>' . esc_html( $d['calc_price'] ?? '' ) . '<input type="text" inputmode="numeric" value="3500000" data-i="price"></label>'
			. '<label>' . esc_html( $d['calc_buyer'] ?? '' ) . '<select data-i="buyer">' . $opt . '</select></label><label>' . esc_html( $d['calc_cur'] ?? '' ) . '<select data-i="cur">' . $cur . '</select></label></div><div class="nlphl-out">' . $out . '</div>'
			. '<p class="nlph-src">' . esc_html( nadlan_phl_t( $d['calc_note'] ?? '', array( 'fxdate' => nadlan_phl_date( $fx['fx']['USD']['date'] ?? '', $d ) ) ) ) . '</p></form>'
			. '<h3>' . esc_html( $d['mort_h'] ?? '' ) . '</h3><p>' . esc_html( $d['mort_p'] ?? '' ) . '</p>' . $tool
			. '<h3>' . esc_html( $d['steps_h'] ?? '' ) . '</h3><ol class="nlphl-steps">' . $steps . '</ol>' . ( $links ? '<p class="nlph-area__l nlphl-links">' . $links . '</p>' : '' ) . '</section>';
	}
}

if ( ! function_exists( 'nadlan_phl_generic_html' ) ) {
	/** timeline, payments, checks, types, numbers, cities, guides, faq, sources: the same structure as the Hebrew hub, in the language */
	function nadlan_phl_generic_html( $d, $lang, $facets ) {
		$h = '';
		$li = ''; foreach ( (array) ( $d['steps_tl'] ?? array() ) as $i => $s ) { $li .= '<li><span class="nlph-tl__n">' . ( $i + 1 ) . '</span><div><h3>' . esc_html( $s[0] ) . '</h3><p class="nlph-tl__t">' . esc_html( $s[1] ) . '</p><p>' . esc_html( $s[2] ) . '</p><p class="nlph-tl__g">' . esc_html( $s[3] ) . '</p></div></li>'; }
		$h .= '<section class="nlph-sec" id="nlph-timeline"><p class="nlph-kick">' . esc_html( $d['timeline_kick'] ?? '' ) . '</p><h2>' . esc_html( $d['timeline_h'] ?? '' ) . '</h2><p class="nlph-lede">' . esc_html( $d['timeline_lede'] ?? '' ) . '</p><ol class="nlph-tl">' . $li . '</ol><p class="nlph-src">' . esc_html( $d['timeline_note'] ?? '' ) . '</p></section>';
		$pl = ''; foreach ( (array) ( $d['pay_plans'] ?? array() ) as $p ) { $seg = ''; foreach ( $p[2] as $x ) { $seg .= '<i style="flex:' . (int) $x[0] . ' 1 0px"><b>' . (int) $x[0] . '%</b><small>' . esc_html( $x[1] ) . '</small></i>'; } $pl .= '<li><p><b>' . esc_html( $p[0] ) . '</b><span>' . esc_html( $p[1] ) . '</span></p><div class="nlph-paybar">' . $seg . '</div></li>'; }
		$lk = ''; foreach ( (array) ( $d['link_parts'] ?? array() ) as $j => $x ) { $lk .= '<i class="' . array( 'a', 'b', 'c' )[ $j ] . '" style="flex:' . array( 20, 40, 40 )[ $j ] . ' 1 0px"><b>' . esc_html( $x[0] ) . '</b><small>' . esc_html( $x[1] ) . '</small></i>'; }
		$h .= '<section class="nlph-sec" id="nlph-pay"><p class="nlph-kick">' . esc_html( $d['pay_kick'] ?? '' ) . '</p><h2>' . esc_html( $d['pay_h'] ?? '' ) . '</h2><p class="nlph-lede">' . esc_html( $d['pay_lede'] ?? '' ) . '</p><ul class="nlph-pay">' . $pl . '</ul><h3>' . esc_html( $d['link_h'] ?? '' ) . '</h3><div class="nlph-link" role="img" aria-label="' . esc_attr( $d['link_aria'] ?? '' ) . '">' . $lk . '</div><p>' . esc_html( $d['link_p'] ?? '' ) . '</p><p>' . esc_html( $d['boi_p'] ?? '' ) . '</p></section>';
		$ck = ''; foreach ( (array) ( $d['checks'] ?? array() ) as $i => $c ) { $ck .= '<li><label><input type="checkbox" data-i="' . $i . '"><span><b>' . esc_html( $c[0] ) . '</b>' . esc_html( $c[1] ) . '</span></label><p class="nlph-ck__l"><a href="' . esc_url( $c[2] ) . '" target="_blank" rel="noopener">' . esc_html( $c[3] ) . '</a></p></li>'; }
		$n = count( (array) ( $d['checks'] ?? array() ) );
		$h .= '<section class="nlph-sec" id="nlph-checks"><p class="nlph-kick">' . esc_html( $d['checks_kick'] ?? '' ) . '</p><h2>' . esc_html( $d['checks_h'] ?? '' ) . '</h2><p class="nlph-lede">' . esc_html( $d['checks_lede'] ?? '' ) . '</p><p class="nlph-ck__p" aria-live="polite">' . str_replace( array( '{n}', '{t}' ), array( '<b id="nlph-ck-n">0</b>', $n ), esc_html( $d['checks_count'] ?? '' ) ) . '</p><ol class="nlph-ck">' . $ck . '</ol></section>';
		$ty = (array) ( $d['types'] ?? array() ); $th = ''; foreach ( $ty as $c ) { $th .= '<th scope="col">' . esc_html( $c[0] ) . '</th>'; }
		$tb = ''; foreach ( (array) ( $d['types_rows'] ?? array() ) as $ri => $label ) { $tb .= '<tr><th scope="row">' . esc_html( $label ) . '</th>'; foreach ( $ty as $c ) { $cell = 4 === $ri ? ( ! empty( $c[5] ) ? '<a href="' . esc_url( home_url( $c[5] ) ) . '">' . esc_html( $c[6] ) . '</a>' : '' ) : esc_html( $c[ $ri + 1 ] ); $tb .= '<td data-l="' . esc_attr( $c[0] ) . '">' . $cell . '</td>'; } $tb .= '</tr>'; }
		$h .= '<section class="nlph-sec" id="nlph-types"><p class="nlph-kick">' . esc_html( $d['types_kick'] ?? '' ) . '</p><h2>' . esc_html( $d['types_h'] ?? '' ) . '</h2><p class="nlph-lede">' . esc_html( $d['types_lede'] ?? '' ) . '</p><div class="nlph-tw"><table class="nlph-ty"><thead><tr><th scope="col"></th>' . $th . '</tr></thead><tbody>' . $tb . '</tbody></table></div></section>';
		$tl = ''; foreach ( (array) ( $d['tiles'] ?? array() ) as $t ) { $tl .= '<li><b dir="ltr">' . esc_html( $t[0] ) . '</b><span>' . esc_html( $t[1] ) . '</span><small>' . esc_html( $t[2] ) . '</small></li>'; }
		$h .= '<section class="nlph-sec" id="nlph-numbers"><p class="nlph-kick">' . esc_html( $d['numbers_kick'] ?? '' ) . '</p><h2>' . esc_html( $d['numbers_h'] ?? '' ) . '</h2><p class="nlph-lede">' . esc_html( $d['numbers_lede'] ?? '' ) . '</p><ul class="nlph-tiles">' . $tl . '</ul></section>';
		$cl = ''; foreach ( array_slice( (array) ( $facets['cities'] ?? array() ), 0, 30 ) as $c ) { $cn = nadlan_phl_city( $c['name'], $d ); if ( '' === $cn || (int) $c['n'] < 3 ) { continue; } $cl .= '<a href="' . esc_url( add_query_arg( 'city', $c['name'], home_url( '/projects/' ) ) ) . '" hreflang="he">' . esc_html( nadlan_phl_t( $d['city_link'] ?? '', array( 'city' => $cn ) ) ) . ' <i>' . (int) $c['n'] . '</i></a>'; }
		$h .= '<section class="nlph-sec" id="nlph-cities"><h2>' . esc_html( $d['cities_h'] ?? '' ) . '</h2><div class="nlph-cl">' . $cl . '</div><p class="nlph-src">' . esc_html( $d['cities_note'] ?? '' ) . '</p></section>';
		$gl = ''; foreach ( (array) ( $d['guides'] ?? array() ) as $g ) { $gl .= '<li><a href="' . esc_url( home_url( $g[0] ) ) . '"><b>' . esc_html( $g[1] ) . '</b><span>' . esc_html( $g[2] ) . '</span></a></li>'; }
		$h .= '<section class="nlph-sec" id="nlph-guides"><h2>' . esc_html( $d['guides_h'] ?? '' ) . '</h2><ul class="nlph-guides">' . $gl . '</ul></section>';
		$fq = ''; foreach ( (array) ( $d['faq'] ?? array() ) as $q ) { $fq .= '<details><summary>' . esc_html( $q[0] ) . '</summary><p>' . esc_html( $q[1] ) . '</p></details>'; }
		$h .= '<section class="nlph-sec" id="nlph-faq"><h2>' . esc_html( $d['faq_h'] ?? '' ) . '</h2><div class="nlph-faq">' . $fq . '</div></section>';
		$sl = ''; foreach ( (array) ( $d['sources'] ?? array() ) as $s ) { $sl .= '<li><a href="' . esc_url( $s[0] ) . '" target="_blank" rel="noopener">' . esc_html( $s[1] ) . '</a></li>'; }
		$h .= '<section class="nlph-sec nlph-sec--src" id="nlph-sources"><h2>' . esc_html( $d['sources_h'] ?? '' ) . '</h2><ul class="nlph-srcs">' . $sl . '</ul><p class="nlph-src">' . esc_html( nadlan_phl_t( $d['updated'] ?? '', array( 'date' => nadlan_phl_date( NADLAN_PH_UPDATED, $d ) ) ) ) . '</p></section>';
		return $h;
	}
}

if ( ! function_exists( 'nadlan_phl_render' ) ) {
	function nadlan_phl_render( $lang ) {
		$d = nadlan_phl_dict( $lang ); if ( ! $d ) { return ''; }
		$facets = function_exists( 'nadlan_dir_project_facets' ) ? nadlan_dir_project_facets() : array();
		$st = nadlan_ph_stage_counts(); $m = nadlan_ph_market();
		$lead = nadlan_phl_t( $d['lead'] ?? '', array( 'total' => nadlan_phl_num( (int) ( $facets['total'] ?? 0 ), $d ), 'cities' => (int) ( $st['cities'] ?? 0 ), 'market' => count( $m['projects'] ), 'date' => nadlan_phl_date( NADLAN_PH_UPDATED, $d ) ) );
		$jump = ''; foreach ( (array) ( $d['jump'] ?? array() ) as $k => $l ) { $jump .= '<a href="#nlph-' . esc_attr( $k ) . '">' . esc_html( $l ) . '</a>'; }
		$out = '<p class="nlph-lede nlphl-lead">' . esc_html( $lead ) . '</p><nav class="nldir-jump nlphl-jump" aria-label="' . esc_attr( $d['crumb'] ?? '' ) . '">' . $jump . '</nav>';
		foreach ( array(
			function () use ( $d, $lang ) { return nadlan_phl_featured_html( $d, $lang ); },
			function () use ( $d, $lang ) { return nadlan_phl_market_html( $d, $lang ); },
			function () use ( $d, $lang ) { return nadlan_phl_tlv_html( $d, $lang ); },
			function () use ( $d, $lang ) { return nadlan_phl_prices_html( $d, $lang ); },
			function () use ( $d, $lang ) { return nadlan_phl_abroad_html( $d, $lang ); },
			function () use ( $d, $lang, $facets ) { return nadlan_phl_generic_html( $d, $lang, $facets ); },
		) as $part ) { try { $out .= $part(); } catch ( \Throwable $e ) { continue; } }
		/* one FAQPage, the language ItemList and the breadcrumb, for search engines and AI answers */
		$faq = array(); foreach ( (array) ( $d['faq'] ?? array() ) as $q ) { $faq[] = array( '@type' => 'Question', 'name' => $q[0], 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $q[1] ) ); }
		$url = get_permalink();
		$g = array( array( '@type' => 'FAQPage', 'url' => $url, 'inLanguage' => $lang, 'mainEntity' => $faq ),
			array( '@type' => 'BreadcrumbList', 'itemListElement' => array( array( '@type' => 'ListItem', 'position' => 1, 'name' => $d['home_label'] ?? 'Home', 'item' => home_url( $d['home'] ?? '/' ) ), array( '@type' => 'ListItem', 'position' => 2, 'name' => $d['crumb'] ?? '', 'item' => $url ) ) ) );
		if ( ! empty( $GLOBALS['nadlan_phl_items'] ) ) { $g[] = array( '@type' => 'ItemList', 'name' => $d['featured_h'] ?? '', 'itemListElement' => $GLOBALS['nadlan_phl_items'] ); }
		$out .= '<script type="application/ld+json" class="nlphl-schema">' . wp_json_encode( array( '@context' => 'https://schema.org', '@graph' => $g ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>';
		return '<div class="nlph nlph--ltr" dir="' . esc_attr( $d['dir'] ?? 'ltr' ) . '" lang="' . esc_attr( $lang ) . '">' . $out . '</div>' . nadlan_ph_assets() . nadlan_phl_assets();
	}
}

if ( ! function_exists( 'nadlan_phl_assets' ) ) {
	function nadlan_phl_assets() {
		return '<style id="nlphl-css">.nlds-pagehead--inpage{direction:ltr!important;text-align:left}.nlds-pagehead--inpage .nlds-pagehead__title{font-family:"Noto Serif",Georgia,"Times New Roman",serif!important}.nlphl-jump{display:flex;gap:6px;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;margin:4px 0 16px;padding-bottom:2px}.nlphl-jump::-webkit-scrollbar{display:none}'
			. '.nlphl-jump a{flex:0 0 auto;font:500 14px/1 "IBM Plex Sans",system-ui,sans-serif;color:#14213D;text-decoration:none;border:1px solid #C9D3DC;background:#fff;border-radius:999px;padding:9px 13px}.nlphl-jump a:hover{border-color:#14213D}html{scroll-padding-top:90px}'
			. '.nlph--ltr th,.nlph--ltr td{text-align:left}.nlph--ltr .nlph-bars i{transform-origin:left}.nlph--ltr .nlph-ck__l{margin:6px 0 0 34px!important}'
			. '.nlph--ltr .nlph-paybar i{border-left:0;border-right:1px solid #fff}.nlphl-lead{margin-top:6px}'
			. '.nlphl-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin:12px 0}.nlphl-card{display:flex;flex-direction:column;gap:4px;border:1px solid var(--li);border-radius:8px;overflow:hidden;text-decoration:none;color:var(--tx);background:#fff}'
			. '.nlphl-card img{width:100%;height:150px;object-fit:cover;display:block}.nlphl-card b,.nlphl-card .nlphl-card__t{padding:0 12px;margin:6px 0 0;color:var(--ink);font-size:15.5px;line-height:1.35;font-weight:700;font-family:inherit}.nlphl-card small{padding:0 12px;color:var(--mu);font-size:13px}.nlphl-card span{padding:4px 12px 12px;color:var(--ac2);font-size:13.5px;font-weight:600}'
			. '.nlphl-mt{width:100%;border-collapse:collapse}.nlphl-mt tr.nlph-more,.nlphl-mt tr.is-off{display:none!important}.nlphl-mt.is-all tr.nlph-more{display:table-row!important}.nlphl-mt .nlph-p b{font-weight:600;color:var(--ink);white-space:nowrap}'
			. '.nlphl-calc{border:1px solid var(--li);border-radius:8px;padding:16px;background:var(--bg)}.nlphl-in{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px}.nlphl-in label{display:flex;flex-direction:column;gap:4px;font-size:13.5px;color:var(--mu)}'
			. '.nlphl-in input,.nlphl-in select{font:500 16px "IBM Plex Sans",system-ui,sans-serif;border:1px solid var(--li);border-radius:6px;padding:9px 10px;min-height:44px;background:#fff;color:var(--tx)}'
			. '.nlphl-out{display:grid;gap:6px;margin:14px 0 4px}.nlphl-r{display:flex;justify-content:space-between;gap:12px;border-bottom:1px dashed var(--li);padding:6px 0;font-size:15px}.nlphl-r b{font-variant-numeric:tabular-nums;color:var(--ink)}.nlphl-r--total{border-bottom:0;font-size:17px}.nlphl-r--total b{font-size:19px}'
			. '.nlphl-steps{display:grid;gap:8px;padding-inline-start:20px}.nlphl-steps b{display:block;color:var(--ink)}.nlphl-steps span{font-size:15px;line-height:1.6}'
			. '@media(max-width:640px){.nlphl-mt thead{display:none}.nlphl-mt tr{display:block;border:1px solid var(--li);border-radius:6px;margin:0 0 8px;padding:6px 10px}.nlphl-mt.is-all tr.nlph-more{display:block!important}.nlphl-mt th,.nlphl-mt td{display:block;border:0;padding:4px 0}'
			. '.nlphl-mt td[data-l]::before{content:attr(data-l) ": ";color:var(--mu);font-size:12.5px}.nlphl-mt td:empty{display:none}.nlph-tl{grid-template-columns:1fr}}</style>'
			. '<script id="nlphl-js">(function(){var s=document.getElementById("nlph-market"),t=s&&s.querySelector(".nlphl-mt");if(t){var reg="",more=document.getElementById("nlphl-more");function f(){[].forEach.call(t.tBodies[0].rows,function(r){r.classList.toggle("is-off",!!reg&&r.dataset.reg!==reg);});t.classList.toggle("is-all",!!reg||t.dataset.all==="1");if(more)more.hidden=!!reg||t.dataset.all==="1";}'
			. 's.querySelectorAll(".nlphl-chips button").forEach(function(b){b.addEventListener("click",function(){s.querySelectorAll(".nlphl-chips button").forEach(function(x){x.classList.toggle("is-on",x===b);});reg=b.dataset.reg;f();});});if(more)more.addEventListener("click",function(){t.dataset.all="1";f();});}'
			. 'var c=document.querySelector(".nlphl-calc");if(c){c.addEventListener("submit",function(e){e.preventDefault();});var cfg={};try{cfg=JSON.parse(c.dataset.cfg);}catch(e){}var sep=cfg.sep||",";function N(n){return Math.round(n).toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g,sep);}'
			. 'function tax(tr,p){var b=cfg.tracks[tr]||[],t=0,lo=0;for(var i=0;i<b.length;i++){var hi=b[i][0]===null?Infinity:b[i][0];if(p>lo){t+=(Math.min(p,hi)-lo)*b[i][1];}lo=hi;}return t;}'
			. 'function run(){var p=+(c.querySelector("[data-i=price]").value.replace(/[^\\d]/g,""))||0,by=c.querySelector("[data-i=buyer]").value,cu=c.querySelector("[data-i=cur]").value,r=cu==="ILS"?1:(cfg.fx[cu]||1),sg={ILS:"₪",USD:"$",EUR:"€",GBP:"£"}[cu];'
			. 'var tx=tax(by,p),ltv=p*(cfg.ltv[by]||0.5),lg=p*0.005*1.18,eq=p-ltv+tx,tot=eq+lg;function M(v){var a=sg+N(v/r);return cu==="ILS"?a:a+"  (₪"+N(v)+")";}'
			. 'var o={tax:tx,ltv:ltv,equity:eq,legal:lg,total:tot};Object.keys(o).forEach(function(k){var e=c.querySelector("[data-o="+k+"]");if(e)e.textContent=M(o[k]);});}'
			. 'c.querySelectorAll("input,select").forEach(function(e){e.addEventListener("input",run);e.addEventListener("change",run);});run();}})();</script>';
	}
}

add_shortcode( 'nadlan_projects_hub', function ( $atts ) {
	$a = shortcode_atts( array( 'lang' => 'en' ), $atts );
	$lang = sanitize_key( $a['lang'] );
	return function_exists( 'nadlan_ph_json' ) ? nadlan_phl_render( $lang ) : '';
} );

/* the language page says when its data was last updated (WebPage dateModified), as the Hebrew catalog does */
add_filter( 'wpseo_schema_webpage', function ( $data ) {
	if ( is_array( $data ) && is_page() && defined( 'NADLAN_PH_UPDATED' ) ) { $p = get_post(); if ( $p && false !== strpos( (string) $p->post_content, '[nadlan_projects_hub' ) ) { $data['dateModified'] = NADLAN_PH_UPDATED . 'T08:00:00+02:00'; } }
	return $data;
}, 20 );

/* the English page mounts the non-resident mortgage tool of the instruments engine */
add_filter( 'nadlan_nli_page_ids', function ( $ids ) {
	if ( is_page() ) { $p = get_post(); if ( $p && false !== strpos( (string) $p->post_content, '[nadlan_projects_hub lang="en"' ) ) { $ids[] = 'nrm'; } }
	return $ids;
} );

/* hreflang: /projects/ prints the same group as its language pages (inc/page-lang.php prints it on the pages, where the
 * family key "projects" resolves the Hebrew member to this archive). First page, no filter. */
add_action( 'wp_head', function () {
	if ( ! is_post_type_archive( 'nadlan_project' ) || max( (int) get_query_var( 'paged' ), (int) ( $_GET['paged'] ?? 0 ) ) > 1 || ! empty( $_GET['city'] ) || ! empty( $_GET['q'] ) || ! empty( $_GET['project_type'] ) ) { return; }
	if ( ! function_exists( 'nadlan_pglang_family' ) ) { return; }
	$fam = array( 'he' => get_post_type_archive_link( 'nadlan_project' ) );
	foreach ( array( 'en', 'fr', 'ru', 'ar' ) as $l ) { $p = get_page_by_path( $l . '/projects', OBJECT, 'page' ); if ( $p && 'publish' === $p->post_status ) { $fam[ $l ] = get_permalink( $p ); } }
	if ( count( $fam ) < 2 ) { return; }
	echo "\n<!-- projects language cluster -->\n";
	foreach ( $fam as $l => $u ) { printf( '<link rel="alternate" hreflang="%s" href="%s" />' . "\n", esc_attr( $l ), esc_url( $u ) ); }
	printf( '<link rel="alternate" hreflang="x-default" href="%s" />' . "\n", esc_url( $fam['he'] ) );
}, 3 );
