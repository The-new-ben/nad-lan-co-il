<?php
/**
 * nadlan-config - lead end-to-end flow (v1.53.0).
 *
 * Ships dark behind nadlan_feature_lead_e2e. When the flag is off, existing
 * conversion-cta/admin-post lead behavior remains untouched.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_lead_e2e_enabled' ) ) {
	function nadlan_lead_e2e_enabled() {
		return (bool) apply_filters( 'nadlan_lead_e2e_enabled', get_option( 'nadlan_feature_lead_e2e', '0' ) === '1' );
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_valid_statuses' ) ) {
	function nadlan_lead_e2e_valid_statuses() {
		return array( 'new', 'contacted', 'won', 'lost' );
	}
}

add_filter( 'nadlan_lead_route_paid_tiers', function ( $tiers ) {
	if ( ! nadlan_lead_e2e_enabled() ) { return $tiers; }
	return array_values( array_unique( array_merge( (array) $tiers, array( 'project premier', 'property pro' ) ) ) );
} );

if ( ! function_exists( 'nadlan_lead_e2e_status_label' ) ) {
	function nadlan_lead_e2e_status_label( $status ) {
		$labels = array(
			'new'       => 'חדשה',
			'contacted' => 'נוצר קשר',
			'won'       => 'נסגרה בהצלחה',
			'lost'      => 'לא נסגרה',
		);
		$status = sanitize_key( (string) $status );
		return isset( $labels[ $status ] ) ? $labels[ $status ] : $labels['new'];
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_default_ack_message' ) ) {
	function nadlan_lead_e2e_default_ack_message() {
		return "שלום {{name}},\n\nקיבלנו את פנייתך לגבי {{card}} בנדלן חכם. נציג יחזור אליך בתוך 24 שעות.\n\nכדי שנוכל לעזור מהר יותר, אפשר להשיב למייל הזה עם מסגרת התקציב והאם זה רלוונטי לחודש הקרוב או מאוחר יותר.\n\n{{site}}";
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_ack_message' ) ) {
	function nadlan_lead_e2e_ack_message() {
		$msg = (string) get_option( 'nadlan_lead_ack_message', '' );
		return $msg !== '' ? $msg : nadlan_lead_e2e_default_ack_message();
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_clean_fields' ) ) {
	function nadlan_lead_e2e_clean_fields( $fields ) {
		$fields = (array) $fields;
		$out = array(
			'name'         => sanitize_text_field( (string) ( $fields['name'] ?? '' ) ),
			'phone'        => preg_replace( '/[^0-9+]/', '', (string) ( $fields['phone'] ?? '' ) ),
			'email'        => sanitize_email( (string) ( $fields['email'] ?? '' ) ),
			'goal'         => sanitize_text_field( (string) ( $fields['goal'] ?? '' ) ),
			'city'         => sanitize_text_field( (string) ( $fields['city'] ?? '' ) ),
			'budget'       => sanitize_text_field( (string) ( $fields['budget'] ?? '' ) ),
			'timeline'     => sanitize_text_field( (string) ( $fields['timeline'] ?? '' ) ),
			'unit'         => sanitize_text_field( (string) ( $fields['unit'] ?? '' ) ),
			'floor'        => isset( $fields['floor'] ) && $fields['floor'] !== '' ? (int) $fields['floor'] : '',
			'rooms'        => sanitize_text_field( (string) ( $fields['rooms'] ?? '' ) ),
			'sqm'          => sanitize_text_field( (string) ( $fields['sqm'] ?? '' ) ),
			'advisor'      => sanitize_key( (string) ( $fields['advisor'] ?? '' ) ),
			'purchase_intent'   => ! empty( $fields['purchase_intent'] ) ? 1 : '',
			'reservation_state' => sanitize_key( (string) ( $fields['reservation_state'] ?? '' ) ),
			'view_bearing'      => isset( $fields['view_bearing'] ) && $fields['view_bearing'] !== '' ? (float) $fields['view_bearing'] : '',
			'view_altitude_m'   => isset( $fields['view_altitude_m'] ) && $fields['view_altitude_m'] !== '' ? (float) $fields['view_altitude_m'] : '',
			'message'      => sanitize_textarea_field( (string) ( $fields['message'] ?? '' ) ),
			'source_url'   => esc_url_raw( (string) ( $fields['source_url'] ?? '' ) ),
			'utm_source'   => sanitize_text_field( (string) ( $fields['utm_source'] ?? ( $fields['source'] ?? '' ) ) ),
			'utm_campaign' => sanitize_text_field( (string) ( $fields['utm_campaign'] ?? '' ) ),
		);
		return $out;
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_fingerprint_base' ) ) {
	function nadlan_lead_e2e_fingerprint_base( $card_id, $fields ) {
		$contact = strtolower( trim( (string) $fields['email'] ) ) . '|' . preg_replace( '/[^0-9+]/', '', (string) $fields['phone'] );
		$name = strtolower( trim( (string) $fields['name'] ) );
		return md5( (int) $card_id . '|' . $contact . '|' . $name );
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_guard_keys' ) ) {
	function nadlan_lead_e2e_guard_keys( $card_id, $fields, $now = null ) {
		$now = $now ? (int) $now : time();
		$window = max( 300, (int) get_option( 'nadlan_lead_e2e_idempotency_window', 15 * MINUTE_IN_SECONDS ) );
		$bucket = (int) floor( $now / $window );
		$base = nadlan_lead_e2e_fingerprint_base( $card_id, $fields );
		return array(
			'nadlan_lead_e2e_guard_' . md5( $base . '|' . $bucket ),
			'nadlan_lead_e2e_guard_' . md5( $base . '|' . ( $bucket - 1 ) ),
		);
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_find_duplicate' ) ) {
	function nadlan_lead_e2e_find_duplicate( $guard_keys ) {
		foreach ( (array) $guard_keys as $key ) {
			$value = get_option( $key, '' );
			if ( is_numeric( $value ) && (int) $value > 0 && get_post_type( (int) $value ) === 'nadlan_lead' ) {
				return (int) $value;
			}
		}
		return 0;
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_acquire_guard' ) ) {
	function nadlan_lead_e2e_acquire_guard( $guard_keys ) {
		$guard_keys = array_values( (array) $guard_keys );
		$primary = isset( $guard_keys[0] ) ? (string) $guard_keys[0] : '';
		if ( $primary === '' ) {
			return false;
		}
		return add_option( $primary, 'pending:' . time(), '', false ) ? $primary : false;
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_complete_guard' ) ) {
	function nadlan_lead_e2e_complete_guard( $guard_key, $lead_id ) {
		if ( $guard_key === '' || (int) $lead_id <= 0 ) {
			return;
		}
		update_option( $guard_key, (int) $lead_id, false );
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_admin_email' ) ) {
	function nadlan_lead_e2e_admin_email() {
		return sanitize_email( get_option( 'admin_email' ) );
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_notify_admin' ) ) {
	function nadlan_lead_e2e_notify_admin( $lead_id, $card_id, $fields, $reason = 'fallback' ) {
		$admin = nadlan_lead_e2e_admin_email();
		if ( ! $admin ) { return false; }
		$card_title = $card_id ? get_the_title( (int) $card_id ) : '';
		$lines = array(
			'פנייה חדשה לטיפול מנהל',
			'',
			'סיבה: ' . sanitize_key( $reason ),
			'מזהה פנייה: ' . (int) $lead_id,
			'כרטיס: ' . ( $card_title !== '' ? $card_title . ' (#' . (int) $card_id . ')' : 'אין' ),
			'שם: ' . $fields['name'],
			'טלפון: ' . $fields['phone'],
			'אימייל: ' . $fields['email'],
			'נושא: ' . $fields['goal'],
			'מקור: ' . ( $fields['source_url'] ?: $fields['utm_source'] ),
			'',
			'הודעה:',
			$fields['message'],
			'',
			'ניהול: ' . admin_url( 'post.php?post=' . (int) $lead_id . '&action=edit' ),
		);
		$sent = wp_mail( $admin, 'פנייה חדשה לטיפול מנהל #' . (int) $lead_id, implode( "\n", $lines ) );
		if ( $sent ) {
			update_post_meta( $lead_id, 'lead_e2e_admin_notified_at', time() );
		}
		update_post_meta( $lead_id, 'lead_e2e_fallback_reason', sanitize_key( $reason ) );
		update_post_meta( $lead_id, 'lead_e2e_fallback_admin', 1 );
		return (bool) $sent;
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_send_ack' ) ) {
	function nadlan_lead_e2e_send_ack( $lead_id, $card_id, $fields ) {
		$lead_id = (int) $lead_id;
		if ( $lead_id <= 0 ) { return false; }
		if ( (int) get_post_meta( $lead_id, 'ack_sent_at', true ) > 0 ) {
			return true;
		}
		$email = sanitize_email( (string) $fields['email'] );
		if ( ! is_email( $email ) ) {
			update_post_meta( $lead_id, 'lead_ack_status', 'no_email' );
			return false;
		}
		$replacements = array(
			'{{name}}'  => $fields['name'] !== '' ? $fields['name'] : 'שלום',
			'{{card}}'  => $card_id && get_the_title( (int) $card_id ) !== '' ? get_the_title( (int) $card_id ) : 'פנייתך',
			'{{site}}'  => get_bloginfo( 'name' ),
			'{{url}}'   => home_url( '/' ),
		);
		$body = strtr( nadlan_lead_e2e_ack_message(), $replacements );
		$subject = (string) get_option( 'nadlan_lead_ack_subject', 'הפנייה שלך התקבלה בנדלן חכם' );
		$headers = array( 'Content-Type: text/plain; charset=UTF-8' );
		$ack_fields = $fields;
		$ack_fields['_delivery_context'] = 'visitor_ack';
		$ack_fields['_recipient_email'] = $email;
		$delivered = apply_filters( 'nadlan_lead_deliver', false, 0, $lead_id, (int) $card_id, $body, $ack_fields, $headers );
		if ( is_wp_error( $delivered ) ) {
			update_post_meta( $lead_id, 'lead_ack_last_error', $delivered->get_error_code() );
			$delivered = false;
		}
		if ( ! $delivered ) {
			$delivered = wp_mail( $email, $subject, $body, $headers );
		}
		if ( $delivered && add_post_meta( $lead_id, 'ack_sent_at', time(), true ) ) {
			update_post_meta( $lead_id, 'lead_ack_status', 'sent' );
			update_post_meta( $lead_id, 'lead_ack_channel', 'email' );
			do_action( 'nadlan_lead_ack', $lead_id, array(
				'card_id' => (int) $card_id,
				'channel' => 'email',
			) );
			return true;
		}
		update_post_meta( $lead_id, 'lead_ack_status', 'failed' );
		return false;
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_capture' ) ) {
	function nadlan_lead_e2e_capture( $fields, $card_id = 0, $context = 'rest' ) {
		if ( ! nadlan_lead_e2e_enabled() ) {
			return new WP_Error( 'lead_e2e_disabled', 'lead_e2e_disabled', array( 'status' => 404 ) );
		}
		$fields = nadlan_lead_e2e_clean_fields( $fields );
		$card_id = function_exists( 'nadlan_config_valid_lead_card_id' ) ? nadlan_config_valid_lead_card_id( $card_id ) : absint( $card_id );
		$context = sanitize_key( (string) $context );
		if ( $fields['name'] === '' || ( $fields['phone'] === '' && $fields['email'] === '' ) ) {
			return new WP_Error( 'invalid', 'נדרשים שם וטלפון או אימייל.', array( 'status' => 422 ) );
		}

		$guard_keys = nadlan_lead_e2e_guard_keys( $card_id, $fields );
		$duplicate_id = nadlan_lead_e2e_find_duplicate( $guard_keys );
		if ( $duplicate_id ) {
			return array(
				'ok'         => true,
				'lead_id'    => $duplicate_id,
				'idempotent' => true,
				'status'     => (string) get_post_meta( $duplicate_id, 'lead_route_status', true ),
			);
		}
		$guard_key = nadlan_lead_e2e_acquire_guard( $guard_keys );
		if ( ! $guard_key ) {
			$duplicate_id = nadlan_lead_e2e_find_duplicate( $guard_keys );
			if ( $duplicate_id ) {
				return array( 'ok' => true, 'lead_id' => $duplicate_id, 'idempotent' => true );
			}
			return new WP_Error( 'duplicate_pending', 'הפנייה כבר נקלטת.', array( 'status' => 409 ) );
		}

		$title = ( $fields['name'] !== '' ? $fields['name'] : 'Lead' ) . ' - ' . ( $fields['goal'] !== '' ? $fields['goal'] : 'General' ) . ' - ' . current_time( 'Y-m-d H:i' );
		$lead_id = wp_insert_post( array(
			'post_type'    => 'nadlan_lead',
			'post_status'  => 'private',
			'post_title'   => $title,
			'post_content' => $fields['message'],
		), true );
		if ( is_wp_error( $lead_id ) ) {
			delete_option( $guard_key );
			return $lead_id;
		}

		foreach ( $fields as $k => $v ) {
			if ( $v !== '' ) {
				update_post_meta( $lead_id, $k, $v );
			}
		}
		if ( $card_id ) {
			update_post_meta( $lead_id, 'lead_card_id', (int) $card_id );
		}
		update_post_meta( $lead_id, 'lead_status', 'new' );
		update_post_meta( $lead_id, 'lead_e2e_enabled', 1 );
		update_post_meta( $lead_id, 'lead_e2e_context', $context );
		update_post_meta( $lead_id, 'lead_e2e_created_at', time() );
		nadlan_lead_e2e_audit( array(
			'lead_id' => $lead_id,
			'card_id' => $card_id,
			'user_id' => 0,
			'old'     => 'created',
			'new'     => 'new',
		) );

		$route = function_exists( 'nadlan_lead_route' ) ? nadlan_lead_route( $lead_id, $card_id, $fields, $context ) : array( 'ok' => false, 'status' => 'fallback_admin', 'reason' => 'router_missing' );
		$route_status = is_array( $route ) ? sanitize_key( (string) ( $route['status'] ?? '' ) ) : '';
		if ( $route_status !== 'delivered_owner' ) {
			$reason = is_array( $route ) ? sanitize_key( (string) ( $route['reason'] ?? $route_status ) ) : 'route_unknown';
			nadlan_lead_e2e_notify_admin( $lead_id, $card_id, $fields, $reason );
		}

		$ack_sent = nadlan_lead_e2e_send_ack( $lead_id, $card_id, $fields );
		nadlan_lead_e2e_complete_guard( $guard_key, $lead_id );
		if ( function_exists( 'nadlan_log_event' ) ) {
			nadlan_log_event( 'lead_e2e', 'capture', 'ok', array(
				'lead_ref'     => (int) $lead_id,
				'listing_ref'  => (int) $card_id,
				'route_status' => $route_status,
				'ack'          => $ack_sent ? 'sent' : 'not_sent',
			) );
		}
		do_action( 'nadlan_lead_e2e_captured', (int) $lead_id, (int) $card_id, $fields, $route );
		return array(
			'ok'           => true,
			'lead_id'      => (int) $lead_id,
			'route_status' => $route_status,
			'ack_sent'     => (bool) $ack_sent,
		);
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_audit' ) ) {
	function nadlan_lead_e2e_audit( $entry ) {
		$entry = wp_parse_args( (array) $entry, array(
			't'       => time(),
			'lead_id' => 0,
			'card_id' => 0,
			'user_id' => 0,
			'old'     => '',
			'new'     => '',
			'note'    => '',
		) );
		$row = array(
			't'            => (int) $entry['t'],
			'lead_id'      => (int) $entry['lead_id'],
			'card_id'      => (int) $entry['card_id'],
			'user_id'      => (int) $entry['user_id'],
			'old_status'   => sanitize_key( (string) $entry['old'] ),
			'new_status'   => sanitize_key( (string) $entry['new'] ),
			'note_present' => (string) $entry['note'] !== '' ? 1 : 0,
			'note_length'  => min( 5000, strlen( (string) $entry['note'] ) ),
		);
		$log = get_option( 'nadlan_lead_audit', array() );
		if ( ! is_array( $log ) ) { $log = array(); }
		array_unshift( $log, $row );
		update_option( 'nadlan_lead_audit', array_slice( $log, 0, 1000 ), false );
		return $row;
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_user_can_manage_lead' ) ) {
	function nadlan_lead_e2e_user_can_manage_lead( $lead_id, $user_id = 0 ) {
		$lead_id = absint( $lead_id );
		$user_id = $user_id ? absint( $user_id ) : get_current_user_id();
		if ( ! $lead_id || ! $user_id || get_post_type( $lead_id ) !== 'nadlan_lead' ) { return false; }
		if ( current_user_can( 'manage_options' ) ) { return true; }
		$card_id = (int) get_post_meta( $lead_id, 'lead_card_id', true );
		if ( ! $card_id ) { return false; }
		$owner_id = (int) get_post_meta( $card_id, 'owner_user_id', true );
		if ( $owner_id !== $user_id ) { return false; }
		$tier = (string) get_post_meta( $card_id, 'paid_tier', true );
		if ( function_exists( 'nadlan_lead_route_paid_tiers' ) && ! in_array( $tier, nadlan_lead_route_paid_tiers(), true ) ) {
			return false;
		}
		return current_user_can( 'edit_post', $card_id );
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_response_minutes' ) ) {
	function nadlan_lead_e2e_response_minutes( $lead_id ) {
		$first = (int) get_post_meta( (int) $lead_id, 'lead_first_response_at', true );
		if ( $first <= 0 ) { return null; }
		$created = get_post_time( 'U', true, (int) $lead_id );
		if ( ! $created ) { $created = (int) get_post_meta( (int) $lead_id, 'lead_e2e_created_at', true ); }
		if ( ! $created || $first < $created ) { return null; }
		return round( ( $first - $created ) / MINUTE_IN_SECONDS, 1 );
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_response_label' ) ) {
	function nadlan_lead_e2e_response_label( $lead_id ) {
		$minutes = nadlan_lead_e2e_response_minutes( $lead_id );
		if ( $minutes === null ) { return 'ממתינה לתגובה ראשונה'; }
		if ( $minutes < 60 ) { return number_format_i18n( $minutes, 1 ) . ' דקות'; }
		return number_format_i18n( $minutes / 60, 1 ) . ' שעות';
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/lead/status', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return is_user_logged_in(); },
		'callback'            => 'nadlan_lead_e2e_rest_status',
	) );
} );

if ( ! function_exists( 'nadlan_lead_e2e_rest_status' ) ) {
	function nadlan_lead_e2e_rest_status( WP_REST_Request $req ) {
		if ( ! nadlan_lead_e2e_enabled() ) {
			return new WP_Error( 'lead_e2e_disabled', 'lead_e2e_disabled', array( 'status' => 404 ) );
		}
		$nonce = (string) $req->get_header( 'x_wp_nonce' );
		if ( $nonce === '' ) { $nonce = (string) $req->get_param( '_wpnonce' ); }
		if ( $nonce === '' || ! wp_verify_nonce( $nonce, 'wp_rest' ) ) {
			return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
		}
		$lead_id = absint( $req->get_param( 'lead_id' ) );
		$new = sanitize_key( (string) $req->get_param( 'status' ) );
		$note = sanitize_textarea_field( (string) $req->get_param( 'note' ) );
		if ( ! in_array( $new, nadlan_lead_e2e_valid_statuses(), true ) ) {
			return new WP_Error( 'invalid_status', 'invalid_status', array( 'status' => 422 ) );
		}
		if ( ! nadlan_lead_e2e_user_can_manage_lead( $lead_id ) ) {
			return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
		}
		$old = sanitize_key( (string) get_post_meta( $lead_id, 'lead_status', true ) );
		if ( $old === '' ) { $old = 'new'; }
		$card_id = (int) get_post_meta( $lead_id, 'lead_card_id', true );
		if ( (int) get_post_meta( $lead_id, 'lead_first_response_at', true ) <= 0 && $new !== 'new' ) {
			update_post_meta( $lead_id, 'lead_first_response_at', time() );
			update_post_meta( $lead_id, 'lead_first_response_user_id', get_current_user_id() );
		}
		if ( $note !== '' ) {
			update_post_meta( $lead_id, 'lead_private_note', $note );
			update_post_meta( $lead_id, 'lead_private_note_updated_at', time() );
		}
		if ( $new !== $old ) {
			update_post_meta( $lead_id, 'lead_status', $new );
			nadlan_lead_e2e_audit( array(
				'lead_id' => $lead_id,
				'card_id' => $card_id,
				'user_id' => get_current_user_id(),
				'old'     => $old,
				'new'     => $new,
				'note'    => $note,
			) );
			if ( in_array( $new, array( 'contacted', 'won' ), true ) ) {
				do_action( 'nadlan_lead_qualified', $lead_id, $new, get_current_user_id() );
			}
		}
		return array(
			'ok'               => true,
			'lead_id'          => $lead_id,
			'old_status'       => $old,
			'new_status'       => $new,
			'label'            => nadlan_lead_e2e_status_label( $new ),
			'response_minutes' => nadlan_lead_e2e_response_minutes( $lead_id ),
		);
	}
}

if ( ! function_exists( 'nadlan_lead_e2e_metrics' ) ) {
	function nadlan_lead_e2e_metrics( $days = 7 ) {
		$days = max( 1, (int) $days );
		$since = time() - $days * DAY_IN_SECONDS;
		$q = new WP_Query( array(
			'post_type'      => 'nadlan_lead',
			'post_status'    => 'any',
			'fields'         => 'ids',
			'posts_per_page' => 500,
			'orderby'        => 'date',
			'order'          => 'DESC',
			'date_query'     => array( array( 'after' => gmdate( 'Y-m-d H:i:s', $since ), 'inclusive' => true ) ),
			'meta_query'     => array( array( 'key' => 'lead_e2e_enabled', 'value' => 1, 'type' => 'NUMERIC' ) ),
		) );
		$out = array(
			'enabled'              => nadlan_lead_e2e_enabled(),
			'leads_7d'             => 0,
			'delivered_7d'         => 0,
			'ack_sent_7d'          => 0,
			'ack_rate'             => null,
			'avg_response_minutes' => null,
			'fallback_7d'          => 0,
			'by_status'            => array_fill_keys( nadlan_lead_e2e_valid_statuses(), 0 ),
			'audit_entries'        => count( (array) get_option( 'nadlan_lead_audit', array() ) ),
		);
		$response_minutes = array();
		foreach ( (array) $q->posts as $lead_id ) {
			$out['leads_7d']++;
			$status = sanitize_key( (string) get_post_meta( $lead_id, 'lead_status', true ) );
			if ( $status === '' ) { $status = 'new'; }
			if ( ! isset( $out['by_status'][ $status ] ) ) { $out['by_status'][ $status ] = 0; }
			$out['by_status'][ $status ]++;
			if ( (string) get_post_meta( $lead_id, 'lead_route_status', true ) === 'delivered_owner' ) { $out['delivered_7d']++; }
			if ( (int) get_post_meta( $lead_id, 'ack_sent_at', true ) > 0 ) { $out['ack_sent_7d']++; }
			if ( (int) get_post_meta( $lead_id, 'lead_e2e_fallback_admin', true ) > 0 ) { $out['fallback_7d']++; }
			$minutes = nadlan_lead_e2e_response_minutes( $lead_id );
			if ( $minutes !== null ) { $response_minutes[] = (float) $minutes; }
		}
		$out['ack_rate'] = $out['leads_7d'] > 0 ? round( $out['ack_sent_7d'] / $out['leads_7d'], 3 ) : null;
		$out['delivery_rate'] = $out['leads_7d'] > 0 ? round( $out['delivered_7d'] / $out['leads_7d'], 3 ) : null;
		$out['avg_response_minutes'] = $response_minutes ? round( array_sum( $response_minutes ) / count( $response_minutes ), 1 ) : null;
		return $out;
	}
}

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['lead_e2e'] = nadlan_lead_e2e_metrics( 7 );
	return $out;
} );

add_filter( 'nadlan_metrics_snapshot', function ( $snapshot ) {
	$metrics = nadlan_lead_e2e_metrics( 7 );
	$snapshot['lead_e2e'] = $metrics;
	$snapshot['lead_ack_rate_7d'] = $metrics['ack_rate'];
	$snapshot['lead_avg_response_minutes_7d'] = $metrics['avg_response_minutes'];
	return $snapshot;
} );

if ( ! function_exists( 'nadlan_lead_e2e_render_ops_panel' ) ) {
	function nadlan_lead_e2e_render_ops_panel() {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		$m = nadlan_lead_e2e_metrics( 7 );
		?>
		<h2 style="margin-top:28px">Lead E2E</h2>
		<p class="description">בדיקת מסלול הפנייה המלא: קליטה, מסירה, אישור ללקוח, תגובה וסטטוס.</p>
		<div class="nlops-grid">
			<div class="nlops-card">
				<h2>מצב</h2>
				<div class="nlops-row"><span>דגל הפעלה</span><strong><?php echo $m['enabled'] ? 'ON' : 'OFF'; ?></strong></div>
				<div class="nlops-row"><span>פניות 7 ימים</span><strong><?php echo (int) $m['leads_7d']; ?></strong></div>
				<div class="nlops-row"><span>נמסרו 7 ימים</span><strong><?php echo (int) $m['delivered_7d']; ?></strong></div>
				<div class="nlops-row"><span>אישור ללקוח</span><strong><?php echo esc_html( $m['ack_rate'] === null ? 'אין נתונים' : number_format_i18n( $m['ack_rate'] * 100, 1 ) . '%' ); ?></strong></div>
				<div class="nlops-row"><span>תגובה ממוצעת</span><strong><?php echo esc_html( $m['avg_response_minutes'] === null ? 'אין נתונים' : number_format_i18n( $m['avg_response_minutes'], 1 ) . ' דקות' ); ?></strong></div>
			</div>
		</div>
		<?php
	}
}
add_action( 'nadlan_ops_after_grid', 'nadlan_lead_e2e_render_ops_panel', 35 );

add_filter( 'nadlan_hardening_public_post_routes', function ( $routes ) {
	$routes[] = '#^/nadlan/v1/lead/status$#';
	return $routes;
} );

add_action( 'admin_menu', function () {
	add_options_page( 'NadLan Lead E2E', 'NadLan Lead E2E', 'manage_options', 'nadlan-lead-e2e', 'nadlan_lead_e2e_settings_page' );
} );

if ( ! function_exists( 'nadlan_lead_e2e_settings_page' ) ) {
	function nadlan_lead_e2e_settings_page() {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		if ( ! empty( $_POST['nadlan_lead_e2e_save'] ) && check_admin_referer( 'nadlan_lead_e2e_save' ) ) {
			update_option( 'nadlan_feature_lead_e2e', ! empty( $_POST['nadlan_feature_lead_e2e'] ) ? '1' : '0', false );
			$msg = isset( $_POST['nadlan_lead_ack_message'] ) ? sanitize_textarea_field( wp_unslash( $_POST['nadlan_lead_ack_message'] ) ) : '';
			update_option( 'nadlan_lead_ack_message', $msg, false );
			$subject = isset( $_POST['nadlan_lead_ack_subject'] ) ? sanitize_text_field( wp_unslash( $_POST['nadlan_lead_ack_subject'] ) ) : '';
			update_option( 'nadlan_lead_ack_subject', $subject, false );
			echo '<div class="notice notice-success"><p>נשמר.</p></div>';
		}
		$enabled = get_option( 'nadlan_feature_lead_e2e', '0' ) === '1';
		$message = nadlan_lead_e2e_ack_message();
		$subject = (string) get_option( 'nadlan_lead_ack_subject', 'הפנייה שלך התקבלה בנדלן חכם' );
		?>
		<div class="wrap" dir="rtl">
			<h1>NadLan Lead E2E</h1>
			<form method="post">
				<?php wp_nonce_field( 'nadlan_lead_e2e_save' ); ?>
				<table class="form-table" role="presentation">
					<tr>
						<th scope="row">הפעלת מסלול לידים מלא</th>
						<td><label><input type="checkbox" name="nadlan_feature_lead_e2e" value="1" <?php checked( $enabled ); ?>> פעיל</label><p class="description">כבוי כברירת מחדל. כשהוא כבוי, מסלול הלידים הישן נשאר ללא שינוי.</p></td>
					</tr>
					<tr>
						<th scope="row">נושא אישור ללקוח</th>
						<td><input type="text" name="nadlan_lead_ack_subject" value="<?php echo esc_attr( $subject ); ?>" class="regular-text"></td>
					</tr>
					<tr>
						<th scope="row">הודעת אישור ללקוח</th>
						<td><textarea name="nadlan_lead_ack_message" rows="8" class="large-text code"><?php echo esc_textarea( $message ); ?></textarea><p class="description">אפשר להשתמש ב-{{name}}, {{card}}, {{site}}, {{url}}.</p></td>
					</tr>
				</table>
				<p class="submit"><button type="submit" name="nadlan_lead_e2e_save" value="1" class="button button-primary">שמור</button></p>
			</form>
		</div>
		<?php
	}
}
