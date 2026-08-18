<?php
/**
 * NadLan flagship v3 surface seam.
 *
 * This module is deliberately inert until the central plugin loader includes it
 * and showroom-engine dispatches a selected post through
 * nadlan_flagship_v3_render_for(). Project copy and coordinates never live here.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_flagship_v3_registry_path' ) ) {
	function nadlan_flagship_v3_registry_path() {
		return dirname( __DIR__ ) . '/assets/flagship-v3/contracts/registry.json';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_registry' ) ) {
	/** Read the reviewed, plugin-owned identity allow-list once per request. */
	function nadlan_flagship_v3_registry() {
		static $registry = null;
		if ( is_array( $registry ) ) {
			return $registry;
		}

		$registry = array( 'contracts' => array() );
		$path     = nadlan_flagship_v3_registry_path();
		if ( ! is_readable( $path ) ) {
			return $registry;
		}
		$raw = file_get_contents( $path );
		$doc = is_string( $raw ) ? json_decode( $raw, true ) : null;
		if ( ! is_array( $doc )
			|| 'nadlan-flagship-contract-registry/v1' !== ( isset( $doc['schema'] ) ? $doc['schema'] : '' )
			|| 'flagship-v3' !== ( isset( $doc['surface_version'] ) ? $doc['surface_version'] : '' )
			|| ! isset( $doc['contracts'] )
			|| ! is_array( $doc['contracts'] ) ) {
			return $registry;
		}
		$registry = $doc;
		return $registry;
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_contract' ) ) {
	function nadlan_flagship_v3_contract( $project_contract_id ) {
		$project_contract_id = (string) $project_contract_id;
		foreach ( (array) nadlan_flagship_v3_registry()['contracts'] as $contract ) {
			if ( is_array( $contract )
				&& isset( $contract['project_contract_id'] )
				&& hash_equals( (string) $contract['project_contract_id'], $project_contract_id ) ) {
				return $contract;
			}
		}
		return array();
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_json_meta' ) ) {
	function nadlan_flagship_v3_json_meta( $post_id, $key ) {
		$raw = get_post_meta( (int) $post_id, (string) $key, true );
		if ( is_array( $raw ) ) {
			return $raw;
		}
		if ( ! is_string( $raw ) || '' === trim( $raw ) ) {
			return array();
		}
		$decoded = json_decode( $raw, true );
		return is_array( $decoded ) ? $decoded : array();
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_sanitize_json_meta' ) ) {
	function nadlan_flagship_v3_sanitize_json_meta( $value ) {
		if ( is_array( $value ) ) {
			$decoded = $value;
		} elseif ( is_string( $value ) && strlen( $value ) <= 524288 ) {
			$decoded = json_decode( $value, true, 64 );
		} else {
			return '';
		}
		if ( ! is_array( $decoded ) ) {
			return '';
		}
		$encoded = wp_json_encode( $decoded, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
		return is_string( $encoded ) && strlen( $encoded ) <= 524288 ? $encoded : '';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_register_meta' ) ) {
	/** Register only the isolated v3 fields; existing showroom fields keep their owner. */
	function nadlan_flagship_v3_register_meta() {
		$auth = function ( $allowed, $meta_key, $post_id ) {
			unset( $allowed, $meta_key );
			return current_user_can( 'edit_post', (int) $post_id );
		};
		$string_fields = array(
			'project_surface_version'               => 'sanitize_key',
			'project_contract_id'                   => 'sanitize_text_field',
			'project_model_lod_glb'                 => 'esc_url_raw',
			'project_identity_contract_json'        => 'nadlan_flagship_v3_sanitize_json_meta',
			'project_representation_registry_json'  => 'nadlan_flagship_v3_sanitize_json_meta',
			'project_visual_playground_json'        => 'nadlan_flagship_v3_sanitize_json_meta',
			'project_buyer_decision_contract_json'  => 'nadlan_flagship_v3_sanitize_json_meta',
			'project_experience_registry_json'      => 'nadlan_flagship_v3_sanitize_json_meta',
		);
		foreach ( $string_fields as $key => $sanitize_callback ) {
			register_post_meta(
				'nadlan_project',
				$key,
				array(
					'type'              => 'string',
					'single'            => true,
					'show_in_rest'      => true,
					'sanitize_callback' => $sanitize_callback,
					'auth_callback'     => $auth,
				)
			);
		}
		register_post_meta(
			'nadlan_project',
			'_nadlan_flagship_source_post_id',
			array(
				'type'              => 'integer',
				'single'            => true,
				'show_in_rest'      => true,
				'sanitize_callback' => 'absint',
				'auth_callback'     => $auth,
			)
		);
	}
}
add_action( 'init', 'nadlan_flagship_v3_register_meta', 12 );

if ( ! function_exists( 'nadlan_flagship_v3_guard_rest_meta' ) ) {
	/**
	 * Keep password-staged v3 payloads and shared showroom media out of
	 * anonymous REST responses. This is intentionally broader than the v3
	 * fields because the legacy showroom registers its model fields in REST.
	 */
	function nadlan_flagship_v3_guard_rest_meta( $response, $post ) {
		$post_id = is_object( $post ) && isset( $post->ID ) ? (int) $post->ID : 0;
		if ( $post_id <= 0 || ! nadlan_flagship_v3_is_private_candidate( $post_id ) || current_user_can( 'edit_post', $post_id )
			|| ! is_object( $response ) || ! method_exists( $response, 'get_data' ) || ! method_exists( $response, 'set_data' ) ) {
			return $response;
		}
		$data = $response->get_data();
		if ( ! is_array( $data ) ) {
			return $response;
		}
		if ( isset( $data['meta'] ) && is_array( $data['meta'] ) ) {
			$private_keys = array(
				'project_surface_version',
				'project_contract_id',
				'project_identity_contract_json',
				'project_representation_registry_json',
				'project_visual_playground_json',
				'project_buyer_decision_contract_json',
				'project_experience_registry_json',
				'_nadlan_flagship_source_post_id',
				'_nadlan_private_unit_journey',
				'_nadlan_private_unit_journey_project_name',
				'source_id',
				'is_demo',
				'data_quality',
			);
			foreach ( array_keys( $data['meta'] ) as $key ) {
				$key = (string) $key;
				if ( in_array( $key, $private_keys, true )
					|| 0 === strpos( $key, 'project_model_' )
					|| 0 === strpos( $key, 'project_3d_' ) ) {
					unset( $data['meta'][ $key ] );
				}
			}
		}
		// Never rely on core password formatting to protect staged body media.
		foreach ( array( 'content', 'excerpt' ) as $body_key ) {
			if ( isset( $data[ $body_key ] ) && is_array( $data[ $body_key ] ) ) {
				$data[ $body_key ]['rendered']  = '';
				$data[ $body_key ]['protected'] = true;
				unset( $data[ $body_key ]['raw'] );
			}
		}
		if ( isset( $data['_links']['wp:featuredmedia'] ) ) {
			unset( $data['_links']['wp:featuredmedia'] );
		}
		$response->set_data( $data );
		if ( method_exists( $response, 'header' ) ) {
			$response->header( 'Cache-Control', 'private, no-store, no-cache, max-age=0, must-revalidate' );
			$response->header( 'X-Robots-Tag', 'noindex, nofollow, noarchive' );
		}
		return $response;
	}
}
add_filter( 'rest_prepare_nadlan_project', 'nadlan_flagship_v3_guard_rest_meta', 100, 2 );

if ( ! function_exists( 'nadlan_flagship_v3_guard_rest_collection' ) ) {
	/** Anonymous collection/search queries must not discover private stages. */
	function nadlan_flagship_v3_guard_rest_collection( $args, $request ) {
		unset( $request );
		if ( current_user_can( 'edit_posts' ) ) {
			return $args;
		}
		$privacy_clause = array(
			'relation' => 'OR',
			array( 'key' => '_nadlan_private_unit_journey', 'compare' => 'NOT EXISTS' ),
			array( 'key' => '_nadlan_private_unit_journey', 'value' => 'private-unit-journey-v2', 'compare' => '!=' ),
		);
		$existing = isset( $args['meta_query'] ) && is_array( $args['meta_query'] ) ? $args['meta_query'] : array();
		$args['meta_query'] = empty( $existing )
			? array( $privacy_clause )
			: array( 'relation' => 'AND', $existing, $privacy_clause );
		return $args;
	}
}
add_filter( 'rest_nadlan_project_query', 'nadlan_flagship_v3_guard_rest_collection', 100, 2 );

if ( ! function_exists( 'nadlan_flagship_v3_guard_rest_item' ) ) {
	/** Private-stage item routes are denial-only for callers without edit access. */
	function nadlan_flagship_v3_guard_rest_item( $result, $server, $request ) {
		unset( $server );
		$route = is_object( $request ) && method_exists( $request, 'get_route' ) ? (string) $request->get_route() : '';
		if ( ! preg_match( '#^/wp/v2/nadlan_project/([1-9][0-9]*)(?:/|$)#', $route, $matches ) ) {
			return $result;
		}
		$post_id = (int) $matches[1];
		if ( nadlan_flagship_v3_is_private_candidate( $post_id ) && ! current_user_can( 'edit_post', $post_id ) ) {
			return new WP_Error( 'nadlan_flagship_private_stage_hidden', 'Not found.', array( 'status' => 404 ) );
		}
		return $result;
	}
}
add_filter( 'rest_pre_dispatch', 'nadlan_flagship_v3_guard_rest_item', 1, 3 );

if ( ! function_exists( 'nadlan_flagship_v3_error' ) ) {
	function nadlan_flagship_v3_error( $code ) {
		return new WP_Error( sanitize_key( (string) $code ), 'Flagship surface contract rejected.' );
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_is_selected' ) ) {
	/** Selection is per post and never a site-wide option. */
	function nadlan_flagship_v3_is_selected( $post_id ) {
		$post_id = (int) $post_id;
		return $post_id > 0
			&& 'nadlan_project' === get_post_type( $post_id )
			&& 'flagship-v3' === (string) get_post_meta( $post_id, 'project_surface_version', true );
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_is_private_candidate' ) ) {
	function nadlan_flagship_v3_is_private_candidate( $post_id = 0 ) {
		$post_id = (int) $post_id;
		if ( $post_id <= 0 ) {
			$post_id = (int) get_queried_object_id();
		}
		$selector = (string) get_post_meta( $post_id, 'project_surface_version', true );
		return 'nadlan_project' === get_post_type( $post_id )
			&& in_array( $selector, array( 'flagship-v3', 'flagship-transition-1-72-210' ), true )
			&& 'private-unit-journey-v2' === (string) get_post_meta( $post_id, '_nadlan_private_unit_journey', true );
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_valid_date_window' ) ) {
	function nadlan_flagship_v3_valid_date_window( $effective_at, $expires_at ) {
		$effective = is_string( $effective_at ) ? strtotime( $effective_at ) : false;
		$expires   = is_string( $expires_at ) ? strtotime( $expires_at ) : false;
		$now       = time();
		return false !== $effective && false !== $expires && $effective <= $now && $expires > $now && $expires > $effective;
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_asset_url' ) ) {
	/**
	 * Project media is accepted only from the site's HTTPS origin and the
	 * reviewed project path marker. Query strings, credentials and fragments
	 * are rejected so signed/external URLs cannot enter the public config.
	 */
	function nadlan_flagship_v3_asset_url( $url, $role, $contract ) {
		$url  = trim( (string) $url );
		$role = sanitize_key( (string) $role );
		if ( '' === $url || preg_match( '/[\x00-\x1F\x7F]/', $url ) ) {
			return '';
		}
		$parts = wp_parse_url( $url );
		$home  = wp_parse_url( home_url( '/' ) );
		if ( ! is_array( $parts ) || ! is_array( $home )
			|| 'https' !== strtolower( isset( $parts['scheme'] ) ? (string) $parts['scheme'] : '' )
			|| empty( $parts['host'] ) || empty( $home['host'] )
			|| strtolower( (string) $parts['host'] ) !== strtolower( (string) $home['host'] )
			|| isset( $parts['user'] ) || isset( $parts['pass'] )
			|| isset( $parts['query'] ) || isset( $parts['fragment'] ) ) {
			return '';
		}
		$home_port = isset( $home['port'] ) ? (int) $home['port'] : 443;
		$url_port  = isset( $parts['port'] ) ? (int) $parts['port'] : 443;
		if ( $home_port !== $url_port ) {
			return '';
		}
		$path = rawurldecode( isset( $parts['path'] ) ? (string) $parts['path'] : '' );
		$path = str_replace( '\\', '/', $path );
		if ( false !== strpos( $path, '/../' ) || false !== strpos( $path, '/./' ) ) {
			return '';
		}
		$is_experience_role = 0 === strpos( $role, 'experience_' );
		$marker = $is_experience_role && isset( $contract['experience_asset_path_marker'] )
			? (string) $contract['experience_asset_path_marker']
			: ( isset( $contract['asset_path_marker'] ) ? (string) $contract['asset_path_marker'] : '' );
		if ( '' === $marker || 0 !== strpos( $path, $marker ) ) {
			return '';
		}
		$extension = strtolower( pathinfo( $path, PATHINFO_EXTENSION ) );
		if ( in_array( $role, array( 'model_hd', 'model_lod' ), true ) ) {
			if ( 'glb' !== $extension ) {
				return '';
			}
		} elseif ( 'poster' === $role ) {
			$expected = isset( $contract['authorized_representations'] ) && is_array( $contract['authorized_representations'] )
				? array_values( array_filter( $contract['authorized_representations'], function ( $asset ) { return is_array( $asset ) && 'poster' === ( isset( $asset['role'] ) ? $asset['role'] : '' ); } ) )
				: array();
			$route_key = isset( $expected[0]['route_key'] ) ? (string) $expected[0]['route_key'] : '';
			/* The public edge intercepts dotted .webp paths before WordPress routes
			   them, so the extensionless compatibility alias declared by the asset
			   contract is also an authorized form of the same governed payload. */
			$route_alias = preg_replace( '/\.webp$/D', '', $route_key );
			if ( '' === $route_key || ! preg_match( '#^media/[a-z0-9][a-z0-9._-]*\.webp$#D', $route_key )
				|| ( ! hash_equals( untrailingslashit( $marker ) . '/' . $route_key, $path )
					&& ! hash_equals( untrailingslashit( $marker ) . '/' . $route_alias, $path ) ) ) {
				return '';
			}
		} elseif ( in_array( $role, array( 'experience_preview', 'experience_fullscreen' ), true ) ) {
			$expected_path = '';
			foreach ( isset( $contract['authorized_experience_assets'] ) && is_array( $contract['authorized_experience_assets'] ) ? $contract['authorized_experience_assets'] : array() as $asset ) {
				$route_key = is_array( $asset ) && isset( $asset['route_key'] ) ? (string) $asset['route_key'] : '';
				if ( ! preg_match( '#^media/experience/[a-z0-9][a-z0-9._-]*\.webp$#D', $route_key ) ) {
					continue;
				}
				$candidate = untrailingslashit( $marker ) . '/' . basename( $route_key );
				$candidate_alias = preg_replace( '/\.webp$/D', '', $candidate );
				if ( hash_equals( $candidate, $path ) || hash_equals( $candidate_alias, $path ) ) {
					$expected_path = $path;
					break;
				}
			}
			if ( '' === $expected_path ) {
				return '';
			}
		} else {
			return '';
		}
		$clean = esc_url_raw( $url, array( 'https' ) );
		return is_string( $clean ) ? $clean : '';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_private_asset_wrapper_prefix' ) ) {
	/** Exact deterministic prefix emitted by scripts/build-flagship-private-assets.mjs. */
	function nadlan_flagship_v3_private_asset_wrapper_prefix() {
		return "<?php\n"
			. "while ( ob_get_level() > 0 ) {\n"
			. "\tob_end_clean();\n"
			. "}\n"
			. "http_response_code( 404 );\n"
			. "header( 'Cache-Control: private, no-store, no-cache, max-age=0, must-revalidate' );\n"
			. "header( 'X-Robots-Tag: noindex, nofollow, noarchive' );\n"
			. "header( 'X-Content-Type-Options: nosniff' );\n"
			. "header( 'Referrer-Policy: no-referrer' );\n"
			. "header( 'Content-Length: 0' );\n"
			. "__halt_compiler();\n";
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_private_asset_registry_entry' ) ) {
	/** Resolve one exact, registry-owned asset name; paths are never inferred. */
	function nadlan_flagship_v3_private_asset_registry_entry( $contract, $requested_name ) {
		$requested_name = (string) $requested_name;
		if ( ! is_array( $contract )
			|| ! preg_match( '#^[a-z0-9][a-z0-9._/-]*$#D', $requested_name )
			|| false !== strpos( $requested_name, '//' )
			|| in_array( '..', explode( '/', $requested_name ), true )
			|| in_array( '.', explode( '/', $requested_name ), true ) ) {
			return array();
		}
		foreach ( isset( $contract['private_assets'] ) && is_array( $contract['private_assets'] ) ? $contract['private_assets'] : array() as $asset ) {
			$route_key        = is_array( $asset ) && isset( $asset['route_key'] ) ? (string) $asset['route_key'] : '';
			$legacy_route_key = is_array( $asset ) && isset( $asset['legacy_route_key'] ) ? (string) $asset['legacy_route_key'] : '';
			if ( ! is_array( $asset ) || ! isset( $asset['requested_name'] )
				|| ( '' !== $route_key || '' !== $legacy_route_key
					? ( ( '' === $route_key || ! hash_equals( $route_key, $requested_name ) )
						&& ( '' === $legacy_route_key || ! hash_equals( $legacy_route_key, $requested_name ) ) )
					: ! hash_equals( (string) $asset['requested_name'], $requested_name ) ) ) {
				continue;
			}
			$storage_file = isset( $asset['storage_file'] ) ? (string) $asset['storage_file'] : '';
			$bytes        = isset( $asset['bytes'] ) ? (int) $asset['bytes'] : 0;
			$sha256       = isset( $asset['sha256'] ) ? strtolower( (string) $asset['sha256'] ) : '';
			$mime         = isset( $asset['mime'] ) ? (string) $asset['mime'] : '';
			if ( 0 !== strpos( $storage_file, 'assets/flagship-v3/private-assets/' )
				|| ! preg_match( '#^[a-z0-9][a-z0-9._/-]*\.asset\.php$#', $storage_file )
				|| false !== strpos( $storage_file, '//' )
				|| in_array( '..', explode( '/', $storage_file ), true )
				|| $bytes <= 0 || ! preg_match( '/^[a-f0-9]{64}$/', $sha256 )
				|| ! in_array( $mime, array( 'model/gltf-binary', 'image/webp' ), true ) ) {
				return array();
			}
			if ( '' !== $route_key && ( ! preg_match( '#^[a-z0-9][a-z0-9._/-]*$#D', $route_key )
				|| false !== strpos( $route_key, '//' )
				|| in_array( '..', explode( '/', $route_key ), true )
				|| in_array( '.', explode( '/', $route_key ), true )
				|| ( 'image/webp' === $mime && ! preg_match( '/\.webp$/D', $route_key ) ) ) ) {
				return array();
			}
			if ( '' !== $legacy_route_key && ( ! preg_match( '#^[a-z0-9][a-z0-9._/-]*$#D', $legacy_route_key )
				|| false !== strpos( $legacy_route_key, '//' )
				|| in_array( '..', explode( '/', $legacy_route_key ), true )
				|| in_array( '.', explode( '/', $legacy_route_key ), true )
				|| hash_equals( $route_key, $legacy_route_key ) ) ) {
				return array();
			}
			return array(
				'requested_name' => (string) $asset['requested_name'],
				'route_key'      => '' !== $route_key ? $route_key : (string) $asset['requested_name'],
				'legacy_route_key' => $legacy_route_key,
				'matched_route_key' => $requested_name,
				'storage_file'   => $storage_file,
				'bytes'          => $bytes,
				'sha256'         => $sha256,
				'mime'           => $mime,
			);
		}
		return array();
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_private_asset_stage_post' ) ) {
	/** Find the one reviewed private stage without falling back to a canonical post. */
	function nadlan_flagship_v3_private_asset_stage_post( $contract ) {
		$slug = isset( $contract['sandbox']['exact_slug'] ) ? (string) $contract['sandbox']['exact_slug'] : '';
		if ( '' === $slug || ! preg_match( '/^[a-z0-9-]+$/', $slug ) ) {
			return null;
		}
		$post = get_page_by_path( $slug, OBJECT, 'nadlan_project' );
		if ( ! is_object( $post ) || empty( $post->ID )
			|| 'publish' !== ( isset( $post->post_status ) ? (string) $post->post_status : '' )
			|| ! hash_equals( $slug, isset( $post->post_name ) ? (string) $post->post_name : '' )
			|| '' === ( isset( $post->post_password ) ? (string) $post->post_password : '' ) ) {
			return null;
		}
		return $post;
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_asset_payload_descriptor' ) ) {
	/** Verify one registry-owned wrapper and its complete binary payload. */
	function nadlan_flagship_v3_asset_payload_descriptor( $contract, $requested_name ) {
		$asset = nadlan_flagship_v3_private_asset_registry_entry( $contract, $requested_name );
		if ( empty( $asset ) ) {
			return nadlan_flagship_v3_error( 'flagship_asset_not_found' );
		}
		$plugin_root  = realpath( dirname( __DIR__ ) );
		$storage_root = is_string( $plugin_root ) ? realpath( $plugin_root . '/assets/flagship-v3/private-assets' ) : false;
		$storage_path = is_string( $plugin_root ) ? realpath( $plugin_root . '/' . $asset['storage_file'] ) : false;
		$root_prefix  = is_string( $storage_root ) ? trailingslashit( str_replace( '\\', '/', $storage_root ) ) : '';
		$clean_path   = is_string( $storage_path ) ? str_replace( '\\', '/', $storage_path ) : '';
		if ( '' === $root_prefix || '' === $clean_path || 0 !== strpos( $clean_path, $root_prefix ) || ! is_readable( $storage_path ) ) {
			return nadlan_flagship_v3_error( 'flagship_asset_storage_missing' );
		}

		$prefix      = nadlan_flagship_v3_private_asset_wrapper_prefix();
		$prefix_size = strlen( $prefix );
		$file_size   = filesize( $storage_path );
		if ( false === $file_size || $prefix_size + (int) $asset['bytes'] !== (int) $file_size ) {
			return nadlan_flagship_v3_error( 'flagship_asset_size_mismatch' );
		}
		$handle = fopen( $storage_path, 'rb' );
		if ( false === $handle ) {
			return nadlan_flagship_v3_error( 'flagship_asset_storage_unreadable' );
		}
		$stored_prefix = fread( $handle, $prefix_size );
		if ( ! is_string( $stored_prefix ) || ! hash_equals( $prefix, $stored_prefix ) ) {
			fclose( $handle );
			return nadlan_flagship_v3_error( 'flagship_asset_wrapper_mismatch' );
		}
		$hash_context = hash_init( 'sha256' );
		$payload_size = 0;
		while ( ! feof( $handle ) ) {
			$chunk = fread( $handle, 1048576 );
			if ( false === $chunk ) {
				fclose( $handle );
				return nadlan_flagship_v3_error( 'flagship_asset_storage_unreadable' );
			}
			if ( '' === $chunk ) {
				continue;
			}
			$payload_size += strlen( $chunk );
			hash_update( $hash_context, $chunk );
		}
		$payload_sha256 = hash_final( $hash_context );
		if ( (int) $asset['bytes'] !== $payload_size || ! hash_equals( (string) $asset['sha256'], $payload_sha256 ) ) {
			fclose( $handle );
			return nadlan_flagship_v3_error( 'flagship_asset_hash_mismatch' );
		}
		if ( 0 !== fseek( $handle, $prefix_size, SEEK_SET ) ) {
			fclose( $handle );
			return nadlan_flagship_v3_error( 'flagship_asset_storage_unreadable' );
		}

		return array_merge(
			$asset,
			array(
				'storage_path'   => $storage_path,
				'payload_offset' => $prefix_size,
				'payload_handle' => $handle,
			)
		);
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_stream_verified_asset' ) ) {
	/** Stream a pre-hashed immutable file handle with bounded memory. */
	function nadlan_flagship_v3_stream_verified_asset( $asset, $method ) {
		$handle = isset( $asset['payload_handle'] ) ? $asset['payload_handle'] : null;
		if ( ! is_resource( $handle ) ) {
			return false;
		}
		$remaining = (int) $asset['bytes'];
		$complete  = true;
		if ( 'HEAD' !== (string) $method ) {
			while ( $remaining > 0 ) {
				$chunk = fread( $handle, min( 1048576, $remaining ) );
				if ( ! is_string( $chunk ) || '' === $chunk ) {
					$complete = false;
					break;
				}
				$remaining -= strlen( $chunk );
				echo $chunk; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- exact pre-verified binary payload.
			}
		}
		fclose( $handle );
		return $complete && ( 'HEAD' === (string) $method || 0 === $remaining );
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_private_asset_descriptor' ) ) {
	/**
	 * Authorize and verify one payload before streaming. The complete payload is
	 * hashed first so a corrupt wrapper can never produce a partial response.
	 */
	function nadlan_flagship_v3_private_asset_descriptor( $project_contract_id, $requested_name ) {
		$project_contract_id = (string) $project_contract_id;
		$contract            = nadlan_flagship_v3_contract( $project_contract_id );
		if ( empty( $contract ) ) {
			return nadlan_flagship_v3_error( 'private_asset_not_found' );
		}
		$post = nadlan_flagship_v3_private_asset_stage_post( $contract );
		if ( ! is_object( $post ) ) {
			return nadlan_flagship_v3_error( 'private_asset_stage_missing' );
		}
		$post_id = (int) $post->ID;
		if ( ! nadlan_flagship_v3_is_selected( $post_id )
			|| ! hash_equals( $project_contract_id, (string) get_post_meta( $post_id, 'project_contract_id', true ) )
			|| ! hash_equals( (string) $contract['sandbox']['privacy_marker'], (string) get_post_meta( $post_id, '_nadlan_private_unit_journey', true ) )
			|| (int) $contract['canonical_post_id'] !== (int) get_post_meta( $post_id, '_nadlan_flagship_source_post_id', true )
			|| '' !== (string) get_post_meta( $post_id, 'source_id', true )
			|| post_password_required( $post_id ) ) {
			return nadlan_flagship_v3_error( 'private_asset_unauthorized' );
		}
		$validated = nadlan_flagship_v3_validate_post( $post_id );
		if ( is_wp_error( $validated ) || ! isset( $validated['contract']['project_contract_id'] )
			|| ! hash_equals( $project_contract_id, (string) $validated['contract']['project_contract_id'] ) ) {
			return nadlan_flagship_v3_error( 'private_asset_stage_invalid' );
		}

		$asset = nadlan_flagship_v3_asset_payload_descriptor( $contract, $requested_name );
		if ( is_wp_error( $asset ) ) {
			return nadlan_flagship_v3_error( 'private_asset_not_found' );
		}
		$asset['post_id'] = $post_id;
		return $asset;
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_private_asset_rewrite' ) ) {
	function nadlan_flagship_v3_private_asset_rewrite() {
		add_rewrite_rule(
			'^flagship-private-asset/([a-z0-9-]+)/([a-z0-9._/-]+)$',
			'index.php?nadlan_flagship_asset_contract=$matches[1]&nadlan_flagship_asset_name=$matches[2]',
			'top'
		);
	}
}
add_action( 'init', 'nadlan_flagship_v3_private_asset_rewrite', 11 );

if ( ! function_exists( 'nadlan_flagship_v3_private_asset_query_vars' ) ) {
	function nadlan_flagship_v3_private_asset_query_vars( $vars ) {
		$vars[] = 'nadlan_flagship_asset_contract';
		$vars[] = 'nadlan_flagship_asset_name';
		return array_values( array_unique( $vars ) );
	}
}
add_filter( 'query_vars', 'nadlan_flagship_v3_private_asset_query_vars' );

if ( ! function_exists( 'nadlan_flagship_v3_private_asset_request' ) ) {
	/** Parse the exact query-free route independently of rewrite-rule flush state. */
	function nadlan_flagship_v3_private_asset_request() {
		$request_uri = isset( $_SERVER['REQUEST_URI'] ) ? (string) wp_unslash( $_SERVER['REQUEST_URI'] ) : '';
		$parts       = wp_parse_url( $request_uri );
		$path        = is_array( $parts ) && isset( $parts['path'] ) ? (string) $parts['path'] : '';
		$route_root  = '/flagship-private-asset';
		$marker      = $route_root . '/';
		if ( $route_root !== $path && 0 !== strpos( $path, $marker ) ) {
			return array();
		}
		$query_string = isset( $_SERVER['QUERY_STRING'] ) ? (string) $_SERVER['QUERY_STRING'] : '';
		$method       = isset( $_SERVER['REQUEST_METHOD'] ) ? strtoupper( (string) $_SERVER['REQUEST_METHOD'] ) : 'GET';
		if ( $route_root === $path || '' !== $query_string || isset( $parts['query'] ) || ! in_array( $method, array( 'GET', 'HEAD' ), true )
			|| false !== strpos( $path, '%' ) || false !== strpos( $path, '\\' ) ) {
			return nadlan_flagship_v3_error( 'private_asset_invalid_request' );
		}
		$route = substr( $path, strlen( $marker ) );
		$bits  = explode( '/', $route, 2 );
		if ( 2 !== count( $bits ) || ! preg_match( '/^[a-z0-9-]+$/', $bits[0] )
			|| ! preg_match( '#^[a-z0-9][a-z0-9._/-]*$#', $bits[1] )
			|| false !== strpos( $bits[1], '//' )
			|| in_array( '..', explode( '/', $bits[1] ), true )
			|| in_array( '.', explode( '/', $bits[1] ), true ) ) {
			return nadlan_flagship_v3_error( 'private_asset_invalid_request' );
		}
		return array( 'project_contract_id' => $bits[0], 'requested_name' => $bits[1], 'method' => $method );
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_private_asset_deny' ) ) {
	/** Exact terminal denial for this binary route only; ordinary page errors keep wp_die(). */
	function nadlan_flagship_v3_private_asset_deny() {
		while ( ob_get_level() > 0 ) {
			ob_end_clean();
		}
		if ( function_exists( 'status_header' ) ) {
			status_header( 404 );
		} else {
			http_response_code( 404 );
		}
		nocache_headers();
		header( 'Cache-Control: private, no-store, no-cache, max-age=0, must-revalidate', true );
		header( 'X-Robots-Tag: noindex, nofollow, noarchive', true );
		header( 'X-Content-Type-Options: nosniff', true );
		header( 'Referrer-Policy: no-referrer', true );
		header( 'Content-Length: 0', true );
		exit;
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_private_asset_template' ) ) {
	/** Terminal binary response; every rejected request receives the same 404. */
	function nadlan_flagship_v3_private_asset_template() {
		$request = nadlan_flagship_v3_private_asset_request();
		if ( empty( $request ) ) {
			return;
		}
		if ( is_wp_error( $request ) ) {
			nadlan_flagship_v3_private_asset_deny();
		}
		$asset = nadlan_flagship_v3_private_asset_descriptor( $request['project_contract_id'], $request['requested_name'] );
		if ( is_wp_error( $asset ) ) {
			nadlan_flagship_v3_private_asset_deny();
		}
		while ( ob_get_level() > 0 ) {
			ob_end_clean();
		}
		if ( function_exists( 'status_header' ) ) {
			status_header( 200 );
		}
		nocache_headers();
		header( 'Content-Type: ' . $asset['mime'], true );
		header( 'Content-Length: ' . (string) $asset['bytes'], true );
		header( 'Cache-Control: private, no-store, no-cache, max-age=0, must-revalidate', true );
		header( 'X-Robots-Tag: noindex, nofollow, noarchive', true );
		header( 'X-Content-Type-Options: nosniff', true );
		header( 'Referrer-Policy: no-referrer', true );
		nadlan_flagship_v3_stream_verified_asset( $asset, $request['method'] );
		exit;
	}
}
add_action( 'template_redirect', 'nadlan_flagship_v3_private_asset_template', -100 );

if ( ! function_exists( 'nadlan_flagship_v3_public_asset_descriptor' ) ) {
	/** Authorize the public route only for the exact doubly-latched canonical post. */
	function nadlan_flagship_v3_public_asset_descriptor( $project_contract_id, $requested_name ) {
		$project_contract_id = (string) $project_contract_id;
		$contract            = nadlan_flagship_v3_contract( $project_contract_id );
		$decision_id         = isset( $contract['public_release_decision_id'] ) ? (string) $contract['public_release_decision_id'] : '';
		$release_meta_key    = isset( $contract['public_release_meta_key'] ) ? (string) $contract['public_release_meta_key'] : '';
		$post_id             = isset( $contract['canonical_post_id'] ) ? (int) $contract['canonical_post_id'] : 0;
		$post                = $post_id > 0 ? get_post( $post_id ) : null;
		$live                = function_exists( 'nadlan_flagship_v3_public_live_contract' ) ? nadlan_flagship_v3_public_live_contract() : false;
		if ( empty( $contract ) || true !== ( isset( $contract['public_release_enabled'] ) ? $contract['public_release_enabled'] : false )
			|| ! is_array( $live ) || $post_id !== (int) ( isset( $live['post_id'] ) ? $live['post_id'] : 0 )
			|| ! preg_match( '/^OWNER-[A-Z0-9-]+$/', $decision_id )
			|| ! preg_match( '/^_nadlan_[a-z0-9_]+$/', $release_meta_key )
			|| ! $post instanceof WP_Post || 'nadlan_project' !== (string) $post->post_type
			|| 'publish' !== (string) $post->post_status || '' !== (string) $post->post_password
			|| ! hash_equals( (string) $contract['canonical_slug'], (string) $post->post_name )
			|| ! nadlan_flagship_v3_is_selected( $post_id )
			|| ! hash_equals( $project_contract_id, (string) get_post_meta( $post_id, 'project_contract_id', true ) )
			|| ! hash_equals( (string) $contract['source_id'], (string) get_post_meta( $post_id, 'source_id', true ) )
			|| ! hash_equals( $decision_id, (string) get_post_meta( $post_id, $release_meta_key, true ) )
			|| metadata_exists( 'post', $post_id, '_nadlan_private_unit_journey' ) ) {
			return nadlan_flagship_v3_error( 'public_asset_release_disabled' );
		}
		$validated = nadlan_flagship_v3_validate_post( $post_id );
		if ( is_wp_error( $validated ) || 'canonical' !== ( isset( $validated['mode'] ) ? $validated['mode'] : '' ) ) {
			return nadlan_flagship_v3_error( 'public_asset_canonical_invalid' );
		}
		$route_asset = nadlan_flagship_v3_private_asset_registry_entry( $contract, $requested_name );
		if ( empty( $route_asset ) || ! hash_equals( (string) $route_asset['matched_route_key'], (string) $requested_name ) ) {
			return nadlan_flagship_v3_error( 'public_asset_not_found' );
		}
		$asset = nadlan_flagship_v3_asset_payload_descriptor( $contract, $requested_name );
		if ( is_wp_error( $asset ) ) {
			return nadlan_flagship_v3_error( 'public_asset_not_found' );
		}
		$asset['post_id'] = $post_id;
		return $asset;
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_public_asset_rewrite' ) ) {
	function nadlan_flagship_v3_public_asset_rewrite() {
		add_rewrite_rule(
			'^flagship-asset/([a-z0-9-]+)/([a-z0-9._/-]+)$',
			'index.php?nadlan_flagship_public_asset_contract=$matches[1]&nadlan_flagship_public_asset_name=$matches[2]',
			'top'
		);
	}
}
add_action( 'init', 'nadlan_flagship_v3_public_asset_rewrite', 11 );

if ( ! function_exists( 'nadlan_flagship_v3_public_asset_query_vars' ) ) {
	function nadlan_flagship_v3_public_asset_query_vars( $vars ) {
		$vars[] = 'nadlan_flagship_public_asset_contract';
		$vars[] = 'nadlan_flagship_public_asset_name';
		return array_values( array_unique( $vars ) );
	}
}
add_filter( 'query_vars', 'nadlan_flagship_v3_public_asset_query_vars' );

if ( ! function_exists( 'nadlan_flagship_v3_public_asset_request' ) ) {
	/** Parse the exact query-free public route without trusting rewrite state. */
	function nadlan_flagship_v3_public_asset_request() {
		$request_uri = isset( $_SERVER['REQUEST_URI'] ) ? (string) wp_unslash( $_SERVER['REQUEST_URI'] ) : '';
		$parts       = wp_parse_url( $request_uri );
		$path        = is_array( $parts ) && isset( $parts['path'] ) ? (string) $parts['path'] : '';
		$route_root  = '/flagship-asset';
		$marker      = $route_root . '/';
		if ( $route_root !== $path && 0 !== strpos( $path, $marker ) ) {
			return array();
		}
		$query_string = isset( $_SERVER['QUERY_STRING'] ) ? (string) $_SERVER['QUERY_STRING'] : '';
		$method       = isset( $_SERVER['REQUEST_METHOD'] ) ? strtoupper( (string) $_SERVER['REQUEST_METHOD'] ) : 'GET';
		if ( $route_root === $path || '' !== $query_string || isset( $parts['query'] ) || ! in_array( $method, array( 'GET', 'HEAD' ), true )
			|| false !== strpos( $path, '%' ) || false !== strpos( $path, '\\' ) ) {
			return nadlan_flagship_v3_error( 'public_asset_invalid_request' );
		}
		$route = substr( $path, strlen( $marker ) );
		$bits  = explode( '/', $route, 2 );
		if ( 2 !== count( $bits ) || ! preg_match( '/^[a-z0-9-]+$/', $bits[0] )
			|| ! preg_match( '#^[a-z0-9][a-z0-9._/-]*$#', $bits[1] )
			|| false !== strpos( $bits[1], '//' )
			|| in_array( '..', explode( '/', $bits[1] ), true )
			|| in_array( '.', explode( '/', $bits[1] ), true ) ) {
			return nadlan_flagship_v3_error( 'public_asset_invalid_request' );
		}
		return array( 'project_contract_id' => $bits[0], 'requested_name' => $bits[1], 'method' => $method );
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_public_asset_template' ) ) {
	function nadlan_flagship_v3_public_asset_template() {
		$request = nadlan_flagship_v3_public_asset_request();
		if ( empty( $request ) ) {
			return;
		}
		if ( is_wp_error( $request ) ) {
			nadlan_flagship_v3_private_asset_deny();
		}
		$asset = nadlan_flagship_v3_public_asset_descriptor( $request['project_contract_id'], $request['requested_name'] );
		if ( is_wp_error( $asset ) ) {
			nadlan_flagship_v3_private_asset_deny();
		}
		while ( ob_get_level() > 0 ) {
			ob_end_clean();
		}
		if ( function_exists( 'status_header' ) ) {
			status_header( 200 );
		}
		header( 'Content-Type: ' . $asset['mime'], true );
		header( 'Content-Length: ' . (string) $asset['bytes'], true );
		header( 'Cache-Control: public, max-age=3600, must-revalidate', true );
		header( 'X-Robots-Tag: noindex, noarchive', true );
		header( 'X-Content-Type-Options: nosniff', true );
		header( 'Referrer-Policy: no-referrer', true );
		nadlan_flagship_v3_stream_verified_asset( $asset, $request['method'] );
		exit;
	}
}
add_action( 'template_redirect', 'nadlan_flagship_v3_public_asset_template', -99 );

if ( ! function_exists( 'nadlan_flagship_v3_validate_inventory' ) ) {
	function nadlan_flagship_v3_validate_inventory( $identity, $post_id ) {
		$inventory = isset( $identity['inventory_contract'] ) && is_array( $identity['inventory_contract'] )
			? $identity['inventory_contract']
			: array();
		$state = isset( $inventory['state'] ) ? (string) $inventory['state'] : '';
		if ( ! in_array( $state, array( 'not_supplied', 'not_verified', 'unavailable' ), true )
			|| ! array_key_exists( 'decision_grade', $inventory )
			|| false !== $inventory['decision_grade']
			|| empty( $inventory['source_ids'] )
			|| ! is_array( $inventory['source_ids'] )
			|| empty( $inventory['note'] )
			|| ! is_string( $inventory['note'] ) ) {
			return nadlan_flagship_v3_error( 'invalid_inventory_contract' );
		}
		$units = nadlan_flagship_v3_json_meta( $post_id, 'project_3d_units' );
		if ( ! empty( $units ) ) {
			return nadlan_flagship_v3_error( 'zero_inventory_required' );
		}
		return array(
			'state'          => $state,
			'decision_grade' => false,
			'effective_at'   => isset( $inventory['effective_at'] ) ? sanitize_text_field( (string) $inventory['effective_at'] ) : '',
			'source_ids'     => array_values( array_filter( array_map( 'sanitize_text_field', $inventory['source_ids'] ) ) ),
		);
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_validate_representations' ) ) {
	function nadlan_flagship_v3_authorized_representation( $contract, $role ) {
		$role = sanitize_key( (string) $role );
		foreach ( isset( $contract['authorized_representations'] ) && is_array( $contract['authorized_representations'] ) ? $contract['authorized_representations'] : array() as $asset ) {
			if ( is_array( $asset ) && $role === ( isset( $asset['role'] ) ? sanitize_key( (string) $asset['role'] ) : '' )
				&& ! empty( $asset['file'] ) && ! empty( $asset['sha256'] )
				&& preg_match( '/^[a-f0-9]{64}$/', (string) $asset['sha256'] ) ) {
				return $asset;
			}
		}
		return array();
	}

	function nadlan_flagship_v3_validate_representations( $registry, $contract, $post_id ) {
		if ( 'nadlan-project-representation-registry/v1' !== ( isset( $registry['schema'] ) ? $registry['schema'] : '' )
			|| (string) $contract['project_contract_id'] !== ( isset( $registry['project_contract_id'] ) ? (string) $registry['project_contract_id'] : '' )
			|| empty( $registry['calibration'] ) || ! is_array( $registry['calibration'] )
			|| empty( $registry['calibration']['calibration_id'] )
			|| empty( $contract['required_calibration_id'] )
			|| (string) $contract['required_calibration_id'] !== (string) $registry['calibration']['calibration_id']
			|| ! isset( $registry['calibration']['north_degrees'] )
			|| 0.0 !== (float) $registry['calibration']['north_degrees']
			|| empty( $registry['representations'] ) || ! is_array( $registry['representations'] ) ) {
			return nadlan_flagship_v3_error( 'invalid_representation_registry' );
		}

		$required  = array_values( (array) $contract['required_representation_roles'] );
		$allowed   = array_values( (array) $contract['owner_decision_ids'] );
		$by_role   = array();
		foreach ( $registry['representations'] as $representation ) {
			if ( ! is_array( $representation ) || empty( $representation['role'] ) ) {
				continue;
			}
			$role = sanitize_key( (string) $representation['role'] );
			$authorized_asset = nadlan_flagship_v3_authorized_representation( $contract, $role );
			if ( ! in_array( $role, $required, true ) || isset( $by_role[ $role ] )
				|| empty( $authorized_asset )
				|| 'owner_approved_illustration' !== ( isset( $representation['representation_kind'] ) ? $representation['representation_kind'] : '' )
				|| ! array_key_exists( 'decision_grade', $representation ) || false !== $representation['decision_grade']
				|| empty( $representation['owner_decision_id'] )
				|| ! in_array( (string) $representation['owner_decision_id'], $allowed, true )
				|| empty( $contract['representation_owner_decision_id'] )
				|| (string) $contract['representation_owner_decision_id'] !== (string) $representation['owner_decision_id']
				|| ! nadlan_flagship_v3_valid_date_window(
					isset( $representation['effective_at'] ) ? $representation['effective_at'] : '',
					isset( $representation['expires_at'] ) ? $representation['expires_at'] : ''
				)
				|| empty( $representation['sha256'] )
				|| ! preg_match( '/^[a-f0-9]{64}$/', (string) $representation['sha256'] )
				|| ! hash_equals( strtolower( (string) $authorized_asset['sha256'] ), strtolower( (string) $representation['sha256'] ) ) ) {
				return nadlan_flagship_v3_error( 'invalid_representation' );
			}
			$url = nadlan_flagship_v3_asset_url(
				isset( $representation['url'] ) ? $representation['url'] : '',
				$role,
				$contract
			);
			if ( '' === $url ) {
				return nadlan_flagship_v3_error( 'unauthorized_representation_url' );
			}
			$url_parts = wp_parse_url( $url );
			$url_file  = is_array( $url_parts ) && isset( $url_parts['path'] ) ? rawurldecode( basename( (string) $url_parts['path'] ) ) : '';
			$expected_url_file = isset( $authorized_asset['route_key'] ) ? basename( (string) $authorized_asset['route_key'] ) : (string) $authorized_asset['file'];
			/* The extensionless edge alias of a governed .webp is the same payload. */
			$expected_url_alias = preg_replace( '/\.webp$/D', '', $expected_url_file );
			if ( $url_file !== $expected_url_file && $url_file !== $expected_url_alias ) {
				return nadlan_flagship_v3_error( 'unauthorized_representation_url' );
			}
			$by_role[ $role ] = array(
				'url'                 => $url,
				'sha256'              => strtolower( (string) $authorized_asset['sha256'] ),
				'representation_kind' => 'owner_approved_illustration',
				'decision_grade'      => false,
				'owner_decision_id'   => (string) $representation['owner_decision_id'],
			);
		}
		foreach ( $required as $role ) {
			if ( ! isset( $by_role[ $role ] ) ) {
				return nadlan_flagship_v3_error( 'missing_representation_role' );
			}
		}
		if ( hash_equals( $by_role['model_hd']['sha256'], $by_role['model_lod']['sha256'] )
			|| $by_role['model_hd']['url'] === $by_role['model_lod']['url'] ) {
			return nadlan_flagship_v3_error( 'lod_must_be_distinct' );
		}

		$meta_urls = array(
			'model_hd'  => (string) get_post_meta( $post_id, 'project_model_glb', true ),
			'model_lod' => (string) get_post_meta( $post_id, 'project_model_lod_glb', true ),
			'poster'    => (string) get_post_meta( $post_id, 'project_model_poster', true ),
		);
		foreach ( $meta_urls as $role => $meta_url ) {
			if ( $by_role[ $role ]['url'] !== nadlan_flagship_v3_asset_url( $meta_url, $role, $contract ) ) {
				return nadlan_flagship_v3_error( 'representation_meta_mismatch' );
			}
		}
		return array(
			'assets'      => $by_role,
			'calibration' => array(
				'calibration_id' => sanitize_key( (string) $contract['required_calibration_id'] ),
				'north_degrees'  => 0,
			),
			'default_orbit'  => isset( $registry['default_orbit'] ) ? sanitize_text_field( (string) $registry['default_orbit'] ) : '35deg 64deg auto',
			'default_target' => isset( $registry['default_target'] ) ? sanitize_text_field( (string) $registry['default_target'] ) : '0m 43m 0m',
		);
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_validate_visual_playground' ) ) {
	function nadlan_flagship_v3_validate_visual_playground( $visual, $contract, $locale ) {
		$expected_tools = array( 'view', 'interior', 'design' );
		$expected_preview_kinds = array(
			'view' => 'satellite_window_view', 'interior' => 'governed_scene_walkthrough',
			'design' => 'illustrative_plan_drag',
		);
		$visual_json = wp_json_encode( $visual, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
		if ( nadlan_flagship_v3_has_delivery_key( $visual )
			|| ( is_string( $visual_json ) && false !== stripos( $visual_json, 'olp' ) )
			|| 'nadlan-visual-playground/v1' !== ( isset( $visual['schema'] ) ? $visual['schema'] : '' )
			|| (string) $contract['project_contract_id'] !== ( isset( $visual['project_contract_id'] ) ? (string) $visual['project_contract_id'] : '' )
			|| (string) $contract['visual_playground_decision_id'] !== ( isset( $visual['decision']['owner_decision_id'] ) ? (string) $visual['decision']['owner_decision_id'] : '' )
			|| 'site_owner' !== ( isset( $visual['decision']['approved_by'] ) ? (string) $visual['decision']['approved_by'] : '' )
			|| ! isset( $visual['decision']['decision_grade'] ) || false !== $visual['decision']['decision_grade']
			|| ! nadlan_flagship_v3_valid_date_window(
				isset( $visual['decision']['effective_at'] ) ? $visual['decision']['effective_at'] : '',
				isset( $visual['decision']['expires_at'] ) ? $visual['decision']['expires_at'] : ''
			)
			|| $locale !== ( isset( $visual['locale'] ) ? (string) $visual['locale'] : '' )
			|| isset( $visual['comments_delivery'] )
			|| ( isset( $visual['writes_enabled'] ) && false !== $visual['writes_enabled'] )
			|| empty( $visual['tools'] ) || ! is_array( $visual['tools'] ) ) {
			return nadlan_flagship_v3_error( 'invalid_visual_playground' );
		}
		$tools = array();
		foreach ( $visual['tools'] as $tool ) {
			$id = is_array( $tool ) && isset( $tool['id'] ) ? sanitize_key( (string) $tool['id'] ) : '';
			if ( ! in_array( $id, $expected_tools, true ) || isset( $tools[ $id ] )
				|| (string) $expected_preview_kinds[ $id ] !== ( isset( $tool['preview_kind'] ) ? (string) $tool['preview_kind'] : '' )
				|| ! isset( $tool['decision_grade'] ) || false !== $tool['decision_grade']
				|| empty( $tool['title'] ) || empty( $tool['description'] ) || empty( $tool['open_label'] ) || empty( $tool['disclosure'] ) ) {
				return nadlan_flagship_v3_error( 'invalid_visual_tool' );
			}
			$tools[ $id ] = array(
				'id'             => $id,
				'preview_kind'   => (string) $expected_preview_kinds[ $id ],
				'title'          => sanitize_text_field( (string) $tool['title'] ),
				'description'    => sanitize_text_field( (string) $tool['description'] ),
				'open_label'     => sanitize_text_field( (string) $tool['open_label'] ),
				'disclosure'     => sanitize_text_field( (string) $tool['disclosure'] ),
				'decision_grade' => false,
			);
		}
		foreach ( $expected_tools as $id ) {
			if ( ! isset( $tools[ $id ] ) ) {
				return nadlan_flagship_v3_error( 'missing_visual_tool' );
			}
		}
		return array(
			'schema'              => 'nadlan-visual-playground/v1',
			'project_contract_id' => (string) $contract['project_contract_id'],
			'locale'              => $locale,
			'decision'            => array(
				'owner_decision_id' => (string) $contract['visual_playground_decision_id'],
				'approved_by'       => 'site_owner',
				'version'           => (string) $contract['visual_playground_version'],
				'effective_at'      => (string) $contract['visual_playground_effective_at'],
				'expires_at'        => (string) $contract['visual_playground_expires_at'],
				'decision_grade'    => false,
			),
			'writes_enabled'      => false,
			'tools'               => array_values( $tools ),
		);
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_source_url' ) ) {
	/** Citation URLs may be external and may carry a GIS query, but must be HTTPS. */
	function nadlan_flagship_v3_source_url( $url ) {
		$url   = trim( (string) $url );
		$parts = wp_parse_url( $url );
		if ( '' === $url || ! is_array( $parts )
			|| 'https' !== strtolower( isset( $parts['scheme'] ) ? (string) $parts['scheme'] : '' )
			|| empty( $parts['host'] ) || isset( $parts['user'] ) || isset( $parts['pass'] ) || isset( $parts['fragment'] ) ) {
			return '';
		}
		$clean = esc_url_raw( $url, array( 'https' ) );
		return is_string( $clean ) ? $clean : '';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_valid_source_ids' ) ) {
	function nadlan_flagship_v3_valid_source_ids( $source_ids, $sources ) {
		if ( empty( $source_ids ) || ! is_array( $source_ids ) ) {
			return false;
		}
		foreach ( $source_ids as $source_id ) {
			if ( ! is_string( $source_id ) || ! isset( $sources[ $source_id ] ) ) {
				return false;
			}
		}
		return true;
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_validate_sourced_rows' ) ) {
	function nadlan_flagship_v3_validate_sourced_rows( $rows, $sources, $required_fields ) {
		if ( empty( $rows ) || ! is_array( $rows ) ) {
			return false;
		}
		foreach ( $rows as $row ) {
			if ( ! is_array( $row ) || ! nadlan_flagship_v3_valid_source_ids( isset( $row['source_ids'] ) ? $row['source_ids'] : array(), $sources ) ) {
				return false;
			}
			foreach ( $required_fields as $field ) {
				if ( ! isset( $row[ $field ] ) || '' === trim( (string) $row[ $field ] ) ) {
					return false;
				}
			}
		}
		return true;
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_model_vector' ) ) {
	/** Validate first-party viewer vectors without allowing arbitrary CSS or markup. */
	function nadlan_flagship_v3_model_vector( $value, $units = false ) {
		$value  = trim( preg_replace( '/\s+/', ' ', (string) $value ) );
		$number = '-?(?:\d+(?:\.\d+)?|\.\d+)';
		$part   = $units ? $number . 'm' : $number;
		return 1 === preg_match( '/^' . $part . ' ' . $part . ' ' . $part . '$/D', $value ) ? $value : '';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_has_delivery_key' ) ) {
	/** Reject embedded delivery, form, tracking and internal-system seams. */
	function nadlan_flagship_v3_has_delivery_key( $value ) {
		if ( ! is_array( $value ) ) {
			return false;
		}
		foreach ( $value as $key => $child ) {
			$normalized_key = is_string( $key ) ? strtolower( preg_replace( '/([a-z0-9])([A-Z])/', '$1_$2', $key ) ) : '';
			if ( '' !== $normalized_key && preg_match( '/(?:^|_)(?:endpoint|webhook|lead|crm|olp|submit|form|route|tracking_pixel)(?:_|$)/', $normalized_key ) ) {
				return true;
			}
			if ( is_array( $child ) && nadlan_flagship_v3_has_delivery_key( $child ) ) {
				return true;
			}
		}
		return false;
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_authorized_experience_asset' ) ) {
	function nadlan_flagship_v3_authorized_experience_asset( $contract, $asset_id, $kind ) {
		$asset_id = sanitize_key( (string) $asset_id );
		$kind     = sanitize_key( (string) $kind );
		foreach ( isset( $contract['authorized_experience_assets'] ) && is_array( $contract['authorized_experience_assets'] ) ? $contract['authorized_experience_assets'] : array() as $asset ) {
			if ( is_array( $asset )
				&& $asset_id === ( isset( $asset['asset_id'] ) ? sanitize_key( (string) $asset['asset_id'] ) : '' )
				&& $kind === ( isset( $asset['kind'] ) ? sanitize_key( (string) $asset['kind'] ) : '' )
				&& ! empty( $asset['scene_id'] ) && preg_match( '/^[a-z0-9][a-z0-9-]*$/', (string) $asset['scene_id'] )
				&& ! empty( $asset['preview_file'] ) && ! empty( $asset['fullscreen_file'] )
				&& ! empty( $asset['bytes'] ) && ! empty( $asset['width'] ) && ! empty( $asset['height'] )
				&& ! empty( $asset['preview_sha256'] ) && preg_match( '/^[a-f0-9]{64}$/', (string) $asset['preview_sha256'] )
				&& ! empty( $asset['fullscreen_sha256'] ) && preg_match( '/^[a-f0-9]{64}$/', (string) $asset['fullscreen_sha256'] ) ) {
				return $asset;
			}
		}
		return array();
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_validate_experiences' ) ) {
	function nadlan_flagship_v3_authorized_illustrative_mapping( $contract, $asset_id ) {
		$asset_id = sanitize_key( (string) $asset_id );
		foreach ( isset( $contract['authorized_illustrative_mappings'] ) && is_array( $contract['authorized_illustrative_mappings'] ) ? $contract['authorized_illustrative_mappings'] : array() as $mapping ) {
			if ( is_array( $mapping ) && $asset_id === ( isset( $mapping['asset_id'] ) ? sanitize_key( (string) $mapping['asset_id'] ) : '' ) ) {
				return $mapping;
			}
		}
		return array();
	}

	/**
	 * Normalize the owner-approved interior/facility illustration registry.
	 * Exact spatial claims are accepted only when they cite a reviewed source.
	 */
	function nadlan_flagship_v3_validate_experiences( $experience, $contract, $locale, $sources, $calibration_id ) {
		$decision = isset( $experience['decision'] ) && is_array( $experience['decision'] ) ? $experience['decision'] : array();
		if ( nadlan_flagship_v3_has_delivery_key( $experience )
			|| 'nadlan-project-experience-registry/v1' !== ( isset( $experience['schema'] ) ? $experience['schema'] : '' )
			|| (string) $contract['project_contract_id'] !== ( isset( $experience['project_contract_id'] ) ? (string) $experience['project_contract_id'] : '' )
			|| $locale !== ( isset( $experience['locale'] ) ? (string) $experience['locale'] : '' )
			|| (string) $contract['experience_decision_id'] !== ( isset( $decision['owner_decision_id'] ) ? (string) $decision['owner_decision_id'] : '' )
			|| 'site_owner' !== ( isset( $decision['approved_by'] ) ? (string) $decision['approved_by'] : '' )
			|| 'owner_approved_illustration' !== ( isset( $decision['representation_kind'] ) ? (string) $decision['representation_kind'] : '' )
			|| ! array_key_exists( 'decision_grade', $decision ) || false !== $decision['decision_grade']
			|| ! hash_equals( (string) $contract['illustrative_mapping_crosswalk_sha256'], isset( $experience['mapping_crosswalk_sha256'] ) ? (string) $experience['mapping_crosswalk_sha256'] : '' )
			|| ! hash_equals( (string) $contract['illustrative_mapping_anchor_summary_sha256'], isset( $experience['mapping_anchor_summary_sha256'] ) ? (string) $experience['mapping_anchor_summary_sha256'] : '' )
			|| ! nadlan_flagship_v3_valid_date_window(
				isset( $decision['effective_at'] ) ? $decision['effective_at'] : '',
				isset( $decision['expires_at'] ) ? $decision['expires_at'] : ''
			)
			|| empty( $experience['heading'] ) || empty( $experience['back_label'] )
			|| empty( $experience['previous_label'] ) || empty( $experience['next_label'] )
			|| empty( $experience['scenes'] ) || ! is_array( $experience['scenes'] ) ) {
			return nadlan_flagship_v3_error( 'invalid_experience_registry' );
		}

		$scenes = array();
		$kinds  = array();
		$model_hotspot_groups = array();
		foreach ( $experience['scenes'] as $scene ) {
			$id            = is_array( $scene ) && isset( $scene['id'] ) ? sanitize_key( (string) $scene['id'] ) : '';
			$asset_id      = is_array( $scene ) && isset( $scene['asset_id'] ) ? sanitize_key( (string) $scene['asset_id'] ) : '';
			$kind          = is_array( $scene ) && isset( $scene['kind'] ) ? sanitize_key( (string) $scene['kind'] ) : '';
			$mapping_state = is_array( $scene ) && isset( $scene['mapping_state'] ) ? sanitize_key( (string) $scene['mapping_state'] ) : '';
			$source_ids    = is_array( $scene ) && isset( $scene['source_ids'] ) && is_array( $scene['source_ids'] ) ? $scene['source_ids'] : array();
			$placement_source_refs = is_array( $scene ) && isset( $scene['placement_source_refs'] ) && is_array( $scene['placement_source_refs'] ) ? $scene['placement_source_refs'] : array();
			$placement_basis = is_array( $scene ) && isset( $scene['placement_basis'] ) ? sanitize_text_field( (string) $scene['placement_basis'] ) : '';
			$placement_confidence = is_array( $scene ) && isset( $scene['placement_confidence'] ) && is_array( $scene['placement_confidence'] ) ? $scene['placement_confidence'] : array();
			$placement_ambiguity = is_array( $scene ) && isset( $scene['placement_ambiguity'] ) ? sanitize_text_field( (string) $scene['placement_ambiguity'] ) : '';
			$model_component = is_array( $scene ) && isset( $scene['model_component'] ) ? sanitize_text_field( (string) $scene['model_component'] ) : '';
			$model_hotspot = is_array( $scene ) && isset( $scene['model_hotspot'] ) && is_array( $scene['model_hotspot'] ) ? $scene['model_hotspot'] : array();
			$model_hotspot_group = is_array( $scene ) && isset( $scene['model_hotspot_group'] ) ? sanitize_key( (string) $scene['model_hotspot_group'] ) : '';
			$position      = nadlan_flagship_v3_model_vector( isset( $model_hotspot['position'] ) ? $model_hotspot['position'] : '', true );
			$normal        = nadlan_flagship_v3_model_vector( isset( $model_hotspot['normal'] ) ? $model_hotspot['normal'] : '', false );
			$preview_url   = nadlan_flagship_v3_asset_url( isset( $scene['preview_url'] ) ? $scene['preview_url'] : '', 'experience_preview', $contract );
			$fullscreen_url = nadlan_flagship_v3_asset_url( isset( $scene['fullscreen_url'] ) ? $scene['fullscreen_url'] : '', 'experience_fullscreen', $contract );
			$authorized_asset = nadlan_flagship_v3_authorized_experience_asset(
				$contract,
				$asset_id,
				$kind
			);
			$authorized_mapping = nadlan_flagship_v3_authorized_illustrative_mapping( $contract, $asset_id );
			$preview_parts    = '' !== $preview_url ? wp_parse_url( $preview_url ) : array();
			$fullscreen_parts = '' !== $fullscreen_url ? wp_parse_url( $fullscreen_url ) : array();
			$preview_file     = is_array( $preview_parts ) && isset( $preview_parts['path'] ) ? rawurldecode( basename( (string) $preview_parts['path'] ) ) : '';
			$fullscreen_file  = is_array( $fullscreen_parts ) && isset( $fullscreen_parts['path'] ) ? rawurldecode( basename( (string) $fullscreen_parts['path'] ) ) : '';
			/* Governed scene files, in dotted form and as their extensionless edge aliases. */
			$expected_preview_file    = ! empty( $authorized_asset )
				? basename( isset( $authorized_asset['route_key'] ) ? (string) $authorized_asset['route_key'] : ( isset( $authorized_asset['preview_file'] ) ? (string) $authorized_asset['preview_file'] : '' ) )
				: '';
			$expected_fullscreen_file = ! empty( $authorized_asset )
				? basename( isset( $authorized_asset['route_key'] ) ? (string) $authorized_asset['route_key'] : ( isset( $authorized_asset['fullscreen_file'] ) ? (string) $authorized_asset['fullscreen_file'] : '' ) )
				: '';
			$expected_preview_alias    = preg_replace( '/\.webp$/D', '', $expected_preview_file );
			$expected_fullscreen_alias = preg_replace( '/\.webp$/D', '', $expected_fullscreen_file );
			$allowed_spatial_source_ids = isset( $contract['spatial_experience_source_ids'] ) && is_array( $contract['spatial_experience_source_ids'] )
				? $contract['spatial_experience_source_ids']
				: array();
			$source_cited_state = isset( $contract['future_verified_mapping_state'] )
				? sanitize_key( (string) $contract['future_verified_mapping_state'] )
				: '';
			$allowed_illustrative_refs = isset( $contract['illustrative_mapping_reference_ids'] ) && is_array( $contract['illustrative_mapping_reference_ids'] )
				? array_values( array_map( 'sanitize_text_field', $contract['illustrative_mapping_reference_ids'] ) )
				: array();
			$placement_refs_valid = ! empty( $placement_source_refs ) && empty( array_diff( $placement_source_refs, $allowed_illustrative_refs ) );
			foreach ( $placement_source_refs as $placement_ref ) {
				if ( ! is_string( $placement_ref ) || ! in_array( $placement_ref, $allowed_illustrative_refs, true ) ) {
					$placement_refs_valid = false;
					break;
				}
			}
			$authorized_confidence = isset( $authorized_mapping['placement_confidence'] ) && is_array( $authorized_mapping['placement_confidence'] ) ? $authorized_mapping['placement_confidence'] : array();
			$placement_confidence_valid = isset( $placement_confidence['zone'], $placement_confidence['exact_point'], $authorized_confidence['zone'], $authorized_confidence['exact_point'] )
				&& is_numeric( $placement_confidence['zone'] ) && is_numeric( $placement_confidence['exact_point'] )
				&& abs( (float) $placement_confidence['zone'] - (float) $authorized_confidence['zone'] ) < 0.000001
				&& abs( (float) $placement_confidence['exact_point'] - (float) $authorized_confidence['exact_point'] ) < 0.000001;
			if ( '' === $id || isset( $scenes[ $id ] ) || ! in_array( $kind, array( 'interior', 'facility' ), true )
				|| 'source_cited_mapping' !== $source_cited_state
				|| ! in_array( $mapping_state, array( 'unmapped_concept', 'owner_approved_illustrative_mapping', $source_cited_state ), true )
				|| 'owner_approved_illustration' !== ( isset( $scene['representation_kind'] ) ? (string) $scene['representation_kind'] : '' )
				|| ! array_key_exists( 'decision_grade', $scene ) || false !== $scene['decision_grade']
				|| empty( $scene['title'] ) || empty( $scene['summary'] ) || empty( $scene['open_label'] )
				|| '' === $preview_url || '' === $fullscreen_url || empty( $authorized_asset )
				|| $id !== sanitize_key( (string) $authorized_asset['scene_id'] )
				|| ! in_array( $preview_file, array( $expected_preview_file, $expected_preview_alias ), true )
				|| ! in_array( $fullscreen_file, array( $expected_fullscreen_file, $expected_fullscreen_alias ), true )
				|| ( 'unmapped_concept' === $mapping_state && ! empty( $model_hotspot ) )
				|| ( 'owner_approved_illustrative_mapping' === $mapping_state && (
					empty( $authorized_mapping )
					|| (string) $contract['illustrative_mapping_owner_decision_id'] !== ( isset( $scene['mapping_owner_decision_id'] ) ? (string) $scene['mapping_owner_decision_id'] : '' )
					|| (string) $authorized_mapping['placement_basis'] !== $placement_basis
					|| ! $placement_confidence_valid
					|| '' === $placement_ambiguity || ! $placement_refs_valid
					|| (string) $authorized_mapping['placement_ambiguity'] !== $placement_ambiguity
					|| array_values( $placement_source_refs ) !== array_values( (array) $authorized_mapping['placement_source_refs'] )
					|| (string) $authorized_mapping['model_component'] !== $model_component
					|| empty( $authorized_mapping['illustrative_zone_id'] )
					|| ! isset( $authorized_mapping['visual_offset_along_normal_m'] ) || ! is_numeric( $authorized_mapping['visual_offset_along_normal_m'] )
					|| '' === $position || '' === $normal
					|| (string) $authorized_mapping['position'] !== $position
					|| (string) $authorized_mapping['normal'] !== $normal
					|| (string) $authorized_mapping['model_hotspot_group'] !== $model_hotspot_group
					|| (string) $calibration_id !== ( isset( $model_hotspot['calibration_id'] ) ? (string) $model_hotspot['calibration_id'] : '' )
					|| ! empty( $source_ids ) ) )
				|| ( $source_cited_state === $mapping_state && ( empty( $allowed_spatial_source_ids ) || '' === $position || '' === $normal
					|| (string) $calibration_id !== ( isset( $model_hotspot['calibration_id'] ) ? (string) $model_hotspot['calibration_id'] : '' ) ) )
				|| ( $source_cited_state === $mapping_state && ( ! nadlan_flagship_v3_valid_source_ids( $source_ids, $sources )
					|| array_diff( $source_ids, $allowed_spatial_source_ids ) ) )
				|| ( ! empty( $source_ids ) && ! nadlan_flagship_v3_valid_source_ids( $source_ids, $sources ) )
				|| empty( $scene['image_hotspots'] ) || ! is_array( $scene['image_hotspots'] ) ) {
				return nadlan_flagship_v3_error( 'invalid_experience_scene' );
			}

			$image_hotspots = array();
			foreach ( $scene['image_hotspots'] as $image_hotspot ) {
				$hotspot_id = is_array( $image_hotspot ) && isset( $image_hotspot['id'] ) ? sanitize_key( (string) $image_hotspot['id'] ) : '';
				$x          = is_array( $image_hotspot ) && isset( $image_hotspot['x_percent'] ) ? $image_hotspot['x_percent'] : null;
				$y          = is_array( $image_hotspot ) && isset( $image_hotspot['y_percent'] ) ? $image_hotspot['y_percent'] : null;
				if ( '' === $hotspot_id || isset( $image_hotspots[ $hotspot_id ] ) || ! is_numeric( $x ) || ! is_numeric( $y )
					|| (float) $x < 0 || (float) $x > 100 || (float) $y < 0 || (float) $y > 100
					|| empty( $image_hotspot['label'] ) || empty( $image_hotspot['detail'] ) ) {
					return nadlan_flagship_v3_error( 'invalid_experience_hotspot' );
				}
				$image_hotspots[ $hotspot_id ] = array(
					'id'        => $hotspot_id,
					'x_percent' => (float) $x,
					'y_percent' => (float) $y,
					'label'     => sanitize_text_field( (string) $image_hotspot['label'] ),
					'detail'    => sanitize_text_field( (string) $image_hotspot['detail'] ),
				);
			}

			$normalized_scene = array(
				'id'                  => $id,
				'asset_id'            => $asset_id,
				'kind'                => $kind,
				'title'               => sanitize_text_field( (string) $scene['title'] ),
				'summary'             => sanitize_text_field( (string) $scene['summary'] ),
				'open_label'          => sanitize_text_field( (string) $scene['open_label'] ),
				'preview_url'         => $preview_url,
				'fullscreen_url'      => $fullscreen_url,
				'preview_sha256'      => strtolower( (string) $authorized_asset['preview_sha256'] ),
				'fullscreen_sha256'   => strtolower( (string) $authorized_asset['fullscreen_sha256'] ),
				'bytes'               => (int) $authorized_asset['bytes'],
				'width'               => (int) $authorized_asset['width'],
				'height'              => (int) $authorized_asset['height'],
				'mapping_state'       => $mapping_state,
				'mapping_owner_decision_id' => 'owner_approved_illustrative_mapping' === $mapping_state
					? (string) $contract['illustrative_mapping_owner_decision_id']
					: '',
				'model_component'       => $model_component,
				'illustrative_zone_id'   => sanitize_key( (string) $authorized_mapping['illustrative_zone_id'] ),
				'visual_offset_along_normal_m' => (float) $authorized_mapping['visual_offset_along_normal_m'],
				'placement_basis'       => $placement_basis,
				'placement_source_refs' => array_values( array_map( 'sanitize_text_field', $placement_source_refs ) ),
				'placement_confidence'  => $placement_confidence_valid ? array(
					'zone'        => (float) $authorized_confidence['zone'],
					'exact_point' => (float) $authorized_confidence['exact_point'],
				) : array(),
				'placement_ambiguity'   => $placement_ambiguity,
				'representation_kind' => 'owner_approved_illustration',
				'decision_grade'      => false,
				'source_cited_mapping'=> $source_cited_state === $mapping_state,
				'source_ids'          => array_values( array_map( 'sanitize_text_field', $source_ids ) ),
				'image_hotspots'      => array_values( $image_hotspots ),
			);
			if ( in_array( $mapping_state, array( 'owner_approved_illustrative_mapping', $source_cited_state ), true ) ) {
				$normalized_scene['model_hotspot'] = array(
					'position'       => $position,
					'normal'         => $normal,
					'calibration_id' => sanitize_key( (string) $model_hotspot['calibration_id'] ),
				);
				$normalized_scene['model_hotspot_group'] = $model_hotspot_group;
				$signature = $position . '|' . $normal . '|' . sanitize_key( (string) $model_hotspot['calibration_id'] );
				if ( isset( $model_hotspot_groups[ $model_hotspot_group ] ) && $model_hotspot_groups[ $model_hotspot_group ] !== $signature ) {
					return nadlan_flagship_v3_error( 'inconsistent_experience_hotspot_group' );
				}
				$model_hotspot_groups[ $model_hotspot_group ] = $signature;
			}
			$scenes[ $id ] = $normalized_scene;
			$kinds[ $kind ] = isset( $kinds[ $kind ] ) ? $kinds[ $kind ] + 1 : 1;
		}
		$minimum_per_kind = isset( $contract['minimum_experience_scenes_per_kind'] )
			? max( 1, min( 8, (int) $contract['minimum_experience_scenes_per_kind'] ) )
			: 1;
		if ( ! isset( $kinds['interior'], $kinds['facility'] )
			|| $kinds['interior'] < $minimum_per_kind || $kinds['facility'] < $minimum_per_kind ) {
			return nadlan_flagship_v3_error( 'missing_experience_kind' );
		}
		$required_hotspot_groups = isset( $contract['required_experience_hotspot_groups'] ) && is_array( $contract['required_experience_hotspot_groups'] )
			? array_values( array_map( 'sanitize_key', $contract['required_experience_hotspot_groups'] ) )
			: array();
		if ( array_diff( $required_hotspot_groups, array_keys( $model_hotspot_groups ) )
			|| array_diff( array_keys( $model_hotspot_groups ), $required_hotspot_groups ) ) {
			return nadlan_flagship_v3_error( 'invalid_experience_hotspot_groups' );
		}
		$scene_group_members = array();
		foreach ( $scenes as $scene_id => $scene ) {
			if ( ! empty( $scene['model_hotspot_group'] ) ) {
				$scene_group_members[ $scene['model_hotspot_group'] ][] = $scene_id;
			}
		}
		foreach ( $scenes as &$normalized_scene ) {
			$group = isset( $normalized_scene['model_hotspot_group'] ) ? $normalized_scene['model_hotspot_group'] : '';
			$normalized_scene['model_hotspot_scene_ids'] = isset( $scene_group_members[ $group ] ) ? array_values( $scene_group_members[ $group ] ) : array();
		}
		unset( $normalized_scene );

		return array(
			'schema'              => 'nadlan-project-experience-registry/v1',
			'project_contract_id' => (string) $contract['project_contract_id'],
			'locale'              => $locale,
			'mapping_crosswalk_sha256' => (string) $contract['illustrative_mapping_crosswalk_sha256'],
			'mapping_anchor_summary_sha256' => (string) $contract['illustrative_mapping_anchor_summary_sha256'],
			'heading'             => sanitize_text_field( (string) $experience['heading'] ),
			'back_label'          => sanitize_text_field( (string) $experience['back_label'] ),
			'previous_label'      => sanitize_text_field( (string) $experience['previous_label'] ),
			'next_label'          => sanitize_text_field( (string) $experience['next_label'] ),
			'decision'            => array(
				'owner_decision_id'   => (string) $contract['experience_decision_id'],
				'approved_by'         => 'site_owner',
				'version'             => (string) $contract['experience_version'],
				'effective_at'        => (string) $contract['experience_effective_at'],
				'expires_at'          => (string) $contract['experience_expires_at'],
				'representation_kind' => 'owner_approved_illustration',
				'decision_grade'      => false,
			),
			'scenes'              => array_values( $scenes ),
		);
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_validate_buyer_decision' ) ) {
	/**
	 * Validate the complete, source-backed Hebrew decision layer. This contract
	 * contains no endpoint and no HTML; every visible value is escaped at render.
	 */
	function nadlan_flagship_v3_validate_buyer_decision( $buyer, $contract, $locale ) {
		if ( nadlan_flagship_v3_has_delivery_key( $buyer )
			|| 'nadlan-buyer-decision-contract/v1' !== ( isset( $buyer['schema'] ) ? $buyer['schema'] : '' )
			|| (string) $contract['project_contract_id'] !== ( isset( $buyer['project_contract_id'] ) ? (string) $buyer['project_contract_id'] : '' )
			|| $locale !== ( isset( $buyer['locale'] ) ? (string) $buyer['locale'] : '' )
			|| empty( $buyer['effective_at'] ) || false === strtotime( (string) $buyer['effective_at'] )
			|| strtotime( (string) $buyer['effective_at'] ) > time()
			|| empty( $buyer['labels'] ) || ! is_array( $buyer['labels'] )
			|| ! isset( $buyer['sources'] ) || ! is_array( $buyer['sources'] ) ) {
			return nadlan_flagship_v3_error( 'invalid_buyer_decision_contract' );
		}

		$required_labels = array( 'facts', 'context', 'sea', 'education', 'transit', 'construction', 'overseas_buyer', 'sources', 'current', 'future', 'source' );
		foreach ( $required_labels as $label ) {
			if ( empty( $buyer['labels'][ $label ] ) || ! is_string( $buyer['labels'][ $label ] ) ) {
				return nadlan_flagship_v3_error( 'missing_buyer_label' );
			}
		}

		$sources = array();
		foreach ( $buyer['sources'] as $source ) {
			$id = is_array( $source ) && isset( $source['id'] ) ? (string) $source['id'] : '';
			if ( ! preg_match( '/^[A-Z][A-Z0-9_-]{1,31}$/', $id ) || isset( $sources[ $id ] )
				|| empty( $source['label'] ) || empty( $source['effective_at'] )
				|| '' === nadlan_flagship_v3_source_url( isset( $source['url'] ) ? $source['url'] : '' ) ) {
				return nadlan_flagship_v3_error( 'invalid_buyer_source' );
			}
			$source['url'] = nadlan_flagship_v3_source_url( $source['url'] );
			$sources[ $id ] = $source;
		}
		if ( empty( $sources ) ) {
			return nadlan_flagship_v3_error( 'missing_buyer_sources' );
		}

		if ( ! nadlan_flagship_v3_validate_sourced_rows( isset( $buyer['facts'] ) ? $buyer['facts'] : array(), $sources, array( 'id', 'label', 'value', 'truth_state' ) ) ) {
			return nadlan_flagship_v3_error( 'invalid_fact_rail' );
		}
		foreach ( $buyer['facts'] as $fact ) {
			if ( ! in_array( (string) $fact['truth_state'], array( 'verified', 'reported', 'current_snapshot', 'owner_approved_illustration' ), true ) ) {
				return nadlan_flagship_v3_error( 'invalid_fact_truth_state' );
			}
		}

		$map = isset( $buyer['context_map'] ) && is_array( $buyer['context_map'] ) ? $buyer['context_map'] : array();
		if ( empty( $map['title'] ) || empty( $map['layers'] ) || ! is_array( $map['layers'] ) ) {
			return nadlan_flagship_v3_error( 'invalid_context_map' );
		}
		$layers = array();
		foreach ( $map['layers'] as $layer ) {
			$id = is_array( $layer ) && isset( $layer['id'] ) ? sanitize_key( (string) $layer['id'] ) : '';
			if ( ! in_array( $id, (array) $contract['required_context_layer_ids'], true ) || isset( $layers[ $id ] )
				|| empty( $layer['label'] )
				|| ! nadlan_flagship_v3_validate_sourced_rows( isset( $layer['items'] ) ? $layer['items'] : array(), $sources, array( 'id', 'label', 'state', 'summary' ) ) ) {
				return nadlan_flagship_v3_error( 'invalid_context_layer' );
			}
			foreach ( $layer['items'] as $item ) {
				if ( isset( $item['lat'] ) && ( ! is_numeric( $item['lat'] ) || abs( (float) $item['lat'] ) > 90 ) ) {
					return nadlan_flagship_v3_error( 'invalid_context_latitude' );
				}
				if ( isset( $item['lng'] ) && ( ! is_numeric( $item['lng'] ) || abs( (float) $item['lng'] ) > 180 ) ) {
					return nadlan_flagship_v3_error( 'invalid_context_longitude' );
				}
			}
			$layers[ $id ] = $layer;
		}
		foreach ( (array) $contract['required_context_layer_ids'] as $layer_id ) {
			if ( ! isset( $layers[ $layer_id ] ) ) {
				return nadlan_flagship_v3_error( 'missing_context_layer' );
			}
		}

		$sea = isset( $buyer['sea'] ) && is_array( $buyer['sea'] ) ? $buyer['sea'] : array();
		if ( empty( $sea['label'] ) || ! isset( $sea['distance_m'] ) || ! is_numeric( $sea['distance_m'] ) || (float) $sea['distance_m'] <= 0
			|| (string) $contract['required_sea_method'] !== ( isset( $sea['method'] ) ? (string) $sea['method'] : '' )
			|| empty( $sea['method_label'] )
			|| ! nadlan_flagship_v3_valid_source_ids( isset( $sea['source_ids'] ) ? $sea['source_ids'] : array(), $sources ) ) {
			return nadlan_flagship_v3_error( 'invalid_sea_context' );
		}

		$education = isset( $buyer['education'] ) && is_array( $buyer['education'] ) ? $buyer['education'] : array();
		if ( empty( $education['snapshot_label'] ) || empty( $education['school_year'] )
			|| ! nadlan_flagship_v3_validate_sourced_rows( isset( $education['schools'] ) ? $education['schools'] : array(), $sources, array( 'name', 'distance_m', 'method' ) )
			|| ! nadlan_flagship_v3_validate_sourced_rows( isset( $education['kindergartens'] ) ? $education['kindergartens'] : array(), $sources, array( 'name', 'distance_m', 'method' ) ) ) {
			return nadlan_flagship_v3_error( 'invalid_education_snapshot' );
		}

		$transit = isset( $buyer['transit'] ) && is_array( $buyer['transit'] ) ? $buyer['transit'] : array();
		if ( empty( $transit['line_label'] )
			|| empty( $transit['current_works'] ) || ! is_array( $transit['current_works'] )
			|| empty( $transit['planned_service'] ) || ! is_array( $transit['planned_service'] )
			|| ! in_array( (string) $transit['current_works']['state'], array( 'observed', 'reported' ), true )
			|| 'planned' !== (string) $transit['planned_service']['state']
			|| ! empty( $transit['planned_service']['operating_date'] )
			|| ! nadlan_flagship_v3_valid_source_ids( isset( $transit['current_works']['source_ids'] ) ? $transit['current_works']['source_ids'] : array(), $sources )
			|| ! nadlan_flagship_v3_valid_source_ids( isset( $transit['planned_service']['source_ids'] ) ? $transit['planned_service']['source_ids'] : array(), $sources ) ) {
			return nadlan_flagship_v3_error( 'invalid_transit_context' );
		}

		$construction = isset( $buyer['construction_and_views'] ) && is_array( $buyer['construction_and_views'] ) ? $buyer['construction_and_views'] : array();
		if ( ! nadlan_flagship_v3_validate_sourced_rows(
			array(
				isset( $construction['current_state'] ) ? $construction['current_state'] : array(),
				isset( $construction['future_context'] ) ? $construction['future_context'] : array(),
				isset( $construction['unit_view_state'] ) ? $construction['unit_view_state'] : array(),
			),
			$sources,
			array( 'label', 'summary', 'state' )
		) ) {
			return nadlan_flagship_v3_error( 'invalid_construction_context' );
		}

		$overseas = isset( $buyer['overseas_buyer'] ) && is_array( $buyer['overseas_buyer'] ) ? $buyer['overseas_buyer'] : array();
		if ( empty( $overseas['title'] ) || empty( $overseas['purchase_structure'] ) || ! is_array( $overseas['purchase_structure'] )
			|| ! nadlan_flagship_v3_valid_source_ids( isset( $overseas['purchase_structure']['source_ids'] ) ? $overseas['purchase_structure']['source_ids'] : array(), $sources )
			|| ! nadlan_flagship_v3_validate_sourced_rows( isset( $overseas['steps'] ) ? $overseas['steps'] : array(), $sources, array( 'id', 'title', 'summary' ) ) ) {
			return nadlan_flagship_v3_error( 'invalid_overseas_path' );
		}

		$action = isset( $buyer['primary_action'] ) && is_array( $buyer['primary_action'] ) ? $buyer['primary_action'] : array();
		if ( empty( $action['label'] ) || empty( $action['target_section'] )
			|| ! in_array( (string) $action['target_section'], array( 'overseas-buyer', 'sources' ), true )
			|| ! empty( $action['url'] ) || ! empty( $action['endpoint'] ) ) {
			return nadlan_flagship_v3_error( 'invalid_primary_action' );
		}

		$buyer['sources'] = array_values( $sources );
		return $buyer;
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_validate_post' ) ) {
	if ( ! function_exists( 'nadlan_flagship_v3_validate_integrations' ) ) {
		function nadlan_flagship_v3_validate_integrations( $buyer, $contract ) {
		$view = isset( $contract['window_view'] ) && is_array( $contract['window_view'] ) ? $contract['window_view'] : array();
		$lead = isset( $contract['lead_contract'] ) && is_array( $contract['lead_contract'] ) ? $contract['lead_contract'] : array();
		$unit = isset( $contract['unit_selection_bridge'] ) && is_array( $contract['unit_selection_bridge'] ) ? $contract['unit_selection_bridge'] : array();
		$lead_consent = nadlan_flagship_v3_lead_consent_contract();
		$corner = array();
		foreach ( isset( $buyer['context_map']['layers'] ) && is_array( $buyer['context_map']['layers'] ) ? $buyer['context_map']['layers'] : array() as $layer ) {
			foreach ( isset( $layer['items'] ) && is_array( $layer['items'] ) ? $layer['items'] : array() as $item ) {
				if ( is_array( $item ) && 'current-corner' === ( isset( $item['id'] ) ? $item['id'] : '' ) ) {
					$corner = $item;
				}
			}
		}
		if ( 'nadlan-einstein-window-view/v1' !== ( isset( $view['schema'] ) ? $view['schema'] : '' )
			|| ! isset( $view['lat'], $view['lng'], $corner['lat'], $corner['lng'] )
			|| abs( (float) $view['lat'] - (float) $corner['lat'] ) > 0.000000001
			|| abs( (float) $view['lng'] - (float) $corner['lng'] ) > 0.000000001
			|| ! isset( $view['illustrative_tower_height_m'] ) || abs( (float) $view['illustrative_tower_height_m'] - 93.22 ) > 0.001
			|| 'owner_approved_model_bounds' !== ( isset( $view['height_basis'] ) ? $view['height_basis'] : '' )
			|| array( 'S001', 'S006' ) !== ( isset( $view['location_source_ids'] ) ? array_values( $view['location_source_ids'] ) : array() )
			|| 'unknown' !== ( isset( $view['bearing_state'] ) ? $view['bearing_state'] : '' )
			|| 'honest_360' !== ( isset( $view['unknown_bearing_fallback'] ) ? $view['unknown_bearing_fallback'] : '' )
			|| 'mapbox://styles/mapbox/satellite-streets-v12' !== ( isset( $view['map_style'] ) ? $view['map_style'] : '' )
			|| '/tour/sde-dov/' !== ( isset( $view['district_tour_url'] ) ? $view['district_tour_url'] : '' )
			|| 'adjacent_district_context_only' !== ( isset( $view['earth_state'] ) ? $view['earth_state'] : '' )
			|| '/earth/sde-dov/' !== ( isset( $view['earth_url'] ) ? $view['earth_url'] : '' )
			|| 'שדה דב הסמוך — הקשר רובעי, לא מיקום איינשטיין' !== ( isset( $view['earth_context_label'] ) ? $view['earth_context_label'] : '' )
			|| 'nadlan-einstein-project-inquiry/v1' !== ( isset( $lead['schema'] ) ? $lead['schema'] : '' )
			|| '/wp-json/nadlan/v1/lead' !== ( isset( $lead['endpoint_path'] ) ? $lead['endpoint_path'] : '' )
			|| 'showroom_unit_journey_v2' !== ( isset( $lead['source'] ) ? $lead['source'] : '' )
			|| 4867 !== ( isset( $lead['card_id'] ) ? (int) $lead['card_id'] : 0 )
			|| 'einstein-tower' !== ( isset( $lead['project_slug'] ) ? $lead['project_slug'] : '' )
			|| 'EINSTEIN TOWER תל אביב' !== ( isset( $lead['project_title'] ) ? $lead['project_title'] : '' )
			|| 'he' !== ( isset( $lead['lang'] ) ? $lead['lang'] : '' )
			|| '/projects/einstein-tower/' !== ( isset( $lead['source_path'] ) ? $lead['source_path'] : '' )
			|| ! preg_match( '/^einstein-project-inquiry-[0-9]{4}-[0-9]{2}-[0-9]{2}$/D', isset( $lead['consent_version'] ) ? (string) $lead['consent_version'] : '' )
			|| ! hash_equals( (string) $lead_consent['version'], isset( $lead['consent_version'] ) ? (string) $lead['consent_version'] : '' )
			|| 'nad-lan.co.il' !== ( isset( $lead['data_controller'] ) ? $lead['data_controller'] : '' )
			|| 'project_inquiry_follow_up' !== ( isset( $lead['purpose'] ) ? $lead['purpose'] : '' )
			|| 'manual_review_until_resolution_or_erasure_request' !== ( isset( $lead['retention_policy'] ) ? $lead['retention_policy'] : '' )
			|| '/contact/' !== ( isset( $lead['rights_path'] ) ? $lead['rights_path'] : '' )
			|| false !== ( isset( $lead['automated_expiry'] ) ? $lead['automated_expiry'] : null )
			|| 'site_admin_fallback' !== ( isset( $lead['routing_state'] ) ? $lead['routing_state'] : '' )
			|| 'recorded_not_routed' !== ( isset( $lead['success_state'] ) ? $lead['success_state'] : '' )
			|| 'nadlan-einstein-unit-map-bridge/v1' !== ( isset( $unit['schema'] ) ? $unit['schema'] : '' )
			|| 'not_supplied' !== ( isset( $unit['inventory_state'] ) ? $unit['inventory_state'] : '' )
			|| false !== ( isset( $unit['production_enabled'] ) ? $unit['production_enabled'] : null )
			|| array( 'showViewCone', 'easeMapToUnitView' ) !== ( isset( $unit['required_methods'] ) ? array_values( $unit['required_methods'] ) : array() ) ) {
			return nadlan_flagship_v3_error( 'invalid_integration_contract' );
		}
		return array( 'window_view' => $view, 'lead' => $lead, 'unit_bridge' => $unit );
		}
	}

	if ( ! function_exists( 'nadlan_flagship_v3_source_id_is_unique' ) ) {
		/** The catalog identity may belong to the canonical post only; sandboxes stay blank. */
		function nadlan_flagship_v3_source_id_is_unique( $source_id, $canonical_post_id ) {
			global $wpdb;
			$source_id         = (string) $source_id;
			$canonical_post_id = (int) $canonical_post_id;
			if ( '' === $source_id || $canonical_post_id < 1 ) {
				return false;
			}
			$ids = $wpdb->get_col(
				$wpdb->prepare(
					"SELECT DISTINCT post_id FROM {$wpdb->postmeta} WHERE meta_key = %s AND meta_value = %s ORDER BY post_id ASC LIMIT 2",
					'source_id',
					$source_id
				)
			);
			return array( $canonical_post_id ) === array_map( 'intval', is_array( $ids ) ? $ids : array() );
		}
	}

	/** Return a normalized runtime contract or a deliberately generic WP_Error. */
	function nadlan_flagship_v3_validate_post( $post_id ) {
		$post_id = (int) $post_id;
		$post    = get_post( $post_id );
		if ( ! $post instanceof WP_Post || ! nadlan_flagship_v3_is_selected( $post_id ) || 'publish' !== (string) $post->post_status ) {
			return nadlan_flagship_v3_error( 'invalid_post' );
		}

		$project_contract_id = (string) get_post_meta( $post_id, 'project_contract_id', true );
		$contract            = nadlan_flagship_v3_contract( $project_contract_id );
		$identity            = nadlan_flagship_v3_json_meta( $post_id, 'project_identity_contract_json' );
		if ( empty( $contract )
			|| 'nadlan-project-identity-contract/v1' !== ( isset( $identity['schema'] ) ? $identity['schema'] : '' )
			|| $project_contract_id !== ( isset( $identity['project_contract_id'] ) ? (string) $identity['project_contract_id'] : '' )
			|| (string) $contract['source_id'] !== ( isset( $identity['source_id'] ) ? (string) $identity['source_id'] : '' )
			|| (int) $contract['canonical_post_id'] !== ( isset( $identity['canonical_post_id'] ) ? (int) $identity['canonical_post_id'] : 0 )
			|| (string) $contract['canonical_slug'] !== ( isset( $identity['canonical_slug'] ) ? (string) $identity['canonical_slug'] : '' )
			|| (string) $contract['parcel'] !== ( isset( $identity['parcel'] ) ? (string) $identity['parcel'] : '' ) ) {
			return nadlan_flagship_v3_error( 'identity_mismatch' );
		}

		$locale = isset( $identity['locale'] ) ? sanitize_key( (string) $identity['locale'] ) : '';
		$page_h1 = isset( $contract['page_h1'][ $locale ] ) ? sanitize_text_field( (string) $contract['page_h1'][ $locale ] ) : '';
		if ( ! in_array( $locale, (array) $contract['allowed_locales'], true ) || '' === $page_h1 ) {
			return nadlan_flagship_v3_error( 'locale_not_approved' );
		}

		$mode = '';
		$runtime_contract  = $contract;
		$catalog_source_id = (string) get_post_meta( $post_id, 'source_id', true );
		if ( $post_id === (int) $contract['canonical_post_id'] ) {
			$release_decision_id = isset( $contract['public_release_decision_id'] ) ? (string) $contract['public_release_decision_id'] : '';
			$release_meta_key    = isset( $contract['public_release_meta_key'] ) ? (string) $contract['public_release_meta_key'] : '';
			$public_asset_marker = isset( $contract['public_asset_path_marker'] ) ? (string) $contract['public_asset_path_marker'] : '';
			$public_experience_marker = isset( $contract['public_experience_asset_path_marker'] ) ? (string) $contract['public_experience_asset_path_marker'] : '';
			if ( ! hash_equals( (string) $contract['source_id'], $catalog_source_id )
				|| (string) $post->post_name !== (string) $contract['canonical_slug'] || true !== ( isset( $contract['public_release_enabled'] ) ? $contract['public_release_enabled'] : false )
				|| '' !== (string) $post->post_password
				|| ! preg_match( '/^OWNER-[A-Z0-9-]+$/', $release_decision_id )
				|| ! preg_match( '/^_nadlan_[a-z0-9_]+$/', $release_meta_key )
				|| ! hash_equals( $release_decision_id, (string) get_post_meta( $post_id, $release_meta_key, true ) )
				|| metadata_exists( 'post', $post_id, '_nadlan_private_unit_journey' )
				|| ! nadlan_flagship_v3_source_id_is_unique( (string) $contract['source_id'], $post_id )
				|| '' === $public_asset_marker || '' === $public_experience_marker ) {
				return nadlan_flagship_v3_error( 'canonical_release_disabled' );
			}
			$runtime_contract['asset_path_marker']            = $public_asset_marker;
			$runtime_contract['experience_asset_path_marker'] = $public_experience_marker;
			$mode = 'canonical';
		} else {
			$sandbox   = isset( $contract['sandbox'] ) && is_array( $contract['sandbox'] ) ? $contract['sandbox'] : array();
			$source_key = isset( $sandbox['source_post_meta_key'] ) ? (string) $sandbox['source_post_meta_key'] : '';
			$pattern    = isset( $sandbox['slug_pattern'] ) ? (string) $sandbox['slug_pattern'] : '';
			if ( '' !== $catalog_source_id
				|| '' === $source_key || (int) get_post_meta( $post_id, $source_key, true ) !== (int) $contract['canonical_post_id']
				|| (string) get_post_meta( $post_id, '_nadlan_private_unit_journey', true ) !== (string) $sandbox['privacy_marker']
				|| '' === (string) $post->post_password || '' === $pattern
				|| 1 !== preg_match( '#' . str_replace( '#', '\\#', $pattern ) . '#D', (string) $post->post_name ) ) {
				return nadlan_flagship_v3_error( 'invalid_private_sandbox' );
			}
			$mode = 'private_sandbox';
		}

		$inventory = nadlan_flagship_v3_validate_inventory( $identity, $post_id );
		if ( is_wp_error( $inventory ) ) {
			return $inventory;
		}
		$representations = nadlan_flagship_v3_validate_representations(
			nadlan_flagship_v3_json_meta( $post_id, 'project_representation_registry_json' ),
			$runtime_contract,
			$post_id
		);
		if ( is_wp_error( $representations ) ) {
			return $representations;
		}
		$visual = nadlan_flagship_v3_validate_visual_playground(
			nadlan_flagship_v3_json_meta( $post_id, 'project_visual_playground_json' ),
			$runtime_contract,
			$locale
		);
		if ( is_wp_error( $visual ) ) {
			return $visual;
		}
		$buyer_decision = nadlan_flagship_v3_validate_buyer_decision(
			nadlan_flagship_v3_json_meta( $post_id, 'project_buyer_decision_contract_json' ),
			$runtime_contract,
			$locale
		);
		if ( is_wp_error( $buyer_decision ) ) {
			return $buyer_decision;
		}
		$integrations = nadlan_flagship_v3_validate_integrations( $buyer_decision, $runtime_contract );
		if ( is_wp_error( $integrations ) ) {
			return $integrations;
		}
		$buyer_sources = array();
		foreach ( $buyer_decision['sources'] as $buyer_source ) {
			$buyer_sources[ (string) $buyer_source['id'] ] = $buyer_source;
		}
		$experiences = nadlan_flagship_v3_validate_experiences(
			nadlan_flagship_v3_json_meta( $post_id, 'project_experience_registry_json' ),
			$runtime_contract,
			$locale,
			$buyer_sources,
			$representations['calibration']['calibration_id']
		);
		if ( is_wp_error( $experiences ) ) {
			return $experiences;
		}

		return array(
			'post_id'         => $post_id,
			'mode'            => $mode,
			'locale'          => $locale,
			'page_h1'         => $page_h1,
			'direction'       => in_array( $locale, array( 'he', 'ar' ), true ) ? 'rtl' : 'ltr',
			'contract'        => $runtime_contract,
			'identity'        => $identity,
			'inventory'       => $inventory,
			'representations' => $representations,
			'visual'          => $visual,
			'experiences'     => $experiences,
			'buyer_decision'  => $buyer_decision,
			'integrations'    => $integrations,
		);
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_base_url' ) ) {
	function nadlan_flagship_v3_base_url() {
		return trailingslashit( plugins_url( 'assets/flagship-v3/', dirname( __DIR__ ) . '/nadlan-config.php' ) );
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_enqueue' ) ) {
	function nadlan_flagship_v3_enqueue() {
		$base = nadlan_flagship_v3_base_url();
		wp_enqueue_style( 'nadlan-flagship-v3-playground', $base . 'flagship-playground.css', array(), NADLAN_CONFIG_VERSION );
		wp_enqueue_style( 'nadlan-flagship-v3', $base . 'flagship.css', array( 'nadlan-flagship-v3-playground' ), NADLAN_CONFIG_VERSION );
		wp_enqueue_script( 'nadlan-flagship-v3-viewer', $base . 'flagship-viewer.js', array(), NADLAN_CONFIG_VERSION, true );
		wp_enqueue_script( 'nadlan-flagship-v3-playground', $base . 'flagship-playground.js', array(), NADLAN_CONFIG_VERSION, true );
		wp_enqueue_script( 'nadlan-flagship-v3-integrations', $base . 'flagship-integrations.js', array(), NADLAN_CONFIG_VERSION, true );
		wp_enqueue_script( 'nadlan-flagship-v3', $base . 'flagship.js', array( 'nadlan-flagship-v3-viewer', 'nadlan-flagship-v3-playground', 'nadlan-flagship-v3-integrations' ), NADLAN_CONFIG_VERSION, true );
		wp_enqueue_script( 'nadlan-flagship-v3-cotour', $base . 'flagship-cotour.js', array( 'nadlan-flagship-v3' ), NADLAN_CONFIG_VERSION, true );
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_copy' ) ) {
	/** Hebrew is the only approved first-release locale; add complete packs later. */
	function nadlan_flagship_v3_copy( $locale ) {
		$copy = array(
			'he' => array(
				'heading'          => 'הפרויקט בתלת ממד',
				'model_label'      => 'מודל אינטראקטיבי של הפרויקט',
				'demo_label'       => 'הדמיה מאושרת',
				'reset'            => 'חזרה למבט הראשי',
				'zoom_in'          => 'התקרבות',
				'zoom_out'         => 'התרחקות',
				'inventory_status' => 'בחירת דירה ומחיר ייפתחו לאחר חיבור מלאי מאומת.',
				'loading'          => 'המודל נטען',
				'error'            => 'המודל לא נטען. תמונת הפרויקט נשארת זמינה.',
			),
		);
		return isset( $copy[ $locale ] ) ? $copy[ $locale ] : array();
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_lead_consent_contract' ) ) {
	function nadlan_flagship_v3_lead_consent_contract() {
		return array(
			'version' => 'einstein-project-inquiry-2026-08-15',
			'text'    => '[einstein-project-inquiry-2026-08-15] אני מסכים/ה שנדלן (nad-lan.co.il) תשמור ותשתמש בפרטים לטיפול בפנייה. הפרטים נשמרים לבחינה ידנית עד השלמת הטיפול או בקשת מחיקה; אין מחיקה אוטומטית ואין התחייבות להעברה ליזם או ליועץ.',
		);
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_mapbox_public_token' ) ) {
	/** Return the existing public token only when it matches the Mapbox public-token contract. */
	function nadlan_flagship_v3_mapbox_public_token() {
		$token = trim( (string) get_option( 'nadlan_mapbox_token', '' ) );
		return 1 === preg_match( '/^pk\.[A-Za-z0-9._-]{20,512}$/D', $token ) ? $token : '';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_lead_pipeline_ready' ) ) {
	/** The governed form is public only while the existing E2E pipeline and truthful admin fallback are ready. */
	function nadlan_flagship_v3_lead_pipeline_ready() {
		$post = get_post( 4867 );
		$admin_email = sanitize_email( (string) get_option( 'admin_email', '' ) );
		return $post instanceof WP_Post && 'nadlan_project' === (string) $post->post_type
			&& function_exists( 'nadlan_lead_e2e_enabled' ) && nadlan_lead_e2e_enabled()
			&& false !== is_email( $admin_email )
			&& 0 === (int) get_post_meta( 4867, 'owner_user_id', true );
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_runtime_config' ) ) {
	function nadlan_flagship_v3_vector_values( $value ) {
		return array_map(
			'floatval',
			preg_split( '/\s+/', str_replace( 'm', '', trim( (string) $value ) ) )
		);
	}

	function nadlan_flagship_v3_playground_experience_assets( $experiences ) {
		$groups = array(
			'interior' => array( 'representation_kind' => 'representative_concept', 'experience_kind' => 'representative_concept', 'scenes' => array() ),
			'facilities' => array( 'representation_kind' => 'selectable_concept_gallery', 'experience_kind' => 'selectable_concept_gallery', 'scenes' => array() ),
		);
		foreach ( $experiences['scenes'] as $scene ) {
			$key  = 'interior' === $scene['kind'] ? 'interior' : 'facilities';
			$kind = $groups[ $key ]['experience_kind'];
			$groups[ $key ]['scenes'][] = array(
				'id' => (string) $scene['id'], 'asset_id' => (string) $scene['asset_id'], 'label' => (string) $scene['title'],
				'url' => wp_make_link_relative( (string) $scene['fullscreen_url'] ), 'sha256' => (string) $scene['fullscreen_sha256'],
				'bytes' => (int) $scene['bytes'], 'width' => (int) $scene['width'], 'height' => (int) $scene['height'],
				'experience_kind' => $kind, 'hotspot_id' => (string) $scene['model_hotspot_group'],
				'open_surface_tool_id' => 'interior', 'illustrative_position' => nadlan_flagship_v3_vector_values( $scene['model_hotspot']['position'] ),
				'mapping_state' => 'owner_approved_illustrative_mapping', 'decision_grade' => false,
				'mapping_owner_decision_id' => (string) $scene['mapping_owner_decision_id'],
				'placement_source_refs' => array_values( $scene['placement_source_refs'] ),
				'placement_confidence' => $scene['placement_confidence'],
				'placement_basis' => (string) $scene['placement_basis'],
				'placement_ambiguity' => (string) $scene['placement_ambiguity'],
			);
		}
		foreach ( $groups as &$group ) {
			$group['mapping_state'] = 'owner_approved_illustrative_mapping';
			$group['decision_grade'] = false;
		}
		unset( $group );
		return $groups;
	}

	function nadlan_flagship_v3_playground_experience_mapping( $experiences, $contract ) {
		$anchors = array();
		foreach ( $experiences['scenes'] as $scene ) {
			$group = (string) $scene['model_hotspot_group'];
			if ( isset( $anchors[ $group ] ) ) {
				$anchors[ $group ]['scene_ids'][] = (string) $scene['id'];
				continue;
			}
			$components = array_values( array_filter( array_map( 'sanitize_text_field', explode( ';', (string) $scene['model_component'] ) ) ) );
			$anchors[ $group ] = array(
				'hotspot_id' => $group, 'tool_id' => 'interior' === $scene['kind'] ? 'interior' : 'facilities',
				'open_surface_tool_id' => 'interior',
				'kind' => 'interior' === $scene['kind'] ? 'interior_walkthrough' : ( 'facility-arrival-concept' === $group ? 'facility_arrival_concept' : 'facility_landscaped_open_space_concept' ),
				'experience_kind' => 'interior' === $scene['kind'] ? 'representative_concept' : 'selectable_concept_gallery',
				'scene_ids' => array( (string) $scene['id'] ), 'model_component_ids' => $components,
				'illustrative_zone_id' => (string) $scene['illustrative_zone_id'],
				'position' => nadlan_flagship_v3_vector_values( $scene['model_hotspot']['position'] ),
				'surface_normal' => nadlan_flagship_v3_vector_values( $scene['model_hotspot']['normal'] ),
				'visual_offset_along_normal_m' => (float) $scene['visual_offset_along_normal_m'],
				'confidence' => 'model_zone_fit_high__source_spatial_confidence_none',
				'placement_confidence' => $scene['placement_confidence'],
				'evidence_basis' => array(
					'primary_reference_ids' => array_slice( $scene['placement_source_refs'], 0, 1 ),
					'corroborating_reference_ids' => array_slice( $scene['placement_source_refs'], 1 ),
					'source_anchors' => array(), 'supports' => (string) $scene['placement_basis'],
				),
				'ambiguity' => (string) $scene['placement_ambiguity'],
				'prohibited_inferences' => array( 'unit identity', 'floor identity', 'official location', 'delivery commitment' ),
			);
		}
		return array(
			'active_state' => 'owner_approved_illustrative_mapping',
			'future_verified_state' => (string) $contract['future_verified_mapping_state'],
			'coordinate_space' => 'model_metres_y_up', 'source_cited' => false, 'decision_grade' => false,
			'real_world_orientation_calibrated' => false, 'anchors' => array_values( $anchors ),
		);
	}

	/**
	 * Read the reusable decision-room contract from the signed registry. This is
	 * structural configuration, not another mutable WordPress metadata surface.
	 */
	function nadlan_flagship_v3_decision_experience_contract( $contract ) {
		$decision = isset( $contract['decision_experience'] ) && is_array( $contract['decision_experience'] )
			? $contract['decision_experience']
			: array();
		$required_order = array(
			'approved_lead',
			'non_affiliation_notice',
			'project_model',
			'attached_area_map',
			'primary_actions',
			'decision_tools',
			'tutorial_film',
			'original_article',
			'supporting_content',
		);
		$required_journey = array( 'understand', 'locate', 'explore', 'verify', 'compare', 'collaborate', 'inquire', 'return' );
		$required_evidence = array( 'verified', 'measured', 'planned', 'simulated', 'illustrative', 'unknown' );
		$selection = isset( $decision['selection_behavior'] ) && is_array( $decision['selection_behavior'] )
			? $decision['selection_behavior']
			: array();
		$state_graph = isset( $decision['state_graph'] ) && is_array( $decision['state_graph'] )
			? $decision['state_graph']
			: array();
		$actions = isset( $decision['primary_actions'] ) && is_array( $decision['primary_actions'] )
			? $decision['primary_actions']
			: array();
		$interest = isset( $actions['interest'] ) && is_array( $actions['interest'] ) ? $actions['interest'] : array();
		$whatsapp = isset( $actions['whatsapp'] ) && is_array( $actions['whatsapp'] ) ? $actions['whatsapp'] : array();
		$film = isset( $decision['tutorial_film'] ) && is_array( $decision['tutorial_film'] )
			? $decision['tutorial_film']
			: array();
		$capabilities = isset( $decision['capabilities'] ) && is_array( $decision['capabilities'] )
			? $decision['capabilities']
			: array();
		$allowed_capability_states = array(
			'ready',
			'ready_with_context_label',
			'requires_verified_data',
			'requires_calibrated_orientation_and_geometry',
			'requires_adapter_verification',
		);
		$required_shareable_keys = array( 'selectedEntity', 'model', 'map', 'media' );
		$selection_laws = array(
			'hotspot_opens_in_place_card',
			'automatic_fullscreen_forbidden',
			'explicit_deeper_action_required',
			'back_to_building_required',
			'facility_cone_forbidden_without_verified_bearing',
			'facility_map_pan_forbidden_without_verified_coordinates',
		);
		if ( 'nadlan-spatial-decision-experience/v1' !== ( isset( $decision['schema'] ) ? (string) $decision['schema'] : '' )
			|| empty( $decision['owner_decision_id'] )
			|| ! in_array( (string) $decision['owner_decision_id'], (array) ( isset( $contract['owner_decision_ids'] ) ? $contract['owner_decision_ids'] : array() ), true )
			|| $required_journey !== array_values( isset( $decision['journey'] ) && is_array( $decision['journey'] ) ? $decision['journey'] : array() )
			|| $required_order !== array_values( isset( $decision['page_order'] ) && is_array( $decision['page_order'] ) ? $decision['page_order'] : array() )
			|| $required_evidence !== array_values( isset( $decision['evidence_states'] ) && is_array( $decision['evidence_states'] ) ? $decision['evidence_states'] : array() )
			|| 'nadlan-spatial-decision-state/v1' !== ( isset( $state_graph['schema'] ) ? (string) $state_graph['schema'] : '' )
			|| $required_shareable_keys !== array_values( isset( $state_graph['shareable_keys'] ) && is_array( $state_graph['shareable_keys'] ) ? $state_graph['shareable_keys'] : array() )
			|| empty( $state_graph['synchronized_consumers'] ) || ! is_array( $state_graph['synchronized_consumers'] )
			|| true !== ( isset( $state_graph['unknown_values_must_remain_null'] ) ? $state_graph['unknown_values_must_remain_null'] : false )
			|| 'adopt_existing' !== ( isset( $interest['mode'] ) ? (string) $interest['mode'] : '' )
			|| ! preg_match( '/^#[A-Za-z][A-Za-z0-9_:.-]{0,127}$/D', isset( $interest['target'] ) ? (string) $interest['target'] : '' )
			|| 'adopt_existing' !== ( isset( $whatsapp['mode'] ) ? (string) $whatsapp['mode'] : '' )
			|| empty( $whatsapp['selector'] ) || strlen( (string) $whatsapp['selector'] ) > 256
			|| preg_match( '/[\x00-\x1F\x7F<>\{\}]/', (string) $whatsapp['selector'] )
			|| empty( $film['attachment_id'] ) || (int) $film['attachment_id'] <= 0
			|| 'video/mp4' !== ( isset( $film['expected_mime'] ) ? (string) $film['expected_mime'] : '' )
			|| ! preg_match( '#^/wp-content/uploads/[0-9]{4}/[0-9]{2}/[a-z0-9][a-z0-9._-]*\.mp4$#D', isset( $film['expected_path'] ) ? (string) $film['expected_path'] : '' )
			|| empty( $film['duration_seconds'] ) || empty( $film['width'] ) || empty( $film['height'] )
			|| true === ( isset( $film['autoplay'] ) ? $film['autoplay'] : true )
			|| 'silent_no_audio_track' !== ( isset( $film['audio_state'] ) ? (string) $film['audio_state'] : '' )
			|| 'nadlan_product_concept_demonstration_not_einstein_inventory' !== ( isset( $film['content_scope'] ) ? (string) $film['content_scope'] : '' )
			|| 'not_applicable_silent_visual' !== ( isset( $film['captions_state'] ) ? (string) $film['captions_state'] : '' )
			|| ! isset( $film['companion_summary'] ) || ! is_array( $film['companion_summary'] ) || 4 !== count( $film['companion_summary'] )
			|| empty( $film['fallback_state'] )
			|| empty( $capabilities ) ) {
			return array();
		}
		foreach ( $film['companion_summary'] as $summary_item ) {
			if ( ! is_string( $summary_item ) || '' === trim( $summary_item ) || strlen( $summary_item ) > 180 || preg_match( '/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/', $summary_item ) ) {
				return array();
			}
		}
		foreach ( $selection_laws as $law ) {
			if ( true !== ( isset( $selection[ $law ] ) ? $selection[ $law ] : false ) ) {
				return array();
			}
		}
		foreach ( $state_graph['synchronized_consumers'] as $state_key ) {
			if ( ! is_string( $state_key ) || ! preg_match( '/^[a-z][a-z0-9_]*$/D', $state_key ) ) {
				return array();
			}
		}
		foreach ( $capabilities as $capability => $state ) {
			if ( ! is_string( $capability ) || ! preg_match( '/^[a-z][a-z0-9_]*$/D', $capability )
				|| ! in_array( $state, $allowed_capability_states, true ) ) {
				return array();
			}
		}
		return $decision;
	}

	function nadlan_flagship_v3_runtime_config( $validated ) {
		$copy = nadlan_flagship_v3_copy( $validated['locale'] );
		$asset_prefix_url = isset( $validated['contract']['experience_asset_path_marker'] ) ? (string) $validated['contract']['experience_asset_path_marker'] : '';
		$mapbox_token = nadlan_flagship_v3_mapbox_public_token();
		$rights_url = home_url( '/contact/' );
		$lead_consent = nadlan_flagship_v3_lead_consent_contract();
		return array(
			'schema'   => 'nadlan-flagship-runtime/v3',
			'playground_trust' => array(
				'allowed_asset_prefix' => $asset_prefix_url,
				'allowed_evidence_reference_ids' => array_values( (array) $validated['contract']['illustrative_mapping_reference_ids'] ),
			),
			'identity' => array(
				'project_contract_id' => (string) $validated['contract']['project_contract_id'],
				'public_slug'        => (string) $validated['contract']['canonical_slug'],
				'representation_name'=> (string) $validated['page_h1'],
			),
			'playground' => array(
				'identity' => array(
					'project_contract_id' => (string) $validated['contract']['project_contract_id'],
					'public_slug'          => (string) $validated['contract']['canonical_slug'],
					'representation_name'  => (string) $validated['page_h1'],
				),
				'decision' => $validated['visual']['decision'],
				'experience_decision' => $validated['experiences']['decision'],
				'experience_assets' => nadlan_flagship_v3_playground_experience_assets( $validated['experiences'] ),
				'experience_mapping' => nadlan_flagship_v3_playground_experience_mapping( $validated['experiences'], $validated['contract'] ),
				'heading' => sanitize_text_field( (string) $validated['experiences']['heading'] ),
				'hint' => sanitize_text_field( (string) $validated['experiences']['heading'] ),
				'illustration_label' => $copy['demo_label'],
				'back_label' => sanitize_text_field( (string) $validated['experiences']['back_label'] ),
				'previous_label' => sanitize_text_field( (string) $validated['experiences']['previous_label'] ),
				'next_label' => sanitize_text_field( (string) $validated['experiences']['next_label'] ),
				'page_label' => '{current} / {total}',
				'tools' => $validated['visual']['tools'],
			),
			'locale'    => $validated['locale'],
			'direction' => $validated['direction'],
			'mode'      => $validated['mode'],
			'model'     => array(
				'hd'             => $validated['representations']['assets']['model_hd'],
				'lod'            => $validated['representations']['assets']['model_lod'],
				'poster'         => $validated['representations']['assets']['poster'],
				'calibration'    => $validated['representations']['calibration'],
				'default_orbit'  => $validated['representations']['default_orbit'],
				'default_target' => $validated['representations']['default_target'],
			),
			'inventory' => $validated['inventory'],
			'visual'    => $validated['visual'],
			'experiences' => $validated['experiences'],
			'buyer_decision' => $validated['buyer_decision'],
			'decision_experience' => nadlan_flagship_v3_decision_experience_contract( $validated['contract'] ),
			'integrations' => array(
				'window_view' => array_merge( $validated['integrations']['window_view'], array( 'mapbox_public_token' => $mapbox_token ) ),
				'lead' => array_merge( $validated['integrations']['lead'], array(
					'endpoint' => rest_url( 'nadlan/v1/lead' ),
					'source_url' => home_url( '/projects/einstein-tower/' ),
					'rights_url' => $rights_url,
					'consent_text' => (string) $lead_consent['text'],
				) ),
				'unit_bridge' => $validated['integrations']['unit_bridge'],
				'design_url' => home_url( '/tour/designer/' ),
				'district_tour_url' => home_url( '/tour/sde-dov/' ),
				'earth_url' => home_url( '/earth/sde-dov/' ),
				'earth_context_label' => (string) $validated['integrations']['window_view']['earth_context_label'],
				'co_tour' => function_exists( 'nadlan_flagship_cotour_runtime_contract' )
					? nadlan_flagship_cotour_runtime_contract( $validated['contract'] )
					: array(),
			),
			'copy'      => $copy,
			'capabilities' => array(
				'inventory_selection' => false,
				'lead_submission'     => true,
				'comment_submission'  => false,
				'content_writes_enabled' => false,
			),
		);
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_is_lead_request' ) ) {
	function nadlan_flagship_v3_is_lead_request( $request ) {
		if ( ! is_object( $request ) || ! method_exists( $request, 'get_route' ) || '/nadlan/v1/lead' !== (string) $request->get_route()
			|| ! method_exists( $request, 'get_method' ) || 'POST' !== strtoupper( (string) $request->get_method() ) ) {
			return false;
		}
		$params = method_exists( $request, 'get_json_params' ) ? $request->get_json_params() : array();
		if ( ! is_array( $params ) ) {
			return false;
		}
		return 4867 === (int) ( isset( $params['card_id'] ) ? $params['card_id'] : 0 )
			|| 4867 === (int) ( isset( $params['lead_card_id'] ) ? $params['lead_card_id'] : 0 )
			|| 4867 === (int) ( isset( $params['project_wp_id'] ) ? $params['project_wp_id'] : 0 )
			|| 4867 === (int) ( isset( $params['wp_id'] ) ? $params['wp_id'] : 0 )
			|| 'einstein-tower' === ( isset( $params['project_slug'] ) ? (string) $params['project_slug'] : '' );
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_guard_lead_request' ) ) {
	/** Bind Einstein inquiries to the signed generic-project contract before the shared lead callback. */
	function nadlan_flagship_v3_guard_lead_request( $response, $handler, $request ) {
		unset( $handler );
		if ( null !== $response || ! nadlan_flagship_v3_is_lead_request( $request ) ) {
			return $response;
		}
		$params = $request->get_json_params();
		$consent = nadlan_flagship_v3_lead_consent_contract();
		$allowed_keys = array(
			'card_id', 'company', 'consent', 'consent_text', 'consent_version',
			'direction', 'email', 'floor', 'lang', 'message', 'name', 'phone',
			'project_slug', 'project_title', 'project_wp_id', 'rooms', 'source',
			'source_url', 'sqm', 'status', 'unit', 'wp_id',
		);
		$empty_inventory = array( 'unit', 'floor', 'rooms', 'sqm', 'direction', 'status' );
		$name = is_array( $params ) ? trim( (string) ( isset( $params['name'] ) ? $params['name'] : '' ) ) : '';
		$phone_raw = is_array( $params ) ? trim( (string) ( isset( $params['phone'] ) ? $params['phone'] : '' ) ) : '';
		$phone = preg_replace( '/[^0-9+]/', '', $phone_raw );
		$email_raw = is_array( $params ) ? trim( (string) ( isset( $params['email'] ) ? $params['email'] : '' ) ) : '';
		$email = sanitize_email( $email_raw );
		$message = is_array( $params ) ? (string) ( isset( $params['message'] ) ? $params['message'] : '' ) : '';
		$source_url = is_array( $params ) ? trim( (string) ( isset( $params['source_url'] ) ? $params['source_url'] : '' ) ) : '';
		$origin = method_exists( $request, 'get_header' ) ? trim( (string) $request->get_header( 'origin' ) ) : '';
		$origin_parts = '' !== $origin ? wp_parse_url( $origin ) : array();
		$home_parts = wp_parse_url( home_url( '/' ) );
		$source_parts = '' !== $source_url ? wp_parse_url( $source_url ) : array();
		$length = function_exists( 'mb_strlen' ) ? 'mb_strlen' : 'strlen';
		$port = static function ( $parts ) {
			if ( isset( $parts['port'] ) ) {
				return (int) $parts['port'];
			}
			return 'https' === strtolower( isset( $parts['scheme'] ) ? (string) $parts['scheme'] : '' ) ? 443 : 80;
		};
		$same_origin = '' === $origin || ( is_array( $origin_parts ) && is_array( $home_parts )
			&& strtolower( isset( $origin_parts['scheme'] ) ? (string) $origin_parts['scheme'] : '' ) === strtolower( isset( $home_parts['scheme'] ) ? (string) $home_parts['scheme'] : '' )
			&& strtolower( isset( $origin_parts['host'] ) ? (string) $origin_parts['host'] : '' ) === strtolower( isset( $home_parts['host'] ) ? (string) $home_parts['host'] : '' )
			&& $port( $origin_parts ) === $port( $home_parts ) );
		$canonical_source = is_array( $source_parts ) && is_array( $home_parts )
			&& strtolower( isset( $source_parts['scheme'] ) ? (string) $source_parts['scheme'] : '' ) === strtolower( isset( $home_parts['scheme'] ) ? (string) $home_parts['scheme'] : '' )
			&& strtolower( isset( $source_parts['host'] ) ? (string) $source_parts['host'] : '' ) === strtolower( isset( $home_parts['host'] ) ? (string) $home_parts['host'] : '' )
			&& $port( $source_parts ) === $port( $home_parts )
			&& '/projects/einstein-tower/' === ( isset( $source_parts['path'] ) ? (string) $source_parts['path'] : '' )
			&& ! isset( $source_parts['query'] ) && ! isset( $source_parts['fragment'] ) && ! isset( $source_parts['user'] ) && ! isset( $source_parts['pass'] );
		$actual_keys = is_array( $params ) ? array_keys( $params ) : array();
		sort( $actual_keys, SORT_STRING );
		sort( $allowed_keys, SORT_STRING );
		$phone_valid = '' === $phone_raw || ( hash_equals( $phone_raw, $phone ) && 1 === preg_match( '/^\+?[0-9]{7,15}$/D', $phone_raw ) );
		$email_valid = '' === $email_raw || ( hash_equals( $email_raw, $email ) && false !== is_email( $email_raw ) );
		$valid = is_array( $params )
			&& $actual_keys === $allowed_keys && $same_origin && $canonical_source
			&& call_user_func( $length, $name ) >= 2 && call_user_func( $length, $name ) <= 120
			&& $phone_valid && $email_valid && ( '' !== $phone_raw || '' !== $email_raw )
			&& call_user_func( $length, $message ) <= 4000
			&& 'showroom_unit_journey_v2' === ( isset( $params['source'] ) ? (string) $params['source'] : '' )
			&& 4867 === (int) ( isset( $params['card_id'] ) ? $params['card_id'] : 0 )
			&& 4867 === (int) ( isset( $params['project_wp_id'] ) ? $params['project_wp_id'] : 0 )
			&& 4867 === (int) ( isset( $params['wp_id'] ) ? $params['wp_id'] : 0 )
			&& 'einstein-tower' === ( isset( $params['project_slug'] ) ? (string) $params['project_slug'] : '' )
			&& 'EINSTEIN TOWER תל אביב' === ( isset( $params['project_title'] ) ? (string) $params['project_title'] : '' )
			&& 'he' === ( isset( $params['lang'] ) ? (string) $params['lang'] : '' )
			&& true === ( isset( $params['consent'] ) ? $params['consent'] : false )
			&& hash_equals( (string) $consent['version'], isset( $params['consent_version'] ) ? (string) $params['consent_version'] : '' )
			&& hash_equals( (string) $consent['text'], isset( $params['consent_text'] ) ? (string) $params['consent_text'] : '' )
			&& '' === trim( isset( $params['company'] ) ? (string) $params['company'] : '' );
		foreach ( $empty_inventory as $key ) {
			$valid = $valid && array_key_exists( $key, $params ) && '' === (string) $params[ $key ];
		}
		return $valid ? null : new WP_Error( 'invalid_einstein_inquiry', 'Request rejected.', array( 'status' => 400 ) );
	}
}
add_filter( 'rest_request_before_callbacks', 'nadlan_flagship_v3_guard_lead_request', 5, 3 );

if ( ! function_exists( 'nadlan_flagship_v3_record_lead_consent_version' ) ) {
	/** Add a queryable consent-version meta field when the shared route created a real lead post. */
	function nadlan_flagship_v3_record_lead_consent_version( $response, $handler, $request ) {
		unset( $handler );
		if ( ! nadlan_flagship_v3_is_lead_request( $request ) ) {
			return $response;
		}
		if ( is_wp_error( $response ) ) {
			return $response;
		}
		$rest_response = function_exists( 'rest_ensure_response' ) ? rest_ensure_response( $response ) : $response;
		if ( is_object( $rest_response ) && method_exists( $rest_response, 'get_status' ) && (int) $rest_response->get_status() >= 400 ) {
			return $response;
		}
		$data = is_object( $rest_response ) && method_exists( $rest_response, 'get_data' ) ? $rest_response->get_data() : array();
		if ( ! is_array( $data ) || true !== ( isset( $data['ok'] ) ? $data['ok'] : false ) ) {
			return $response;
		}
		$lead_id = (int) ( isset( $data['lead_id'] ) ? $data['lead_id'] : 0 );
		if ( $lead_id < 1 || 'nadlan_lead' !== get_post_type( $lead_id ) ) {
			return new WP_Error( 'einstein_inquiry_not_persisted', 'Request could not be verified.', array( 'status' => 500 ) );
		}
		$params = method_exists( $request, 'get_json_params' ) ? $request->get_json_params() : array();
		$consent = nadlan_flagship_v3_lead_consent_contract();
		update_post_meta( $lead_id, 'consent_version', (string) $consent['version'] );
		update_post_meta( $lead_id, 'source_url', home_url( '/projects/einstein-tower/' ) );
		update_post_meta( $lead_id, 'utm_source', 'showroom_unit_journey_v2' );
		update_post_meta( $lead_id, 'einstein_inquiry_contract', 'nadlan-einstein-project-inquiry/v1' );
		$persisted = 4867 === (int) get_post_meta( $lead_id, 'lead_card_id', true )
			&& 4867 === (int) get_post_meta( $lead_id, 'project_wp_id', true )
			&& 'einstein-tower' === (string) get_post_meta( $lead_id, 'project_slug', true )
			&& 'EINSTEIN TOWER תל אביב' === (string) get_post_meta( $lead_id, 'project_title', true )
			&& 'nadlan-einstein-project-inquiry/v1' === (string) get_post_meta( $lead_id, 'einstein_inquiry_contract', true )
			&& hash_equals( home_url( '/projects/einstein-tower/' ), (string) get_post_meta( $lead_id, 'source_url', true ) )
			&& 'showroom_unit_journey_v2' === (string) get_post_meta( $lead_id, 'utm_source', true )
			&& 1 === (int) get_post_meta( $lead_id, 'consent', true )
			&& '' !== (string) get_post_meta( $lead_id, 'consent_recorded', true )
			&& hash_equals( (string) $consent['text'], (string) get_post_meta( $lead_id, 'consent_text', true ) )
			&& hash_equals( (string) $consent['version'], (string) get_post_meta( $lead_id, 'consent_version', true ) )
			&& 'new' === (string) get_post_meta( $lead_id, 'lead_status', true )
			&& 1 === (int) get_post_meta( $lead_id, 'lead_e2e_enabled', true )
			&& 'rest' === (string) get_post_meta( $lead_id, 'lead_e2e_context', true )
			&& 1 === (int) get_post_meta( $lead_id, 'lead_route_attempted', true )
			&& (int) get_post_meta( $lead_id, 'lead_route_attempted_at', true ) > 0
			&& 'fallback_admin' === (string) get_post_meta( $lead_id, 'lead_route_status', true )
			&& 'unclaimed_card' === (string) get_post_meta( $lead_id, 'lead_route_reason', true )
			&& 1 === (int) get_post_meta( $lead_id, 'lead_e2e_fallback_admin', true )
			&& 'unclaimed_card' === (string) get_post_meta( $lead_id, 'lead_e2e_fallback_reason', true )
			&& (int) get_post_meta( $lead_id, 'lead_e2e_admin_notified_at', true ) > 0
			&& is_array( $params ) && hash_equals( home_url( '/projects/einstein-tower/' ), (string) ( isset( $params['source_url'] ) ? $params['source_url'] : '' ) );
		if ( ! $persisted ) {
			return new WP_Error( 'einstein_inquiry_contract_not_persisted', 'Request could not be verified.', array( 'status' => 500 ) );
		}
		$data['routing_state'] = 'site_admin_fallback';
		$data['delivery_state'] = 'admin_notified';
		if ( is_object( $rest_response ) && method_exists( $rest_response, 'set_data' ) ) {
			$rest_response->set_data( $data );
			return $rest_response;
		}
		return $response;
	}
}
add_filter( 'rest_request_after_callbacks', 'nadlan_flagship_v3_record_lead_consent_version', 20, 3 );

if ( ! function_exists( 'nadlan_flagship_v3_source_refs_html' ) ) {
	function nadlan_flagship_v3_source_refs_html( $source_ids, $instance ) {
		$links = array();
		foreach ( (array) $source_ids as $source_id ) {
			$links[] = '<a href="#' . esc_attr( $instance . '-source-' . sanitize_key( (string) $source_id ) ) . '">' . esc_html( (string) $source_id ) . '</a>';
		}
		return '<span class="nlfs__source-refs">' . implode( ' ', $links ) . '</span>';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_evidence_reference_ids_html' ) ) {
	/** Render evidence-ledger IDs as text unless a real in-page source target exists. */
	function nadlan_flagship_v3_evidence_reference_ids_html( $source_ids ) {
		$items = array();
		foreach ( (array) $source_ids as $source_id ) {
			$items[] = '<bdi data-nlfs-evidence-ref>' . esc_html( (string) $source_id ) . '</bdi>';
		}
		return '<span class="nlfs__source-refs" aria-label="מזהי אסמכתאות ביומן הראיות">' . implode( ' ', $items ) . '</span>';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_scene_evidence_html' ) ) {
	/** Render the same source/date/limitation lane for every visual decision item. */
	function nadlan_flagship_v3_scene_evidence_html( $scene, $decision, $instance ) {
		$refs = ! empty( $scene['placement_source_refs'] ) ? (array) $scene['placement_source_refs'] : (array) ( isset( $scene['source_ids'] ) ? $scene['source_ids'] : array() );
		$decision_id = isset( $scene['mapping_owner_decision_id'] ) ? (string) $scene['mapping_owner_decision_id'] : (string) ( isset( $decision['owner_decision_id'] ) ? $decision['owner_decision_id'] : '' );
		$effective_at = (string) ( isset( $decision['effective_at'] ) ? $decision['effective_at'] : '' );
		$limitation = (string) ( isset( $scene['placement_ambiguity'] ) ? $scene['placement_ambiguity'] : 'No verified unit, floor, bearing or exact facility coordinate is supplied.' );
		$basis = (string) ( isset( $scene['placement_basis'] ) ? $scene['placement_basis'] : 'Owner-approved illustrative media; not a verified unit or exact facility location.' );
		$zone = isset( $scene['placement_confidence']['zone'] ) ? (int) round( 100 * (float) $scene['placement_confidence']['zone'] ) : 0;
		$point = isset( $scene['placement_confidence']['exact_point'] ) ? (int) round( 100 * (float) $scene['placement_confidence']['exact_point'] ) : 0;
		$refs_html = empty( $refs ) ? '<span>לא סופק מקור מרחבי לפריט זה.</span>' : nadlan_flagship_v3_evidence_reference_ids_html( $refs );
		return '<details class="nlfs__evidence" data-nlfs-evidence-badge data-decision-grade="false"><summary>מקורות ומגבלות</summary><dl>'
			. '<div><dt>החלטה</dt><dd><bdi>' . esc_html( $decision_id ) . '</bdi></dd></div>'
			. '<div><dt>בתוקף מ־</dt><dd><bdi>' . esc_html( $effective_at ) . '</bdi></dd></div>'
			. '<div><dt>אסמכתאות</dt><dd>' . $refs_html . '</dd></div>'
			. '<div><dt>ביטחון מיפוי</dt><dd>אזור <bdi>' . esc_html( (string) $zone ) . '%</bdi> · נקודה מדויקת <bdi>' . esc_html( (string) $point ) . '%</bdi></dd></div>'
			. '<div><dt>בסיס</dt><dd lang="en">' . esc_html( $basis ) . '</dd></div>'
			. '<div><dt>מגבלה</dt><dd lang="en">' . esc_html( $limitation ) . '</dd></div>'
			. '</dl></details>';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_render_model_hotspots' ) ) {
	function nadlan_flagship_v3_render_model_hotspots( $experiences, $instance ) {
		$html  = '';
		$index = 0;
		$seen_groups = array();
		$decision = isset( $experiences['decision'] ) && is_array( $experiences['decision'] ) ? $experiences['decision'] : array();
		foreach ( $experiences['scenes'] as $scene ) {
			if ( empty( $scene['model_hotspot'] ) || ! is_array( $scene['model_hotspot'] ) ) {
				continue;
			}
			$group = isset( $scene['model_hotspot_group'] ) ? sanitize_key( (string) $scene['model_hotspot_group'] ) : '';
			if ( '' === $group || isset( $seen_groups[ $group ] ) ) {
				continue;
			}
			$seen_groups[ $group ] = true;
			++$index;
			$hotspot = $scene['model_hotspot'];
			$zone_confidence = isset( $scene['placement_confidence']['zone'] ) ? (int) round( 100 * (float) $scene['placement_confidence']['zone'] ) : 0;
			$point_confidence = isset( $scene['placement_confidence']['exact_point'] ) ? (int) round( 100 * (float) $scene['placement_confidence']['exact_point'] ) : 0;
			$disclosure_id = $instance . '-hotspot-disclosure-' . $group;
			$html    .= '<button type="button" class="nlfs__model-hotspot" slot="hotspot-' . esc_attr( $scene['id'] )
				. '" data-position="' . esc_attr( $hotspot['position'] ) . '" data-normal="' . esc_attr( $hotspot['normal'] )
				. '" data-nlfs-scene="' . esc_attr( $scene['id'] ) . '" data-nlfs-scene-group="' . esc_attr( $group )
				. '" data-nlfs-selection-mode="in-place" data-evidence-state="illustrative" data-decision-grade="false" aria-describedby="' . esc_attr( $disclosure_id )
				. '" aria-label="' . esc_attr( $scene['open_label'] . ': ' . $scene['title'] )
				. '" hidden disabled aria-disabled="true"><span aria-hidden="true">' . esc_html( (string) $index ) . '</span><small id="' . esc_attr( $disclosure_id )
				. '" class="nlfs__visually-hidden">המחשה מאושרת שאינה מיקום רשמי, כיוון דירה או ראיה תכנונית. החלטה ' . esc_html( (string) ( isset( $scene['mapping_owner_decision_id'] ) ? $scene['mapping_owner_decision_id'] : ( isset( $decision['owner_decision_id'] ) ? $decision['owner_decision_id'] : '' ) ) )
				. '; בתוקף מ־' . esc_html( (string) ( isset( $decision['effective_at'] ) ? $decision['effective_at'] : '' ) )
				. '; אסמכתאות ' . esc_html( implode( ', ', (array) ( isset( $scene['placement_source_refs'] ) ? $scene['placement_source_refs'] : array() ) ) )
				. '; ביטחון אזור ' . esc_html( (string) $zone_confidence ) . ' אחוז, נקודה מדויקת ' . esc_html( (string) $point_confidence ) . ' אחוז'
				. '; בסיס המיקום: ' . esc_html( (string) ( isset( $scene['placement_basis'] ) ? $scene['placement_basis'] : 'Owner-approved illustration; no verified spatial basis supplied.' ) )
				. '; מגבלה: ' . esc_html( (string) ( isset( $scene['placement_ambiguity'] ) ? $scene['placement_ambiguity'] : 'No verified location.' ) ) . '</small></button>';
		}
		return $html;
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_render_experiences' ) ) {
	function nadlan_flagship_v3_render_experiences( $experiences, $instance ) {
		$html = '<section class="nlfs__experiences" aria-labelledby="' . esc_attr( $instance . '-experiences' ) . '"><h2 id="'
			. esc_attr( $instance . '-experiences' ) . '">' . esc_html( $experiences['heading'] ) . '</h2><div class="nlfs__experience-grid">';
		$decision = isset( $experiences['decision'] ) && is_array( $experiences['decision'] ) ? $experiences['decision'] : array();
		foreach ( $experiences['scenes'] as $scene ) {
			$truth_label = 'facility' === (string) $scene['kind']
				? 'המחשת חלל משותף; השיוך לאזור במודל אינו מיקום רשמי.'
				: 'המחשת פנים מייצגת; אינה תכנית או דירה מסוימת.';
			$html .= '<article class="nlfs__experience-card" data-experience-kind="' . esc_attr( $scene['kind'] ) . '" data-evidence-state="illustrative" data-decision-grade="false"><div class="nlfs__experience-preview">'
				. '<img src="' . esc_url( $scene['preview_url'] ) . '" alt="' . esc_attr( $scene['title'] ) . '" loading="lazy" decoding="async"></div>'
				. '<div class="nlfs__experience-copy"><h3>' . esc_html( $scene['title'] ) . '</h3><p class="nlfs__experience-truth">' . esc_html( $truth_label ) . '</p><p>' . esc_html( $scene['summary'] ) . '</p>';
			$html .= nadlan_flagship_v3_scene_evidence_html( $scene, $decision, $instance );
			$html .= '<button type="button" data-nlfs-scene="' . esc_attr( $scene['id'] ) . '">' . esc_html( $scene['open_label'] ) . '</button></div></article>';
		}
		return $html . '</div></section>';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_render_media_dock' ) ) {
	/** One state-persistent, section-local switcher keeps linked media in one decision context. */
	function nadlan_flagship_v3_render_media_dock( $experiences, $instance ) {
		$html = '<nav class="nlfs__media-dock" data-nlfs-media-dock aria-label="מעבר בין חומרי ההחלטה"><strong>חומרי החלטה</strong><div>'
			. '<button type="button" data-nlfs-media-target="model">מודל</button>'
			. '<button type="button" data-nlfs-media-target="view">מבט לוויין</button>';
		foreach ( (array) $experiences['scenes'] as $scene ) {
			$html .= '<button type="button" data-nlfs-media-target="scene" data-nlfs-media-scene="' . esc_attr( (string) $scene['id'] ) . '">' . esc_html( (string) $scene['title'] ) . '</button>';
		}
		return $html . '<a href="#' . esc_attr( $instance . '-article-path' ) . '">הסקירה והמקורות</a></div><p>כל מעבר שומר את המודל והמפה כהקשר; סימון המחשה אינו הוכחת מיקום, כיוון או מלאי.</p></nav>';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_render_buyer_decision' ) ) {
	function nadlan_flagship_v3_render_buyer_decision( $buyer, $instance ) {
		$labels = $buyer['labels'];
		$html   = '<div class="nlfs__decision" data-nlfs-decision-contract>';
		$html  .= '<section class="nlfs__facts" aria-labelledby="' . esc_attr( $instance . '-facts' ) . '"><h2 id="' . esc_attr( $instance . '-facts' ) . '">' . esc_html( $labels['facts'] ) . '</h2><div class="nlfs__fact-grid">';
		foreach ( $buyer['facts'] as $fact ) {
			$html .= '<article data-truth-state="' . esc_attr( $fact['truth_state'] ) . '"><span>' . esc_html( $fact['label'] ) . '</span><strong><bdi>' . esc_html( $fact['value'] ) . '</bdi></strong>'
				. nadlan_flagship_v3_source_refs_html( $fact['source_ids'], $instance ) . '</article>';
		}
		$html .= '</div></section>';

		$html .= '<section class="nlfs__context" aria-labelledby="' . esc_attr( $instance . '-context' ) . '"><h2 id="' . esc_attr( $instance . '-context' ) . '">' . esc_html( $labels['context'] ) . '</h2><p>' . esc_html( $buyer['context_map']['title'] ) . '</p><div class="nlfs__context-layers">';
		foreach ( $buyer['context_map']['layers'] as $layer ) {
			$html .= '<article data-context-layer="' . esc_attr( $layer['id'] ) . '"><header><span aria-hidden="true"></span><h3>' . esc_html( $layer['label'] ) . '</h3></header><ul>';
			foreach ( $layer['items'] as $item ) {
				$html .= '<li data-context-state="' . esc_attr( $item['state'] ) . '"><strong>' . esc_html( $item['label'] ) . '</strong><p>' . esc_html( $item['summary'] ) . '</p>'
					. nadlan_flagship_v3_source_refs_html( $item['source_ids'], $instance ) . '</li>';
			}
			$html .= '</ul></article>';
		}
		$html .= '</div></section>';

		$html .= '<div class="nlfs__decision-grid">';
		$html .= '<section aria-labelledby="' . esc_attr( $instance . '-sea' ) . '"><h2 id="' . esc_attr( $instance . '-sea' ) . '">' . esc_html( $labels['sea'] ) . '</h2><strong>' . esc_html( $buyer['sea']['label'] ) . ': <bdi>' . esc_html( (string) $buyer['sea']['distance_m'] ) . ' מ׳</bdi></strong><p>' . esc_html( $buyer['sea']['method_label'] ) . '</p>' . nadlan_flagship_v3_source_refs_html( $buyer['sea']['source_ids'], $instance ) . '</section>';

		$html .= '<section aria-labelledby="' . esc_attr( $instance . '-education' ) . '"><h2 id="' . esc_attr( $instance . '-education' ) . '">' . esc_html( $labels['education'] ) . '</h2><p>' . esc_html( $buyer['education']['snapshot_label'] ) . ' · <bdi>' . esc_html( $buyer['education']['school_year'] ) . '</bdi></p><ul>';
		foreach ( array_merge( $buyer['education']['schools'], $buyer['education']['kindergartens'] ) as $place ) {
			$html .= '<li><strong>' . esc_html( $place['name'] ) . '</strong> · <bdi>' . esc_html( (string) $place['distance_m'] ) . ' מ׳</bdi><small>' . esc_html( $place['method'] ) . '</small>' . nadlan_flagship_v3_source_refs_html( $place['source_ids'], $instance ) . '</li>';
		}
		$html .= '</ul></section>';

		$html .= '<section aria-labelledby="' . esc_attr( $instance . '-transit' ) . '"><h2 id="' . esc_attr( $instance . '-transit' ) . '">' . esc_html( $labels['transit'] ) . '</h2><strong>' . esc_html( $buyer['transit']['line_label'] ) . '</strong><h3>' . esc_html( $labels['current'] ) . '</h3><p>' . esc_html( $buyer['transit']['current_works']['summary'] ) . '</p>' . nadlan_flagship_v3_source_refs_html( $buyer['transit']['current_works']['source_ids'], $instance ) . '<h3>' . esc_html( $labels['future'] ) . '</h3><p>' . esc_html( $buyer['transit']['planned_service']['summary'] ) . '</p>' . nadlan_flagship_v3_source_refs_html( $buyer['transit']['planned_service']['source_ids'], $instance ) . '</section>';

		$html .= '<section aria-labelledby="' . esc_attr( $instance . '-construction' ) . '"><h2 id="' . esc_attr( $instance . '-construction' ) . '">' . esc_html( $labels['construction'] ) . '</h2>';
		foreach ( array( 'current_state', 'future_context', 'unit_view_state' ) as $key ) {
			$row = $buyer['construction_and_views'][ $key ];
			$html .= '<h3>' . esc_html( $row['label'] ) . '</h3><p>' . esc_html( $row['summary'] ) . '</p>' . nadlan_flagship_v3_source_refs_html( $row['source_ids'], $instance );
		}
		$html .= '</section></div>';

		$overseas_id = $instance . '-overseas-buyer';
		$html .= '<section id="' . esc_attr( $overseas_id ) . '" class="nlfs__overseas" aria-labelledby="' . esc_attr( $overseas_id . '-title' ) . '"><h2 id="' . esc_attr( $overseas_id . '-title' ) . '">' . esc_html( $buyer['overseas_buyer']['title'] ) . '</h2><div class="nlfs__purchase-structure"><strong>' . esc_html( $buyer['overseas_buyer']['purchase_structure']['label'] ) . '</strong><p>' . esc_html( $buyer['overseas_buyer']['purchase_structure']['summary'] ) . '</p>' . nadlan_flagship_v3_source_refs_html( $buyer['overseas_buyer']['purchase_structure']['source_ids'], $instance ) . '</div><ol>';
		foreach ( $buyer['overseas_buyer']['steps'] as $step ) {
			$html .= '<li><strong>' . esc_html( $step['title'] ) . '</strong><p>' . esc_html( $step['summary'] ) . '</p>' . nadlan_flagship_v3_source_refs_html( $step['source_ids'], $instance ) . '</li>';
		}
		$html .= '</ol></section>';

		$target_id = 'overseas-buyer' === $buyer['primary_action']['target_section'] ? $overseas_id : $instance . '-sources';
		$html .= '<a class="nlfs__primary-action" href="#' . esc_attr( $target_id ) . '">' . esc_html( $buyer['primary_action']['label'] ) . '</a>';

		$html .= '<section id="' . esc_attr( $instance . '-sources' ) . '" class="nlfs__sources" aria-labelledby="' . esc_attr( $instance . '-sources-title' ) . '"><h2 id="' . esc_attr( $instance . '-sources-title' ) . '">' . esc_html( $labels['sources'] ) . '</h2><ol>';
		foreach ( $buyer['sources'] as $source ) {
			$html .= '<li id="' . esc_attr( $instance . '-source-' . sanitize_key( (string) $source['id'] ) ) . '"><a href="' . esc_url( $source['url'] ) . '" target="_blank" rel="noopener noreferrer">' . esc_html( $source['id'] . ' · ' . $source['label'] ) . '</a><small><bdi>' . esc_html( $source['effective_at'] ) . '</bdi></small></li>';
		}
		$html .= '</ol></section></div>';
		return $html;
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_safe_article_html' ) ) {
	/**
	 * Accept the already-rendered staged dossier from the shared composer.
	 * It must be marker-bound, H1/main/showroom-free and scriptless. Shortcodes
	 * are never evaluated here, preventing recursion into the content pipeline.
	 */
	function nadlan_flagship_v3_safe_article_html( $html, $contract ) {
		$html   = is_string( $html ) ? str_replace( array( "\r\n", "\r" ), "\n", $html ) : '';
		$marker = isset( $contract['required_article_marker'] ) ? sanitize_key( (string) $contract['required_article_marker'] ) : '';
		$article_sha256 = isset( $contract['required_article_lf_sha256'] ) ? strtolower( (string) $contract['required_article_lf_sha256'] ) : '';
		if ( '' === $html || '' === $marker || strlen( $html ) > 524288
			|| ! preg_match( '/^[a-f0-9]{64}$/D', $article_sha256 )
			|| ! hash_equals( $article_sha256, hash( 'sha256', $html ) )
			|| false === strpos( $html, 'data-nlfs-dossier="' . $marker . '"' )
			|| 1 !== substr_count( $html, 'data-nlfs-dossier="' . $marker . '"' )
			|| preg_match( '#<(?:h1|main|script|style|iframe|object|embed|form)\b#i', $html )
			|| preg_match( '#\son[a-z]+\s*=#i', $html )
			|| preg_match( '#\b(?:javascript|data):#i', $html )
			|| false !== stripos( $html, 'data-nl-flagship=' )
			|| false !== stripos( $html, 'olp' )
			|| false !== stripos( $html, 'id="nl-root"' ) ) {
			return '';
		}
		if ( preg_match_all( '#\ssrc\s*=\s*(["\'])(.*?)\1#i', $html, $source_matches ) ) {
			$home = wp_parse_url( home_url( '/' ) );
			foreach ( $source_matches[2] as $source_url ) {
				$parts = wp_parse_url( html_entity_decode( (string) $source_url, ENT_QUOTES | ENT_HTML5, 'UTF-8' ) );
				if ( ! is_array( $parts ) || ! isset( $parts['host'], $parts['scheme'] ) || ! is_array( $home ) || empty( $home['host'] )
					|| 'https' !== strtolower( (string) $parts['scheme'] )
					|| strtolower( (string) $parts['host'] ) !== strtolower( (string) $home['host'] )
					|| isset( $parts['user'] ) || isset( $parts['pass'] ) || isset( $parts['fragment'] ) ) {
					return '';
				}
			}
		}
		// The complete LF-normalized dossier is registry-pinned above; returning it
		// unchanged preserves every original TOC target, source marker and byte.
		return $html;
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_article_parts' ) ) {
	/**
	 * Move the byte-pinned editorial lede into the decision-first opening without
	 * changing post_content. The remaining article wrapper and every source/TOC
	 * node are rendered once, later in the declared page order.
	 */
	function nadlan_flagship_v3_article_parts( $article_html ) {
		$article_html = (string) $article_html;
		$pattern = '#\s*<header class="nlfs-article__header">\s*(<p class="nlfs-eyebrow">.*?</p>)\s*(<p class="nlfs-lede">.*?</p>)\s*</header>\s*#s';
		if ( 1 !== substr_count( $article_html, 'class="nlfs-article__header"' )
			|| 1 !== substr_count( $article_html, 'class="nlfs-lede"' )
			|| 1 !== preg_match( $pattern, $article_html, $matches ) ) {
			return array();
		}
		$count = 0;
		$remainder = preg_replace( $pattern, '', $article_html, 1, $count );
		if ( 1 !== $count || ! is_string( $remainder )
			|| false !== strpos( $remainder, 'class="nlfs-lede"' )
			|| 1 !== substr_count( $remainder, 'data-nlfs-dossier=' ) ) {
			return array();
		}
		return array(
			'lead'      => $matches[1] . $matches[2],
			'remainder' => $remainder,
		);
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_render_independence_notice' ) ) {
	/** Render the fleet legal wording once, directly under the approved lede. */
	function nadlan_flagship_v3_render_independence_notice( $post_id, $instance ) {
		$strings = function_exists( 'nadlan_project_notice_strings' )
			? nadlan_project_notice_strings( 'he' )
			: array(
				'אתר עצמאי',
				'עמוד זה אינו האתר הרשמי של %s ואינו מופעל מטעמה. נדל״ן היא פלטפורמת מידע עצמאית, ללא קשר מסחרי עם היזם. הפרטים נאספו ממקורות גלויים ויש לאמת אותם מול היזם.',
				'עמוד זה אינו אתר רשמי של היזם ואינו מופעל מטעמו. נדל״ן היא פלטפורמת מידע עצמאית. הפרטים נאספו ממקורות גלויים ויש לאמת אותם מול היזם.',
			);
		$developer = trim( (string) get_post_meta( (int) $post_id, 'developer_name', true ) );
		$text = '' !== $developer ? sprintf( (string) $strings[1], $developer ) : (string) $strings[2];
		return '<aside id="' . esc_attr( $instance . '-non-affiliation' ) . '" class="nlfs__independence" data-nlfs-page-slot="non_affiliation_notice" role="note">'
			. '<strong>' . esc_html( (string) $strings[0] ) . '</strong><span>' . esc_html( $text ) . '</span></aside>';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_render_primary_actions' ) ) {
	/** Existing fleet controls are adopted by JS only after an exact target check. */
	function nadlan_flagship_v3_render_primary_actions( $decision, $instance ) {
		$actions = isset( $decision['primary_actions'] ) && is_array( $decision['primary_actions'] ) ? $decision['primary_actions'] : array();
		$interest = isset( $actions['interest'] ) && is_array( $actions['interest'] ) ? $actions['interest'] : array();
		$whatsapp = isset( $actions['whatsapp'] ) && is_array( $actions['whatsapp'] ) ? $actions['whatsapp'] : array();
		return '<section id="' . esc_attr( $instance . '-primary-actions' ) . '" class="nlfs__cta-band" data-nlfs-page-slot="primary_actions" aria-labelledby="' . esc_attr( $instance . '-primary-actions-title' ) . '">'
			. '<div><h2 id="' . esc_attr( $instance . '-primary-actions-title' ) . '">רוצים לבדוק את הפרויקט לעומק?</h2><p>אפשר לפתוח פנייה או לעבור לשיחה, בלי לבחור דירה שאינה קיימת במלאי מאומת.</p></div>'
			. '<div class="nlfs__cta-band-buttons">'
			. '<button type="button" data-nlfs-primary-action="interest" data-nlfs-adopt-target="' . esc_attr( isset( $interest['target'] ) ? (string) $interest['target'] : '' ) . '" disabled aria-disabled="true">מעניין אותי</button>'
			. '<button type="button" data-nlfs-primary-action="whatsapp" data-nlfs-adopt-selector="' . esc_attr( isset( $whatsapp['selector'] ) ? (string) $whatsapp['selector'] : '' ) . '" disabled aria-disabled="true">WhatsApp</button>'
			. '</div><p class="nlfs__cta-band-status" data-nlfs-primary-actions-status role="status" aria-live="polite">הפעולות יופעלו לאחר אימות בקרי הקשר הקיימים בעמוד.</p></section>';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_render_capability_slots' ) ) {
	/**
	 * Ready capabilities receive inert mount slots; data-gated capabilities are
	 * disclosed as text, never rendered as dimmed or clickable dead controls.
	 */
	function nadlan_flagship_v3_render_capability_slots( $decision, $instance ) {
		$capabilities = isset( $decision['capabilities'] ) && is_array( $decision['capabilities'] ) ? $decision['capabilities'] : array();
		$labels = array(
			'project_model' => 'מודל הפרויקט',
			'attached_area_map' => 'מפת הסביבה הצמודה',
			'project_window_view' => 'מבט חלון ברמת הפרויקט',
			'governed_scene_gallery' => 'גלריית המחשות מפוקחת',
			'designer_link' => 'מעצב חלל',
			'district_tour' => 'סיור בשכונה',
			'adjacent_district_earth' => 'סצנת Earth סמוכה',
			'tutorial_film' => 'סרט הדרכה',
			'project_inquiry' => 'פניית פרויקט',
			'project_share' => 'שיתוף פרויקט',
			'unit_inventory' => 'מלאי דירות',
			'unit_favorites' => 'מועדפים לדירות',
			'unit_compare' => 'השוואת דירות',
			'per_unit_window_view' => 'מבט חלון לדירה',
			'floor_bands' => 'טווחי קומות',
			'sun_simulation' => 'הדמיית שמש',
			'co_tour' => 'סיור מרחבי מסונכרן',
		);
		$reasons = array(
			'requires_verified_data' => 'יופעל רק עם נתוני יחידה ומלאי מאומתים.',
			'requires_calibrated_orientation_and_geometry' => 'יופעל רק לאחר כיול כיוון וגאומטריה מתאים להחלטה.',
			'requires_adapter_verification' => 'יופעל רק לאחר אימות מתאם מצב מקצה לקצה.',
		);
		$slots = '';
		$unavailable = '';
		foreach ( $capabilities as $capability => $state ) {
			$label = isset( $labels[ $capability ] ) ? $labels[ $capability ] : str_replace( '_', ' ', (string) $capability );
			$slots .= '<span hidden data-nlfs-capability-slot="' . esc_attr( (string) $capability ) . '" data-capability-state="' . esc_attr( (string) $state ) . '">' . esc_html( $label ) . '</span>';
			if ( isset( $reasons[ $state ] ) ) {
				$unavailable .= '<li data-nlfs-capability="' . esc_attr( (string) $capability ) . '"><strong>' . esc_html( $label ) . '</strong><span>' . esc_html( $reasons[ $state ] ) . '</span></li>';
			}
		}
		$html = '<div class="nlfs__capability-slots" data-nlfs-capability-slots data-state-graph="' . esc_attr( isset( $decision['state_graph']['schema'] ) ? (string) $decision['state_graph']['schema'] : '' ) . '" hidden>' . $slots . '</div>';
		if ( '' !== $unavailable ) {
			$html .= '<details class="nlfs__capability-disclosure"><summary>מה ייפתח רק עם נתונים מאומתים</summary><ul>' . $unavailable . '</ul></details>';
		}
		return $html;
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_render_tutorial_film' ) ) {
	/** Resolve the governed tutorial by attachment identity, MIME and exact path. */
	function nadlan_flagship_v3_render_tutorial_film( $decision, $instance ) {
		$film = isset( $decision['tutorial_film'] ) && is_array( $decision['tutorial_film'] ) ? $decision['tutorial_film'] : array();
		$attachment_id = isset( $film['attachment_id'] ) ? (int) $film['attachment_id'] : 0;
		$url = $attachment_id > 0 && function_exists( 'wp_get_attachment_url' ) ? wp_get_attachment_url( $attachment_id ) : false;
		$attachment = $attachment_id > 0 ? get_post( $attachment_id ) : null;
		$mime = function_exists( 'get_post_mime_type' ) ? (string) get_post_mime_type( $attachment_id ) : ( is_object( $attachment ) && isset( $attachment->post_mime_type ) ? (string) $attachment->post_mime_type : '' );
		$parts = is_string( $url ) && '' !== $url ? wp_parse_url( $url ) : array();
		$home = wp_parse_url( home_url( '/' ) );
		$path = is_array( $parts ) && isset( $parts['path'] ) ? rawurldecode( (string) $parts['path'] ) : '';
		$home_port = is_array( $home ) && isset( $home['port'] ) ? (int) $home['port'] : 443;
		$url_port = is_array( $parts ) && isset( $parts['port'] ) ? (int) $parts['port'] : 443;
		$metadata = function_exists( 'wp_get_attachment_metadata' ) ? wp_get_attachment_metadata( $attachment_id ) : array();
		$metadata_matches = ! is_array( $metadata )
			|| ( ( ! isset( $metadata['width'] ) || (int) $metadata['width'] === (int) $film['width'] )
				&& ( ! isset( $metadata['height'] ) || (int) $metadata['height'] === (int) $film['height'] )
				&& ( ! isset( $metadata['length'] ) || abs( (float) $metadata['length'] - (float) $film['duration_seconds'] ) <= 1.0 ) );
		$ready = $attachment instanceof WP_Post
			&& 'attachment' === ( isset( $attachment->post_type ) ? (string) $attachment->post_type : '' )
			&& in_array( isset( $attachment->post_status ) ? (string) $attachment->post_status : '', array( 'inherit', 'publish' ), true )
			&& (string) ( isset( $film['expected_mime'] ) ? $film['expected_mime'] : '' ) === $mime
			&& is_array( $parts ) && is_array( $home )
			&& 'https' === strtolower( isset( $parts['scheme'] ) ? (string) $parts['scheme'] : '' )
			&& ! empty( $parts['host'] ) && ! empty( $home['host'] )
			&& strtolower( (string) $parts['host'] ) === strtolower( (string) $home['host'] )
			&& $home_port === $url_port
			&& ! isset( $parts['user'] ) && ! isset( $parts['pass'] ) && ! isset( $parts['query'] ) && ! isset( $parts['fragment'] )
			&& hash_equals( (string) ( isset( $film['expected_path'] ) ? $film['expected_path'] : '' ), $path )
			&& $metadata_matches;
		$heading_id = $instance . '-tutorial-title';
		if ( ! $ready ) {
			return '<section id="' . esc_attr( $instance . '-tutorial' ) . '" class="nlfs__tutorial nlfs__tutorial--unavailable" data-nlfs-page-slot="tutorial_film" data-capability-state="honest_unavailable" aria-labelledby="' . esc_attr( $heading_id ) . '"><h2 id="' . esc_attr( $heading_id ) . '">איך משתמשים בחוויית הפרויקט</h2><p>סרט ההדרכה אינו זמין כרגע לאחר בדיקת קובץ המקור. שאר כלי ההחלטה נשארים זמינים.</p></section>';
		}
		$caption_id = $instance . '-tutorial-caption';
		$summary_items = '';
		foreach ( $film['companion_summary'] as $summary_item ) {
			$summary_items .= '<li>' . esc_html( (string) $summary_item ) . '</li>';
		}
		return '<section id="' . esc_attr( $instance . '-tutorial' ) . '" class="nlfs__tutorial" data-nlfs-page-slot="tutorial_film" data-attachment-id="' . esc_attr( (string) $attachment_id ) . '" aria-labelledby="' . esc_attr( $heading_id ) . '">'
			. '<div class="nlfs__tutorial-copy"><span><bdi>' . esc_html( (string) (int) $film['duration_seconds'] ) . '</bdi> שניות של הדגמה חזותית</span><h2 id="' . esc_attr( $heading_id ) . '">איך חוויית החלטה מרחבית יכולה לעבוד</h2><p>זהו סרט קונספט שקט של מוצר NadLan, לא צילום של מלאי איינשטיין ולא הבטחה שכל יכולת שמופיעה בו זמינה בפרויקט. סטטוס היכולות המדויק מופיע בכלי ההחלטה בעמוד.</p></div>'
			. '<video controls preload="metadata" playsinline muted width="' . esc_attr( (string) (int) $film['width'] ) . '" height="' . esc_attr( (string) (int) $film['height'] ) . '" data-audio-state="silent-no-audio-track" aria-describedby="' . esc_attr( $caption_id ) . '"><source src="' . esc_url( $url ) . '" type="' . esc_attr( $mime ) . '">הדפדפן אינו תומך בווידאו HTML5.</video>'
			. '<div id="' . esc_attr( $caption_id ) . '" class="nlfs__tutorial-caption"><p>לקובץ המקור אין ערוץ שמע, ולכן אין כתוביות שמע. תיאור טקסטואלי מקביל:</p><ol>' . $summary_items . '</ol></div></section>';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_render_inquiry' ) ) {
	function nadlan_flagship_v3_render_inquiry( $config, $instance ) {
		$lead = isset( $config['integrations']['lead'] ) && is_array( $config['integrations']['lead'] ) ? $config['integrations']['lead'] : array();
		if ( empty( $lead['endpoint'] ) || empty( $lead['consent_text'] ) || empty( $lead['rights_url'] ) ) {
			return '';
		}
		$rights = ! empty( $lead['rights_url'] ) ? '<a href="' . esc_url( $lead['rights_url'] ) . '">יצירת קשר לבקשת תיקון או מחיקה</a>' : '';
		return '<section id="' . esc_attr( $instance . '-inquiry' ) . '" class="nlfs__inquiry" aria-labelledby="' . esc_attr( $instance . '-inquiry-title' ) . '">'
			. '<div><h2 id="' . esc_attr( $instance . '-inquiry-title' ) . '">לקבלת מסמכים ומידע מאומת</h2><p>השאירו פרטים בלי לבחור דירה: אין כרגע מלאי דירות מאומת במערכת.</p></div>'
			. '<form id="nl-form" method="post" action="' . esc_url( $lead['source_url'] ) . '" data-nlfs-inquiry data-routing-state="' . esc_attr( $lead['routing_state'] ) . '" data-success-state="' . esc_attr( $lead['success_state'] ) . '" aria-describedby="' . esc_attr( $instance . '-inquiry-status' ) . '"><label>שם מלא<input data-nlfs-lead-field name="name" autocomplete="name" minlength="2" maxlength="120" required disabled></label>'
			. '<label>טלפון<input data-nlfs-lead-field name="phone" inputmode="tel" autocomplete="tel" maxlength="40" disabled></label><label>אימייל<input data-nlfs-lead-field name="email" type="email" inputmode="email" autocomplete="email" disabled></label>'
			. '<label class="nlfs__honeypot" aria-hidden="true">חברה<input data-nlfs-lead-field name="company" autocomplete="off" tabindex="-1" disabled></label>'
			. '<label class="nlfs__message">מה תרצו לבדוק?<textarea data-nlfs-lead-field name="message" rows="4" maxlength="4000" disabled></textarea></label>'
			. '<p class="nlfs__inquiry-context" data-nlfs-inquiry-context data-context-state="project">הפנייה מתייחסת לפרויקט כולו. בחירה המחשתית תצורף כהקשר בלבד, בלי דירה, קומה, כיוון או מיקום מומצאים.</p>'
			. '<p class="nlfs__inquiry-governance">בקר המידע: nad-lan.co.il. מטרת העיבוד: טיפול בפניית פרויקט. הפרטים נבחנים ידנית ונשמרים עד השלמת הטיפול או בקשת מחיקה; אין מחיקה אוטומטית מוגדרת. במצב הנוכחי הפנייה מנותבת למנהל האתר; אין הבטחה להעברה ליזם או ליועץ.</p>'
			. '<label class="nlfs__consent"><input data-nlfs-lead-field name="consent" type="checkbox" value="1" required disabled><span>' . esc_html( $lead['consent_text'] ) . '</span></label>'
			. $rights . '<button type="submit" disabled aria-disabled="true">שליחת פנייה</button><p id="' . esc_attr( $instance . '-inquiry-status' ) . '" data-nlfs-inquiry-status data-state="unavailable" role="status" aria-live="polite">הטופס יופעל רק לאחר טעינת החיבור המאובטח. אם הוא אינו מופעל, אפשר להשתמש בקישור יצירת הקשר בלי להזין כאן פרטים.</p></form></section>';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_render_cotour' ) ) {
	/** A spatial-state room, deliberately not described as video conferencing. */
	function nadlan_flagship_v3_render_cotour( $config, $instance ) {
		$contract = isset( $config['integrations']['co_tour'] ) && is_array( $config['integrations']['co_tour'] )
			? $config['integrations']['co_tour']
			: array();
		if ( true !== ( isset( $contract['enabled'] ) ? $contract['enabled'] : false ) ) {
			return '<section class="nlfs__cotour nlfs__cotour--unavailable" data-capability-state="honest_unavailable"><h3>סיור מרחבי מסונכרן</h3><p>החיבור המרחבי אינו זמין עד שחוזה החדר והאבטחה מאומת.</p></section>';
		}
		return '<section id="' . esc_attr( $instance . '-cotour' ) . '" class="nlfs__cotour" data-nlfs-cotour data-capability-state="ready" aria-labelledby="' . esc_attr( $instance . '-cotour-title' ) . '">'
			. '<header><span>אותו מודל, אותו רגע</span><h3 id="' . esc_attr( $instance . '-cotour-title' ) . '">סיור מרחבי מסונכרן</h3><p>מארח אחד ועוקב אחד רואים את אותה בחירה, מפה וכלי פעיל — ורק אחרי הסכמה מפורשת של העוקב.</p></header>'
			. '<div class="nlfs__cotour-idle" data-nlfs-cotour-idle><button type="button" data-nlfs-cotour-start>פתיחת חדר מרחבי</button><div class="nlfs__cotour-join"><label for="' . esc_attr( $instance . '-cotour-code' ) . '">קוד חדר ידני</label><input id="' . esc_attr( $instance . '-cotour-code' ) . '" data-nlfs-cotour-room-input type="text" dir="ltr" inputmode="text" autocomplete="off" autocapitalize="characters" spellcheck="false" maxlength="17" aria-describedby="' . esc_attr( $instance . '-cotour-code-help' ) . '"><button type="button" data-nlfs-cotour-join disabled aria-disabled="true">הצטרפות</button></div><label class="nlfs__cotour-consent"><input type="checkbox" data-nlfs-cotour-consent><span>אני מסכים/ה להופיע כעוקב היחיד בחדר ולקבל את מצב המודל, המפה והכלי הפעיל של המארח. אין כאן קול, וידאו, צ׳אט או הקלטה.</span></label><p id="' . esc_attr( $instance . '-cotour-code-help' ) . '">הקוד הוא מזהה ידני בלבד. הרשאת החדר נשמרת בעוגייה מוגנת שאינה נגישה לקוד העמוד.</p></div>'
			. '<div class="nlfs__cotour-active" data-nlfs-cotour-active hidden><dl><div><dt>חדר</dt><dd><output data-nlfs-cotour-room-output dir="ltr"></output></dd></div><div><dt>תפקיד</dt><dd data-nlfs-cotour-role></dd></div><div><dt>נוכחות</dt><dd><output data-nlfs-cotour-presence>0 מתוך 2</output></dd></div></dl><div class="nlfs__cotour-actions"><button type="button" data-nlfs-cotour-follow hidden>השהיית מעקב</button><button type="button" data-nlfs-cotour-reconnect hidden>חיבור מחדש</button><button type="button" data-nlfs-cotour-end>סיום החדר</button></div></div>'
			. '<p class="nlfs__cotour-status" data-nlfs-cotour-status role="status" aria-live="polite">בודקים את חוזה החיבור.</p><p class="nlfs__cotour-privacy">מסונכרן רק מצב מרחבי קצר־חיים ובקיבולת של מארח אחד ועוקב אחד. אין שיחת וידאו, קול, צ׳אט, הקלטה, פרטים אישיים או מלאי מומצא.</p></section>';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_render_for' ) ) {
	/** Render one isolated page. Any contract/article error returns no payload. */
	function nadlan_flagship_v3_render_for( $post_id, $rendered_article = '' ) {
		$post_id = (int) $post_id;
		if ( ! nadlan_flagship_v3_is_selected( $post_id ) || post_password_required( $post_id ) ) {
			return '';
		}
		$validated = nadlan_flagship_v3_validate_post( $post_id );
		if ( is_wp_error( $validated ) ) {
			return '';
		}
		$decision = nadlan_flagship_v3_decision_experience_contract( $validated['contract'] );
		$config = nadlan_flagship_v3_runtime_config( $validated );
		$article_html = nadlan_flagship_v3_safe_article_html( $rendered_article, $validated['contract'] );
		$article_parts = nadlan_flagship_v3_article_parts( $article_html );
		if ( empty( $decision ) || empty( $config['decision_experience'] ) || '' === $article_html
			|| empty( $article_parts['lead'] ) || empty( $article_parts['remainder'] )
			|| false !== strpos( $article_html, $config['copy']['demo_label'] ) ) {
			return '';
		}
		nadlan_flagship_v3_enqueue();
		$runtime_config = $config;
		unset( $runtime_config['copy']['demo_label'] );
		$json = wp_json_encode( $runtime_config, JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
		if ( ! is_string( $json ) || '' === $json ) {
			return '';
		}
		$copy       = $config['copy'];
		$assets     = $config['model'];
		$instance   = 'nlfs-' . $post_id;
		$model_alt  = $copy['model_label'] . ': ' . $config['identity']['representation_name'];
		$public_marker = 'canonical' === (string) $validated['mode'] ? (string) ( isset( $validated['contract']['public_body_marker'] ) ? $validated['contract']['public_body_marker'] : '' ) : '';
		$deployment_id = 'canonical' === (string) $validated['mode'] ? (string) get_post_meta( $post_id, '_nadlan_flagship_deployment_id', true ) : '';
		$public_attributes = '';
		if ( '' !== $public_marker && preg_match( '/^einstein-flagship-public-[0-9.]+$/', $public_marker )
			&& preg_match( '/^einstein-public-[0-9]{8}T[0-9]{6}Z-[a-f0-9]{6,16}$/', $deployment_id )
			&& hash_equals( $public_marker, (string) get_post_meta( $post_id, '_nadlan_flagship_body_marker', true ) ) ) {
			$public_attributes = ' data-nadlan-public-release="' . esc_attr( $public_marker ) . '" data-nadlan-deployment-id="' . esc_attr( $deployment_id ) . '"';
		}
		if ( 'canonical' === (string) $validated['mode'] && '' === $public_attributes ) {
			return '';
		}
		return '<div id="' . esc_attr( $instance ) . '" class="nlfs" data-nl-flagship="v3" data-project-contract-id="'
			. esc_attr( $config['identity']['project_contract_id'] ) . '" data-inventory-state="' . esc_attr( $config['inventory']['state'] )
			. '" data-decision-grade="false" data-decision-experience="' . esc_attr( (string) $decision['schema'] )
			. '" data-decision-owner-id="' . esc_attr( (string) $decision['owner_decision_id'] )
			. '" data-page-order="' . esc_attr( implode( ' ', $decision['page_order'] ) )
			. '" data-facility-cone-policy="verified-bearing-only" data-facility-map-pan-policy="verified-coordinates-only"'
			. $public_attributes . ' dir="' . esc_attr( $config['direction'] ) . '" lang="' . esc_attr( $config['locale'] ) . '">'
			. '<header class="nlfs__page-heading"><h1>' . esc_html( $config['identity']['representation_name'] ) . '</h1></header>'
			. '<section id="' . esc_attr( $instance . '-approved-lead' ) . '" class="nlfs__lead" data-nlfs-page-slot="approved_lead" aria-label="פתיח הפרויקט">' . $article_parts['lead'] . '</section>'
			. nadlan_flagship_v3_render_independence_notice( $post_id, $instance )
			. '<div id="' . esc_attr( $instance . '-decision-room' ) . '" class="nlfs__decision-hero" data-nlfs-decision-hero tabindex="-1">'
			. '<section class="nlfs__showroom" data-nlfs-page-slot="project_model" aria-labelledby="' . esc_attr( $instance . '-showroom-title' ) . '">'
			. '<header class="nlfs__heading"><h2 id="' . esc_attr( $instance . '-showroom-title' ) . '">' . esc_html( $copy['heading'] ) . '</h2></header>'
			. '<div class="nlfs__protected-stage" data-nlfs-protected-stage>'
			. '<img class="nlfs__poster" data-nlfs-poster src="' . esc_url( $assets['poster']['url'] ) . '" alt="' . esc_attr( $model_alt ) . '" decoding="async">'
			. '<canvas class="nlfs__model" data-nlfs-model tabindex="-1" aria-disabled="true" aria-label="' . esc_attr( $model_alt ) . '"></canvas>'
			. '<div class="nlfs__model-hotspots" data-nlfs-model-hotspots>' . nadlan_flagship_v3_render_model_hotspots( $config['experiences'], $instance ) . '</div>'
			. '</div>'
			. '<div class="nlfs__controls" aria-label="' . esc_attr( $copy['model_label'] ) . '">'
			. '<button type="button" data-nlfs-action="reset" disabled aria-disabled="true">' . esc_html( $copy['reset'] ) . '</button>'
			. '<button type="button" data-nlfs-action="north" aria-label="איפוס אזימוט ההמחשה לאפס מעלות" disabled aria-disabled="true">איפוס אזימוט 0°</button>'
			. '<button type="button" data-nlfs-action="zoom-in" aria-label="' . esc_attr( $copy['zoom_in'] ) . '" disabled aria-disabled="true">+</button>'
			. '<button type="button" data-nlfs-action="zoom-out" aria-label="' . esc_attr( $copy['zoom_out'] ) . '" disabled aria-disabled="true">−</button>'
			. '<output data-nlfs-model-bearing aria-live="polite">אזימוט המחשה: 0°</output>'
			. '<p data-nlfs-model-status role="status">' . esc_html( $copy['loading'] ) . '</p></div>'
			. '<aside class="nlfs__selection" data-nlfs-selection-card data-selection-state="idle" hidden aria-live="polite" aria-labelledby="' . esc_attr( $instance . '-selection-title' ) . '">'
			. '<button type="button" class="nlfs__selection-back" data-nlfs-selection-back aria-label="חזרה לבניין">← <span>חזרה לבניין</span></button>'
			. '<div class="nlfs__selection-copy"><span data-nlfs-selection-truth>המחשה בלבד · לא מיקום רשמי</span><h3 id="' . esc_attr( $instance . '-selection-title' ) . '" data-nlfs-selection-title>בחירה במודל</h3><p data-nlfs-selection-summary></p><p data-nlfs-selection-disclosure>הבחירה נשארת ליד הבניין והמפה; חומר עמוק נפתח רק בפעולה מפורשת.</p><p data-nlfs-selection-map-state>המפה תגיב רק למיקום או לכיוון שאומתו.</p>'
			. '<details class="nlfs__evidence nlfs__selection-evidence" data-nlfs-selection-evidence data-decision-grade="false"><summary>מקורות ומגבלות לבחירה</summary><dl><div><dt>החלטה</dt><dd data-nlfs-selection-decision></dd></div><div><dt>בתוקף מ־</dt><dd data-nlfs-selection-effective></dd></div><div><dt>אסמכתאות</dt><dd data-nlfs-selection-sources></dd></div><div><dt>ביטחון</dt><dd data-nlfs-selection-confidence></dd></div><div><dt>בסיס המיקום</dt><dd data-nlfs-selection-basis></dd></div><div><dt>מגבלה</dt><dd data-nlfs-selection-limitation lang="en"></dd></div></dl></details></div>'
			. '<div class="nlfs__selection-actions" data-nlfs-selection-actions aria-label="המשך מפורש לבחירה"></div></aside>'
			. '</section>'
			. '<section id="' . esc_attr( $instance . '-area-map' ) . '" class="nlfs__map-shadow" data-nlfs-page-slot="attached_area_map" data-nlfs-map-slot aria-labelledby="' . esc_attr( $instance . '-area-map-title' ) . '"><header><span>אותו הקשר מרחבי</span><h2 id="' . esc_attr( $instance . '-area-map-title' ) . '">המודל והמפה עובדים יחד</h2><p>בחירה מאומתת יכולה למקד את המפה. המחשת מתקן בלי קואורדינטות אינה מזיזה אותה ואינה מסובבת את אלומת הכיוון.</p></header><div class="nlfs__map-mount" data-nlfs-map-mount aria-busy="true"><p data-nlfs-map-slot-status role="status">מפת הסביבה הקיימת מתחברת כאן.</p></div></section></div>'
			. nadlan_flagship_v3_render_primary_actions( $decision, $instance )
			. '<section id="' . esc_attr( $instance . '-decision-tools' ) . '" class="nlfs__decision-tools" data-nlfs-page-slot="decision_tools" aria-labelledby="' . esc_attr( $instance . '-decision-tools-title' ) . '"><header><h2 id="' . esc_attr( $instance . '-decision-tools-title' ) . '">כלי החלטה חזותיים</h2><p>פותחים חוויה עמוקה רק בפעולה מפורשת; חזרה מחזירה למודל ולמפה.</p></header>'
			. nadlan_flagship_v3_render_media_dock( $config['experiences'], $instance )
			. '<div class="nlfs__playground" data-nlfs-playground aria-live="polite"></div>'
			. nadlan_flagship_v3_render_experiences( $config['experiences'], $instance )
			. nadlan_flagship_v3_render_cotour( $config, $instance )
			. '<div class="nlfs__inventory-state"><p class="nlfs__inventory" data-decision-grade="false">' . esc_html( $copy['inventory_status'] ) . '</p><p class="nlfs__unit-bridge" data-nlfs-unit-bridge-status role="status">אין מלאי דירות מאומת; בחירת קומה או דירה ומבט כיוון נשארים לא זמינים עד לקבלת שורת מלאי חתומה.</p></div>'
			. nadlan_flagship_v3_render_capability_slots( $decision, $instance ) . '</section>'
			. nadlan_flagship_v3_render_tutorial_film( $decision, $instance )
			. '<section id="' . esc_attr( $instance . '-article-path' ) . '" class="nlfs__original-article" data-nlfs-page-slot="original_article" tabindex="-1" aria-labelledby="' . esc_attr( $instance . '-original-article-title' ) . '"><a class="nlfs__return-decision" data-nlfs-return-decision href="#' . esc_attr( $instance . '-decision-room' ) . '">חזרה לחדר ההחלטה</a><h2 id="' . esc_attr( $instance . '-original-article-title' ) . '" class="nlfs__visually-hidden">הסקירה המקורית המלאה</h2><aside class="nlfs__article-amendment" aria-label="עדכון תפעולי לסקירה"><strong>עדכון לממשק הציבורי:</strong> שלושת הכלים הפעילים הם מבט, פנים ועיצוב. פנים הוא סיור מודרך בין ארבע תמונות המחשה מאושרות, לא הליכה מרחבית, דלת פעילה או הדמיית דירה. מיקום הרהיט בעיצוב נשמר רק בהיסטוריית הדפדפן של הכלי בזמן הביקור וממשיך למעצב הנפרד; הוא אינו העדפת דירה שמורה. כלי ההערות הישן הוסר, ואין שמירת שאלה או פתק. שאלות נשלחות רק מטופס הפנייה בהסכמה. תיאור המצפן או “צפון 0°” בסקירה ההיסטורית מבוטל: למודל אין כיול לכיוונים בעולם האמיתי; איפוס אזימוט 0° מחזיר את זווית ההמחשה בלבד ואינו כיוון דירה או ראיה תכנונית. הפתיח המאושר הוצג בראש העמוד; יתר הסקירה המקורית נשמר להלן פעם אחת, והעדכון הזה גובר על תיאור הכלים ההיסטורי שבה.</aside>'
			. '<div id="' . esc_attr( $instance . '-article' ) . '" class="nlfs__dossier">' . $article_parts['remainder'] . '</div></section>'
			. '<div class="nlfs__supporting" data-nlfs-page-slot="supporting_content"><a class="nlfs__return-decision" data-nlfs-return-decision href="#' . esc_attr( $instance . '-decision-room' ) . '">חזרה לחדר ההחלטה</a>'
			. nadlan_flagship_v3_render_buyer_decision( $config['buyer_decision'], $instance )
			. nadlan_flagship_v3_render_inquiry( $config, $instance ) . '</div>'
			. '<script type="application/json" data-nlfs-config>' . $json . '</script>'
			. '</div>';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_dispatch' ) ) {
	/** Shared composer seam: selected v3 posts never fall back after rejection. */
	function nadlan_flagship_v3_dispatch( $post_id, $legacy_html ) {
		return nadlan_flagship_v3_is_selected( $post_id )
			? nadlan_flagship_v3_render_for( $post_id, $legacy_html )
			: (string) $legacy_html;
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_fail_closed' ) ) {
	function nadlan_flagship_v3_fail_closed() {
		nocache_headers();
		header( 'Cache-Control: private, no-store, no-cache, max-age=0, must-revalidate', true );
		header( 'X-Robots-Tag: noindex, nofollow, noarchive', true );
		wp_die(
			esc_html__( 'Not found.' ),
			esc_html__( 'Not found.' ),
			array( 'response' => 404 )
		);
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_template_guard' ) ) {
	function nadlan_flagship_v3_template_guard() {
		if ( ! is_singular( 'nadlan_project' ) ) {
			return;
		}
		$post_id = (int) get_queried_object_id();
		if ( ! nadlan_flagship_v3_is_selected( $post_id ) ) {
			return;
		}
		if ( is_wp_error( nadlan_flagship_v3_validate_post( $post_id ) ) ) {
			nadlan_flagship_v3_fail_closed();
		}
	}
}
add_action( 'template_redirect', 'nadlan_flagship_v3_template_guard', -20 );

if ( ! function_exists( 'nadlan_flagship_v3_robots' ) ) {
	function nadlan_flagship_v3_robots( $robots ) {
		if ( nadlan_flagship_v3_is_private_candidate() ) {
			$robots['noindex']   = true;
			$robots['nofollow']  = true;
			$robots['noarchive'] = true;
		}
		return $robots;
	}
}
add_filter( 'wp_robots', 'nadlan_flagship_v3_robots', 100 );

if ( ! function_exists( 'nadlan_flagship_v3_private_headers' ) ) {
	function nadlan_flagship_v3_private_headers() {
		if ( ! nadlan_flagship_v3_is_private_candidate() ) {
			$live = function_exists( 'nadlan_flagship_v3_public_live_contract' ) ? nadlan_flagship_v3_public_live_contract() : false;
			if ( is_singular( 'nadlan_project' ) && is_array( $live ) && (int) $live['post_id'] === (int) get_queried_object_id() ) {
				header( 'Cache-Control: public, max-age=300, must-revalidate', true );
				header( 'X-Nadlan-Public-Release: ' . (string) $live['deployment_id'], true );
			}
			return;
		}
		nocache_headers();
		header( 'Cache-Control: private, no-store, no-cache, max-age=0, must-revalidate', true );
		header( 'X-Robots-Tag: noindex, nofollow, noarchive', true );
		header( 'Referrer-Policy: no-referrer', true );
		header( 'X-Content-Type-Options: nosniff', true );
		header( 'X-Frame-Options: SAMEORIGIN', true );
	}
}
add_action( 'send_headers', 'nadlan_flagship_v3_private_headers', 999 );

if ( ! function_exists( 'nadlan_flagship_v3_private_head_text' ) ) {
	function nadlan_flagship_v3_private_head_text( $value ) {
		return nadlan_flagship_v3_is_private_candidate() ? '' : $value;
	}
}
foreach ( array( 'wpseo_metadesc', 'wpseo_opengraph_title', 'wpseo_opengraph_desc', 'wpseo_twitter_title', 'wpseo_twitter_description' ) as $nadlan_flagship_v3_head_filter ) {
	add_filter( $nadlan_flagship_v3_head_filter, 'nadlan_flagship_v3_private_head_text', 100 );
}
unset( $nadlan_flagship_v3_head_filter );

if ( ! function_exists( 'nadlan_flagship_v3_private_canonical' ) ) {
	function nadlan_flagship_v3_private_canonical( $canonical ) {
		return nadlan_flagship_v3_is_private_candidate() ? false : $canonical;
	}
}
add_filter( 'wpseo_canonical', 'nadlan_flagship_v3_private_canonical', PHP_INT_MAX );

if ( ! function_exists( 'nadlan_flagship_v3_suppress_false_inventory_faq' ) ) {
	/** The shared project FAQ promises floor/unit selection; suppress it for signed zero-inventory Einstein. */
	function nadlan_flagship_v3_suppress_false_inventory_faq() {
		if ( is_singular( 'nadlan_project' ) && nadlan_flagship_v3_is_selected( (int) get_queried_object_id() ) ) {
			remove_action( 'wp_head', 'nadlan_pjx_faq_jsonld', 30 );
		}
	}
}
add_action( 'wp_head', 'nadlan_flagship_v3_suppress_false_inventory_faq', 29 );

if ( ! function_exists( 'nadlan_flagship_v3_suppress_legacy_lead_duplication' ) ) {
	/**
	 * V3 owns the exact lead -> non-affiliation sequence inside the governed root.
	 * Remove the generic extraction/recomposition and generic notice for this one
	 * selected route, then render the shared legal wording once in that sequence.
	 * The later glossary text mutation is also excluded so the pinned dossier is
	 * not changed after its hash gate.
	 */
	function nadlan_flagship_v3_suppress_legacy_lead_duplication() {
		if ( ! is_singular( 'nadlan_project' ) || ! nadlan_flagship_v3_is_selected( (int) get_queried_object_id() ) ) {
			return;
		}
		remove_filter( 'the_content', 'nadlan_lead_extract', 0 );
		remove_filter( 'the_content', 'nadlan_project_notice_render', 20 );
		remove_filter( 'the_content', 'nadlan_lead_recompose', 21 );
		remove_filter( 'the_content', 'nadlan_autolink_content', 24 );
		/* The fleet feature bar prepends itself before the approved lead and
		   duplicates the governed decision-tools row. Every live capability it
		   links (designer, district tour, earth context) is carried by the v3
		   integrations config, so the flagship page renders one tools surface. */
		remove_filter( 'the_content', 'nadlan_fbar_render', 11 );
		remove_filter( 'the_content', 'nadlan_fbar_repair', PHP_INT_MAX );
		unset( $GLOBALS['nl_lead_html'] );
	}
}
add_action( 'wp', 'nadlan_flagship_v3_suppress_legacy_lead_duplication', PHP_INT_MAX );

if ( ! function_exists( 'nadlan_flagship_v3_public_live_contract' ) ) {
	/** Return release identity only after the exact canonical promotion is live. */
	function nadlan_flagship_v3_public_live_contract() {
		$contract = nadlan_flagship_v3_contract( 'einstein-tower-6885-32' );
		$post_id = isset( $contract['canonical_post_id'] ) ? (int) $contract['canonical_post_id'] : 0;
		$post = $post_id > 0 ? get_post( $post_id ) : null;
		$decision = isset( $contract['public_release_decision_id'] ) ? (string) $contract['public_release_decision_id'] : '';
		$release_key = isset( $contract['public_release_meta_key'] ) ? (string) $contract['public_release_meta_key'] : '';
		$body_marker = isset( $contract['public_body_marker'] ) ? (string) $contract['public_body_marker'] : '';
		$article_marker = isset( $contract['required_article_marker'] ) ? sanitize_key( (string) $contract['required_article_marker'] ) : '';
		$article_sha256 = isset( $contract['required_article_lf_sha256'] ) ? strtolower( (string) $contract['required_article_lf_sha256'] ) : '';
		$deployment_id = $post_id > 0 ? (string) get_post_meta( $post_id, '_nadlan_flagship_deployment_id', true ) : '';
		$article_html = $post instanceof WP_Post ? str_replace( array( "\r\n", "\r" ), "\n", (string) $post->post_content ) : '';
		if ( empty( $contract ) || true !== ( isset( $contract['public_release_enabled'] ) ? $contract['public_release_enabled'] : false )
			|| ! $post instanceof WP_Post || 'nadlan_project' !== (string) $post->post_type || 'publish' !== (string) $post->post_status
			|| '' !== (string) $post->post_password || (string) $contract['canonical_slug'] !== (string) $post->post_name
			|| ! preg_match( '/^_nadlan_[a-z0-9_]+$/', $release_key ) || ! hash_equals( $decision, (string) get_post_meta( $post_id, $release_key, true ) )
			|| ! preg_match( '/^einstein-flagship-public-[0-9.]+$/', $body_marker ) || ! hash_equals( $body_marker, (string) get_post_meta( $post_id, '_nadlan_flagship_body_marker', true ) )
			|| ! preg_match( '/^einstein-public-[0-9]{8}T[0-9]{6}Z-[a-f0-9]{6,16}$/', $deployment_id )
			|| '' === $article_marker || 1 !== preg_match( '/^[a-f0-9]{64}$/D', $article_sha256 ) || ! hash_equals( $article_sha256, hash( 'sha256', $article_html ) )
			|| 1 !== substr_count( $article_html, 'data-nlfs-dossier="' . $article_marker . '"' )
			|| '' === nadlan_flagship_v3_mapbox_public_token()
			|| ! nadlan_flagship_v3_lead_pipeline_ready()
			|| (string) $contract['source_id'] !== (string) get_post_meta( $post_id, 'source_id', true )
			|| metadata_exists( 'post', $post_id, '_nadlan_private_unit_journey' ) || ! nadlan_flagship_v3_source_id_is_unique( (string) $contract['source_id'], $post_id ) ) {
			return false;
		}
		$validated = nadlan_flagship_v3_validate_post( $post_id );
		if ( is_wp_error( $validated ) || 'canonical' !== (string) ( isset( $validated['mode'] ) ? $validated['mode'] : '' ) ) {
			return false;
		}
		return array( 'post_id' => $post_id, 'decision_id' => $decision, 'deployment_id' => $deployment_id, 'body_marker' => $body_marker );
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_health' ) ) {
	function nadlan_flagship_v3_health( $out ) {
		$live = nadlan_flagship_v3_public_live_contract();
		$out['flagship_v3'] = array(
			'loaded'                  => true,
			'public_release_enabled'  => is_array( $live ),
			'public_release_decision' => is_array( $live ) ? (string) $live['decision_id'] : '',
			'deployment_id'           => is_array( $live ) ? (string) $live['deployment_id'] : '',
			'public_body_marker'      => is_array( $live ) ? (string) $live['body_marker'] : '',
			'public_asset_route'      => is_array( $live ),
			'private_password_gate'   => true,
			'same_origin_assets_only' => true,
			'zero_inventory_only'     => true,
			'content_writes_enabled'  => false,
			'lead_submission_enabled' => true,
			'lead_contract_enforced'  => true,
			'lead_form_contract_ready' => nadlan_flagship_v3_lead_pipeline_ready(),
			'lead_delivery_runtime_ready' => nadlan_flagship_v3_lead_pipeline_ready(),
			'lead_routing_state'       => 'site_admin_fallback',
			'lead_delivery_live_proof_state' => 'external_action_time_required',
			'mapbox_public_token_ready' => '' !== nadlan_flagship_v3_mapbox_public_token(),
		);
		return $out;
	}
}
add_filter( 'nadlan_config_healthcheck', 'nadlan_flagship_v3_health', 20 );

if ( ! function_exists( 'nadlan_flagship_v3_augment_primary_health_route' ) ) {
	/** inc/health.php owns /health separately; mirror the exact public-release contract there. */
	function nadlan_flagship_v3_augment_primary_health_route( $response, $handler, $request ) {
		unset( $handler );
		if ( ! is_object( $request ) || ! method_exists( $request, 'get_route' ) || '/nadlan/v1/health' !== (string) $request->get_route()
			|| ! method_exists( $request, 'get_method' ) || 'GET' !== strtoupper( (string) $request->get_method() ) ) {
			return $response;
		}
		$rest_response = function_exists( 'rest_ensure_response' ) ? rest_ensure_response( $response ) : $response;
		if ( ! is_object( $rest_response ) || ! method_exists( $rest_response, 'get_data' ) || ! method_exists( $rest_response, 'set_data' ) ) {
			return $response;
		}
		$data = $rest_response->get_data();
		if ( ! is_array( $data ) ) {
			return $response;
		}
		$data['version'] = NADLAN_CONFIG_VERSION;
		$data['plugin_version'] = NADLAN_CONFIG_VERSION;
		$rest_response->set_data( nadlan_flagship_v3_health( $data ) );
		return $rest_response;
	}
}
add_filter( 'rest_request_after_callbacks', 'nadlan_flagship_v3_augment_primary_health_route', 30, 3 );
