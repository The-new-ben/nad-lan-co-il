<?php
/**
 * nadlan-config — Card claim & ownership funnel (v1.5.0)
 *
 * Flow: free auto-created card (unclaimed) → owner submits a CLAIM via the public
 * REST endpoint → stored as a private nadlan_claim, card flips to "pending", admin
 * is emailed → admin APPROVES (assigns a WP user as owner) → card flips to
 * "verified" and that user may edit ONLY their own card (upload photos, edit text).
 *
 * SECURITY NOTE (flagged for the Cowork review pass — see docs/listings-questions.md):
 *  - The identity-verification METHOD (proving the claimant truly owns the entity)
 *    is intentionally left to admin judgement + a token here; a stronger automated
 *    check (email-domain match, phone OTP, registry cross-check) is a TODO.
 *  - Owner editing is scoped to the owner's own single card via map_meta_cap.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

const NADLAN_CARD_CPTS = array( 'nadlan_property', 'nadlan_project', 'nadlan_professional' );

/* ---- claim-request CPT (private back-office) ---- */
if ( ! function_exists( 'nadlan_claim_register_cpt' ) ) {
	function nadlan_claim_register_cpt() {
		register_post_type( 'nadlan_claim', array(
			'labels'       => array( 'name' => 'NadLan Claims', 'singular_name' => 'NadLan Claim' ),
			'public'       => false,
			'show_ui'      => true,
			'show_in_menu' => true,
			'menu_icon'    => 'dashicons-id-alt',
			'menu_position'=> 29,
			'supports'     => array( 'title', 'editor', 'custom-fields' ),
			'capability_type' => 'post',
		) );
	}
}
add_action( 'init', 'nadlan_claim_register_cpt' );

/* ---- public REST: POST /nadlan/v1/claim ---- */
if ( ! function_exists( 'nadlan_claim_register_rest' ) ) {
	function nadlan_claim_register_rest() {
		register_rest_route( 'nadlan/v1', '/claim', array(
			'methods'             => 'POST',
			'callback'            => 'nadlan_claim_rest_handler',
			'permission_callback' => '__return_true',
		) );
	}
}
add_action( 'rest_api_init', 'nadlan_claim_register_rest' );

if ( ! function_exists( 'nadlan_claim_rest_handler' ) ) {
	function nadlan_claim_rest_handler( $req ) {
		$p = $req->get_json_params();
		if ( ! is_array( $p ) ) { $p = $req->get_params(); }

		// Honeypot
		if ( ! empty( $p['company'] ) ) {
			return new WP_REST_Response( array( 'ok' => true ), 200 );
		}
		$g = function( $k ) use ( $p ) {
			return isset( $p[ $k ] ) ? sanitize_text_field( wp_unslash( (string) $p[ $k ] ) ) : '';
		};
		$post_id = (int) ( $p['post_id'] ?? 0 );
		$name    = $g( 'name' );
		$phone   = $g( 'phone' );
		$email   = isset( $p['email'] ) ? sanitize_email( wp_unslash( (string) $p['email'] ) ) : '';
		$message = isset( $p['message'] ) ? sanitize_textarea_field( wp_unslash( (string) $p['message'] ) ) : '';

		$card = $post_id ? get_post( $post_id ) : null;
		if ( ! $card || ! in_array( $card->post_type, NADLAN_CARD_CPTS, true ) ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'bad_card' ), 400 );
		}
		if ( $email === '' && $phone === '' ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'need_contact' ), 400 );
		}
		// Rate-limit: 5 / 10 min per IP
		$iph = isset( $_SERVER['REMOTE_ADDR'] ) ? md5( $_SERVER['REMOTE_ADDR'] . 'nadlanclaim' ) : 'x';
		$key = 'nadlan_clrl_' . $iph;
		if ( (int) get_transient( $key ) >= 5 ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'rate' ), 429 );
		}
		set_transient( $key, ( (int) get_transient( $key ) ) + 1, 10 * MINUTE_IN_SECONDS );

		$token = strtolower( bin2hex( random_bytes( 16 ) ) );
		$title = sprintf( 'CLAIM: %s ← %s (%s)', get_the_title( $card ), $name ?: $email, current_time( 'Y-m-d H:i' ) );
		$claim_id = wp_insert_post( array(
			'post_type'    => 'nadlan_claim',
			'post_status'  => 'private',
			'post_title'   => $title,
			'post_content' => $message,
		), true );
		if ( is_wp_error( $claim_id ) ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'save' ), 500 );
		}
		foreach ( array(
			'card_id' => $post_id, 'card_type' => $card->post_type,
			'name' => $name, 'phone' => $phone, 'email' => $email,
			'token' => $token, 'claim_state' => 'pending',
		) as $k => $v ) {
			if ( $v !== '' ) { update_post_meta( $claim_id, $k, $v ); }
		}
		// Flip the card to pending (does not grant access yet)
		update_post_meta( $post_id, 'claim_status', 'pending' );

		$admin = get_option( 'admin_email' );
		if ( $admin ) {
			$link = admin_url( 'post.php?post=' . $claim_id . '&action=edit' );
			$body = "בקשת בעלות על כרטיס ב-nad-lan.co.il\n\n";
			$body .= 'כרטיס: ' . get_the_title( $card ) . ' (' . get_permalink( $card ) . ")\n";
			$body .= "שם: $name\nטלפון: $phone\nאימייל: $email\n\nהודעה:\n$message\n\n";
			$body .= "אישור הבקשה: $link\n";
			wp_mail( $admin, 'NadLan claim: ' . get_the_title( $card ), $body );
		}
		return new WP_REST_Response( array( 'ok' => true, 'claim_id' => $claim_id ), 200 );
	}
}

/* ---- admin approval: assign owner + verify ----
 * Triggered from the claim edit screen via a nonce'd admin-post action.
 * Looks up the WP user by the claim email; if none, creates a subscriber-level
 * account (so the owner can log in and edit their card). The owner is then mapped
 * to edit ONLY this card (see map_meta_cap below).
 */
if ( ! function_exists( 'nadlan_claim_approve' ) ) {
	function nadlan_claim_approve() {
		if ( ! current_user_can( 'manage_options' ) ) { wp_die( 'forbidden' ); }
		$claim_id = isset( $_GET['claim_id'] ) ? (int) $_GET['claim_id'] : 0;
		check_admin_referer( 'nadlan_approve_' . $claim_id );

		$card_id = (int) get_post_meta( $claim_id, 'card_id', true );
		$email   = (string) get_post_meta( $claim_id, 'email', true );
		$name    = (string) get_post_meta( $claim_id, 'name', true );
		if ( ! $card_id || ! get_post( $card_id ) ) { wp_die( 'bad card' ); }

		$user = $email ? get_user_by( 'email', $email ) : false;
		if ( ! $user && $email ) {
			$uid = wp_insert_user( array(
				'user_login'   => 'owner_' . $card_id . '_' . wp_generate_password( 4, false ),
				'user_email'   => $email,
				'user_pass'    => wp_generate_password( 20 ),
				'display_name' => $name ?: $email,
				'role'         => 'subscriber',
			) );
			if ( ! is_wp_error( $uid ) ) {
				$user = get_user_by( 'id', $uid );
				wp_new_user_notification( $uid, null, 'user' ); // sends set-password email
			}
		}
		if ( $user ) {
			update_post_meta( $card_id, 'owner_user_id', (int) $user->ID );
			update_post_meta( $card_id, 'claim_status', 'verified' );
			update_post_meta( $card_id, 'verified_at', time() );
			update_post_meta( $claim_id, 'claim_state', 'approved' );
		}
		wp_safe_redirect( admin_url( 'post.php?post=' . $claim_id . '&action=edit&claim=approved' ) );
		exit;
	}
}
add_action( 'admin_post_nadlan_claim_approve', 'nadlan_claim_approve' );

/* Approve button on the claim edit screen */
if ( ! function_exists( 'nadlan_claim_meta_box' ) ) {
	function nadlan_claim_meta_box() {
		add_meta_box( 'nadlan_claim_actions', 'Claim actions', function( $post ) {
			$state   = get_post_meta( $post->ID, 'claim_state', true );
			$card_id = (int) get_post_meta( $post->ID, 'card_id', true );
			$url = wp_nonce_url(
				admin_url( 'admin-post.php?action=nadlan_claim_approve&claim_id=' . $post->ID ),
				'nadlan_approve_' . $post->ID
			);
			echo '<p>State: <strong>' . esc_html( $state ?: 'pending' ) . '</strong></p>';
			if ( $card_id ) {
				echo '<p>Card: <a href="' . esc_url( get_edit_post_link( $card_id ) ) . '">#' . (int) $card_id . '</a></p>';
			}
			if ( $state !== 'approved' ) {
				echo '<a class="button button-primary" href="' . esc_url( $url ) . '">Approve &amp; assign owner</a>';
			} else {
				echo '<p>✓ Approved — owner assigned.</p>';
			}
		}, 'nadlan_claim', 'side' );
	}
}
add_action( 'add_meta_boxes', 'nadlan_claim_meta_box' );

/* ---- owner editing: a verified owner may edit ONLY their own card ---- */
if ( ! function_exists( 'nadlan_claim_map_meta_cap' ) ) {
	function nadlan_claim_map_meta_cap( $caps, $cap, $user_id, $args ) {
		if ( ! in_array( $cap, array( 'edit_post', 'edit_published_posts', 'upload_files' ), true ) ) {
			return $caps;
		}
		$post_id = isset( $args[0] ) ? (int) $args[0] : 0;
		if ( $cap === 'upload_files' && $user_id ) {
			// allow uploads for any verified card owner (needed for photo upload)
			$owns = get_posts( array(
				'post_type' => NADLAN_CARD_CPTS, 'posts_per_page' => 1, 'fields' => 'ids',
				'meta_query' => array(
					array( 'key' => 'owner_user_id', 'value' => $user_id ),
					array( 'key' => 'claim_status', 'value' => 'verified' ),
				),
			) );
			if ( $owns ) { return array( 'read' ); }
			return $caps;
		}
		if ( ! $post_id ) { return $caps; }
		$post = get_post( $post_id );
		if ( ! $post || ! in_array( $post->post_type, NADLAN_CARD_CPTS, true ) ) { return $caps; }
		$owner = (int) get_post_meta( $post_id, 'owner_user_id', true );
		if ( $owner && $owner === (int) $user_id
			&& get_post_meta( $post_id, 'claim_status', true ) === 'verified' ) {
			return array( 'read' ); // grant: owner edits their own verified card
		}
		return $caps;
	}
}
add_filter( 'map_meta_cap', 'nadlan_claim_map_meta_cap', 10, 4 );
