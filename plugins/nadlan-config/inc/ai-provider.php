<?php
/**
 * nadlan-config - provider-agnostic AI adapter (GAP 4, v1.43.2).
 *
 * Default provider is OpenAI. Anthropic stays available as a fallback so older
 * installs with an existing key keep working. Secrets are read only from server
 * constants or WordPress options, never from client-side code.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ai_provider' ) ) {
	function nadlan_ai_provider() {
		$provider = sanitize_key( (string) get_option( 'nadlan_ai_provider', 'openai' ) );
		return in_array( $provider, array( 'openai', 'anthropic' ), true ) ? $provider : 'openai';
	}
}

if ( ! function_exists( 'nadlan_ai_openai_key' ) ) {
	function nadlan_ai_openai_key() {
		if ( defined( 'NADLAN_OPENAI_API_KEY' ) && NADLAN_OPENAI_API_KEY ) { return (string) NADLAN_OPENAI_API_KEY; }
		if ( defined( 'OPENAI_API_KEY' ) && OPENAI_API_KEY ) { return (string) OPENAI_API_KEY; }
		return (string) get_option( 'nadlan_ai_openai_key', '' );
	}
}

if ( ! function_exists( 'nadlan_ai_anthropic_key' ) ) {
	function nadlan_ai_anthropic_key() {
		if ( defined( 'ANTHROPIC_API_KEY' ) && ANTHROPIC_API_KEY ) { return (string) ANTHROPIC_API_KEY; }
		if ( defined( 'NADLAN_LLM_API_KEY' ) && NADLAN_LLM_API_KEY ) { return (string) NADLAN_LLM_API_KEY; }
		$key = (string) get_option( 'nadlan_ai_anthropic_key', '' );
		return $key !== '' ? $key : (string) get_option( 'nadlan_llm_key', '' );
	}
}

if ( ! function_exists( 'nadlan_ai_key' ) ) {
	function nadlan_ai_key() {
		return nadlan_ai_provider() === 'anthropic' ? nadlan_ai_anthropic_key() : nadlan_ai_openai_key();
	}
}

if ( ! function_exists( 'nadlan_ai_enabled' ) ) {
	function nadlan_ai_enabled() {
		if ( defined( 'NADLAN_DISABLE_AI' ) && NADLAN_DISABLE_AI ) { return false; }
		if ( (int) get_option( 'nadlan_ai_enabled', 1 ) !== 1 ) { return false; }
		return nadlan_ai_key() !== '';
	}
}

if ( ! function_exists( 'nadlan_ai_missing_message' ) ) {
	function nadlan_ai_missing_message() {
		return 'השירות אינו זמין כרגע. השאירו פרטים ונחזור אליכם.';
	}
}

if ( ! function_exists( 'nadlan_ai_strlen' ) ) {
	function nadlan_ai_strlen( $text ) {
		return function_exists( 'mb_strlen' ) ? mb_strlen( (string) $text ) : strlen( (string) $text );
	}
}

if ( ! function_exists( 'nadlan_ai_normalize_messages' ) ) {
	function nadlan_ai_normalize_messages( $messages ) {
		$out = array();
		foreach ( (array) $messages as $message ) {
			if ( ! is_array( $message ) ) { continue; }
			$role = isset( $message['role'] ) && $message['role'] === 'assistant' ? 'assistant' : 'user';
			$text = sanitize_textarea_field( (string) ( $message['content'] ?? '' ) );
			if ( $text === '' ) { continue; }
			$out[] = array(
				'role'    => $role,
				'content' => function_exists( 'mb_substr' ) ? mb_substr( $text, 0, 2500 ) : substr( $text, 0, 2500 ),
			);
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_ai_estimate_tokens' ) ) {
	function nadlan_ai_estimate_tokens( $system, $messages, $max_tokens ) {
		$chars = nadlan_ai_strlen( $system );
		foreach ( (array) $messages as $message ) {
			if ( is_array( $message ) ) {
				$chars += nadlan_ai_strlen( $message['content'] ?? '' );
			}
		}
		return max( 1, (int) ceil( $chars / 4 ) + max( 1, (int) $max_tokens ) );
	}
}

if ( ! function_exists( 'nadlan_ai_request_ip' ) ) {
	function nadlan_ai_request_ip() {
		$ip = isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '0.0.0.0';
		return $ip !== '' ? $ip : '0.0.0.0';
	}
}

if ( ! function_exists( 'nadlan_ai_guard' ) ) {
	function nadlan_ai_guard( $ip, $estimated_tokens = 0 ) {
		$estimated_tokens = max( 1, (int) $estimated_tokens );
		$global_cap = (int) get_option( 'nadlan_ai_daily_token_cap_global', 200000 );
		if ( $global_cap < 10000 ) { $global_cap = 200000; }
		$global_used = (int) get_option( 'nadlan_ai_tokens_today_' . gmdate( 'Ymd' ), 0 );
		if ( $global_used + $estimated_tokens > $global_cap ) {
			return new WP_Error( 'ai_global_cap', 'daily budget reached' );
		}
		$cap = (int) get_option( 'nadlan_ai_daily_token_cap', 30000 );
		if ( $cap < 1000 ) { $cap = 30000; }
		$key = 'nadlan_ai_daily_' . gmdate( 'Ymd' ) . '_' . md5( (string) $ip );
		$used = (int) get_transient( $key );
		if ( $used + $estimated_tokens > $cap ) {
			return new WP_Error( 'ai_daily_cap', 'daily_token_cap' );
		}
		set_transient( $key, $used + $estimated_tokens, DAY_IN_SECONDS + HOUR_IN_SECONDS );
		return true;
	}
}

if ( ! function_exists( 'nadlan_ai_prune_daily_counters' ) ) {
	function nadlan_ai_prune_daily_counters() {
		if ( get_transient( 'nadlan_ai_pruned_' . gmdate( 'Ymd' ) ) ) { return; }
		global $wpdb;
		$prefix = 'nadlan_ai_tokens_today_';
		$cutoff = gmdate( 'Ymd', time() - 7 * DAY_IN_SECONDS );
		$names = $wpdb->get_col( $wpdb->prepare(
			"SELECT option_name FROM {$wpdb->options} WHERE option_name LIKE %s",
			$wpdb->esc_like( $prefix ) . '%'
		) );
		foreach ( (array) $names as $name ) {
			$day = substr( (string) $name, strlen( $prefix ), 8 );
			if ( preg_match( '/^\d{8}$/', $day ) && $day < $cutoff ) {
				delete_option( $name );
			}
		}
		set_transient( 'nadlan_ai_pruned_' . gmdate( 'Ymd' ), 1, DAY_IN_SECONDS );
	}
}

if ( ! function_exists( 'nadlan_ai_increment_global_tokens' ) ) {
	function nadlan_ai_increment_global_tokens( $tokens ) {
		$tokens = max( 0, (int) $tokens );
		if ( $tokens <= 0 ) { return; }
		$key = 'nadlan_ai_tokens_today_' . gmdate( 'Ymd' );
		update_option( $key, (int) get_option( $key, 0 ) + $tokens, false );
		nadlan_ai_prune_daily_counters();
	}
}

if ( ! function_exists( 'nadlan_ai_openai_model' ) ) {
	function nadlan_ai_openai_model() {
		return (string) apply_filters( 'nadlan_ai_openai_model', 'gpt-4o-mini' );
	}
}

if ( ! function_exists( 'nadlan_ai_anthropic_model' ) ) {
	function nadlan_ai_anthropic_model() {
		return (string) apply_filters( 'nadlan_ai_model', apply_filters( 'nadlan_ai_anthropic_model', 'claude-haiku-4-5' ) );
	}
}

if ( ! function_exists( 'nadlan_ai_last_usage' ) ) {
	function nadlan_ai_last_usage() {
		return isset( $GLOBALS['nadlan_ai_last_usage'] ) && is_array( $GLOBALS['nadlan_ai_last_usage'] )
			? $GLOBALS['nadlan_ai_last_usage']
			: array();
	}
}

if ( ! function_exists( 'nadlan_ai_estimated_cost_usd' ) ) {
	function nadlan_ai_estimated_cost_usd( $provider, $model, $input_tokens, $output_tokens ) {
		if ( $provider !== 'openai' || strpos( $model, 'gpt-4o-mini' ) !== 0 ) {
			return 0.0;
		}
		$input_per_m  = (float) apply_filters( 'nadlan_ai_openai_input_per_m_usd', 0.15, $model );
		$output_per_m = (float) apply_filters( 'nadlan_ai_openai_output_per_m_usd', 0.60, $model );
		return ( $input_tokens / 1000000 * $input_per_m ) + ( $output_tokens / 1000000 * $output_per_m );
	}
}

if ( ! function_exists( 'nadlan_ai_record_usage' ) ) {
	function nadlan_ai_record_usage( $provider, $model, $usage, $estimated_tokens = 0, $status = 'ok' ) {
		$usage = is_array( $usage ) ? $usage : array();
		$input = (int) ( $usage['prompt_tokens'] ?? $usage['input_tokens'] ?? 0 );
		$output = (int) ( $usage['completion_tokens'] ?? $usage['output_tokens'] ?? 0 );
		$total = (int) ( $usage['total_tokens'] ?? ( $input + $output ) );
		if ( $total <= 0 ) { $total = max( 0, (int) $estimated_tokens ); }
		$cost = nadlan_ai_estimated_cost_usd( $provider, $model, $input, $output );
		$month = gmdate( 'Ym' );
		$key = 'nadlan_ai_usage_' . $month;
		$stats = get_option( $key, array() );
		if ( ! is_array( $stats ) ) { $stats = array(); }
		foreach ( array( 'calls', 'errors', 'tokens_total', 'tokens_input', 'tokens_output', 'estimated_cost_usd' ) as $field ) {
			if ( ! isset( $stats[ $field ] ) ) { $stats[ $field ] = 0; }
		}
		$stats['calls'] += 1;
		if ( $status !== 'ok' ) { $stats['errors'] += 1; }
		$stats['tokens_total'] += $total;
		$stats['tokens_input'] += $input;
		$stats['tokens_output'] += $output;
		$stats['estimated_cost_usd'] += $cost;
		$stats['last_provider'] = $provider;
		$stats['last_model'] = $model;
		$stats['last_status'] = $status;
		$stats['last_at'] = time();
		update_option( $key, $stats, false );
		if ( $status === 'ok' ) {
			nadlan_ai_increment_global_tokens( $total );
		}
		update_option( 'nadlan_ai_total_tokens', (int) get_option( 'nadlan_ai_total_tokens', 0 ) + $total, false );
		update_option( 'nadlan_ai_total_msgs', (int) get_option( 'nadlan_ai_total_msgs', 0 ) + 1, false );
		$GLOBALS['nadlan_ai_last_usage'] = array(
			'provider' => $provider,
			'model'    => $model,
			'status'   => $status,
			'input_tokens' => $input,
			'output_tokens' => $output,
			'total_tokens' => $total,
			'estimated_cost_usd' => $cost,
		);
	}
}

if ( ! function_exists( 'nadlan_ai_note_error' ) ) {
	function nadlan_ai_note_error( $provider, $model, $code, $message ) {
		update_option( 'nadlan_ai_last_error', array(
			't'        => time(),
			'provider' => $provider,
			'model'    => $model,
			'code'     => sanitize_key( (string) $code ),
			'message'  => function_exists( 'mb_substr' ) ? mb_substr( sanitize_text_field( (string) $message ), 0, 180 ) : substr( sanitize_text_field( (string) $message ), 0, 180 ),
		), false );
		nadlan_ai_record_usage( $provider, $model, array(), 0, 'error' );
	}
}

if ( ! function_exists( 'nadlan_ai_chat_openai' ) ) {
	function nadlan_ai_chat_openai( $system, $messages, $max_tokens = 600, $estimated_tokens = 0 ) {
		$key = nadlan_ai_openai_key();
		$model = nadlan_ai_openai_model();
		if ( $key === '' ) { return new WP_Error( 'nokey', 'OpenAI key missing' ); }
		$payload = array(
			'model'      => $model,
			'store'      => false,
			'max_tokens' => max( 1, (int) $max_tokens ),
			'messages'   => array_merge(
				array( array( 'role' => 'system', 'content' => (string) $system ) ),
				nadlan_ai_normalize_messages( $messages )
			),
		);
		$resp = wp_remote_post( 'https://api.openai.com/v1/chat/completions', array(
			'timeout' => 30,
			'headers' => array(
				'Authorization'       => 'Bearer ' . $key,
				'Content-Type'        => 'application/json',
				'X-Client-Request-Id' => function_exists( 'wp_generate_uuid4' ) ? wp_generate_uuid4() : uniqid( 'nadlan-ai-', true ),
			),
			'body' => wp_json_encode( $payload, JSON_UNESCAPED_UNICODE ),
			'sslverify' => true,
		) );
		if ( is_wp_error( $resp ) ) {
			nadlan_ai_note_error( 'openai', $model, $resp->get_error_code(), $resp->get_error_message() );
			return $resp;
		}
		$code = (int) wp_remote_retrieve_response_code( $resp );
		$data = json_decode( wp_remote_retrieve_body( $resp ), true );
		if ( $code < 200 || $code >= 300 || ! is_array( $data ) ) {
			$msg = is_array( $data ) ? (string) ( $data['error']['message'] ?? '' ) : wp_remote_retrieve_body( $resp );
			nadlan_ai_note_error( 'openai', $model, 'http_' . $code, $msg );
			return new WP_Error( 'openai_http', 'OpenAI HTTP ' . $code );
		}
		$text = trim( (string) ( $data['choices'][0]['message']['content'] ?? '' ) );
		if ( $text === '' ) {
			nadlan_ai_note_error( 'openai', $model, 'empty', 'empty response' );
			return new WP_Error( 'openai_empty', 'OpenAI returned no content' );
		}
		nadlan_ai_record_usage( 'openai', $model, (array) ( $data['usage'] ?? array() ), $estimated_tokens, 'ok' );
		return $text;
	}
}

if ( ! function_exists( 'nadlan_ai_chat_anthropic' ) ) {
	function nadlan_ai_chat_anthropic( $system, $messages, $max_tokens = 600, $estimated_tokens = 0 ) {
		$key = nadlan_ai_anthropic_key();
		$model = nadlan_ai_anthropic_model();
		if ( $key === '' ) { return new WP_Error( 'nokey', 'Anthropic key missing' ); }
		$body = array(
			'model'      => $model,
			'max_tokens' => max( 1, (int) $max_tokens ),
			'system'     => (string) $system,
			'messages'   => nadlan_ai_normalize_messages( $messages ),
		);
		$resp = wp_remote_post( 'https://api.anthropic.com/v1/messages', array(
			'timeout' => 30,
			'headers' => array(
				'x-api-key'         => $key,
				'anthropic-version' => '2023-06-01',
				'content-type'      => 'application/json',
			),
			'body' => wp_json_encode( $body, JSON_UNESCAPED_UNICODE ),
			'sslverify' => true,
		) );
		if ( is_wp_error( $resp ) ) {
			nadlan_ai_note_error( 'anthropic', $model, $resp->get_error_code(), $resp->get_error_message() );
			return $resp;
		}
		$code = (int) wp_remote_retrieve_response_code( $resp );
		$data = json_decode( wp_remote_retrieve_body( $resp ), true );
		if ( $code < 200 || $code >= 300 || ! is_array( $data ) ) {
			$msg = is_array( $data ) ? (string) ( $data['error']['message'] ?? '' ) : wp_remote_retrieve_body( $resp );
			nadlan_ai_note_error( 'anthropic', $model, 'http_' . $code, $msg );
			return new WP_Error( 'anthropic_http', 'Anthropic HTTP ' . $code );
		}
		$text = '';
		foreach ( (array) ( $data['content'] ?? array() ) as $block ) {
			if ( ( $block['type'] ?? '' ) === 'text' ) { $text .= $block['text']; }
		}
		$text = trim( $text );
		if ( $text === '' ) {
			nadlan_ai_note_error( 'anthropic', $model, 'empty', 'empty response' );
			return new WP_Error( 'anthropic_empty', 'Anthropic returned no content' );
		}
		nadlan_ai_record_usage( 'anthropic', $model, (array) ( $data['usage'] ?? array() ), $estimated_tokens, 'ok' );
		return $text;
	}
}

if ( ! function_exists( 'nadlan_ai_chat' ) ) {
	/**
	 * @param string $system   System instructions.
	 * @param array  $messages Array of role/content messages.
	 * @param int    $max_tokens Max output tokens.
	 * @return string|WP_Error
	 */
	function nadlan_ai_chat( $system, $messages, $max_tokens = 600 ) {
		if ( defined( 'NADLAN_DISABLE_AI' ) && NADLAN_DISABLE_AI ) {
			return new WP_Error( 'disabled', 'AI disabled' );
		}
		if ( (int) get_option( 'nadlan_ai_enabled', 1 ) !== 1 ) {
			return new WP_Error( 'disabled', 'AI disabled' );
		}
		$messages = nadlan_ai_normalize_messages( $messages );
		if ( ! $messages ) { return new WP_Error( 'invalid', 'no messages' ); }
		$estimated = nadlan_ai_estimate_tokens( $system, $messages, $max_tokens );
		$guard = nadlan_ai_guard( nadlan_ai_request_ip(), $estimated );
		if ( is_wp_error( $guard ) ) { return $guard; }
		$provider = nadlan_ai_provider();
		if ( $provider === 'anthropic' ) {
			return nadlan_ai_chat_anthropic( $system, $messages, $max_tokens, $estimated );
		}
		return nadlan_ai_chat_openai( $system, $messages, $max_tokens, $estimated );
	}
}

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$month = gmdate( 'Ym' );
	$usage = get_option( 'nadlan_ai_usage_' . $month, array() );
	$out['ai'] = array(
		'provider'              => nadlan_ai_provider(),
		'enabled'               => (int) get_option( 'nadlan_ai_enabled', 1 ) === 1,
		'openai_key_present'    => nadlan_ai_openai_key() !== '',
		'anthropic_key_present' => nadlan_ai_anthropic_key() !== '',
		'daily_token_cap'       => (int) get_option( 'nadlan_ai_daily_token_cap', 30000 ),
		'daily_token_cap_global'=> (int) get_option( 'nadlan_ai_daily_token_cap_global', 200000 ),
		'tokens_today'          => (int) get_option( 'nadlan_ai_tokens_today_' . gmdate( 'Ymd' ), 0 ),
		'usage_month'           => $month,
		'usage_calls'           => is_array( $usage ) ? (int) ( $usage['calls'] ?? 0 ) : 0,
		'usage_tokens'          => is_array( $usage ) ? (int) ( $usage['tokens_total'] ?? 0 ) : 0,
	);
	return $out;
} );
