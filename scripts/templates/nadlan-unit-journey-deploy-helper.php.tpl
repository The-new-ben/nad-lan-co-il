add_action( 'rest_api_init', function () {
	$route_path      = __ROUTE_PATH__;
	$expected_token  = __TOKEN__;
	$run_id          = __RUN_ID__;
	$helper_id       = __HELPER_ID__;
	$helper_name     = __HELPER_NAME__;
	$artifact_mode   = __ARTIFACT_MODE__;
	$artifact_url    = __ARTIFACT_URL__;
	$artifact_sha256 = __ARTIFACT_SHA256__;
	$artifact_bytes  = __ARTIFACT_BYTES__;
	$artifact_entry_count = __ARTIFACT_ENTRY_COUNT__;
	$artifact_uncompressed_bytes = __ARTIFACT_UNCOMPRESSED_BYTES__;
	$expected_version = __EXPECTED_VERSION__;
	$source_post_id  = __SOURCE_POST_ID__;
	$page_slug       = __PAGE_SLUG__;
	$page_title      = __PAGE_TITLE__;
	$project_display_name = __PROJECT_DISPLAY_NAME__;
	$recovery_adoption_enabled = __RECOVERY_ADOPTION_ENABLED__;
	$external_stage_commit_enabled = __EXTERNAL_STAGE_COMMIT_ENABLED__;
	$project_contract_id = __PROJECT_CONTRACT_ID__;
	$external_stage_meta_b64 = __EXTERNAL_STAGE_META_B64__;
	$external_stage_meta_sha256 = __EXTERNAL_STAGE_META_SHA256__;
	$external_stage_supplemental_meta_b64 = __EXTERNAL_STAGE_SUPPLEMENTAL_META_B64__;
	$external_stage_supplemental_meta_sha256 = __EXTERNAL_STAGE_SUPPLEMENTAL_META_SHA256__;
	$external_stage_title_sha256 = __EXTERNAL_STAGE_TITLE_SHA256__;
	$external_stage_content_sha256 = __EXTERNAL_STAGE_CONTENT_SHA256__;
	$external_stage_excerpt_sha256 = __EXTERNAL_STAGE_EXCERPT_SHA256__;

	register_rest_route( 'nadlan-private-release/v1', $route_path, array(
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
			$artifact_mode,
			$artifact_url,
			$artifact_sha256,
			$artifact_bytes,
			$artifact_entry_count,
			$artifact_uncompressed_bytes,
			$expected_version,
			$source_post_id,
			$page_slug,
			$page_title,
			$project_display_name,
			$recovery_adoption_enabled,
			$external_stage_commit_enabled,
			$project_contract_id,
			$external_stage_meta_b64,
			$external_stage_meta_sha256,
			$external_stage_supplemental_meta_b64,
			$external_stage_supplemental_meta_sha256,
			$external_stage_title_sha256,
			$external_stage_content_sha256,
			$external_stage_excerpt_sha256
		) {
			$provided_token = (string) $request->get_param( 'token' );
			if ( ! hash_equals( $expected_token, $provided_token ) ) {
				return new WP_Error( 'nadlan_release_token_invalid', 'Release token is invalid.', array( 'status' => 403 ) );
			}

			$helper_sha256 = strtolower( (string) $request->get_param( 'helper_sha256' ) );
			if ( 1 !== preg_match( '/^[a-f0-9]{64}$/', $helper_sha256 ) ) {
				return new WP_Error( 'nadlan_release_helper_hash_invalid', 'Helper hash is invalid.', array( 'status' => 400 ) );
			}
			if ( ! function_exists( 'Code_Snippets\\get_snippet' ) ) {
				return new WP_Error( 'nadlan_release_snippets_api_missing', 'Code Snippets API is unavailable.', array( 'status' => 500 ) );
			}

			$self = \Code_Snippets\get_snippet( $helper_id, false );
			$self_valid =
				$self
				&& $helper_id === (int) $self->id
				&& $helper_name === (string) $self->name
				&& 'global' === (string) $self->scope
				&& true === (bool) $self->active
				&& false === (bool) $self->network
				&& method_exists( $self, 'is_trashed' )
				&& false === $self->is_trashed()
				&& hash_equals( $helper_sha256, hash( 'sha256', (string) $self->code ) )
				&& false !== strpos( (string) $self->code, $route_path );
			if ( ! $self_valid ) {
				return new WP_Error( 'nadlan_release_helper_changed', 'Helper identity, state, or code hash changed.', array( 'status' => 409 ) );
			}

			$action       = sanitize_key( (string) $request->get_param( 'action' ) );
			$plugin_slug  = 'nadlan-config';
			$plugin_file  = 'nadlan-config/nadlan-config.php';
			$target_path  = wp_normalize_path( WP_PLUGIN_DIR . '/nadlan-config' );
			$content_root = wp_normalize_path( WP_CONTENT_DIR );
			$upgrade_root = wp_normalize_path( WP_CONTENT_DIR . '/upgrade' );
			$state_key    = 'nadlan_unit_journey_state_' . substr( hash( 'sha256', $run_id ), 0, 16 );
			$lock_key     = 'nadlan_unit_journey_deploy_lock';
			$upload_chunk_bytes = 128 * 1024;
			$artifact_total_chunks = (int) ceil( $artifact_bytes / $upload_chunk_bytes );
			$storage_name  = '.nadlan-unit-journey-release-' . substr( hash( 'sha256', $run_id . '|' . $expected_token . '|storage' ), 0, 32 );
			$storage_root  = $content_root . '/' . $storage_name;
			$upload_root   = $storage_root . '/artifact';
			$upload_path   = $upload_root . '/nadlan-config.zip';
			$backup_root_expected = $storage_root . '/backup';
			$legacy_upload_root = $upgrade_root . '/.nadlan-unit-journey-upload-' . substr( hash( 'sha256', $run_id . '|' . $expected_token ), 0, 24 );
			$legacy_upload_path = $legacy_upload_root . '/nadlan-config.zip';
			$legacy_backup_root = $upgrade_root . '/.nadlan-unit-journey-' . substr( hash( 'sha256', $run_id ), 0, 20 );
			$unmeasured_capacity_cap = 96 * 1024 * 1024;
			$artifact_contract_valid =
				in_array( $artifact_mode, array( 'url', 'upload' ), true )
				&& 1 === preg_match( '/^[a-f0-9]{64}$/', $artifact_sha256 )
				&& $artifact_bytes > 0
				&& $artifact_bytes <= 25 * 1024 * 1024
				&& $artifact_entry_count > 0
				&& $artifact_entry_count <= 4000
				&& $artifact_uncompressed_bytes > 0
				&& $artifact_uncompressed_bytes <= 100 * 1024 * 1024
				&& $artifact_total_chunks > 0
				&& $artifact_total_chunks <= 256;
			if ( ! $artifact_contract_valid ) {
				return new WP_Error( 'nadlan_release_artifact_contract_invalid', 'Embedded artifact contract is invalid.', array( 'status' => 500 ) );
			}
			$external_stage_expected_meta = array();
			$external_stage_supplemental_meta = array();
			if ( $external_stage_commit_enabled ) {
				$external_meta_json = base64_decode( $external_stage_meta_b64, true );
				$external_supplemental_meta_json = base64_decode( $external_stage_supplemental_meta_b64, true );
				$external_stage_expected_meta = is_string( $external_meta_json )
					? json_decode( $external_meta_json, true )
					: null;
				$external_stage_supplemental_meta = is_string( $external_supplemental_meta_json )
					? json_decode( $external_supplemental_meta_json, true )
					: null;
				if (
					! is_string( $external_meta_json )
					|| ! hash_equals( $external_stage_meta_sha256, hash( 'sha256', $external_meta_json ) )
					|| ! is_array( $external_stage_expected_meta )
					|| empty( $external_stage_expected_meta )
					|| ! is_string( $external_supplemental_meta_json )
					|| ! hash_equals( $external_stage_supplemental_meta_sha256, hash( 'sha256', $external_supplemental_meta_json ) )
					|| array( 'claim_status' => 'unclaimed' ) !== $external_stage_supplemental_meta
					|| 1 !== preg_match( '/^[a-f0-9]{64}$/', $external_stage_title_sha256 )
					|| 1 !== preg_match( '/^[a-f0-9]{64}$/', $external_stage_content_sha256 )
					|| 1 !== preg_match( '/^[a-f0-9]{64}$/', $external_stage_excerpt_sha256 )
					|| hash( 'sha256', '' ) === $external_stage_title_sha256
					|| hash( 'sha256', '' ) === $external_stage_content_sha256
				) {
					return new WP_Error( 'nadlan_release_stage_contract_invalid', 'Embedded external stage contract is invalid.', array( 'status' => 500 ) );
				}
				ksort( $external_stage_expected_meta, SORT_STRING );
				ksort( $external_stage_supplemental_meta, SORT_STRING );
			}

			$inventory = function ( $root ) {
				$root_real = realpath( $root );
				if ( false === $root_real || ! is_dir( $root_real ) || is_link( $root ) ) {
					throw new RuntimeException( 'Plugin inventory root is unavailable.' );
				}
				$root_real = wp_normalize_path( $root_real );
				$rows      = array();
				$bytes     = 0;
				$iterator  = new RecursiveIteratorIterator(
					new RecursiveDirectoryIterator( $root_real, FilesystemIterator::SKIP_DOTS ),
					RecursiveIteratorIterator::LEAVES_ONLY
				);
				foreach ( $iterator as $file_info ) {
					$path = wp_normalize_path( $file_info->getPathname() );
					if ( $file_info->isLink() || 0 !== strpos( $path, $root_real . '/' ) || ! $file_info->isFile() ) {
						throw new RuntimeException( 'Plugin inventory contains an unsafe entry.' );
					}
					$relative = substr( $path, strlen( $root_real ) + 1 );
					$size     = (int) $file_info->getSize();
					$hash     = hash_file( 'sha256', $path );
					if ( false === $hash ) {
						throw new RuntimeException( 'Plugin inventory hash failed.' );
					}
					$bytes += $size;
					$rows[] = $relative . "\t" . $size . "\t" . $hash;
				}
				sort( $rows, SORT_STRING );
				return array(
					'file_count' => count( $rows ),
					'bytes'      => $bytes,
					'digest'     => hash( 'sha256', implode( "\n", $rows ) ),
				);
			};

			$plugin_state = function () use ( $plugin_file, $target_path, $inventory ) {
				require_once ABSPATH . 'wp-admin/includes/plugin.php';
				$main_file = wp_normalize_path( WP_PLUGIN_DIR . '/' . $plugin_file );
				if ( ! is_file( $main_file ) || is_link( $main_file ) ) {
					throw new RuntimeException( 'Exact nadlan-config plugin main file is unavailable.' );
				}
				$data = get_plugin_data( $main_file, false, false );
				return array(
					'plugin_file' => $plugin_file,
					'version'     => isset( $data['Version'] ) ? (string) $data['Version'] : '',
					'active'      => is_plugin_active( $plugin_file ),
					'inventory'   => $inventory( $target_path ),
				);
			};

			$validate_zip = function ( $zip_path ) use ( $plugin_slug ) {
				if ( ! class_exists( 'ZipArchive' ) ) {
					throw new RuntimeException( 'ZipArchive is unavailable.' );
				}
				$archive_size = filesize( $zip_path );
				if ( false === $archive_size || $archive_size < 1 || $archive_size > 25 * 1024 * 1024 ) {
					throw new RuntimeException( 'Artifact archive size is outside the release limit.' );
				}
				$zip  = new ZipArchive();
				$open = $zip->open( $zip_path, ZipArchive::CHECKCONS );
				if ( true !== $open ) {
					throw new RuntimeException( 'Artifact ZIP consistency validation failed.' );
				}
				try {
					if ( $zip->numFiles < 1 || $zip->numFiles > 4000 ) {
						throw new RuntimeException( 'Artifact ZIP entry count is outside the release limit.' );
					}
					$total_uncompressed = 0;
					$has_main           = false;
					$seen_names         = array();
					for ( $index = 0; $index < $zip->numFiles; $index++ ) {
						$stat = $zip->statIndex( $index, ZipArchive::FL_UNCHANGED );
						if ( false === $stat || ! isset( $stat['name'], $stat['size'], $stat['crc'] ) ) {
							throw new RuntimeException( 'Artifact ZIP entry metadata is invalid.' );
						}
						$name = (string) $stat['name'];
						if (
							'' === $name
							|| false !== strpos( $name, "\0" )
							|| false !== strpos( $name, '\\' )
							|| '/' === substr( $name, 0, 1 )
							|| false !== strpos( $name, ':' )
						) {
							throw new RuntimeException( 'Artifact ZIP contains an unsafe path.' );
						}
						$trimmed = rtrim( $name, '/' );
						if ( isset( $seen_names[ $trimmed ] ) ) {
							throw new RuntimeException( 'Artifact ZIP contains a duplicate path.' );
						}
						$seen_names[ $trimmed ] = true;
						$parts   = explode( '/', $trimmed );
						if ( empty( $parts ) || $plugin_slug !== $parts[0] ) {
							throw new RuntimeException( 'Artifact ZIP root is not exactly nadlan-config.' );
						}
						foreach ( $parts as $part ) {
							if ( '' === $part || '.' === $part || '..' === $part ) {
								throw new RuntimeException( 'Artifact ZIP contains path traversal.' );
							}
						}
						$opsys = 0;
						$attr  = 0;
						if ( $zip->getExternalAttributesIndex( $index, $opsys, $attr ) ) {
							$mode = ( $attr >> 16 ) & 0170000;
							if ( 0120000 === $mode ) {
								throw new RuntimeException( 'Artifact ZIP contains a symbolic link.' );
							}
						}
						$is_dir = '/' === substr( $name, -1 );
						if ( $plugin_slug === $trimmed && ! $is_dir ) {
							throw new RuntimeException( 'Artifact ZIP root entry is not a directory.' );
						}
						$size   = (int) $stat['size'];
						if ( $size < 0 || $size > 20 * 1024 * 1024 ) {
							throw new RuntimeException( 'Artifact ZIP entry size is outside the release limit.' );
						}
						$total_uncompressed += $size;
						if ( $total_uncompressed > 100 * 1024 * 1024 ) {
							throw new RuntimeException( 'Artifact ZIP expanded size exceeds the release limit.' );
						}
						if ( ! $is_dir ) {
							$contents = $zip->getFromIndex( $index );
							if ( false === $contents || strlen( $contents ) !== $size ) {
								throw new RuntimeException( 'Artifact ZIP entry could not be read.' );
							}
							$expected_crc = strtolower( sprintf( '%08x', (int) $stat['crc'] ) );
							if ( ! hash_equals( $expected_crc, hash( 'crc32b', $contents ) ) ) {
								throw new RuntimeException( 'Artifact ZIP CRC validation failed.' );
							}
						}
						if ( $plugin_slug . '/nadlan-config.php' === $name ) {
							$has_main = true;
						}
					}
					if ( ! $has_main ) {
						throw new RuntimeException( 'Artifact ZIP is missing the exact plugin main file.' );
					}
					return array(
						'archive_bytes'     => (int) $archive_size,
						'entry_count'       => (int) $zip->numFiles,
						'uncompressed_bytes'=> $total_uncompressed,
					);
				} finally {
					$zip->close();
				}
			};

			$ensure_filesystem = function () {
				require_once ABSPATH . 'wp-admin/includes/file.php';
				if ( ! WP_Filesystem() ) {
					throw new RuntimeException( 'WordPress filesystem could not be initialized.' );
				}
				global $wp_filesystem;
				if ( ! is_object( $wp_filesystem ) ) {
					throw new RuntimeException( 'WordPress filesystem object is unavailable.' );
				}
				return $wp_filesystem;
			};

			$strict_int = function ( $value, $allow_zero = false ) {
				if ( is_int( $value ) ) {
					$parsed = $value;
				} elseif ( is_string( $value ) && 1 === preg_match( '/^(0|[1-9][0-9]*)$/D', $value ) ) {
					$parsed = (int) $value;
				} else {
					return null;
				}
				if ( $parsed < 0 || ( ! $allow_zero && 0 === $parsed ) ) {
					return null;
				}
				return $parsed;
			};

			$storage_scope_status = function () use (
				$content_root,
				$upgrade_root,
				$storage_root,
				$upload_root,
				$upload_path,
				$backup_root_expected
			) {
				$content_real = @realpath( $content_root );
				$upgrade_real = @realpath( $upgrade_root );
				$storage_exists = @file_exists( $storage_root );
				$storage_real = $storage_exists ? @realpath( $storage_root ) : false;
				$scope_exact =
					false !== $content_real
					&& wp_normalize_path( $content_real ) === $content_root
					&& 0 === strpos( $storage_root, $content_root . '/.nadlan-unit-journey-release-' )
					&& $upload_root === $storage_root . '/artifact'
					&& $upload_path === $upload_root . '/nadlan-config.zip'
					&& $backup_root_expected === $storage_root . '/backup';
				$disjoint =
					$storage_root !== $upgrade_root
					&& 0 !== strpos( $storage_root . '/', $upgrade_root . '/' )
					&& 0 !== strpos( $upgrade_root . '/', $storage_root . '/' );
				if ( false !== $upgrade_real && false !== $storage_real ) {
					$upgrade_real = wp_normalize_path( $upgrade_real );
					$storage_real = wp_normalize_path( $storage_real );
					$disjoint =
						$disjoint
						&& $storage_real !== $upgrade_real
						&& 0 !== strpos( $storage_real . '/', $upgrade_real . '/' )
						&& 0 !== strpos( $upgrade_real . '/', $storage_real . '/' );
				}
				$safe =
					$scope_exact
					&& $disjoint
					&& ! @is_link( $content_root )
					&& ! @is_link( $storage_root )
					&& ! @is_link( $upload_root )
					&& ! @is_link( $upload_path )
					&& ! @is_link( $backup_root_expected )
					&& ( ! $storage_exists || ( @is_dir( $storage_root ) && false !== $storage_real ) );
				return array(
					'scope_exact'          => $scope_exact,
					'core_upgrade_disjoint'=> $disjoint,
					'safe'                 => $safe,
					'root_exists'          => $storage_exists,
					'parent_writable'      => @is_dir( $content_root ) && @is_writable( $content_root ),
				);
			};

			$upload_temp_status = function () use ( $storage_scope_status, $upload_root, $upload_path ) {
				clearstatcache( true, $upload_path );
				$root_exists = file_exists( $upload_root );
				$file_exists = file_exists( $upload_path );
				$root_real   = $root_exists ? @realpath( $upload_root ) : false;
				$file_real   = $file_exists ? @realpath( $upload_path ) : false;
				$scope       = $storage_scope_status();
				$safe        =
					$scope['safe']
					&& ! is_link( $upload_root )
					&& ! is_link( $upload_path )
					&& ( ! $root_exists || ( is_dir( $upload_root ) && false !== $root_real ) )
					&& (
						! $file_exists
						|| (
							false !== $root_real
							&& false !== $file_real
							&& wp_normalize_path( $root_real . '/nadlan-config.zip' ) === wp_normalize_path( $file_real )
						)
					);
				$file_bytes  = $safe && is_file( $upload_path ) ? @filesize( $upload_path ) : 0;
				return array(
					'temp_absent' => ! $root_exists && ! $file_exists,
					'temp_exists' => $root_exists || $file_exists,
					'temp_safe'   => $safe,
					'temp_bytes'  => false === $file_bytes ? 0 : (int) $file_bytes,
				);
			};

			$recorded_upload_status = function ( $recorded_path ) use (
				$upload_path,
				$upload_temp_status,
				$legacy_upload_root,
				$legacy_upload_path,
				$upgrade_root
			) {
				$recorded_path = wp_normalize_path( (string) $recorded_path );
				if ( $upload_path === $recorded_path ) {
					$status = $upload_temp_status();
					$status['allowed'] = true;
					$status['legacy']  = false;
					return $status;
				}
				if ( $legacy_upload_path !== $recorded_path ) {
					return array( 'allowed' => false, 'legacy' => false, 'temp_absent' => false, 'temp_exists' => false, 'temp_safe' => false, 'temp_bytes' => 0 );
				}
				clearstatcache( true, $legacy_upload_path );
				$root_exists = @file_exists( $legacy_upload_root );
				$file_exists = @file_exists( $legacy_upload_path );
				$safe =
					$legacy_upload_path === $legacy_upload_root . '/nadlan-config.zip'
					&& 0 === strpos( $legacy_upload_root, $upgrade_root . '/.nadlan-unit-journey-upload-' )
					&& ! @is_link( $upgrade_root )
					&& ! @is_link( $legacy_upload_root )
					&& ! @is_link( $legacy_upload_path )
					&& ( ! $root_exists || @is_dir( $legacy_upload_root ) )
					&& ( ! $file_exists || @is_file( $legacy_upload_path ) );
				$file_bytes = $safe && $file_exists ? @filesize( $legacy_upload_path ) : 0;
				return array(
					'allowed'     => true,
					'legacy'      => true,
					'temp_absent' => ! $root_exists && ! $file_exists,
					'temp_exists' => $root_exists || $file_exists,
					'temp_safe'   => $safe,
					'temp_bytes'  => false === $file_bytes ? 0 : (int) $file_bytes,
				);
			};

			$cleanup_upload_temp = function () use ( $upload_root, $upload_path, $ensure_filesystem, $upload_temp_status ) {
				try {
					$status = $upload_temp_status();
					if ( ! $status['temp_safe'] ) {
						return false;
					}
					if ( $status['temp_exists'] ) {
						$wp_filesystem = $ensure_filesystem();
						if ( ! $wp_filesystem->delete( $upload_root, true, 'd' ) ) {
							return false;
						}
					}
					$status = $upload_temp_status();
					return $status['temp_absent'] && $status['temp_safe'];
				} catch ( Throwable $error ) {
					return false;
				}
			};

			$prepare_upload_root = function () use (
				$storage_root,
				$upload_root,
				$upload_path,
				$ensure_filesystem,
				$cleanup_upload_temp,
				$storage_scope_status
			) {
				$scope = $storage_scope_status();
				if ( ! $scope['safe'] || is_link( $upload_root ) || is_link( $upload_path ) ) {
					throw new RuntimeException( 'Upload scope contains a symbolic link.' );
				}
				if ( ! $cleanup_upload_temp() ) {
					throw new RuntimeException( 'Prior run-scoped upload could not be removed safely.' );
				}
				$wp_filesystem = $ensure_filesystem();
				if ( ! $wp_filesystem->exists( $storage_root ) && ! $wp_filesystem->mkdir( $storage_root, FS_CHMOD_DIR ) ) {
					throw new RuntimeException( 'Run-scoped release root could not be created.' );
				}
				$root_deny_written  = $wp_filesystem->put_contents( $storage_root . '/.htaccess', "Require all denied\nDeny from all\n", FS_CHMOD_FILE );
				$root_index_written = $wp_filesystem->put_contents( $storage_root . '/index.php', "<?php\nhttp_response_code(404);\nexit;\n", FS_CHMOD_FILE );
				if ( ! $wp_filesystem->mkdir( $upload_root, FS_CHMOD_DIR ) ) {
					throw new RuntimeException( 'Run-scoped upload directory could not be created.' );
				}
				$deny_written  = $wp_filesystem->put_contents( $upload_root . '/.htaccess', "Require all denied\nDeny from all\n", FS_CHMOD_FILE );
				$index_written = $wp_filesystem->put_contents( $upload_root . '/index.php', "<?php\nhttp_response_code(404);\nexit;\n", FS_CHMOD_FILE );
				$file_handle   = @fopen( $upload_path, 'x+b' );
				$file_written  = false !== $file_handle;
				$file_permissions = false;
				if ( false !== $file_handle ) {
					$file_written = @fclose( $file_handle );
					$file_permissions = $wp_filesystem->chmod( $upload_path, FS_CHMOD_FILE );
				}
				clearstatcache( true, $upload_path );
				if (
					! $root_deny_written
					|| ! $root_index_written
					|| ! $deny_written
					|| ! $index_written
					|| ! $file_written
					|| ! $file_permissions
					|| ! is_file( $upload_path )
					|| is_link( $upload_path )
					|| 0 !== (int) @filesize( $upload_path )
				) {
					$cleanup_upload_temp();
					throw new RuntimeException( 'Run-scoped upload initialization failed.' );
				}
			};

			$purge_caches = function () {
				wp_clean_plugins_cache( true );
				$object_cache_flushed = wp_cache_flush();
				do_action( 'litespeed_purge_all' );
				return array(
					'object_cache_flushed'    => false !== $object_cache_flushed,
					'litespeed_purge_requested'=> true,
				);
			};

			$state = get_option( $state_key, array() );
			if ( ! is_array( $state ) || ( ! empty( $state ) && $run_id !== (string) ( isset( $state['run_id'] ) ? $state['run_id'] : '' ) ) ) {
				return new WP_Error( 'nadlan_release_state_changed', 'Release state identity changed.', array( 'status' => 409 ) );
			}

			$save_state = function ( $next ) use ( $state_key, $run_id ) {
				$next['run_id']    = $run_id;
				$next['updated_at'] = time();
				update_option( $state_key, $next, false );
				$observed = get_option( $state_key, array() );
				if (
					! is_array( $observed )
					|| $run_id !== (string) ( isset( $observed['run_id'] ) ? $observed['run_id'] : '' )
					|| ! hash_equals( hash( 'sha256', maybe_serialize( $next ) ), hash( 'sha256', maybe_serialize( $observed ) ) )
				) {
					throw new RuntimeException( 'Release state persistence verification failed.' );
				}
				return $observed;
			};

			$acquire_lock = function () use ( $lock_key, $run_id ) {
				$current = get_option( $lock_key, array() );
				if ( empty( $current ) ) {
					if ( ! add_option( $lock_key, array( 'run_id' => $run_id, 'created_at' => time() ), '', 'no' ) ) {
						return false;
					}
					$current = get_option( $lock_key, array() );
				}
				return is_array( $current ) && $run_id === (string) ( isset( $current['run_id'] ) ? $current['run_id'] : '' );
			};

			$release_lock = function () use ( $lock_key, $run_id ) {
				$current = get_option( $lock_key, array() );
				if ( empty( $current ) ) {
					return true;
				}
				if ( is_array( $current ) && $run_id === (string) ( isset( $current['run_id'] ) ? $current['run_id'] : '' ) ) {
					delete_option( $lock_key );
					return false === get_option( $lock_key, false );
				}
				return false;
			};

			$upload_state_valid = function ( $current_state ) use (
				$artifact_mode,
				$artifact_sha256,
				$artifact_bytes,
				$artifact_entry_count,
				$artifact_uncompressed_bytes,
				$artifact_total_chunks,
				$upload_chunk_bytes,
				$upload_path
			) {
				return
					'upload' === $artifact_mode
					&& is_array( $current_state )
					&& in_array( isset( $current_state['phase'] ) ? $current_state['phase'] : '', array( 'uploading', 'upload_verified', 'backup_ready', 'deployed', 'page_creating', 'page_ready', 'rolled_back' ), true )
					&& 'upload' === (string) ( isset( $current_state['artifact_mode'] ) ? $current_state['artifact_mode'] : '' )
					&& $upload_path === wp_normalize_path( (string) ( isset( $current_state['upload_path'] ) ? $current_state['upload_path'] : '' ) )
					&& hash_equals( $artifact_sha256, (string) ( isset( $current_state['upload_expected_sha256'] ) ? $current_state['upload_expected_sha256'] : '' ) )
					&& $artifact_bytes === (int) ( isset( $current_state['upload_expected_bytes'] ) ? $current_state['upload_expected_bytes'] : 0 )
					&& $artifact_entry_count === (int) ( isset( $current_state['upload_expected_entries'] ) ? $current_state['upload_expected_entries'] : 0 )
					&& $artifact_uncompressed_bytes === (int) ( isset( $current_state['upload_expected_uncompressed_bytes'] ) ? $current_state['upload_expected_uncompressed_bytes'] : 0 )
					&& $artifact_total_chunks === (int) ( isset( $current_state['upload_total_chunks'] ) ? $current_state['upload_total_chunks'] : 0 )
					&& $upload_chunk_bytes === (int) ( isset( $current_state['upload_chunk_bytes'] ) ? $current_state['upload_chunk_bytes'] : 0 );
			};

			$retained_upload_state_valid = function ( $current_state ) use (
				$artifact_mode,
				$artifact_sha256,
				$artifact_bytes,
				$artifact_entry_count,
				$artifact_uncompressed_bytes,
				$artifact_total_chunks,
				$upload_chunk_bytes,
				$upload_path,
				$legacy_upload_path
			) {
				if ( ! is_array( $current_state ) ) {
					return false;
				}
				$recorded_path = wp_normalize_path( (string) ( isset( $current_state['upload_path'] ) ? $current_state['upload_path'] : '' ) );
				return
					'upload' === $artifact_mode
					&& in_array( isset( $current_state['phase'] ) ? $current_state['phase'] : '', array( 'backup_ready', 'deployed', 'page_ready', 'rolled_back' ), true )
					&& 'upload' === (string) ( isset( $current_state['artifact_mode'] ) ? $current_state['artifact_mode'] : '' )
					&& in_array( $recorded_path, array( $upload_path, $legacy_upload_path ), true )
					&& hash_equals( $artifact_sha256, (string) ( isset( $current_state['upload_expected_sha256'] ) ? $current_state['upload_expected_sha256'] : '' ) )
					&& $artifact_bytes === ( isset( $current_state['upload_expected_bytes'] ) && is_int( $current_state['upload_expected_bytes'] ) ? $current_state['upload_expected_bytes'] : -1 )
					&& $artifact_entry_count === ( isset( $current_state['upload_expected_entries'] ) && is_int( $current_state['upload_expected_entries'] ) ? $current_state['upload_expected_entries'] : -1 )
					&& $artifact_uncompressed_bytes === ( isset( $current_state['upload_expected_uncompressed_bytes'] ) && is_int( $current_state['upload_expected_uncompressed_bytes'] ) ? $current_state['upload_expected_uncompressed_bytes'] : -1 )
					&& $artifact_total_chunks === ( isset( $current_state['upload_total_chunks'] ) && is_int( $current_state['upload_total_chunks'] ) ? $current_state['upload_total_chunks'] : -1 )
					&& $upload_chunk_bytes === ( isset( $current_state['upload_chunk_bytes'] ) && is_int( $current_state['upload_chunk_bytes'] ) ? $current_state['upload_chunk_bytes'] : -1 )
					&& $artifact_total_chunks === ( isset( $current_state['upload_next_index'] ) && is_int( $current_state['upload_next_index'] ) ? $current_state['upload_next_index'] : -1 )
					&& $artifact_bytes === ( isset( $current_state['upload_received_bytes'] ) && is_int( $current_state['upload_received_bytes'] ) ? $current_state['upload_received_bytes'] : -1 )
					&& true === ( isset( $current_state['upload_verified'] ) ? $current_state['upload_verified'] : false )
					&& hash_equals( $artifact_sha256, (string) ( isset( $current_state['upload_archive_sha256'] ) ? $current_state['upload_archive_sha256'] : '' ) );
			};

			$stage_contract_snapshot = function ( $page_id, $meta_keys ) use (
				$page_slug,
				$source_post_id,
				$project_contract_id,
				$expected_token,
				$external_stage_commit_enabled,
				$external_stage_expected_meta,
				$external_stage_supplemental_meta,
				$external_stage_title_sha256,
				$external_stage_content_sha256,
				$external_stage_excerpt_sha256
			) {
				if ( ! is_int( $page_id ) || $page_id < 1 || $page_id === $source_post_id || ! is_array( $meta_keys ) || count( $meta_keys ) < 3 || count( $meta_keys ) > 128 ) {
					throw new RuntimeException( 'Stage contract identity or meta-key count is invalid.' );
				}
				$normalized_keys = array();
				foreach ( $meta_keys as $meta_key ) {
					if ( ! is_string( $meta_key ) || 1 !== preg_match( '/^[A-Za-z0-9_-]{1,191}$/D', $meta_key ) ) {
						throw new RuntimeException( 'Stage contract contains an invalid meta key.' );
					}
					$normalized_keys[] = $meta_key;
				}
				$sorted_keys = $normalized_keys;
				sort( $sorted_keys, SORT_STRING );
				if ( $sorted_keys !== $normalized_keys || count( array_unique( $normalized_keys ) ) !== count( $normalized_keys ) ) {
					throw new RuntimeException( 'Stage contract meta keys must be unique and sorted.' );
				}
				$required_meta_keys = array( '_nadlan_private_unit_journey', '_nadlan_flagship_source_post_id' );
				if ( '' !== $project_contract_id ) {
					$required_meta_keys[] = 'project_contract_id';
				}
				foreach ( $required_meta_keys as $required_key ) {
					if ( ! in_array( $required_key, $normalized_keys, true ) ) {
						throw new RuntimeException( 'Stage contract is missing a governed meta key.' );
					}
				}
				if ( $external_stage_commit_enabled ) {
					$pinned_keys = array_keys( $external_stage_expected_meta );
					sort( $pinned_keys, SORT_STRING );
					if ( $normalized_keys !== $pinned_keys ) {
						throw new RuntimeException( 'External stage meta keys differ from the embedded allowlist.' );
					}
				}
				$page = get_post( $page_id );
				if (
					! $page
					|| 'nadlan_project' !== (string) $page->post_type
					|| $page_slug !== (string) $page->post_name
					|| 'publish' !== (string) $page->post_status
					|| '' === (string) $page->post_password
					|| '' === (string) $page->post_title
					|| '' === (string) $page->post_content
					|| 'private-unit-journey-v2' !== (string) get_post_meta( $page_id, '_nadlan_private_unit_journey', true )
					|| $source_post_id !== (int) get_post_meta( $page_id, '_nadlan_flagship_source_post_id', true )
					|| ( '' !== $project_contract_id && $project_contract_id !== (string) get_post_meta( $page_id, 'project_contract_id', true ) )
				) {
					throw new RuntimeException( 'Stage contract post fields or governed markers are not exact.' );
				}
				$taxonomy_terms = array();
				$taxonomies = get_object_taxonomies( 'nadlan_project', 'names' );
				if ( ! is_array( $taxonomies ) ) {
					throw new RuntimeException( 'Stage contract taxonomy registry is unavailable.' );
				}
				sort( $taxonomies, SORT_STRING );
				foreach ( $taxonomies as $taxonomy ) {
					$term_ids = wp_get_object_terms( $page_id, $taxonomy, array( 'fields' => 'ids' ) );
					if ( is_wp_error( $term_ids ) || ! is_array( $term_ids ) ) {
						throw new RuntimeException( 'Stage contract taxonomy assignments are unavailable.' );
					}
					$term_ids = array_map( 'intval', $term_ids );
					sort( $term_ids, SORT_NUMERIC );
					foreach ( $term_ids as $term_id ) {
						$taxonomy_terms[] = (string) $taxonomy . ':' . $term_id;
					}
				}
				$template_slug = get_page_template_slug( $page_id );
				$template_slug = false === $template_slug ? '' : (string) $template_slug;
				$core_contract = array(
					'author_id'       => (int) $page->post_author,
					'parent_id'       => (int) $page->post_parent,
					'comment_status'  => (string) $page->comment_status,
					'ping_status'     => (string) $page->ping_status,
					'menu_order'      => (int) $page->menu_order,
					'template'        => $template_slug,
					'taxonomy_terms'  => $taxonomy_terms,
				);
				if (
					(int) get_current_user_id() !== $core_contract['author_id']
					|| 0 !== $core_contract['parent_id']
					|| 'closed' !== $core_contract['comment_status']
					|| 'closed' !== $core_contract['ping_status']
					|| 0 !== $core_contract['menu_order']
					|| '' !== $core_contract['template']
					|| ! empty( $core_contract['taxonomy_terms'] )
				) {
					throw new RuntimeException( 'Stage contract core ownership, hierarchy, discussion, template, or taxonomy fields are not exact.' );
				}
				$core_json = wp_json_encode( $core_contract, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
				if ( ! is_string( $core_json ) ) {
					throw new RuntimeException( 'Stage contract core-field encoding failed.' );
				}
				$slug_matches = get_posts(
					array(
						'name'                   => $page_slug,
						'post_type'              => 'nadlan_project',
						'post_status'            => array_values( get_post_stati( array(), 'names' ) ),
						'posts_per_page'         => 2,
						'fields'                 => 'ids',
						'no_found_rows'          => true,
						'suppress_filters'       => true,
						'update_post_meta_cache' => false,
						'update_post_term_cache' => false,
					)
				);
				if ( ! is_array( $slug_matches ) || array( $page_id ) !== array_map( 'intval', $slug_matches ) ) {
					throw new RuntimeException( 'Stage contract slug is absent or ambiguous.' );
				}
				if (
					$external_stage_commit_enabled
					&& (
						! hash_equals( $external_stage_title_sha256, hash( 'sha256', (string) $page->post_title ) )
						|| ! hash_equals( $external_stage_content_sha256, hash( 'sha256', (string) $page->post_content ) )
						|| ! hash_equals( $external_stage_excerpt_sha256, hash( 'sha256', (string) $page->post_excerpt ) )
					)
				) {
					throw new RuntimeException( 'External stage fields differ from the embedded content contract.' );
				}
				$meta_contract = array();
				if ( $external_stage_commit_enabled ) {
					$rest_request = new WP_REST_Request( 'GET', '/wp/v2/nadlan_project/' . $page_id );
					$rest_request->set_param( 'context', 'edit' );
					$rest_response = rest_do_request( $rest_request );
					if ( is_wp_error( $rest_response ) || 200 !== (int) $rest_response->get_status() ) {
						throw new RuntimeException( 'External stage REST contract could not be read.' );
					}
					$rest_data = $rest_response->get_data();
					$rest_meta = is_array( $rest_data ) && isset( $rest_data['meta'] ) && is_array( $rest_data['meta'] )
						? $rest_data['meta']
						: null;
					if ( ! is_array( $rest_meta ) ) {
						throw new RuntimeException( 'External stage REST meta contract is unavailable.' );
					}
					ksort( $rest_meta, SORT_STRING );
					$expected_meta = $external_stage_expected_meta;
					ksort( $expected_meta, SORT_STRING );
					$pinned_rest_meta = array_intersect_key( $rest_meta, $expected_meta );
					ksort( $pinned_rest_meta, SORT_STRING );
					$rest_meta_json = wp_json_encode( $pinned_rest_meta, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
					$expected_meta_json = wp_json_encode( $expected_meta, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
					if ( ! is_string( $rest_meta_json ) || ! is_string( $expected_meta_json ) || ! hash_equals( hash( 'sha256', $expected_meta_json ), hash( 'sha256', $rest_meta_json ) ) ) {
						throw new RuntimeException( 'External stage pinned REST meta differs from the embedded exact contract.' );
					}
					$supplemental_rest_meta = array_intersect_key( $rest_meta, $external_stage_supplemental_meta );
					ksort( $supplemental_rest_meta, SORT_STRING );
					$supplemental_rest_json = wp_json_encode( $supplemental_rest_meta, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
					$expected_supplemental_json = wp_json_encode( $external_stage_supplemental_meta, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
					if ( ! is_string( $supplemental_rest_json ) || ! is_string( $expected_supplemental_json ) || ! hash_equals( hash( 'sha256', $expected_supplemental_json ), hash( 'sha256', $supplemental_rest_json ) ) ) {
						throw new RuntimeException( 'External stage supplemental REST meta is missing or changed.' );
					}
					foreach ( array_diff_key( $rest_meta, $expected_meta ) as $rest_meta_key => $rest_meta_value ) {
						if ( array_key_exists( $rest_meta_key, $external_stage_supplemental_meta ) ) {
							if ( $external_stage_supplemental_meta[ $rest_meta_key ] !== $rest_meta_value ) {
								throw new RuntimeException( 'External stage supplemental REST meta differs from the exact contract.' );
							}
							$raw_supplemental_values = get_post_meta( $page_id, (string) $rest_meta_key, false );
							if ( ! is_array( $raw_supplemental_values ) || 1 !== count( $raw_supplemental_values ) || $external_stage_supplemental_meta[ $rest_meta_key ] !== $raw_supplemental_values[0] ) {
								throw new RuntimeException( 'External stage supplemental raw meta is missing, duplicated, or changed.' );
							}
							continue;
						}
						$neutral_default =
							null === $rest_meta_value
							|| false === $rest_meta_value
							|| 0 === $rest_meta_value
							|| '' === $rest_meta_value
							|| ( is_array( $rest_meta_value ) && empty( $rest_meta_value ) );
						if ( metadata_exists( 'post', $page_id, (string) $rest_meta_key ) || ! $neutral_default ) {
							throw new RuntimeException( 'External stage has a non-neutral unpinned REST meta field.' );
						}
					}
					$all_raw_meta = get_post_meta( $page_id );
					foreach ( $normalized_keys as $meta_key ) {
						$raw_values = get_post_meta( $page_id, $meta_key, false );
						if ( ! is_array( $raw_values ) || 1 !== count( $raw_values ) ) {
							throw new RuntimeException( 'External stage meta is missing or duplicated.' );
						}
					}
					$allowed_raw_meta = array_merge( $normalized_keys, array_keys( $external_stage_supplemental_meta ) );
					foreach ( array_keys( is_array( $all_raw_meta ) ? $all_raw_meta : array() ) as $observed_meta_key ) {
						if ( ! in_array( (string) $observed_meta_key, $allowed_raw_meta, true ) ) {
							throw new RuntimeException( 'External stage contains unexpected raw meta.' );
						}
					}
					$meta_contract = array_merge( $pinned_rest_meta, $external_stage_supplemental_meta );
				} else {
					$all_raw_meta = get_post_meta( $page_id );
					$observed_raw_keys = array_keys( is_array( $all_raw_meta ) ? $all_raw_meta : array() );
					sort( $observed_raw_keys, SORT_STRING );
					if ( $observed_raw_keys !== $normalized_keys ) {
						throw new RuntimeException( 'Helper-created stage raw meta keys differ from the exact created allowlist.' );
					}
					foreach ( $normalized_keys as $meta_key ) {
						$raw_values = get_post_meta( $page_id, $meta_key, false );
						if ( ! is_array( $raw_values ) || 1 !== count( $raw_values ) ) {
							throw new RuntimeException( 'Helper-created stage meta is missing or duplicated.' );
						}
						$meta_contract[ $meta_key ] = maybe_unserialize( $raw_values[0] );
					}
				}
				ksort( $meta_contract, SORT_STRING );
				$meta_json = wp_json_encode( $meta_contract, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
				if ( ! is_string( $meta_json ) ) {
					throw new RuntimeException( 'Stage contract meta encoding failed.' );
				}
				$snapshot = array(
					'page_id'              => $page_id,
					'title_sha256'         => hash( 'sha256', (string) $page->post_title ),
					'content_sha256'       => hash( 'sha256', (string) $page->post_content ),
					'excerpt_sha256'       => hash( 'sha256', (string) $page->post_excerpt ),
					'core_sha256'          => hash( 'sha256', $core_json ),
					'meta_sha256'          => hash( 'sha256', $meta_json ),
					'meta_keys'            => $normalized_keys,
					'password_fingerprint' => hash_hmac( 'sha256', (string) $page->post_password, $expected_token ),
				);
				$snapshot_json = wp_json_encode( $snapshot, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
				if ( ! is_string( $snapshot_json ) ) {
					throw new RuntimeException( 'Stage contract snapshot encoding failed.' );
				}
				$snapshot['contract_sha256'] = hash( 'sha256', $snapshot_json );
				return $snapshot;
			};

			$stage_scope_absent = function () use ( $page_slug, $source_post_id ) {
				$query = array(
					'post_type'              => 'nadlan_project',
					'post_status'            => array_values( get_post_stati( array(), 'names' ) ),
					'posts_per_page'         => 2,
					'fields'                 => 'ids',
					'no_found_rows'          => true,
					'suppress_filters'       => true,
					'update_post_meta_cache' => false,
					'update_post_term_cache' => false,
				);
				$slug_query = $query;
				$slug_query['name'] = $page_slug;
				$slug_matches = get_posts( $slug_query );
				$marker_query = $query;
				$marker_query['meta_query'] = array(
					'relation' => 'AND',
					array(
						'key'     => '_nadlan_private_unit_journey',
						'value'   => 'private-unit-journey-v2',
						'compare' => '=',
					),
					array(
						'key'     => '_nadlan_flagship_source_post_id',
						'value'   => (string) $source_post_id,
						'compare' => '=',
					),
				);
				$marker_matches = get_posts( $marker_query );
				return
					is_array( $slug_matches )
					&& empty( $slug_matches )
					&& is_array( $marker_matches )
					&& empty( $marker_matches );
			};

			$stage_absence_proved = function ( $page_id ) use ( $source_post_id, $stage_scope_absent ) {
				return
					is_int( $page_id )
					&& $page_id > 0
					&& $page_id !== $source_post_id
					&& ! get_post( $page_id )
					&& $stage_scope_absent();
			};

			$restore_backup = function ( $current_state ) use (
				$run_id,
				$plugin_file,
				$target_path,
				$backup_root_expected,
				$ensure_filesystem,
				$inventory,
				$plugin_state,
				$purge_caches,
				$save_state
			) {
				if (
					empty( $current_state['backup_root'] )
					|| empty( $current_state['backup_digest'] )
					|| empty( $current_state['before_version'] )
					|| ! array_key_exists( 'before_active', $current_state )
				) {
					throw new RuntimeException( 'A verified rollback backup is unavailable.' );
				}
				$before_version = (string) $current_state['before_version'];
				$before_active  = (bool) $current_state['before_active'];
				$backup_root = wp_normalize_path( (string) $current_state['backup_root'] );
				$backup_path = $backup_root . '/nadlan-config';
				if ( $backup_root_expected !== $backup_root || ! is_dir( $backup_path ) || is_link( $backup_root ) || is_link( $backup_path ) ) {
					throw new RuntimeException( 'Rollback backup path failed exact-scope validation.' );
				}
				$backup_inventory = $inventory( $backup_path );
				if ( ! hash_equals( (string) $current_state['backup_digest'], (string) $backup_inventory['digest'] ) ) {
					throw new RuntimeException( 'Rollback backup digest changed.' );
				}
				$wp_filesystem = $ensure_filesystem();
				if ( $wp_filesystem->exists( $target_path ) && ! $wp_filesystem->delete( $target_path, true, 'd' ) ) {
					throw new RuntimeException( 'Rollback could not remove the exact plugin destination.' );
				}
				require_once ABSPATH . 'wp-admin/includes/file.php';
				$copied = copy_dir( $backup_path, $target_path );
				if ( is_wp_error( $copied ) ) {
					throw new RuntimeException( 'Rollback copy failed.' );
				}
				$restored = $inventory( $target_path );
				if ( ! hash_equals( (string) $backup_inventory['digest'], (string) $restored['digest'] ) ) {
					throw new RuntimeException( 'Rollback restoration digest mismatch.' );
				}
				require_once ABSPATH . 'wp-admin/includes/plugin.php';
				$active_after_copy = is_plugin_active( $plugin_file );
				if ( $before_active && ! $active_after_copy ) {
					$activated = activate_plugin( $plugin_file, '', false, true );
					if ( is_wp_error( $activated ) ) {
						throw new RuntimeException( 'Rollback could not restore the prior active state.' );
					}
				} elseif ( ! $before_active && $active_after_copy ) {
					deactivate_plugins( $plugin_file, true, false );
				}
				$purge_caches();
				$restored_plugin = $plugin_state();
				if (
					$before_version !== (string) $restored_plugin['version']
					|| $before_active !== (bool) $restored_plugin['active']
					|| ! hash_equals( (string) $backup_inventory['digest'], (string) $restored_plugin['inventory']['digest'] )
				) {
					throw new RuntimeException( 'Rollback did not restore the exact pre-deployment plugin state.' );
				}
				$current_state['phase']           = 'rolled_back';
				$current_state['rollback_digest'] = $restored['digest'];
				$current_state['rollback_version']= $restored_plugin['version'];
				$current_state['rollback_active'] = $restored_plugin['active'];
				return $save_state( $current_state );
			};

			if ( 'inspect' === $action ) {
				try {
					$live = $plugin_state();
				} catch ( Throwable $error ) {
					return new WP_Error( 'nadlan_release_inspect_failed', 'Exact plugin inventory failed.', array( 'status' => 500 ) );
				}
				$lock = get_option( $lock_key, array() );
				$upload_status = $upload_temp_status();
				return array(
					'run_id'       => $run_id,
					'plugin'       => $live,
					'lock_free'    => empty( $lock ),
					'lock_owned'   => is_array( $lock ) && $run_id === (string) ( isset( $lock['run_id'] ) ? $lock['run_id'] : '' ),
					'state_phase'  => isset( $state['phase'] ) ? (string) $state['phase'] : 'none',
					'target_exact' => 'nadlan-config/nadlan-config.php',
					'artifact'     => array(
						'mode'               => $artifact_mode,
						'sha256'             => $artifact_sha256,
						'archive_bytes'       => $artifact_bytes,
						'entry_count'         => $artifact_entry_count,
						'uncompressed_bytes'  => $artifact_uncompressed_bytes,
					),
					'upload_temp_absent' => $upload_status['temp_absent'],
				);
			}

			if ( 'deploy_preflight' === $action ) {
				$target_readable = false;
				$target_active   = false;
				$target_version  = '';
				$target_files    = 0;
				$target_bytes    = 0;
				try {
					$live            = $plugin_state();
					$target_readable = true;
					$target_active   = true === (bool) $live['active'];
					$target_version  = (string) $live['version'];
					$target_files    = (int) $live['inventory']['file_count'];
					$target_bytes    = (int) $live['inventory']['bytes'];
				} catch ( Throwable $error ) {
					// Return only coarse allowlisted diagnostics; never serialize the exception.
				}

				$disk_free = false;
				try {
					$disk_free = @disk_free_space( WP_CONTENT_DIR );
				} catch ( Throwable $error ) {
					// A disabled/unavailable probe is reported only as measurable=false.
				}
				$disk_probe_unavailable = false === $disk_free;
				$disk_measurable = false !== $disk_free && is_numeric( $disk_free ) && (float) $disk_free >= 0;
				$disk_free_bytes = $disk_measurable ? (int) floor( (float) $disk_free ) : null;
				$disk_required   = $target_bytes + $artifact_uncompressed_bytes + $artifact_bytes + 20 * 1024 * 1024;
				$disk_sufficient = $disk_measurable ? $disk_free_bytes >= $disk_required : null;
				$bounded_unmeasured = $disk_probe_unavailable && $disk_required <= $unmeasured_capacity_cap;
				$capacity_mode = $disk_measurable ? 'measured' : ( $bounded_unmeasured ? 'bounded_unmeasured' : 'unavailable' );
				$capacity_accepted = $disk_measurable ? true === $disk_sufficient : $bounded_unmeasured;
				$backup_root     = $backup_root_expected;
				$root_safe       = false;
				$root_writable   = false;
				$backup_absent   = false;
				$storage_scope_exact = false;
				$core_upgrade_disjoint = false;
				try {
					$scope = $storage_scope_status();
					$storage_scope_exact = true === $scope['scope_exact'];
					$core_upgrade_disjoint = true === $scope['core_upgrade_disjoint'];
					$root_safe     = true === $scope['safe'];
					$root_writable = $root_safe && true === $scope['parent_writable'];
					$backup_absent = ! @file_exists( $backup_root ) && ! @is_link( $backup_root );
				} catch ( Throwable $error ) {
					// Filesystem probe failures remain coarse false booleans.
				}
				$filesystem_available = false;
				try {
					$wp_filesystem = $ensure_filesystem();
					$filesystem_available = is_object( $wp_filesystem );
				} catch ( Throwable $error ) {
					// Boolean result only; never serialize the exception or filesystem paths.
				}
				$passed =
					$target_readable
					&& $target_active
					&& '' !== $target_version
					&& $target_files > 0
					&& $target_bytes > 0
					&& $capacity_accepted
					&& $root_safe
					&& $root_writable
					&& $backup_absent
					&& $filesystem_available;
				return array(
					'schema'     => 'nadlan-private-release-deploy-preflight/v1',
					'passed'     => $passed,
					'target'     => array(
						'readable'   => $target_readable,
						'active'     => $target_active,
						'version'    => $target_version,
						'file_count' => $target_files,
						'bytes'      => $target_bytes,
					),
					'artifact'   => array(
						'archive_bytes'      => $artifact_bytes,
						'entry_count'       => $artifact_entry_count,
						'uncompressed_bytes'=> $artifact_uncompressed_bytes,
					),
					'disk'       => array(
						'capacity_mode'      => $capacity_mode,
						'measurable'         => $disk_measurable,
						'probe_unavailable'  => $disk_probe_unavailable,
						'free_bytes'         => $disk_free_bytes,
						'required_bytes'     => $disk_required,
						'hard_cap_bytes'     => $unmeasured_capacity_cap,
						'sufficient'         => $disk_sufficient,
						'bounded_unmeasured' => $bounded_unmeasured,
					),
					'upgrade'    => array(
						'root_safe'         => $root_safe,
						'root_writable'     => $root_writable,
						'backup_path_absent'=> $backup_absent,
						'storage_scope_exact'=> $storage_scope_exact,
						'core_upgrade_disjoint'=> $core_upgrade_disjoint,
					),
					'filesystem' => array( 'available' => $filesystem_available ),
				);
			}

			if ( 'status' === $action ) {
				try {
					$live = $plugin_state();
				} catch ( Throwable $error ) {
					return new WP_Error( 'nadlan_release_status_failed', 'Exact plugin status failed.', array( 'status' => 500 ) );
				}
				$upload_status = $upload_temp_status();
				return array(
					'plugin'      => $live,
					'state_phase' => isset( $state['phase'] ) ? (string) $state['phase'] : 'none',
					'backup_ready'=> ! empty( $state['backup_digest'] ),
					'page_id'     => isset( $state['page_id'] ) ? (int) $state['page_id'] : 0,
					'upload'      => array(
						'mode'             => $artifact_mode,
						'verified'         => ! empty( $state['upload_verified'] ),
						'next_index'       => isset( $state['upload_next_index'] ) ? (int) $state['upload_next_index'] : 0,
						'total_chunks'     => isset( $state['upload_total_chunks'] ) ? (int) $state['upload_total_chunks'] : $artifact_total_chunks,
						'received_bytes'   => isset( $state['upload_received_bytes'] ) ? (int) $state['upload_received_bytes'] : 0,
						'temp_absent'      => $upload_status['temp_absent'],
						'temp_exists'      => $upload_status['temp_exists'],
						'temp_safe'        => $upload_status['temp_safe'],
						'temp_bytes'       => $upload_status['temp_bytes'],
					),
				);
			}

			if ( 'recovery_status' === $action ) {
				try {
					if ( true !== $recovery_adoption_enabled ) {
						throw new RuntimeException( 'Recovery status is disabled for this helper.' );
					}
					$live = $plugin_state();
					$lock = get_option( $lock_key, false );
					$legacy_upload = $recorded_upload_status( $legacy_upload_path );
					$legacy_backup_absent =
						! @file_exists( $legacy_backup_root )
						&& ! @file_exists( $legacy_backup_root . '/nadlan-config' )
						&& ! @is_link( $legacy_backup_root )
						&& ! @is_link( $legacy_backup_root . '/nadlan-config' );
					$current_storage_absent = ! @file_exists( $storage_root ) && ! @is_link( $storage_root );
					$stage_matches = get_posts(
						array(
							'name'                   => $page_slug,
							'post_type'              => 'nadlan_project',
							'post_status'            => array_values( get_post_stati( array(), 'names' ) ),
							'posts_per_page'         => 2,
							'fields'                 => 'ids',
							'no_found_rows'          => true,
							'suppress_filters'       => true,
							'update_post_meta_cache' => false,
							'update_post_term_cache' => false,
						)
					);
					$owned_stage_matches = get_posts(
						array(
							'post_type'              => 'nadlan_project',
							'post_status'            => array_values( get_post_stati( array(), 'names' ) ),
							'posts_per_page'         => 2,
							'fields'                 => 'ids',
							'no_found_rows'          => true,
							'suppress_filters'       => true,
							'update_post_meta_cache' => false,
							'update_post_term_cache' => false,
							'meta_query'             => array(
								'relation' => 'AND',
								array( 'key' => '_nadlan_private_unit_journey', 'value' => 'private-unit-journey-v2', 'compare' => '=' ),
								array( 'key' => '_nadlan_flagship_source_post_id', 'value' => (string) $source_post_id, 'compare' => '=' ),
							),
						)
					);
					return array(
						'schema'                  => 'nadlan-private-release-recovery-status/v1',
						'plugin'                  => $live,
						'state_phase'             => isset( $state['phase'] ) ? (string) $state['phase'] : 'none',
						'backup_ready'            => ! empty( $state['backup_digest'] ),
						'lock_owned'              => is_array( $lock ) && $run_id === (string) ( isset( $lock['run_id'] ) ? $lock['run_id'] : '' ),
						'lock_free'               => false === $lock,
						'legacy_upload_absent'    => $legacy_upload['allowed'] && $legacy_upload['temp_safe'] && $legacy_upload['temp_absent'],
						'legacy_backup_absent'    => $legacy_backup_absent,
						'current_storage_absent'  => $current_storage_absent,
						'exact_stage_match_count' => is_array( $stage_matches ) ? count( $stage_matches ) : -1,
						'owned_stage_match_count' => is_array( $owned_stage_matches ) ? count( $owned_stage_matches ) : -1,
					);
				} catch ( Throwable $error ) {
					return new WP_Error( 'nadlan_release_recovery_status_failed', 'Exact recovery status failed.', array( 'status' => 409 ) );
				}
			}

			if ( 'upload_init' === $action ) {
				if ( 'upload' !== $artifact_mode ) {
					return new WP_Error( 'nadlan_release_upload_mode_invalid', 'Chunk upload is disabled for this release.', array( 'status' => 409 ) );
				}
				$requested_bytes        = $strict_int( $request->get_param( 'expected_bytes' ) );
				$requested_entries      = $strict_int( $request->get_param( 'expected_entry_count' ) );
				$requested_uncompressed = $strict_int( $request->get_param( 'expected_uncompressed_bytes' ) );
				$requested_chunks       = $strict_int( $request->get_param( 'total_chunks' ) );
				$requested_sha256       = strtolower( (string) $request->get_param( 'expected_sha256' ) );
				if (
					$artifact_bytes !== $requested_bytes
					|| $artifact_entry_count !== $requested_entries
					|| $artifact_uncompressed_bytes !== $requested_uncompressed
					|| $artifact_total_chunks !== $requested_chunks
					|| ! hash_equals( $artifact_sha256, $requested_sha256 )
				) {
					return new WP_Error( 'nadlan_release_upload_contract_mismatch', 'Upload contract differs from the embedded artifact.', array( 'status' => 409 ) );
				}
				if (
					! empty( $state )
					&& (
						! $upload_state_valid( $state )
						|| ! in_array( isset( $state['phase'] ) ? $state['phase'] : '', array( 'uploading', 'upload_verified' ), true )
					)
				) {
					return new WP_Error( 'nadlan_release_upload_state_collision', 'Existing release state cannot be mutated by upload initialization.', array( 'status' => 409 ) );
				}
				if ( ! $acquire_lock() ) {
					return new WP_Error( 'nadlan_release_locked', 'Another release owns the deployment lock.', array( 'status' => 409 ) );
				}
				try {
					if ( $upload_state_valid( $state ) ) {
						$status   = $upload_temp_status();
						$received = (int) ( isset( $state['upload_received_bytes'] ) ? $state['upload_received_bytes'] : 0 );
						$next     = (int) ( isset( $state['upload_next_index'] ) ? $state['upload_next_index'] : 0 );
						$expected_received = min( $artifact_bytes, $next * $upload_chunk_bytes );
						$consistent =
							$status['temp_safe']
							&& $status['temp_exists']
							&& $status['temp_bytes'] === $received
							&& $received >= 0
							&& $received <= $artifact_bytes
							&& $received === $expected_received
							&& $next >= 0
							&& $next <= $artifact_total_chunks;
						if ( $consistent ) {
							return array(
								'idempotent'     => true,
								'verified'       => 'upload_verified' === $state['phase'] && ! empty( $state['upload_verified'] ),
								'next_index'     => $next,
								'total_chunks'   => $artifact_total_chunks,
								'chunk_bytes_max' => $upload_chunk_bytes,
								'received_bytes' => $received,
								'expected_bytes' => $artifact_bytes,
							);
						}
						if ( 'upload_verified' === $state['phase'] ) {
							throw new RuntimeException( 'A verified upload changed before deployment.' );
						}
					}

					$prepare_upload_root();
					$state = $save_state( array(
						'phase'                              => 'uploading',
						'artifact_mode'                      => 'upload',
						'upload_path'                        => $upload_path,
						'upload_expected_sha256'             => $artifact_sha256,
						'upload_expected_bytes'              => $artifact_bytes,
						'upload_expected_entries'            => $artifact_entry_count,
						'upload_expected_uncompressed_bytes' => $artifact_uncompressed_bytes,
						'upload_chunk_bytes'                 => $upload_chunk_bytes,
						'upload_total_chunks'                => $artifact_total_chunks,
						'upload_next_index'                  => 0,
						'upload_received_bytes'              => 0,
						'upload_verified'                    => false,
					) );
					return array(
						'idempotent'     => false,
						'verified'       => false,
						'next_index'     => 0,
						'total_chunks'   => $artifact_total_chunks,
						'chunk_bytes_max'=> $upload_chunk_bytes,
						'received_bytes' => 0,
						'expected_bytes' => $artifact_bytes,
					);
				} catch ( Throwable $error ) {
					$cleanup_upload_temp();
					$release_lock();
					return new WP_Error( 'nadlan_release_upload_init_failed', 'Run-scoped upload initialization failed.', array( 'status' => 500 ) );
				}
			}

			if ( 'upload_chunk' === $action ) {
				if ( 'upload' !== $artifact_mode || ! $upload_state_valid( $state ) || 'uploading' !== $state['phase'] ) {
					return new WP_Error( 'nadlan_release_upload_state_invalid', 'Upload is not ready for a chunk.', array( 'status' => 409 ) );
				}
				if ( ! $acquire_lock() ) {
					return new WP_Error( 'nadlan_release_locked', 'Another release owns the deployment lock.', array( 'status' => 409 ) );
				}
				$index   = $strict_int( $request->get_param( 'index' ), true );
				$encoded = (string) $request->get_param( 'chunk_b64' );
				$max_encoded_bytes = 4 * (int) ceil( $upload_chunk_bytes / 3 );
				if (
					null === $index
					|| '' === $encoded
					|| strlen( $encoded ) > $max_encoded_bytes
					|| 1 !== preg_match( '/^[A-Za-z0-9+\\/]*={0,2}$/D', $encoded )
				) {
					return new WP_Error( 'nadlan_release_upload_chunk_invalid', 'Upload chunk encoding or index is invalid.', array( 'status' => 400 ) );
				}
				$decoded = base64_decode( $encoded, true );
				if ( false === $decoded || ! hash_equals( $encoded, base64_encode( $decoded ) ) ) {
					return new WP_Error( 'nadlan_release_upload_chunk_invalid', 'Upload chunk is not canonical base64.', array( 'status' => 400 ) );
				}
				$decoded_bytes = strlen( $decoded );
				$chunk_sha256  = hash( 'sha256', $decoded );
				$next_index    = (int) $state['upload_next_index'];
				$received      = (int) $state['upload_received_bytes'];
				if ( $index === $next_index - 1 ) {
					$duplicate_valid =
						$index >= 0
						&& $index === (int) ( isset( $state['upload_last_index'] ) ? $state['upload_last_index'] : -1 )
						&& $decoded_bytes === (int) ( isset( $state['upload_last_bytes'] ) ? $state['upload_last_bytes'] : -1 )
						&& hash_equals( (string) ( isset( $state['upload_last_sha256'] ) ? $state['upload_last_sha256'] : '' ), $chunk_sha256 );
					if ( $duplicate_valid ) {
						return array(
							'idempotent'     => true,
							'accepted_index' => $index,
							'chunk_bytes'    => $decoded_bytes,
							'chunk_sha256'   => $chunk_sha256,
							'next_index'     => $next_index,
							'total_chunks'   => $artifact_total_chunks,
							'received_bytes' => $received,
						);
					}
				}
				$expected_chunk_bytes = min( $upload_chunk_bytes, $artifact_bytes - $received );
				if (
					$index !== $next_index
					|| $index >= $artifact_total_chunks
					|| $expected_chunk_bytes <= 0
					|| $decoded_bytes !== $expected_chunk_bytes
				) {
					return new WP_Error( 'nadlan_release_upload_sequence_invalid', 'Upload chunk is out of sequence or has an unexpected size.', array( 'status' => 409 ) );
				}
				$status = $upload_temp_status();
				if ( ! $status['temp_safe'] || ! $status['temp_exists'] || $status['temp_bytes'] !== $received ) {
					return new WP_Error( 'nadlan_release_upload_drift', 'Upload file differs from its recorded state.', array( 'status' => 409 ) );
				}
				try {
					$handle = @fopen( $upload_path, 'ab' );
					if ( false === $handle || ! @flock( $handle, LOCK_EX ) ) {
						throw new RuntimeException( 'Upload file could not be locked.' );
					}
					$stat = fstat( $handle );
					if ( ! is_array( $stat ) || (int) $stat['size'] !== $received ) {
						throw new RuntimeException( 'Upload file changed while acquiring its lock.' );
					}
					$offset = 0;
					while ( $offset < $decoded_bytes ) {
						$written = @fwrite( $handle, substr( $decoded, $offset ) );
						if ( false === $written || $written < 1 ) {
							throw new RuntimeException( 'Upload chunk append failed.' );
						}
						$offset += $written;
					}
					if ( ! @fflush( $handle ) ) {
						throw new RuntimeException( 'Upload chunk flush failed.' );
					}
				} catch ( Throwable $error ) {
					if ( isset( $handle ) && is_resource( $handle ) ) {
						@flock( $handle, LOCK_UN );
						@fclose( $handle );
					}
					return new WP_Error( 'nadlan_release_upload_write_failed', 'Upload chunk could not be appended safely.', array( 'status' => 500 ) );
				}
				@flock( $handle, LOCK_UN );
				@fclose( $handle );
				$received += $decoded_bytes;
				clearstatcache( true, $upload_path );
				if ( ! is_file( $upload_path ) || is_link( $upload_path ) || (int) @filesize( $upload_path ) !== $received ) {
					return new WP_Error( 'nadlan_release_upload_write_drift', 'Upload chunk append could not be verified.', array( 'status' => 500 ) );
				}
				$state['upload_last_index']    = $index;
				$state['upload_last_bytes']    = $decoded_bytes;
				$state['upload_last_sha256']   = $chunk_sha256;
				$state['upload_next_index']    = $index + 1;
				$state['upload_received_bytes']= $received;
				try {
					$state = $save_state( $state );
				} catch ( Throwable $error ) {
					return new WP_Error( 'nadlan_release_upload_state_failed', 'Upload chunk state could not be persisted.', array( 'status' => 500 ) );
				}
				return array(
					'idempotent'     => false,
					'accepted_index' => $index,
					'chunk_bytes'    => $decoded_bytes,
					'chunk_sha256'   => $chunk_sha256,
					'next_index'     => $index + 1,
					'total_chunks'   => $artifact_total_chunks,
					'received_bytes' => $received,
				);
			}

			if ( 'upload_finish' === $action ) {
				if (
					'upload' !== $artifact_mode
					|| ! $upload_state_valid( $state )
					|| ! in_array( $state['phase'], array( 'uploading', 'upload_verified' ), true )
				) {
					return new WP_Error( 'nadlan_release_upload_state_invalid', 'Upload is not ready for verification.', array( 'status' => 409 ) );
				}
				if ( ! $acquire_lock() ) {
					return new WP_Error( 'nadlan_release_locked', 'Another release owns the deployment lock.', array( 'status' => 409 ) );
				}
				try {
					$status = $upload_temp_status();
					if (
						! $status['temp_safe']
						|| ! $status['temp_exists']
						|| $status['temp_bytes'] !== $artifact_bytes
						|| (int) $state['upload_received_bytes'] !== $artifact_bytes
						|| (int) $state['upload_next_index'] !== $artifact_total_chunks
					) {
						throw new RuntimeException( 'Completed upload size or sequence is invalid.' );
					}
					$observed_sha256 = @hash_file( 'sha256', $upload_path );
					if ( false === $observed_sha256 || ! hash_equals( $artifact_sha256, $observed_sha256 ) ) {
						throw new RuntimeException( 'Completed upload SHA-256 mismatch.' );
					}
					$zip_proof = $validate_zip( $upload_path );
					if (
						$artifact_bytes !== (int) $zip_proof['archive_bytes']
						|| $artifact_entry_count !== (int) $zip_proof['entry_count']
						|| $artifact_uncompressed_bytes !== (int) $zip_proof['uncompressed_bytes']
					) {
						throw new RuntimeException( 'Completed upload ZIP contract mismatch.' );
					}
					$idempotent = 'upload_verified' === $state['phase'] && ! empty( $state['upload_verified'] );
					$state['phase']                 = 'upload_verified';
					$state['upload_verified']       = true;
					$state['upload_archive_sha256'] = $observed_sha256;
					$state = $save_state( $state );
					return array(
						'idempotent'          => $idempotent,
						'verified'            => true,
						'sha256'              => $observed_sha256,
						'archive_bytes'        => (int) $zip_proof['archive_bytes'],
						'entry_count'          => (int) $zip_proof['entry_count'],
						'uncompressed_bytes'   => (int) $zip_proof['uncompressed_bytes'],
						'total_chunks'         => $artifact_total_chunks,
					);
				} catch ( Throwable $error ) {
					return new WP_Error( 'nadlan_release_upload_finish_failed', 'Completed upload failed exact artifact verification.', array( 'status' => 500 ) );
				}
			}

			if ( 'deploy' === $action ) {
				$valid_source = false;
				if ( 'url' === $artifact_mode ) {
					$url_parts = wp_parse_url( $artifact_url );
					$valid_source =
						is_array( $url_parts )
						&& 'https' === strtolower( (string) ( isset( $url_parts['scheme'] ) ? $url_parts['scheme'] : '' ) )
						&& 'raw.githubusercontent.com' === strtolower( (string) ( isset( $url_parts['host'] ) ? $url_parts['host'] : '' ) )
						&& empty( $url_parts['user'] )
						&& empty( $url_parts['pass'] )
						&& ( empty( $url_parts['port'] ) || 443 === (int) $url_parts['port'] )
						&& empty( $url_parts['query'] )
						&& empty( $url_parts['fragment'] )
						&& 1 === preg_match( '#^/The-new-ben/nad-lan-co-il/[a-f0-9]{40}/plugin-dist/nadlan-config-[A-Za-z0-9._-]+\\.zip$#', (string) ( isset( $url_parts['path'] ) ? $url_parts['path'] : '' ) );
				} elseif ( 'upload' === $artifact_mode ) {
					$upload_phase = isset( $state['phase'] ) ? (string) $state['phase'] : '';
					$valid_source =
						'' === $artifact_url
						&& $upload_state_valid( $state )
						&& ! empty( $state['upload_verified'] )
						&& $upload_path === wp_normalize_path( (string) $state['upload_path'] )
						&& (
							'upload_verified' === $upload_phase
							|| in_array( $upload_phase, array( 'deployed', 'page_ready' ), true )
						);
				}
				if ( ! $valid_source ) {
					return new WP_Error(
						'nadlan_release_artifact_identity_invalid',
						'Immutable artifact identity is invalid.',
						array(
							'status'              => 400,
							'failure_stage'       => 'request_validation',
							'failure_reason_code' => 'artifact_identity_invalid',
						)
					);
				}
				if ( ! $acquire_lock() ) {
					return new WP_Error(
						'nadlan_release_locked',
						'Another release owns the deployment lock.',
						array(
							'status'              => 409,
							'failure_stage'       => 'lock_acquisition',
							'failure_reason_code' => 'deployment_lock_unavailable',
						)
					);
				}

				if ( isset( $state['phase'] ) && in_array( $state['phase'], array( 'deployed', 'page_ready' ), true ) ) {
					try {
						$live = $plugin_state();
						$idempotent_scope = $storage_scope_status();
						$idempotent_state_exact =
							$expected_version === (string) $live['version']
							&& true === (bool) $live['active']
							&& $expected_version === (string) ( isset( $state['after_version'] ) ? $state['after_version'] : '' )
							&& 1 === preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['after_digest'] ) ? $state['after_digest'] : '' ) )
							&& hash_equals( (string) $state['after_digest'], (string) $live['inventory']['digest'] )
							&& hash_equals( $artifact_sha256, (string) ( isset( $state['artifact_sha256'] ) ? $state['artifact_sha256'] : '' ) )
							&& $backup_root_expected === wp_normalize_path( (string) ( isset( $state['backup_root'] ) ? $state['backup_root'] : '' ) )
							&& 1 === preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['backup_digest'] ) ? $state['backup_digest'] : '' ) )
							&& isset( $state['backup_files'] ) && is_int( $state['backup_files'] ) && $state['backup_files'] > 0
							&& isset( $state['backup_bytes'] ) && is_int( $state['backup_bytes'] ) && $state['backup_bytes'] > 0
							&& hash_equals( $artifact_sha256, (string) ( isset( $state['preinstall_artifact_sha256'] ) ? $state['preinstall_artifact_sha256'] : '' ) )
							&& hash_equals( (string) $state['backup_digest'], (string) ( isset( $state['preinstall_backup_digest'] ) ? $state['preinstall_backup_digest'] : '' ) )
							&& $idempotent_scope['safe']
							&& $idempotent_scope['core_upgrade_disjoint']
							&& $idempotent_scope['root_exists']
							&& @is_file( $storage_root . '/.htaccess' )
							&& @is_file( $storage_root . '/index.php' );
						if ( $idempotent_state_exact ) {
							if ( ! $cleanup_upload_temp() ) {
								return new WP_Error(
									'nadlan_release_upload_cleanup_failed',
									'Run-scoped upload temp cleanup could not be verified.',
									array(
										'status'              => 500,
										'failure_stage'       => 'idempotent_cleanup',
										'failure_reason_code' => 'artifact_cleanup_failed',
									)
								);
							}
							return array(
								'idempotent'          => true,
								'plugin'              => $live,
								'state_phase'         => $state['phase'],
								'backup_ready'        => true,
								'artifact_mode'       => $artifact_mode,
								'artifact_sha256'     => $artifact_sha256,
								'upload_temp_absent'  => true,
								'storage'             => array(
									'scope_exact'          => true,
									'core_upgrade_disjoint'=> true,
									'artifact_rehashed'    => true,
									'backup_reinventoried' => true,
									'protected_root'       => true,
								),
							);
						}
					} catch ( Throwable $error ) {
						// Fall through to the guarded deployment path.
					}
				}

				$temp_file   = '';
				$backup_root = '';
				$cleanup_deploy_temp = function () use ( &$temp_file, $cleanup_upload_temp ) {
					$clean = $cleanup_upload_temp();
					$temp_file = '';
					return $clean;
				};
				$failure_stage       = 'preflight';
				$failure_reason_code = 'plugin_state_unavailable';
				try {
					$before = $plugin_state();
					if ( ! $before['active'] ) {
						$failure_reason_code = 'plugin_inactive';
						throw new RuntimeException( 'Exact nadlan-config plugin is not active.' );
					}
					if ( ! empty( $state['backup_digest'] ) ) {
						$failure_reason_code = 'prior_backup_present';
						throw new RuntimeException( 'A prior backup already exists for this run.' );
					}

					require_once ABSPATH . 'wp-admin/includes/file.php';
					$failure_stage = 'artifact_acquisition';
					if ( 'url' === $artifact_mode ) {
						$failure_reason_code = 'artifact_download_failed';
						$download_url = add_query_arg( 'nlcb', rawurlencode( $run_id ), $artifact_url );
						$prepare_upload_root();
						$download_response = wp_safe_remote_get(
							$download_url,
							array(
								'timeout'     => 120,
								'redirection' => 0,
								'reject_unsafe_urls' => true,
								'limit_response_size' => $artifact_bytes + 1,
								'stream'      => true,
								'filename'    => $upload_path,
							)
						);
						$temp_file = $upload_path;
						if ( is_wp_error( $download_response ) || 200 !== (int) wp_remote_retrieve_response_code( $download_response ) ) {
							throw new RuntimeException( 'Immutable artifact download failed.' );
						}
						clearstatcache( true, $upload_path );
						$download_size = @filesize( $upload_path );
						if ( false === $download_size || $artifact_bytes !== (int) $download_size ) {
							$failure_stage       = 'artifact_verification';
							$failure_reason_code = 'artifact_contract_mismatch';
							throw new RuntimeException( 'Immutable artifact size differs from its embedded contract.' );
						}
					} else {
						$failure_reason_code = 'upload_path_unavailable';
						$temp_file = $upload_path;
						if ( $upload_path !== wp_normalize_path( (string) $state['upload_path'] ) || is_link( $upload_path ) || ! is_file( $upload_path ) ) {
							throw new RuntimeException( 'Recorded verified upload path is unavailable.' );
						}
					}
					$failure_stage       = 'artifact_verification';
					$failure_reason_code = 'artifact_hash_mismatch';
					$download_hash = @hash_file( 'sha256', $temp_file );
					if ( false === $download_hash || ! hash_equals( $artifact_sha256, $download_hash ) ) {
						throw new RuntimeException( 'Immutable artifact SHA-256 mismatch.' );
					}
					$failure_reason_code = 'artifact_zip_invalid';
					$zip_proof = $validate_zip( $temp_file );
					if (
						$artifact_bytes !== (int) $zip_proof['archive_bytes']
						|| $artifact_entry_count !== (int) $zip_proof['entry_count']
						|| $artifact_uncompressed_bytes !== (int) $zip_proof['uncompressed_bytes']
					) {
						$failure_reason_code = 'artifact_contract_mismatch';
						throw new RuntimeException( 'Artifact ZIP differs from its embedded entry contract.' );
					}
					$failure_stage       = 'capacity_check';
					$failure_reason_code = 'disk_space_unavailable';
					$disk_free = false;
					try {
						$disk_free = @disk_free_space( WP_CONTENT_DIR );
					} catch ( Throwable $capacity_error ) {
						// The bounded-unmeasured policy below handles an unavailable host probe.
					}
					$disk_required =
						(int) $before['inventory']['bytes']
						+ (int) $zip_proof['uncompressed_bytes']
						+ (int) $zip_proof['archive_bytes']
						+ 20 * 1024 * 1024;
					$disk_probe_unavailable = false === $disk_free;
					$disk_measurable = false !== $disk_free && is_numeric( $disk_free ) && (float) $disk_free >= 0;
					$disk_free_bytes = $disk_measurable ? (int) floor( (float) $disk_free ) : null;
					$disk_sufficient = $disk_measurable ? $disk_free_bytes >= $disk_required : null;
					$bounded_unmeasured = $disk_probe_unavailable && $disk_required <= $unmeasured_capacity_cap;
					$capacity_mode = $disk_measurable ? 'measured' : ( $bounded_unmeasured ? 'bounded_unmeasured' : 'unavailable' );
					if ( $disk_measurable && true !== $disk_sufficient ) {
						$failure_reason_code = 'disk_space_insufficient';
						throw new RuntimeException( 'Free disk space is insufficient for active, incoming, and backup plugin copies.' );
					}
					if ( ! $disk_measurable && ! $bounded_unmeasured ) {
						$failure_reason_code = $disk_probe_unavailable ? 'unmeasured_capacity_over_cap' : 'disk_space_unavailable';
						throw new RuntimeException( 'Unmeasured deployment capacity exceeds the bounded release cap.' );
					}
					$disk_proof = array(
						'capacity_mode'      => $capacity_mode,
						'measurable'         => $disk_measurable,
						'probe_unavailable'  => $disk_probe_unavailable,
						'free_bytes'         => $disk_free_bytes,
						'required_bytes'     => $disk_required,
						'hard_cap_bytes'     => $unmeasured_capacity_cap,
						'sufficient'         => $disk_sufficient,
						'bounded_unmeasured' => $bounded_unmeasured,
					);

					$failure_stage       = 'backup_prepare';
					$failure_reason_code = 'backup_destination_unsafe';
					$backup_root = $backup_root_expected;
					$backup_path = $backup_root . '/nadlan-config';
					$scope_before_backup = $storage_scope_status();
					if (
						! $scope_before_backup['safe']
						|| ! $scope_before_backup['core_upgrade_disjoint']
						|| ! $scope_before_backup['root_exists']
						|| $backup_root !== $storage_root . '/backup'
						|| file_exists( $backup_root )
						|| is_link( $backup_root )
					) {
						throw new RuntimeException( 'Scoped backup destination is not empty and exact.' );
					}
					$failure_reason_code = 'filesystem_unavailable';
					$wp_filesystem = $ensure_filesystem();
					$failure_reason_code = 'backup_root_create_failed';
					if ( ! $wp_filesystem->mkdir( $backup_root, FS_CHMOD_DIR ) ) {
						throw new RuntimeException( 'Scoped backup root could not be created.' );
					}
					$failure_reason_code = 'backup_guard_write_failed';
					$deny_written  = $wp_filesystem->put_contents( $backup_root . '/.htaccess', "Deny from all\n", FS_CHMOD_FILE );
					$index_written = $wp_filesystem->put_contents( $backup_root . '/index.php', "<?php\nhttp_response_code(404);\nexit;\n", FS_CHMOD_FILE );
					if ( ! $deny_written || ! $index_written ) {
						$wp_filesystem->delete( $backup_root, true, 'd' );
						throw new RuntimeException( 'Scoped backup access guards could not be written.' );
					}
					$failure_stage       = 'backup_copy';
					$failure_reason_code = 'plugin_backup_copy_failed';
					$copied = copy_dir( $target_path, $backup_path );
					if ( is_wp_error( $copied ) ) {
						$wp_filesystem->delete( $backup_root, true, 'd' );
						throw new RuntimeException( 'Scoped plugin backup failed.' );
					}
					$failure_stage       = 'backup_verify';
					$failure_reason_code = 'backup_inventory_failed';
					$backup_inventory = $inventory( $backup_path );
					if ( ! hash_equals( (string) $before['inventory']['digest'], (string) $backup_inventory['digest'] ) ) {
						$failure_reason_code = 'backup_digest_mismatch';
						$wp_filesystem->delete( $backup_root, true, 'd' );
						throw new RuntimeException( 'Scoped plugin backup digest mismatch.' );
					}
					$failure_reason_code = 'preinstall_storage_invariant_failed';
					$scope_before_install = $storage_scope_status();
					$artifact_real = @realpath( $temp_file );
					$backup_real = @realpath( $backup_path );
					$storage_real = @realpath( $storage_root );
					$upgrade_real = @realpath( $upgrade_root );
					if (
						! $scope_before_install['safe']
						|| ! $scope_before_install['core_upgrade_disjoint']
						|| false === $artifact_real
						|| false === $backup_real
						|| false === $storage_real
						|| wp_normalize_path( $artifact_real ) !== $upload_path
						|| 0 !== strpos( wp_normalize_path( $backup_real ) . '/', $backup_root . '/' )
						|| ( false !== $upgrade_real && 0 === strpos( wp_normalize_path( $artifact_real ) . '/', wp_normalize_path( $upgrade_real ) . '/' ) )
						|| ( false !== $upgrade_real && 0 === strpos( wp_normalize_path( $backup_real ) . '/', wp_normalize_path( $upgrade_real ) . '/' ) )
					) {
						throw new RuntimeException( 'Pre-install release storage is not disjoint from the WordPress upgrade workspace.' );
					}
					$failure_reason_code = 'preinstall_artifact_rehash_failed';
					$preinstall_hash = @hash_file( 'sha256', $temp_file );
					$preinstall_zip = $validate_zip( $temp_file );
					if (
						false === $preinstall_hash
						|| ! hash_equals( $artifact_sha256, $preinstall_hash )
						|| $artifact_bytes !== (int) $preinstall_zip['archive_bytes']
						|| $artifact_entry_count !== (int) $preinstall_zip['entry_count']
						|| $artifact_uncompressed_bytes !== (int) $preinstall_zip['uncompressed_bytes']
					) {
						throw new RuntimeException( 'Artifact changed immediately before plugin installation.' );
					}
					$failure_reason_code = 'preinstall_backup_reinventory_failed';
					$preinstall_backup = $inventory( $backup_path );
					if (
						! hash_equals( (string) $backup_inventory['digest'], (string) $preinstall_backup['digest'] )
						|| (int) $backup_inventory['file_count'] !== (int) $preinstall_backup['file_count']
						|| (int) $backup_inventory['bytes'] !== (int) $preinstall_backup['bytes']
					) {
						throw new RuntimeException( 'Backup changed immediately before plugin installation.' );
					}
					$next_state = array_merge( $state, array(
						'phase'          => 'backup_ready',
						'backup_root'    => $backup_root,
						'backup_digest'  => $backup_inventory['digest'],
						'backup_files'   => $backup_inventory['file_count'],
						'backup_bytes'   => $backup_inventory['bytes'],
						'before_version' => $before['version'],
						'before_active'  => $before['active'],
						'artifact_sha256'=> $artifact_sha256,
						'storage_scope'  => $storage_name,
						'preinstall_artifact_sha256'=> $preinstall_hash,
						'preinstall_backup_digest'=> $preinstall_backup['digest'],
					) );
					$failure_stage       = 'backup_commit';
					$failure_reason_code = 'backup_state_persist_failed';
					$state = $save_state( $next_state );

					$failure_stage       = 'plugin_install';
					$failure_reason_code = 'plugin_upgrade_failed';
					require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';
					$skin     = new Automatic_Upgrader_Skin();
					$upgrader = new Plugin_Upgrader( $skin );
					$result   = $upgrader->install( $temp_file, array( 'overwrite_package' => true, 'clear_update_cache' => true ) );
					if ( is_wp_error( $result ) || true !== $result ) {
						throw new RuntimeException( 'Plugin_Upgrader did not confirm overwrite installation.' );
					}
					$failure_stage       = 'post_install';
					$failure_reason_code = 'cache_purge_failed';
					$cache_proof = $purge_caches();
					$failure_reason_code = 'plugin_state_unavailable';
					$after = $plugin_state();
					if ( $expected_version !== $after['version'] || ! $after['active'] ) {
						$failure_reason_code = 'plugin_contract_mismatch';
						throw new RuntimeException( 'Installed plugin version or activation state is unexpected.' );
					}
					$failure_reason_code = 'postinstall_backup_reinventory_failed';
					$postinstall_backup = $inventory( $backup_path );
					if (
						! hash_equals( (string) $preinstall_backup['digest'], (string) $postinstall_backup['digest'] )
						|| (int) $preinstall_backup['file_count'] !== (int) $postinstall_backup['file_count']
						|| (int) $preinstall_backup['bytes'] !== (int) $postinstall_backup['bytes']
					) {
						throw new RuntimeException( 'Rollback backup changed during plugin installation.' );
					}
					$state['phase']         = 'deployed';
					$state['after_version'] = $after['version'];
					$state['after_digest']  = $after['inventory']['digest'];
					$failure_stage       = 'artifact_cleanup';
					$failure_reason_code = 'artifact_cleanup_failed';
					if ( ! $cleanup_deploy_temp() ) {
						throw new RuntimeException( 'Artifact temp cleanup could not be verified after installation.' );
					}
					$state['upload_temp_absent'] = true;
					$failure_stage       = 'deployment_commit';
					$failure_reason_code = 'deployment_storage_proof_failed';
					$scope_after_deploy = $storage_scope_status();
					if (
						! $scope_after_deploy['safe']
						|| ! $scope_after_deploy['core_upgrade_disjoint']
						|| ! $scope_after_deploy['root_exists']
						|| ! @is_file( $storage_root . '/.htaccess' )
						|| ! @is_file( $storage_root . '/index.php' )
					) {
						throw new RuntimeException( 'Run-scoped release storage is not exact after plugin installation.' );
					}
					$failure_reason_code = 'deployment_state_persist_failed';
					$state = $save_state( $state );
					return array(
						'idempotent'   => false,
						'plugin'       => $after,
						'zip'          => $zip_proof,
						'disk'         => $disk_proof,
						'cache'        => $cache_proof,
						'backup_ready' => true,
						'backup'       => array(
							'digest'     => $backup_inventory['digest'],
							'file_count' => $backup_inventory['file_count'],
							'bytes'      => $backup_inventory['bytes'],
						),
						'state_phase'  => 'deployed',
						'artifact_mode'=> $artifact_mode,
						'artifact_sha256'=> $artifact_sha256,
						'upload_temp_absent'=> true,
						'storage'       => array(
							'scope_exact'          => true,
							'core_upgrade_disjoint'=> true,
							'artifact_rehashed'    => true,
							'backup_reinventoried' => true,
							'protected_root'       => true,
						),
					);
				} catch ( Throwable $error ) {
					$rolled_back     = false;
					$rollback_outcome = 'not_required';
					$state           = get_option( $state_key, array() );
					if ( is_array( $state ) && ! empty( $state['backup_digest'] ) ) {
						try {
							$state            = $restore_backup( $state );
							$rolled_back      = true;
							$rollback_outcome = 'succeeded';
						} catch ( Throwable $rollback_error ) {
							$rolled_back      = false;
							$rollback_outcome = 'failed';
						}
					} elseif ( is_string( $backup_root ) && '' !== $backup_root ) {
						if ( $backup_root_expected === wp_normalize_path( $backup_root ) ) {
							try {
								$wp_filesystem = $ensure_filesystem();
								$wp_filesystem->delete( $backup_root, true, 'd' );
							} catch ( Throwable $cleanup_error ) {
								// The deployment has not started; leave the guarded backup for manual recovery.
							}
						}
					}
					$temp_absent = $cleanup_deploy_temp();
					$existence = array(
						'target_plugin'  => @is_dir( $target_path ) && @is_file( $target_path . '/nadlan-config.php' ),
						'storage_root'   => @is_dir( $storage_root ),
						'artifact_spool' => @is_file( $upload_path ),
						'backup_root'    => @is_dir( $backup_root_expected ),
						'backup_plugin'  => @is_dir( $backup_root_expected . '/nadlan-config' ),
					);
					return new WP_Error(
						'nadlan_release_deploy_failed',
						'Guarded plugin deployment failed.',
						array(
							'status'              => 500,
							'rolled_back'         => $rolled_back,
							'rollback_outcome'    => $rollback_outcome,
							'upload_temp_absent'  => $temp_absent,
							'failure_stage'       => $failure_stage,
							'failure_reason_code' => $failure_reason_code,
							'existence'           => $existence,
						)
					);
				} finally {
					$cleanup_deploy_temp();
				}
			}

			if ( 'commit_external_stage' === $action ) {
				$stage_commit_failure_stage = 'contract_validation';
				$stage_commit_failure_reason_code = 'stage_commit_disabled';
				try {
					if ( true !== $external_stage_commit_enabled || '' === $project_contract_id ) {
						throw new RuntimeException( 'External stage commit is disabled for this helper.' );
					}
					$page_id = $request->get_param( 'page_id' );
					$created_new = $request->get_param( 'created_new' );
					$post_password = (string) $request->get_param( 'post_password' );
					$meta_keys = array_keys( $external_stage_expected_meta );
					sort( $meta_keys, SORT_STRING );
					if ( ! is_int( $page_id ) || $page_id < 1 || $page_id === $source_post_id || true !== $created_new || '' === $post_password || strlen( $post_password ) > 255 ) {
						$stage_commit_failure_reason_code = 'stage_commit_request_invalid';
						throw new RuntimeException( 'External stage commit request is invalid.' );
					}
					$stage_phase = isset( $state['phase'] ) ? (string) $state['phase'] : '';
					if ( ! in_array( $stage_phase, array( 'deployed', 'page_ready' ), true ) ) {
						$stage_commit_failure_reason_code = 'stage_commit_phase_invalid';
						throw new RuntimeException( 'External stage commit requires one exact deployed state.' );
					}
					$stage_commit_failure_stage = 'lock_validation';
					$stage_commit_failure_reason_code = 'lock_not_owned';
					$stage_lock = get_option( $lock_key, false );
					if ( ! is_array( $stage_lock ) || $run_id !== (string) ( isset( $stage_lock['run_id'] ) ? $stage_lock['run_id'] : '' ) ) {
						throw new RuntimeException( 'External stage commit lock is not owned by this run.' );
					}
					$stage_commit_failure_stage = 'plugin_validation';
					$stage_commit_failure_reason_code = 'deployed_plugin_mismatch';
					$stage_live = $plugin_state();
					if (
						$expected_version !== (string) $stage_live['version']
						|| ! $stage_live['active']
						|| $expected_version !== (string) ( isset( $state['after_version'] ) ? $state['after_version'] : '' )
						|| 1 !== preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['after_digest'] ) ? $state['after_digest'] : '' ) )
						|| ! hash_equals( (string) $state['after_digest'], (string) $stage_live['inventory']['digest'] )
					) {
						throw new RuntimeException( 'External stage commit plugin state is not exact.' );
					}
					$stage_commit_failure_stage = 'stage_identity';
					$stage_commit_failure_reason_code = 'stage_identity_mismatch';
					$stage_candidate = get_post( $page_id );
					$stage_slug_matches = get_posts(
						array(
							'name'                   => $page_slug,
							'post_type'              => 'nadlan_project',
							'post_status'            => array_values( get_post_stati( array(), 'names' ) ),
							'posts_per_page'         => 2,
							'fields'                 => 'ids',
							'no_found_rows'          => true,
							'suppress_filters'       => true,
							'update_post_meta_cache' => false,
							'update_post_term_cache' => false,
						)
					);
					if (
						! $stage_candidate
						|| 'nadlan_project' !== (string) $stage_candidate->post_type
						|| $page_slug !== (string) $stage_candidate->post_name
						|| 'publish' !== (string) $stage_candidate->post_status
						|| ! hash_equals( $post_password, (string) $stage_candidate->post_password )
						|| ! hash_equals( $external_stage_title_sha256, hash( 'sha256', (string) $stage_candidate->post_title ) )
						|| ! hash_equals( $external_stage_content_sha256, hash( 'sha256', (string) $stage_candidate->post_content ) )
						|| ! hash_equals( $external_stage_excerpt_sha256, hash( 'sha256', (string) $stage_candidate->post_excerpt ) )
						|| ! is_array( $stage_slug_matches )
						|| array( $page_id ) !== array_map( 'intval', $stage_slug_matches )
					) {
						throw new RuntimeException( 'External stage identity differs from its embedded contract.' );
					}
					$stage_commit_failure_stage = 'stage_validation';
					$stage_commit_failure_reason_code = 'stage_contract_mismatch';
					$stage_lock = get_option( $lock_key, false );
					if ( ! is_array( $stage_lock ) || $run_id !== (string) ( isset( $stage_lock['run_id'] ) ? $stage_lock['run_id'] : '' ) ) {
						$stage_commit_failure_stage = 'lock_validation';
						$stage_commit_failure_reason_code = 'lock_not_owned';
						throw new RuntimeException( 'External stage commit lock changed before read-only validation.' );
					}
					$stage_snapshot = $stage_contract_snapshot( $page_id, $meta_keys );
					$provided_password_fingerprint = hash_hmac( 'sha256', $post_password, $expected_token );
					if ( ! hash_equals( $provided_password_fingerprint, (string) $stage_snapshot['password_fingerprint'] ) ) {
						$stage_commit_failure_reason_code = 'stage_password_mismatch';
						throw new RuntimeException( 'External stage password is not exact.' );
					}
					$idempotent = 'page_ready' === $stage_phase;
					if ( $idempotent ) {
						if (
							'external_committed' !== (string) ( isset( $state['page_contract_kind'] ) ? $state['page_contract_kind'] : '' )
							|| $page_id !== ( isset( $state['page_id'] ) && is_int( $state['page_id'] ) ? $state['page_id'] : 0 )
							|| $created_new !== ( isset( $state['page_created_new'] ) && is_bool( $state['page_created_new'] ) ? $state['page_created_new'] : null )
							|| $stage_snapshot['meta_keys'] !== ( isset( $state['page_meta_keys'] ) && is_array( $state['page_meta_keys'] ) ? $state['page_meta_keys'] : array() )
							|| ! hash_equals( (string) $stage_snapshot['contract_sha256'], (string) ( isset( $state['page_contract_sha256'] ) ? $state['page_contract_sha256'] : '' ) )
							|| ! hash_equals( (string) $stage_snapshot['password_fingerprint'], (string) ( isset( $state['page_password_fingerprint'] ) ? $state['page_password_fingerprint'] : '' ) )
						) {
							throw new RuntimeException( 'Idempotent external stage commit differs from recorded state.' );
						}
					} else {
						$stage_commit_failure_stage = 'state_commit';
						$stage_commit_failure_reason_code = 'stage_state_persist_failed';
						$stage_lock = get_option( $lock_key, false );
						if ( ! is_array( $stage_lock ) || $run_id !== (string) ( isset( $stage_lock['run_id'] ) ? $stage_lock['run_id'] : '' ) ) {
							$stage_commit_failure_stage = 'lock_validation';
							$stage_commit_failure_reason_code = 'lock_not_owned';
							throw new RuntimeException( 'External stage commit lock changed before state persistence.' );
						}
						$state['phase'] = 'page_ready';
						$state['page_id'] = $page_id;
						$state['page_created_new'] = $created_new;
						$state['page_contract_kind'] = 'external_committed';
						$state['page_meta_keys'] = $stage_snapshot['meta_keys'];
						$state['page_title_sha256'] = $stage_snapshot['title_sha256'];
						$state['page_content_sha256'] = $stage_snapshot['content_sha256'];
						$state['page_excerpt_sha256'] = $stage_snapshot['excerpt_sha256'];
						$state['page_core_sha256'] = $stage_snapshot['core_sha256'];
						$state['page_meta_sha256'] = $stage_snapshot['meta_sha256'];
						$state['page_password_fingerprint'] = $stage_snapshot['password_fingerprint'];
						$state['page_contract_sha256'] = $stage_snapshot['contract_sha256'];
						$state = $save_state( $state );
					}
					return array(
						'schema'                => 'nadlan-private-release-stage-commit/v1',
						'idempotent'            => $idempotent,
						'state_phase'           => 'page_ready',
						'page_id'               => $page_id,
						'created_new'           => $created_new,
						'page_contract_kind'    => 'external_committed',
						'page_contract_sha256'  => $stage_snapshot['contract_sha256'],
						'page_meta_key_count'   => count( $stage_snapshot['meta_keys'] ),
						'password_protected'    => true,
						'plugin_digest'         => $stage_live['inventory']['digest'],
					);
				} catch ( Throwable $error ) {
					return new WP_Error(
						'nadlan_release_stage_commit_failed',
						'External stage commit failed.',
						array(
							'status'              => 409,
							'failure_stage'       => $stage_commit_failure_stage,
							'failure_reason_code' => $stage_commit_failure_reason_code,
						)
					);
				}
			}

			if ( 'adopt_exact_rollback' === $action ) {
				$adoption_failure_stage = 'contract_validation';
				$adoption_failure_reason_code = 'retained_state_invalid';
				try {
					if ( true !== $recovery_adoption_enabled ) {
						$adoption_failure_reason_code = 'adoption_disabled';
						throw new RuntimeException( 'Already-original adoption is disabled for this helper.' );
					}
					$phase = isset( $state['phase'] ) ? (string) $state['phase'] : '';
					$idempotent = 'rolled_back' === $phase;
					if ( ! in_array( $phase, array( 'backup_ready', 'rolled_back' ), true ) ) {
						throw new RuntimeException( 'Already-original adoption requires an exact retained backup-ready state.' );
					}
					if (
						'upload' !== $artifact_mode
						|| ! is_array( $state )
						|| $run_id !== (string) ( isset( $state['run_id'] ) ? $state['run_id'] : '' )
						|| empty( $state['backup_root'] )
						|| empty( $state['backup_digest'] )
						|| ! isset( $state['backup_files'] )
						|| ! is_int( $state['backup_files'] )
						|| $state['backup_files'] < 1
						|| ! isset( $state['backup_bytes'] )
						|| ! is_int( $state['backup_bytes'] )
						|| $state['backup_bytes'] < 1
						|| empty( $state['before_version'] )
						|| ! array_key_exists( 'before_active', $state )
						|| ! is_bool( $state['before_active'] )
						|| empty( $state['upload_path'] )
						|| ! hash_equals( $artifact_sha256, (string) ( isset( $state['artifact_sha256'] ) ? $state['artifact_sha256'] : '' ) )
						|| 1 !== preg_match( '/^[a-f0-9]{64}$/', (string) $state['backup_digest'] )
						|| ! empty( $state['page_id'] )
						|| ! empty( $state['page_created_new'] )
						|| ! $retained_upload_state_valid( $state )
					) {
						throw new RuntimeException( 'Retained release state is incomplete or outside recovery scope.' );
					}
					$adoption_failure_stage = 'lock_validation';
					$adoption_failure_reason_code = 'lock_not_owned';
					$lock = get_option( $lock_key, false );
					if ( ! is_array( $lock ) || $run_id !== (string) ( isset( $lock['run_id'] ) ? $lock['run_id'] : '' ) ) {
						throw new RuntimeException( 'Retained release lock is not owned by this run.' );
					}
					$adoption_failure_stage = 'stage_absence';
					$adoption_failure_reason_code = 'exact_stage_present';
					$stage_matches = get_posts(
						array(
							'name'                   => $page_slug,
							'post_type'              => 'nadlan_project',
							'post_status'            => array_values( get_post_stati( array(), 'names' ) ),
							'posts_per_page'         => 2,
							'fields'                 => 'ids',
							'no_found_rows'          => true,
							'suppress_filters'       => true,
							'update_post_meta_cache' => false,
							'update_post_term_cache' => false,
						)
					);
					if ( ! is_array( $stage_matches ) || ! empty( $stage_matches ) ) {
						throw new RuntimeException( 'Exact private-stage slug is not absent.' );
					}
					$adoption_failure_reason_code = 'governed_stage_present';
					$owned_stage_matches = get_posts(
						array(
							'post_type'              => 'nadlan_project',
							'post_status'            => array_values( get_post_stati( array(), 'names' ) ),
							'posts_per_page'         => 2,
							'fields'                 => 'ids',
							'no_found_rows'          => true,
							'suppress_filters'       => true,
							'update_post_meta_cache' => false,
							'update_post_term_cache' => false,
							'meta_query'             => array(
								'relation' => 'AND',
								array( 'key' => '_nadlan_private_unit_journey', 'value' => 'private-unit-journey-v2', 'compare' => '=' ),
								array( 'key' => '_nadlan_flagship_source_post_id', 'value' => (string) $source_post_id, 'compare' => '=' ),
							),
						)
					);
					if ( ! is_array( $owned_stage_matches ) || ! empty( $owned_stage_matches ) ) {
						throw new RuntimeException( 'Governed private-stage marker is not absent.' );
					}
					$adoption_failure_stage = 'upload_absence';
					$adoption_failure_reason_code = 'upload_scope_invalid';
					$recorded_upload = $recorded_upload_status( $state['upload_path'] );
					if (
						! $recorded_upload['allowed']
						|| ! $recorded_upload['temp_safe']
						|| ! $recorded_upload['temp_absent']
						|| $recorded_upload['temp_exists']
					) {
						throw new RuntimeException( 'Recorded artifact spool is not proved safely absent.' );
					}

					$adoption_failure_stage = 'backup_validation';
					$adoption_failure_reason_code = 'backup_contract_invalid';
					$backup_root = wp_normalize_path( (string) $state['backup_root'] );
					$backup_path = $backup_root . '/nadlan-config';
					$backup_is_legacy = $legacy_backup_root === $backup_root;
					$backup_is_current = $backup_root_expected === $backup_root;
					if ( ! $backup_is_legacy && ! $backup_is_current ) {
						throw new RuntimeException( 'Recorded backup root is not an exact run-owned path.' );
					}
					clearstatcache( true, $backup_path );
					$backup_root_exists = @file_exists( $backup_root );
					$backup_path_exists = @file_exists( $backup_path );
					if ( @is_link( $backup_root ) || @is_link( $backup_path ) ) {
						throw new RuntimeException( 'Recorded backup scope contains a symbolic link.' );
					}
					if ( ! $backup_root_exists && ! $backup_path_exists ) {
						if ( ! $backup_is_legacy ) {
							throw new RuntimeException( 'Current-storage backup disappeared outside the known WordPress upgrade purge.' );
						}
						$backup_disposition = 'absent_due_core_upgrade_purge';
						$backup_inventory = array(
							'digest'     => (string) $state['backup_digest'],
							'file_count' => (int) $state['backup_files'],
							'bytes'      => (int) $state['backup_bytes'],
						);
					} else {
						if ( ! $backup_root_exists || ! $backup_path_exists || ! @is_dir( $backup_root ) || ! @is_dir( $backup_path ) ) {
							throw new RuntimeException( 'Recorded backup is only partially present.' );
						}
						$backup_inventory = $inventory( $backup_path );
						if (
							! hash_equals( (string) $state['backup_digest'], (string) $backup_inventory['digest'] )
							|| (int) $state['backup_files'] !== (int) $backup_inventory['file_count']
							|| (int) $state['backup_bytes'] !== (int) $backup_inventory['bytes']
						) {
							throw new RuntimeException( 'Present backup differs from its retained exact inventory.' );
						}
						$backup_disposition = 'present_exact';
					}

					$adoption_failure_stage = 'plugin_validation';
					$adoption_failure_reason_code = 'live_plugin_mismatch';
					$live = $plugin_state();
					if (
						(string) $state['before_version'] !== (string) $live['version']
						|| (bool) $state['before_active'] !== (bool) $live['active']
						|| ! hash_equals( (string) $state['backup_digest'], (string) $live['inventory']['digest'] )
						|| (int) $state['backup_files'] !== (int) $live['inventory']['file_count']
						|| (int) $state['backup_bytes'] !== (int) $live['inventory']['bytes']
					) {
						throw new RuntimeException( 'Live plugin is not the exact retained pre-deployment inventory.' );
					}
					if ( $idempotent ) {
						if (
							'already_original_exact/v1' !== (string) ( isset( $state['rollback_adoption_mode'] ) ? $state['rollback_adoption_mode'] : '' )
							|| true !== ( isset( $state['rollback_adopted_without_copy'] ) ? $state['rollback_adopted_without_copy'] : false )
							|| $backup_disposition !== (string) ( isset( $state['rollback_backup_disposition'] ) ? $state['rollback_backup_disposition'] : '' )
							|| ! hash_equals( (string) $live['inventory']['digest'], (string) ( isset( $state['rollback_digest'] ) ? $state['rollback_digest'] : '' ) )
							|| (string) $live['version'] !== (string) ( isset( $state['rollback_version'] ) ? $state['rollback_version'] : '' )
							|| (bool) $live['active'] !== (bool) ( isset( $state['rollback_active'] ) ? $state['rollback_active'] : null )
						) {
							throw new RuntimeException( 'Rolled-back state was not created by this exact already-original adoption.' );
						}
						$lock = get_option( $lock_key, false );
						if ( ! is_array( $lock ) || $run_id !== (string) ( isset( $lock['run_id'] ) ? $lock['run_id'] : '' ) ) {
							$adoption_failure_stage = 'lock_validation';
							$adoption_failure_reason_code = 'lock_not_owned';
							throw new RuntimeException( 'Retained release lock changed before idempotent adoption success.' );
						}
						$adoption_failure_stage = 'stage_absence';
						$adoption_failure_reason_code = 'late_stage_present';
						if ( ! $stage_scope_absent() ) {
							throw new RuntimeException( 'A private stage appeared before idempotent adoption success.' );
						}
					} else {
						$adoption_failure_stage = 'state_commit';
						$adoption_failure_reason_code = 'state_persist_failed';
						$lock = get_option( $lock_key, false );
						if ( ! is_array( $lock ) || $run_id !== (string) ( isset( $lock['run_id'] ) ? $lock['run_id'] : '' ) ) {
							$adoption_failure_stage = 'lock_validation';
							$adoption_failure_reason_code = 'lock_not_owned';
							throw new RuntimeException( 'Retained release lock changed before adoption commit.' );
						}
						$adoption_failure_stage = 'stage_absence';
						$adoption_failure_reason_code = 'late_stage_present';
						if ( ! $stage_scope_absent() ) {
							throw new RuntimeException( 'A private stage appeared before adoption state commit.' );
						}
						$adoption_failure_stage = 'state_commit';
						$adoption_failure_reason_code = 'state_persist_failed';
						$state['phase']                         = 'rolled_back';
						$state['rollback_digest']               = $live['inventory']['digest'];
						$state['rollback_version']              = $live['version'];
						$state['rollback_active']               = $live['active'];
						$state['rollback_adoption_mode']        = 'already_original_exact/v1';
						$state['rollback_adopted_without_copy'] = true;
						$state['rollback_backup_disposition']   = $backup_disposition;
						$state = $save_state( $state );
					}
					return array(
						'schema'                => 'nadlan-private-release-adopt-exact-rollback/v1',
						'idempotent'            => $idempotent,
						'adopted_without_copy'  => true,
						'rolled_back'           => true,
						'state_phase'           => 'rolled_back',
						'backup_disposition'    => $backup_disposition,
						'upload_temp_absent'    => true,
						'lock_owned'            => true,
						'plugin'                => $live,
						'before'                => array(
							'version' => (string) $state['before_version'],
							'active'  => (bool) $state['before_active'],
						),
						'rollback_digest'       => (string) $state['rollback_digest'],
						'backup'                => array(
							'digest'     => (string) $backup_inventory['digest'],
							'file_count' => (int) $backup_inventory['file_count'],
							'bytes'      => (int) $backup_inventory['bytes'],
						),
					);
				} catch ( Throwable $error ) {
					return new WP_Error(
						'nadlan_release_adopt_exact_failed',
						'Exact already-original recovery adoption failed.',
						array(
							'status'              => 409,
							'failure_stage'       => $adoption_failure_stage,
							'failure_reason_code' => $adoption_failure_reason_code,
						)
					);
				}
			}

			if ( 'rollback' === $action ) {
				$rollback_failure_stage = 'lock_validation';
				$rollback_failure_reason_code = 'lock_not_owned';
				try {
					$rollback_lock = get_option( $lock_key, false );
					if ( ! is_array( $rollback_lock ) || $run_id !== (string) ( isset( $rollback_lock['run_id'] ) ? $rollback_lock['run_id'] : '' ) ) {
						throw new RuntimeException( 'Rollback lock is not owned by this run.' );
					}
					$rollback_failure_stage = 'upload_validation';
					$rollback_failure_reason_code = 'upload_scope_invalid';
					$rollback_upload = empty( $state['upload_path'] )
						? array( 'allowed' => true, 'legacy' => false, 'temp_absent' => true, 'temp_exists' => false, 'temp_safe' => true, 'temp_bytes' => 0 )
						: $recorded_upload_status( $state['upload_path'] );
					if ( ! $rollback_upload['allowed'] || ! $rollback_upload['temp_safe'] || ( $rollback_upload['legacy'] && ! $rollback_upload['temp_absent'] ) ) {
						throw new RuntimeException( 'Rollback upload path failed exact-scope validation.' );
					}
					$was_rolled_back = isset( $state['phase'] ) && 'rolled_back' === $state['phase'];
					$page_cleanup_required =
						isset( $state['page_id'] )
						&& is_int( $state['page_id'] )
						&& $state['page_id'] > 0
						&& true === ( isset( $state['page_created_new'] ) ? $state['page_created_new'] : false );
					if ( $page_cleanup_required ) {
						$rollback_failure_stage = 'page_validation';
						$rollback_failure_reason_code = 'page_changed';
						$expected_page_contract_kind = $external_stage_commit_enabled ? 'external_committed' : 'helper_created';
						if (
							$state['page_id'] === $source_post_id
							|| $expected_page_contract_kind !== (string) ( isset( $state['page_contract_kind'] ) ? $state['page_contract_kind'] : '' )
							|| ! isset( $state['page_meta_keys'] )
							|| ! is_array( $state['page_meta_keys'] )
							|| 1 !== preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['page_title_sha256'] ) ? $state['page_title_sha256'] : '' ) )
							|| 1 !== preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['page_content_sha256'] ) ? $state['page_content_sha256'] : '' ) )
							|| 1 !== preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['page_excerpt_sha256'] ) ? $state['page_excerpt_sha256'] : '' ) )
							|| 1 !== preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['page_core_sha256'] ) ? $state['page_core_sha256'] : '' ) )
							|| 1 !== preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['page_meta_sha256'] ) ? $state['page_meta_sha256'] : '' ) )
							|| 1 !== preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['page_password_fingerprint'] ) ? $state['page_password_fingerprint'] : '' ) )
							|| 1 !== preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['page_contract_sha256'] ) ? $state['page_contract_sha256'] : '' ) )
						) {
							throw new RuntimeException( 'Rollback page contract state is incomplete.' );
						}
						$rollback_lock = get_option( $lock_key, false );
						if ( ! is_array( $rollback_lock ) || $run_id !== (string) ( isset( $rollback_lock['run_id'] ) ? $rollback_lock['run_id'] : '' ) ) {
							$rollback_failure_stage = 'lock_validation';
							$rollback_failure_reason_code = 'lock_not_owned';
							throw new RuntimeException( 'Rollback lock changed before page validation.' );
						}
						$page_id = (int) $state['page_id'];
						$page    = get_post( $page_id );
						if ( $page ) {
							if ( $was_rolled_back ) {
								$rollback_failure_reason_code = 'page_cleanup_incomplete';
								throw new RuntimeException( 'Rolled-back plugin state still has a tracked private page.' );
							}
							$page_contract_now = $stage_contract_snapshot( $page_id, $state['page_meta_keys'] );
							if (
								! hash_equals( (string) $state['page_title_sha256'], (string) $page_contract_now['title_sha256'] )
								|| ! hash_equals( (string) $state['page_content_sha256'], (string) $page_contract_now['content_sha256'] )
								|| ! hash_equals( (string) $state['page_excerpt_sha256'], (string) $page_contract_now['excerpt_sha256'] )
								|| ! hash_equals( (string) $state['page_core_sha256'], (string) $page_contract_now['core_sha256'] )
								|| ! hash_equals( (string) $state['page_meta_sha256'], (string) $page_contract_now['meta_sha256'] )
								|| ! hash_equals( (string) $state['page_password_fingerprint'], (string) $page_contract_now['password_fingerprint'] )
								|| ! hash_equals( (string) $state['page_contract_sha256'], (string) $page_contract_now['contract_sha256'] )
							) {
								throw new RuntimeException( 'Rollback refused a changed exact page contract.' );
							}
							$rollback_lock = get_option( $lock_key, false );
							if ( ! is_array( $rollback_lock ) || $run_id !== (string) ( isset( $rollback_lock['run_id'] ) ? $rollback_lock['run_id'] : '' ) ) {
								$rollback_failure_stage = 'lock_validation';
								$rollback_failure_reason_code = 'lock_not_owned';
								throw new RuntimeException( 'Rollback lock changed before exact page deletion.' );
							}
							$rollback_failure_stage = 'page_cleanup';
							$rollback_failure_reason_code = 'page_delete_failed';
							$deleted = wp_delete_post( $page_id, true );
							if ( ! $deleted ) {
								throw new RuntimeException( 'Rollback could not delete the exact tracked private page.' );
							}
						}
						clean_post_cache( $page_id );
						$rollback_failure_reason_code = 'page_absence_unproved';
						if ( ! $stage_absence_proved( $page_id ) ) {
							throw new RuntimeException( 'Rollback could not prove tracked ID, exact slug, and governed marker absence.' );
						}
						if ( true !== ( isset( $state['page_deleted'] ) ? $state['page_deleted'] : false ) ) {
							$rollback_lock = get_option( $lock_key, false );
							if ( ! is_array( $rollback_lock ) || $run_id !== (string) ( isset( $rollback_lock['run_id'] ) ? $rollback_lock['run_id'] : '' ) ) {
								$rollback_failure_stage = 'lock_validation';
								$rollback_failure_reason_code = 'lock_not_owned';
								throw new RuntimeException( 'Rollback lock changed before page-deletion state commit.' );
							}
							$rollback_failure_stage = 'page_state_commit';
							$rollback_failure_reason_code = 'page_state_persist_failed';
							$state['page_deleted'] = true;
							$state = $save_state( $state );
						}
					}
					if ( ! $was_rolled_back ) {
						$rollback_failure_stage = 'backup_restore';
						$rollback_failure_reason_code = 'backup_restore_failed';
						$rollback_lock = get_option( $lock_key, false );
						if ( ! is_array( $rollback_lock ) || $run_id !== (string) ( isset( $rollback_lock['run_id'] ) ? $rollback_lock['run_id'] : '' ) ) {
							$rollback_failure_stage = 'lock_validation';
							$rollback_failure_reason_code = 'lock_not_owned';
							throw new RuntimeException( 'Rollback lock changed before plugin restore.' );
						}
						$state = $restore_backup( $state );
					}
					$rollback_failure_stage = 'artifact_cleanup';
					$rollback_failure_reason_code = 'upload_cleanup_failed';
					$rollback_lock = get_option( $lock_key, false );
					if ( ! is_array( $rollback_lock ) || $run_id !== (string) ( isset( $rollback_lock['run_id'] ) ? $rollback_lock['run_id'] : '' ) ) {
						$rollback_failure_stage = 'lock_validation';
						$rollback_failure_reason_code = 'lock_not_owned';
						throw new RuntimeException( 'Rollback lock changed before artifact cleanup.' );
					}
					if ( ! $cleanup_upload_temp() ) {
						throw new RuntimeException( 'Rollback upload temp cleanup could not be verified.' );
					}
					$rollback_upload_after = empty( $state['upload_path'] )
						? array( 'allowed' => true, 'temp_absent' => true, 'temp_safe' => true )
						: $recorded_upload_status( $state['upload_path'] );
					if ( ! $rollback_upload_after['allowed'] || ! $rollback_upload_after['temp_safe'] || ! $rollback_upload_after['temp_absent'] ) {
						$rollback_failure_reason_code = 'upload_absence_unproved';
						throw new RuntimeException( 'Rollback recorded upload absence could not be verified.' );
					}
					$rollback_failure_stage = 'state_commit';
					$rollback_failure_reason_code = 'state_persist_failed';
					$state['upload_temp_absent'] = true;
					$state = $save_state( $state );
					$rollback_failure_stage = 'plugin_validation';
					$rollback_failure_reason_code = 'live_plugin_mismatch';
					$rollback_plugin = $plugin_state();
					if (
						empty( $state['before_version'] )
						|| ! array_key_exists( 'before_active', $state )
						|| (string) $state['before_version'] !== (string) $rollback_plugin['version']
						|| (bool) $state['before_active'] !== (bool) $rollback_plugin['active']
						|| empty( $state['rollback_digest'] )
						|| ! hash_equals( (string) $state['rollback_digest'], (string) $rollback_plugin['inventory']['digest'] )
					) {
						throw new RuntimeException( 'Rollback response could not prove exact pre-deployment state.' );
					}
					return array(
						'idempotent'          => $was_rolled_back,
						'rolled_back'         => true,
						'plugin'              => $rollback_plugin,
						'before'              => array(
							'version' => (string) $state['before_version'],
							'active'  => (bool) $state['before_active'],
						),
						'rollback_digest'     => (string) $state['rollback_digest'],
						'upload_temp_absent'  => true,
						'page_deleted'        => ! $page_cleanup_required || true === ( isset( $state['page_deleted'] ) ? $state['page_deleted'] : false ),
					);
				} catch ( Throwable $error ) {
					return new WP_Error(
						'nadlan_release_rollback_failed',
						'Exact backup rollback failed.',
						array(
							'status'              => 500,
							'failure_stage'       => $rollback_failure_stage,
							'failure_reason_code' => $rollback_failure_reason_code,
						)
					);
				}
			}

			if ( 'create_page' === $action ) {
				if ( ! current_user_can( 'publish_posts' ) ) {
					return new WP_Error( 'nadlan_release_publish_forbidden', 'Current user cannot publish the private sandbox.', array( 'status' => 403 ) );
				}
				$password = (string) $request->get_param( 'post_password' );
				if ( '' === $password || strlen( $password ) > 255 ) {
					return new WP_Error( 'nadlan_release_password_required', 'A non-empty sandbox password is required.', array( 'status' => 400 ) );
				}
				try {
					$live = $plugin_state();
					if ( $expected_version !== $live['version'] || ! in_array( isset( $state['phase'] ) ? $state['phase'] : '', array( 'deployed', 'page_ready' ), true ) ) {
						throw new RuntimeException( 'Expected release is not stable before page creation.' );
					}
					$source = get_post( $source_post_id );
					if ( ! $source || 'nadlan_project' !== $source->post_type ) {
						throw new RuntimeException( 'Exact source project 6201 is unavailable.' );
					}
					// Explicit, sanitized showroom-only clone contract. It deliberately
					// excludes SEO/canonical, language/relationship, paid-placement/featured,
					// thumbnail, ownership, and arbitrary third-party metadata.
					$sanitize_panoramas = function ( $raw ) {
						$decoded = json_decode( trim( (string) wp_unslash( $raw ) ), true );
						if ( ! is_array( $decoded ) ) {
							return '';
						}
						$clean = array();
						foreach ( array_slice( $decoded, 0, 24 ) as $item ) {
							if ( is_string( $item ) ) {
								$url = esc_url_raw( $item );
								if ( '' !== $url ) {
									$clean[] = $url;
								}
								continue;
							}
							if ( ! is_array( $item ) ) {
								continue;
							}
							$url = esc_url_raw( (string) ( isset( $item['url'] ) ? $item['url'] : ( isset( $item['image'] ) ? $item['image'] : '' ) ) );
							if ( '' === $url ) {
								continue;
							}
							$clean[] = array(
								'url'   => $url,
								'title' => sanitize_text_field( (string) ( isset( $item['title'] ) ? $item['title'] : '' ) ),
							);
						}
						return $clean ? wp_json_encode( $clean, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) : '';
					};
					$sanitize_facades = function ( $raw ) {
						$decoded = json_decode( trim( (string) wp_unslash( $raw ) ), true );
						$clean   = is_array( $decoded ) && function_exists( 'nadlan_p3d_clean_facade_images' )
							? nadlan_p3d_clean_facade_images( $decoded )
							: array();
						return $clean ? wp_json_encode( $clean, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) : '';
					};
					$sanitize_polygons = function ( $raw ) {
						$decoded = json_decode( trim( (string) wp_unslash( $raw ) ), true );
						$clean   = is_array( $decoded ) && function_exists( 'nadlan_p3d_clean_site_plan_polygons' )
							? nadlan_p3d_clean_site_plan_polygons( $decoded )
							: array();
						return $clean ? wp_json_encode( $clean, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) : '';
					};
					$showroom_meta_schema = array(
						'project_3d_image'                      => 'esc_url_raw',
						'project_3d_viewbox'                    => 'sanitize_text_field',
						'project_3d_floor_height_m'             => 'nadlan_p3d_sanitize_decimal',
						'project_3d_ground_elevation_m'         => 'nadlan_p3d_sanitize_decimal',
						'project_3d_avg_price_per_sqm'          => 'nadlan_p3d_sanitize_decimal',
						'project_3d_price_source_note'          => 'sanitize_text_field',
						'project_3d_model_type'                 => 'nadlan_p3d_sanitize_model_type',
						'project_model_glb'                     => 'esc_url_raw',
						'project_model_usdz'                    => 'esc_url_raw',
						'project_model_poster'                  => 'esc_url_raw',
						'project_default_interior'              => 'esc_url_raw',
						'project_3d_camera_lock'                => 'nadlan_p3d_sanitize_camera_lock',
						'project_3d_camera_min_polar'           => 'nadlan_p3d_sanitize_degree',
						'project_3d_camera_max_polar'           => 'nadlan_p3d_sanitize_degree',
						'project_3d_camera_auto_rotate'         => 'nadlan_p3d_sanitize_checkbox',
						'project_3d_camera_rotation_per_second' => 'nadlan_p3d_sanitize_degree',
						'project_3d_video_url'                  => 'esc_url_raw',
						'project_3d_tour_url'                   => 'esc_url_raw',
						'project_3d_cesium_tiles_url'           => 'esc_url_raw',
						'project_3d_drawings_json'              => 'nadlan_p3d_sanitize_material_json',
						'project_3d_environment_json'           => 'nadlan_p3d_sanitize_material_json',
						'project_3d_facade_images'              => $sanitize_facades,
						'project_3d_site_plan_image'            => 'esc_url_raw',
						'project_3d_site_plan_polygons'         => $sanitize_polygons,
						'project_3d_units'                      => 'nadlan_p3d_sanitize_units_json',
						'project_3d_demo'                       => 'nadlan_p3d_sanitize_checkbox',
						'project_interior_panoramas'            => $sanitize_panoramas,
						'project_floors'                        => 'absint',
						'project_subtitle'                      => 'sanitize_text_field',
						'building'                             => 'sanitize_text_field',
						'lat'                                  => 'nadlan_p3d_sanitize_decimal',
						'lng'                                  => 'nadlan_p3d_sanitize_decimal',
						'geo_confidence'                       => 'sanitize_key',
					);
					$expected_meta = array();
					foreach ( $showroom_meta_schema as $meta_key => $sanitize_callback ) {
						if ( ! is_callable( $sanitize_callback ) ) {
							throw new RuntimeException( 'A required showroom metadata sanitizer is unavailable.' );
						}
						if ( metadata_exists( 'post', $source_post_id, $meta_key ) ) {
							$expected_meta[ $meta_key ] = call_user_func( $sanitize_callback, get_post_meta( $source_post_id, $meta_key, true ) );
						}
					}
					/* The source is itself an administrative sandbox whose post title is
					 * Hebrew and begins with [SANDBOX]. Keep that operational title out
					 * of every buyer-facing locale. */
					$source_project_name = sanitize_text_field( (string) $project_display_name );
					if ( '' === $source_project_name ) {
						throw new RuntimeException( 'Project display name is unavailable after sanitization.' );
					}
					$surface_meta = array(
						'_nadlan_private_unit_journey'              => 'private-unit-journey-v2',
						'_nadlan_flagship_source_post_id'            => $source_post_id,
						'_nadlan_private_unit_journey_project_name' => $source_project_name,
						'nl_unit_scene_v2'                          => 'on',
						'nl_unit_scene'                             => 'off',
					);
					$sandbox_author_id = (int) get_current_user_id();

					$page_matches_expected = function ( $candidate ) use (
						$page_slug,
						$page_title,
						$password,
						$source,
						$sandbox_author_id,
						$expected_meta,
						$surface_meta
					) {
						if (
							! $candidate
							|| 'nadlan_project' !== (string) $candidate->post_type
							|| $page_slug !== (string) $candidate->post_name
							|| $page_title !== (string) $candidate->post_title
							|| 'publish' !== (string) $candidate->post_status
							|| $password !== (string) $candidate->post_password
							|| (string) $source->post_content !== (string) $candidate->post_content
							|| (string) $source->post_excerpt !== (string) $candidate->post_excerpt
							|| $sandbox_author_id !== (int) $candidate->post_author
							|| 0 !== (int) $candidate->post_parent
							|| 'closed' !== (string) $candidate->comment_status
							|| 'closed' !== (string) $candidate->ping_status
						) {
							return false;
						}
						$all_meta     = get_post_meta( (int) $candidate->ID );
						$allowed_keys = array_merge( array_keys( $expected_meta ), array_keys( $surface_meta ) );
						foreach ( array_keys( $all_meta ) as $observed_key ) {
							if ( ! in_array( $observed_key, $allowed_keys, true ) ) {
								return false;
							}
						}
						foreach ( array_merge( $expected_meta, $surface_meta ) as $meta_key => $expected_value ) {
							$values = isset( $all_meta[ $meta_key ] ) ? (array) $all_meta[ $meta_key ] : array();
							if ( 1 !== count( $values ) || (string) $expected_value !== (string) maybe_unserialize( $values[0] ) ) {
								return false;
							}
						}
						$taxonomies = get_object_taxonomies( 'nadlan_project' );
						$term_ids   = empty( $taxonomies ) ? array() : wp_get_object_terms( (int) $candidate->ID, $taxonomies, array( 'fields' => 'ids' ) );
						return ! is_wp_error( $term_ids ) && empty( $term_ids );
					};
					$page_meta_keys = array_keys( array_merge( $expected_meta, $surface_meta ) );
					sort( $page_meta_keys, SORT_STRING );

					$existing = get_page_by_path( $page_slug, OBJECT, 'nadlan_project' );
					$created  = false;
					if ( $existing ) {
						if ( ! $page_matches_expected( $existing ) ) {
							return new WP_Error( 'nadlan_release_slug_collision', 'Private sandbox slug is not the exact expected protected v2 object; no mutation was performed.', array( 'status' => 409 ) );
						}
						$page_id = (int) $existing->ID;
					} else {
						$page_id = wp_insert_post( wp_slash( array(
							'post_type'      => 'nadlan_project',
							'post_status'    => 'draft',
							'post_name'      => $page_slug,
							'post_title'     => $page_title,
							'post_content'   => $source->post_content,
							'post_excerpt'   => $source->post_excerpt,
							'post_author'    => $sandbox_author_id,
							'post_parent'    => 0,
							'comment_status' => 'closed',
							'ping_status'    => 'closed',
							'post_password'  => $password,
						) ), true );
						if ( is_wp_error( $page_id ) ) {
							throw new RuntimeException( 'Private sandbox post creation failed.' );
						}
						$page_id = (int) $page_id;
						$created = true;
						$state['phase']            = 'page_creating';
						$state['page_id']          = $page_id;
						$state['page_created_new'] = true;
						$state = $save_state( $state );
						foreach ( array_merge( $expected_meta, $surface_meta ) as $meta_key => $meta_value ) {
							if ( ! add_post_meta( $page_id, $meta_key, $meta_value, true ) ) {
								throw new RuntimeException( 'Sanitized showroom metadata could not be cloned exactly.' );
							}
						}
						$published = wp_update_post( array( 'ID' => $page_id, 'post_status' => 'publish' ), true );
						if ( is_wp_error( $published ) ) {
							throw new RuntimeException( 'Private sandbox could not be published after protection was applied.' );
						}
						$page = get_post( $page_id );
						if ( ! $page_matches_expected( $page ) ) {
							throw new RuntimeException( 'Created private sandbox differs from its exact protected v2 contract.' );
						}
					}
					clean_post_cache( $page_id );
					$page = get_post( $page_id );
					if ( ! $page || '' === (string) $page->post_password ) {
						throw new RuntimeException( 'Private sandbox password verification failed.' );
					}
					$page_url = get_permalink( $page_id );
					if ( ! is_string( $page_url ) || '' === $page_url ) {
						throw new RuntimeException( 'Private sandbox permalink is unavailable.' );
					}
					$page_contract = $stage_contract_snapshot( $page_id, $page_meta_keys );
					$state['phase']            = 'page_ready';
					$state['page_id']          = $page_id;
					$state['page_created_new'] = $created;
					$state['page_contract_kind'] = 'helper_created';
					$state['page_meta_keys'] = $page_contract['meta_keys'];
					$state['page_title_sha256'] = $page_contract['title_sha256'];
					$state['page_content_sha256'] = $page_contract['content_sha256'];
					$state['page_excerpt_sha256'] = $page_contract['excerpt_sha256'];
					$state['page_core_sha256'] = $page_contract['core_sha256'];
					$state['page_meta_sha256'] = $page_contract['meta_sha256'];
					$state['page_password_fingerprint'] = $page_contract['password_fingerprint'];
					$state['page_contract_sha256'] = $page_contract['contract_sha256'];
					$state = $save_state( $state );
					$cache_proof = $purge_caches();
					return array(
						'page_id'            => $page_id,
						'page_url'           => $page_url,
						'created'            => $created,
						'idempotent'         => ! $created,
						'password_protected' => true,
						'noindex'            => true,
						'nofollow'           => true,
						'source_post_id'     => $source_post_id,
						'cloned_meta_keys'   => array_keys( $expected_meta ),
						'cache'              => $cache_proof,
					);
				} catch ( Throwable $error ) {
					if ( ! empty( $created ) && ! empty( $page_id ) ) {
						$page_id = (int) $page_id;
						$delete_exact_created_page = false;
						try {
							clean_post_cache( $page_id );
							$failed_page = get_post( $page_id );
							if ( $failed_page && $page_matches_expected( $failed_page ) ) {
								$failed_snapshot = $stage_contract_snapshot( $page_id, $page_meta_keys );
								clean_post_cache( $page_id );
								$failed_page_recheck = get_post( $page_id );
								$failed_snapshot_recheck = $stage_contract_snapshot( $page_id, $page_meta_keys );
								$delete_exact_created_page =
									$page_matches_expected( $failed_page_recheck )
									&& hash_equals( (string) $failed_snapshot['contract_sha256'], (string) $failed_snapshot_recheck['contract_sha256'] );
							}
						} catch ( Throwable $cleanup_error ) {
							$delete_exact_created_page = false;
						}
						if ( $delete_exact_created_page ) {
							try {
								$cleanup_lock = get_option( $lock_key, false );
								if ( ! is_array( $cleanup_lock ) || $run_id !== (string) ( isset( $cleanup_lock['run_id'] ) ? $cleanup_lock['run_id'] : '' ) ) {
									throw new RuntimeException( 'Page failure cleanup lock is not owned by this run.' );
								}
								$state['page_contract_kind'] = 'helper_created';
								$state['page_meta_keys'] = $failed_snapshot_recheck['meta_keys'];
								$state['page_title_sha256'] = $failed_snapshot_recheck['title_sha256'];
								$state['page_content_sha256'] = $failed_snapshot_recheck['content_sha256'];
								$state['page_excerpt_sha256'] = $failed_snapshot_recheck['excerpt_sha256'];
								$state['page_core_sha256'] = $failed_snapshot_recheck['core_sha256'];
								$state['page_meta_sha256'] = $failed_snapshot_recheck['meta_sha256'];
								$state['page_password_fingerprint'] = $failed_snapshot_recheck['password_fingerprint'];
								$state['page_contract_sha256'] = $failed_snapshot_recheck['contract_sha256'];
								$state = $save_state( $state );
								$cleanup_lock = get_option( $lock_key, false );
								if ( ! is_array( $cleanup_lock ) || $run_id !== (string) ( isset( $cleanup_lock['run_id'] ) ? $cleanup_lock['run_id'] : '' ) ) {
									throw new RuntimeException( 'Page failure cleanup lock changed before deletion.' );
								}
								$deleted = wp_delete_post( $page_id, true );
								if ( $deleted && $stage_absence_proved( $page_id ) ) {
									$state['page_deleted'] = true;
									$state = $save_state( $state );
								}
							} catch ( Throwable $cleanup_error ) {
								// Preserve the exact page, backup, lock, and state for authenticated recovery.
							}
						} elseif ( ! get_post( $page_id ) && $stage_absence_proved( $page_id ) ) {
							$state['page_deleted'] = true;
							$state = $save_state( $state );
						}
					}
					return new WP_Error( 'nadlan_release_page_failed', 'Private sandbox creation failed.', array( 'status' => 500 ) );
				}
			}

			if ( 'finalize' === $action ) {
				$finalize_failure_stage = 'state_validation';
				$finalize_failure_reason_code = 'terminal_state_invalid';
				$finalize_helper_retained = function () use ( $helper_id, $helper_name, $helper_sha256, $route_path ) {
					$helper_after = \Code_Snippets\get_snippet( $helper_id, false );
					return
						$helper_after
						&& $helper_id === (int) $helper_after->id
						&& $helper_name === (string) $helper_after->name
						&& 'global' === (string) $helper_after->scope
						&& true === (bool) $helper_after->active
						&& false === (bool) $helper_after->network
						&& method_exists( $helper_after, 'is_trashed' )
						&& false === $helper_after->is_trashed()
						&& hash_equals( $helper_sha256, hash( 'sha256', (string) $helper_after->code ) )
						&& false !== strpos( (string) $helper_after->code, $route_path );
				};
				$finalize_resources_absent = function () use (
					$storage_root,
					$legacy_upload_root,
					$legacy_upload_path,
					$legacy_backup_root
				) {
					return
						! @file_exists( $storage_root )
						&& ! @is_link( $storage_root )
						&& ! @file_exists( $legacy_upload_root )
						&& ! @file_exists( $legacy_upload_path )
						&& ! @is_link( $legacy_upload_root )
						&& ! @is_link( $legacy_upload_path )
						&& ! @file_exists( $legacy_backup_root )
						&& ! @file_exists( $legacy_backup_root . '/nadlan-config' )
						&& ! @is_link( $legacy_backup_root )
						&& ! @is_link( $legacy_backup_root . '/nadlan-config' );
				};
				try {
					$finalize_lock = get_option( $lock_key, false );
					if ( empty( $state ) ) {
						if ( ! $finalize_resources_absent() ) {
							$finalize_failure_reason_code = 'already_finalized_absence_unproved';
							throw new RuntimeException( 'Absent release state still has a run-owned resource.' );
						}
						if ( false !== $finalize_lock ) {
							$finalize_failure_stage = 'lock_validation';
							$finalize_failure_reason_code = 'lock_not_absent';
							throw new RuntimeException( 'Absent release state requires an already-absent lock.' );
						}
						$lock_released = true;
						$finalize_failure_stage = 'helper_retention';
						$finalize_failure_reason_code = 'helper_changed';
						if ( ! $finalize_helper_retained() ) {
							throw new RuntimeException( 'Helper retention could not be verified for idempotent finalization.' );
						}
						return array(
							'idempotent'                => true,
							'resource_cleanup_complete' => true,
							'backup_deleted'           => true,
							'storage_root_deleted'     => true,
							'lock_released'            => $lock_released,
							'state_deleted'            => true,
							'upload_temp_absent'       => true,
							'helper_retained'          => true,
							'helper_cleanup_pending'   => true,
							'helper_id'                => $helper_id,
						);
					}
					$observed_finalize_phase = isset( $state['phase'] ) ? (string) $state['phase'] : '';
					$finalize_marker = 'finalizing_cleanup_complete' === $observed_finalize_phase;
					$finalize_phase = $finalize_marker
						? (string) ( isset( $state['finalize_terminal_phase'] ) ? $state['finalize_terminal_phase'] : '' )
						: $observed_finalize_phase;
					$finalize_contract_state = $state;
					$finalize_contract_state['phase'] = $finalize_phase;
					$backup_root = wp_normalize_path( (string) ( isset( $state['backup_root'] ) ? $state['backup_root'] : '' ) );
					$expected_page_contract_kind = $external_stage_commit_enabled ? 'external_committed' : 'helper_created';
					$page_state_structurally_exact =
						'page_ready' === $finalize_phase
						&& isset( $state['page_id'] ) && is_int( $state['page_id'] ) && $state['page_id'] > 0 && $state['page_id'] !== $source_post_id
						&& isset( $state['page_created_new'] ) && is_bool( $state['page_created_new'] )
						&& $expected_page_contract_kind === (string) ( isset( $state['page_contract_kind'] ) ? $state['page_contract_kind'] : '' )
						&& isset( $state['page_meta_keys'] ) && is_array( $state['page_meta_keys'] )
						&& 1 === preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['page_title_sha256'] ) ? $state['page_title_sha256'] : '' ) )
						&& 1 === preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['page_content_sha256'] ) ? $state['page_content_sha256'] : '' ) )
						&& 1 === preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['page_excerpt_sha256'] ) ? $state['page_excerpt_sha256'] : '' ) )
						&& 1 === preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['page_core_sha256'] ) ? $state['page_core_sha256'] : '' ) )
						&& 1 === preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['page_meta_sha256'] ) ? $state['page_meta_sha256'] : '' ) )
						&& 1 === preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['page_password_fingerprint'] ) ? $state['page_password_fingerprint'] : '' ) )
						&& 1 === preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['page_contract_sha256'] ) ? $state['page_contract_sha256'] : '' ) );
					$rolled_back_page_fields_present =
						'rolled_back' === $finalize_phase
						&& (
							array_key_exists( 'page_id', $state )
							|| array_key_exists( 'page_created_new', $state )
							|| array_key_exists( 'page_deleted', $state )
							|| array_key_exists( 'page_contract_kind', $state )
							|| array_key_exists( 'page_contract_sha256', $state )
						);
					$rolled_back_page_tracked =
						$rolled_back_page_fields_present
						&& isset( $state['page_id'] )
						&& is_int( $state['page_id'] )
						&& $state['page_id'] > 0
						&& $state['page_id'] !== $source_post_id
						&& isset( $state['page_created_new'] )
						&& is_bool( $state['page_created_new'] );
					$rolled_back_created_page =
						$rolled_back_page_tracked
						&& true === ( isset( $state['page_created_new'] ) ? $state['page_created_new'] : false );
					$rolled_back_page_state_exact =
						'rolled_back' !== $finalize_phase
						|| ! $rolled_back_page_fields_present
						|| (
							$rolled_back_page_tracked
							&& (
								! $state['page_created_new']
								|| true === ( isset( $state['page_deleted'] ) ? $state['page_deleted'] : false )
							)
						);
					$state_structurally_exact =
						in_array( $finalize_phase, array( 'page_ready', 'rolled_back' ), true )
						&& (
							! $finalize_marker
							|| (
								'nadlan-private-release-finalize-marker/v1' === (string) ( isset( $state['finalize_marker_schema'] ) ? $state['finalize_marker_schema'] : '' )
								&& true === ( isset( $state['finalize_resources_absent'] ) ? $state['finalize_resources_absent'] : false )
								&& 1 === preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['finalize_live_digest'] ) ? $state['finalize_live_digest'] : '' ) )
							)
						)
						&& ( 'rolled_back' === $finalize_phase || $page_state_structurally_exact )
						&& $rolled_back_page_state_exact
						&& in_array( $backup_root, array( $backup_root_expected, $legacy_backup_root ), true )
						&& 1 === preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['backup_digest'] ) ? $state['backup_digest'] : '' ) )
						&& isset( $state['backup_files'] )
						&& is_int( $state['backup_files'] )
						&& $state['backup_files'] > 0
						&& isset( $state['backup_bytes'] )
						&& is_int( $state['backup_bytes'] )
						&& $state['backup_bytes'] > 0
						&& ! empty( $state['before_version'] )
						&& isset( $state['before_active'] )
						&& is_bool( $state['before_active'] )
						&& hash_equals( $artifact_sha256, (string) ( isset( $state['artifact_sha256'] ) ? $state['artifact_sha256'] : '' ) )
						&& ( 'upload' !== $artifact_mode || $retained_upload_state_valid( $finalize_contract_state ) );
					if ( ! $state_structurally_exact ) {
						throw new RuntimeException( 'Terminal release state is structurally incomplete.' );
					}
					$finalize_failure_stage = 'lock_validation';
					$finalize_failure_reason_code = 'lock_not_owned';
					if (
						( ! $finalize_marker && ( ! is_array( $finalize_lock ) || $run_id !== (string) ( isset( $finalize_lock['run_id'] ) ? $finalize_lock['run_id'] : '' ) ) )
						|| ( $finalize_marker && false !== $finalize_lock && ( ! is_array( $finalize_lock ) || $run_id !== (string) ( isset( $finalize_lock['run_id'] ) ? $finalize_lock['run_id'] : '' ) ) )
					) {
						throw new RuntimeException( 'Terminal release lock is not owned by this run.' );
					}
					if ( $rolled_back_created_page ) {
						$finalize_failure_stage = 'page_validation';
						$finalize_failure_reason_code = 'page_absence_unproved';
						if (
							true !== ( isset( $state['page_deleted'] ) ? $state['page_deleted'] : false )
							|| ! $stage_absence_proved( (int) $state['page_id'] )
						) {
							throw new RuntimeException( 'Rolled-back created page is not proved absent before finalization.' );
						}
					}
					if ( 'rolled_back' === $finalize_phase && $recovery_adoption_enabled && ! $stage_scope_absent() ) {
						$finalize_failure_stage = 'page_validation';
						$finalize_failure_reason_code = 'recovery_stage_present';
						throw new RuntimeException( 'Recovery finalization found an exact-slug or governed private stage.' );
					}
					$finalize_failure_stage = 'plugin_validation';
					$finalize_failure_reason_code = 'live_plugin_mismatch';
					$finalize_live = $plugin_state();
					if ( $finalize_marker && ! hash_equals( (string) $state['finalize_live_digest'], (string) $finalize_live['inventory']['digest'] ) ) {
						throw new RuntimeException( 'Finalization marker live plugin digest changed.' );
					}
					if ( 'rolled_back' === $finalize_phase ) {
						if (
							empty( $state['rollback_digest'] )
							|| ! hash_equals( (string) $state['backup_digest'], (string) $state['rollback_digest'] )
							|| ! hash_equals( (string) $state['rollback_digest'], (string) $finalize_live['inventory']['digest'] )
							|| (int) $state['backup_files'] !== (int) $finalize_live['inventory']['file_count']
							|| (int) $state['backup_bytes'] !== (int) $finalize_live['inventory']['bytes']
							|| (string) $state['before_version'] !== (string) $finalize_live['version']
							|| (bool) $state['before_active'] !== (bool) $finalize_live['active']
							|| (string) ( isset( $state['rollback_version'] ) ? $state['rollback_version'] : '' ) !== (string) $finalize_live['version']
							|| ! isset( $state['rollback_active'] )
							|| ! is_bool( $state['rollback_active'] )
							|| $state['rollback_active'] !== (bool) $finalize_live['active']
						) {
							throw new RuntimeException( 'Rolled-back state does not match the exact live plugin before finalization.' );
						}
						if (
							$recovery_adoption_enabled
							&& (
								'already_original_exact/v1' !== (string) ( isset( $state['rollback_adoption_mode'] ) ? $state['rollback_adoption_mode'] : '' )
								|| true !== ( isset( $state['rollback_adopted_without_copy'] ) ? $state['rollback_adopted_without_copy'] : false )
							)
						) {
							$finalize_failure_reason_code = 'adoption_marker_invalid';
							throw new RuntimeException( 'Recovery-enabled finalization requires an exact already-original adoption marker.' );
						}
					} elseif (
						$expected_version !== (string) $finalize_live['version']
						|| ! $finalize_live['active']
						|| $expected_version !== (string) ( isset( $state['after_version'] ) ? $state['after_version'] : '' )
						|| 1 !== preg_match( '/^[a-f0-9]{64}$/', (string) ( isset( $state['after_digest'] ) ? $state['after_digest'] : '' ) )
						|| ! hash_equals( (string) $state['after_digest'], (string) $finalize_live['inventory']['digest'] )
					) {
						throw new RuntimeException( 'Forward release is not exact before finalization.' );
					}
					if ( 'page_ready' === $finalize_phase ) {
						$finalize_failure_stage = 'page_validation';
						$finalize_failure_reason_code = 'page_contract_mismatch';
						$page_contract_now = $stage_contract_snapshot( $state['page_id'], $state['page_meta_keys'] );
						if (
							! hash_equals( (string) $state['page_title_sha256'], (string) $page_contract_now['title_sha256'] )
							|| ! hash_equals( (string) $state['page_content_sha256'], (string) $page_contract_now['content_sha256'] )
							|| ! hash_equals( (string) $state['page_excerpt_sha256'], (string) $page_contract_now['excerpt_sha256'] )
							|| ! hash_equals( (string) $state['page_core_sha256'], (string) $page_contract_now['core_sha256'] )
							|| ! hash_equals( (string) $state['page_meta_sha256'], (string) $page_contract_now['meta_sha256'] )
							|| ! hash_equals( (string) $state['page_password_fingerprint'], (string) $page_contract_now['password_fingerprint'] )
							|| ! hash_equals( (string) $state['page_contract_sha256'], (string) $page_contract_now['contract_sha256'] )
						) {
							throw new RuntimeException( 'Protected page changed after its exact terminal commit.' );
						}
					}
					if ( $finalize_marker ) {
						$finalize_failure_stage = 'marker_reconciliation';
						$finalize_failure_reason_code = 'resource_absence_unproved';
						if ( ! $finalize_resources_absent() ) {
							throw new RuntimeException( 'Finalization marker resources are not all absent.' );
						}
						$finalize_failure_stage = 'helper_retention';
						$finalize_failure_reason_code = 'helper_changed';
						if ( ! $finalize_helper_retained() ) {
							throw new RuntimeException( 'Helper retention changed during marker reconciliation.' );
						}
						if ( 'rolled_back' === $finalize_phase && $recovery_adoption_enabled && ! $stage_scope_absent() ) {
							$finalize_failure_stage = 'page_validation';
							$finalize_failure_reason_code = 'recovery_stage_present';
							throw new RuntimeException( 'Recovery finalization marker found a new exact-slug or governed private stage.' );
						}
						$lock_released = false === $finalize_lock;
						if ( ! $lock_released ) {
							$finalize_failure_stage = 'lock_cleanup';
							$finalize_failure_reason_code = 'lock_release_failed';
							$lock_released = $release_lock();
							if ( ! $lock_released ) {
								throw new RuntimeException( 'Finalization marker lock cleanup failed.' );
							}
						}
						$finalize_failure_stage = 'helper_retention';
						$finalize_failure_reason_code = 'helper_changed';
						if ( ! $finalize_helper_retained() ) {
							throw new RuntimeException( 'Helper retention changed after marker lock cleanup.' );
						}
						if ( 'rolled_back' === $finalize_phase && $recovery_adoption_enabled && ! $stage_scope_absent() ) {
							$finalize_failure_stage = 'page_validation';
							$finalize_failure_reason_code = 'recovery_stage_present';
							throw new RuntimeException( 'Recovery finalization marker found a new exact-slug or governed private stage before state cleanup.' );
						}
						$finalize_failure_stage = 'state_cleanup';
						$finalize_failure_reason_code = 'state_delete_failed';
						delete_option( $state_key );
						if ( false !== get_option( $state_key, false ) ) {
							throw new RuntimeException( 'Finalization marker state cleanup failed.' );
						}
						return array(
							'idempotent'                => true,
							'resource_cleanup_complete' => true,
							'backup_deleted'           => true,
							'storage_root_deleted'     => true,
							'lock_released'            => true,
							'state_deleted'            => true,
							'upload_temp_absent'       => true,
							'helper_retained'          => true,
							'helper_cleanup_pending'   => true,
							'helper_id'                => $helper_id,
						);
					}
					if ( 'rolled_back' === $finalize_phase && $recovery_adoption_enabled && ! $stage_scope_absent() ) {
						$finalize_failure_stage = 'page_validation';
						$finalize_failure_reason_code = 'recovery_stage_present';
						throw new RuntimeException( 'Recovery finalization found a new exact-slug or governed private stage before cleanup.' );
					}
					$finalize_failure_stage = 'artifact_cleanup';
					$finalize_failure_reason_code = 'upload_scope_invalid';
					$finalize_lock_now = get_option( $lock_key, false );
					if ( ! is_array( $finalize_lock_now ) || $run_id !== (string) ( isset( $finalize_lock_now['run_id'] ) ? $finalize_lock_now['run_id'] : '' ) ) {
						$finalize_failure_stage = 'lock_validation';
						$finalize_failure_reason_code = 'lock_not_owned';
						throw new RuntimeException( 'Release lock changed before artifact cleanup.' );
					}
					$finalize_upload = empty( $state['upload_path'] )
						? array( 'allowed' => true, 'legacy' => false, 'temp_absent' => true, 'temp_exists' => false, 'temp_safe' => true )
						: $recorded_upload_status( $state['upload_path'] );
					if ( ! $finalize_upload['allowed'] || ! $finalize_upload['temp_safe'] || ( $finalize_upload['legacy'] && ! $finalize_upload['temp_absent'] ) ) {
						throw new RuntimeException( 'Recorded upload path failed exact-scope validation.' );
					}
					$finalize_failure_reason_code = 'upload_cleanup_failed';
					if ( ! $cleanup_upload_temp() ) {
						throw new RuntimeException( 'Run-scoped upload temp cleanup could not be verified.' );
					}
					$finalize_failure_reason_code = 'upload_absence_unproved';
					$upload_status = $upload_temp_status();
					if ( ! $upload_status['temp_absent'] || ! $upload_status['temp_safe'] ) {
						throw new RuntimeException( 'Run-scoped upload temp absence proof failed.' );
					}
					$finalize_upload_after = empty( $state['upload_path'] )
						? array( 'allowed' => true, 'temp_absent' => true, 'temp_safe' => true )
						: $recorded_upload_status( $state['upload_path'] );
					if ( ! $finalize_upload_after['allowed'] || ! $finalize_upload_after['temp_safe'] || ! $finalize_upload_after['temp_absent'] ) {
						throw new RuntimeException( 'Recorded upload absence proof failed.' );
					}
					$finalize_failure_stage = 'backup_cleanup';
					$finalize_failure_reason_code = 'backup_scope_invalid';
					if ( ! in_array( $backup_root, array( $backup_root_expected, $legacy_backup_root ), true ) ) {
						throw new RuntimeException( 'Derived backup cleanup path escaped its exact scope.' );
					}
					$finalize_lock_now = get_option( $lock_key, false );
					if ( ! is_array( $finalize_lock_now ) || $run_id !== (string) ( isset( $finalize_lock_now['run_id'] ) ? $finalize_lock_now['run_id'] : '' ) ) {
						$finalize_failure_stage = 'lock_validation';
						$finalize_failure_reason_code = 'lock_not_owned';
						throw new RuntimeException( 'Release lock changed before backup cleanup.' );
					}
					$wp_filesystem = $ensure_filesystem();
					if ( is_link( $backup_root ) ) {
						$finalize_failure_reason_code = 'backup_symlink';
						throw new RuntimeException( 'Scoped backup cleanup refused a symbolic link.' );
					}
					$finalize_failure_reason_code = 'backup_delete_failed';
					if ( $wp_filesystem->exists( $backup_root ) && ! $wp_filesystem->delete( $backup_root, true, 'd' ) ) {
						throw new RuntimeException( 'Scoped backup cleanup failed.' );
					}
					$backup_deleted = ! $wp_filesystem->exists( $backup_root );
					if ( ! $backup_deleted ) {
						$finalize_failure_reason_code = 'backup_absence_unproved';
						throw new RuntimeException( 'Scoped backup absence could not be verified.' );
					}
					$finalize_failure_stage = 'storage_cleanup';
					$finalize_failure_reason_code = 'storage_scope_invalid';
					$storage_root_deleted = ! $wp_filesystem->exists( $storage_root );
					if ( ! $storage_root_deleted ) {
						if ( is_link( $storage_root ) || ! is_dir( $storage_root ) ) {
							throw new RuntimeException( 'Run-scoped release root changed before cleanup.' );
						}
						$storage_entries = @scandir( $storage_root );
						if ( false === $storage_entries ) {
							$finalize_failure_reason_code = 'storage_inventory_failed';
							throw new RuntimeException( 'Run-scoped release root could not be inventoried before cleanup.' );
						}
						$storage_entries = array_values( array_diff( $storage_entries, array( '.', '..' ) ) );
						sort( $storage_entries, SORT_STRING );
						if ( array_diff( $storage_entries, array( '.htaccess', 'index.php' ) ) ) {
							$finalize_failure_reason_code = 'storage_unexpected_child';
							throw new RuntimeException( 'Run-scoped release root contains an unexpected child.' );
						}
						$finalize_failure_reason_code = 'storage_guard_delete_failed';
						if ( in_array( 'index.php', $storage_entries, true ) && ! $wp_filesystem->delete( $storage_root . '/index.php', false, 'f' ) ) {
							throw new RuntimeException( 'Exact run-scoped release index cleanup failed.' );
						}
						if ( in_array( '.htaccess', $storage_entries, true ) && ! $wp_filesystem->delete( $storage_root . '/.htaccess', false, 'f' ) ) {
							throw new RuntimeException( 'Exact run-scoped release deny-file cleanup failed.' );
						}
						if ( ! $wp_filesystem->delete( $storage_root, false, 'd' ) ) {
							$finalize_failure_reason_code = 'storage_root_delete_failed';
							throw new RuntimeException( 'Exact run-scoped release root cleanup failed.' );
						}
						$storage_root_deleted = ! $wp_filesystem->exists( $storage_root );
					}
					if ( ! $storage_root_deleted ) {
						$finalize_failure_reason_code = 'storage_absence_unproved';
						throw new RuntimeException( 'Run-scoped release root absence could not be verified.' );
					}
					clearstatcache( true, $storage_root );
					if ( $wp_filesystem->exists( $storage_root ) || file_exists( $storage_root ) || is_link( $storage_root ) ) {
						$finalize_failure_reason_code = 'storage_absence_unproved';
						throw new RuntimeException( 'Run-scoped release root absence changed before ownership cleanup.' );
					}
					$finalize_failure_stage = 'marker_commit';
					$finalize_failure_reason_code = 'resource_absence_unproved';
					if ( ! $finalize_resources_absent() ) {
						throw new RuntimeException( 'Release resources changed before finalization marker commit.' );
					}
					if ( 'rolled_back' === $finalize_phase && $recovery_adoption_enabled && ! $stage_scope_absent() ) {
						$finalize_failure_stage = 'page_validation';
						$finalize_failure_reason_code = 'recovery_stage_present';
						throw new RuntimeException( 'Recovery finalization found a new exact-slug or governed private stage before marker commit.' );
					}
					$finalize_lock_now = get_option( $lock_key, false );
					if ( ! is_array( $finalize_lock_now ) || $run_id !== (string) ( isset( $finalize_lock_now['run_id'] ) ? $finalize_lock_now['run_id'] : '' ) ) {
						$finalize_failure_stage = 'lock_validation';
						$finalize_failure_reason_code = 'lock_not_owned';
						throw new RuntimeException( 'Release lock changed before finalization marker commit.' );
					}
					$finalize_failure_stage = 'helper_retention';
					$finalize_failure_reason_code = 'helper_changed';
					if ( ! $finalize_helper_retained() ) {
						throw new RuntimeException( 'Helper retention changed before finalization marker commit.' );
					}
					$finalize_failure_stage = 'marker_commit';
					$finalize_failure_reason_code = 'marker_persist_failed';
					$state['phase'] = 'finalizing_cleanup_complete';
					$state['finalize_marker_schema'] = 'nadlan-private-release-finalize-marker/v1';
					$state['finalize_terminal_phase'] = $finalize_phase;
					$state['finalize_resources_absent'] = true;
					$state['finalize_live_digest'] = $finalize_live['inventory']['digest'];
					$state = $save_state( $state );
					$finalize_failure_stage = 'lock_cleanup';
					$finalize_failure_reason_code = 'lock_release_failed';
					$lock_released = $release_lock();
					if ( ! $lock_released ) {
						throw new RuntimeException( 'Release lock cleanup could not be verified.' );
					}

					$finalize_failure_stage = 'helper_retention';
					$finalize_failure_reason_code = 'helper_changed';
					$helper_retained = $finalize_helper_retained();
					if ( ! $helper_retained ) {
						throw new RuntimeException( 'Helper retention could not be verified after release resource cleanup.' );
					}
					$finalize_failure_stage = 'state_cleanup';
					$finalize_failure_reason_code = 'state_delete_failed';
					delete_option( $state_key );
					if ( false !== get_option( $state_key, false ) ) {
						throw new RuntimeException( 'Release state cleanup could not be verified.' );
					}

					// Keep this authenticated route alive until every release resource has
					// been removed and verified. The driver hard-deletes this exact helper
					// only after this phase succeeds, using an independent cleanup bridge.
					return array(
						'idempotent'                => false,
						'resource_cleanup_complete' => true,
						'backup_deleted'           => $backup_deleted,
						'storage_root_deleted'     => $storage_root_deleted,
						'lock_released'            => $lock_released,
						'state_deleted'            => true,
						'upload_temp_absent'       => true,
						'helper_retained'          => true,
						'helper_cleanup_pending'   => true,
						'helper_id'                => $helper_id,
					);
				} catch ( Throwable $error ) {
					return new WP_Error(
						'nadlan_release_finalize_failed',
						'Release finalization failed.',
						array(
							'status'              => 500,
							'failure_stage'       => $finalize_failure_stage,
							'failure_reason_code' => $finalize_failure_reason_code,
						)
					);
				}
			}

			return new WP_Error( 'nadlan_release_action_invalid', 'Release action is invalid.', array( 'status' => 400 ) );
		},
	) );
} );
