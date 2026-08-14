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
		if ( $post_id <= 0 || ! nadlan_flagship_v3_is_selected( $post_id ) || current_user_can( 'edit_post', $post_id )
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
		return nadlan_flagship_v3_is_selected( $post_id )
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
		$extensions = array(
			'model_hd'              => array( 'glb' ),
			'model_lod'             => array( 'glb' ),
			'poster'                => array( 'webp', 'jpg', 'jpeg', 'png', 'avif' ),
			'experience_preview'    => array( 'webp', 'jpg', 'jpeg', 'png', 'avif' ),
			'experience_fullscreen' => array( 'webp', 'jpg', 'jpeg', 'png', 'avif' ),
		);
		$extension = strtolower( pathinfo( $path, PATHINFO_EXTENSION ) );
		if ( ! isset( $extensions[ $role ] ) || ! in_array( $extension, $extensions[ $role ], true ) ) {
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
			. "http_response_code( 404 );\n"
			. "header( 'Cache-Control: private, no-store, no-cache, max-age=0, must-revalidate' );\n"
			. "header( 'X-Robots-Tag: noindex, nofollow, noarchive' );\n"
			. "header( 'X-Content-Type-Options: nosniff' );\n"
			. "__halt_compiler();\n";
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_private_asset_registry_entry' ) ) {
	/** Resolve one exact, registry-owned asset name; paths are never inferred. */
	function nadlan_flagship_v3_private_asset_registry_entry( $contract, $requested_name ) {
		$requested_name = (string) $requested_name;
		if ( ! is_array( $contract )
			|| ! preg_match( '#^[a-z0-9][a-z0-9._/-]*$#', $requested_name )
			|| false !== strpos( $requested_name, '//' )
			|| in_array( '..', explode( '/', $requested_name ), true ) ) {
			return array();
		}
		foreach ( isset( $contract['private_assets'] ) && is_array( $contract['private_assets'] ) ? $contract['private_assets'] : array() as $asset ) {
			if ( ! is_array( $asset ) || ! isset( $asset['requested_name'] )
				|| ! hash_equals( (string) $asset['requested_name'], $requested_name ) ) {
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
			return array(
				'requested_name' => $requested_name,
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

if ( ! function_exists( 'nadlan_flagship_v3_private_asset_descriptor' ) ) {
	/**
	 * Authorize and verify one payload before streaming. The complete payload is
	 * hashed first so a corrupt wrapper can never produce a partial response.
	 */
	function nadlan_flagship_v3_private_asset_descriptor( $project_contract_id, $requested_name ) {
		$project_contract_id = (string) $project_contract_id;
		$contract            = nadlan_flagship_v3_contract( $project_contract_id );
		if ( empty( $contract ) || ! empty( $contract['public_release_enabled'] ) ) {
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

		$asset = nadlan_flagship_v3_private_asset_registry_entry( $contract, $requested_name );
		if ( empty( $asset ) ) {
			return nadlan_flagship_v3_error( 'private_asset_not_found' );
		}
		$plugin_root  = realpath( dirname( __DIR__ ) );
		$storage_root = is_string( $plugin_root ) ? realpath( $plugin_root . '/assets/flagship-v3/private-assets' ) : false;
		$storage_path = is_string( $plugin_root ) ? realpath( $plugin_root . '/' . $asset['storage_file'] ) : false;
		$root_prefix  = is_string( $storage_root ) ? trailingslashit( str_replace( '\\', '/', $storage_root ) ) : '';
		$clean_path   = is_string( $storage_path ) ? str_replace( '\\', '/', $storage_path ) : '';
		if ( '' === $root_prefix || '' === $clean_path || 0 !== strpos( $clean_path, $root_prefix ) || ! is_readable( $storage_path ) ) {
			return nadlan_flagship_v3_error( 'private_asset_storage_missing' );
		}

		$prefix      = nadlan_flagship_v3_private_asset_wrapper_prefix();
		$prefix_size = strlen( $prefix );
		$file_size   = filesize( $storage_path );
		if ( false === $file_size || $prefix_size + (int) $asset['bytes'] !== (int) $file_size ) {
			return nadlan_flagship_v3_error( 'private_asset_size_mismatch' );
		}
		$handle = fopen( $storage_path, 'rb' );
		if ( false === $handle ) {
			return nadlan_flagship_v3_error( 'private_asset_storage_unreadable' );
		}
		$stored_prefix = fread( $handle, $prefix_size );
		if ( ! is_string( $stored_prefix ) || ! hash_equals( $prefix, $stored_prefix ) ) {
			fclose( $handle );
			return nadlan_flagship_v3_error( 'private_asset_wrapper_mismatch' );
		}
		$hash_context = hash_init( 'sha256' );
		$payload_size = 0;
		$payload      = '';
		while ( ! feof( $handle ) ) {
			$chunk = fread( $handle, 1048576 );
			if ( false === $chunk ) {
				fclose( $handle );
				return nadlan_flagship_v3_error( 'private_asset_storage_unreadable' );
			}
			if ( '' === $chunk ) {
				continue;
			}
			$payload_size += strlen( $chunk );
			hash_update( $hash_context, $chunk );
			$payload .= $chunk;
		}
		fclose( $handle );
		$payload_sha256 = hash_final( $hash_context );
		if ( (int) $asset['bytes'] !== $payload_size || ! hash_equals( (string) $asset['sha256'], $payload_sha256 ) ) {
			return nadlan_flagship_v3_error( 'private_asset_hash_mismatch' );
		}

		return array_merge(
			$asset,
			array(
				'post_id'        => $post_id,
				'storage_path'   => $storage_path,
				'payload_offset' => $prefix_size,
				'payload'        => $payload,
			)
		);
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
		$marker      = '/flagship-private-asset/';
		if ( 0 !== strpos( $path, $marker ) ) {
			return array();
		}
		$query_string = isset( $_SERVER['QUERY_STRING'] ) ? (string) $_SERVER['QUERY_STRING'] : '';
		$method       = isset( $_SERVER['REQUEST_METHOD'] ) ? strtoupper( (string) $_SERVER['REQUEST_METHOD'] ) : 'GET';
		if ( '' !== $query_string || isset( $parts['query'] ) || ! in_array( $method, array( 'GET', 'HEAD' ), true )
			|| false !== strpos( $path, '%' ) || false !== strpos( $path, '\\' ) ) {
			return nadlan_flagship_v3_error( 'private_asset_invalid_request' );
		}
		$route = substr( $path, strlen( $marker ) );
		$bits  = explode( '/', $route, 2 );
		if ( 2 !== count( $bits ) || ! preg_match( '/^[a-z0-9-]+$/', $bits[0] )
			|| ! preg_match( '#^[a-z0-9][a-z0-9._/-]*$#', $bits[1] )
			|| false !== strpos( $bits[1], '//' ) || in_array( '..', explode( '/', $bits[1] ), true ) ) {
			return nadlan_flagship_v3_error( 'private_asset_invalid_request' );
		}
		return array( 'project_contract_id' => $bits[0], 'requested_name' => $bits[1], 'method' => $method );
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
			nadlan_flagship_v3_fail_closed();
		}
		$asset = nadlan_flagship_v3_private_asset_descriptor( $request['project_contract_id'], $request['requested_name'] );
		if ( is_wp_error( $asset ) ) {
			nadlan_flagship_v3_fail_closed();
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
		if ( 'HEAD' !== $request['method'] ) {
			$offset = 0;
			while ( $offset < (int) $asset['bytes'] ) {
				$chunk = substr( $asset['payload'], $offset, 1048576 );
				$offset += strlen( $chunk );
				echo $chunk; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- exact pre-verified binary payload.
			}
		}
		exit;
	}
}
add_action( 'template_redirect', 'nadlan_flagship_v3_private_asset_template', -100 );

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
			if ( $url_file !== (string) $authorized_asset['file'] ) {
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
		$expected_tools = array( 'view', 'interior', 'design', 'comments' );
		$expected_preview_kinds = array(
			'view' => 'schematic_live_map', 'interior' => 'first_person_door',
			'design' => 'illustrative_plan_drag', 'comments' => 'visual_annotation_request',
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
			|| 'prepared_no_write' !== ( isset( $visual['comments_delivery'] ) ? (string) $visual['comments_delivery'] : '' )
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
			'comments_delivery'   => 'prepared_no_write',
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
				|| $preview_file !== (string) $authorized_asset['preview_file']
				|| $fullscreen_file !== (string) $authorized_asset['fullscreen_file']
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
		$catalog_source_id = (string) get_post_meta( $post_id, 'source_id', true );
		if ( $post_id === (int) $contract['canonical_post_id'] ) {
			if ( ! hash_equals( (string) $contract['source_id'], $catalog_source_id )
				|| (string) $post->post_name !== (string) $contract['canonical_slug'] || empty( $contract['public_release_enabled'] ) || '' !== (string) $post->post_password ) {
				return nadlan_flagship_v3_error( 'canonical_release_disabled' );
			}
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
			$contract,
			$post_id
		);
		if ( is_wp_error( $representations ) ) {
			return $representations;
		}
		$visual = nadlan_flagship_v3_validate_visual_playground(
			nadlan_flagship_v3_json_meta( $post_id, 'project_visual_playground_json' ),
			$contract,
			$locale
		);
		if ( is_wp_error( $visual ) ) {
			return $visual;
		}
		$buyer_decision = nadlan_flagship_v3_validate_buyer_decision(
			nadlan_flagship_v3_json_meta( $post_id, 'project_buyer_decision_contract_json' ),
			$contract,
			$locale
		);
		if ( is_wp_error( $buyer_decision ) ) {
			return $buyer_decision;
		}
		$buyer_sources = array();
		foreach ( $buyer_decision['sources'] as $buyer_source ) {
			$buyer_sources[ (string) $buyer_source['id'] ] = $buyer_source;
		}
		$experiences = nadlan_flagship_v3_validate_experiences(
			nadlan_flagship_v3_json_meta( $post_id, 'project_experience_registry_json' ),
			$contract,
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
			'contract'        => $contract,
			'identity'        => $identity,
			'inventory'       => $inventory,
			'representations' => $representations,
			'visual'          => $visual,
			'experiences'     => $experiences,
			'buyer_decision'  => $buyer_decision,
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
		wp_enqueue_script( 'nadlan-flagship-v3', $base . 'flagship.js', array( 'nadlan-flagship-v3-viewer', 'nadlan-flagship-v3-playground' ), NADLAN_CONFIG_VERSION, true );
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

	function nadlan_flagship_v3_runtime_config( $validated ) {
		$copy = nadlan_flagship_v3_copy( $validated['locale'] );
		$asset_prefix_url = isset( $validated['contract']['experience_asset_path_marker'] ) ? (string) $validated['contract']['experience_asset_path_marker'] : '';
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
			'copy'      => $copy,
			'capabilities' => array(
				'inventory_selection' => false,
				'lead_submission'     => false,
				'comment_submission'  => false,
				'writes_enabled'      => false,
			),
		);
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_source_refs_html' ) ) {
	function nadlan_flagship_v3_source_refs_html( $source_ids, $instance ) {
		$links = array();
		foreach ( (array) $source_ids as $source_id ) {
			$links[] = '<a href="#' . esc_attr( $instance . '-source-' . sanitize_key( (string) $source_id ) ) . '">' . esc_html( (string) $source_id ) . '</a>';
		}
		return '<span class="nlfs__source-refs">' . implode( ' ', $links ) . '</span>';
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_render_model_hotspots' ) ) {
	function nadlan_flagship_v3_render_model_hotspots( $experiences ) {
		$html  = '';
		$index = 0;
		$seen_groups = array();
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
			$html    .= '<button type="button" class="nlfs__model-hotspot" slot="hotspot-' . esc_attr( $scene['id'] )
				. '" data-position="' . esc_attr( $hotspot['position'] ) . '" data-normal="' . esc_attr( $hotspot['normal'] )
				. '" data-nlfs-scene="' . esc_attr( $scene['id'] ) . '" data-nlfs-scene-group="' . esc_attr( $group ) . '" aria-label="' . esc_attr( $scene['open_label'] . ': ' . $scene['title'] )
				. '"><span aria-hidden="true">' . esc_html( (string) $index ) . '</span></button>';
		}
		return $html;
	}
}

if ( ! function_exists( 'nadlan_flagship_v3_render_experiences' ) ) {
	function nadlan_flagship_v3_render_experiences( $experiences, $instance ) {
		$html = '<section class="nlfs__experiences" aria-labelledby="' . esc_attr( $instance . '-experiences' ) . '"><h2 id="'
			. esc_attr( $instance . '-experiences' ) . '">' . esc_html( $experiences['heading'] ) . '</h2><div class="nlfs__experience-grid">';
		foreach ( $experiences['scenes'] as $scene ) {
			$html .= '<article class="nlfs__experience-card" data-experience-kind="' . esc_attr( $scene['kind'] ) . '"><div class="nlfs__experience-preview">'
				. '<img src="' . esc_url( $scene['preview_url'] ) . '" alt="' . esc_attr( $scene['title'] ) . '" loading="lazy" decoding="async"></div>'
				. '<div class="nlfs__experience-copy"><h3>' . esc_html( $scene['title'] ) . '</h3><p>' . esc_html( $scene['summary'] ) . '</p>';
			if ( ! empty( $scene['source_ids'] ) ) {
				$html .= nadlan_flagship_v3_source_refs_html( $scene['source_ids'], $instance );
			}
			$html .= '<button type="button" data-nlfs-scene="' . esc_attr( $scene['id'] ) . '">' . esc_html( $scene['open_label'] ) . '</button></div></article>';
		}
		return $html . '</div></section>';
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
		$html   = is_string( $html ) ? trim( $html ) : '';
		$marker = isset( $contract['required_article_marker'] ) ? sanitize_key( (string) $contract['required_article_marker'] ) : '';
		if ( '' === $html || '' === $marker || strlen( $html ) > 524288
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
		$allowed = array(
			'article' => array( 'class' => true, 'data-nlfs-dossier' => true, 'dir' => true, 'lang' => true, 'aria-labelledby' => true ),
			'section' => array( 'id' => true, 'class' => true, 'aria-labelledby' => true, 'data-source-ids' => true, 'data-as-of' => true ),
			'div' => array( 'class' => true ), 'header' => array( 'class' => true ), 'footer' => array( 'class' => true ),
			'nav' => array( 'class' => true, 'aria-label' => true ),
			'h2' => array( 'id' => true, 'class' => true ), 'h3' => array( 'id' => true, 'class' => true ), 'h4' => array( 'id' => true, 'class' => true ),
			'p' => array( 'class' => true, 'role' => true ), 'ul' => array( 'class' => true ), 'ol' => array( 'class' => true ), 'li' => array( 'class' => true ),
			'details' => array( 'class' => true, 'open' => true ), 'summary' => array( 'class' => true ),
			'table' => array( 'class' => true ), 'thead' => array(), 'tbody' => array(), 'tr' => array(), 'th' => array( 'scope' => true ), 'td' => array(),
			'a' => array( 'href' => true, 'target' => true, 'rel' => true, 'class' => true ),
			'strong' => array(), 'em' => array(), 'small' => array(), 'span' => array( 'class' => true ), 'bdi' => array(), 'br' => array(),
			'figure' => array( 'class' => true ), 'figcaption' => array(), 'img' => array( 'src' => true, 'alt' => true, 'width' => true, 'height' => true, 'loading' => true, 'decoding' => true ),
		);
		$clean = wp_kses( $html, $allowed );
		return 1 === substr_count( $clean, 'data-nlfs-dossier="' . $marker . '"' ) ? $clean : '';
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
		nadlan_flagship_v3_enqueue();
		$config         = nadlan_flagship_v3_runtime_config( $validated );
		$article_html   = nadlan_flagship_v3_safe_article_html( $rendered_article, $validated['contract'] );
		if ( '' === $article_html || false !== strpos( $article_html, $config['copy']['demo_label'] ) ) {
			return '';
		}
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
		return '<main id="' . esc_attr( $instance ) . '" class="nlfs" data-nl-flagship="v3" data-project-contract-id="'
			. esc_attr( $config['identity']['project_contract_id'] ) . '" data-inventory-state="' . esc_attr( $config['inventory']['state'] )
			. '" data-decision-grade="false" dir="' . esc_attr( $config['direction'] ) . '" lang="' . esc_attr( $config['locale'] ) . '">'
			. '<header class="nlfs__page-heading"><h1>' . esc_html( $config['identity']['representation_name'] ) . '</h1></header>'
			. '<section class="nlfs__showroom" aria-labelledby="' . esc_attr( $instance . '-showroom-title' ) . '">'
			. '<header class="nlfs__heading"><h2 id="' . esc_attr( $instance . '-showroom-title' ) . '">' . esc_html( $copy['heading'] ) . '</h2></header>'
			. '<div class="nlfs__protected-stage" data-nlfs-protected-stage>'
			. '<img class="nlfs__poster" data-nlfs-poster src="' . esc_url( $assets['poster']['url'] ) . '" alt="' . esc_attr( $model_alt ) . '" decoding="async">'
			. '<canvas class="nlfs__model" data-nlfs-model tabindex="0" aria-label="' . esc_attr( $model_alt ) . '"></canvas>'
			. '<div class="nlfs__model-hotspots" data-nlfs-model-hotspots>' . nadlan_flagship_v3_render_model_hotspots( $config['experiences'] ) . '</div>'
			. '</div>'
			. '<div class="nlfs__controls" aria-label="' . esc_attr( $copy['model_label'] ) . '">'
			. '<button type="button" data-nlfs-action="reset">' . esc_html( $copy['reset'] ) . '</button>'
			. '<button type="button" data-nlfs-action="zoom-in" aria-label="' . esc_attr( $copy['zoom_in'] ) . '">+</button>'
			. '<button type="button" data-nlfs-action="zoom-out" aria-label="' . esc_attr( $copy['zoom_out'] ) . '">−</button>'
			. '<p data-nlfs-model-status role="status">' . esc_html( $copy['loading'] ) . '</p></div>'
			. '<p class="nlfs__inventory" data-decision-grade="false">' . esc_html( $copy['inventory_status'] ) . '</p>'
			. '<div class="nlfs__playground" data-nlfs-playground aria-live="polite"></div>'
			. nadlan_flagship_v3_render_experiences( $config['experiences'], $instance )
			. nadlan_flagship_v3_render_buyer_decision( $config['buyer_decision'], $instance )
			. '</section><div class="nlfs__dossier">' . $article_html . '</div>'
			. '<script type="application/json" data-nlfs-config>' . $json . '</script>'
			. '</main>';
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
add_action( 'send_headers', 'nadlan_flagship_v3_private_headers', 100 );

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

if ( ! function_exists( 'nadlan_flagship_v3_health' ) ) {
	function nadlan_flagship_v3_health( $out ) {
		$out['flagship_v3'] = array(
			'loaded'                  => true,
			'public_release_enabled'  => false,
			'private_password_gate'   => true,
			'same_origin_assets_only' => true,
			'zero_inventory_only'     => true,
			'writes_enabled'          => false,
		);
		return $out;
	}
}
add_filter( 'nadlan_config_healthcheck', 'nadlan_flagship_v3_health', 20 );
