<?php
/**
 * Governed flagship spatial co-tour transport.
 *
 * This is intentionally separate from the legacy shared co-tour module. It
 * transports a bounded flagship spatial-state snapshot only: no chat, audio,
 * video, recording, lead data or inventory. Room codes are manual opaque
 * locators. Authority is held only in a rotated, same-origin HttpOnly cookie;
 * browser JavaScript never receives or stores an authorization credential.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_flagship_cotour_now' ) ) {
	function nadlan_flagship_cotour_now() {
		return isset( $GLOBALS['nadlan_flagship_cotour_test_now'] )
			? (int) $GLOBALS['nadlan_flagship_cotour_test_now']
			: time();
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_exact_keys' ) ) {
	function nadlan_flagship_cotour_exact_keys( $value, $keys ) {
		if ( ! is_array( $value ) ) {
			return false;
		}
		$actual = array_keys( $value );
		sort( $actual, SORT_STRING );
		$keys = array_values( $keys );
		sort( $keys, SORT_STRING );
		return $actual === $keys;
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_number' ) ) {
	function nadlan_flagship_cotour_number( $value, $minimum, $maximum ) {
		return ( is_int( $value ) || is_float( $value ) )
			&& is_finite( (float) $value )
			&& $value >= $minimum
			&& $value <= $maximum;
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_identifier' ) ) {
	function nadlan_flagship_cotour_identifier( $value, $allow_empty = false ) {
		return is_string( $value )
			&& ( ( $allow_empty && '' === $value ) || preg_match( '/^[a-z0-9][a-z0-9-]{0,127}$/D', $value ) );
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_valid_camera' ) ) {
	function nadlan_flagship_cotour_valid_camera( $camera ) {
		if ( ! nadlan_flagship_cotour_exact_keys( $camera, array( 'azimuth', 'elevation', 'distance', 'target', 'fieldOfView' ) )
			|| ! nadlan_flagship_cotour_number( $camera['azimuth'], -M_PI * 1000, M_PI * 1000 )
			|| ! nadlan_flagship_cotour_number( $camera['elevation'], -0.08, 1.18 )
			|| ! nadlan_flagship_cotour_number( $camera['distance'], 0.000001, 1000000 )
			|| ! nadlan_flagship_cotour_number( $camera['fieldOfView'], 10, 100 )
			|| ! is_array( $camera['target'] ) || array_keys( $camera['target'] ) !== array( 0, 1, 2 ) ) {
			return false;
		}
		foreach ( $camera['target'] as $coordinate ) {
			if ( ! nadlan_flagship_cotour_number( $coordinate, -1000000, 1000000 ) ) {
				return false;
			}
		}
		return true;
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_valid_lighting' ) ) {
	function nadlan_flagship_cotour_valid_lighting( $lighting ) {
		if ( ! nadlan_flagship_cotour_exact_keys( $lighting, array( 'schema', 'mode', 'direction', 'ambient', 'diffuse', 'decisionGrade', 'sunSimulation' ) )
			|| 'nadlan-flagship-viewer-lighting/v1' !== $lighting['schema']
			|| 'illustrative_directional' !== $lighting['mode']
			|| false !== $lighting['decisionGrade'] || false !== $lighting['sunSimulation']
			|| ! nadlan_flagship_cotour_number( $lighting['ambient'], 0, 1 )
			|| ! nadlan_flagship_cotour_number( $lighting['diffuse'], 0, 1 )
			|| $lighting['ambient'] + $lighting['diffuse'] > 1.5
			|| ! is_array( $lighting['direction'] ) || array_keys( $lighting['direction'] ) !== array( 0, 1, 2 ) ) {
			return false;
		}
		$length = 0.0;
		foreach ( $lighting['direction'] as $component ) {
			if ( ! nadlan_flagship_cotour_number( $component, -1, 1 ) ) {
				return false;
			}
			$length += $component * $component;
		}
		return $length >= 0.000001;
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_valid_selection' ) ) {
	function nadlan_flagship_cotour_valid_selection( $selection ) {
		return null === $selection || (
			nadlan_flagship_cotour_exact_keys( $selection, array( 'type', 'id', 'hotspotId', 'evidenceLane' ) )
			&& 'scene' === $selection['type']
			&& nadlan_flagship_cotour_identifier( $selection['id'] )
			&& nadlan_flagship_cotour_identifier( $selection['hotspotId'] )
			&& in_array( $selection['evidenceLane'], array( 'verified', 'illustrative' ), true )
		);
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_valid_map_camera' ) ) {
	function nadlan_flagship_cotour_valid_map_camera( $camera ) {
		return nadlan_flagship_cotour_exact_keys( $camera, array( 'lng', 'lat', 'zoom', 'bearing', 'pitch' ) )
			&& nadlan_flagship_cotour_number( $camera['lng'], -180, 180 )
			&& nadlan_flagship_cotour_number( $camera['lat'], -90, 90 )
			&& nadlan_flagship_cotour_number( $camera['zoom'], 0, 24 )
			&& nadlan_flagship_cotour_number( $camera['bearing'], -3600, 3600 )
			&& nadlan_flagship_cotour_number( $camera['pitch'], 0, 85 );
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_valid_map_state' ) ) {
	function nadlan_flagship_cotour_valid_map_state( $map ) {
		if ( null === $map ) {
			return true;
		}
		if ( ! nadlan_flagship_cotour_exact_keys( $map, array( 'schema', 'map', 'selectedEntityId', 'coTour' ) )
			|| 'nadlan-einstein-integration-state/v1' !== $map['schema']
			|| ! nadlan_flagship_cotour_identifier( $map['selectedEntityId'], true )
			|| ! nadlan_flagship_cotour_exact_keys( $map['map'], array( 'schema', 'available', 'camera', 'selectedEntityId', 'correlationState' ) )
			|| 'nadlan-einstein-canonical-map-state/v1' !== $map['map']['schema']
			|| ! is_bool( $map['map']['available'] )
			|| ! nadlan_flagship_cotour_identifier( $map['map']['selectedEntityId'], true )
			|| ! in_array( $map['map']['correlationState'], array( 'idle', 'panned', 'cone', 'unavailable-no-source', 'unavailable-no-bearing' ), true ) ) {
			return false;
		}
		if ( true === $map['map']['available'] ) {
			if ( ! nadlan_flagship_cotour_valid_map_camera( $map['map']['camera'] ) ) {
				return false;
			}
		} elseif ( null !== $map['map']['camera'] ) {
			return false;
		}
		$capability = $map['coTour'];
		return nadlan_flagship_cotour_exact_keys( $capability, array( 'schema', 'state', 'enabled', 'transport', 'privateEngineClosuresUsed', 'roomIdentifiersInUrl', 'hostSecretInUrlOrDom', 'ttlSeconds' ) )
			&& 'nadlan-einstein-cotour-capability/v1' === $capability['schema']
			&& 'ready_dedicated_adapter' === $capability['state']
			&& true === $capability['enabled']
			&& 'same_origin_ephemeral_rest' === $capability['transport']
			&& false === $capability['privateEngineClosuresUsed']
			&& false === $capability['roomIdentifiersInUrl']
			&& false === $capability['hostSecretInUrlOrDom']
			&& 600 === $capability['ttlSeconds'];
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_valid_media_state' ) ) {
	function nadlan_flagship_cotour_valid_media_state( $media ) {
		if ( ! nadlan_flagship_cotour_exact_keys( $media, array( 'schema', 'mode', 'toolId', 'sceneId', 'hotspotId', 'page', 'activePreview', 'material', 'decisionGrade' ) )
			|| 'nadlan-flagship-media-state/v1' !== $media['schema']
			|| ! in_array( $media['mode'], array( 'surface', 'tool', 'deferred' ), true )
			|| false !== $media['decisionGrade']
			|| ! is_int( $media['page'] ) || $media['page'] < 0 || $media['page'] >= 3
			|| ! in_array( $media['activePreview'], array( 'view', 'interior', 'design' ), true )
			|| ! nadlan_flagship_cotour_identifier( $media['toolId'], true )
			|| ! nadlan_flagship_cotour_identifier( $media['sceneId'], true )
			|| ! nadlan_flagship_cotour_identifier( $media['hotspotId'], true )
			|| ! nadlan_flagship_cotour_exact_keys( $media['material'], array( 'interior', 'design', 'windowView' ) ) ) {
			return false;
		}
		$material = $media['material'];
		if ( 'surface' === $media['mode'] ) {
			return '' === $media['toolId'] && '' === $media['sceneId'] && '' === $media['hotspotId']
				&& null === $material['interior'] && null === $material['design'] && null === $material['windowView'];
		}
		if ( 'interior' === $media['toolId'] ) {
			return nadlan_flagship_cotour_exact_keys( $material['interior'], array( 'sceneId' ) )
				&& $material['interior']['sceneId'] === $media['sceneId']
				&& nadlan_flagship_cotour_identifier( $media['sceneId'] )
				&& nadlan_flagship_cotour_identifier( $media['hotspotId'] )
				&& null === $material['design'] && null === $material['windowView'];
		}
		if ( 'design' === $media['toolId'] ) {
			return '' === $media['sceneId'] && '' === $media['hotspotId']
				&& nadlan_flagship_cotour_exact_keys( $material['design'], array( 'x', 'y' ) )
				&& nadlan_flagship_cotour_number( $material['design']['x'], 10, 82 )
				&& nadlan_flagship_cotour_number( $material['design']['y'], 20, 78 )
				&& null === $material['interior'] && null === $material['windowView'];
		}
		return 'view' === $media['toolId'] && '' === $media['sceneId'] && '' === $media['hotspotId']
			&& nadlan_flagship_cotour_exact_keys( $material['windowView'], array( 'bearing', 'pitch' ) )
			&& nadlan_flagship_cotour_number( $material['windowView']['bearing'], 0, 359.999999 )
			&& nadlan_flagship_cotour_number( $material['windowView']['pitch'], 62, 85 )
			&& null === $material['interior'] && null === $material['design'];
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_valid_cross_consumer_state' ) ) {
	/** One decision state must name the same entity across selection, map and media. */
	function nadlan_flagship_cotour_valid_cross_consumer_state( $state ) {
		if ( ! is_array( $state['map'] ) || ! is_array( $state['map']['map'] ) ) {
			return false;
		}
		$selection = $state['selectedEntity'];
		$map       = $state['map'];
		$nested    = $map['map'];
		$media     = $state['media'];
		if ( null === $selection ) {
			return '' === $map['selectedEntityId'] && '' === $nested['selectedEntityId']
				&& 'idle' === $nested['correlationState']
				&& 'interior' !== $media['toolId'];
		}
		$entity_id  = (string) $selection['id'];
		$hotspot_id = (string) $selection['hotspotId'];
		if ( ! hash_equals( $entity_id, (string) $map['selectedEntityId'] )
			|| ! hash_equals( $entity_id, (string) $nested['selectedEntityId'] )
			|| 'idle' === $nested['correlationState'] ) {
			return false;
		}
		if ( 'illustrative' === $selection['evidenceLane'] && 'unavailable-no-source' !== $nested['correlationState'] ) {
			return false;
		}
		if ( false === $nested['available']
			&& ! in_array( $nested['correlationState'], array( 'unavailable-no-source', 'unavailable-no-bearing' ), true ) ) {
			return false;
		}
		if ( true === $nested['available']
			&& ! in_array( $nested['correlationState'], array( 'panned', 'cone', 'unavailable-no-source', 'unavailable-no-bearing' ), true ) ) {
			return false;
		}
		if ( 'interior' === $media['toolId'] ) {
			return hash_equals( $entity_id, (string) $media['sceneId'] )
				&& hash_equals( $hotspot_id, (string) $media['hotspotId'] );
		}
		return true;
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_valid_spatial_state' ) ) {
	/** Exact portable state emitted by NadlanFlagshipV3.getState(). */
	function nadlan_flagship_cotour_valid_spatial_state( $state, $project_contract_id ) {
		if ( ! nadlan_flagship_cotour_exact_keys( $state, array( 'schema', 'projectContractId', 'historyVersion', 'selectedEntity', 'model', 'map', 'media' ) )
			|| 'nadlan-spatial-decision-state/v1' !== $state['schema']
			|| ! is_string( $state['projectContractId'] )
			|| ! hash_equals( (string) $project_contract_id, $state['projectContractId'] )
			|| 1 !== $state['historyVersion']
			|| ! nadlan_flagship_cotour_valid_selection( $state['selectedEntity'] )
			|| ! nadlan_flagship_cotour_exact_keys( $state['model'], array( 'camera', 'lighting' ) )
			|| ! nadlan_flagship_cotour_valid_camera( $state['model']['camera'] )
			|| ! nadlan_flagship_cotour_valid_lighting( $state['model']['lighting'] )
			|| ! nadlan_flagship_cotour_valid_map_state( $state['map'] )
			|| ! nadlan_flagship_cotour_valid_media_state( $state['media'] )
			|| ! nadlan_flagship_cotour_valid_cross_consumer_state( $state ) ) {
			return false;
		}
		$encoded = wp_json_encode( $state, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
		return is_string( $encoded ) && strlen( $encoded ) <= 65536;
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_origin' ) ) {
	function nadlan_flagship_cotour_origin( $value ) {
		if ( ! is_string( $value ) || strlen( $value ) > 255 ) {
			return '';
		}
		$parts = parse_url( $value );
		if ( ! is_array( $parts ) || ! isset( $parts['scheme'], $parts['host'] )
			|| ! in_array( strtolower( $parts['scheme'] ), array( 'http', 'https' ), true )
			|| isset( $parts['user'] ) || isset( $parts['pass'] ) || isset( $parts['query'] ) || isset( $parts['fragment'] )
			|| ( isset( $parts['path'] ) && '' !== $parts['path'] && '/' !== $parts['path'] ) ) {
			return '';
		}
		$origin = strtolower( $parts['scheme'] ) . '://' . strtolower( $parts['host'] );
		if ( isset( $parts['port'] ) ) {
			$origin .= ':' . (int) $parts['port'];
		}
		return $origin;
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_same_origin' ) ) {
	function nadlan_flagship_cotour_same_origin( $request ) {
		if ( ! is_object( $request ) || ! method_exists( $request, 'get_header' ) ) {
			return false;
		}
		$origin = nadlan_flagship_cotour_origin( (string) $request->get_header( 'origin' ) );
		$home   = nadlan_flagship_cotour_origin( home_url( '/' ) );
		$fetch  = strtolower( trim( (string) $request->get_header( 'sec-fetch-site' ) ) );
		$guard  = (string) $request->get_header( 'x-nadlan-flagship-cotour' );
		return '' !== $origin && '' !== $home && hash_equals( $home, $origin )
			&& ( '' === $fetch || 'same-origin' === $fetch )
			&& '1' === $guard;
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_response' ) ) {
	function nadlan_flagship_cotour_response( $data, $status = 200 ) {
		$response = new WP_REST_Response( $data, $status );
		$response->header( 'Cache-Control', 'no-store, private, max-age=0' );
		$response->header( 'Pragma', 'no-cache' );
		$response->header( 'X-Content-Type-Options', 'nosniff' );
		return $response;
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_error' ) ) {
	function nadlan_flagship_cotour_error( $code, $status, $extra = array() ) {
		return nadlan_flagship_cotour_response(
			array_merge(
				array(
					'schema' => 'nadlan-flagship-cotour-response/v1',
					'ok'     => false,
					'code'   => (string) $code,
				),
				$extra
			),
			$status
		);
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_success' ) ) {
	function nadlan_flagship_cotour_success( $data = array() ) {
		return nadlan_flagship_cotour_response(
			array_merge(
				array(
					'schema' => 'nadlan-flagship-cotour-response/v1',
					'ok'     => true,
				),
				$data
			),
			200
		);
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_cookie_name' ) ) {
	/** A room-specific __Host cookie permits independent rooms in separate tabs. */
	function nadlan_flagship_cotour_cookie_name( $room_code ) {
		return '__Host-nlfsct_' . substr( nadlan_flagship_cotour_hash( 'cookie-name', (string) $room_code ), 0, 20 );
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_cookie_value' ) ) {
	/** Authorization cookies are deliberately unavailable to JavaScript. */
	function nadlan_flagship_cotour_cookie_value( $room_code ) {
		$name  = nadlan_flagship_cotour_cookie_name( $room_code );
		$value = isset( $_COOKIE[ $name ] ) ? (string) $_COOKIE[ $name ] : '';
		return preg_match( '/^[A-Za-z0-9_-]{43}$/D', $value ) ? $value : '';
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_attach_cookie' ) ) {
	/** Set or clear an opaque production cookie. Set-Cookie is a forbidden fetch response header. */
	function nadlan_flagship_cotour_attach_cookie( $response, $room_code, $value, $max_age ) {
		if ( ! $response instanceof WP_REST_Response ) {
			return $response;
		}
		$max_age = max( 0, min( 600, (int) $max_age ) );
		$cookie  = nadlan_flagship_cotour_cookie_name( $room_code ) . '=' . rawurlencode( (string) $value )
			. '; Path=/; Max-Age=' . $max_age
			. '; Expires=' . gmdate( 'D, d M Y H:i:s', nadlan_flagship_cotour_now() + $max_age ) . ' GMT'
			. '; Secure; HttpOnly; SameSite=Strict';
		$response->header( 'Set-Cookie', $cookie );
		return $response;
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_random_credential' ) ) {
	function nadlan_flagship_cotour_random_credential() {
		return rtrim( strtr( base64_encode( random_bytes( 32 ) ), '+/', '-_' ), '=' );
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_hash' ) ) {
	function nadlan_flagship_cotour_hash( $purpose, $value ) {
		return hash_hmac( 'sha256', (string) $value, 'nadlan-flagship-cotour|' . (string) $purpose . '|' . wp_salt( 'auth' ) );
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_room_key' ) ) {
	function nadlan_flagship_cotour_room_key( $room_code ) {
		return 'nlfsct_room_' . substr( nadlan_flagship_cotour_hash( 'room', $room_code ), 0, 40 );
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_rate_contract' ) ) {
	function nadlan_flagship_cotour_rate_contract() {
		return array(
			'window_seconds' => 60,
			'global_per_ip'  => array( 'create' => 5, 'join-poll' => 90, 'update' => 90, 'end' => 15 ),
			'room'           => array( 'join-poll' => 75, 'update' => 90, 'end' => 10 ),
		);
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_lock' ) ) {
	/**
	 * MySQL advisory locks are connection-owned: no process can delete a newer
	 * owner's lock, and a lost connection releases its locks automatically.
	 * If the database cannot prove ownership, callers fail closed.
	 */
	function nadlan_flagship_cotour_lock( $scope ) {
		global $wpdb;
		if ( ! is_object( $wpdb ) || ! method_exists( $wpdb, 'prepare' ) || ! method_exists( $wpdb, 'get_var' ) ) {
			return '';
		}
		$name   = 'nlfsct:' . substr( nadlan_flagship_cotour_hash( 'db-lock', (string) $scope ), 0, 48 );
		$result = $wpdb->get_var( $wpdb->prepare( 'SELECT GET_LOCK(%s, 0)', $name ) ); // phpcs:ignore WordPress.DB.PreparedSQL.NotPrepared
		return 1 === (int) $result ? $name : '';
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_unlock' ) ) {
	function nadlan_flagship_cotour_unlock( $name ) {
		global $wpdb;
		if ( ! is_string( $name ) || ! preg_match( '/^nlfsct:[a-f0-9]{48}$/D', $name )
			|| ! is_object( $wpdb ) || ! method_exists( $wpdb, 'prepare' ) || ! method_exists( $wpdb, 'get_var' ) ) {
			return false;
		}
		return 1 === (int) $wpdb->get_var( $wpdb->prepare( 'SELECT RELEASE_LOCK(%s)', $name ) ); // phpcs:ignore WordPress.DB.PreparedSQL.NotPrepared
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_rate_consume' ) ) {
	function nadlan_flagship_cotour_rate_consume( $scope, $limit ) {
		$lock = nadlan_flagship_cotour_lock( 'rate|' . $scope );
		if ( '' === $lock ) {
			return false;
		}
		try {
			$key   = 'nlfsct_rate_' . substr( nadlan_flagship_cotour_hash( 'rate', $scope ), 0, 40 );
			$count = (int) get_transient( $key );
			if ( $count >= (int) $limit ) {
				return false;
			}
			return true === set_transient( $key, $count + 1, 65 );
		} finally {
			nadlan_flagship_cotour_unlock( $lock );
		}
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_rate_limit' ) ) {
	/** Global IP/action limit cannot be bypassed by varying attacker-controlled room codes. */
	function nadlan_flagship_cotour_rate_limit( $action, $room_code = '' ) {
		$contract = nadlan_flagship_cotour_rate_contract();
		if ( ! isset( $contract['global_per_ip'][ $action ] ) ) {
			return false;
		}
		$address = isset( $_SERVER['REMOTE_ADDR'] ) ? (string) $_SERVER['REMOTE_ADDR'] : 'unknown';
		if ( strlen( $address ) > 64 || ! preg_match( '/^[0-9A-Fa-f:.]{3,64}$/D', $address ) ) {
			$address = 'unknown';
		}
		$bucket = (int) floor( nadlan_flagship_cotour_now() / (int) $contract['window_seconds'] );
		$global_scope = 'global|' . $action . '|' . $address . '|' . $bucket;
		if ( ! nadlan_flagship_cotour_rate_consume( $global_scope, $contract['global_per_ip'][ $action ] ) ) {
			return false;
		}
		if ( '' !== $room_code && isset( $contract['room'][ $action ] ) ) {
			$room_scope = 'room|' . $action . '|' . $room_code . '|' . $bucket;
			if ( ! nadlan_flagship_cotour_rate_consume( $room_scope, $contract['room'][ $action ] ) ) {
				return false;
			}
		}
		return true;
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_binding' ) ) {
	function nadlan_flagship_cotour_binding( $project_id, $project_contract_id ) {
		if ( ! is_int( $project_id ) || $project_id <= 0 || ! is_string( $project_contract_id )
			|| ! preg_match( '/^[a-z0-9][a-z0-9-]{7,127}$/D', $project_contract_id )
			|| ! function_exists( 'nadlan_flagship_v3_contract' ) ) {
			return array();
		}
		$contract = nadlan_flagship_v3_contract( $project_contract_id );
		$decision = isset( $contract['decision_experience'] ) && is_array( $contract['decision_experience'] ) ? $contract['decision_experience'] : array();
		$caps = isset( $decision['capabilities'] ) && is_array( $decision['capabilities'] ) ? $decision['capabilities'] : array();
		if ( ! is_array( $contract ) || (int) ( isset( $contract['canonical_post_id'] ) ? $contract['canonical_post_id'] : 0 ) !== $project_id
			|| ! isset( $contract['project_contract_id'] ) || ! hash_equals( (string) $contract['project_contract_id'], $project_contract_id )
			|| 'ready' !== ( isset( $caps['co_tour'] ) ? $caps['co_tour'] : '' ) ) {
			return array();
		}
		return $contract;
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_request_payload' ) ) {
	function nadlan_flagship_cotour_request_payload( $request, $action ) {
		if ( ! is_object( $request ) || ! method_exists( $request, 'get_method' ) || 'POST' !== strtoupper( (string) $request->get_method() ) ) {
			return new WP_Error( 'method_not_allowed', 'POST required.', array( 'status' => 405 ) );
		}
		$body = method_exists( $request, 'get_body' ) ? (string) $request->get_body() : '';
		if ( strlen( $body ) > 73728 ) {
			return new WP_Error( 'payload_too_large', 'Payload too large.', array( 'status' => 413 ) );
		}
		$params = method_exists( $request, 'get_json_params' ) ? $request->get_json_params() : null;
		$keys = array(
			'create'    => array( 'schema', 'projectId', 'projectContractId' ),
			'join-poll' => array( 'schema', 'projectId', 'projectContractId', 'roomCode', 'afterSequence', 'intent', 'consent' ),
			'update'    => array( 'schema', 'projectId', 'projectContractId', 'roomCode', 'sequence', 'state' ),
			'end'       => array( 'schema', 'projectId', 'projectContractId', 'roomCode', 'sequence' ),
		);
		if ( ! isset( $keys[ $action ] ) || ! nadlan_flagship_cotour_exact_keys( $params, $keys[ $action ] )
			|| 'nadlan-flagship-cotour-request/v1' !== $params['schema']
			|| ! is_int( $params['projectId'] ) || $params['projectId'] <= 0
			|| ! is_string( $params['projectContractId'] ) ) {
			return new WP_Error( 'invalid_request', 'Invalid request.', array( 'status' => 400 ) );
		}
		if ( 'create' !== $action ) {
			if ( ! is_string( $params['roomCode'] ) || ! preg_match( '/^[A-F0-9]{12}$/D', $params['roomCode'] ) ) {
				return new WP_Error( 'invalid_room_code', 'Invalid room code.', array( 'status' => 400 ) );
			}
		}
		if ( 'join-poll' === $action ) {
			if ( ! is_int( $params['afterSequence'] ) || $params['afterSequence'] < 0 || $params['afterSequence'] > 1000000000
				|| ! is_string( $params['intent'] ) || ! in_array( $params['intent'], array( 'join', 'poll', 'resume', 'leave' ), true )
				|| ! is_bool( $params['consent'] ) || ( 'join' !== $params['intent'] && true === $params['consent'] ) ) {
				return new WP_Error( 'invalid_join_request', 'Invalid join request.', array( 'status' => 400 ) );
			}
		}
		if ( in_array( $action, array( 'update', 'end' ), true ) ) {
			if ( ! is_int( $params['sequence'] ) || $params['sequence'] < 1 || $params['sequence'] > 1000000000 ) {
				return new WP_Error( 'invalid_host_request', 'Invalid host request.', array( 'status' => 400 ) );
			}
		}
		return $params;
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_room' ) ) {
	function nadlan_flagship_cotour_room( $params ) {
		$key = nadlan_flagship_cotour_room_key( $params['roomCode'] );
		$room = get_transient( $key );
		if ( ! is_array( $room ) || 'nadlan-flagship-cotour-room/v2' !== ( isset( $room['schema'] ) ? $room['schema'] : '' ) ) {
			return array();
		}
		if ( (int) $room['project_id'] !== $params['projectId']
			|| ! hash_equals( (string) $room['project_contract_id'], (string) $params['projectContractId'] ) ) {
			return array();
		}
		return $room;
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_create' ) ) {
	function nadlan_flagship_cotour_create( $params ) {
		if ( empty( nadlan_flagship_cotour_binding( $params['projectId'], $params['projectContractId'] ) ) ) {
			return nadlan_flagship_cotour_error( 'contract_unavailable', 404 );
		}
		for ( $attempt = 0; $attempt < 8; $attempt++ ) {
			try {
				$room_code  = strtoupper( bin2hex( random_bytes( 6 ) ) );
				$credential = nadlan_flagship_cotour_random_credential();
			} catch ( Exception $error ) {
				unset( $error );
				return nadlan_flagship_cotour_error( 'secure_random_unavailable', 503 );
			}
			$lock = nadlan_flagship_cotour_lock( 'room|' . $room_code );
			if ( '' === $lock ) {
				continue;
			}
			try {
				$key = nadlan_flagship_cotour_room_key( $room_code );
				if ( false !== get_transient( $key ) ) {
					continue;
				}
				$now        = nadlan_flagship_cotour_now();
				$expires_at = $now + 600;
				$room       = array(
					'schema'               => 'nadlan-flagship-cotour-room/v2',
					'project_id'           => $params['projectId'],
					'project_contract_id'  => $params['projectContractId'],
					'host_auth_hash'       => nadlan_flagship_cotour_hash( 'auth|' . $room_code, $credential ),
					'follower_auth_hash'   => '',
					'follower_joined_at'   => 0,
					'follower_seen_at'     => 0,
					'status'               => 'active',
					'sequence'             => 0,
					'state'                => null,
					'created_at'           => $now,
					'updated_at'           => $now,
					'expires_at'           => $expires_at,
				);
				if ( true !== set_transient( $key, $room, 600 ) ) {
					return nadlan_flagship_cotour_error( 'room_storage_unavailable', 503 );
				}
				$response = nadlan_flagship_cotour_success(
					array(
						'role'          => 'host',
						'status'        => 'active',
						'roomCode'      => $room_code,
						'sequence'      => 0,
						'expiresAt'     => $expires_at,
						'presenceCount' => 1,
						'capacity'      => 2,
					)
				);
				return nadlan_flagship_cotour_attach_cookie( $response, $room_code, $credential, 600 );
			} finally {
				nadlan_flagship_cotour_unlock( $lock );
			}
		}
		return nadlan_flagship_cotour_error( 'room_capacity_unavailable', 503 );
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_auth_role' ) ) {
	function nadlan_flagship_cotour_auth_role( $room, $room_code ) {
		$credential = nadlan_flagship_cotour_cookie_value( $room_code );
		$supplied   = nadlan_flagship_cotour_hash( 'auth|' . $room_code, $credential );
		$host       = isset( $room['host_auth_hash'] ) ? (string) $room['host_auth_hash'] : str_repeat( '0', 64 );
		$follower   = isset( $room['follower_auth_hash'] ) ? (string) $room['follower_auth_hash'] : str_repeat( '0', 64 );
		if ( '' !== $credential && 64 === strlen( $host ) && hash_equals( $host, $supplied ) ) {
			return 'host';
		}
		if ( '' !== $credential && 64 === strlen( $follower ) && hash_equals( $follower, $supplied ) ) {
			return 'follower';
		}
		return '';
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_follower_present' ) ) {
	function nadlan_flagship_cotour_follower_present( $room, $now ) {
		return ! empty( $room['follower_auth_hash'] ) && (int) $room['follower_seen_at'] > (int) $now - 30;
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_prune_follower' ) ) {
	function nadlan_flagship_cotour_prune_follower( $room, $now ) {
		if ( ! empty( $room['follower_auth_hash'] ) && ! nadlan_flagship_cotour_follower_present( $room, $now ) ) {
			$room['follower_auth_hash'] = '';
			$room['follower_joined_at'] = 0;
			$room['follower_seen_at'] = 0;
		}
		return $room;
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_presence_count' ) ) {
	function nadlan_flagship_cotour_presence_count( $room, $now ) {
		return 1 + ( nadlan_flagship_cotour_follower_present( $room, $now ) ? 1 : 0 );
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_join_poll' ) ) {
	function nadlan_flagship_cotour_join_poll( $params ) {
		if ( empty( nadlan_flagship_cotour_binding( $params['projectId'], $params['projectContractId'] ) ) ) {
			return nadlan_flagship_cotour_error( 'room_unavailable', 404 );
		}
		$lock = nadlan_flagship_cotour_lock( 'room|' . $params['roomCode'] );
		if ( '' === $lock ) {
			return nadlan_flagship_cotour_error( 'room_busy', 409 );
		}
		try {
			$room = nadlan_flagship_cotour_room( $params );
			if ( empty( $room ) ) {
				return nadlan_flagship_cotour_error( 'room_unavailable', 404 );
			}
			$now = nadlan_flagship_cotour_now();
			if ( (int) $room['expires_at'] <= $now ) {
				delete_transient( nadlan_flagship_cotour_room_key( $params['roomCode'] ) );
				return nadlan_flagship_cotour_error( 'room_expired', 410 );
			}
			if ( 'ended' === $room['status'] ) {
				return nadlan_flagship_cotour_success(
					array( 'role' => 'follower', 'status' => 'ended', 'sequence' => (int) $room['sequence'], 'expiresAt' => (int) $room['expires_at'], 'presenceCount' => 0, 'capacity' => 2, 'state' => null )
				);
			}
			$role   = nadlan_flagship_cotour_auth_role( $room, $params['roomCode'] );
			$intent = $params['intent'];
			$key    = nadlan_flagship_cotour_room_key( $params['roomCode'] );

			if ( 'resume' === $intent ) {
				if ( '' === $role ) {
					return nadlan_flagship_cotour_error( 'resume_auth_failed', 403 );
				}
				try {
					$rotated = nadlan_flagship_cotour_random_credential();
				} catch ( Exception $error ) {
					unset( $error );
					return nadlan_flagship_cotour_error( 'secure_random_unavailable', 503 );
				}
				$room[ $role . '_auth_hash' ] = nadlan_flagship_cotour_hash( 'auth|' . $params['roomCode'], $rotated );
				if ( 'follower' === $role ) {
					$room['follower_seen_at'] = $now;
				}
				$remaining = max( 1, (int) $room['expires_at'] - $now );
				set_transient( $key, $room, $remaining );
				$changed  = 'follower' === $role && (int) $room['sequence'] > $params['afterSequence'] && is_array( $room['state'] );
				$response = nadlan_flagship_cotour_success(
					array(
						'role'          => $role,
						'status'        => 'host' === $role ? 'resumed' : ( $changed ? 'changed' : 'no_change' ),
						'sequence'      => (int) $room['sequence'],
						'expiresAt'     => (int) $room['expires_at'],
						'presenceCount' => nadlan_flagship_cotour_presence_count( $room, $now ),
						'capacity'      => 2,
						'state'         => $changed ? $room['state'] : null,
					)
				);
				return nadlan_flagship_cotour_attach_cookie( $response, $params['roomCode'], $rotated, $remaining );
			}

			if ( 'join' === $intent ) {
				if ( true !== $params['consent'] ) {
					return nadlan_flagship_cotour_error( 'consent_required', 428 );
				}
				if ( 'host' === $role ) {
					return nadlan_flagship_cotour_error( 'role_conflict', 409 );
				}
				if ( 'follower' !== $role ) {
					$room = nadlan_flagship_cotour_prune_follower( $room, $now );
					if ( ! empty( $room['follower_auth_hash'] ) ) {
						return nadlan_flagship_cotour_error( 'capacity_reached', 409, array( 'presenceCount' => 2, 'capacity' => 2 ) );
					}
					try {
						$follower_credential = nadlan_flagship_cotour_random_credential();
					} catch ( Exception $error ) {
						unset( $error );
						return nadlan_flagship_cotour_error( 'secure_random_unavailable', 503 );
					}
					$room['follower_auth_hash'] = nadlan_flagship_cotour_hash( 'auth|' . $params['roomCode'], $follower_credential );
					$room['follower_joined_at'] = $now;
				} else {
					$follower_credential = nadlan_flagship_cotour_cookie_value( $params['roomCode'] );
				}
				$room['follower_seen_at'] = $now;
				$remaining = max( 1, (int) $room['expires_at'] - $now );
				set_transient( $key, $room, $remaining );
				$changed  = (int) $room['sequence'] > $params['afterSequence'] && is_array( $room['state'] );
				$response = nadlan_flagship_cotour_success(
					array(
						'role'          => 'follower',
						'status'        => $changed ? 'changed' : 'no_change',
						'sequence'      => (int) $room['sequence'],
						'expiresAt'     => (int) $room['expires_at'],
						'presenceCount' => 2,
						'capacity'      => 2,
						'state'         => $changed ? $room['state'] : null,
					)
				);
				return nadlan_flagship_cotour_attach_cookie( $response, $params['roomCode'], $follower_credential, $remaining );
			}

			if ( 'follower' !== $role ) {
				return nadlan_flagship_cotour_error( 'follower_auth_failed', 403 );
			}
			if ( 'leave' === $intent ) {
				$room['follower_auth_hash'] = '';
				$room['follower_joined_at'] = 0;
				$room['follower_seen_at'] = 0;
				$remaining = max( 1, (int) $room['expires_at'] - $now );
				set_transient( $key, $room, $remaining );
				$response = nadlan_flagship_cotour_success(
					array( 'role' => 'follower', 'status' => 'left', 'sequence' => (int) $room['sequence'], 'expiresAt' => (int) $room['expires_at'], 'presenceCount' => 1, 'capacity' => 2, 'state' => null )
				);
				return nadlan_flagship_cotour_attach_cookie( $response, $params['roomCode'], '', 0 );
			}

			$room['follower_seen_at'] = $now;
			$remaining = max( 1, (int) $room['expires_at'] - $now );
			set_transient( $key, $room, $remaining );
			$changed = (int) $room['sequence'] > $params['afterSequence'] && is_array( $room['state'] );
			return nadlan_flagship_cotour_success(
				array(
					'role'          => 'follower',
					'status'        => $changed ? 'changed' : 'no_change',
					'sequence'      => (int) $room['sequence'],
					'expiresAt'     => (int) $room['expires_at'],
					'presenceCount' => 2,
					'capacity'      => 2,
					'state'         => $changed ? $room['state'] : null,
				)
			);
		} finally {
			nadlan_flagship_cotour_unlock( $lock );
		}
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_update' ) ) {
	function nadlan_flagship_cotour_update( $params ) {
		if ( empty( nadlan_flagship_cotour_binding( $params['projectId'], $params['projectContractId'] ) ) ) {
			return nadlan_flagship_cotour_error( 'room_unavailable', 404 );
		}
		if ( ! nadlan_flagship_cotour_valid_spatial_state( $params['state'], $params['projectContractId'] ) ) {
			return nadlan_flagship_cotour_error( 'invalid_spatial_state', 400 );
		}
		$lock = nadlan_flagship_cotour_lock( 'room|' . $params['roomCode'] );
		if ( '' === $lock ) {
			return nadlan_flagship_cotour_error( 'room_busy', 409 );
		}
		try {
			$room = nadlan_flagship_cotour_room( $params );
			if ( empty( $room ) ) {
				return nadlan_flagship_cotour_error( 'room_unavailable', 404 );
			}
			if ( 'host' !== nadlan_flagship_cotour_auth_role( $room, $params['roomCode'] ) ) {
				return nadlan_flagship_cotour_error( 'host_auth_failed', 403 );
			}
			$now = nadlan_flagship_cotour_now();
			if ( 'active' !== $room['status'] || (int) $room['expires_at'] <= $now ) {
				delete_transient( nadlan_flagship_cotour_room_key( $params['roomCode'] ) );
				return nadlan_flagship_cotour_error( 'room_expired', 410 );
			}
			if ( $params['sequence'] !== (int) $room['sequence'] + 1 ) {
				return nadlan_flagship_cotour_error( 'sequence_conflict', 409, array( 'sequence' => (int) $room['sequence'] ) );
			}
			try {
				$rotated = nadlan_flagship_cotour_random_credential();
			} catch ( Exception $error ) {
				unset( $error );
				return nadlan_flagship_cotour_error( 'secure_random_unavailable', 503 );
			}
			$room['host_auth_hash'] = nadlan_flagship_cotour_hash( 'auth|' . $params['roomCode'], $rotated );
			$room['sequence'] = $params['sequence'];
			$room['state'] = $params['state'];
			$room['updated_at'] = $now;
			$remaining = max( 1, (int) $room['expires_at'] - $now );
			set_transient( nadlan_flagship_cotour_room_key( $params['roomCode'] ), $room, $remaining );
			$response = nadlan_flagship_cotour_success(
				array( 'role' => 'host', 'status' => 'updated', 'sequence' => $params['sequence'], 'expiresAt' => (int) $room['expires_at'], 'presenceCount' => nadlan_flagship_cotour_presence_count( $room, $now ), 'capacity' => 2 )
			);
			return nadlan_flagship_cotour_attach_cookie( $response, $params['roomCode'], $rotated, $remaining );
		} finally {
			nadlan_flagship_cotour_unlock( $lock );
		}
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_end' ) ) {
	function nadlan_flagship_cotour_end( $params ) {
		if ( empty( nadlan_flagship_cotour_binding( $params['projectId'], $params['projectContractId'] ) ) ) {
			return nadlan_flagship_cotour_error( 'room_unavailable', 404 );
		}
		$lock = nadlan_flagship_cotour_lock( 'room|' . $params['roomCode'] );
		if ( '' === $lock ) {
			return nadlan_flagship_cotour_error( 'room_busy', 409 );
		}
		try {
			$room = nadlan_flagship_cotour_room( $params );
			if ( empty( $room ) ) {
				return nadlan_flagship_cotour_error( 'room_unavailable', 404 );
			}
			if ( 'host' !== nadlan_flagship_cotour_auth_role( $room, $params['roomCode'] ) ) {
				return nadlan_flagship_cotour_error( 'host_auth_failed', 403 );
			}
			if ( 'active' !== $room['status'] || $params['sequence'] !== (int) $room['sequence'] + 1 ) {
				return nadlan_flagship_cotour_error( 'sequence_conflict', 409, array( 'sequence' => (int) $room['sequence'] ) );
			}
			$expires_at = nadlan_flagship_cotour_now() + 30;
			$tombstone = array(
				'schema'              => 'nadlan-flagship-cotour-room/v2',
				'project_id'          => $room['project_id'],
				'project_contract_id' => $room['project_contract_id'],
				'host_auth_hash'      => '',
				'follower_auth_hash'  => '',
				'follower_joined_at'  => 0,
				'follower_seen_at'    => 0,
				'status'              => 'ended',
				'sequence'            => $params['sequence'],
				'state'               => null,
				'created_at'          => $room['created_at'],
				'updated_at'          => nadlan_flagship_cotour_now(),
				'expires_at'          => $expires_at,
			);
			set_transient( nadlan_flagship_cotour_room_key( $params['roomCode'] ), $tombstone, 30 );
			$response = nadlan_flagship_cotour_success(
				array( 'role' => 'host', 'status' => 'ended', 'sequence' => $params['sequence'], 'expiresAt' => $expires_at, 'presenceCount' => 0, 'capacity' => 2 )
			);
			return nadlan_flagship_cotour_attach_cookie( $response, $params['roomCode'], '', 0 );
		} finally {
			nadlan_flagship_cotour_unlock( $lock );
		}
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_handle' ) ) {
	function nadlan_flagship_cotour_handle( $request, $action ) {
		if ( ! nadlan_flagship_cotour_same_origin( $request ) ) {
			return nadlan_flagship_cotour_error( 'same_origin_required', 403 );
		}
		$params = nadlan_flagship_cotour_request_payload( $request, $action );
		if ( is_wp_error( $params ) ) {
			$data = $params->get_error_data();
			$status = is_array( $data ) && isset( $data['status'] ) ? (int) $data['status'] : 400;
			return nadlan_flagship_cotour_error( $params->get_error_code(), $status );
		}
		$room_code = isset( $params['roomCode'] ) ? $params['roomCode'] : '';
		if ( ! nadlan_flagship_cotour_rate_limit( $action, $room_code ) ) {
			$response = nadlan_flagship_cotour_error( 'rate_limited', 429, array( 'retryAfterSeconds' => 5 ) );
			$response->header( 'Retry-After', '5' );
			return $response;
		}
		if ( 'create' === $action ) {
			return nadlan_flagship_cotour_create( $params );
		}
		if ( 'join-poll' === $action ) {
			return nadlan_flagship_cotour_join_poll( $params );
		}
		if ( 'update' === $action ) {
			return nadlan_flagship_cotour_update( $params );
		}
		return nadlan_flagship_cotour_end( $params );
	}
}

if ( ! function_exists( 'nadlan_flagship_cotour_register_routes' ) ) {
	function nadlan_flagship_cotour_register_routes() {
		foreach ( array( 'create', 'join-poll', 'update', 'end' ) as $action ) {
			register_rest_route(
				'nadlan/v1',
				'/flagship-cotour/' . $action,
				array(
					'methods'             => 'POST',
					'permission_callback' => '__return_true',
					'callback'            => function ( $request ) use ( $action ) {
						return nadlan_flagship_cotour_handle( $request, $action );
					},
				)
			);
		}
	}
	add_action( 'rest_api_init', 'nadlan_flagship_cotour_register_routes' );
}

if ( ! function_exists( 'nadlan_flagship_cotour_runtime_contract' ) ) {
	/** Public configuration contains no authorization credential or room identifier. */
	function nadlan_flagship_cotour_runtime_contract( $contract ) {
		$decision = isset( $contract['decision_experience'] ) && is_array( $contract['decision_experience'] ) ? $contract['decision_experience'] : array();
		$caps = isset( $decision['capabilities'] ) && is_array( $decision['capabilities'] ) ? $decision['capabilities'] : array();
		$enabled = 'ready' === ( isset( $caps['co_tour'] ) ? $caps['co_tour'] : '' );
		return array(
			'schema'              => 'nadlan-flagship-cotour-runtime/v1',
			'enabled'             => $enabled,
			'project_id'          => (int) ( isset( $contract['canonical_post_id'] ) ? $contract['canonical_post_id'] : 0 ),
			'project_contract_id' => (string) ( isset( $contract['project_contract_id'] ) ? $contract['project_contract_id'] : '' ),
			'endpoints'           => array(
				'create'    => rest_url( 'nadlan/v1/flagship-cotour/create' ),
				'join_poll' => rest_url( 'nadlan/v1/flagship-cotour/join-poll' ),
				'update'    => rest_url( 'nadlan/v1/flagship-cotour/update' ),
				'end'       => rest_url( 'nadlan/v1/flagship-cotour/end' ),
			),
			'ttl_seconds'         => 600,
			'poll_interval_ms'    => 1200,
			'poll_backoff_ms'     => array( 1200, 1800, 2700, 4050, 5000 ),
			'max_state_bytes'     => 65536,
			'capacity'            => array( 'hosts' => 1, 'followers' => 1, 'total' => 2 ),
			'rate_limits'         => nadlan_flagship_cotour_rate_contract(),
			'authorization'       => array(
				'transport'           => 'same_origin_http_only_cookie',
				'secure'              => true,
				'same_site'           => 'Strict',
				'javascript_readable' => false,
				'rotation'            => 'create_resume_and_each_host_update',
			),
		);
	}
}
