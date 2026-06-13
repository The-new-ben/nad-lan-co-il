<?php
/**
 * nadlan-config - WhatsApp-to-lead ingestion bridge.
 *
 * This does not scrape WhatsApp and does not require unofficial libraries. It
 * gives the owner a secure bridge for iOS/Android shortcuts, a future Cloud API
 * webhook relay, or a manual operator paste flow so WhatsApp messages enter the
 * same lead CPT, routing, ack, AI and nurture rails as site forms.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_wa_ingest_secret' ) ) {
	function nadlan_wa_ingest_secret() {
		return trim( (string) get_option( 'nadlan_wa_ingest_secret', '' ) );
	}
}

if ( ! function_exists( 'nadlan_wa_ingest_rate_limited' ) ) {
	function nadlan_wa_ingest_rate_limited() {
		$ip = (string) ( $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0' );
		$key = 'nadlan_wa_ingest_rl_' . md5( $ip );
		$count = (int) get_transient( $key );
		if ( $count >= 12 ) {
			return true;
		}
		set_transient( $key, $count + 1, HOUR_IN_SECONDS );
		return false;
	}
}

if ( ! function_exists( 'nadlan_wa_ingest_card_from_text' ) ) {
	function nadlan_wa_ingest_card_from_text( $text, $provided = 0 ) {
		$card_id = function_exists( 'nadlan_config_valid_lead_card_id' ) ? nadlan_config_valid_lead_card_id( absint( $provided ) ) : absint( $provided );
		if ( $card_id ) {
			return $card_id;
		}
		$text = (string) $text;
		if ( preg_match_all( '~https?://[^\s<>"\']+~u', $text, $m ) ) {
			foreach ( $m[0] as $url ) {
				$id = url_to_postid( esc_url_raw( $url ) );
				$id = function_exists( 'nadlan_config_valid_lead_card_id' ) ? nadlan_config_valid_lead_card_id( $id ) : absint( $id );
				if ( $id ) {
					return $id;
				}
			}
		}
		if ( preg_match( '/(?:card_id|lead_card_id|listing|project)[=: #]+(\d+)/i', $text, $m ) ) {
			$id = function_exists( 'nadlan_config_valid_lead_card_id' ) ? nadlan_config_valid_lead_card_id( absint( $m[1] ) ) : absint( $m[1] );
			if ( $id ) {
				return $id;
			}
		}
		return 0;
	}
}

if ( ! function_exists( 'nadlan_wa_ingest_guard_key' ) ) {
	function nadlan_wa_ingest_guard_key( $phone, $message, $card_id ) {
		$bucket = (int) floor( time() / ( 15 * MINUTE_IN_SECONDS ) );
		return 'nadlan_wa_ingest_guard_' . md5( preg_replace( '/[^0-9+]/', '', (string) $phone ) . '|' . (int) $card_id . '|' . wp_strip_all_tags( (string) $message ) . '|' . $bucket );
	}
}

if ( ! function_exists( 'nadlan_wa_ingest_handle' ) ) {
	function nadlan_wa_ingest_handle( WP_REST_Request $req ) {
		$secret = nadlan_wa_ingest_secret();
		if ( $secret === '' ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'not_configured' ), 503 );
		}
		$given = trim( (string) $req->get_header( 'x-nadlan-wa-secret' ) );
		if ( $given === '' || ! hash_equals( $secret, $given ) ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'unauthorized' ), 401 );
		}
		if ( nadlan_wa_ingest_rate_limited() ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'rate_limited' ), 429 );
		}
		$p = $req->get_json_params();
		if ( ! is_array( $p ) ) {
			$p = array();
		}
		$message = sanitize_textarea_field( (string) ( $p['message'] ?? ( $p['text'] ?? '' ) ) );
		$phone   = preg_replace( '/[^0-9+]/', '', (string) ( $p['phone'] ?? ( $p['from'] ?? '' ) ) );
		$email   = sanitize_email( (string) ( $p['email'] ?? '' ) );
		$name    = sanitize_text_field( (string) ( $p['name'] ?? ( $p['contact_name'] ?? '' ) ) );
		if ( $name === '' && $phone !== '' ) {
			$name = 'WhatsApp ' . substr( $phone, -4 );
		}
		$card_id = nadlan_wa_ingest_card_from_text( $message . ' ' . (string) ( $p['url'] ?? '' ), absint( $p['card_id'] ?? 0 ) );
		if ( $message === '' || $name === '' || ( $phone === '' && $email === '' ) ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'invalid', 'message' => 'נדרשים שם, הודעה וטלפון או אימייל.' ), 422 );
		}
		$guard = nadlan_wa_ingest_guard_key( $phone . '|' . $email, $message, $card_id );
		if ( ! add_option( $guard, time(), '', false ) ) {
			return new WP_REST_Response( array( 'ok' => true, 'idempotent' => true ), 200 );
		}
		$payload = array(
			'name'       => $name,
			'phone'      => $phone,
			'email'      => $email,
			'goal'       => sanitize_text_field( (string) ( $p['goal'] ?? 'פנייה מ-WhatsApp' ) ),
			'message'    => $message,
			'source'     => 'whatsapp_ingest',
			'source_url' => esc_url_raw( (string) ( $p['url'] ?? '' ) ),
			'budget'     => sanitize_text_field( (string) ( $p['budget'] ?? '' ) ),
			'timeline'   => sanitize_text_field( (string) ( $p['timeline'] ?? '' ) ),
		);
		if ( function_exists( 'nadlan_lead_e2e_enabled' ) && nadlan_lead_e2e_enabled() && function_exists( 'nadlan_lead_e2e_capture' ) ) {
			$result = nadlan_lead_e2e_capture( $payload, $card_id, 'whatsapp_ingest' );
			if ( is_wp_error( $result ) ) {
				delete_option( $guard );
				return $result;
			}
			$lead_id = (int) ( $result['lead_id'] ?? 0 );
		} else {
			$lead_id = wp_insert_post( array(
				'post_type'    => 'nadlan_lead',
				'post_status'  => 'private',
				'post_title'   => $name . ' - WhatsApp - ' . current_time( 'Y-m-d H:i' ),
				'post_content' => $message,
			), true );
			if ( is_wp_error( $lead_id ) ) {
				delete_option( $guard );
				return $lead_id;
			}
			foreach ( $payload as $key => $value ) {
				if ( $value !== '' ) {
					update_post_meta( $lead_id, $key, $value );
				}
			}
			if ( $card_id ) {
				update_post_meta( $lead_id, 'lead_card_id', $card_id );
			}
			if ( function_exists( 'nadlan_lead_route' ) ) {
				nadlan_lead_route( $lead_id, $card_id, $payload, 'whatsapp_ingest' );
			}
		}
		if ( $lead_id ) {
			update_post_meta( $lead_id, 'whatsapp_ingested_at', time() );
			update_post_meta( $lead_id, 'whatsapp_ingest_context', sanitize_text_field( (string) ( $p['context'] ?? '' ) ) );
		}
		if ( function_exists( 'nadlan_log_event' ) ) {
			nadlan_log_event( 'lead_whatsapp', 'ingest', 'ok', array(
				'lead_ref'    => (int) $lead_id,
				'listing_ref' => (int) $card_id,
				'has_card'    => $card_id ? 1 : 0,
			) );
		}
		return new WP_REST_Response( array(
			'ok'        => true,
			'lead_id'   => (int) $lead_id,
			'card_id'   => (int) $card_id,
			'attributed'=> $card_id > 0,
		), 200 );
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/wa-lead', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => 'nadlan_wa_ingest_handle',
	) );
} );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['whatsapp_funnel'] = array(
		'loaded'          => true,
		'ingest_secret'   => nadlan_wa_ingest_secret() !== '',
		'endpoint'        => '/wp-json/nadlan/v1/wa-lead',
		'uses_lead_e2e'   => function_exists( 'nadlan_lead_e2e_capture' ),
	);
	return $out;
} );
