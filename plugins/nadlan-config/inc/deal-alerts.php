<?php
/**
 * nadlan-config - "a new developer deal in my area" alerts (HAD-743, Ben 16.11.2026). Design: Claude Design canvas board 11.
 * Not a parallel system: a request is an ordinary near-alerts row (inc/near-alerts.php, CPT nadlan_saved_search, kind 'nf') whose
 * nf_what holds 'deal'. Sign-up, double opt-in, the daily run, the one-click unsubscribe, the privacy notice and the rate limits are
 * near-alerts'. This file only plugs into its filters:
 *   nadlan_na_collect_more  - the deals of the map (nadlan_dm_deals()) inside the row's area that were not sent before;
 *   nadlan_na_sent          - those deals are marked seen (meta nf_dseen) after the mail went out;
 *   nadlan_na_mail_more     - the deals block of the mail, first in the mail.
 * On a row's first run the deals already in the area are marked seen without a mail: the alert is about NEW deals.
 * Every deal is named with its terms as published, the publish month and the source, and the mail says it is not advice.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_da_in_area' ) ) {
	/** The live deals inside a row's area: [deal + km], nearest first. */
	function nadlan_da_in_area( $p ) {
		if ( ! function_exists( 'nadlan_dm_deals' ) || ! isset( $p['lat'], $p['lng'] ) ) { return array(); }
		$out = array();
		foreach ( nadlan_dm_deals() as $d ) {
			$km = function_exists( 'nadlan_na_km' ) ? nadlan_na_km( (float) $p['lat'], (float) $p['lng'], (float) $d['lat'], (float) $d['lng'] ) : 999;
			$in = ! empty( $p['poly'] ) && function_exists( 'nadlan_na_in_poly' ) ? nadlan_na_in_poly( (float) $d['lat'], (float) $d['lng'], $p['poly'] ) : $km <= max( 1.0, (float) ( $p['r'] ?? 0 ) );
			if ( $in ) { $out[] = $d + array( 'km' => $km ); }
		}
		usort( $out, function ( $a, $b ) { return $a['km'] <=> $b['km']; } );
		return $out;
	}
}

add_filter( 'nadlan_na_collect_more', function ( $out, $s, $now, $floor ) {
	$out['deal'] = array();
	if ( ! in_array( 'deal', (array) ( $s['what'] ?? array() ), true ) ) { return $out; }
	$sid  = (int) ( $s['id'] ?? 0 );
	$all  = nadlan_da_in_area( (array) ( $s['p'] ?? array() ) );
	$seen = get_post_meta( $sid, 'nf_dseen', true );
	if ( ! is_array( $seen ) ) { // first run: what is already there is not news
		if ( null === $floor && $sid ) { update_post_meta( $sid, 'nf_dseen', array_values( wp_list_pluck( $all, 'id' ) ) ); }
		return $out;
	}
	foreach ( $all as $d ) { if ( ! in_array( $d['id'], $seen, true ) ) { $out['deal'][] = $d; } }
	$out['deal'] = array_slice( $out['deal'], 0, 6 );
	return $out;
}, 10, 4 );

add_action( 'nadlan_na_sent', function ( $sid, $c ) {
	if ( empty( $c['deal'] ) ) { return; }
	$seen = get_post_meta( $sid, 'nf_dseen', true );
	$seen = is_array( $seen ) ? $seen : array();
	update_post_meta( $sid, 'nf_dseen', array_slice( array_values( array_unique( array_merge( $seen, wp_list_pluck( $c['deal'], 'id' ) ) ) ), -200 ) );
}, 10, 2 );

add_filter( 'nadlan_na_mail_more', function ( $bt, $s, $c ) {
	if ( empty( $c['deal'] ) || ! function_exists( 'nadlan_na_card' ) ) { return $bt; }
	list( $b, $t ) = $bt;
	$map  = home_url( '/developer-deals/#nldm-map' );
	$b   .= nadlan_na_h2( 1 === count( $c['deal'] ) ? 'מבצע קבלן חדש באזור שלכם' : count( $c['deal'] ) . ' מבצעי קבלנים חדשים באזור שלכם' );
	foreach ( $c['deal'] as $d ) {
		$src = ! empty( $d['src'] ) ? ' · <a href="' . esc_url( $d['src'] ) . '" style="color:#1F4B5C">המקור</a>' : '';
		$in  = '<p style="margin:0 0 2px;font-size:13px;line-height:18px;color:#5E6A75">' . esc_html( $d['devFull'] . ' · ' . $d['city'] ) . '</p>'
			. '<p style="margin:0 0 4px;font-size:16px;line-height:22px;font-weight:600"><a href="' . esc_url( $map ) . '" style="color:#12202A;text-decoration:none">' . esc_html( $d['project'] ) . '</a></p>'
			. '<p style="margin:0 0 6px;font-size:13px;line-height:18px;color:#A10D25;font-weight:600">' . esc_html( $d['kind'] ) . '</p>'
			. '<p style="margin:0 0 6px;font-size:14px;line-height:21px;color:#3E4C58">' . esc_html( $d['terms'] ) . '</p>'
			. '<p style="margin:0;font-size:12px;line-height:18px;color:#5E6A75">פורסם: ' . esc_html( $d['pub'] ) . $src . '. הפרטים לפי פרסומים, והתנאים המחייבים הם אלה שבחוזה. זה לא ייעוץ.</p>'
			. '<p style="margin:12px 0 0">' . nadlan_na_button( $map, 'למפת המבצעים' ) . '</p>';
		$b .= nadlan_na_card( array( 'url' => $map ), $in );
		$t .= 'מבצע קבלן חדש: ' . $d['project'] . ' (' . $d['devFull'] . ")\n" . $d['kind'] . "\n" . $d['terms'] . "\nפורסם: " . $d['pub'] . ( ! empty( $d['src'] ) ? ' · ' . $d['src'] : '' ) . "\n" . $map . "\n\n";
	}
	return array( $b, $t );
}, 10, 3 );
