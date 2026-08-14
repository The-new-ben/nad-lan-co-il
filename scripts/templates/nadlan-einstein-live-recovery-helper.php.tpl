add_action( 'rest_api_init', function () {
	$route_path    = __ROUTE_PATH_JSON__;
	$expected_token = __TOKEN_JSON__;
	$run_id        = __RUN_ID_JSON__;
	$helper_id     = __HELPER_ID_INT__;
	$helper_name   = __HELPER_NAME_JSON__;
	$source_commit = __SOURCE_COMMIT_JSON__;
	$storage_slug  = __STORAGE_SLUG_JSON__;

	register_rest_route( 'nadlan-live-recovery/v1', $route_path, array(
		'methods'             => 'POST',
		'permission_callback' => function () {
			return current_user_can( 'update_plugins' );
		},
		'callback'            => function ( WP_REST_Request $request ) use (
			$route_path,
			$expected_token,
			$run_id,
			$helper_id,
			$helper_name,
			$source_commit,
			$storage_slug
		) {
			global $wpdb;

			$provided_token = (string) $request->get_param( 'token' );
			if ( ! hash_equals( $expected_token, $provided_token ) ) {
				return new WP_Error( 'nadlan_live_recovery_token_invalid', 'Recovery token is invalid.', array( 'status' => 403 ) );
			}

			$helper_sha256 = strtolower( (string) $request->get_param( 'helper_sha256' ) );
			if ( 1 !== preg_match( '/^[a-f0-9]{64}$/D', $helper_sha256 ) ) {
				return new WP_Error( 'nadlan_live_recovery_helper_hash_invalid', 'Recovery helper hash is invalid.', array( 'status' => 400 ) );
			}
			if (
				1 !== preg_match( '/^\/[a-z0-9-]{20,96}$/D', $route_path )
				|| 1 !== preg_match( '/^[a-z0-9.-]{20,96}$/D', $helper_name )
				|| 1 !== preg_match( '/^[a-f0-9]{40}$/D', $source_commit )
				|| 1 !== preg_match( '/^\.nadlan-live-recovery-[a-f0-9]{32}$/D', $storage_slug )
				|| $helper_id < 1
				|| in_array( $helper_id, array( 449, 450 ), true )
			) {
				return new WP_Error( 'nadlan_live_recovery_embedded_contract_invalid', 'Embedded recovery contract is invalid.', array( 'status' => 500 ) );
			}

			$snippets_table = $wpdb->prefix . 'snippets';
			$wpdb->last_error = '';
			$self_rows = $wpdb->get_results(
				$wpdb->prepare(
					"SELECT id, name, code, scope, active FROM {$snippets_table} WHERE id = %d LIMIT 2",
					$helper_id
				),
				ARRAY_A
			);
			if (
				! is_array( $self_rows )
				|| '' !== (string) $wpdb->last_error
				|| 1 !== count( $self_rows )
				|| $helper_id !== (int) $self_rows[0]['id']
				|| $helper_name !== (string) $self_rows[0]['name']
				|| 'global' !== (string) $self_rows[0]['scope']
				|| 1 !== (int) $self_rows[0]['active']
				|| ! hash_equals( $helper_sha256, hash( 'sha256', (string) $self_rows[0]['code'] ) )
				|| false === strpos( (string) $self_rows[0]['code'], $route_path )
			) {
				return new WP_Error( 'nadlan_live_recovery_helper_changed', 'Recovery helper identity, state, or source changed.', array( 'status' => 409 ) );
			}

			$action = sanitize_key( (string) $request->get_param( 'action' ) );
			$allowed_actions = array(
				'audit',
				'snapshot_create',
				'snapshot_status',
				'download_chunk',
				'cleanup_snapshot',
				'storage_status',
				'delete_self',
			);
			if ( ! in_array( $action, $allowed_actions, true ) ) {
				return new WP_Error( 'nadlan_live_recovery_action_invalid', 'Recovery action is invalid.', array( 'status' => 400 ) );
			}

			$expected_run_id = 'einstein-flagship-20260814T124439Z-4527b2';
			$state_key       = 'nadlan_unit_journey_state_' . substr( hash( 'sha256', $expected_run_id ), 0, 16 );
			$lock_key        = 'nadlan_unit_journey_deploy_lock';
			$plugin_file     = 'nadlan-config/nadlan-config.php';
			$plugin_root     = wp_normalize_path( WP_PLUGIN_DIR . '/nadlan-config' );
			$content_root    = wp_normalize_path( WP_CONTENT_DIR );
			$storage_root    = $content_root . '/' . $storage_slug;
			$archive_path    = $storage_root . '/snapshot.zip';
			$archive_partial = $storage_root . '/snapshot.partial.zip';
			$manifest_path   = $storage_root . '/snapshot.json';
			$manifest_partial = $storage_root . '/snapshot.partial.json';
			$chunk_bytes     = 64 * 1024;
			$max_files       = 1024;
			$max_file_bytes  = 25 * 1024 * 1024;
			$max_tree_bytes  = 64 * 1024 * 1024;
			$max_archive_bytes = 32 * 1024 * 1024;
			$failure_stage   = 'request_validation';

			if ( $expected_run_id !== $run_id ) {
				return new WP_Error( 'nadlan_live_recovery_run_identity_invalid', 'Recovery run identity is invalid.', array( 'status' => 500 ) );
			}

			$valid_hash = function ( $value ) {
				return is_string( $value ) && 1 === preg_match( '/^[a-f0-9]{64}$/D', $value );
			};

			$encode_json = function ( $value ) {
				$encoded = wp_json_encode( $value, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
				if ( ! is_string( $encoded ) || '' === $encoded ) {
					throw new RuntimeException( 'json_encoding_failed' );
				}
				return $encoded;
			};

			$validate_relative = function ( $relative ) {
				if (
					! is_string( $relative )
					|| '' === $relative
					|| strlen( $relative ) > 512
					|| false !== strpos( $relative, "\0" )
					|| false !== strpos( $relative, '\\' )
					|| '/' === substr( $relative, 0, 1 )
					|| false !== strpos( $relative, ':' )
				) {
					return false;
				}
				$segments = explode( '/', $relative );
				foreach ( $segments as $segment ) {
					$stem = strtolower( (string) strtok( $segment, '.' ) );
					if (
						'' === $segment
						|| '.' === $segment
						|| '..' === $segment
						|| strlen( $segment ) > 191
						|| 1 === preg_match( '/[\x00-\x1f\x7f]/', $segment )
						|| rtrim( $segment, " ." ) !== $segment
						|| in_array( $stem, array( 'con', 'prn', 'aux', 'nul' ), true )
						|| 1 === preg_match( '/^(?:com|lpt)[1-9]$/D', $stem )
					) {
						return false;
					}
				}
				return true;
			};

			$inventory = function ( $root, $include_rows = false ) use (
				$validate_relative,
				$max_files,
				$max_file_bytes,
				$max_tree_bytes
			) {
				$root_real = @realpath( $root );
				$root_normalized = wp_normalize_path( $root );
				if (
					false === $root_real
					|| wp_normalize_path( $root_real ) !== $root_normalized
					|| ! @is_dir( $root_real )
					|| @is_link( $root )
				) {
					throw new RuntimeException( 'inventory_root_unsafe' );
				}
				$root_real = wp_normalize_path( $root_real );
				$rows = array();
				$bytes = 0;
				$seen = array();
				$iterator = new RecursiveIteratorIterator(
					new RecursiveDirectoryIterator( $root_real, FilesystemIterator::SKIP_DOTS ),
					RecursiveIteratorIterator::SELF_FIRST
				);
				foreach ( $iterator as $file_info ) {
					$path = wp_normalize_path( $file_info->getPathname() );
					if ( $file_info->isLink() || 0 !== strpos( $path, $root_real . '/' ) ) {
						throw new RuntimeException( 'inventory_entry_unsafe' );
					}
					$relative = substr( $path, strlen( $root_real ) + 1 );
					if ( ! $validate_relative( $relative ) ) {
						throw new RuntimeException( 'inventory_relative_path_invalid' );
					}
					if ( $file_info->isDir() ) {
						continue;
					}
					if ( ! $file_info->isFile() ) {
						throw new RuntimeException( 'inventory_non_file_entry' );
					}
					$folded = strtolower( $relative );
					if ( isset( $seen[ $folded ] ) ) {
						throw new RuntimeException( 'inventory_duplicate_path' );
					}
					$seen[ $folded ] = true;
					$size = (int) $file_info->getSize();
					if ( $size < 0 || $size > $max_file_bytes ) {
						throw new RuntimeException( 'inventory_file_size_invalid' );
					}
					$hash = @hash_file( 'sha256', $path );
					if ( ! is_string( $hash ) ) {
						throw new RuntimeException( 'inventory_hash_failed' );
					}
					$bytes += $size;
					if ( $bytes > $max_tree_bytes || count( $rows ) >= $max_files ) {
						throw new RuntimeException( 'inventory_limit_exceeded' );
					}
					$rows[] = array(
						'path'   => $relative,
						'bytes'  => $size,
						'sha256' => $hash,
					);
				}
				usort( $rows, function ( $left, $right ) {
					return strcmp( (string) $left['path'], (string) $right['path'] );
				} );
				$digest_rows = array();
				foreach ( $rows as $row ) {
					$digest_rows[] = $row['path'] . "\t" . $row['bytes'] . "\t" . $row['sha256'];
				}
				$result = array(
					'file_count' => count( $rows ),
					'bytes'      => $bytes,
					'digest'     => hash( 'sha256', implode( "\n", $digest_rows ) ),
				);
				if ( $include_rows ) {
					$result['rows'] = $rows;
				}
				return $result;
			};

			$post_storage_proof = function ( $post_id, $expected_slug = '' ) use ( $encode_json ) {
				global $wpdb;
				$wpdb->last_error = '';
				$core_row = $wpdb->get_row(
					$wpdb->prepare( "SELECT * FROM {$wpdb->posts} WHERE ID = %d", $post_id ),
					ARRAY_A
				);
				if (
					! is_array( $core_row )
					|| '' !== (string) $wpdb->last_error
					|| $post_id !== (int) ( isset( $core_row['ID'] ) ? $core_row['ID'] : 0 )
					|| 'nadlan_project' !== (string) ( isset( $core_row['post_type'] ) ? $core_row['post_type'] : '' )
					|| ( '' !== $expected_slug && $expected_slug !== (string) ( isset( $core_row['post_name'] ) ? $core_row['post_name'] : '' ) )
				) {
					throw new RuntimeException( 'post_core_read_failed' );
				}
				ksort( $core_row, SORT_STRING );
				$wpdb->last_error = '';
				$meta_rows = $wpdb->get_results(
					$wpdb->prepare(
						"SELECT meta_id, meta_key, meta_value FROM {$wpdb->postmeta} WHERE post_id = %d ORDER BY meta_id ASC",
						$post_id
					),
					ARRAY_A
				);
				if ( ! is_array( $meta_rows ) || '' !== (string) $wpdb->last_error || count( $meta_rows ) > 4096 ) {
					throw new RuntimeException( 'post_meta_read_failed' );
				}
				$raw_map = array();
				$duplicate_keys = array();
				foreach ( $meta_rows as &$meta_row ) {
					ksort( $meta_row, SORT_STRING );
					$key = (string) $meta_row['meta_key'];
					if ( array_key_exists( $key, $raw_map ) ) {
						$duplicate_keys[] = $key;
					} else {
						$raw_map[ $key ] = (string) $meta_row['meta_value'];
					}
				}
				unset( $meta_row );
				ksort( $raw_map, SORT_STRING );
				$wpdb->last_error = '';
				$term_rows = $wpdb->get_results(
					$wpdb->prepare(
						"SELECT object_id, term_taxonomy_id, term_order FROM {$wpdb->term_relationships} WHERE object_id = %d ORDER BY term_taxonomy_id ASC",
						$post_id
					),
					ARRAY_A
				);
				if ( ! is_array( $term_rows ) || '' !== (string) $wpdb->last_error || count( $term_rows ) > 1024 ) {
					throw new RuntimeException( 'post_terms_read_failed' );
				}
				foreach ( $term_rows as &$term_row ) {
					ksort( $term_row, SORT_STRING );
				}
				unset( $term_row );
				$core_bytes = serialize( $core_row );
				$meta_bytes = serialize( $meta_rows );
				$term_bytes = serialize( $term_rows );
				if ( strlen( $core_bytes ) + strlen( $meta_bytes ) + strlen( $term_bytes ) > 8 * 1024 * 1024 ) {
					throw new RuntimeException( 'post_storage_too_large' );
				}
				$contract = array(
					'schema'                       => 'nadlan-canonical-post-storage-proof/v1',
					'post_id'                      => $post_id,
					'core_sha256'                  => hash( 'sha256', $core_bytes ),
					'core_column_count'             => count( $core_row ),
					'raw_meta_sha256'              => hash( 'sha256', $meta_bytes ),
					'raw_meta_row_count'           => count( $meta_rows ),
					'term_relationships_sha256'    => hash( 'sha256', $term_bytes ),
					'term_relationships_row_count' => count( $term_rows ),
				);
				$contract['contract_sha256'] = hash( 'sha256', $encode_json( $contract ) );
				return array(
					'contract'       => $contract,
					'core'           => array(
						'post_name'       => (string) $core_row['post_name'],
						'post_status'     => (string) $core_row['post_status'],
						'post_type'       => (string) $core_row['post_type'],
						'password_length' => strlen( (string) $core_row['post_password'] ),
						'title_sha256'    => hash( 'sha256', (string) $core_row['post_title'] ),
						'content_sha256'  => hash( 'sha256', (string) $core_row['post_content'] ),
						'excerpt_sha256'  => hash( 'sha256', (string) $core_row['post_excerpt'] ),
					),
					'raw_map'        => $raw_map,
					'raw_map_sha256' => hash( 'sha256', $encode_json( $raw_map ) ),
					'duplicate_keys' => array_values( array_unique( $duplicate_keys ) ),
				);
			};

			$decode_option = function ( $option_name ) {
				global $wpdb;
				$wpdb->last_error = '';
				$rows = $wpdb->get_results(
					$wpdb->prepare(
						"SELECT option_id, option_name, option_value, autoload FROM {$wpdb->options} WHERE option_name = %s LIMIT 2",
						$option_name
					),
					ARRAY_A
				);
				if ( ! is_array( $rows ) || '' !== (string) $wpdb->last_error || 1 !== count( $rows ) ) {
					throw new RuntimeException( 'option_row_read_failed' );
				}
				$raw = (string) $rows[0]['option_value'];
				if ( '' === $raw || strlen( $raw ) > 2 * 1024 * 1024 || ! is_serialized( $raw ) ) {
					throw new RuntimeException( 'option_value_invalid' );
				}
				$value = @unserialize( trim( $raw ), array( 'allowed_classes' => false ) );
				if ( ! is_array( $value ) ) {
					throw new RuntimeException( 'option_value_decode_failed' );
				}
				return array(
					'option_id'   => (int) $rows[0]['option_id'],
					'option_name' => (string) $rows[0]['option_name'],
					'autoload'    => (string) $rows[0]['autoload'],
					'raw_sha256'  => hash( 'sha256', $raw ),
					'value'       => $value,
				);
			};

			$canonical_contract_valid = function ( $proof, $post_id ) use ( $valid_hash, $encode_json ) {
				if (
					! is_array( $proof )
					|| 'nadlan-canonical-post-storage-proof/v1' !== (string) ( isset( $proof['schema'] ) ? $proof['schema'] : '' )
					|| $post_id !== (int) ( isset( $proof['post_id'] ) ? $proof['post_id'] : 0 )
					|| ! isset( $proof['core_column_count'], $proof['raw_meta_row_count'], $proof['term_relationships_row_count'] )
					|| ! is_int( $proof['core_column_count'] )
					|| ! is_int( $proof['raw_meta_row_count'] )
					|| ! is_int( $proof['term_relationships_row_count'] )
				) {
					return false;
				}
				foreach ( array( 'core_sha256', 'raw_meta_sha256', 'term_relationships_sha256', 'contract_sha256' ) as $key ) {
					if ( ! isset( $proof[ $key ] ) || ! $valid_hash( $proof[ $key ] ) ) {
						return false;
					}
				}
				$base = array(
					'schema'                       => 'nadlan-canonical-post-storage-proof/v1',
					'post_id'                      => $post_id,
					'core_sha256'                  => (string) $proof['core_sha256'],
					'core_column_count'             => $proof['core_column_count'],
					'raw_meta_sha256'              => (string) $proof['raw_meta_sha256'],
					'raw_meta_row_count'           => $proof['raw_meta_row_count'],
					'term_relationships_sha256'    => (string) $proof['term_relationships_sha256'],
					'term_relationships_row_count' => $proof['term_relationships_row_count'],
				);
				return hash_equals( (string) $proof['contract_sha256'], hash( 'sha256', $encode_json( $base ) ) );
			};

			$read_retained_helpers = function () use ( $snippets_table ) {
				global $wpdb;
				$wpdb->last_error = '';
				$rows = $wpdb->get_results(
					"SELECT id, name, code, scope, active FROM {$snippets_table} WHERE id IN (449, 450) ORDER BY id ASC",
					ARRAY_A
				);
				if ( ! is_array( $rows ) || '' !== (string) $wpdb->last_error || 2 !== count( $rows ) ) {
					throw new RuntimeException( 'retained_helper_rows_unavailable' );
				}
				$expected = array(
					449 => array(
						'name'   => 'x-einstein-private-stage-direct-route-6885-32',
						'sha256' => 'dbe87ddc2bd1a5055e0fe75f2aff134ddb04bd327a5f9715981408fe403677a8',
					),
					450 => array(
						'name'   => 'x-einstein-flagship-20260814T124439Z-4527b2',
						'sha256' => '3a365295c1122fdccacc397d0f93e31ee694ec432513616f26490a7c6c5aa449',
					),
				);
				$result = array();
				foreach ( $rows as $row ) {
					$id = (int) $row['id'];
					if ( ! isset( $expected[ $id ] ) ) {
						throw new RuntimeException( 'retained_helper_identity_unknown' );
					}
					$observed_hash = hash( 'sha256', (string) $row['code'] );
					$exact =
						$expected[ $id ]['name'] === (string) $row['name']
						&& $expected[ $id ]['sha256'] === $observed_hash
						&& 'global' === (string) $row['scope']
						&& 1 === (int) $row['active'];
					$result[ (string) $id ] = array(
						'id'          => $id,
						'name'        => (string) $row['name'],
						'scope'       => (string) $row['scope'],
						'active'      => 1 === (int) $row['active'],
						'code_sha256' => $observed_hash,
						'exact'       => $exact,
					);
				}
				return $result;
			};

			$plugin_state = function ( $include_rows = false ) use ( $plugin_file, $plugin_root, $inventory ) {
				require_once ABSPATH . 'wp-admin/includes/plugin.php';
				$main_file = wp_normalize_path( WP_PLUGIN_DIR . '/' . $plugin_file );
				$root_real = @realpath( $plugin_root );
				if (
					false === $root_real
					|| wp_normalize_path( $root_real ) !== $plugin_root
					|| @is_link( $plugin_root )
					|| ! @is_file( $main_file )
					|| @is_link( $main_file )
				) {
					throw new RuntimeException( 'plugin_root_unsafe' );
				}
				$data = get_plugin_data( $main_file, false, false );
				return array(
					'plugin_file'      => $plugin_file,
					'version'          => (string) ( isset( $data['Version'] ) ? $data['Version'] : '' ),
					'active'           => is_plugin_active( $plugin_file ),
					'provenance'       => 'unknown_live_1.72.207_capture',
					'main_file_sha256' => hash_file( 'sha256', $main_file ),
					'inventory'        => $inventory( $plugin_root, $include_rows ),
				);
			};

			$build_audit = function () use (
				$read_retained_helpers,
				$decode_option,
				$state_key,
				$lock_key,
				$expected_run_id,
				$inventory,
				$content_root,
				$post_storage_proof,
				$canonical_contract_valid,
				$plugin_state,
				$encode_json,
				$valid_hash
			) {
				$helpers = $read_retained_helpers();
				$state_row = $decode_option( $state_key );
				$lock_row = $decode_option( $lock_key );
				$state = $state_row['value'];
				$lock = $lock_row['value'];
				$expected_raw_map_sha256 = 'cc0fd63af6f339e70115231f0bfacf62e3f37628ed0abd45a4b0d8fa76a1ee48';
				$expected_backup_digest = 'f1d3a5729bca013a04cced06d54fbc3061733540a948b28eb68c73cefbee3470';
				$expected_canonical_digest = '8e502f9d598fcd2521290ae929d95a0662c90ef965ee0bbc416b772c0d49750b';

				$state_fields_exact =
					$expected_run_id === (string) ( isset( $state['run_id'] ) ? $state['run_id'] : '' )
					&& 'page_creating' === (string) ( isset( $state['phase'] ) ? $state['phase'] : '' )
					&& 6594 === (int) ( isset( $state['page_id'] ) ? $state['page_id'] : 0 )
					&& true === ( isset( $state['page_created_new'] ) ? $state['page_created_new'] : null )
					&& 'external_committed' === (string) ( isset( $state['page_contract_kind'] ) ? $state['page_contract_kind'] : '' )
					&& 'upload' === (string) ( isset( $state['artifact_mode'] ) ? $state['artifact_mode'] : '' )
					&& true === ( isset( $state['upload_verified'] ) ? $state['upload_verified'] : null )
					&& 97 === (int) ( isset( $state['upload_next_index'] ) ? $state['upload_next_index'] : -1 )
					&& 97 === (int) ( isset( $state['upload_total_chunks'] ) ? $state['upload_total_chunks'] : -1 )
					&& 12585473 === (int) ( isset( $state['upload_received_bytes'] ) ? $state['upload_received_bytes'] : -1 )
					&& '1.72.204' === (string) ( isset( $state['before_version'] ) ? $state['before_version'] : '' )
					&& true === ( isset( $state['before_active'] ) ? $state['before_active'] : null )
					&& $expected_backup_digest === (string) ( isset( $state['backup_digest'] ) ? $state['backup_digest'] : '' )
					&& 469 === (int) ( isset( $state['backup_files'] ) ? $state['backup_files'] : -1 )
					&& 28047176 === (int) ( isset( $state['backup_bytes'] ) ? $state['backup_bytes'] : -1 )
					&& $expected_raw_map_sha256 === (string) ( isset( $state['page_raw_meta_sha256'] ) ? $state['page_raw_meta_sha256'] : '' );

				$lock_exact =
					$expected_run_id === (string) ( isset( $lock['run_id'] ) ? $lock['run_id'] : '' )
					&& isset( $lock['created_at'] )
					&& is_int( $lock['created_at'] )
					&& $lock['created_at'] > 0;

				$backup_root = wp_normalize_path( (string) ( isset( $state['backup_root'] ) ? $state['backup_root'] : '' ) );
				$backup_root_pattern = '#^' . preg_quote( $content_root, '#' ) . '/\.nadlan-unit-journey-release-[a-f0-9]{32}/backup$#D';
				if ( 1 !== preg_match( $backup_root_pattern, $backup_root ) || @is_link( $backup_root ) ) {
					throw new RuntimeException( 'retained_backup_scope_invalid' );
				}
				$retained_storage_root = dirname( $backup_root );
				$backup_path = $backup_root . '/nadlan-config';
				$backup_real = @realpath( $backup_root );
				$retained_storage_real = @realpath( $retained_storage_root );
				if (
					false === $backup_real
					|| false === $retained_storage_real
					|| wp_normalize_path( $backup_real ) !== $backup_root
					|| wp_normalize_path( $retained_storage_real ) !== $retained_storage_root
					|| @is_link( $retained_storage_root )
				) {
					throw new RuntimeException( 'retained_storage_realpath_invalid' );
				}
				$backup_inventory = $inventory( $backup_path, false );
				$retained_storage_inventory = $inventory( $retained_storage_root, false );
				$backup_exact =
					$expected_backup_digest === (string) $backup_inventory['digest']
					&& 469 === (int) $backup_inventory['file_count']
					&& 28047176 === (int) $backup_inventory['bytes'];

				$upload_path = wp_normalize_path( (string) ( isset( $state['upload_path'] ) ? $state['upload_path'] : '' ) );
				$expected_upload_path = $retained_storage_root . '/artifact/nadlan-config.zip';
				$upload_absent =
					$expected_upload_path === $upload_path
					&& ! @file_exists( $upload_path )
					&& ! @is_link( $upload_path );

				$stage = $post_storage_proof( 6594, 'sandbox-einstein-tower-flagship-v3-review' );
				$stage_keys = array_keys( $stage['raw_map'] );
				$state_meta_keys = isset( $state['page_meta_keys'] ) && is_array( $state['page_meta_keys'] ) ? $state['page_meta_keys'] : array();
				$expected_stage_keys = $state_meta_keys;
				$expected_stage_keys[] = 'claim_status';
				sort( $expected_stage_keys, SORT_STRING );
				$stage_meta_exact =
					37 === (int) $stage['contract']['raw_meta_row_count']
					&& empty( $stage['duplicate_keys'] )
					&& 37 === count( $stage_keys )
					&& $expected_stage_keys === $stage_keys
					&& $expected_raw_map_sha256 === $stage['raw_map_sha256']
					&& 'private-unit-journey-v2' === (string) ( isset( $stage['raw_map']['_nadlan_private_unit_journey'] ) ? $stage['raw_map']['_nadlan_private_unit_journey'] : '' )
					&& '4867' === (string) ( isset( $stage['raw_map']['_nadlan_flagship_source_post_id'] ) ? $stage['raw_map']['_nadlan_flagship_source_post_id'] : '' )
					&& 'einstein-tower-6885-32' === (string) ( isset( $stage['raw_map']['project_contract_id'] ) ? $stage['raw_map']['project_contract_id'] : '' )
					&& 'unclaimed' === (string) ( isset( $stage['raw_map']['claim_status'] ) ? $stage['raw_map']['claim_status'] : '' )
					&& 0 === (int) $stage['contract']['term_relationships_row_count'];
				$stage_core_exact =
					23 === (int) $stage['contract']['core_column_count']
					&& 'publish' === $stage['core']['post_status']
					&& 'nadlan_project' === $stage['core']['post_type']
					&& 0 === (int) $stage['core']['password_length']
					&& hash_equals( (string) ( isset( $state['page_title_sha256'] ) ? $state['page_title_sha256'] : '' ), $stage['core']['title_sha256'] )
					&& hash_equals( (string) ( isset( $state['page_content_sha256'] ) ? $state['page_content_sha256'] : '' ), $stage['core']['content_sha256'] )
					&& hash_equals( (string) ( isset( $state['page_excerpt_sha256'] ) ? $state['page_excerpt_sha256'] : '' ), $stage['core']['excerpt_sha256'] );

				$canonical = $post_storage_proof( 4867, 'einstein-tower' );
				$baseline = isset( $state['canonical_post_storage_baseline'] ) ? $state['canonical_post_storage_baseline'] : null;
				$canonical_exact =
					$canonical_contract_valid( $baseline, 4867 )
					&& $expected_canonical_digest === (string) $baseline['contract_sha256']
					&& $expected_canonical_digest === (string) $canonical['contract']['contract_sha256']
					&& 23 === (int) $canonical['contract']['core_column_count']
					&& 20 === (int) $canonical['contract']['raw_meta_row_count']
					&& 2 === (int) $canonical['contract']['term_relationships_row_count'];

				$plugin = $plugin_state( false );
				$marker_pre_registered = registered_meta_key_exists( 'post', '_nadlan_private_unit_journey', 'nadlan_project' );
				$plugin_exact =
					'1.72.207' === $plugin['version']
					&& true === $plugin['active']
					&& $valid_hash( $plugin['main_file_sha256'] )
					&& $valid_hash( $plugin['inventory']['digest'] )
					&& $plugin['inventory']['file_count'] > 0
					&& $plugin['inventory']['bytes'] > 0;

				$helpers_exact = $helpers['449']['exact'] && $helpers['450']['exact'];
				$integrity_passed =
					$helpers_exact
					&& $state_fields_exact
					&& $lock_exact
					&& $backup_exact
					&& $upload_absent
					&& $stage_meta_exact
					&& $stage_core_exact
					&& $canonical_exact
					&& $plugin_exact
					&& $marker_pre_registered;
				$fingerprint_contract = array(
					'schema'                    => 'nadlan-einstein-live-recovery-audit-fingerprint/v1',
					'run_id'                    => $expected_run_id,
					'helper_449_sha256'         => $helpers['449']['code_sha256'],
					'helper_450_sha256'         => $helpers['450']['code_sha256'],
					'state_raw_sha256'          => $state_row['raw_sha256'],
					'lock_raw_sha256'           => $lock_row['raw_sha256'],
					'integrity_passed'          => $integrity_passed,
					'retained_storage_digest'   => $retained_storage_inventory['digest'],
					'retained_storage_files'    => $retained_storage_inventory['file_count'],
					'retained_storage_bytes'    => $retained_storage_inventory['bytes'],
					'backup_digest'              => $backup_inventory['digest'],
					'upload_temp_absent'         => $upload_absent,
					'stage_storage_sha256'      => $stage['contract']['contract_sha256'],
					'stage_raw_map_sha256'      => $stage['raw_map_sha256'],
					'canonical_storage_sha256'  => $canonical['contract']['contract_sha256'],
					'plugin_version'             => $plugin['version'],
					'plugin_inventory_digest'    => $plugin['inventory']['digest'],
					'plugin_inventory_files'     => $plugin['inventory']['file_count'],
					'plugin_inventory_bytes'     => $plugin['inventory']['bytes'],
					'marker_pre_registered'      => $marker_pre_registered,
				);
				$audit_fingerprint = hash( 'sha256', $encode_json( $fingerprint_contract ) );
				$safety_holds = array(
					'stage_post_password_absent',
					'live_plugin_provenance_unknown',
				);
				if (
					isset( $state['after_digest'] )
					&& is_string( $state['after_digest'] )
					&& $valid_hash( $state['after_digest'] )
					&& ! hash_equals( $state['after_digest'], $plugin['inventory']['digest'] )
				) {
					$safety_holds[] = 'live_plugin_differs_from_retained_after_digest';
				}

				return array(
					'schema'             => 'nadlan-einstein-live-recovery-audit/v1',
					'run_id'             => $expected_run_id,
					'integrity_passed'    => $integrity_passed,
					'snapshot_eligible'   => $integrity_passed,
					'audit_fingerprint'   => $audit_fingerprint,
					'safety_holds'        => $safety_holds,
					'retained_helpers'    => $helpers,
					'state'               => array(
						'option_row_count'   => 1,
						'raw_sha256'         => $state_row['raw_sha256'],
						'autoload'           => $state_row['autoload'],
						'run_id'             => (string) ( isset( $state['run_id'] ) ? $state['run_id'] : '' ),
						'phase'              => (string) ( isset( $state['phase'] ) ? $state['phase'] : '' ),
						'page_id'            => (int) ( isset( $state['page_id'] ) ? $state['page_id'] : 0 ),
						'fields_exact'       => $state_fields_exact,
					),
					'lock'                => array(
						'option_row_count'   => 1,
						'raw_sha256'         => $lock_row['raw_sha256'],
						'autoload'           => $lock_row['autoload'],
						'run_id'             => (string) ( isset( $lock['run_id'] ) ? $lock['run_id'] : '' ),
						'owned'              => $lock_exact,
					),
					'retained_storage'    => array(
						'storage_leaf'       => basename( $retained_storage_root ),
						'inventory'          => $retained_storage_inventory,
						'backup'             => array(
							'version'          => '1.72.204',
							'inventory'        => $backup_inventory,
							'exact'            => $backup_exact,
						),
						'upload_temp_absent' => $upload_absent,
					),
					'stage_post'         => array(
						'post_id'              => 6594,
						'core'                 => $stage['core'],
						'storage'              => $stage['contract'],
						'raw_map_sha256'       => $stage['raw_map_sha256'],
						'raw_meta_unique_keys' => count( $stage_keys ),
						'duplicate_key_count'  => count( $stage['duplicate_keys'] ),
						'core_exact'           => $stage_core_exact,
						'meta_exact'           => $stage_meta_exact,
					),
					'canonical_post'     => array(
						'post_id' => 4867,
						'storage' => $canonical['contract'],
						'exact'   => $canonical_exact,
					),
					'plugin'             => $plugin,
					'marker_pre_registered' => $marker_pre_registered,
				);
			};

			$storage_status = function () use ( $storage_root ) {
				clearstatcache( true, $storage_root );
				if ( ! @file_exists( $storage_root ) && ! @is_link( $storage_root ) ) {
					return array(
						'absent'       => true,
						'exact_entries'=> array(),
					);
				}
				$real = @realpath( $storage_root );
				if ( false === $real || wp_normalize_path( $real ) !== $storage_root || ! @is_dir( $storage_root ) || @is_link( $storage_root ) ) {
					throw new RuntimeException( 'snapshot_storage_root_unsafe' );
				}
				$entries = @scandir( $storage_root );
				if ( ! is_array( $entries ) ) {
					throw new RuntimeException( 'snapshot_storage_scan_failed' );
				}
				$entries = array_values( array_diff( $entries, array( '.', '..' ) ) );
				sort( $entries, SORT_STRING );
				$allowed = array( '.htaccess', 'index.php', 'snapshot.json', 'snapshot.partial.json', 'snapshot.partial.zip', 'snapshot.zip' );
				foreach ( $entries as $entry ) {
					$path = $storage_root . '/' . $entry;
					if ( ! in_array( $entry, $allowed, true ) || @is_link( $path ) || ! @is_file( $path ) ) {
						throw new RuntimeException( 'snapshot_storage_entry_unsafe' );
					}
				}
				return array(
					'absent'        => false,
					'exact_entries' => $entries,
				);
			};

			$archive_inventory = function ( $path ) use (
				$validate_relative,
				$max_files,
				$max_file_bytes,
				$max_tree_bytes,
				$max_archive_bytes
			) {
				if ( ! class_exists( 'ZipArchive' ) || ! @is_file( $path ) || @is_link( $path ) ) {
					throw new RuntimeException( 'snapshot_archive_unavailable' );
				}
				$archive_bytes = @filesize( $path );
				if ( false === $archive_bytes || $archive_bytes < 1 || $archive_bytes > $max_archive_bytes ) {
					throw new RuntimeException( 'snapshot_archive_size_invalid' );
				}
				$zip = new ZipArchive();
				if ( true !== $zip->open( $path, ZipArchive::CHECKCONS ) ) {
					throw new RuntimeException( 'snapshot_archive_open_failed' );
				}
				$rows = array();
				$seen = array();
				$total = 0;
				try {
					if ( $zip->numFiles < 1 || $zip->numFiles > $max_files * 4 ) {
						throw new RuntimeException( 'snapshot_archive_entry_limit' );
					}
					for ( $index = 0; $index < $zip->numFiles; $index++ ) {
						$stat = $zip->statIndex( $index, ZipArchive::FL_UNCHANGED );
						if ( false === $stat || ! isset( $stat['name'], $stat['size'] ) ) {
							throw new RuntimeException( 'snapshot_archive_stat_failed' );
						}
						$name = (string) $stat['name'];
						if ( 'nadlan-config/' === $name ) {
							continue;
						}
						if ( 0 !== strpos( $name, 'nadlan-config/' ) ) {
							throw new RuntimeException( 'snapshot_archive_root_invalid' );
						}
						$relative = substr( $name, strlen( 'nadlan-config/' ) );
						if ( '/' === substr( $name, -1 ) ) {
							$relative = rtrim( $relative, '/' );
							if ( '' !== $relative && ! $validate_relative( $relative ) ) {
								throw new RuntimeException( 'snapshot_archive_directory_invalid' );
							}
							continue;
						}
						if ( ! $validate_relative( $relative ) ) {
							throw new RuntimeException( 'snapshot_archive_path_invalid' );
						}
						$folded = strtolower( $relative );
						if ( isset( $seen[ $folded ] ) ) {
							throw new RuntimeException( 'snapshot_archive_duplicate_path' );
						}
						$seen[ $folded ] = true;
						$size = (int) $stat['size'];
						if ( $size < 0 || $size > $max_file_bytes || count( $rows ) >= $max_files ) {
							throw new RuntimeException( 'snapshot_archive_file_limit' );
						}
						if ( method_exists( $zip, 'getExternalAttributesIndex' ) ) {
							$opsys = 0;
							$attributes = 0;
							if ( $zip->getExternalAttributesIndex( $index, $opsys, $attributes ) && 3 === (int) $opsys ) {
								$mode = ( $attributes >> 16 ) & 0170000;
								if ( 0120000 === $mode ) {
									throw new RuntimeException( 'snapshot_archive_symlink_rejected' );
								}
							}
						}
						$stream = $zip->getStream( $name );
						if ( false === $stream ) {
							throw new RuntimeException( 'snapshot_archive_stream_failed' );
						}
						$context = hash_init( 'sha256' );
						$read = hash_update_stream( $context, $stream );
						fclose( $stream );
						if ( $size !== $read ) {
							throw new RuntimeException( 'snapshot_archive_stream_size_changed' );
						}
						$total += $size;
						if ( $total > $max_tree_bytes ) {
							throw new RuntimeException( 'snapshot_archive_tree_limit' );
						}
						$rows[] = array(
							'path'   => $relative,
							'bytes'  => $size,
							'sha256' => hash_final( $context ),
						);
					}
				} finally {
					$zip->close();
				}
				usort( $rows, function ( $left, $right ) {
					return strcmp( (string) $left['path'], (string) $right['path'] );
				} );
				$digest_rows = array();
				foreach ( $rows as $row ) {
					$digest_rows[] = $row['path'] . "\t" . $row['bytes'] . "\t" . $row['sha256'];
				}
				return array(
					'file_count' => count( $rows ),
					'bytes'      => $total,
					'digest'     => hash( 'sha256', implode( "\n", $digest_rows ) ),
					'rows'       => $rows,
				);
			};

			$read_manifest = function ( $deep = true ) use (
				$manifest_path,
				$archive_path,
				$run_id,
				$source_commit,
				$storage_slug,
				$valid_hash,
				$encode_json,
				$archive_inventory,
				$chunk_bytes,
				$max_archive_bytes
			) {
				if ( ! @is_file( $manifest_path ) || @is_link( $manifest_path ) || ! @is_file( $archive_path ) || @is_link( $archive_path ) ) {
					throw new RuntimeException( 'snapshot_manifest_unavailable' );
				}
				$manifest_bytes = @file_get_contents( $manifest_path );
				if ( ! is_string( $manifest_bytes ) || '' === $manifest_bytes || strlen( $manifest_bytes ) > 2 * 1024 * 1024 ) {
					throw new RuntimeException( 'snapshot_manifest_size_invalid' );
				}
				$manifest = json_decode( $manifest_bytes, true );
				if ( ! is_array( $manifest ) ) {
					throw new RuntimeException( 'snapshot_manifest_decode_failed' );
				}
				$base = array(
					'schema'             => (string) ( isset( $manifest['schema'] ) ? $manifest['schema'] : '' ),
					'run_id'             => (string) ( isset( $manifest['run_id'] ) ? $manifest['run_id'] : '' ),
					'source_commit'      => (string) ( isset( $manifest['source_commit'] ) ? $manifest['source_commit'] : '' ),
					'storage_slug'       => (string) ( isset( $manifest['storage_slug'] ) ? $manifest['storage_slug'] : '' ),
					'created_at_utc'     => (string) ( isset( $manifest['created_at_utc'] ) ? $manifest['created_at_utc'] : '' ),
					'audit_fingerprint'  => (string) ( isset( $manifest['audit_fingerprint'] ) ? $manifest['audit_fingerprint'] : '' ),
					'plugin'             => isset( $manifest['plugin'] ) ? $manifest['plugin'] : null,
					'archive'            => isset( $manifest['archive'] ) ? $manifest['archive'] : null,
					'public_probe_url'   => (string) ( isset( $manifest['public_probe_url'] ) ? $manifest['public_probe_url'] : '' ),
				);
				if (
					'nadlan-einstein-live-plugin-snapshot/v1' !== $base['schema']
					|| $run_id !== $base['run_id']
					|| $source_commit !== $base['source_commit']
					|| $storage_slug !== $base['storage_slug']
					|| ! $valid_hash( $base['audit_fingerprint'] )
					|| ! is_array( $base['plugin'] )
					|| ! is_array( $base['archive'] )
					|| ! isset( $manifest['contract_sha256'] )
					|| ! $valid_hash( (string) $manifest['contract_sha256'] )
					|| ! hash_equals( (string) $manifest['contract_sha256'], hash( 'sha256', $encode_json( $base ) ) )
				) {
					throw new RuntimeException( 'snapshot_manifest_contract_invalid' );
				}
				$archive = $base['archive'];
				$archive_size = @filesize( $archive_path );
				$archive_mtime = @filemtime( $archive_path );
				if (
					! isset( $archive['sha256'], $archive['bytes'], $archive['chunks'], $archive['chunk_bytes'], $archive['mtime'] )
					|| ! $valid_hash( (string) $archive['sha256'] )
					|| ! is_int( $archive['bytes'] )
					|| $archive['bytes'] < 1
					|| $archive['bytes'] > $max_archive_bytes
					|| $archive['bytes'] !== $archive_size
					|| ! is_int( $archive['mtime'] )
					|| $archive['mtime'] !== $archive_mtime
					|| $chunk_bytes !== (int) $archive['chunk_bytes']
					|| (int) ceil( $archive['bytes'] / $chunk_bytes ) !== (int) $archive['chunks']
				) {
					throw new RuntimeException( 'snapshot_archive_stat_changed' );
				}
				if ( $deep ) {
					$observed_sha256 = @hash_file( 'sha256', $archive_path );
					$observed_inventory = $archive_inventory( $archive_path );
					if (
						! is_string( $observed_sha256 )
						|| ! hash_equals( (string) $archive['sha256'], $observed_sha256 )
						|| ! isset( $base['plugin']['inventory'] )
						|| $base['plugin']['inventory'] !== $observed_inventory
					) {
						throw new RuntimeException( 'snapshot_archive_content_changed' );
					}
				}
				return $manifest;
			};

			try {
				if ( 'audit' === $action ) {
					$failure_stage = 'retained_audit';
					return $build_audit();
				}

				if ( 'storage_status' === $action ) {
					$failure_stage = 'snapshot_storage_status';
					return array(
						'schema'  => 'nadlan-einstein-live-recovery-storage-status/v1',
						'storage' => $storage_status(),
					);
				}

				if ( 'snapshot_create' === $action ) {
					$confirmation = (string) $request->get_param( 'confirmation' );
					if ( ! hash_equals( 'SNAPSHOT-LIVE-NADLAN-CONFIG-1.72.207', $confirmation ) ) {
						return new WP_Error( 'nadlan_live_recovery_snapshot_confirmation_invalid', 'Snapshot confirmation is invalid.', array( 'status' => 400 ) );
					}
					$failure_stage = 'snapshot_preflight';
					$audit_before = $build_audit();
					if ( true !== $audit_before['snapshot_eligible'] ) {
						throw new RuntimeException( 'snapshot_preflight_failed' );
					}
					$current_storage = $storage_status();
					if ( ! $current_storage['absent'] ) {
						if ( in_array( 'snapshot.json', $current_storage['exact_entries'], true ) && in_array( 'snapshot.zip', $current_storage['exact_entries'], true ) ) {
							$manifest = $read_manifest( true );
							if ( ! hash_equals( $audit_before['audit_fingerprint'], (string) $manifest['audit_fingerprint'] ) ) {
								throw new RuntimeException( 'existing_snapshot_live_drift' );
							}
							return array(
								'schema'     => 'nadlan-einstein-live-plugin-snapshot-create/v1',
								'idempotent' => true,
								'manifest'   => $manifest,
								'audit'      => $audit_before,
							);
						}
						throw new RuntimeException( 'partial_snapshot_requires_cleanup' );
					}
					$failure_stage = 'snapshot_storage_create';
					if ( ! @mkdir( $storage_root, 0700 ) || @is_link( $storage_root ) || wp_normalize_path( (string) @realpath( $storage_root ) ) !== $storage_root ) {
						throw new RuntimeException( 'snapshot_storage_create_failed' );
					}
					$guard_htaccess = "<IfModule mod_authz_core.c>\nRequire all denied\n</IfModule>\n<IfModule !mod_authz_core.c>\nDeny from all\n</IfModule>\n";
					$guard_index = "<?php\nhttp_response_code( 404 );\nexit;\n";
					if (
						strlen( $guard_htaccess ) !== @file_put_contents( $storage_root . '/.htaccess', $guard_htaccess, LOCK_EX )
						|| strlen( $guard_index ) !== @file_put_contents( $storage_root . '/index.php', $guard_index, LOCK_EX )
					) {
						throw new RuntimeException( 'snapshot_guard_write_failed' );
					}
					@chmod( $storage_root . '/.htaccess', 0400 );
					@chmod( $storage_root . '/index.php', 0400 );

					$failure_stage = 'snapshot_inventory_before';
					$plugin_before = $plugin_state( true );
					if ( '1.72.207' !== $plugin_before['version'] || true !== $plugin_before['active'] ) {
						throw new RuntimeException( 'snapshot_plugin_identity_invalid' );
					}
					$failure_stage = 'snapshot_archive_create';
					if ( ! class_exists( 'ZipArchive' ) ) {
						throw new RuntimeException( 'ziparchive_unavailable' );
					}
					$zip = new ZipArchive();
					if ( true !== $zip->open( $archive_partial, ZipArchive::CREATE | ZipArchive::EXCL ) ) {
						throw new RuntimeException( 'snapshot_archive_create_failed' );
					}
					$zip_ok = true;
					$directories = array( 'nadlan-config' => true );
					foreach ( $plugin_before['inventory']['rows'] as $row ) {
						$parent = dirname( (string) $row['path'] );
						while ( '.' !== $parent && '' !== $parent ) {
							$directories[ 'nadlan-config/' . $parent ] = true;
							$next = dirname( $parent );
							if ( $next === $parent ) {
								break;
							}
							$parent = $next;
						}
					}
					$directory_names = array_keys( $directories );
					sort( $directory_names, SORT_STRING );
					foreach ( $directory_names as $directory_name ) {
						if ( ! $zip->addEmptyDir( $directory_name ) ) {
							$zip_ok = false;
							break;
						}
					}
					if ( $zip_ok ) {
						foreach ( $plugin_before['inventory']['rows'] as $row ) {
							$source_path = $plugin_root . '/' . $row['path'];
							$archive_name = 'nadlan-config/' . $row['path'];
							if ( @is_link( $source_path ) || ! @is_file( $source_path ) || ! $zip->addFile( $source_path, $archive_name ) ) {
								$zip_ok = false;
								break;
							}
							if ( method_exists( $zip, 'setMtimeName' ) ) {
								$mtime = @filemtime( $source_path );
								if ( false !== $mtime ) {
									$zip->setMtimeName( $archive_name, $mtime );
								}
							}
						}
					}
					$close_ok = $zip->close();
					if ( ! $zip_ok || ! $close_ok ) {
						throw new RuntimeException( 'snapshot_archive_write_failed' );
					}
					@chmod( $archive_partial, 0400 );
					$failure_stage = 'snapshot_archive_verify';
					$archive_inventory = $archive_inventory( $archive_partial );
					if ( $plugin_before['inventory'] !== $archive_inventory ) {
						throw new RuntimeException( 'snapshot_archive_inventory_mismatch' );
					}
					$archive_sha256 = @hash_file( 'sha256', $archive_partial );
					$archive_bytes = @filesize( $archive_partial );
					if ( ! is_string( $archive_sha256 ) || false === $archive_bytes || $archive_bytes < 1 || $archive_bytes > $max_archive_bytes ) {
						throw new RuntimeException( 'snapshot_archive_identity_failed' );
					}
					$failure_stage = 'snapshot_concurrent_drift';
					$plugin_after = $plugin_state( true );
					$audit_after = $build_audit();
					if (
						$plugin_before !== $plugin_after
						|| ! hash_equals( $audit_before['audit_fingerprint'], $audit_after['audit_fingerprint'] )
					) {
						throw new RuntimeException( 'snapshot_concurrent_drift_detected' );
					}
					if ( ! @rename( $archive_partial, $archive_path ) ) {
						throw new RuntimeException( 'snapshot_archive_commit_failed' );
					}
					@chmod( $archive_path, 0400 );
					clearstatcache( true, $archive_path );
					$archive_mtime = @filemtime( $archive_path );
					if ( false === $archive_mtime ) {
						throw new RuntimeException( 'snapshot_archive_mtime_failed' );
					}
					$manifest_base = array(
						'schema'            => 'nadlan-einstein-live-plugin-snapshot/v1',
						'run_id'            => $run_id,
						'source_commit'     => $source_commit,
						'storage_slug'      => $storage_slug,
						'created_at_utc'    => gmdate( 'Y-m-d\TH:i:s\Z' ),
						'audit_fingerprint' => $audit_after['audit_fingerprint'],
						'plugin'            => $plugin_after,
						'archive'           => array(
							'sha256'     => $archive_sha256,
							'bytes'      => (int) $archive_bytes,
							'chunk_bytes'=> $chunk_bytes,
							'chunks'     => (int) ceil( $archive_bytes / $chunk_bytes ),
							'mtime'      => (int) $archive_mtime,
						),
						'public_probe_url'  => content_url( '/' . $storage_slug . '/snapshot.zip' ),
					);
					$manifest = $manifest_base;
					$manifest['contract_sha256'] = hash( 'sha256', $encode_json( $manifest_base ) );
					$manifest_bytes = $encode_json( $manifest );
					if ( strlen( $manifest_bytes ) !== @file_put_contents( $manifest_partial, $manifest_bytes, LOCK_EX ) ) {
						throw new RuntimeException( 'snapshot_manifest_write_failed' );
					}
					@chmod( $manifest_partial, 0400 );
					if ( ! @rename( $manifest_partial, $manifest_path ) ) {
						throw new RuntimeException( 'snapshot_manifest_commit_failed' );
					}
					@chmod( $manifest_path, 0400 );
					$failure_stage = 'snapshot_final_verify';
					$verified_manifest = $read_manifest( true );
					return array(
						'schema'     => 'nadlan-einstein-live-plugin-snapshot-create/v1',
						'idempotent' => false,
						'manifest'   => $verified_manifest,
						'audit'      => $audit_after,
					);
				}

				if ( 'snapshot_status' === $action ) {
					$failure_stage = 'snapshot_status_verify';
					return array(
						'schema'   => 'nadlan-einstein-live-plugin-snapshot-status/v1',
						'manifest' => $read_manifest( true ),
						'storage'  => $storage_status(),
					);
				}

				if ( 'download_chunk' === $action ) {
					$failure_stage = 'snapshot_download_contract';
					$manifest = $read_manifest( false );
					$requested_sha256 = strtolower( (string) $request->get_param( 'archive_sha256' ) );
					$index_raw = $request->get_param( 'index' );
					if (
						! is_int( $index_raw )
						|| $index_raw < 0
						|| $index_raw >= (int) $manifest['archive']['chunks']
						|| ! hash_equals( (string) $manifest['archive']['sha256'], $requested_sha256 )
					) {
						return new WP_Error( 'nadlan_live_recovery_chunk_contract_invalid', 'Snapshot chunk contract is invalid.', array( 'status' => 409 ) );
					}
					$offset = $index_raw * $chunk_bytes;
					$expected_length = min( $chunk_bytes, (int) $manifest['archive']['bytes'] - $offset );
					$handle = @fopen( $archive_path, 'rb' );
					if ( false === $handle || 0 !== fseek( $handle, $offset ) ) {
						if ( is_resource( $handle ) ) {
							fclose( $handle );
						}
						throw new RuntimeException( 'snapshot_chunk_open_failed' );
					}
					$data = '';
					while ( strlen( $data ) < $expected_length && ! feof( $handle ) ) {
						$piece = fread( $handle, $expected_length - strlen( $data ) );
						if ( false === $piece ) {
							fclose( $handle );
							throw new RuntimeException( 'snapshot_chunk_read_failed' );
						}
						$data .= $piece;
					}
					fclose( $handle );
					if ( strlen( $data ) !== $expected_length ) {
						throw new RuntimeException( 'snapshot_chunk_length_changed' );
					}
					return array(
						'schema'         => 'nadlan-einstein-live-plugin-snapshot-chunk/v1',
						'archive_sha256' => $requested_sha256,
						'index'           => $index_raw,
						'chunks'          => (int) $manifest['archive']['chunks'],
						'offset'          => $offset,
						'bytes'           => strlen( $data ),
						'chunk_sha256'    => hash( 'sha256', $data ),
						'data_b64'        => base64_encode( $data ),
					);
				}

				if ( 'cleanup_snapshot' === $action ) {
					$failure_stage = 'snapshot_cleanup_contract';
					$confirmation = (string) $request->get_param( 'confirmation' );
					$allow_partial = true === $request->get_param( 'allow_partial' );
					$expected_archive_sha256 = strtolower( (string) $request->get_param( 'archive_sha256' ) );
					$current_storage = $storage_status();
					if ( $current_storage['absent'] ) {
						return array(
							'schema'     => 'nadlan-einstein-live-plugin-snapshot-cleanup/v1',
							'idempotent' => true,
							'absent'     => true,
						);
					}
					if ( $allow_partial ) {
						$complete_snapshot =
							in_array( 'snapshot.json', $current_storage['exact_entries'], true )
							&& in_array( 'snapshot.zip', $current_storage['exact_entries'], true );
						if ( ! hash_equals( 'CLEANUP-OWN-PARTIAL-SNAPSHOT', $confirmation ) || $complete_snapshot ) {
							return new WP_Error( 'nadlan_live_recovery_partial_cleanup_invalid', 'Partial snapshot cleanup contract is invalid.', array( 'status' => 409 ) );
						}
					} else {
						if ( ! hash_equals( 'CLEANUP-VERIFIED-LIVE-SNAPSHOT', $confirmation ) ) {
							return new WP_Error( 'nadlan_live_recovery_cleanup_confirmation_invalid', 'Snapshot cleanup confirmation is invalid.', array( 'status' => 400 ) );
						}
						$manifest = $read_manifest( true );
						if ( ! hash_equals( (string) $manifest['archive']['sha256'], $expected_archive_sha256 ) ) {
							return new WP_Error( 'nadlan_live_recovery_cleanup_archive_changed', 'Snapshot cleanup archive identity changed.', array( 'status' => 409 ) );
						}
					}
					$failure_stage = 'snapshot_cleanup_delete';
					$delete_order = array( 'snapshot.zip', 'snapshot.partial.zip', 'snapshot.json', 'snapshot.partial.json', 'index.php', '.htaccess' );
					foreach ( $delete_order as $entry ) {
						if ( ! in_array( $entry, $current_storage['exact_entries'], true ) ) {
							continue;
						}
						$path = $storage_root . '/' . $entry;
						if ( @is_link( $path ) || ! @is_file( $path ) || ! @unlink( $path ) ) {
							throw new RuntimeException( 'snapshot_cleanup_file_failed' );
						}
					}
					if ( ! @rmdir( $storage_root ) ) {
						throw new RuntimeException( 'snapshot_cleanup_root_failed' );
					}
					$after = $storage_status();
					if ( ! $after['absent'] ) {
						throw new RuntimeException( 'snapshot_cleanup_absence_unproved' );
					}
					return array(
						'schema'     => 'nadlan-einstein-live-plugin-snapshot-cleanup/v1',
						'idempotent' => false,
						'absent'     => true,
					);
				}

				if ( 'delete_self' === $action ) {
					$failure_stage = 'self_delete_preflight';
					$confirmation = (string) $request->get_param( 'confirmation' );
					if ( ! hash_equals( 'DELETE-OWN-RECOVERY-HELPER', $confirmation ) ) {
						return new WP_Error( 'nadlan_live_recovery_self_delete_confirmation_invalid', 'Helper deletion confirmation is invalid.', array( 'status' => 400 ) );
					}
					if ( ! $storage_status()['absent'] ) {
						return new WP_Error( 'nadlan_live_recovery_self_delete_storage_present', 'Helper deletion requires absent snapshot storage.', array( 'status' => 409 ) );
					}
					$audit_before_delete = null;
					try {
						$audit_before_delete = $build_audit();
					} catch ( Throwable $audit_error ) {
						$audit_before_delete = null;
					}
					if ( ! function_exists( 'Code_Snippets\\delete_snippet' ) ) {
						throw new RuntimeException( 'snippet_delete_api_missing' );
					}
					$failure_stage = 'self_delete';
					\Code_Snippets\delete_snippet( $helper_id, false );
					$wpdb->last_error = '';
					$count_raw = $wpdb->get_var(
						$wpdb->prepare( "SELECT COUNT(*) FROM {$snippets_table} WHERE id = %d", $helper_id )
					);
					if ( '' !== (string) $wpdb->last_error || null === $count_raw || ! ctype_digit( (string) $count_raw ) || 0 !== (int) $count_raw ) {
						throw new RuntimeException( 'snippet_row_absence_unproved' );
					}
					return array(
						'schema'                    => 'nadlan-einstein-live-recovery-helper-delete/v1',
						'helper_id'                 => $helper_id,
						'direct_snippet_row_count' => 0,
						'storage_absent'            => true,
						'retained_audit_fingerprint'=> is_array( $audit_before_delete ) ? $audit_before_delete['audit_fingerprint'] : '',
						'retained_integrity_passed' => is_array( $audit_before_delete ) ? $audit_before_delete['integrity_passed'] : null,
					);
				}
			} catch ( Throwable $error ) {
				return new WP_Error(
					'nadlan_live_recovery_action_failed',
					'Recovery action failed closed.',
					array(
						'status'        => 409,
						'failure_stage' => $failure_stage,
					)
				);
			}
		},
	) );
} );
