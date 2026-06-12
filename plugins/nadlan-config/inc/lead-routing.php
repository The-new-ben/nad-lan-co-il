<?php
/**
 * nadlan-config - Lead routing to paid card owners (v1.42.9).
 *
 * Routes a captured nadlan_lead to the owner of the exact card that received
 * the inquiry, only when that card is on a paid tier. Admin notification remains
 * the fallback path for free, unclaimed, invalid, or owner-unavailable cards.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_lead_route_card_types' ) ) {
	function nadlan_lead_route_card_types() {
		return array( 'nadlan_professional', 'nadlan_project', 'nadlan_property' );
	}
}

if ( ! function_exists( 'nadlan_lead_route_paid_tiers' ) ) {
	function nadlan_lead_route_paid_tiers() {
		return apply_filters( 'nadlan_lead_route_paid_tiers', array( 'pro', 'premier' ) );
	}
}

if ( ! function_exists( 'nadlan_lead_route_fields' ) ) {
	function nadlan_lead_route_fields( $lead_id, $fields = array() ) {
		$lead = get_post( (int) $lead_id );
		$out = array(
			'name'    => '',
			'phone'   => '',
			'email'   => '',
			'goal'    => '',
			'message' => '',
			'source'  => '',
		);
		foreach ( $out as $key => $empty ) {
			if ( isset( $fields[ $key ] ) && $fields[ $key ] !== '' ) {
				$out[ $key ] = (string) $fields[ $key ];
			} else {
				$meta_key = $key === 'source' ? 'utm_source' : $key;
				$out[ $key ] = (string) get_post_meta( (int) $lead_id, $meta_key, true );
			}
		}
		if ( $out['message'] === '' && $lead ) {
			$out['message'] = (string) $lead->post_content;
		}
		$out['name']    = sanitize_text_field( $out['name'] );
		$out['phone']   = preg_replace( '/[^0-9+]/', '', $out['phone'] );
		$out['email']   = sanitize_email( $out['email'] );
		$out['goal']    = sanitize_text_field( $out['goal'] );
		$out['message'] = sanitize_textarea_field( $out['message'] );
		$out['source']  = sanitize_text_field( $out['source'] );
		return $out;
	}
}

if ( ! function_exists( 'nadlan_lead_routing_log' ) ) {
	function nadlan_lead_routing_log( $entry ) {
		$entry = wp_parse_args( (array) $entry, array(
			't'        => time(),
			'lead_id'  => 0,
			'card_id'  => 0,
			'owner_id' => 0,
			'tier'     => '',
			'status'   => '',
			'reason'   => '',
			'context'  => '',
		) );
		$entry['t']        = (int) $entry['t'];
		$entry['lead_id']  = (int) $entry['lead_id'];
		$entry['card_id']  = (int) $entry['card_id'];
		$entry['owner_id'] = (int) $entry['owner_id'];
		$entry['tier']     = sanitize_key( (string) $entry['tier'] );
		$entry['status']   = sanitize_key( (string) $entry['status'] );
		$entry['reason']   = sanitize_key( (string) $entry['reason'] );
		$entry['context']  = sanitize_key( (string) $entry['context'] );

		$log = get_option( 'nadlan_lead_log', array() );
		if ( ! is_array( $log ) ) { $log = array(); }
		array_unshift( $log, $entry );
		update_option( 'nadlan_lead_log', array_slice( $log, 0, 500 ), false );
	}
}

if ( ! function_exists( 'nadlan_lead_route_mark' ) ) {
	function nadlan_lead_route_mark( $lead_id, $card_id, $owner_id, $tier, $status, $reason, $context ) {
		$lead_id = (int) $lead_id;
		if ( $lead_id > 0 ) {
			update_post_meta( $lead_id, 'lead_route_attempted', 1 );
			update_post_meta( $lead_id, 'lead_route_attempted_at', time() );
			update_post_meta( $lead_id, 'lead_route_status', sanitize_key( $status ) );
			update_post_meta( $lead_id, 'lead_route_reason', sanitize_key( $reason ) );
			update_post_meta( $lead_id, 'lead_routed_to_owner', $status === 'delivered_owner' ? 1 : 0 );
			if ( $owner_id > 0 ) {
				update_post_meta( $lead_id, 'lead_routed_owner_user_id', (int) $owner_id );
			}
			if ( $status === 'delivered_owner' ) {
				update_post_meta( $lead_id, 'lead_routed_at', time() );
			}
		}
		nadlan_lead_routing_log( array(
			'lead_id'  => $lead_id,
			'card_id'  => (int) $card_id,
			'owner_id' => (int) $owner_id,
			'tier'     => (string) $tier,
			'status'   => (string) $status,
			'reason'   => (string) $reason,
			'context'  => (string) $context,
		) );
	}
}

if ( ! function_exists( 'nadlan_lead_route_email_body' ) ) {
	function nadlan_lead_route_email_body( $owner_id, $lead_id, $card_id, $fields ) {
		$card_title = get_the_title( (int) $card_id );
		$card_url   = get_permalink( (int) $card_id );
		$center_url = home_url( '/advertiser-center/' );
		$lines = array(
			'שלום,',
			'התקבלה פנייה חדשה דרך הכרטיס שלכם: ' . $card_title,
			'',
			'שם: ' . $fields['name'],
		);
		if ( $fields['phone'] !== '' ) { $lines[] = 'טלפון: ' . $fields['phone']; }
		if ( $fields['email'] !== '' ) { $lines[] = 'אימייל: ' . $fields['email']; }
		if ( $fields['goal'] !== '' ) { $lines[] = 'נושא: ' . $fields['goal']; }
		if ( ! empty( $fields['unit'] ) || ! empty( $fields['floor'] ) || ! empty( $fields['advisor'] ) ) {
			$lines[] = '';
			$lines[] = 'פרטי בחירת דירה:';
			if ( ! empty( $fields['unit'] ) ) { $lines[] = 'דירה/קו: ' . $fields['unit']; }
			if ( ! empty( $fields['building'] ) ) { $lines[] = 'בניין: ' . $fields['building']; }
			if ( ! empty( $fields['floor'] ) ) { $lines[] = 'קומה: ' . $fields['floor']; }
			if ( ! empty( $fields['rooms'] ) ) { $lines[] = 'חדרים: ' . $fields['rooms']; }
			if ( ! empty( $fields['sqm'] ) ) { $lines[] = 'שטח: ' . $fields['sqm']; }
			if ( ! empty( $fields['availability'] ) ) { $lines[] = 'זמינות: ' . $fields['availability']; }
			if ( ! empty( $fields['market_note'] ) ) { $lines[] = 'נתוני שוק: ' . $fields['market_note']; }
			if ( ! empty( $fields['timeline'] ) ) { $lines[] = 'מועד התקדמות: ' . $fields['timeline']; }
			if ( ! empty( $fields['advisor'] ) ) { $lines[] = 'ליווי מבוקש: ' . $fields['advisor']; }
			if ( ! empty( $fields['purchase_intent'] ) ) { $lines[] = 'סוג פנייה: בדיקת רכישה לא מחייבת'; }
		}
		if ( $fields['message'] !== '' ) {
			$lines[] = '';
			$lines[] = 'הודעה:';
			$lines[] = $fields['message'];
		}
		$lines[] = '';
		$lines[] = 'הכרטיס: ' . $card_url;
		$lines[] = 'כל הפניות שלכם: ' . $center_url;
		$lines[] = '';
		$lines[] = 'כדאי לחזור ללקוח בהקדם ולסמן לעצמכם את איכות הפנייה.';
		$lines[] = 'נדל״ן חכם';
		return implode( "\n", $lines );
	}
}

if ( ! function_exists( 'nadlan_lead_route' ) ) {
	function nadlan_lead_route( $lead_id, $card_id, $fields = array(), $context = 'rest' ) {
		$lead_id = (int) $lead_id;
		$card_id = (int) $card_id;
		$context = sanitize_key( (string) $context );
		if ( $context === '' ) { $context = 'rest'; }

		$lead = $lead_id > 0 ? get_post( $lead_id ) : null;
		if ( ! $lead || $lead->post_type !== 'nadlan_lead' ) {
			return array( 'ok' => false, 'status' => 'invalid_lead' );
		}
		if ( ! add_post_meta( $lead_id, 'lead_route_attempted', 1, true ) ) {
			$status = (string) get_post_meta( $lead_id, 'lead_route_status', true );
			return array( 'ok' => true, 'status' => $status !== '' ? $status : 'routing', 'idempotent' => true );
		}
		update_post_meta( $lead_id, 'lead_route_status', 'routing' );
		update_post_meta( $lead_id, 'lead_route_attempted_at', time() );

		$fields = nadlan_lead_route_fields( $lead_id, $fields );
		if ( $card_id <= 0 ) {
			nadlan_lead_route_mark( $lead_id, 0, 0, '', 'fallback_admin', 'no_card', $context );
			return array( 'ok' => true, 'status' => 'fallback_admin', 'reason' => 'no_card' );
		}

		$card = get_post( $card_id );
		if ( ! $card || ! in_array( $card->post_type, nadlan_lead_route_card_types(), true ) ) {
			nadlan_lead_route_mark( $lead_id, $card_id, 0, '', 'fallback_admin', 'invalid_card', $context );
			return array( 'ok' => true, 'status' => 'fallback_admin', 'reason' => 'invalid_card' );
		}

		$owner_id = (int) get_post_meta( $card_id, 'owner_user_id', true );
		$tier     = (string) get_post_meta( $card_id, 'paid_tier', true );
		if ( $tier === '' ) { $tier = 'free'; }

		if ( $owner_id < 1 ) {
			nadlan_lead_route_mark( $lead_id, $card_id, 0, $tier, 'fallback_admin', 'unclaimed_card', $context );
			return array( 'ok' => true, 'status' => 'fallback_admin', 'reason' => 'unclaimed_card' );
		}
		if ( ! in_array( $tier, nadlan_lead_route_paid_tiers(), true ) ) {
			nadlan_lead_route_mark( $lead_id, $card_id, $owner_id, $tier, 'fallback_admin', 'free_tier', $context );
			return array( 'ok' => true, 'status' => 'fallback_admin', 'reason' => 'free_tier' );
		}
		$requester_id = get_current_user_id();
		if ( $requester_id > 0 && $owner_id === (int) $requester_id ) {
			nadlan_lead_route_mark( $lead_id, $card_id, $owner_id, $tier, 'skipped_self', 'self_submission', $context );
			return array( 'ok' => true, 'status' => 'skipped_self', 'reason' => 'self_submission' );
		}

		$owner = get_userdata( $owner_id );
		if ( ! $owner || ! is_email( $owner->user_email ) ) {
			nadlan_lead_route_mark( $lead_id, $card_id, $owner_id, $tier, 'fallback_admin', 'owner_unavailable', $context );
			return array( 'ok' => true, 'status' => 'fallback_admin', 'reason' => 'owner_unavailable' );
		}

		$body    = nadlan_lead_route_email_body( $owner_id, $lead_id, $card_id, $fields );
		$subject = 'פנייה חדשה לכרטיס שלך | נדל״ן חכם';
		$headers = array( 'Content-Type: text/plain; charset=UTF-8' );
		$delivered = apply_filters( 'nadlan_lead_deliver', false, $owner_id, $lead_id, $card_id, $body, $fields, $headers );
		if ( is_wp_error( $delivered ) ) {
			update_post_meta( $lead_id, 'lead_route_last_error', $delivered->get_error_code() );
			$delivered = false;
		}
		if ( ! $delivered ) {
			$delivered = wp_mail( $owner->user_email, $subject, $body, $headers );
		}

		if ( $delivered ) {
			nadlan_lead_route_mark( $lead_id, $card_id, $owner_id, $tier, 'delivered_owner', 'email', $context );
			update_post_meta( $lead_id, 'lead_route_channel', 'email' );
			return array( 'ok' => true, 'status' => 'delivered_owner' );
		}

		nadlan_lead_route_mark( $lead_id, $card_id, $owner_id, $tier, 'failed_email', 'wp_mail_false', $context );
		update_post_meta( $lead_id, 'lead_route_last_error', 'wp_mail_false' );
		return array( 'ok' => false, 'status' => 'failed_email' );
	}
}

if ( ! function_exists( 'nadlan_lead_routing_stats' ) ) {
	function nadlan_lead_routing_stats( $days = 7 ) {
		$since = time() - max( 1, (int) $days ) * DAY_IN_SECONDS;
		$stats = array(
			'attempted' => 0,
			'routed'   => 0,
			'fallback' => 0,
			'failed'   => 0,
			'last'     => array(),
		);
		$log = get_option( 'nadlan_lead_log', array() );
		if ( ! is_array( $log ) ) { return $stats; }
		foreach ( $log as $row ) {
			$t = isset( $row['t'] ) ? (int) $row['t'] : 0;
			if ( $t < $since ) { continue; }
			$status = isset( $row['status'] ) ? (string) $row['status'] : '';
			$stats['attempted']++;
			if ( $status === 'delivered_owner' ) { $stats['routed']++; }
			if ( $status === 'fallback_admin' || $status === 'skipped_self' ) { $stats['fallback']++; }
			if ( strpos( $status, 'failed_' ) === 0 ) { $stats['failed']++; }
			if ( ! $stats['last'] ) { $stats['last'] = $row; }
		}
		return $stats;
	}
}

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['lead_routing'] = array(
		'loaded'       => true,
		'log_entries'  => count( (array) get_option( 'nadlan_lead_log', array() ) ),
		'last_7_days'  => nadlan_lead_routing_stats( 7 ),
	);
	return $out;
} );
