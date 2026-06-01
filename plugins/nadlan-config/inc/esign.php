<?php
/**
 * nadlan-config — e-Signature adapter (v1.11.0)
 *
 * Pluggable e-sign request kicked off on `nadlan_auction_closed` (status=sold).
 * Provider-agnostic via filter — default is a no-op that stores a "pending"
 * record + emails the parties; real provider (BoldSign/Dropbox Sign/DocuSign)
 * wires in by returning a signing URL from the `nadlan_esign_create_request`
 * filter.
 *
 * ⚠️ ISRAELI LAW (Electronic Signature Law 5761-2001, amended 2018):
 *   Electronic signatures ARE legally valid for most documents — BUT NOT for:
 *   wills, notarized deeds, **property transactions / conveyances**, land-registry
 *   requests, POAs, and bank-customer agreements. SO: this adapter is intended
 *   for the auction-WIN ENGAGEMENT/OFFER LETTER + earnest-deposit confirmation,
 *   NOT the actual שטר מכר (which must be handwritten + filed via a lawyer).
 *   The default email body and any provider template MUST make this scope
 *   explicit. Verify with counsel before going live.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_esign_register_cpt' ) ) {
	function nadlan_esign_register_cpt() {
		register_post_type( 'nadlan_esign', array(
			'labels' => array( 'name' => 'NadLan e-Sign Requests', 'singular_name' => 'e-Sign Request' ),
			'public' => false, 'show_ui' => true, 'show_in_menu' => true,
			'menu_icon' => 'dashicons-edit-page', 'menu_position' => 32,
			'supports' => array( 'title', 'editor', 'custom-fields' ),
		) );
	}
}
add_action( 'init', 'nadlan_esign_register_cpt' );

/**
 * Build the document text for an auction-win offer letter (Hebrew + the legal scope note).
 */
if ( ! function_exists( 'nadlan_esign_offer_doc' ) ) {
	function nadlan_esign_offer_doc( $auction_id ) {
		$listing_id = (int) get_post_meta( $auction_id, 'listing_id', true );
		$high       = (float) get_post_meta( $auction_id, 'current_high_bid', true );
		$premium    = (float) get_post_meta( $auction_id, 'buyers_premium_pct', true );
		$total      = $high * ( 1 + $premium / 100 );
		$lines  = "מכתב הצעת רכש — מכרז #" . $auction_id . "\n\n";
		$lines .= "נכס: " . ( $listing_id ? get_the_title( $listing_id ) : '—' ) . "\n";
		$lines .= "הצעה זוכה: ₪" . number_format( $high ) . " (כולל פרמיית קונה " . $premium . "% = ₪" . number_format( $total ) . ")\n\n";
		$lines .= "החותם מאשר את ההצעה הזוכה ומתחייב להתקדם לעריכת חוזה מכר רשמי באמצעות עו\"ד מקרקעין.\n\n";
		$lines .= "⚠ הבהרה משפטית: מסמך זה הוא מכתב הצעה / התחייבות עקרונית בלבד. בהתאם לחוק חתימה אלקטרונית, התשס\"א-2001, ולפסיקה — חוזה מכר מקרקעין וטיפול ברישום בטאבו דורשים חתימה ידנית וטיפול עו\"ד. חתימה אלקטרונית כאן תקפה אך ורק להצעה ולעקרונות העסקה.";
		return $lines;
	}
}

/**
 * Create a sign request. Default implementation: store + email. Real providers
 * filter to return a hosted signing URL.
 */
if ( ! function_exists( 'nadlan_esign_create' ) ) {
	function nadlan_esign_create( $auction_id ) {
		$winner_id = (int) get_post_meta( $auction_id, 'current_high_bidder', true );
		$winner    = $winner_id ? get_userdata( $winner_id ) : null;
		if ( ! $winner || ! is_email( $winner->user_email ) ) {
			return new WP_Error( 'no_winner_email', 'No winner email' );
		}
		$doc   = nadlan_esign_offer_doc( $auction_id );
		$req   = array( 'auction_id' => $auction_id, 'signer_email' => $winner->user_email, 'doc' => $doc );
		$ext   = apply_filters( 'nadlan_esign_create_request', null, $req ); // providers hook here
		$sign_url = is_array( $ext ) && ! empty( $ext['url'] ) ? (string) $ext['url'] : '';

		$id = wp_insert_post( array(
			'post_type' => 'nadlan_esign', 'post_status' => 'private',
			'post_title' => 'e-Sign #' . $auction_id . ' → ' . $winner->user_email,
			'post_content' => $doc,
		) );
		if ( is_wp_error( $id ) ) { return $id; }
		update_post_meta( $id, 'auction_id', $auction_id );
		update_post_meta( $id, 'signer_email', $winner->user_email );
		update_post_meta( $id, 'state', $sign_url ? 'sent' : 'pending_provider' );
		update_post_meta( $id, 'sign_url', $sign_url );

		$body  = "מזל טוב! זכית במכרז #" . $auction_id . " בנדל\"ן חכם.\n\n";
		$body .= $doc . "\n\n";
		if ( $sign_url ) {
			$body .= "לחתימה אלקטרונית: " . $sign_url . "\n";
		} else {
			$body .= "ניצור איתך קשר בהמשך לתיאום החתימה.\n";
		}
		wp_mail( $winner->user_email, 'זכית במכרז — מכתב הצעה לחתימה', $body );

		$admin = get_option( 'admin_email' );
		if ( $admin ) {
			wp_mail( $admin, 'NadLan auction sold #' . $auction_id,
				"Auction #$auction_id sold to {$winner->user_email}.\nDoc + sign-request stored as post #$id." );
		}
		return $id;
	}
}

/* Hook the auction close: status=sold triggers the offer letter */
add_action( 'nadlan_auction_closed', function ( $auction_id ) {
	if ( get_post_meta( $auction_id, 'status', true ) !== 'sold' ) { return; }
	nadlan_esign_create( $auction_id );
} );
