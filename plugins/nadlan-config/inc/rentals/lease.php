<?php
/**
 * nadlan-config - RENTALS v2: the lease text on the server (HAD-383).
 * Renders assets/rentals/i18n/lease.json exactly as rm-lease.js does. This
 * is the text a tenant signs; its SHA-256 goes into the signing record.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nlrm_json' ) ) {
	function nlrm_json( $name ) {
		static $c = array();
		if ( ! isset( $c[ $name ] ) ) {
			$raw = @file_get_contents( NLRM_DIR_ASSETS . 'i18n/' . $name . '.json' ); // phpcs:ignore
			$c[ $name ] = $raw ? json_decode( $raw, true ) : array();
		}
		return $c[ $name ];
	}
}
if ( ! function_exists( 'nlrm_fill' ) ) {
	function nlrm_fill( $s, $v ) {
		return preg_replace_callback( '/\{\{([a-z_]+)\}\}/', function ( $m ) use ( $v ) { return isset( $v[ $m[1] ] ) ? (string) $v[ $m[1] ] : ''; }, (string) $s );
	}
}
if ( ! function_exists( 'nlrm_lease_money' ) ) {
	function nlrm_lease_money( $n, $lang ) {
		$s = number_format( (int) round( (float) $n ) );
		return 'he' === $lang ? $s . ' ₪' : '₪' . $s;
	}
}
if ( ! function_exists( 'nlrm_lease_date' ) ) {
	function nlrm_lease_date( $iso, $lang ) {
		if ( ! $iso ) { return ''; }
		$t = strtotime( substr( (string) $iso, 0, 10 ) . ' 12:00:00 UTC' );
		return 'he' === $lang ? gmdate( 'j.n.Y', $t ) : gmdate( 'j F Y', $t );
	}
}
if ( ! function_exists( 'nlrm_lease_text' ) ) {
	/* -> array( title, intro, sections => [ [h, ps] ], signatures, footer, version, lang ) */
	function nlrm_lease_text( $owner, $lease, $lang ) {
		$T = nlrm_json( 'lease' );
		if ( ! $T ) { return array(); }
		$lang = isset( $T['title'][ $lang ] ) ? $lang : 'he';
		$W = $T['words'][ $lang ];
		$ui = nlrm_json( $lang );
		$unit = nlrm_get( 'unit', (int) $lease['unit_id'], $owner ) ?: array();
		$prop = $unit ? ( nlrm_get( 'property', (int) $unit['property_id'], $owner ) ?: array() ) : array();
		$m = isset( $unit['meta'] ) ? (array) $unit['meta'] : array();
		$sec = (array) $lease['securities']; $terms = (array) $lease['terms']; $link = (array) $lease['linkage'];
		$flags = array(
			'cpi' => ( $link['mode'] ?? '' ) === 'cpi', 'option' => ! empty( $lease['option_until'] ), 'pets' => ! empty( $terms['pets'] ), 'nopets' => empty( $terms['pets'] ),
			'deposit' => ! empty( $sec['deposit'] ), 'cheque' => ! empty( $sec['cheque'] ), 'note' => ! empty( $sec['note'] ), 'guarantors' => ! empty( $sec['guarantors'] ), 'bank' => ! empty( $sec['bank'] ),
			'furnished' => ! empty( $m['furnished'] ), 'parking' => ! empty( $m['parking'] ), 'storage' => ! empty( $m['storage'] ),
		);
		$secs = array();
		if ( ! empty( $sec['cheque'] ) ) { $secs[] = nlrm_fill( $W['cheque'], array( 'n' => nlrm_lease_money( $sec['cheque'], $lang ) ) ); }
		if ( ! empty( $sec['note'] ) ) { $secs[] = nlrm_fill( $W['note'], array( 'n' => nlrm_lease_money( $sec['note'], $lang ) ) ); }
		if ( ! empty( $sec['deposit'] ) ) { $secs[] = nlrm_fill( $W['deposit'], array( 'n' => nlrm_lease_money( $sec['deposit'], $lang ) ) ); }
		if ( ! empty( $sec['guarantors'] ) ) { $secs[] = $W['guarantors']; }
		if ( ! empty( $sec['bank'] ) ) { $secs[] = $W['bank']; }
		$tenants = array();
		foreach ( (array) ( ( (array) $lease['parties'] )['tenants'] ?? array() ) as $cid ) {
			$c = nlrm_get( 'contact', (int) $cid, $owner );
			if ( $c ) { $tenants[] = $c['name'] . ( $c['idno'] ? nlrm_fill( $W['id'], array( 'id' => $c['idno'] ) ) : '' ); }
		}
		$u = get_userdata( $owner );
		$lid = nlrm_dec( (string) get_user_meta( $owner, 'nlrm_idno_enc', true ) );
		$method = (string) ( $terms['method'] ?? 'transfer' );
		$v = array(
			'date' => nlrm_lease_date( substr( (string) ( $lease['created_at'] ?? gmdate( 'Y-m-d' ) ), 0, 10 ), $lang ),
			'landlord' => (string) ( get_user_meta( $owner, 'nlrm_display', true ) ?: ( $u ? $u->display_name : '' ) ), 'landlord_id' => $lid ? nlrm_fill( $W['id'], array( 'id' => $lid ) ) : '',
			'tenants' => implode( $W['and'], $tenants ), 'address' => (string) ( $prop['address'] ?? '' ), 'city' => (string) ( $prop['city'] ?? '' ), 'unit_label' => (string) ( $unit['label'] ?? '' ),
			'floor_txt' => ! empty( $unit['floor'] ) ? nlrm_fill( $W['floor'], array( 'n' => $unit['floor'] ) ) : '', 'rooms_txt' => ! empty( $unit['rooms'] ) ? nlrm_fill( $W['rooms'], array( 'n' => rtrim( rtrim( (string) $unit['rooms'], '0' ), '.' ) ) ) : '',
			'extras' => ( $flags['furnished'] ? $W['furnished'] : '' ) . ( $flags['parking'] ? $W['parking'] : '' ) . ( $flags['storage'] ? $W['storage'] : '' ),
			'start' => nlrm_lease_date( $lease['start_date'], $lang ), 'end' => nlrm_lease_date( $lease['end_date'], $lang ), 'option_until' => nlrm_lease_date( $lease['option_until'], $lang ),
			'rent' => nlrm_lease_money( $lease['rent'], $lang ), 'pay_day' => (int) $lease['pay_day'], 'method' => mb_strtolower( (string) ( $ui['ui'][ 'm_' . $method ] ?? $method ) ),
			'link_pct' => (int) ( $link['pct'] ?? 100 ), 'link_base' => nlrm_lease_date( $link['base_date'] ?? $lease['start_date'], $lang ), 'link_every' => (int) ( $link['every'] ?? 12 ), 'link_floor' => ! empty( $link['floor'] ) ? $W['floor_clause'] : '',
			'securities' => $secs ? implode( ', ', $secs ) : $W['none'],
		);
		$sections = array();
		$num = 0;
		foreach ( $T['sections'] as $s ) {
			if ( ! empty( $s['when'] ) && empty( $flags[ $s['when'] ] ) ) { continue; }
			/* the clause numbers run in order whatever optional clause is left out (HAD-401: 3, then 5) */
			$h = (string) $s['h'][ $lang ];
			if ( preg_match( '/^\d+\.\s*/u', $h ) ) { $num++; $h = $num . '. ' . preg_replace( '/^\d+\.\s*/u', '', $h ); }
			$sections[] = array( 'h' => $h, 'ps' => array_map( function ( $x ) use ( $lang, $v ) { return nlrm_fill( $x[ $lang ], $v ); }, $s['p'] ) );
		}
		return array( 'version' => $T['version'], 'lang' => $lang, 'title' => $T['title'][ $lang ], 'intro' => nlrm_fill( $T['intro'][ $lang ], $v ), 'sections' => $sections, 'signatures' => $T['signatures'][ $lang ], 'footer' => $T['footer'][ $lang ] );
	}
}
