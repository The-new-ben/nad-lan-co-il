<?php
/**
 * nadlan-config - THE TRANSIT MAP (HAD-816, Ben 23.11.2026): light rail, Metro and Israel Railways in Gush Dan, with the
 * site's new projects and the walking minutes from each project to its nearest station.
 *
 * Two addresses, one module: /transit/ (Hebrew) and /en/transit/ (English). The address lives in the option nltr_path
 * (default 'transit'); setting it to '' takes both pages down without a release. No menu, no sitemap entry, no noindex,
 * no block on any other page: project pages are linked FROM the map, never the other way round in this version.
 *
 * Data: assets/transit/transit-data.json, built by scripts/had816/build_transit_data.py from official open data only
 * (Ministry of Transport on data.gov.il, the national GTFS of 22.11.2026, Tel Aviv-Yafo municipal GIS). The site's
 * projects come from assets/deals/projects.json (the same points the deals map shows). No opening dates are shown:
 * none could be read from an official source on 23.11.2026. A line's state is a word (פועל / בבנייה / מתוכנן).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nltr_path' ) ) {
	function nltr_path() {
		$p = trim( (string) get_option( 'nltr_path', 'transit' ), '/' );
		return preg_match( '#^[a-z0-9][a-z0-9-]{1,40}$#', $p ) ? $p : '';
	}
}

add_action( 'init', function () {
	$p = nltr_path();
	if ( '' === $p ) { return; }
	add_rewrite_rule( '^' . preg_quote( $p, '#' ) . '/?$', 'index.php?nltr_page=he', 'top' );
	add_rewrite_rule( '^en/' . preg_quote( $p, '#' ) . '/?$', 'index.php?nltr_page=en', 'top' );
	if ( get_option( 'nltr_rewrite_for' ) !== $p ) { update_option( 'nltr_rewrite_for', $p, false ); flush_rewrite_rules( false ); }
} );
add_filter( 'query_vars', function ( $v ) { $v[] = 'nltr_page'; return $v; } );
add_action( 'template_redirect', function () {
	$l = get_query_var( 'nltr_page' );
	if ( ! $l || '' === nltr_path() ) { return; }
	nltr_render( 'en' === $l ? 'en' : 'he' );
	exit;
} );

if ( ! function_exists( 'nltr_dir' ) ) {
	function nltr_dir() { return dirname( __DIR__ ) . '/assets/'; }
	function nltr_url( $f ) { return plugins_url( 'assets/' . $f, dirname( __DIR__ ) . '/nadlan-config.php' ); }
	function nltr_self( $lang ) { return home_url( ( 'en' === $lang ? '/en/' : '/' ) . nltr_path() . '/' ); }
}

if ( ! function_exists( 'nltr_data' ) ) {
	/** The transit data and the projects, read once per request. */
	function nltr_data() {
		static $d = null;
		if ( null !== $d ) { return $d; }
		$t = json_decode( (string) @file_get_contents( nltr_dir() . 'transit/transit-data.json' ), true ); // phpcs:ignore
		$p = json_decode( (string) @file_get_contents( nltr_dir() . 'deals/projects.json' ), true ); // phpcs:ignore
		$d = array( 't' => is_array( $t ) ? $t : array( 'meta' => array(), 'lines' => array(), 'stations' => array() ), 'p' => is_array( $p ) ? $p : array() );
		return $d;
	}
	/** Metres between two [lon, lat] points (equirectangular, fine at city scale). */
	function nltr_m( $a, $b ) {
		$k = cos( deg2rad( ( $a[1] + $b[1] ) / 2 ) );
		return sqrt( pow( ( $a[0] - $b[0] ) * 111320 * $k, 2 ) + pow( ( $a[1] - $b[1] ) * 110540, 2 ) );
	}
	/** Walking minutes: straight-line metres x 1.3 for the street grid, at 80 metres a minute. An estimate, and the page says so. */
	function nltr_walk( $m ) { return max( 1, (int) round( $m * 1.3 / 80 ) ); }
}

if ( ! function_exists( 'nltr_words' ) ) {
	function nltr_words( $lang ) {
		$he = array(
			'title' => 'מפת הרכבת הקלה והמטרו בגוש דן 2026: תחנות, קווים ופרויקטים ליד התחנה',
			'h1' => 'מפת הרכבת הקלה והמטרו בגוש דן: התחנות, הקווים והפרויקטים החדשים ליד כל תחנה',
			'crumb' => 'מפת הרכבת הקלה והמטרו', 'home' => 'דף הבית',
			'open' => 'פועל', 'build' => 'בבנייה', 'plan' => 'מתוכנן',
		);
		$en = array(
			'title' => 'Tel Aviv light rail and metro map 2026: stations, lines and new projects near each station',
			'h1' => 'Tel Aviv light rail and metro map: the stations, the lines and the new projects near each station',
			'crumb' => 'Light rail and metro map', 'home' => 'Home',
			'open' => 'running', 'build' => 'under construction', 'plan' => 'planned',
		);
		return 'en' === $lang ? $en : $he;
	}
}

if ( ! function_exists( 'nltr_projects' ) ) {
	/** The catalogue points for one language: never a private review page (sandbox); the Hebrew page shows the Hebrew project
	    pages, the English page the English twin of a project where one exists (/projects/<slug>-en/), else the Hebrew page. */
	function nltr_projects( $lang ) {
		$D = nltr_data(); $base = array(); $en = array();
		foreach ( $D['p'] as $p ) {
			if ( ! is_array( $p ) || count( $p ) < 4 || false !== strpos( (string) $p[3], 'sandbox' ) ) { continue; }
			if ( preg_match( '#^(.*)-(en|fr|ru|ar)/$#', (string) $p[3], $m ) ) { if ( 'en' === $m[2] ) { $en[ $m[1] . '/' ] = $p; } continue; }
			$base[ (string) $p[3] ] = $p;
		}
		/* a point shared by 3 or more projects is a city centre placed for lack of an address, not the project: left out */
		$cnt = array();
		foreach ( $base as $p ) { $k = round( $p[0], 4 ) . ',' . round( $p[1], 4 ); $cnt[ $k ] = isset( $cnt[ $k ] ) ? $cnt[ $k ] + 1 : 1; }
		foreach ( $base as $u => $p ) { if ( $cnt[ round( $p[0], 4 ) . ',' . round( $p[1], 4 ) ] >= 3 ) { unset( $base[ $u ] ); } }
		if ( 'en' === $lang ) { foreach ( $en as $k => $p ) { if ( isset( $base[ $k ] ) ) { $base[ $k ] = $p; } } }
		return array_values( $base );
	}
}

if ( ! function_exists( 'nltr_facts' ) ) {
	/** Everything the server prints: counts per line, the station lists and the projects near stations (Gush Dan). */
	function nltr_facts( $lang ) {
		$D = nltr_data();
		$lines = array(); $by = array();
		foreach ( $D['t']['lines'] as $l ) { $lines[ $l['id'] ] = $l; }
		foreach ( $D['t']['stations'] as $s ) { $by[ $s['line'] ][] = $s; }
		$near = array();
		$cands = array_values( array_filter( $D['t']['stations'], function ( $s ) { return 'red-ext' !== $s['line']; } ) );
		foreach ( nltr_projects( $lang ) as $p ) {
			$pt = array( (float) $p[0], (float) $p[1] );
			if ( $pt[1] < 31.85 || $pt[1] > 32.25 || $pt[0] < 34.70 || $pt[0] > 35.00 ) { continue; } // Gush Dan
			$best = null;
			foreach ( $cands as $s ) {
				if ( 'rail' === $s['kind'] && 'open' !== $s['status'] ) { continue; }
				$m = nltr_m( $pt, $s['p'] );
				if ( null === $best || $m < $best[0] ) { $best = array( $m, $s ); }
			}
			if ( $best && nltr_walk( $best[0] ) <= 10 ) {
				$near[] = array( 'name' => (string) $p[2], 'url' => (string) $p[3], 'min' => nltr_walk( $best[0] ), 's' => $best[1] );
			}
		}
		usort( $near, function ( $a, $b ) { return $a['min'] - $b['min'] ?: strcmp( $a['name'], $b['name'] ); } );
		return array( 'lines' => $lines, 'by' => $by, 'near' => $near, 'meta' => $D['t']['meta'] );
	}
}

if ( ! function_exists( 'nltr_line_name' ) ) {
	function nltr_line_name( $l, $lang ) { return 'en' === $lang ? $l['en'] : $l['he']; }
	function nltr_st_name( $s, $lang ) { return ( 'en' === $lang && ! empty( $s['en'] ) ) ? $s['en'] : $s['he']; }
}

if ( ! function_exists( 'nltr_render' ) ) {
	function nltr_render( $lang ) {
		$v = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1';
		$W = nltr_words( $lang );
		$F = nltr_facts( $lang );
		$EN = 'en' === $lang;
		$self = nltr_self( $lang );
		$home = home_url( $EN ? '/en/' : '/' );
		$n = function ( $id ) use ( $F ) { return isset( $F['by'][ $id ] ) ? count( $F['by'][ $id ] ) : 0; };
		$rail_open = count( array_filter( isset( $F['by']['rail'] ) ? $F['by']['rail'] : array(), function ( $s ) { return 'open' === $s['status']; } ) );
		$rail_build = $n( 'rail' ) - $rail_open;
		$metro = $n( 'm1' ) + $n( 'm2' ) + $n( 'm3' );
		$near_n = count( $F['near'] );
		$answer = $EN
			? sprintf( 'Every light rail, Metro and Israel Railways station in Gush Dan on one map: the Red Line runs today with %d stations from Petah Tikva Central Station to HaKomemiyut in Bat Yam, the Purple and Green lines are under construction, and the three Metro lines M1, M2 and M3 are planned with %d stations. Pick a station to see the new projects within walking distance, or pick a project to see its nearest station on every line.', $n( 'red' ), $metro )
			: sprintf( 'כל תחנות הרכבת הקלה, המטרו ורכבת ישראל בגוש דן על מפה אחת: הקו האדום פועל היום ב־%d תחנות, מתחנה מרכזית פתח תקווה ועד הקוממיות בבת ים. הקו הסגול והקו הירוק בבנייה, ושלושת קווי המטרו M1, M2 ו־M3 מתוכננים עם %d תחנות. בחרו תחנה וראו את הפרויקטים החדשים במרחק הליכה ממנה, או בחרו פרויקט וראו את התחנה הקרובה אליו בכל קו.', $n( 'red' ), $metro );
		$desc = $EN
			? sprintf( 'Tel Aviv light rail and metro map: the Red Line (%d stations, running), the Purple and Green lines (under construction), Metro M1, M2, M3 (%d planned stations) and Israel Railways, with walking minutes from new projects to each station.', $n( 'red' ), $metro )
			: sprintf( 'מפת הרכבת הקלה והמטרו בגוש דן: הקו האדום (%d תחנות, פועל), הקו הסגול והירוק (בבנייה), המטרו M1, M2, M3 (%d תחנות מתוכננות) ורכבת ישראל, עם דקות ההליכה מהפרויקטים החדשים לכל תחנה.', $n( 'red' ), $metro );

		/* ---------- questions and answers: the questions Google showed on 23.11.2026 (serp/), answered from our own data ---------- */
		$faq = $EN ? array(
			array( 'Where can I find a map of the light rail in Gush Dan?', sprintf( 'On this page: the Red Line with its %d running stations, the Purple Line (%d stations) and the Green Line (%d stations) under construction, the Metro and Israel Railways, all on one map with the new projects around each station.', $n( 'red' ), $n( 'purple' ), $n( 'green' ) ) ),
			array( 'What is the Gush Dan Metro project?', sprintf( 'Three planned underground lines, M1, M2 and M3, with %d stations in the Ministry of Transport file: M1 %d stations, M2 %d, M3 %d. The station positions in that file date from 12.2021 and may still change.', $metro, $n( 'm1' ), $n( 'm2' ), $n( 'm3' ) ) ),
			array( 'How many stations does the Red Line have?', sprintf( '%d stations, 10 of them underground, from Petah Tikva Central Station to HaKomemiyut in Bat Yam, per the Ministry of Transport timetable of 22.11.2026.', $n( 'red' ) ) ),
			array( 'How are the walking minutes worked out?', 'From the straight-line distance between the project and the station, times 1.3 for the street grid, at about 80 metres a minute. It is an estimate; the real walk depends on crossings and entrances.' ),
		) : array(
			array( 'איפה אפשר למצוא מפה של הרכבת הקלה בגוש דן?', sprintf( 'בדף הזה: הקו האדום עם %d התחנות שפועלות, הקו הסגול (%d תחנות) והקו הירוק (%d תחנות) שבבנייה, המטרו ורכבת ישראל, הכול על מפה אחת עם הפרויקטים החדשים סביב כל תחנה.', $n( 'red' ), $n( 'purple' ), $n( 'green' ) ) ),
			array( 'מהו פרויקט המטרו בגוש דן?', sprintf( 'שלושה קווי רכבת תחתית מתוכננים, M1, M2 ו־M3, עם %d תחנות בקובץ של משרד התחבורה: ב־M1 יש %d תחנות, ב־M2 יש %d וב־M3 יש %d. מיקומי התחנות בקובץ הם מ־12.2021 ועשויים להשתנות.', $metro, $n( 'm1' ), $n( 'm2' ), $n( 'm3' ) ) ),
			array( 'כמה תחנות יש בקו האדום?', sprintf( '%d תחנות, 10 מהן תת־קרקעיות, מתחנה מרכזית פתח תקווה ועד הקוממיות בבת ים, לפי לוח הזמנים של משרד התחבורה מ־22.11.2026.', $n( 'red' ) ) ),
			array( 'איך מחושבות דקות ההליכה מהפרויקט לתחנה?', 'לפי המרחק בקו אווירי בין הפרויקט לתחנה, כפול 1.3 בגלל הרחובות, בקצב של כ־80 מטר לדקה. זו הערכה; ההליכה בפועל תלויה במעברים ובכניסות לתחנה.' ),
		);

		$crumbs = array(
			array( '@type' => 'ListItem', 'position' => 1, 'name' => $W['home'], 'item' => $home ),
			array( '@type' => 'ListItem', 'position' => 2, 'name' => $W['crumb'], 'item' => $self ),
		);
		$ld = array(
			array( '@context' => 'https://schema.org', '@type' => 'BreadcrumbList', 'itemListElement' => $crumbs ),
			array( '@context' => 'https://schema.org', '@type' => 'Dataset', 'name' => $W['h1'], 'description' => $desc, 'url' => $self, 'inLanguage' => $EN ? 'en' : 'he',
				'license' => 'https://creativecommons.org/licenses/by/4.0/', 'dateModified' => isset( $F['meta']['built'] ) ? $F['meta']['built'] : '2026-11-23',
				'spatialCoverage' => array( '@type' => 'Place', 'name' => $EN ? 'Gush Dan, Israel' : 'גוש דן, ישראל' ),
				'creator' => array( '@type' => 'Organization', 'name' => $EN ? 'NadLan' : 'נדל״ן', 'url' => home_url( '/' ) ),
				'isBasedOn' => array( 'https://data.gov.il/dataset/lrt_stat', 'https://data.gov.il/dataset/metro_stat', 'https://data.gov.il/dataset/rail_stat', 'https://gtfs.mot.gov.il/gtfsfiles/israel-public-transportation.zip' ) ),
			array( '@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => array_map( function ( $q ) {
				return array( '@type' => 'Question', 'name' => $q[0], 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $q[1] ) );
			}, $faq ) ),
		);

		header( 'Referrer-Policy: same-origin' );
		add_filter( 'pre_get_document_title', function () use ( $W ) { return $W['title']; }, 99 );
		if ( $EN ) {
			add_filter( 'language_attributes', function () { return 'lang="en-US" dir="ltr"'; }, 99 );
		}
		add_action( 'wp_head', function () use ( $desc, $self, $ld ) {
			echo '<meta name="description" content="' . esc_attr( $desc ) . '">' . "\n";
			echo '<link rel="canonical" href="' . esc_url( $self ) . '">' . "\n";
			echo '<link rel="alternate" hreflang="he" href="' . esc_url( nltr_self( 'he' ) ) . '">' . "\n";
			echo '<link rel="alternate" hreflang="en" href="' . esc_url( nltr_self( 'en' ) ) . '">' . "\n";
			foreach ( $ld as $o ) { echo '<script type="application/ld+json">' . wp_json_encode( $o, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n"; }
			echo '<link rel="preconnect" href="https://tiles.openfreemap.org" crossorigin>' . "\n";
		}, 4 );
		wp_enqueue_style( 'nltr', nltr_url( 'transit/transit.css' ), array(), $v );
		wp_enqueue_script( 'nltr', nltr_url( 'transit/transit.js' ), array(), $v, true );
		wp_add_inline_script( 'nltr', 'window.NLTR_CFG = ' . wp_json_encode( array(
			'lang' => $lang, 'data' => nltr_url( 'transit/transit-data.json' ) . '?ver=' . $v, 'projects' => nltr_url( 'deals/projects.json' ) . '?ver=' . $v,
			'mlJs' => 'https://cdnjs.cloudflare.com/ajax/libs/maplibre-gl/5.24.0/maplibre-gl.js', 'mlCss' => 'https://cdnjs.cloudflare.com/ajax/libs/maplibre-gl/5.24.0/maplibre-gl.css',
			'rtl' => 'https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.3.0/mapbox-gl-rtl-text.js', 'style' => 'https://tiles.openfreemap.org/styles/positron',
			'geo' => 'https://photon.komoot.io/api/',
		), JSON_UNESCAPED_SLASHES ) . ';', 'before' );

		if ( function_exists( 'nadlan_dir_header_single_h1' ) ) { nadlan_dir_header_single_h1(); } else { get_header(); }
		$dir = $EN ? 'ltr' : 'rtl';
		$h = '<main id="primary" class="site-main nltr-main" dir="' . $dir . '" lang="' . ( $EN ? 'en' : 'he' ) . '">';
		$h .= '<header class="nltr-lead"><nav class="nlbc nlbc--page nltr-crumbs" aria-label="' . esc_attr( $EN ? 'Breadcrumb' : 'מיקום בעמוד' ) . '"><a href="' . esc_url( $home ) . '">' . esc_html( $W['home'] ) . '</a><span class="nlbc-sep" aria-hidden="true">' . ( $EN ? '›' : '›' ) . '</span><span aria-current="page">' . esc_html( $W['crumb'] ) . '</span></nav>';
		$h .= '<h1 class="nltr-h1">' . esc_html( $W['h1'] ) . '</h1>';
		$h .= '<p class="nltr-answer">' . esc_html( $answer ) . '</p></header>';

		/* ---------- the map ---------- */
		$chips = $EN
			? array( array( 'lrt', 'Light rail', 'red' ), array( 'metro', 'Metro', 'm1' ), array( 'rail', 'Israel Railways', 'rail' ), array( 'proj', 'New projects', 'proj' ) )
			: array( array( 'lrt', 'רכבת קלה', 'red' ), array( 'metro', 'מטרו', 'm1' ), array( 'rail', 'רכבת ישראל', 'rail' ), array( 'proj', 'פרויקטים חדשים', 'proj' ) );
		$h .= '<section id="nltr" class="nltr" aria-label="' . esc_attr( $EN ? 'Transit map' : 'מפת התחבורה' ) . '">';
		$h .= '<div class="nltr-bar"><form class="nltr-search" role="search" action="#"><label class="nltr-sr" for="nltr-q">' . esc_html( $EN ? 'Search a station, project or address' : 'חיפוש תחנה, פרויקט או כתובת' ) . '</label>'
			. '<input id="nltr-q" type="search" autocomplete="off" placeholder="' . esc_attr( $EN ? 'Station, project or address' : 'תחנה, פרויקט או כתובת' ) . '"><button type="submit">' . esc_html( $EN ? 'Search' : 'חיפוש' ) . '</button><ul class="nltr-res" hidden></ul></form>';
		$h .= '<div class="nltr-chips" role="group" aria-label="' . esc_attr( $EN ? 'What the map shows' : 'מה רואים על המפה' ) . '">';
		foreach ( $chips as $c ) {
			$h .= '<button type="button" class="nltr-chip" data-k="' . esc_attr( $c[0] ) . '" aria-pressed="true"><i class="nltr-sw nltr-sw--' . esc_attr( $c[2] ) . '" aria-hidden="true"></i>' . esc_html( $c[1] ) . '</button>';
		}
		$h .= '</div></div>';
		$h .= '<div class="nltr-stage"><div id="nltr-map" class="nltr-map"><p class="nltr-wait">' . esc_html( $EN ? 'Loading the map' : 'המפה נטענת' ) . '</p></div>'
			. '<aside class="nltr-card" id="nltr-card" hidden aria-live="polite"></aside></div>';
		$h .= '<p class="nltr-src">' . esc_html( $EN ? 'Sources and last update: Ministry of Transport open data and national timetable of 22.11.2026, Tel Aviv-Yafo municipal GIS; checked 23.11.2026. Walking minutes are estimates.' : 'מקורות ועדכון אחרון: המאגרים הפתוחים ולוח הזמנים הארצי של משרד התחבורה מ־22.11.2026, ומערכת המידע הגאוגרפי של עיריית תל אביב־יפו. נבדק ב־23.11.2026. דקות ההליכה הן הערכה.' ) . ' <a href="#nltr-sources">' . esc_html( $EN ? 'Full list' : 'הרשימה המלאה' ) . '</a></p>';
		$h .= '</section>';

		/* ---------- the lines table ---------- */
		$rows = array(
			array( 'red', $W['open'], $n( 'red' ) ), array( 'purple', $W['build'], $n( 'purple' ) ), array( 'green', $W['build'], $n( 'green' ) ),
			array( 'm1', $W['plan'], $n( 'm1' ) ), array( 'm2', $W['plan'], $n( 'm2' ) ), array( 'm3', $W['plan'], $n( 'm3' ) ),
		);
		$h .= '<section class="nltr-sec"><h2>' . esc_html( $EN ? 'The lines in Gush Dan: state and number of stations' : 'הקווים בגוש דן: מצב הקו ומספר התחנות' ) . '</h2>';
		$h .= '<div class="nltr-tw"><table class="nltr-t"><caption>' . esc_html( $EN ? 'Per the Ministry of Transport files and timetable, checked 23.11.2026' : 'לפי הקבצים ולוח הזמנים של משרד התחבורה, נבדק ב־23.11.2026' ) . '</caption><thead><tr><th scope="col">' . esc_html( $EN ? 'Line' : 'הקו' ) . '</th><th scope="col">' . esc_html( $EN ? 'State' : 'מצב' ) . '</th><th scope="col">' . esc_html( $EN ? 'Stations' : 'תחנות' ) . '</th></tr></thead><tbody>';
		foreach ( $rows as $r ) {
			if ( empty( $F['lines'][ $r[0] ] ) ) { continue; }
			$h .= '<tr><th scope="row"><i class="nltr-sw nltr-sw--' . esc_attr( $r[0] ) . '" aria-hidden="true"></i>' . esc_html( nltr_line_name( $F['lines'][ $r[0] ], $lang ) ) . '</th><td>' . esc_html( $r[1] ) . '</td><td>' . (int) $r[2] . '</td></tr>';
		}
		$h .= '<tr><th scope="row"><i class="nltr-sw nltr-sw--rail" aria-hidden="true"></i>' . esc_html( $EN ? 'Israel Railways (whole country)' : 'רכבת ישראל (כל הארץ)' ) . '</th><td>' . esc_html( $W['open'] ) . '</td><td>' . (int) $rail_open . ( $rail_build ? esc_html( $EN ? ' + ' . $rail_build . ' under construction' : ' ועוד ' . $rail_build . ' בבנייה' ) : '' ) . '</td></tr>';
		$h .= '</tbody></table></div></section>';

		/* ---------- projects near stations ---------- */
		if ( $near_n ) {
			$h .= '<section class="nltr-sec" id="nltr-near"><h2>' . esc_html( $EN ? 'New projects within a 10 minute walk of a station' : 'פרויקטים חדשים עד 10 דקות הליכה מתחנה' ) . '</h2>';
			$h .= '<p>' . esc_html( $EN ? sprintf( '%d projects from our catalogue in Gush Dan are within about 10 minutes on foot of a light rail, Metro or Israel Railways station. The nearest station of each, closest first:', $near_n ) : sprintf( '%d פרויקטים מהקטלוג שלנו בגוש דן נמצאים עד כ־10 דקות הליכה מתחנת רכבת קלה, מטרו או רכבת ישראל. התחנה הקרובה לכל אחד, מהקרוב לרחוק:', $near_n ) ) . '</p>';
			$h .= '<div class="nltr-tw"><table class="nltr-t"><thead><tr><th scope="col">' . esc_html( $EN ? 'Project' : 'הפרויקט' ) . '</th><th scope="col">' . esc_html( $EN ? 'Nearest station' : 'התחנה הקרובה' ) . '</th><th scope="col">' . esc_html( $EN ? 'Line and state' : 'הקו ומצבו' ) . '</th><th scope="col">' . esc_html( $EN ? 'Walk' : 'הליכה' ) . '</th></tr></thead><tbody>';
			foreach ( array_slice( $F['near'], 0, 60 ) as $r ) {
				$l = isset( $F['lines'][ $r['s']['line'] ] ) ? $F['lines'][ $r['s']['line'] ] : null;
				$h .= '<tr><th scope="row"><a href="' . esc_url( home_url( $r['url'] ) ) . '">' . esc_html( $r['name'] ) . '</a></th><td>' . esc_html( nltr_st_name( $r['s'], $lang ) ) . '</td><td>' . esc_html( ( $l ? nltr_line_name( $l, $lang ) : '' ) . ' · ' . $W[ $r['s']['status'] ] ) . '</td><td>' . esc_html( $EN ? 'about ' . $r['min'] . ' min' : 'כ־' . $r['min'] . ' דק׳' ) . '</td></tr>';
			}
			$h .= '</tbody></table></div>';
			if ( $near_n > 60 ) { $h .= '<p class="nltr-note">' . esc_html( $EN ? 'The other projects are on the map: switch on "New projects".' : 'שאר הפרויקטים על המפה: הפעילו "פרויקטים חדשים".' ) . '</p>'; }
			$h .= '</section>';
		}

		/* ---------- station lists per line ---------- */
		$h .= '<section class="nltr-sec"><h2>' . esc_html( $EN ? 'The stations of every line' : 'התחנות של כל קו' ) . '</h2>';
		foreach ( array( 'red', 'purple', 'green', 'm1', 'm2', 'm3' ) as $id ) {
			if ( empty( $F['by'][ $id ] ) || empty( $F['lines'][ $id ] ) ) { continue; }
			$names = array_map( function ( $s ) use ( $lang ) { return nltr_st_name( $s, $lang ); }, $F['by'][ $id ] );
			$st = 'red' === $id ? $W['open'] : ( in_array( $id, array( 'purple', 'green' ), true ) ? $W['build'] : $W['plan'] );
			$h .= '<details class="nltr-det"><summary><i class="nltr-sw nltr-sw--' . esc_attr( $id ) . '" aria-hidden="true"></i>' . esc_html( ( $EN ? 'Stations of the ' : 'תחנות ' ) . nltr_line_name( $F['lines'][ $id ], $lang ) . ' · ' . $st . ' · ' . count( $names ) ) . '</summary><p>' . esc_html( implode( ' · ', $names ) ) . '</p></details>';
		}
		$dan = array_filter( isset( $F['by']['rail'] ) ? $F['by']['rail'] : array(), function ( $s ) { return $s['p'][1] > 31.85 && $s['p'][1] < 32.25 && $s['p'][0] < 35.0; } );
		if ( $dan ) {
			$h .= '<details class="nltr-det"><summary><i class="nltr-sw nltr-sw--rail" aria-hidden="true"></i>' . esc_html( ( $EN ? 'Israel Railways stations in Gush Dan · ' : 'תחנות רכבת ישראל בגוש דן · ' ) . count( $dan ) ) . '</summary><p>' . esc_html( implode( ' · ', array_map( function ( $s ) use ( $lang, $W ) { return nltr_st_name( $s, $lang ) . ( 'build' === $s['status'] ? ' (' . $W['build'] . ')' : '' ); }, $dan ) ) ) . '</p></details>';
		}
		$h .= '</section>';

		/* ---------- questions ---------- */
		$h .= '<section class="nltr-sec"><h2>' . esc_html( $EN ? 'Questions and answers' : 'שאלות ותשובות' ) . '</h2>';
		foreach ( $faq as $q ) { $h .= '<h3>' . esc_html( $q[0] ) . '</h3><p>' . esc_html( $q[1] ) . '</p>'; }
		$h .= '</section>';

		/* ---------- sources ---------- */
		$h .= '<section class="nltr-sec nltr-sources" id="nltr-sources"><h2>' . esc_html( $EN ? 'Sources and last update' : 'מקורות ועדכון אחרון' ) . '</h2><ul>';
		foreach ( isset( $F['meta']['sources'] ) ? $F['meta']['sources'] : array() as $s ) { $h .= '<li>' . esc_html( $EN ? $s['en'] : $s['he'] ) . '</li>'; }
		$h .= '</ul><p>' . esc_html( $EN
			? 'A line\'s state is shown in words and comes from these sources. Opening dates are shown only when an official source publishes them, with the source and the date we checked it. The Red Line stations that run today come from the national timetable, not from the status field of the station file. Metro station positions are from the 12.2021 file and may change.'
			: 'מצב כל קו כתוב במילים ולקוח מהמקורות האלה. מועד פתיחה מוצג רק כשמקור רשמי מפרסם אותו, עם המקור ותאריך הבדיקה. התחנות של הקו האדום שפועלות היום נלקחות מלוח הזמנים הארצי, ולא משדה המצב בקובץ התחנות. מיקומי תחנות המטרו לקוחים מהקובץ של 12.2021 ועשויים להשתנות.' ) . '</p>';
		if ( ! $EN ) {
			$h .= '<p>' . 'עוד באתר: <a href="' . esc_url( home_url( '/sde-dov/transport/' ) ) . '">תחבורה ונגישות ברובע שדה דב</a> · <a href="' . esc_url( home_url( '/jerusalem-green-line-light-rail-property-2026/' ) ) . '">הקו הירוק בירושלים</a> · <a href="' . esc_url( nltr_self( 'en' ) ) . '" hreflang="en" lang="en">English</a></p>';
		} else {
			$h .= '<p><a href="' . esc_url( nltr_self( 'he' ) ) . '" hreflang="he" lang="he">עברית</a></p>';
		}
		$h .= '</section></main>';
		echo $h; // phpcs:ignore -- every value above is escaped where it is built
		get_footer();
	}
}
