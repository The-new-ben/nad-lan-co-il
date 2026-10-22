<?php
/**
 * The registered-contractor check (HAD-592, /pinkas-hakablanim/, Ben 22.10.2026: "ultra complex tools with UX that gives you
 * everything with one tap"). Loaded from inc/instruments.php (a module the live plugin already loads).
 *
 * GET /wp-json/nadlan/v1/pinkas?q=&city=&anaf=&min=&mukar=&off=
 *   q      a name (every word must appear; final letters, quotes and בע"מ ignored), a contractor number (up to 6 digits) or a
 *          9-digit company number
 *   city   a city name exactly as in pinkas-meta.json; anaf a branch code; min the lowest level wanted in that branch (ק, 1-5);
 *   mukar  1 = recognised for government works only; off = the offset for "more"
 * Returns at most 30 contractors and the total. Data: data/pinkas-register.php (tools/instruments/build_pinkas.py from the
 * data.gov.il register): number, name, company number, city, first year, recognised level, our profile slug, and per branch
 * code, group, level and restriction. No phone, email or street (they are on the official record, which every card links).
 * The file starts with "<?php exit; ?>" so a direct request returns nothing; nobody pulls the whole list in one request.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_pinkas_data' ) ) {

	function nadlan_pinkas_data() {
		static $d = null;
		if ( null !== $d ) { return $d; }
		$path = dirname( __DIR__ ) . '/data/pinkas-register.php';
		$raw = is_readable( $path ) ? (string) file_get_contents( $path ) : '';
		$nl = strpos( $raw, "\n" );
		$d = false !== $nl ? json_decode( substr( $raw, $nl + 1 ), true ) : null;
		if ( ! is_array( $d ) || empty( $d['rows'] ) ) { $d = array( 'asof' => '', 'n' => 0, 'cities' => array(), 'rows' => array() ); }
		return $d;
	}

	/** The same normalisation as build_pinkas.py norm(). */
	function nadlan_pinkas_norm( $s ) {
		$s = str_replace( array( 'בע"מ', 'בע״מ', 'בעמ' ), ' ', (string) $s );
		$s = preg_replace( '/["\'״׳`.,()\-–_\/\\\\]/u', ' ', $s );
		$s = strtr( $s, array( 'ך' => 'כ', 'ם' => 'מ', 'ן' => 'נ', 'ף' => 'פ', 'ץ' => 'צ' ) );
		return trim( preg_replace( '/\s+/u', ' ', mb_strtolower( $s, 'UTF-8' ) ) );
	}

	function nadlan_pinkas_rank( $lv ) { return 'ק' === $lv ? 0 : (int) $lv; }

	function nadlan_pinkas_search( WP_REST_Request $req ) {
		$d = nadlan_pinkas_data();
		$q = trim( (string) $req->get_param( 'q' ) );
		$city = trim( (string) $req->get_param( 'city' ) );
		$anaf = (int) $req->get_param( 'anaf' );
		$min = (string) $req->get_param( 'min' );
		$muk = (int) $req->get_param( 'mukar' );
		$off = max( 0, min( 20000, (int) $req->get_param( 'off' ) ) );
		$ci = -1;
		if ( '' !== $city ) { $ci = array_search( $city, $d['cities'], true ); if ( false === $ci ) { $ci = -2; } }
		$digits = preg_match( '/^\d{1,9}$/', $q ) ? $q : '';
		$words = '' === $digits && '' !== $q ? array_filter( explode( ' ', nadlan_pinkas_norm( $q ) ), 'strlen' ) : array();
		$nq = $words ? implode( ' ', $words ) : '';
		$minr = '' === $min ? -1 : nadlan_pinkas_rank( $min );
		if ( '' === $q && $ci < 0 && ! $anaf && ! $muk ) {
			return new WP_REST_Response( array( 'total' => 0, 'all' => $d['n'], 'asof' => $d['asof'], 'items' => array() ), 200 );
		}
		$hits = array();
		foreach ( $d['rows'] as $r ) {
			if ( '' !== $digits ) {
				if ( strlen( $digits ) >= 8 ? $r[2] !== $digits : (string) $r[0] !== $digits ) { continue; }
			} elseif ( $words ) {
				$ok = true; foreach ( $words as $w ) { if ( false === strpos( $r[8], $w ) ) { $ok = false; break; } }
				if ( ! $ok ) { continue; }
			}
			if ( $ci >= 0 && $r[3] !== $ci ) { continue; }
			if ( -2 === $ci ) { continue; }
			if ( $muk && ! $r[5] ) { continue; }
			if ( $anaf ) {
				$ok = false;
				foreach ( $r[7] as $b ) { if ( $b[0] === $anaf && ( $minr < 0 || nadlan_pinkas_rank( $b[2] ) >= $minr ) ) { $ok = true; break; } }
				if ( ! $ok ) { continue; }
			}
			$s = 0;
			if ( $nq ) { $s = $r[8] === $nq ? 3 : ( 0 === strpos( $r[8], $nq ) ? 2 : 0 ); }
			$top = 0; foreach ( $r[7] as $b ) { $top = max( $top, nadlan_pinkas_rank( $b[2] ) ); }
			$hits[] = array( $s, $r[6] ? 1 : 0, $top, $r );
		}
		usort( $hits, function ( $a, $b ) { return array( $b[0], $b[1], $b[2], $a[3][1] ) <=> array( $a[0], $a[1], $a[2], $b[3][1] ); } );
		$items = array();
		foreach ( array_slice( $hits, $off, 30 ) as $h ) {
			$r = $h[3];
			$items[] = array( 'n' => $r[0], 'name' => $r[1], 'co' => $r[2], 'city' => isset( $d['cities'][ $r[3] ] ) ? $d['cities'][ $r[3] ] : '', 'y' => $r[4], 'mukar' => $r[5],
				'page' => $r[6] ? home_url( '/professionals/' . rawurlencode( $r[6] ) . '/' ) : '', 'b' => $r[7] );
		}
		$res = new WP_REST_Response( array( 'total' => count( $hits ), 'all' => $d['n'], 'asof' => $d['asof'], 'off' => $off, 'items' => $items ), 200 );
		$res->header( 'Cache-Control', 'public, max-age=3600' );
		return $res;
	}

	add_action( 'rest_api_init', function () {
		register_rest_route( 'nadlan/v1', '/pinkas', array(
			'methods' => 'GET', 'callback' => 'nadlan_pinkas_search', 'permission_callback' => '__return_true',
			'args' => array( 'q' => array( 'sanitize_callback' => 'sanitize_text_field' ), 'city' => array( 'sanitize_callback' => 'sanitize_text_field' ),
				'min' => array( 'sanitize_callback' => 'sanitize_text_field' ) ),
		) );
	} );
}
