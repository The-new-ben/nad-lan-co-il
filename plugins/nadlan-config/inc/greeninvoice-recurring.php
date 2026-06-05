<?php
/**
 * nadlan-config - Green Invoice recurring IPN bridge (GAP 3).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_revenue_event' ) ) {
	function nadlan_revenue_event( $type, $amount = 0, $meta = array() ) {
		do_action( 'nadlan_revenue_event', $type, $amount, $meta );
	}
}

if ( ! function_exists( 'nadlan_deal_closed' ) ) {
	function nadlan_deal_closed( $deal ) {
		do_action( 'nadlan_deal_closed', $deal );
	}
}

if ( ! function_exists( 'nadlan_gi_card_post_types' ) ) {
	function nadlan_gi_card_post_types() {
		return array( 'nadlan_professional', 'nadlan_project', 'nadlan_property' );
	}
}

if ( ! function_exists( 'nadlan_gi_sig_scheme' ) ) {
	function nadlan_gi_sig_scheme() {
		$scheme = sanitize_key( (string) get_option( 'nadlan_gi_sig_scheme', 'morning' ) );
		return in_array( $scheme, array( 'morning', 'stripe' ), true ) ? $scheme : 'morning';
	}
}

if ( ! function_exists( 'nadlan_gi_verify_morning' ) ) {
	function nadlan_gi_verify_morning( $raw, $sig_header, $secret ) {
		$raw        = (string) $raw;
		$sig_header = trim( (string) $sig_header );
		$secret     = (string) $secret;
		if ( $raw === '' || $sig_header === '' || $secret === '' ) { return false; }

		if ( strpos( $sig_header, 'sha256=' ) === 0 ) {
			$sig_header = substr( $sig_header, 7 );
		}

		$expected_hex = hash_hmac( 'sha256', $raw, $secret );
		if ( preg_match( '/^[a-f0-9]{64}$/i', $sig_header ) ) {
			return hash_equals( strtolower( $expected_hex ), strtolower( $sig_header ) );
		}

		$expected_b64 = base64_encode( hash_hmac( 'sha256', $raw, $secret, true ) );
		return hash_equals( $expected_b64, $sig_header );
	}
}

if ( ! function_exists( 'nadlan_gi_verify_stripe' ) ) {
	function nadlan_gi_verify_stripe( $raw, $sig_header, $secret, $tolerance = 300 ) {
		$raw        = (string) $raw;
		$sig_header = (string) $sig_header;
		$secret     = (string) $secret;
		if ( $raw === '' || $sig_header === '' || $secret === '' ) { return false; }

		$parts = array();
		foreach ( explode( ',', $sig_header ) as $part ) {
			$kv = array_map( 'trim', explode( '=', $part, 2 ) );
			if ( count( $kv ) === 2 ) {
				$parts[ $kv[0] ] = $kv[1];
			}
		}
		$t  = isset( $parts['t'] ) ? (int) $parts['t'] : 0;
		$v1 = isset( $parts['v1'] ) ? (string) $parts['v1'] : '';
		if ( ! $t || $v1 === '' ) { return false; }
		if ( abs( time() - $t ) > (int) $tolerance ) { return false; }

		$expected = hash_hmac( 'sha256', $t . '.' . $raw, $secret );
		return hash_equals( $expected, $v1 );
	}
}

if ( ! function_exists( 'nadlan_gi_verify' ) ) {
	function nadlan_gi_verify( $raw, $sig_header, $secret, $tolerance = 300, $scheme = null ) {
		$scheme = $scheme ? sanitize_key( (string) $scheme ) : nadlan_gi_sig_scheme();
		if ( $scheme === 'stripe' ) {
			return nadlan_gi_verify_stripe( $raw, $sig_header, $secret, $tolerance );
		}
		return nadlan_gi_verify_morning( $raw, $sig_header, $secret );
	}
}

if ( ! function_exists( 'nadlan_gi_payload_get' ) ) {
	function nadlan_gi_payload_get( $payload, $paths, $default = null ) {
		foreach ( (array) $paths as $path ) {
			$cursor = $payload;
			$found  = true;
			foreach ( explode( '.', (string) $path ) as $part ) {
				if ( is_array( $cursor ) && array_key_exists( $part, $cursor ) ) {
					$cursor = $cursor[ $part ];
				} else {
					$found = false;
					break;
				}
			}
			if ( $found ) { return $cursor; }
		}
		return $default;
	}
}

if ( ! function_exists( 'nadlan_gi_normalize_status' ) ) {
	function nadlan_gi_normalize_status( $status ) {
		$status = strtolower( sanitize_key( (string) $status ) );
		if ( in_array( $status, array( 'paid', 'success', 'succeeded', 'completed', 'approved' ), true ) ) {
			return 'paid';
		}
		if ( in_array( $status, array( 'failed', 'failure', 'declined', 'rejected', 'unpaid' ), true ) ) {
			return 'failed';
		}
		return $status ?: 'unknown';
	}
}

if ( ! function_exists( 'nadlan_gi_parse_ref' ) ) {
	function nadlan_gi_parse_ref( $ref ) {
		$ref = trim( (string) $ref );
		if ( ! preg_match( '/^card_(\d+)_user_(\d+)_tier_(pro|premier)$/', $ref, $m ) ) {
			return new WP_Error( 'bad_ref', 'bad_ref', array( 'status' => 422 ) );
		}
		$card_id = (int) $m[1];
		$user_id = (int) $m[2];
		$tier    = (string) $m[3];
		$post    = get_post( $card_id );
		if ( ! $post || ! in_array( $post->post_type, nadlan_gi_card_post_types(), true ) ) {
			return new WP_Error( 'bad_card', 'bad_card', array( 'status' => 422 ) );
		}
		$owner = (int) get_post_meta( $card_id, 'owner_user_id', true );
		if ( $owner > 0 && $user_id > 0 && $owner !== $user_id ) {
			return new WP_Error( 'owner_mismatch', 'owner_mismatch', array( 'status' => 422 ) );
		}
		return array( 'card_id' => $card_id, 'user_id' => $user_id, 'tier' => $tier, 'ref' => $ref );
	}
}

if ( ! function_exists( 'nadlan_gi_cycle_days' ) ) {
	function nadlan_gi_cycle_days( $tier ) {
		$tier = in_array( $tier, array( 'pro', 'premier' ), true ) ? $tier : 'pro';
		return max( 1, min( 366, (int) get_option( 'nadlan_gi_cycle_days_' . $tier, 31 ) ) );
	}
}

if ( ! function_exists( 'nadlan_gi_charge_log' ) ) {
	function nadlan_gi_charge_log() {
		$log = get_option( 'nadlan_gi_charge_log', array() );
		return is_array( $log ) ? $log : array();
	}
}

if ( ! function_exists( 'nadlan_gi_prune_log' ) ) {
	function nadlan_gi_prune_log( $log = null ) {
		$log    = is_array( $log ) ? $log : nadlan_gi_charge_log();
		$floor  = time() - ( 3 * DAY_IN_SECONDS );
		$recent = array();
		$old    = array();
		foreach ( $log as $id => $entry ) {
			if ( (int) ( $entry['ts'] ?? 0 ) >= $floor ) {
				$recent[ $id ] = $entry;
			} else {
				$old[ $id ] = $entry;
			}
		}
		$sorter = function ( $a, $b ) {
			return (int) ( $b['ts'] ?? 0 ) <=> (int) ( $a['ts'] ?? 0 );
		};
		uasort( $recent, $sorter );
		uasort( $old, $sorter );
		$remaining = max( 0, 4000 - count( $recent ) );
		if ( $remaining > 0 ) {
			$log = $recent + array_slice( $old, 0, $remaining, true );
		} else {
			$log = $recent;
		}
		if ( count( $log ) > 4000 ) {
			uasort( $log, function ( $a, $b ) {
				return (int) ( $b['ts'] ?? 0 ) <=> (int) ( $a['ts'] ?? 0 );
			} );
		}
		update_option( 'nadlan_gi_charge_log', $log, false );
		return $log;
	}
}

if ( ! function_exists( 'nadlan_gi_log_event' ) ) {
	function nadlan_gi_log_event( $event_id, $entry ) {
		$event_id = sanitize_text_field( (string) $event_id );
		if ( $event_id === '' ) { return; }
		$log = nadlan_gi_prune_log();
		$log[ $event_id ] = array(
			'id'      => $event_id,
			'ts'      => (int) ( $entry['ts'] ?? time() ),
			'ref'     => sanitize_text_field( (string) ( $entry['ref'] ?? '' ) ),
			'card_id' => (int) ( $entry['card_id'] ?? 0 ),
			'tier'    => sanitize_key( (string) ( $entry['tier'] ?? '' ) ),
			'status'  => sanitize_key( (string) ( $entry['status'] ?? '' ) ),
			'action'  => sanitize_key( (string) ( $entry['action'] ?? '' ) ),
			'amount'  => (float) ( $entry['amount'] ?? 0 ),
		);
		update_option( 'nadlan_gi_charge_log', $log, false );
	}
}

if ( ! function_exists( 'nadlan_gi_extend_campaign' ) ) {
	function nadlan_gi_extend_campaign( $card_id, $tier, $amount = 0 ) {
		$card_id = (int) $card_id;
		$tier    = in_array( $tier, array( 'pro', 'premier' ), true ) ? $tier : 'pro';
		$now     = current_time( 'timestamp' );
		$current = (int) get_post_meta( $card_id, 'campaign_end', true );
		$end     = max( $now, $current ) + ( nadlan_gi_cycle_days( $tier ) * DAY_IN_SECONDS );

		update_post_meta( $card_id, 'paid_tier', $tier );
		update_post_meta( $card_id, 'campaign_end', $end );
		update_post_meta( $card_id, 'dunning_state', 'active' );
		delete_post_meta( $card_id, 'dunning_since' );
		delete_post_meta( $card_id, 'dunning_notice_day' );
		update_post_meta( $card_id, 'gi_last_paid_at', $now );

		nadlan_revenue_event( 'subscription_paid', (float) $amount, array( 'card_id' => $card_id, 'tier' => $tier ) );
		do_action( 'nadlan_subscription_renewed', $card_id, $tier );
		return $end;
	}
}

if ( ! function_exists( 'nadlan_gi_mark_dunning' ) ) {
	function nadlan_gi_mark_dunning( $card_id, $tier ) {
		$card_id = (int) $card_id;
		$tier    = in_array( $tier, array( 'pro', 'premier' ), true ) ? $tier : 'pro';
		update_post_meta( $card_id, 'dunning_state', 'retrying' );
		update_post_meta( $card_id, 'dunning_since', current_time( 'timestamp' ) );
		update_post_meta( $card_id, 'dunning_tier', $tier );
		delete_post_meta( $card_id, 'dunning_notice_day' );
		do_action( 'nadlan_subscription_payment_failed', $card_id, $tier );
	}
}

if ( ! function_exists( 'nadlan_gi_apply_event' ) ) {
	function nadlan_gi_apply_event( $payload, $source = 'ipn' ) {
		$event_id = sanitize_text_field( (string) nadlan_gi_payload_get( $payload, array( 'id', 'event_id', 'event.id' ), '' ) );
		if ( $event_id === '' ) {
			return new WP_Error( 'missing_event_id', 'missing_event_id', array( 'status' => 400 ) );
		}
		$log = nadlan_gi_charge_log();
		if ( isset( $log[ $event_id ] ) ) {
			return array( 'ok' => true, 'idempotent' => true, 'event_id' => $event_id );
		}

		$status = nadlan_gi_normalize_status( nadlan_gi_payload_get( $payload, array( 'status', 'payment_status', 'charge.status', 'data.status' ), '' ) );
		$ref    = sanitize_text_field( (string) nadlan_gi_payload_get( $payload, array( 'ref', 'reference', 'external_reference', 'charge.ref', 'data.ref' ), '' ) );
		$amount = (float) nadlan_gi_payload_get( $payload, array( 'amount', 'total', 'charge.amount', 'data.amount' ), 0 );
		$parsed = nadlan_gi_parse_ref( $ref );
		if ( is_wp_error( $parsed ) ) { return $parsed; }

		$action = 'ignored';
		$end    = 0;
		if ( $status === 'paid' ) {
			$end    = nadlan_gi_extend_campaign( $parsed['card_id'], $parsed['tier'], $amount );
			$action = 'extended';
		} elseif ( $status === 'failed' ) {
			nadlan_gi_mark_dunning( $parsed['card_id'], $parsed['tier'] );
			$action = 'dunning';
		}

		nadlan_gi_log_event( $event_id, array(
			'ts'      => time(),
			'ref'     => $ref,
			'card_id' => $parsed['card_id'],
			'tier'    => $parsed['tier'],
			'status'  => $status,
			'action'  => $action,
			'amount'  => $amount,
			'source'  => $source,
		) );

		return array(
			'ok'           => true,
			'event_id'     => $event_id,
			'status'       => $status,
			'action'       => $action,
			'card_id'      => $parsed['card_id'],
			'campaign_end' => $end,
		);
	}
}

if ( ! function_exists( 'nadlan_gi_signature_header' ) ) {
	function nadlan_gi_signature_header( $request ) {
		foreach ( array( 'x-data-signature', 'x-gi-signature', 'x-greeninvoice-signature', 'x-morning-signature', 'x-nadlan-signature' ) as $header ) {
			$value = $request->get_header( $header );
			if ( $value ) { return $value; }
		}
		return '';
	}
}

if ( ! function_exists( 'nadlan_gi_ipn_handler' ) ) {
	function nadlan_gi_ipn_handler( $request ) {
		$secret = (string) get_option( 'nadlan_gi_ipn_secret', '' );
		if ( $secret === '' ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'not_configured' ), 503 );
		}
		$raw = (string) $request->get_body();
		if ( $raw === '' ) { $raw = (string) file_get_contents( 'php://input' ); }
		if ( ! nadlan_gi_verify( $raw, nadlan_gi_signature_header( $request ), $secret, 300, nadlan_gi_sig_scheme() ) ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'bad_signature' ), 401 );
		}
		$payload = json_decode( $raw, true );
		if ( ! is_array( $payload ) ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'bad_json' ), 400 );
		}
		$result = nadlan_gi_apply_event( $payload, 'ipn' );
		if ( is_wp_error( $result ) ) { return $result; }
		return new WP_REST_Response( $result, 200 );
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/gi-ipn', array(
		'methods'             => 'POST',
		'callback'            => 'nadlan_gi_ipn_handler',
		'permission_callback' => '__return_true',
	) );
} );

if ( ! function_exists( 'nadlan_gi_dunning_tick' ) ) {
	function nadlan_gi_dunning_tick() {
		$now = current_time( 'timestamp' );
		$q = new WP_Query( array(
			'post_type'      => nadlan_gi_card_post_types(),
			'post_status'    => array( 'publish', 'pending', 'draft', 'private' ),
			'fields'         => 'ids',
			'posts_per_page' => 500,
			'meta_query'     => array(
				array( 'key' => 'dunning_state', 'value' => 'retrying' ),
				array( 'key' => 'dunning_since', 'compare' => 'EXISTS' ),
			),
		) );
		foreach ( $q->posts as $card_id ) {
			$since = (int) get_post_meta( $card_id, 'dunning_since', true );
			if ( ! $since ) { continue; }
			$days = (int) floor( ( $now - $since ) / DAY_IN_SECONDS );
			$last = (int) get_post_meta( $card_id, 'dunning_notice_day', true );
			foreach ( array( 2, 4, 7, 14 ) as $marker ) {
				if ( $days >= $marker && $last < $marker ) {
					update_post_meta( $card_id, 'dunning_notice_day', $marker );
					do_action( 'nadlan_subscription_dunning_notice', (int) $card_id, $marker );
					break;
				}
			}
			if ( $days >= 27 && in_array( (string) get_post_meta( $card_id, 'paid_tier', true ), array( 'pro', 'premier' ), true ) ) {
				update_post_meta( $card_id, 'paid_tier', 'free' );
				update_post_meta( $card_id, 'dunning_state', 'lapsed' );
				update_post_meta( $card_id, 'gi_lapsed_at', $now );
				do_action( 'nadlan_subscription_lapsed', (int) $card_id );
			}
		}
		wp_reset_postdata();
	}
}
add_action( 'nadlan_gi_dunning_tick', 'nadlan_gi_dunning_tick' );

if ( ! function_exists( 'nadlan_gi_reconcile' ) ) {
	function nadlan_gi_reconcile() {
		$url = trim( (string) apply_filters( 'nadlan_gi_reconcile_url', get_option( 'nadlan_gi_reconcile_url', '' ) ) );
		$key = (string) get_option( 'nadlan_gi_api_key', '' );
		if ( $url === '' || $key === '' ) { return; }
		$response = wp_remote_get( $url, array(
			'headers'   => array( 'Authorization' => 'Bearer ' . $key ),
			'timeout'   => 15,
			'sslverify' => true,
		) );
		if ( is_wp_error( $response ) || (int) wp_remote_retrieve_response_code( $response ) >= 400 ) { return; }
		$data = json_decode( wp_remote_retrieve_body( $response ), true );
		if ( ! is_array( $data ) ) { return; }
		$charges = nadlan_gi_payload_get( $data, array( 'charges', 'data', 'items' ), array() );
		if ( ! is_array( $charges ) ) { return; }
		foreach ( $charges as $charge ) {
			if ( ! is_array( $charge ) ) { continue; }
			if ( nadlan_gi_normalize_status( nadlan_gi_payload_get( $charge, array( 'status', 'payment_status' ), '' ) ) !== 'paid' ) { continue; }
			nadlan_gi_apply_event( $charge, 'reconcile' );
		}
	}
}
add_action( 'nadlan_gi_reconcile', 'nadlan_gi_reconcile' );

if ( ! function_exists( 'nadlan_gi_schedule_crons' ) ) {
	function nadlan_gi_schedule_crons() {
		if ( ! wp_next_scheduled( 'nadlan_gi_dunning_tick' ) ) {
			wp_schedule_event( time() + ( 2 * HOUR_IN_SECONDS ), 'daily', 'nadlan_gi_dunning_tick' );
		}
		if ( ! wp_next_scheduled( 'nadlan_gi_reconcile' ) ) {
			wp_schedule_event( time() + ( 3 * HOUR_IN_SECONDS ), 'daily', 'nadlan_gi_reconcile' );
		}
	}
}
add_action( 'init', 'nadlan_gi_schedule_crons' );

if ( ! function_exists( 'nadlan_gi_admin_menu' ) ) {
	function nadlan_gi_admin_menu() {
		add_options_page( 'NadLan Green Invoice', 'NadLan GI', 'manage_options', 'nadlan-gi-recurring', 'nadlan_gi_admin_render' );
	}
}
add_action( 'admin_menu', 'nadlan_gi_admin_menu' );

if ( ! function_exists( 'nadlan_gi_admin_render' ) ) {
	function nadlan_gi_admin_render() {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		if ( isset( $_POST['nadlan_gi_save'] ) && check_admin_referer( 'nadlan_gi_settings' ) ) {
			$scheme = isset( $_POST['nadlan_gi_sig_scheme'] ) ? sanitize_key( wp_unslash( $_POST['nadlan_gi_sig_scheme'] ) ) : 'morning';
			if ( ! in_array( $scheme, array( 'morning', 'stripe' ), true ) ) { $scheme = 'morning'; }
			update_option( 'nadlan_gi_sig_scheme', $scheme, false );
			$secret = isset( $_POST['nadlan_gi_ipn_secret_new'] ) ? trim( sanitize_text_field( wp_unslash( $_POST['nadlan_gi_ipn_secret_new'] ) ) ) : '';
			if ( $secret !== '' ) { update_option( 'nadlan_gi_ipn_secret', $secret, false ); }
			$api_key = isset( $_POST['nadlan_gi_api_key_new'] ) ? trim( sanitize_text_field( wp_unslash( $_POST['nadlan_gi_api_key_new'] ) ) ) : '';
			if ( $api_key !== '' ) { update_option( 'nadlan_gi_api_key', $api_key, false ); }
			foreach ( array( 'pro', 'premier' ) as $tier ) {
				$days = isset( $_POST[ 'nadlan_gi_cycle_days_' . $tier ] ) ? (int) $_POST[ 'nadlan_gi_cycle_days_' . $tier ] : 31;
				update_option( 'nadlan_gi_cycle_days_' . $tier, max( 1, min( 366, $days ) ), false );
				$link = isset( $_POST[ 'nadlan_gi_link_' . $tier ] ) ? esc_url_raw( wp_unslash( $_POST[ 'nadlan_gi_link_' . $tier ] ) ) : '';
				update_option( 'nadlan_gi_link_' . $tier, $link, false );
			}
			$reconcile_url = isset( $_POST['nadlan_gi_reconcile_url'] ) ? esc_url_raw( wp_unslash( $_POST['nadlan_gi_reconcile_url'] ) ) : '';
			update_option( 'nadlan_gi_reconcile_url', $reconcile_url, false );
			echo '<div class="updated"><p>Settings saved.</p></div>';
		}
		$log = nadlan_gi_charge_log();
		uasort( $log, function ( $a, $b ) { return (int) ( $b['ts'] ?? 0 ) <=> (int) ( $a['ts'] ?? 0 ); } );
		?>
		<div class="wrap">
			<h1>NadLan Green Invoice recurring</h1>
			<form method="post">
				<?php wp_nonce_field( 'nadlan_gi_settings' ); ?>
				<input type="hidden" name="nadlan_gi_save" value="1">
				<table class="form-table" role="presentation">
					<tr><th scope="row">Signature scheme</th><td><select name="nadlan_gi_sig_scheme"><option value="morning" <?php selected( nadlan_gi_sig_scheme(), 'morning' ); ?>>Morning X-Data-Signature</option><option value="stripe" <?php selected( nadlan_gi_sig_scheme(), 'stripe' ); ?>>Stripe-style t/v1 signature</option></select></td></tr>
					<tr><th scope="row">IPN secret</th><td><input type="password" name="nadlan_gi_ipn_secret_new" value="" class="regular-text" autocomplete="new-password"> <p class="description"><?php echo get_option( 'nadlan_gi_ipn_secret' ) ? 'Configured. Enter a new value only to replace it.' : 'Not configured.'; ?></p></td></tr>
					<tr><th scope="row">API key for reconciliation</th><td><input type="password" name="nadlan_gi_api_key_new" value="" class="regular-text" autocomplete="new-password"> <p class="description"><?php echo get_option( 'nadlan_gi_api_key' ) ? 'Configured. Enter a new value only to replace it.' : 'Optional, required for daily reconciliation.'; ?></p></td></tr>
					<tr><th scope="row">Reconciliation URL</th><td><input type="url" name="nadlan_gi_reconcile_url" value="<?php echo esc_attr( (string) get_option( 'nadlan_gi_reconcile_url', '' ) ); ?>" class="large-text"></td></tr>
					<?php foreach ( array( 'pro' => 'Pro', 'premier' => 'Premier' ) as $tier => $label ) : ?>
						<tr><th scope="row"><?php echo esc_html( $label ); ?> cycle days</th><td><input type="number" min="1" max="366" name="nadlan_gi_cycle_days_<?php echo esc_attr( $tier ); ?>" value="<?php echo (int) nadlan_gi_cycle_days( $tier ); ?>"></td></tr>
						<tr><th scope="row"><?php echo esc_html( $label ); ?> Morning recurring link</th><td><input type="url" name="nadlan_gi_link_<?php echo esc_attr( $tier ); ?>" value="<?php echo esc_attr( (string) get_option( 'nadlan_gi_link_' . $tier, '' ) ); ?>" class="large-text"></td></tr>
					<?php endforeach; ?>
				</table>
				<?php submit_button( 'Save settings' ); ?>
			</form>
			<h2>Charge log</h2>
			<table class="widefat striped">
				<thead><tr><th>Date</th><th>Ref</th><th>Tier</th><th>Status</th><th>Action</th></tr></thead>
				<tbody>
				<?php foreach ( array_slice( $log, 0, 50, true ) as $entry ) : ?>
					<tr>
						<td><?php echo esc_html( date_i18n( 'Y-m-d H:i', (int) ( $entry['ts'] ?? 0 ) ) ); ?></td>
						<td><?php echo esc_html( (string) ( $entry['ref'] ?? '' ) ); ?></td>
						<td><?php echo esc_html( (string) ( $entry['tier'] ?? '' ) ); ?></td>
						<td><?php echo esc_html( (string) ( $entry['status'] ?? '' ) ); ?></td>
						<td><?php echo esc_html( (string) ( $entry['action'] ?? '' ) ); ?></td>
					</tr>
				<?php endforeach; ?>
				<?php if ( ! $log ) : ?><tr><td colspan="5">No charges logged yet.</td></tr><?php endif; ?>
				</tbody>
			</table>
		</div>
		<?php
	}
}

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$log   = nadlan_gi_charge_log();
	$since = time() - ( 30 * DAY_IN_SECONDS );
	$paid  = 0;
	foreach ( $log as $entry ) {
		if ( (int) ( $entry['ts'] ?? 0 ) >= $since && ( $entry['status'] ?? '' ) === 'paid' ) {
			$paid++;
		}
	}
	$dunning = new WP_Query( array(
		'post_type'      => nadlan_gi_card_post_types(),
		'post_status'    => 'any',
		'fields'         => 'ids',
		'posts_per_page' => 1,
		'meta_query'     => array( array( 'key' => 'dunning_state', 'value' => 'retrying' ) ),
	) );
	$lapsed = new WP_Query( array(
		'post_type'      => nadlan_gi_card_post_types(),
		'post_status'    => 'any',
		'fields'         => 'ids',
		'posts_per_page' => 1,
		'meta_query'     => array( array( 'key' => 'gi_lapsed_at', 'value' => $since, 'compare' => '>=', 'type' => 'NUMERIC' ) ),
	) );
	$out['gi'] = array(
		'recurring_loaded' => true,
		'sig_scheme'       => nadlan_gi_sig_scheme(),
		'charges_30d'      => $paid,
		'in_dunning'       => (int) $dunning->found_posts,
		'lapsed_30d'       => (int) $lapsed->found_posts,
	);
	wp_reset_postdata();
	return $out;
} );
