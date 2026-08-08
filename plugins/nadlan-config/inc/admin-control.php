<?php
/**
 * nadlan-config - Chunk E operator admin control plane (v1.55.0).
 *
 * Ships dark behind nadlan_feature_admin_control. OFF means no menu, no REST
 * routes, no registered admin-control meta, and no custom operator capability.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! defined( 'NADLAN_ADMIN_CONTROL_CAP' ) ) {
	define( 'NADLAN_ADMIN_CONTROL_CAP', 'nadlan_manage_clients' );
}

if ( ! function_exists( 'nadlan_admin_control_enabled' ) ) {
	function nadlan_admin_control_enabled() {
		return (bool) apply_filters( 'nadlan_admin_control_enabled', get_option( 'nadlan_feature_admin_control', '0' ) === '1' );
	}
}

if ( ! function_exists( 'nadlan_admin_control_card_post_types' ) ) {
	function nadlan_admin_control_card_post_types() {
		return function_exists( 'nadlan_roles_card_cpts' )
			? nadlan_roles_card_cpts()
			: array( 'nadlan_property', 'nadlan_project', 'nadlan_professional' );
	}
}

if ( ! function_exists( 'nadlan_admin_control_field_keys' ) ) {
	function nadlan_admin_control_field_keys() {
		return array( 'city', 'lat', 'lng', 'references', 'priority_weight' );
	}
}

if ( ! function_exists( 'nadlan_admin_control_override_keys' ) ) {
	function nadlan_admin_control_override_keys() {
		return array( 'is_pinned', 'boost_multiplier', 'reserved_slot', 'promo_until' );
	}
}

if ( ! function_exists( 'nadlan_admin_control_all_keys' ) ) {
	function nadlan_admin_control_all_keys() {
		return array_merge( nadlan_admin_control_field_keys(), nadlan_admin_control_override_keys() );
	}
}

if ( ! function_exists( 'nadlan_admin_control_key_label' ) ) {
	function nadlan_admin_control_key_label( $key ) {
		$labels = array(
			'city'             => 'עיר',
			'lat'              => 'קו רוחב',
			'lng'              => 'קו אורך',
			'references'       => 'קישורי אסמכתה',
			'priority_weight'  => 'משקל מיקום',
			'is_pinned'        => 'נעיצה',
			'boost_multiplier' => 'מכפיל חשיפה',
			'reserved_slot'    => 'מקום שמור',
			'promo_until'      => 'תוקף קידום',
		);
		return isset( $labels[ $key ] ) ? $labels[ $key ] : $key;
	}
}

if ( ! function_exists( 'nadlan_admin_control_sanitize_bool' ) ) {
	function nadlan_admin_control_sanitize_bool( $value ) {
		if ( is_bool( $value ) ) { return $value ? 1 : 0; }
		$value = strtolower( trim( (string) $value ) );
		return in_array( $value, array( '1', 'yes', 'true', 'on' ), true ) ? 1 : 0;
	}
}

if ( ! function_exists( 'nadlan_admin_control_sanitize_references' ) ) {
	function nadlan_admin_control_sanitize_references( $value ) {
		if ( is_string( $value ) ) {
			$raw = trim( wp_unslash( $value ) );
			$decoded = json_decode( $raw, true );
			if ( is_array( $decoded ) ) {
				$value = $decoded;
			} else {
				$rows = array();
				foreach ( preg_split( '/\r\n|\r|\n/', $raw ) as $line ) {
					$line = trim( $line );
					if ( $line === '' ) { continue; }
					$parts = array_map( 'trim', explode( '|', $line, 2 ) );
					$rows[] = array(
						'label' => isset( $parts[0] ) ? $parts[0] : '',
						'url'   => isset( $parts[1] ) ? $parts[1] : $parts[0],
					);
				}
				$value = $rows;
			}
		}
		$out = array();
		foreach ( (array) $value as $row ) {
			$row = (array) $row;
			$url = esc_url_raw( (string) ( $row['url'] ?? '' ) );
			if ( $url === '' ) { continue; }
			$label = sanitize_text_field( (string) ( $row['label'] ?? '' ) );
			if ( $label === '' ) {
				$host = wp_parse_url( $url, PHP_URL_HOST );
				$label = $host ? $host : $url;
			}
			$out[] = array(
				'label' => mb_substr( $label, 0, 80 ),
				'url'   => $url,
			);
			if ( count( $out ) >= 20 ) { break; }
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_admin_control_sanitize_by_key' ) ) {
	function nadlan_admin_control_sanitize_by_key( $key, $value ) {
		$key = sanitize_key( (string) $key );
		switch ( $key ) {
			case 'city':
				return mb_substr( sanitize_text_field( (string) $value ), 0, 120 );
			case 'lat':
				if ( $value === '' || $value === null || ! is_numeric( $value ) ) { return ''; }
				return round( max( -90, min( 90, (float) $value ) ), 6 );
			case 'lng':
				if ( $value === '' || $value === null || ! is_numeric( $value ) ) { return ''; }
				return round( max( -180, min( 180, (float) $value ) ), 6 );
			case 'references':
				return nadlan_admin_control_sanitize_references( $value );
			case 'priority_weight':
				return max( 0, min( 100, (int) $value ) );
			case 'is_pinned':
			case 'reserved_slot':
				return nadlan_admin_control_sanitize_bool( $value );
			case 'boost_multiplier':
				if ( $value === '' || $value === null || ! is_numeric( $value ) ) { return ''; }
				return round( max( 1, min( 3, (float) $value ) ), 2 );
			case 'promo_until':
				if ( $value === '' || $value === null ) { return 0; }
				if ( is_numeric( $value ) ) { return max( 0, (int) $value ); }
				$ts = strtotime( sanitize_text_field( (string) $value ) );
				return $ts ? max( 0, (int) $ts ) : 0;
		}
		return sanitize_text_field( (string) $value );
	}
}

if ( ! function_exists( 'nadlan_admin_control_value_for_log' ) ) {
	function nadlan_admin_control_value_for_log( $value ) {
		if ( is_array( $value ) ) {
			$value = wp_json_encode( $value, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
		}
		if ( is_bool( $value ) ) { $value = $value ? '1' : '0'; }
		if ( $value === null ) { $value = ''; }
		return mb_substr( sanitize_text_field( (string) $value ), 0, 260 );
	}
}

if ( ! function_exists( 'nadlan_admin_control_impersonation' ) ) {
	function nadlan_admin_control_impersonation( $user_id = 0 ) {
		$user_id = $user_id ? (int) $user_id : get_current_user_id();
		if ( $user_id <= 0 ) { return array(); }
		$target  = (int) get_user_meta( $user_id, 'nadlan_impersonation_target', true );
		$expires = (int) get_user_meta( $user_id, 'nadlan_impersonation_expires', true );
		if ( ! $target || ! get_user_by( 'id', $target ) ) { return array(); }
		if ( $expires <= time() ) {
			delete_user_meta( $user_id, 'nadlan_impersonation_target' );
			delete_user_meta( $user_id, 'nadlan_impersonation_started' );
			delete_user_meta( $user_id, 'nadlan_impersonation_expires' );
			delete_user_meta( $user_id, 'nadlan_impersonation_write' );
			return array();
		}
		return array(
			'operator_id'   => $user_id,
			'target_id'     => $target,
			'started_at'    => (int) get_user_meta( $user_id, 'nadlan_impersonation_started', true ),
			'expires_at'    => $expires,
			'write_enabled' => (int) get_user_meta( $user_id, 'nadlan_impersonation_write', true ) === 1,
		);
	}
}

if ( ! function_exists( 'nadlan_admin_control_effective_user_id' ) ) {
	function nadlan_admin_control_effective_user_id( $user_id ) {
		if ( ! nadlan_admin_control_enabled() ) { return $user_id; }
		$session = nadlan_admin_control_impersonation();
		return ! empty( $session['target_id'] ) ? (int) $session['target_id'] : $user_id;
	}
}
add_filter( 'nadlan_effective_user_id', 'nadlan_admin_control_effective_user_id', 10, 1 );

if ( ! function_exists( 'nadlan_admin_control_audit' ) ) {
	function nadlan_admin_control_audit( $entry ) {
		$entry = wp_parse_args( (array) $entry, array(
			'ts'      => time(),
			'actor'   => get_current_user_id(),
			'action'  => 'update',
			'card_id' => 0,
			'field'   => '',
			'old'     => '',
			'new'     => '',
		) );
		$session = nadlan_admin_control_impersonation();
		$row = array(
			'ts'              => (int) $entry['ts'],
			'actor'           => (int) $entry['actor'],
			'impersonated_by' => ! empty( $session['operator_id'] ) ? (int) $session['operator_id'] : 0,
			'target_user'     => ! empty( $session['target_id'] ) ? (int) $session['target_id'] : 0,
			'action'          => sanitize_key( (string) $entry['action'] ),
			'card_id'         => (int) $entry['card_id'],
			'field'           => sanitize_key( (string) $entry['field'] ),
			'old'             => nadlan_admin_control_value_for_log( $entry['old'] ),
			'new'             => nadlan_admin_control_value_for_log( $entry['new'] ),
		);
		$log = get_option( 'nadlan_admin_audit', array() );
		if ( ! is_array( $log ) ) { $log = array(); }
		array_unshift( $log, $row );
		update_option( 'nadlan_admin_audit', array_slice( $log, 0, 2000 ), false );
		if ( function_exists( 'nadlan_log_event' ) ) {
			nadlan_log_event( 'admin_control', $row['action'], 'ok', array(
				'card_ref' => $row['card_id'],
				'field'    => $row['field'],
				'actor'    => $row['actor'],
			) );
		}
		return $row;
	}
}

if ( ! function_exists( 'nadlan_admin_control_sync_caps' ) ) {
	function nadlan_admin_control_sync_caps() {
		$enabled = nadlan_admin_control_enabled();
		if ( $enabled ) {
			$operator = get_role( 'nadlan_operator' );
			if ( ! $operator ) {
				add_role( 'nadlan_operator', 'מפעיל נדלן', array(
					'read'                    => true,
					NADLAN_ADMIN_CONTROL_CAP  => true,
					'edit_listings'           => true,
					'edit_published_listings' => true,
				) );
				$operator = get_role( 'nadlan_operator' );
			}
			if ( $operator ) {
				$operator->add_cap( NADLAN_ADMIN_CONTROL_CAP );
				$operator->add_cap( 'edit_listings' );
				$operator->add_cap( 'edit_published_listings' );
				$operator->remove_cap( 'manage_options' );
				$operator->remove_cap( 'edit_others_listings' );
			}
			$admin = get_role( 'administrator' );
			if ( $admin ) { $admin->add_cap( NADLAN_ADMIN_CONTROL_CAP ); }
			update_option( 'nadlan_admin_control_caps_state', 'on', false );
			return;
		}
		$admin = get_role( 'administrator' );
		if ( $admin ) { $admin->remove_cap( NADLAN_ADMIN_CONTROL_CAP ); }
		$operator = get_role( 'nadlan_operator' );
		if ( $operator ) { $operator->remove_cap( NADLAN_ADMIN_CONTROL_CAP ); }
		if ( $operator || get_option( 'nadlan_admin_control_caps_state', '' ) === 'on' ) {
			remove_role( 'nadlan_operator' );
		}
		update_option( 'nadlan_admin_control_caps_state', 'off', false );
	}
}
add_action( 'init', 'nadlan_admin_control_sync_caps', 20 );

if ( ! function_exists( 'nadlan_admin_control_uninstall' ) ) {
	function nadlan_admin_control_uninstall() {
		if ( function_exists( 'wp_roles' ) ) {
			foreach ( array_keys( wp_roles()->roles ) as $role_name ) {
				$role = get_role( $role_name );
				if ( $role ) { $role->remove_cap( NADLAN_ADMIN_CONTROL_CAP ); }
			}
		}
		remove_role( 'nadlan_operator' );
		delete_option( 'nadlan_admin_audit' );
		delete_option( 'nadlan_admin_control_caps_state' );
	}
}
register_uninstall_hook( dirname( __DIR__ ) . '/nadlan-config.php', 'nadlan_admin_control_uninstall' );

if ( ! function_exists( 'nadlan_admin_control_meta_auth' ) ) {
	function nadlan_admin_control_meta_auth( $allowed, $meta_key, $post_id, $user_id = 0, $cap = '', $caps = array() ) {
		if ( ! nadlan_admin_control_enabled() ) { return false; }
		$user_id = $user_id ? (int) $user_id : get_current_user_id();
		if ( ! $user_id || ! user_can( $user_id, NADLAN_ADMIN_CONTROL_CAP ) ) { return false; }
		$post = get_post( (int) $post_id );
		if ( ! $post || ! in_array( $post->post_type, nadlan_admin_control_card_post_types(), true ) ) { return false; }
		if ( user_can( $user_id, 'manage_options' ) ) { return true; }
		return user_can( $user_id, 'edit_post', (int) $post_id );
	}
}

if ( ! function_exists( 'nadlan_admin_control_register_meta' ) ) {
	function nadlan_admin_control_register_meta() {
		if ( ! nadlan_admin_control_enabled() ) { return; }
		$schemas = array(
			'city'             => array( 'type' => 'string' ),
			'lat'              => array( 'type' => 'number' ),
			'lng'              => array( 'type' => 'number' ),
			'references'       => array(
				'type'       => 'array',
				'show_rest'  => array(
					'schema' => array(
						'type'  => 'array',
						'items' => array(
							'type'       => 'object',
							'properties' => array(
								'label' => array( 'type' => 'string' ),
								'url'   => array( 'type' => 'string' ),
							),
						),
					),
				),
			),
			'priority_weight'  => array( 'type' => 'integer' ),
			'is_pinned'        => array( 'type' => 'boolean' ),
			'boost_multiplier' => array( 'type' => 'number' ),
			'reserved_slot'    => array( 'type' => 'boolean' ),
			'promo_until'      => array( 'type' => 'integer' ),
		);
		foreach ( nadlan_admin_control_card_post_types() as $pt ) {
			foreach ( $schemas as $key => $schema ) {
				$args = array(
					'single'            => true,
					'type'              => $schema['type'],
					'show_in_rest'      => isset( $schema['show_rest'] ) ? $schema['show_rest'] : true,
					'auth_callback'     => 'nadlan_admin_control_meta_auth',
					'sanitize_callback' => function ( $value, $meta_key ) {
						return nadlan_admin_control_sanitize_by_key( $meta_key, $value );
					},
				);
				register_post_meta( $pt, $key, $args );
			}
		}
	}
}
add_action( 'init', 'nadlan_admin_control_register_meta', 30 );

if ( ! function_exists( 'nadlan_admin_control_can_manage' ) ) {
	function nadlan_admin_control_can_manage() {
		return nadlan_admin_control_enabled() && current_user_can( NADLAN_ADMIN_CONTROL_CAP );
	}
}

if ( ! function_exists( 'nadlan_admin_control_can_write_card' ) ) {
	function nadlan_admin_control_can_write_card( $post_id ) {
		$post_id = (int) $post_id;
		$post = get_post( $post_id );
		if ( ! nadlan_admin_control_can_manage() || ! $post || ! in_array( $post->post_type, nadlan_admin_control_card_post_types(), true ) ) {
			return false;
		}
		if ( current_user_can( 'manage_options' ) ) { return true; }
		return current_user_can( 'edit_post', $post_id );
	}
}

if ( ! function_exists( 'nadlan_admin_control_impersonation_write_allowed' ) ) {
	function nadlan_admin_control_impersonation_write_allowed() {
		$session = nadlan_admin_control_impersonation();
		if ( empty( $session ) ) { return true; }
		return ! empty( $session['write_enabled'] );
	}
}

if ( ! function_exists( 'nadlan_admin_control_normalize_payload' ) ) {
	function nadlan_admin_control_normalize_payload( $payload ) {
		$payload = (array) $payload;
		if ( isset( $payload['fields'] ) && is_array( $payload['fields'] ) ) {
			$payload = array_merge( $payload, $payload['fields'] );
		}
		if ( isset( $payload['overrides'] ) && is_array( $payload['overrides'] ) ) {
			$payload = array_merge( $payload, $payload['overrides'] );
		}
		$out = array();
		foreach ( nadlan_admin_control_all_keys() as $key ) {
			if ( array_key_exists( $key, $payload ) ) {
				$out[ $key ] = nadlan_admin_control_sanitize_by_key( $key, $payload[ $key ] );
			}
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_admin_control_write_card' ) ) {
	function nadlan_admin_control_write_card( $post_id, $data, $action = 'update' ) {
		$post_id = (int) $post_id;
		if ( ! nadlan_admin_control_can_write_card( $post_id ) ) {
			return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
		}
		if ( ! nadlan_admin_control_impersonation_write_allowed() ) {
			return new WP_Error( 'impersonation_readonly', 'impersonation_readonly', array( 'status' => 403 ) );
		}
		$written = array();
		foreach ( (array) $data as $key => $value ) {
			if ( ! in_array( $key, nadlan_admin_control_all_keys(), true ) ) { continue; }
			$old = get_post_meta( $post_id, $key, true );
			$new = nadlan_admin_control_sanitize_by_key( $key, $value );
			if ( nadlan_admin_control_value_for_log( $old ) === nadlan_admin_control_value_for_log( $new ) ) {
				continue;
			}
			if ( $new === '' || ( $key === 'references' && empty( $new ) ) ) {
				delete_post_meta( $post_id, $key );
			} else {
				update_post_meta( $post_id, $key, $new );
			}
			nadlan_admin_control_audit( array(
				'action'  => $action,
				'card_id' => $post_id,
				'field'   => $key,
				'old'     => $old,
				'new'     => $new,
			) );
			$written[] = $key;
		}
		delete_transient( 'nadlan_sp_block_v3' );
		delete_transient( 'nadlan_sp_block_v4' );
		if ( function_exists( 'nadlan_auction_clear_rank_cache' ) ) {
			nadlan_auction_clear_rank_cache();
		}
		return array( 'ok' => true, 'post_id' => $post_id, 'written' => $written );
	}
}

if ( ! function_exists( 'nadlan_admin_control_card_snapshot' ) ) {
	function nadlan_admin_control_card_snapshot( $post_id ) {
		$post_id = (int) $post_id;
		$post = get_post( $post_id );
		if ( ! $post || ! in_array( $post->post_type, nadlan_admin_control_card_post_types(), true ) ) {
			return array();
		}
		$meta = array();
		foreach ( nadlan_admin_control_all_keys() as $key ) {
			$meta[ $key ] = get_post_meta( $post_id, $key, true );
		}
		return array(
			'id'            => $post_id,
			'title'         => get_the_title( $post_id ),
			'post_type'     => $post->post_type,
			'post_status'   => $post->post_status,
			'owner_user_id' => (int) get_post_meta( $post_id, 'owner_user_id', true ),
			'paid_tier'     => (string) get_post_meta( $post_id, 'paid_tier', true ),
			'permalink'     => get_permalink( $post_id ),
			'edit_link'     => get_edit_post_link( $post_id, 'raw' ),
			'meta'          => $meta,
		);
	}
}

if ( ! function_exists( 'nadlan_admin_control_require_rest_nonce' ) ) {
	function nadlan_admin_control_require_rest_nonce( WP_REST_Request $request ) {
		$nonce = (string) $request->get_header( 'x_wp_nonce' );
		if ( $nonce === '' ) { $nonce = (string) $request->get_param( '_wpnonce' ); }
		return $nonce !== '' && wp_verify_nonce( $nonce, 'wp_rest' );
	}
}

if ( ! function_exists( 'nadlan_admin_control_rest_permission' ) ) {
	function nadlan_admin_control_rest_permission() {
		if ( ! nadlan_admin_control_enabled() ) {
			return new WP_Error( 'admin_control_disabled', 'admin_control_disabled', array( 'status' => 404 ) );
		}
		if ( ! is_user_logged_in() || ! current_user_can( NADLAN_ADMIN_CONTROL_CAP ) ) {
			return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
		}
		return true;
	}
}

if ( ! function_exists( 'nadlan_admin_control_list_cards' ) ) {
	function nadlan_admin_control_list_cards( $request ) {
		$type = sanitize_key( (string) $request->get_param( 'type' ) );
		$city = sanitize_text_field( (string) $request->get_param( 'city' ) );
		$search = sanitize_text_field( (string) $request->get_param( 's' ) );
		$limit = max( 1, min( 100, (int) ( $request->get_param( 'limit' ) ?: 50 ) ) );
		$post_types = in_array( $type, nadlan_admin_control_card_post_types(), true ) ? array( $type ) : nadlan_admin_control_card_post_types();
		$args = array(
			'post_type'      => $post_types,
			'post_status'    => array( 'publish', 'pending', 'draft', 'private' ),
			'posts_per_page' => $limit,
			'orderby'        => 'modified',
			'order'          => 'DESC',
			's'              => $search,
		);
		$meta_query = array();
		if ( $city !== '' ) {
			$meta_query[] = array( 'key' => 'city', 'value' => $city, 'compare' => 'LIKE' );
		}
		if ( ! current_user_can( 'manage_options' ) ) {
			$meta_query[] = array( 'key' => 'owner_user_id', 'value' => get_current_user_id(), 'type' => 'NUMERIC' );
		}
		if ( count( $meta_query ) > 1 ) {
			$meta_query['relation'] = 'AND';
		}
		if ( $meta_query ) {
			$args['meta_query'] = $meta_query;
		}
		$q = new WP_Query( $args );
		$cards = array();
		foreach ( (array) $q->posts as $post ) {
			$cards[] = nadlan_admin_control_card_snapshot( $post->ID );
		}
		wp_reset_postdata();
		return array( 'ok' => true, 'cards' => $cards, 'found' => (int) $q->found_posts );
	}
}

if ( ! function_exists( 'nadlan_admin_control_rest_write_card' ) ) {
	function nadlan_admin_control_rest_write_card( WP_REST_Request $request ) {
		if ( ! nadlan_admin_control_require_rest_nonce( $request ) ) {
			return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
		}
		$payload = $request->get_json_params();
		if ( ! is_array( $payload ) ) { $payload = $request->get_params(); }
		$result = nadlan_admin_control_write_card( (int) $request['id'], nadlan_admin_control_normalize_payload( $payload ), 'rest_update' );
		if ( is_wp_error( $result ) ) { return $result; }
		$result['card'] = nadlan_admin_control_card_snapshot( (int) $request['id'] );
		return $result;
	}
}

if ( ! function_exists( 'nadlan_admin_control_start_impersonation' ) ) {
	function nadlan_admin_control_start_impersonation( WP_REST_Request $request ) {
		if ( ! nadlan_admin_control_require_rest_nonce( $request ) ) {
			return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
		}
		if ( ! current_user_can( 'manage_options' ) ) {
			return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
		}
		$target = absint( $request->get_param( 'user_id' ) );
		$user = $target ? get_user_by( 'id', $target ) : false;
		if ( ! $user ) { return new WP_Error( 'bad_user', 'bad_user', array( 'status' => 422 ) ); }
		$duration = max( 60, min( 30 * MINUTE_IN_SECONDS, (int) ( $request->get_param( 'duration' ) ?: 30 * MINUTE_IN_SECONDS ) ) );
		$operator = get_current_user_id();
		update_user_meta( $operator, 'nadlan_impersonation_target', $target );
		update_user_meta( $operator, 'nadlan_impersonation_started', time() );
		update_user_meta( $operator, 'nadlan_impersonation_expires', time() + $duration );
		update_user_meta( $operator, 'nadlan_impersonation_write', 0 );
		nadlan_admin_control_audit( array(
			'action' => 'impersonation_start',
			'field'  => 'impersonation',
			'old'    => '',
			'new'    => 'target_user:' . $target,
		) );
		return array( 'ok' => true, 'session' => nadlan_admin_control_impersonation( $operator ) );
	}
}

if ( ! function_exists( 'nadlan_admin_control_end_impersonation' ) ) {
	function nadlan_admin_control_end_impersonation( WP_REST_Request $request ) {
		if ( ! nadlan_admin_control_require_rest_nonce( $request ) ) {
			return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
		}
		$operator = get_current_user_id();
		$session = nadlan_admin_control_impersonation( $operator );
		if ( ! empty( $session ) ) {
			nadlan_admin_control_audit( array(
				'action' => 'impersonation_end',
				'field'  => 'impersonation',
				'old'    => 'target_user:' . (int) $session['target_id'],
				'new'    => '',
			) );
		}
		delete_user_meta( $operator, 'nadlan_impersonation_target' );
		delete_user_meta( $operator, 'nadlan_impersonation_started' );
		delete_user_meta( $operator, 'nadlan_impersonation_expires' );
		delete_user_meta( $operator, 'nadlan_impersonation_write' );
		return array( 'ok' => true );
	}
}

if ( ! function_exists( 'nadlan_admin_control_toggle_impersonation_write' ) ) {
	function nadlan_admin_control_toggle_impersonation_write( WP_REST_Request $request ) {
		if ( ! nadlan_admin_control_require_rest_nonce( $request ) ) {
			return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
		}
		if ( ! current_user_can( 'manage_options' ) ) {
			return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
		}
		$operator = get_current_user_id();
		$session = nadlan_admin_control_impersonation( $operator );
		if ( empty( $session ) ) { return new WP_Error( 'no_session', 'no_session', array( 'status' => 404 ) ); }
		$enabled = nadlan_admin_control_sanitize_bool( $request->get_param( 'write_enabled' ) );
		update_user_meta( $operator, 'nadlan_impersonation_write', $enabled );
		nadlan_admin_control_audit( array(
			'action' => 'impersonation_write_toggle',
			'field'  => 'impersonation_write',
			'old'    => ! empty( $session['write_enabled'] ) ? '1' : '0',
			'new'    => $enabled ? '1' : '0',
		) );
		return array( 'ok' => true, 'session' => nadlan_admin_control_impersonation( $operator ) );
	}
}

add_action( 'rest_api_init', function () {
	if ( ! nadlan_admin_control_enabled() ) { return; }
	register_rest_route( 'nadlan/v1', '/admin-control/cards', array(
		'methods'             => 'GET',
		'permission_callback' => 'nadlan_admin_control_rest_permission',
		'callback'            => 'nadlan_admin_control_list_cards',
	) );
	register_rest_route( 'nadlan/v1', '/admin-control/card/(?P<id>\d+)', array(
		array(
			'methods'             => 'GET',
			'permission_callback' => 'nadlan_admin_control_rest_permission',
			'callback'            => function ( $request ) {
				if ( ! nadlan_admin_control_can_write_card( (int) $request['id'] ) && ! current_user_can( 'manage_options' ) ) {
					return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
				}
				return array( 'ok' => true, 'card' => nadlan_admin_control_card_snapshot( (int) $request['id'] ) );
			},
		),
		array(
			'methods'             => 'POST',
			'permission_callback' => 'nadlan_admin_control_rest_permission',
			'callback'            => 'nadlan_admin_control_rest_write_card',
		),
	) );
	register_rest_route( 'nadlan/v1', '/admin-control/bulk', array(
		'methods'             => 'POST',
		'permission_callback' => 'nadlan_admin_control_rest_permission',
		'callback'            => 'nadlan_admin_control_rest_bulk',
	) );
	register_rest_route( 'nadlan/v1', '/admin-control/impersonate/start', array(
		'methods'             => 'POST',
		'permission_callback' => 'nadlan_admin_control_rest_permission',
		'callback'            => 'nadlan_admin_control_start_impersonation',
	) );
	register_rest_route( 'nadlan/v1', '/admin-control/impersonate/end', array(
		'methods'             => 'POST',
		'permission_callback' => 'nadlan_admin_control_rest_permission',
		'callback'            => 'nadlan_admin_control_end_impersonation',
	) );
	register_rest_route( 'nadlan/v1', '/admin-control/impersonate/write-toggle', array(
		'methods'             => 'POST',
		'permission_callback' => 'nadlan_admin_control_rest_permission',
		'callback'            => 'nadlan_admin_control_toggle_impersonation_write',
	) );
} );

add_filter( 'rest_pre_dispatch', function ( $result, $server, $request ) {
	if ( strtoupper( $request->get_method() ) === 'GET' ) { return $result; }
	$session = nadlan_admin_control_impersonation();
	if ( empty( $session ) || ! empty( $session['write_enabled'] ) ) { return $result; }
	$route = (string) $request->get_route();
	if ( preg_match( '#^/nadlan/v1/admin-control/impersonate/(end|write-toggle)$#', $route ) ) {
		return $result;
	}
	if ( strpos( $route, '/nadlan/v1/' ) === 0 ) {
		return new WP_Error( 'impersonation_readonly', 'impersonation_readonly', array( 'status' => 403 ) );
	}
	return $result;
}, 8, 3 );

if ( ! function_exists( 'nadlan_admin_control_placement_clauses' ) ) {
	function nadlan_admin_control_placement_clauses( $clauses, $query ) {
		if ( ! nadlan_admin_control_enabled() || ! $query->get( 'nadlan_paid_placement_boost' ) ) {
			return $clauses;
		}
		global $wpdb;
		$aliases = array(
			'w' => array( 'alias' => 'nadlan_admin_weight_pm', 'key' => 'priority_weight' ),
			'p' => array( 'alias' => 'nadlan_admin_pin_pm', 'key' => 'is_pinned' ),
			'b' => array( 'alias' => 'nadlan_admin_boost_pm', 'key' => 'boost_multiplier' ),
			'r' => array( 'alias' => 'nadlan_admin_reserved_pm', 'key' => 'reserved_slot' ),
			'u' => array( 'alias' => 'nadlan_admin_until_pm', 'key' => 'promo_until' ),
		);
		foreach ( $aliases as $row ) {
			$alias = $row['alias'];
			if ( strpos( $clauses['join'], " AS {$alias} " ) === false ) {
				$clauses['join'] .= $wpdb->prepare(
					" LEFT JOIN {$wpdb->postmeta} AS {$alias} ON ({$wpdb->posts}.ID = {$alias}.post_id AND {$alias}.meta_key = %s)",
					$row['key']
				);
			}
		}
		$now = time();
		$until = $aliases['u']['alias'];
		$active = "(COALESCE(CAST({$until}.meta_value AS UNSIGNED),0)=0 OR CAST({$until}.meta_value AS UNSIGNED) >= {$now})";
		$weight = "LEAST(100,GREATEST(0,COALESCE(CAST({$aliases['w']['alias']}.meta_value AS SIGNED),0)))";
		$boost = "CASE WHEN {$active} AND CAST({$aliases['b']['alias']}.meta_value AS DECIMAL(4,2)) BETWEEN 1 AND 3 THEN CAST({$aliases['b']['alias']}.meta_value AS DECIMAL(4,2)) ELSE 1 END";
		$reserved = "CASE WHEN {$active} AND {$aliases['r']['alias']}.meta_value IN ('1','yes','true','on') THEN 1 ELSE 0 END";
		$pinned = "CASE WHEN {$active} AND {$aliases['p']['alias']}.meta_value IN ('1','yes','true','on') THEN 1 ELSE 0 END";
		$override_order = "{$reserved} DESC, {$pinned} DESC, ({$weight} * {$boost}) DESC";
		$clauses['orderby'] = trim( (string) $clauses['orderby'] ) !== '' ? $override_order . ', ' . $clauses['orderby'] : $override_order;
		return $clauses;
	}
}
add_filter( 'posts_clauses', 'nadlan_admin_control_placement_clauses', 27, 2 );

if ( ! function_exists( 'nadlan_admin_control_schedule_cron' ) ) {
	function nadlan_admin_control_schedule_cron() {
		if ( nadlan_admin_control_enabled() && ! wp_next_scheduled( 'nadlan_admin_control_expire_overrides' ) ) {
			wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', 'nadlan_admin_control_expire_overrides' );
		}
	}
}
add_action( 'init', 'nadlan_admin_control_schedule_cron', 40 );

if ( ! function_exists( 'nadlan_admin_control_expire_overrides' ) ) {
	function nadlan_admin_control_expire_overrides() {
		if ( ! nadlan_admin_control_enabled() ) { return; }
		$now = time();
		$q = new WP_Query( array(
			'post_type'      => nadlan_admin_control_card_post_types(),
			'post_status'    => 'any',
			'fields'         => 'ids',
			'posts_per_page' => 200,
			'meta_query'     => array(
				array( 'key' => 'promo_until', 'value' => array( 1, $now - 1 ), 'compare' => 'BETWEEN', 'type' => 'NUMERIC' ),
			),
		) );
		foreach ( (array) $q->posts as $card_id ) {
			$old = array();
			foreach ( nadlan_admin_control_override_keys() as $key ) {
				$old[ $key ] = get_post_meta( $card_id, $key, true );
				delete_post_meta( $card_id, $key );
			}
			nadlan_admin_control_audit( array(
				'action'  => 'override_expired',
				'card_id' => (int) $card_id,
				'field'   => 'placement_overrides',
				'old'     => $old,
				'new'     => '',
			) );
		}
		wp_reset_postdata();
		if ( function_exists( 'nadlan_auction_clear_rank_cache' ) ) {
			nadlan_auction_clear_rank_cache();
		}
	}
}
add_action( 'nadlan_admin_control_expire_overrides', 'nadlan_admin_control_expire_overrides' );

if ( ! function_exists( 'nadlan_admin_control_meta_box' ) ) {
	function nadlan_admin_control_meta_box() {
		if ( ! nadlan_admin_control_enabled() ) { return; }
		foreach ( nadlan_admin_control_card_post_types() as $pt ) {
			add_meta_box( 'nadlan_admin_control_box', 'בקרת מפעיל', 'nadlan_admin_control_render_meta_box', $pt, 'side', 'default' );
		}
	}
}
add_action( 'add_meta_boxes', 'nadlan_admin_control_meta_box' );

if ( ! function_exists( 'nadlan_admin_control_render_meta_box' ) ) {
	function nadlan_admin_control_render_meta_box( $post ) {
		if ( ! nadlan_admin_control_can_write_card( $post->ID ) ) {
			echo '<p>אין הרשאה.</p>';
			return;
		}
		wp_nonce_field( 'nadlan_admin_control_card_' . $post->ID, 'nadlan_admin_control_nonce' );
		$refs = get_post_meta( $post->ID, 'references', true );
		if ( ! is_array( $refs ) ) { $refs = array(); }
		?>
		<p><label>עיר<br><input type="text" name="nadlan_admin_control[city]" value="<?php echo esc_attr( get_post_meta( $post->ID, 'city', true ) ); ?>" style="width:100%"></label></p>
		<p><label>קו רוחב<br><input type="number" step="0.000001" name="nadlan_admin_control[lat]" value="<?php echo esc_attr( get_post_meta( $post->ID, 'lat', true ) ); ?>" style="width:100%"></label></p>
		<p><label>קו אורך<br><input type="number" step="0.000001" name="nadlan_admin_control[lng]" value="<?php echo esc_attr( get_post_meta( $post->ID, 'lng', true ) ); ?>" style="width:100%"></label></p>
		<p><label>משקל מיקום 0-100<br><input type="number" min="0" max="100" name="nadlan_admin_control[priority_weight]" value="<?php echo esc_attr( get_post_meta( $post->ID, 'priority_weight', true ) ); ?>" style="width:100%"></label></p>
		<input type="hidden" name="nadlan_admin_control[is_pinned]" value="0">
		<input type="hidden" name="nadlan_admin_control[reserved_slot]" value="0">
		<p><label><input type="checkbox" name="nadlan_admin_control[is_pinned]" value="1" <?php checked( (int) get_post_meta( $post->ID, 'is_pinned', true ), 1 ); ?>> נעוץ</label></p>
		<p><label><input type="checkbox" name="nadlan_admin_control[reserved_slot]" value="1" <?php checked( (int) get_post_meta( $post->ID, 'reserved_slot', true ), 1 ); ?>> מקום שמור</label></p>
		<p><label>מכפיל חשיפה 1-3<br><input type="number" step="0.1" min="1" max="3" name="nadlan_admin_control[boost_multiplier]" value="<?php echo esc_attr( get_post_meta( $post->ID, 'boost_multiplier', true ) ); ?>" style="width:100%"></label></p>
		<p><label>תוקף קידום Unix<br><input type="number" min="0" name="nadlan_admin_control[promo_until]" value="<?php echo esc_attr( get_post_meta( $post->ID, 'promo_until', true ) ); ?>" style="width:100%"></label></p>
		<p><label>קישורי אסמכתה JSON<br><textarea name="nadlan_admin_control[references]" rows="5" style="width:100%"><?php echo esc_textarea( wp_json_encode( $refs, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) ); ?></textarea></label></p>
		<?php
	}
}

if ( ! function_exists( 'nadlan_admin_control_save_meta_box' ) ) {
	function nadlan_admin_control_save_meta_box( $post_id, $post ) {
		if ( ! nadlan_admin_control_enabled() || wp_is_post_autosave( $post_id ) || wp_is_post_revision( $post_id ) ) { return; }
		if ( ! $post || ! in_array( $post->post_type, nadlan_admin_control_card_post_types(), true ) ) { return; }
		$nonce = isset( $_POST['nadlan_admin_control_nonce'] ) ? sanitize_text_field( wp_unslash( $_POST['nadlan_admin_control_nonce'] ) ) : '';
		if ( $nonce === '' || ! wp_verify_nonce( $nonce, 'nadlan_admin_control_card_' . $post_id ) ) { return; }
		$raw = isset( $_POST['nadlan_admin_control'] ) && is_array( $_POST['nadlan_admin_control'] ) ? wp_unslash( $_POST['nadlan_admin_control'] ) : array();
		nadlan_admin_control_write_card( $post_id, nadlan_admin_control_normalize_payload( $raw ), 'meta_box_update' );
	}
}
add_action( 'save_post', 'nadlan_admin_control_save_meta_box', 20, 2 );

if ( ! function_exists( 'nadlan_admin_control_rest_bulk' ) ) {
	function nadlan_admin_control_rest_bulk( WP_REST_Request $request ) {
		if ( ! nadlan_admin_control_require_rest_nonce( $request ) ) {
			return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
		}
		$p = $request->get_json_params();
		if ( ! is_array( $p ) ) { $p = $request->get_params(); }
		return nadlan_admin_control_bulk_apply( $p );
	}
}

if ( ! function_exists( 'nadlan_admin_control_bulk_apply' ) ) {
	function nadlan_admin_control_bulk_apply( $payload ) {
		$payload = (array) $payload;
		$ids = isset( $payload['card_ids'] ) && is_array( $payload['card_ids'] ) ? array_map( 'absint', $payload['card_ids'] ) : array();
		$ids = array_values( array_unique( array_filter( $ids ) ) );
		$action = sanitize_key( (string) ( $payload['bulk_action'] ?? $payload['action'] ?? '' ) );
		if ( ! $ids || ! in_array( $action, array( 'pin', 'unpin', 'clear_overrides', 'set_weight', 'delete' ), true ) ) {
			return new WP_Error( 'invalid_bulk', 'invalid_bulk', array( 'status' => 422 ) );
		}
		if ( count( $ids ) > 20 || $action === 'delete' ) {
			$confirm = sanitize_text_field( (string) ( $payload['confirm'] ?? '' ) );
			if ( $confirm !== 'CONFIRM' ) {
				return new WP_Error( 'confirm_required', 'confirm_required', array( 'status' => 409 ) );
			}
		}
		if ( ! nadlan_admin_control_impersonation_write_allowed() ) {
			return new WP_Error( 'impersonation_readonly', 'impersonation_readonly', array( 'status' => 403 ) );
		}
		$undo = array();
		$changed = 0;
		foreach ( $ids as $id ) {
			if ( ! nadlan_admin_control_can_write_card( $id ) ) { continue; }
			if ( $action !== 'delete' ) {
				$undo[ $id ] = array();
				foreach ( nadlan_admin_control_all_keys() as $key ) {
					$undo[ $id ][ $key ] = get_post_meta( $id, $key, true );
				}
			}
			if ( $action === 'pin' ) {
				$res = nadlan_admin_control_write_card( $id, array( 'is_pinned' => 1 ), 'bulk_pin' );
			} elseif ( $action === 'unpin' ) {
				$res = nadlan_admin_control_write_card( $id, array( 'is_pinned' => 0 ), 'bulk_unpin' );
			} elseif ( $action === 'set_weight' ) {
				$res = nadlan_admin_control_write_card( $id, array( 'priority_weight' => (int) ( $payload['priority_weight'] ?? 0 ) ), 'bulk_weight' );
			} elseif ( $action === 'clear_overrides' ) {
				$old = array();
				foreach ( nadlan_admin_control_override_keys() as $key ) {
					$old[ $key ] = get_post_meta( $id, $key, true );
					delete_post_meta( $id, $key );
				}
				nadlan_admin_control_audit( array( 'action' => 'bulk_clear_overrides', 'card_id' => $id, 'field' => 'placement_overrides', 'old' => $old, 'new' => '' ) );
				$res = array( 'ok' => true );
			} else {
				if ( ! current_user_can( 'delete_post', $id ) && ! current_user_can( 'manage_options' ) ) { continue; }
				$old_status = get_post_status( $id );
				wp_trash_post( $id );
				nadlan_admin_control_audit( array( 'action' => 'bulk_trash', 'card_id' => $id, 'field' => 'post_status', 'old' => $old_status, 'new' => 'trash' ) );
				$res = array( 'ok' => true );
			}
			if ( ! is_wp_error( $res ) ) { $changed++; }
		}
		$token = '';
		if ( $action !== 'delete' && $undo ) {
			$token = wp_generate_password( 18, false, false );
			set_transient( 'nadlan_admin_undo_' . get_current_user_id() . '_' . $token, $undo, 5 );
		}
		return array( 'ok' => true, 'changed' => $changed, 'undo_token' => $token );
	}
}

if ( ! function_exists( 'nadlan_admin_control_undo_bulk' ) ) {
	function nadlan_admin_control_undo_bulk( $token ) {
		$token = preg_replace( '/[^A-Za-z0-9]/', '', (string) $token );
		if ( $token === '' ) { return new WP_Error( 'bad_token', 'bad_token' ); }
		$key = 'nadlan_admin_undo_' . get_current_user_id() . '_' . $token;
		$undo = get_transient( $key );
		if ( ! is_array( $undo ) ) { return new WP_Error( 'expired', 'expired' ); }
		foreach ( $undo as $card_id => $fields ) {
			if ( ! nadlan_admin_control_can_write_card( (int) $card_id ) ) { continue; }
			foreach ( (array) $fields as $field => $old ) {
				if ( $old === '' || $old === array() ) {
					delete_post_meta( (int) $card_id, $field );
				} else {
					update_post_meta( (int) $card_id, $field, $old );
				}
			}
			nadlan_admin_control_audit( array( 'action' => 'bulk_undo', 'card_id' => (int) $card_id, 'field' => 'bulk', 'old' => 'changed', 'new' => 'restored' ) );
		}
		delete_transient( $key );
		return array( 'ok' => true );
	}
}

if ( ! function_exists( 'nadlan_admin_control_admin_menu' ) ) {
	function nadlan_admin_control_admin_menu() {
		if ( ! nadlan_admin_control_enabled() ) { return; }
		add_submenu_page( 'nadlan-ops', 'בקרת לקוחות', 'בקרת לקוחות', NADLAN_ADMIN_CONTROL_CAP, 'nadlan-admin-control', 'nadlan_admin_control_render_screen' );
	}
}
add_action( 'admin_menu', 'nadlan_admin_control_admin_menu', 30 );

if ( ! function_exists( 'nadlan_admin_control_handle_screen_post' ) ) {
	function nadlan_admin_control_handle_screen_post() {
		if ( empty( $_POST['nadlan_admin_control_action'] ) ) { return ''; }
		if ( ! current_user_can( NADLAN_ADMIN_CONTROL_CAP ) || ! check_admin_referer( 'nadlan_admin_control_screen' ) ) {
			return 'forbidden';
		}
		$action = sanitize_key( (string) wp_unslash( $_POST['nadlan_admin_control_action'] ) );
		if ( $action === 'save_card' ) {
			$card_id = absint( $_POST['card_id'] ?? 0 );
			$raw = isset( $_POST['nadlan_admin_control'] ) && is_array( $_POST['nadlan_admin_control'] ) ? wp_unslash( $_POST['nadlan_admin_control'] ) : array();
			$result = nadlan_admin_control_write_card( $card_id, nadlan_admin_control_normalize_payload( $raw ), 'screen_update' );
			return is_wp_error( $result ) ? $result->get_error_code() : 'saved';
		}
		if ( $action === 'bulk' ) {
			$result = nadlan_admin_control_bulk_apply( array(
				'card_ids'        => isset( $_POST['card_ids'] ) ? (array) wp_unslash( $_POST['card_ids'] ) : array(),
				'bulk_action'     => isset( $_POST['bulk_action'] ) ? wp_unslash( $_POST['bulk_action'] ) : '',
				'priority_weight' => isset( $_POST['priority_weight'] ) ? wp_unslash( $_POST['priority_weight'] ) : 0,
				'confirm'         => isset( $_POST['confirm'] ) ? wp_unslash( $_POST['confirm'] ) : '',
			) );
			if ( is_wp_error( $result ) ) { return $result->get_error_code(); }
			return 'bulk:' . (int) $result['changed'] . ':' . (string) $result['undo_token'];
		}
		if ( $action === 'undo' ) {
			$result = nadlan_admin_control_undo_bulk( isset( $_POST['undo_token'] ) ? wp_unslash( $_POST['undo_token'] ) : '' );
			return is_wp_error( $result ) ? $result->get_error_code() : 'undone';
		}
		if ( $action === 'impersonate_start' ) {
			if ( ! current_user_can( 'manage_options' ) ) { return 'forbidden'; }
			$target = absint( $_POST['target_user_id'] ?? 0 );
			if ( ! $target || ! get_user_by( 'id', $target ) ) { return 'bad_user'; }
			$operator = get_current_user_id();
			update_user_meta( $operator, 'nadlan_impersonation_target', $target );
			update_user_meta( $operator, 'nadlan_impersonation_started', time() );
			update_user_meta( $operator, 'nadlan_impersonation_expires', time() + 30 * MINUTE_IN_SECONDS );
			update_user_meta( $operator, 'nadlan_impersonation_write', 0 );
			nadlan_admin_control_audit( array( 'action' => 'impersonation_start', 'field' => 'impersonation', 'old' => '', 'new' => 'target_user:' . $target ) );
			return 'impersonation_started';
		}
		if ( $action === 'impersonate_end' ) {
			$operator = get_current_user_id();
			$session = nadlan_admin_control_impersonation( $operator );
			if ( $session ) {
				nadlan_admin_control_audit( array( 'action' => 'impersonation_end', 'field' => 'impersonation', 'old' => 'target_user:' . (int) $session['target_id'], 'new' => '' ) );
			}
			delete_user_meta( $operator, 'nadlan_impersonation_target' );
			delete_user_meta( $operator, 'nadlan_impersonation_started' );
			delete_user_meta( $operator, 'nadlan_impersonation_expires' );
			delete_user_meta( $operator, 'nadlan_impersonation_write' );
			return 'impersonation_ended';
		}
		if ( $action === 'impersonate_toggle_write' ) {
			if ( ! current_user_can( 'manage_options' ) ) { return 'forbidden'; }
			$operator = get_current_user_id();
			$session = nadlan_admin_control_impersonation( $operator );
			if ( ! $session ) { return 'no_session'; }
			$new = empty( $session['write_enabled'] ) ? 1 : 0;
			update_user_meta( $operator, 'nadlan_impersonation_write', $new );
			nadlan_admin_control_audit( array( 'action' => 'impersonation_write_toggle', 'field' => 'impersonation_write', 'old' => ! empty( $session['write_enabled'] ) ? '1' : '0', 'new' => $new ? '1' : '0' ) );
			return 'impersonation_write_' . ( $new ? 'on' : 'off' );
		}
		return '';
	}
}

if ( ! function_exists( 'nadlan_admin_control_screen_cards' ) ) {
	function nadlan_admin_control_screen_cards() {
		$type = isset( $_GET['type'] ) ? sanitize_key( wp_unslash( $_GET['type'] ) ) : '';
		$city = isset( $_GET['city'] ) ? sanitize_text_field( wp_unslash( $_GET['city'] ) ) : '';
		$s = isset( $_GET['s'] ) ? sanitize_text_field( wp_unslash( $_GET['s'] ) ) : '';
		$args = array(
			'post_type'      => in_array( $type, nadlan_admin_control_card_post_types(), true ) ? array( $type ) : nadlan_admin_control_card_post_types(),
			'post_status'    => array( 'publish', 'pending', 'draft', 'private' ),
			'posts_per_page' => 50,
			'orderby'        => 'modified',
			'order'          => 'DESC',
			's'              => $s,
		);
		$meta_query = array();
		if ( $city !== '' ) {
			$meta_query[] = array( 'key' => 'city', 'value' => $city, 'compare' => 'LIKE' );
		}
		if ( ! current_user_can( 'manage_options' ) ) {
			$meta_query[] = array( 'key' => 'owner_user_id', 'value' => get_current_user_id(), 'type' => 'NUMERIC' );
		}
		if ( count( $meta_query ) > 1 ) {
			$meta_query['relation'] = 'AND';
		}
		if ( $meta_query ) {
			$args['meta_query'] = $meta_query;
		}
		$q = new WP_Query( $args );
		$posts = $q->posts;
		wp_reset_postdata();
		return $posts;
	}
}

if ( ! function_exists( 'nadlan_admin_control_render_screen' ) ) {
	function nadlan_admin_control_render_screen() {
		if ( ! current_user_can( NADLAN_ADMIN_CONTROL_CAP ) ) { wp_die( 'forbidden' ); }
		$notice = nadlan_admin_control_handle_screen_post();
		$cards = nadlan_admin_control_screen_cards();
		$selected = isset( $_GET['card_id'] ) ? absint( $_GET['card_id'] ) : ( ! empty( $cards[0]->ID ) ? (int) $cards[0]->ID : 0 );
		$snapshot = $selected ? nadlan_admin_control_card_snapshot( $selected ) : array();
		$audit = array_slice( (array) get_option( 'nadlan_admin_audit', array() ), 0, 20 );
		$session = nadlan_admin_control_impersonation();
		$nonce = wp_create_nonce( 'wp_rest' );
		?>
		<div class="wrap" dir="rtl">
			<h1>בקרת לקוחות וכרטיסים</h1>
			<?php if ( $notice ) : ?>
				<div class="notice notice-info is-dismissible"><p><?php echo esc_html( $notice ); ?></p>
				<?php if ( strpos( $notice, 'bulk:' ) === 0 ) :
					$parts = explode( ':', $notice );
					$token = isset( $parts[2] ) ? $parts[2] : '';
					if ( $token ) : ?>
						<form method="post" style="margin:8px 0">
							<?php wp_nonce_field( 'nadlan_admin_control_screen' ); ?>
							<input type="hidden" name="nadlan_admin_control_action" value="undo">
							<input type="hidden" name="undo_token" value="<?php echo esc_attr( $token ); ?>">
							<button class="button">בטל שינוי אחרון</button>
						</form>
					<?php endif;
				endif; ?>
				</div>
			<?php endif; ?>
			<?php if ( $session ) : ?>
				<div class="notice notice-warning"><p>צפייה כלקוח #<?php echo (int) $session['target_id']; ?>. מפעיל: <?php echo (int) $session['operator_id']; ?>. כתיבה: <?php echo $session['write_enabled'] ? 'פתוחה' : 'קריאה בלבד'; ?>. תוקף עד <?php echo esc_html( gmdate( 'H:i', (int) $session['expires_at'] ) ); ?> UTC.</p></div>
			<?php endif; ?>
			<p><code>X-WP-Nonce</code> ל-REST בבדיקה: <code><?php echo esc_html( $nonce ); ?></code></p>
			<form method="get" style="margin:16px 0">
				<input type="hidden" name="page" value="nadlan-admin-control">
				<input type="search" name="s" value="<?php echo esc_attr( isset( $_GET['s'] ) ? wp_unslash( $_GET['s'] ) : '' ); ?>" placeholder="חיפוש לפי שם">
				<input type="text" name="city" value="<?php echo esc_attr( isset( $_GET['city'] ) ? wp_unslash( $_GET['city'] ) : '' ); ?>" placeholder="עיר">
				<select name="type">
					<option value="">כל הסוגים</option>
					<?php foreach ( nadlan_admin_control_card_post_types() as $pt ) : ?>
						<option value="<?php echo esc_attr( $pt ); ?>" <?php selected( isset( $_GET['type'] ) ? sanitize_key( wp_unslash( $_GET['type'] ) ) : '', $pt ); ?>><?php echo esc_html( $pt ); ?></option>
					<?php endforeach; ?>
				</select>
				<button class="button">סנן</button>
			</form>

			<div style="display:grid;grid-template-columns:minmax(0,1.2fr) minmax(320px,.8fr);gap:18px;align-items:start">
				<form method="post">
					<?php wp_nonce_field( 'nadlan_admin_control_screen' ); ?>
					<input type="hidden" name="nadlan_admin_control_action" value="bulk">
					<table class="widefat striped">
						<thead><tr><th></th><th>כרטיס</th><th>עיר</th><th>משקל</th><th>נעוץ</th><th>תוקף</th></tr></thead>
						<tbody>
						<?php foreach ( $cards as $card ) : ?>
							<tr>
								<td><input type="checkbox" name="card_ids[]" value="<?php echo (int) $card->ID; ?>"></td>
								<td><a href="<?php echo esc_url( add_query_arg( array( 'page' => 'nadlan-admin-control', 'card_id' => (int) $card->ID ), admin_url( 'admin.php' ) ) ); ?>"><?php echo esc_html( get_the_title( $card ) ); ?></a><br><small>#<?php echo (int) $card->ID; ?> · <?php echo esc_html( $card->post_type ); ?></small></td>
								<td><?php echo esc_html( get_post_meta( $card->ID, 'city', true ) ); ?></td>
								<td><?php echo esc_html( get_post_meta( $card->ID, 'priority_weight', true ) ); ?></td>
								<td><?php echo (int) get_post_meta( $card->ID, 'is_pinned', true ) ? 'כן' : 'לא'; ?></td>
								<td><?php $until = (int) get_post_meta( $card->ID, 'promo_until', true ); echo esc_html( $until ? gmdate( 'Y-m-d', $until ) : 'ללא' ); ?></td>
							</tr>
						<?php endforeach; ?>
						<?php if ( ! $cards ) : ?>
							<tr><td colspan="6"><?php $empty = function_exists( 'nadlan_help_empty_state' ) ? nadlan_help_empty_state( 'nadlan-ops_page_nadlan-admin-control', 'cards_empty' ) : ''; echo $empty ? $empty : esc_html( 'אין כרטיסים להצגה' ); ?></td></tr>
						<?php endif; ?>
						</tbody>
					</table>
					<p>
						<select name="bulk_action">
							<option value="pin">נעץ</option>
							<option value="unpin">בטל נעיצה</option>
							<option value="clear_overrides">נקה קידומים</option>
							<option value="set_weight">קבע משקל</option>
							<option value="delete">העבר לפח</option>
						</select>
						<input type="number" name="priority_weight" min="0" max="100" placeholder="משקל">
						<input type="text" name="confirm" placeholder="CONFIRM לפעולה גדולה או מחיקה">
						<button class="button button-primary">החל</button>
					</p>
				</form>

				<div>
					<?php if ( $snapshot ) : $m = $snapshot['meta']; ?>
						<form method="post" style="background:#fff;border:1px solid #c3c4c7;padding:14px">
							<?php wp_nonce_field( 'nadlan_admin_control_screen' ); ?>
							<input type="hidden" name="nadlan_admin_control_action" value="save_card">
							<input type="hidden" name="card_id" value="<?php echo (int) $snapshot['id']; ?>">
							<h2 style="margin-top:0"><?php echo esc_html( $snapshot['title'] ); ?></h2>
							<p><label>עיר<br><input class="regular-text" name="nadlan_admin_control[city]" value="<?php echo esc_attr( $m['city'] ); ?>"></label></p>
							<p><label>קו רוחב<br><input type="number" step="0.000001" name="nadlan_admin_control[lat]" value="<?php echo esc_attr( $m['lat'] ); ?>"></label></p>
							<p><label>קו אורך<br><input type="number" step="0.000001" name="nadlan_admin_control[lng]" value="<?php echo esc_attr( $m['lng'] ); ?>"></label></p>
							<p><label>משקל 0-100<br><input type="number" min="0" max="100" name="nadlan_admin_control[priority_weight]" value="<?php echo esc_attr( $m['priority_weight'] ); ?>"></label></p>
							<input type="hidden" name="nadlan_admin_control[is_pinned]" value="0">
							<input type="hidden" name="nadlan_admin_control[reserved_slot]" value="0">
							<p><label><input type="checkbox" name="nadlan_admin_control[is_pinned]" value="1" <?php checked( (int) $m['is_pinned'], 1 ); ?>> נעוץ</label> <label><input type="checkbox" name="nadlan_admin_control[reserved_slot]" value="1" <?php checked( (int) $m['reserved_slot'], 1 ); ?>> מקום שמור</label></p>
							<p><label>מכפיל<br><input type="number" step="0.1" min="1" max="3" name="nadlan_admin_control[boost_multiplier]" value="<?php echo esc_attr( $m['boost_multiplier'] ); ?>"></label></p>
							<p><label>תוקף Unix<br><input type="number" min="0" name="nadlan_admin_control[promo_until]" value="<?php echo esc_attr( $m['promo_until'] ); ?>"></label></p>
							<p><label>אסמכתאות JSON<br><textarea class="large-text code" rows="7" name="nadlan_admin_control[references]"><?php echo esc_textarea( wp_json_encode( is_array( $m['references'] ) ? $m['references'] : array(), JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) ); ?></textarea></label></p>
							<p><button class="button button-primary">שמור כרטיס</button> <a class="button" href="<?php echo esc_url( $snapshot['permalink'] ); ?>" target="_blank">פתח</a></p>
						</form>
					<?php endif; ?>

					<div style="background:#fff;border:1px solid #c3c4c7;padding:14px;margin-top:14px">
						<h2 style="margin-top:0">צפייה כלקוח</h2>
						<p class="description">הפעלת הצפייה אינה מחליפה הרשאות. כתיבה חסומה עד שמפעילים אותה במפורש.</p>
						<form method="post" style="margin-bottom:8px">
							<?php wp_nonce_field( 'nadlan_admin_control_screen' ); ?>
							<input type="hidden" name="nadlan_admin_control_action" value="impersonate_start">
							<input type="number" min="1" name="target_user_id" placeholder="מזהה משתמש">
							<button class="button">צפה כמפרסם</button>
						</form>
						<?php if ( $session ) : ?>
							<form method="post" style="display:inline-block;margin-inline-end:6px">
								<?php wp_nonce_field( 'nadlan_admin_control_screen' ); ?>
								<input type="hidden" name="nadlan_admin_control_action" value="impersonate_toggle_write">
								<button class="button"><?php echo $session['write_enabled'] ? 'חזור לקריאה בלבד' : 'אפשר כתיבה זמנית'; ?></button>
							</form>
							<form method="post" style="display:inline-block">
								<?php wp_nonce_field( 'nadlan_admin_control_screen' ); ?>
								<input type="hidden" name="nadlan_admin_control_action" value="impersonate_end">
								<button class="button">סיים צפייה</button>
							</form>
						<?php endif; ?>
					</div>
				</div>
			</div>

			<h2>יומן שינויים אחרון</h2>
			<table class="widefat striped">
				<thead><tr><th>זמן</th><th>שחקן</th><th>פעולה</th><th>כרטיס</th><th>שדה</th><th>ישן</th><th>חדש</th></tr></thead>
				<tbody>
				<?php foreach ( $audit as $row ) : ?>
					<tr>
						<td><?php echo esc_html( gmdate( 'Y-m-d H:i', (int) ( $row['ts'] ?? 0 ) ) ); ?></td>
						<td><?php echo (int) ( $row['actor'] ?? 0 ); ?><?php if ( ! empty( $row['impersonated_by'] ) ) : ?> · Impersonated By <?php echo (int) $row['impersonated_by']; ?><?php endif; ?></td>
						<td><?php echo esc_html( $row['action'] ?? '' ); ?></td>
						<td><?php echo (int) ( $row['card_id'] ?? 0 ); ?></td>
						<td><?php echo esc_html( $row['field'] ?? '' ); ?></td>
						<td><?php echo esc_html( $row['old'] ?? '' ); ?></td>
						<td><?php echo esc_html( $row['new'] ?? '' ); ?></td>
					</tr>
				<?php endforeach; ?>
				<?php if ( ! $audit ) : ?>
					<tr><td colspan="7"><?php $empty = function_exists( 'nadlan_help_empty_state' ) ? nadlan_help_empty_state( 'nadlan-ops_page_nadlan-admin-control', 'audit_empty' ) : ''; echo $empty ? $empty : esc_html( 'אין עדיין שינויים ביומן' ); ?></td></tr>
				<?php endif; ?>
				</tbody>
			</table>
		</div>
		<?php
	}
}

add_action( 'admin_notices', function () {
	$session = nadlan_admin_control_impersonation();
	if ( empty( $session ) ) { return; }
	echo '<div class="notice notice-warning"><p>' . esc_html( 'מצב צפייה כלקוח פעיל. Impersonated By ' . (int) $session['operator_id'] . ' -> user ' . (int) $session['target_id'] . '. כתיבה: ' . ( $session['write_enabled'] ? 'פתוחה' : 'קריאה בלבד' ) ) . '</p></div>';
} );

add_action( 'wp_footer', function () {
	$session = nadlan_admin_control_impersonation();
	if ( empty( $session ) ) { return; }
	echo '<div dir="rtl" style="position:fixed;z-index:99999;inset-inline:16px;bottom:16px;background:#1b1a17;color:#fff;padding:10px 14px;border-radius:8px;text-align:center;font:600 13px system-ui">מצב צפייה כלקוח פעיל · Impersonated By ' . (int) $session['operator_id'] . ' · כתיבה: ' . esc_html( $session['write_enabled'] ? 'פתוחה' : 'קריאה בלבד' ) . '</div>';
} );

if ( ! function_exists( 'nadlan_admin_control_metrics' ) ) {
	function nadlan_admin_control_metrics() {
		$counts = count_users();
		$roles = (array) ( $counts['avail_roles'] ?? array() );
		$active_overrides = new WP_Query( array(
			'post_type'      => nadlan_admin_control_card_post_types(),
			'post_status'    => 'any',
			'fields'         => 'ids',
			'posts_per_page' => 1,
			'meta_query'     => array(
				'relation' => 'OR',
				array( 'key' => 'is_pinned', 'value' => '1' ),
				array( 'key' => 'reserved_slot', 'value' => '1' ),
				array( 'key' => 'priority_weight', 'value' => 0, 'compare' => '>', 'type' => 'NUMERIC' ),
			),
		) );
		$expired = new WP_Query( array(
			'post_type'      => nadlan_admin_control_card_post_types(),
			'post_status'    => 'any',
			'fields'         => 'ids',
			'posts_per_page' => 1,
			'meta_query'     => array( array( 'key' => 'promo_until', 'value' => array( 1, time() - 1 ), 'compare' => 'BETWEEN', 'type' => 'NUMERIC' ) ),
		) );
		$operator = get_role( 'nadlan_operator' );
		$admin = get_role( 'administrator' );
		$impersonations = get_users( array(
			'fields'     => 'ID',
			'meta_query' => array( array( 'key' => 'nadlan_impersonation_expires', 'value' => time(), 'compare' => '>=', 'type' => 'NUMERIC' ) ),
		) );
		return array(
			'loaded'                       => true,
			'enabled'                      => nadlan_admin_control_enabled(),
			'capability'                   => NADLAN_ADMIN_CONTROL_CAP,
			'admin_has_cap'                => $admin ? (bool) $admin->has_cap( NADLAN_ADMIN_CONTROL_CAP ) : false,
			'operator_role_exists'         => (bool) $operator,
			'operator_has_manage_options'  => $operator ? (bool) $operator->has_cap( 'manage_options' ) : false,
			'nadlan_operators'             => (int) ( $roles['nadlan_operator'] ?? 0 ),
			'audit_entries'                => count( (array) get_option( 'nadlan_admin_audit', array() ) ),
			'active_impersonations'        => count( $impersonations ),
			'active_overrides'             => (int) $active_overrides->found_posts,
			'expired_overrides_waiting'    => (int) $expired->found_posts,
			'cron_scheduled'               => (bool) wp_next_scheduled( 'nadlan_admin_control_expire_overrides' ),
		);
	}
}

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['admin_control'] = nadlan_admin_control_metrics();
	return $out;
} );

add_filter( 'nadlan_metrics_snapshot', function ( $snapshot ) {
	$snapshot['admin_control'] = nadlan_admin_control_metrics();
	return $snapshot;
} );

add_action( 'nadlan_ops_after_grid', function () {
	if ( ! current_user_can( 'manage_options' ) || ! function_exists( 'nadlan_admin_control_metrics' ) ) { return; }
	$m = nadlan_admin_control_metrics();
	?>
	<h2 style="margin-top:28px">Admin Control</h2>
	<div class="nlops-grid">
		<div class="nlops-card">
			<h2>Operator control</h2>
			<div class="nlops-row"><span>Flag</span><strong><?php echo $m['enabled'] ? 'ON' : 'OFF'; ?></strong></div>
			<div class="nlops-row"><span>Audit rows</span><strong><?php echo (int) $m['audit_entries']; ?></strong></div>
			<div class="nlops-row"><span>Active overrides</span><strong><?php echo (int) $m['active_overrides']; ?></strong></div>
			<div class="nlops-row"><span>Expired waiting</span><strong><?php echo (int) $m['expired_overrides_waiting']; ?></strong></div>
			<div class="nlops-row"><span>Impersonations</span><strong><?php echo (int) $m['active_impersonations']; ?></strong></div>
		</div>
	</div>
	<?php
}, 70 );
