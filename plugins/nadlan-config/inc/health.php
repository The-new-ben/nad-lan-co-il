<?php
/**
 * nadlan-config - reliability health endpoint + bounded event log (v1.56.0).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_health_now' ) ) {
	function nadlan_health_now() {
		return time();
	}
}

if ( ! function_exists( 'nadlan_health_scrub' ) ) {
	function nadlan_health_scrub( $value, $key = '' ) {
		$key = strtolower( (string) $key );
		if ( preg_match( '/(secret|token|password|pass|key|authorization|auth|cookie|email|phone|mobile|card|raw|body|name|ip)/', $key ) ) {
			return '[redacted]';
		}
		if ( is_array( $value ) ) {
			$out = array();
			foreach ( $value as $k => $v ) {
				$out[ sanitize_key( (string) $k ) ] = nadlan_health_scrub( $v, (string) $k );
			}
			return $out;
		}
		if ( is_object( $value ) ) {
			return '[object]';
		}
		if ( is_bool( $value ) || is_numeric( $value ) || $value === null ) {
			return $value;
		}
		$value = sanitize_text_field( (string) $value );
		return substr( $value, 0, 160 );
	}
}

if ( ! function_exists( 'nadlan_log_event' ) ) {
	function nadlan_log_event( $channel, $id, $status, $meta = array() ) {
		$channel = sanitize_key( (string) $channel );
		$id = substr( sanitize_text_field( (string) $id ), 0, 120 );
		$status = sanitize_key( (string) $status );
		if ( $channel === '' || $id === '' || $status === '' ) { return false; }

		$now = nadlan_health_now();
		$retention = max( 1, (int) get_option( 'nadlan_event_log_retention_days', 30 ) ) * DAY_IN_SECONDS;
		$limit = min( 2000, max( 50, (int) get_option( 'nadlan_event_log_limit', 500 ) ) );
		$log = get_option( 'nadlan_event_log', array() );
		if ( ! is_array( $log ) ) { $log = array(); }
		$log[] = array(
			'ts'      => $now,
			'channel' => $channel,
			'id'      => $id,
			'status'  => $status,
			'meta'    => nadlan_health_scrub( is_array( $meta ) ? $meta : array( 'value' => $meta ) ),
		);
		$log = array_values( array_filter( $log, function ( $row ) use ( $now, $retention ) {
			return is_array( $row ) && (int) ( $row['ts'] ?? 0 ) >= ( $now - $retention );
		} ) );
		if ( count( $log ) > $limit ) {
			$log = array_slice( $log, -1 * $limit );
		}
		update_option( 'nadlan_event_log', $log, false );
		nadlan_health_maybe_alert( $channel, $id, $status, $log );
		return true;
	}
}

if ( ! function_exists( 'nadlan_health_maybe_alert' ) ) {
	function nadlan_health_maybe_alert( $channel, $id, $status, $log ) {
		if ( ! in_array( $status, array( 'fail', 'error', 'critical', 'degraded' ), true ) ) { return; }
		$window = max( 60, (int) get_option( 'nadlan_event_alert_window_sec', 15 * MINUTE_IN_SECONDS ) );
		$threshold = max( 2, (int) get_option( 'nadlan_event_alert_threshold', 5 ) );
		$now = nadlan_health_now();
		$count = 0;
		foreach ( array_reverse( (array) $log ) as $row ) {
			if ( ! is_array( $row ) ) { continue; }
			if ( (int) ( $row['ts'] ?? 0 ) < $now - $window ) { break; }
			if ( ( $row['channel'] ?? '' ) === $channel && ( $row['id'] ?? '' ) === $id && ( $row['status'] ?? '' ) === $status ) {
				$count++;
			}
		}
		if ( $count < $threshold ) { return; }
		$tk = 'nadlan_event_alert_' . md5( $channel . '|' . $id . '|' . $status );
		if ( get_transient( $tk ) ) { return; }
		set_transient( $tk, 1, $window );
		if ( ! apply_filters( 'nadlan_reliability_alert_should_send', true, $channel, $id, $status, $count ) ) { return; }
		$admin = sanitize_email( get_option( 'admin_email' ) );
		if ( ! $admin ) { return; }
		$subject = sprintf( 'NadLan alert: %s %s', $channel, $status );
		$body = sprintf(
			"Event: %s\nStatus: %s\nCount in window: %d\nWindow seconds: %d\nTime UTC: %s\n",
			$id,
			$status,
			$count,
			$window,
			gmdate( 'Y-m-d H:i:s', $now )
		);
		wp_mail( $admin, $subject, $body );
	}
}

if ( ! function_exists( 'nadlan_health_probe_db' ) ) {
	function nadlan_health_probe_db() {
		global $wpdb;
		$start = microtime( true );
		$ok = false;
		$error = '';
		try {
			$ok = (string) $wpdb->get_var( 'SELECT 1' ) === '1';
			if ( ! $ok ) { $error = 'unexpected_result'; }
		} catch ( Throwable $e ) {
			$error = $e->getMessage();
		}
		return array(
			'status' => $ok ? 'ok' : 'fail',
			'latency_ms' => round( ( microtime( true ) - $start ) * 1000, 1 ),
			'error' => $ok ? null : nadlan_health_scrub( $error, 'db_error' ),
		);
	}
}

if ( ! function_exists( 'nadlan_health_probe_http' ) ) {
	function nadlan_health_probe_http( $name, $url ) {
		$url = esc_url_raw( (string) $url );
		if ( $url === '' ) {
			return array( 'status' => 'skipped', 'configured' => false, 'code' => null, 'latency_ms' => null );
		}
		$start = microtime( true );
		$res = wp_remote_get( $url, array(
			'timeout'             => 4,
			'redirection'         => 1,
			'limit_response_size' => 256,
			'sslverify'           => true,
			'user-agent'          => 'NadLanHealth/1.56.0; ' . home_url( '/' ),
		) );
		$latency = round( ( microtime( true ) - $start ) * 1000, 1 );
		if ( is_wp_error( $res ) ) {
			return array(
				'status'     => 'fail',
				'configured' => true,
				'code'       => null,
				'latency_ms' => $latency,
				'error'      => nadlan_health_scrub( $res->get_error_message(), $name . '_error' ),
			);
		}
		$code = (int) wp_remote_retrieve_response_code( $res );
		return array(
			'status'     => $code >= 500 || $code === 0 ? 'fail' : 'ok',
			'configured' => true,
			'code'       => $code,
			'latency_ms' => $latency,
		);
	}
}

if ( ! function_exists( 'nadlan_health_dependency_report' ) ) {
	function nadlan_health_dependency_report() {
		$green_url = apply_filters( 'nadlan_health_greeninvoice_url', get_option( 'nadlan_gi_health_url', 'https://api.greeninvoice.co.il/api/v1' ) );
		$openai_url = apply_filters( 'nadlan_health_openai_url', get_option( 'nadlan_openai_health_url', 'https://api.openai.com/v1/models' ) );
		return array(
			'db' => nadlan_health_probe_db(),
			'greeninvoice' => nadlan_health_probe_http( 'greeninvoice', $green_url ),
			'openai' => nadlan_health_probe_http( 'openai', $openai_url ),
		);
	}
}

if ( ! function_exists( 'nadlan_health_aggregate' ) ) {
	function nadlan_health_aggregate( $deps ) {
		$aggregate = 'ok';
		foreach ( (array) $deps as $name => $dep ) {
			$status = (string) ( $dep['status'] ?? 'fail' );
			if ( $name === 'db' && $status === 'fail' ) { return 'fail'; }
			if ( $status === 'fail' ) { $aggregate = 'degraded'; }
		}
		return $aggregate;
	}
}

if ( ! function_exists( 'nadlan_health_rest' ) ) {
	function nadlan_health_rest() {
		$deps = nadlan_health_dependency_report();
		$aggregate = nadlan_health_aggregate( $deps );
		if ( $aggregate !== 'ok' ) {
			nadlan_log_event( 'health', 'aggregate', $aggregate, array( 'dependencies' => $deps ) );
		}
		return new WP_REST_Response( array(
			'plugin'       => 'nadlan-config',
			'version'      => '1.64.3',
			'status'       => $aggregate,
			'generated_at' => gmdate( 'c' ),
			'dependencies' => $deps,
			'lead_e2e'     => function_exists( 'nadlan_lead_e2e_metrics' ) ? nadlan_lead_e2e_metrics( 7 ) : array( 'enabled' => false, 'loaded' => false ),
			'lead_ai'      => function_exists( 'nadlan_lead_ai_metrics' ) ? nadlan_lead_ai_metrics( 7 ) : array( 'enabled' => false, 'loaded' => false ),
			'lead_nurture' => function_exists( 'nadlan_lead_nurture_metrics' ) ? nadlan_lead_nurture_metrics( 7 ) : array( 'enabled' => false, 'loaded' => false ),
			'admin_control' => function_exists( 'nadlan_admin_control_metrics' ) ? nadlan_admin_control_metrics() : array( 'enabled' => false, 'loaded' => false ),
			'slo'          => array(
				'target' => '99.9',
				'alerting' => 'multi-window multi-burn-rate, symptom first',
			),
		), 200 );
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/health', array(
		'methods'             => 'GET',
		'callback'            => 'nadlan_health_rest',
		'permission_callback' => '__return_true',
	) );
} );

if ( ! function_exists( 'nadlan_reliability_ping_heartbeat' ) ) {
	function nadlan_reliability_ping_heartbeat( $name ) {
		$name = sanitize_key( (string) $name );
		if ( $name === '' ) { return false; }
		update_option( 'nadlan_reliability_last_cron_' . $name, nadlan_health_now(), false );
		$url = esc_url_raw( (string) get_option( 'nadlan_heartbeat_' . $name . '_url', '' ) );
		if ( $url === '' ) {
			nadlan_log_event( 'cron', $name, 'seen', array( 'heartbeat_configured' => false ) );
			return false;
		}
		wp_remote_get( $url, array(
			'timeout'     => 4,
			'blocking'    => false,
			'sslverify'   => true,
			'user-agent'  => 'NadLanCronHeartbeat/1.56.0; ' . home_url( '/' ),
		) );
		nadlan_log_event( 'cron', $name, 'heartbeat_sent', array( 'heartbeat_configured' => true ) );
		return true;
	}
}

add_action( 'nadlan_gi_reconcile', function () { nadlan_reliability_ping_heartbeat( 'nadlan_gi_reconcile' ); }, 99 );
add_action( 'nadlan_gi_dunning_tick', function () { nadlan_reliability_ping_heartbeat( 'nadlan_gi_dunning_tick' ); }, 99 );
add_action( 'nadlan_ao_daily_downgrade', function () { nadlan_reliability_ping_heartbeat( 'nadlan_ao_daily_downgrade' ); }, 99 );

if ( ! function_exists( 'nadlan_reliability_last_cron_run' ) ) {
	function nadlan_reliability_last_cron_run() {
		$hooks = array( 'nadlan_gi_reconcile', 'nadlan_gi_dunning_tick', 'nadlan_ao_daily_downgrade' );
		$last = 0;
		foreach ( $hooks as $hook ) {
			$last = max( $last, (int) get_option( 'nadlan_reliability_last_cron_' . $hook, 0 ) );
		}
		return $last;
	}
}

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$last = nadlan_reliability_last_cron_run();
	$out['reliability'] = array(
		'health_loaded'  => true,
		'deps_ok'        => nadlan_health_aggregate( nadlan_health_dependency_report() ) === 'ok',
		'last_cron_run'  => $last,
		'last_cron_age'  => $last ? nadlan_health_now() - $last : null,
		'event_log_size' => count( (array) get_option( 'nadlan_event_log', array() ) ),
	);
	return $out;
} );

add_filter( 'site_status_tests', function ( $tests ) {
	$tests['direct']['nadlan_reliability_cron'] = array(
		'label' => 'NadLan reliability cron heartbeat',
		'test'  => 'nadlan_reliability_site_health_cron',
	);
	return $tests;
} );

if ( ! function_exists( 'nadlan_reliability_site_health_cron' ) ) {
	function nadlan_reliability_site_health_cron() {
		$last = nadlan_reliability_last_cron_run();
		$disabled = defined( 'DISABLE_WP_CRON' ) && DISABLE_WP_CRON;
		$status = $last && ( nadlan_health_now() - $last ) < 2 * DAY_IN_SECONDS ? 'good' : 'recommended';
		return array(
			'label'       => 'NadLan cron heartbeat visibility',
			'status'      => $status,
			'badge'       => array( 'label' => 'NadLan', 'color' => 'blue' ),
			'description' => $disabled
				? '<p>WP-Cron is disabled. Confirm the server cron calls wp-cron.php on a fixed schedule and configure heartbeat URLs for billing crons.</p>'
				: '<p>WP-Cron is traffic dependent. For revenue operations, use a real server cron and heartbeat URLs.</p>',
			'actions'     => '<p>Monitor /wp-json/nadlan/v1/health externally every 30 to 60 seconds. Configure heartbeat options for dunning and reconciliation cron hooks.</p>',
			'test'        => 'nadlan_reliability_cron',
		);
	}
}
