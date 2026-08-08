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
			$project_display_name
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
			$upgrade_root = wp_normalize_path( WP_CONTENT_DIR . '/upgrade' );
			$state_key    = 'nadlan_unit_journey_state_' . substr( hash( 'sha256', $run_id ), 0, 16 );
			$lock_key     = 'nadlan_unit_journey_deploy_lock';
			$upload_chunk_bytes = 128 * 1024;
			$artifact_total_chunks = (int) ceil( $artifact_bytes / $upload_chunk_bytes );
			$upload_root   = $upgrade_root . '/.nadlan-unit-journey-upload-' . substr( hash( 'sha256', $run_id . '|' . $expected_token ), 0, 24 );
			$upload_path   = $upload_root . '/nadlan-config.zip';
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

			$upload_temp_status = function () use ( $upload_root, $upload_path ) {
				clearstatcache( true, $upload_path );
				$root_exists = file_exists( $upload_root );
				$file_exists = file_exists( $upload_path );
				$root_real   = $root_exists ? @realpath( $upload_root ) : false;
				$file_real   = $file_exists ? @realpath( $upload_path ) : false;
				$safe        =
					! is_link( $upload_root )
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
				$upgrade_root,
				$upload_root,
				$upload_path,
				$ensure_filesystem,
				$cleanup_upload_temp
			) {
				if ( is_link( $upgrade_root ) || is_link( $upload_root ) || is_link( $upload_path ) ) {
					throw new RuntimeException( 'Upload scope contains a symbolic link.' );
				}
				if ( ! $cleanup_upload_temp() ) {
					throw new RuntimeException( 'Prior run-scoped upload could not be removed safely.' );
				}
				$wp_filesystem = $ensure_filesystem();
				if ( ! $wp_filesystem->exists( $upgrade_root ) && ! $wp_filesystem->mkdir( $upgrade_root, FS_CHMOD_DIR ) ) {
					throw new RuntimeException( 'WordPress upgrade directory could not be created for upload.' );
				}
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
					! $deny_written
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

			$restore_backup = function ( $current_state ) use (
				$run_id,
				$plugin_file,
				$target_path,
				$upgrade_root,
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
				$allowed     = $upgrade_root . '/.nadlan-unit-journey-' . substr( hash( 'sha256', $run_id ), 0, 20 );
				if ( $allowed !== $backup_root || 0 !== strpos( $backup_root, $upgrade_root . '/' ) || ! is_dir( $backup_path ) ) {
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
					return new WP_Error( 'nadlan_release_artifact_identity_invalid', 'Immutable artifact identity is invalid.', array( 'status' => 400 ) );
				}
				if ( ! $acquire_lock() ) {
					return new WP_Error( 'nadlan_release_locked', 'Another release owns the deployment lock.', array( 'status' => 409 ) );
				}

				if ( isset( $state['phase'] ) && in_array( $state['phase'], array( 'deployed', 'page_ready' ), true ) ) {
					try {
						$live = $plugin_state();
						if ( $expected_version === $live['version'] ) {
							if ( ! $cleanup_upload_temp() ) {
								return new WP_Error( 'nadlan_release_upload_cleanup_failed', 'Run-scoped upload temp cleanup could not be verified.', array( 'status' => 500 ) );
							}
							return array(
								'idempotent'          => true,
								'plugin'              => $live,
								'state_phase'         => $state['phase'],
								'backup_ready'        => true,
								'artifact_mode'       => $artifact_mode,
								'artifact_sha256'     => $artifact_sha256,
								'upload_temp_absent'  => true,
							);
						}
					} catch ( Throwable $error ) {
						// Fall through to the guarded deployment path.
					}
				}

				$temp_file   = '';
				$backup_root = '';
				$cleanup_deploy_temp = function () use ( &$temp_file, $artifact_mode, $cleanup_upload_temp ) {
					if ( 'upload' === $artifact_mode ) {
						return $cleanup_upload_temp();
					}
					if ( is_string( $temp_file ) && '' !== $temp_file && file_exists( $temp_file ) ) {
						if ( ! @unlink( $temp_file ) ) {
							return false;
						}
					}
					$absent   = ! is_string( $temp_file ) || '' === $temp_file || ! file_exists( $temp_file );
					$temp_file = '';
					return $absent && $cleanup_upload_temp();
				};
				try {
					$before = $plugin_state();
					if ( ! $before['active'] ) {
						throw new RuntimeException( 'Exact nadlan-config plugin is not active.' );
					}
					if ( ! empty( $state['backup_digest'] ) ) {
						throw new RuntimeException( 'A prior backup already exists for this run.' );
					}

					require_once ABSPATH . 'wp-admin/includes/file.php';
					if ( 'url' === $artifact_mode ) {
						$download_url = add_query_arg( 'nlcb', rawurlencode( $run_id ), $artifact_url );
						$temp_file = download_url( $download_url, 120 );
						if ( is_wp_error( $temp_file ) ) {
							throw new RuntimeException( 'Immutable artifact download failed.' );
						}
					} else {
						$temp_file = $upload_path;
						if ( $upload_path !== wp_normalize_path( (string) $state['upload_path'] ) || is_link( $upload_path ) || ! is_file( $upload_path ) ) {
							throw new RuntimeException( 'Recorded verified upload path is unavailable.' );
						}
					}
					$download_hash = @hash_file( 'sha256', $temp_file );
					if ( false === $download_hash || ! hash_equals( $artifact_sha256, $download_hash ) ) {
						throw new RuntimeException( 'Immutable artifact SHA-256 mismatch.' );
					}
					$zip_proof = $validate_zip( $temp_file );
					if (
						$artifact_bytes !== (int) $zip_proof['archive_bytes']
						|| $artifact_entry_count !== (int) $zip_proof['entry_count']
						|| $artifact_uncompressed_bytes !== (int) $zip_proof['uncompressed_bytes']
					) {
						throw new RuntimeException( 'Artifact ZIP differs from its embedded entry contract.' );
					}
					$disk_free = disk_free_space( WP_CONTENT_DIR );
					$disk_required =
						(int) $before['inventory']['bytes']
						+ (int) $zip_proof['uncompressed_bytes']
						+ (int) $zip_proof['archive_bytes']
						+ 20 * 1024 * 1024;
					if ( false === $disk_free || $disk_free < $disk_required ) {
						throw new RuntimeException( 'Free disk space is insufficient for active, incoming, and backup plugin copies.' );
					}
					$disk_proof = array(
						'free_bytes'     => (int) $disk_free,
						'required_bytes' => $disk_required,
						'sufficient'     => true,
					);

					$backup_root = $upgrade_root . '/.nadlan-unit-journey-' . substr( hash( 'sha256', $run_id ), 0, 20 );
					$backup_path = $backup_root . '/nadlan-config';
					if ( 0 !== strpos( $backup_root, $upgrade_root . '/' ) || file_exists( $backup_root ) ) {
						throw new RuntimeException( 'Scoped backup destination is not empty and exact.' );
					}
					$wp_filesystem = $ensure_filesystem();
					if ( ! $wp_filesystem->exists( $upgrade_root ) && ! $wp_filesystem->mkdir( $upgrade_root, FS_CHMOD_DIR ) ) {
						throw new RuntimeException( 'WordPress upgrade directory could not be created.' );
					}
					if ( ! $wp_filesystem->mkdir( $backup_root, FS_CHMOD_DIR ) ) {
						throw new RuntimeException( 'Scoped backup root could not be created.' );
					}
					$deny_written  = $wp_filesystem->put_contents( $backup_root . '/.htaccess', "Deny from all\n", FS_CHMOD_FILE );
					$index_written = $wp_filesystem->put_contents( $backup_root . '/index.php', "<?php\nhttp_response_code(404);\nexit;\n", FS_CHMOD_FILE );
					if ( ! $deny_written || ! $index_written ) {
						$wp_filesystem->delete( $backup_root, true, 'd' );
						throw new RuntimeException( 'Scoped backup access guards could not be written.' );
					}
					$copied = copy_dir( $target_path, $backup_path );
					if ( is_wp_error( $copied ) ) {
						$wp_filesystem->delete( $backup_root, true, 'd' );
						throw new RuntimeException( 'Scoped plugin backup failed.' );
					}
					$backup_inventory = $inventory( $backup_path );
					if ( ! hash_equals( (string) $before['inventory']['digest'], (string) $backup_inventory['digest'] ) ) {
						$wp_filesystem->delete( $backup_root, true, 'd' );
						throw new RuntimeException( 'Scoped plugin backup digest mismatch.' );
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
					) );
					$state = $save_state( $next_state );

					require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';
					$skin     = new Automatic_Upgrader_Skin();
					$upgrader = new Plugin_Upgrader( $skin );
					$result   = $upgrader->install( $temp_file, array( 'overwrite_package' => true, 'clear_update_cache' => true ) );
					if ( is_wp_error( $result ) || true !== $result ) {
						throw new RuntimeException( 'Plugin_Upgrader did not confirm overwrite installation.' );
					}
					$cache_proof = $purge_caches();
					$after = $plugin_state();
					if ( $expected_version !== $after['version'] || ! $after['active'] ) {
						throw new RuntimeException( 'Installed plugin version or activation state is unexpected.' );
					}
					$state['phase']         = 'deployed';
					$state['after_version'] = $after['version'];
					$state['after_digest']  = $after['inventory']['digest'];
					if ( ! $cleanup_deploy_temp() ) {
						throw new RuntimeException( 'Artifact temp cleanup could not be verified after installation.' );
					}
					$state['upload_temp_absent'] = true;
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
					);
				} catch ( Throwable $error ) {
					$rolled_back = false;
					$state       = get_option( $state_key, array() );
					if ( is_array( $state ) && ! empty( $state['backup_digest'] ) ) {
						try {
							$state       = $restore_backup( $state );
							$rolled_back = true;
						} catch ( Throwable $rollback_error ) {
							$rolled_back = false;
						}
					} elseif ( is_string( $backup_root ) && '' !== $backup_root ) {
						$allowed = $upgrade_root . '/.nadlan-unit-journey-' . substr( hash( 'sha256', $run_id ), 0, 20 );
						if ( $allowed === wp_normalize_path( $backup_root ) ) {
							try {
								$wp_filesystem = $ensure_filesystem();
								$wp_filesystem->delete( $backup_root, true, 'd' );
							} catch ( Throwable $cleanup_error ) {
								// The deployment has not started; leave the guarded backup for manual recovery.
							}
						}
					}
					$temp_absent = $cleanup_deploy_temp();
					return new WP_Error(
						'nadlan_release_deploy_failed',
						'Guarded plugin deployment failed.',
						array( 'status' => 500, 'rolled_back' => $rolled_back, 'upload_temp_absent' => $temp_absent )
					);
				} finally {
					$cleanup_deploy_temp();
				}
			}

			if ( 'rollback' === $action ) {
				try {
					if (
						! empty( $state['upload_path'] )
						&& $upload_path !== wp_normalize_path( (string) $state['upload_path'] )
					) {
						throw new RuntimeException( 'Rollback upload path failed exact-scope validation.' );
					}
					$was_rolled_back = isset( $state['phase'] ) && 'rolled_back' === $state['phase'];
					if ( ! $was_rolled_back ) {
						$state = $restore_backup( $state );
					}
					if ( ! empty( $state['page_id'] ) && ! empty( $state['page_created_new'] ) ) {
						$page_id = (int) $state['page_id'];
						$page    = get_post( $page_id );
						if ( $page ) {
							if (
								'private-unit-journey-v2' !== (string) get_post_meta( $page_id, '_nadlan_private_unit_journey', true )
								|| $page_slug !== (string) $page->post_name
							) {
								throw new RuntimeException( 'Rollback refused a changed private sandbox object.' );
							}
							$deleted = wp_delete_post( $page_id, true );
							if ( ! $deleted || get_post( $page_id ) ) {
								throw new RuntimeException( 'Rollback could not prove private sandbox deletion.' );
							}
						}
						$state['page_deleted'] = true;
						$state = $save_state( $state );
					}
					if ( ! $cleanup_upload_temp() ) {
						throw new RuntimeException( 'Rollback upload temp cleanup could not be verified.' );
					}
					$state['upload_temp_absent'] = true;
					$state = $save_state( $state );
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
					);
				} catch ( Throwable $error ) {
					return new WP_Error( 'nadlan_release_rollback_failed', 'Exact backup rollback failed.', array( 'status' => 500 ) );
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
					$state['phase']            = 'page_ready';
					$state['page_id']          = $page_id;
					$state['page_created_new'] = $created;
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
						$deleted = wp_delete_post( (int) $page_id, true );
						if ( $deleted && ! get_post( (int) $page_id ) ) {
							$state['page_deleted'] = true;
							$state = $save_state( $state );
						}
					}
					return new WP_Error( 'nadlan_release_page_failed', 'Private sandbox creation failed.', array( 'status' => 500 ) );
				}
			}

			if ( 'finalize' === $action ) {
				try {
					if (
						! empty( $state['upload_path'] )
						&& $upload_path !== wp_normalize_path( (string) $state['upload_path'] )
					) {
						throw new RuntimeException( 'Recorded upload path failed exact-scope validation.' );
					}
					if ( ! $cleanup_upload_temp() ) {
						throw new RuntimeException( 'Run-scoped upload temp cleanup could not be verified.' );
					}
					$upload_status = $upload_temp_status();
					if ( ! $upload_status['temp_absent'] || ! $upload_status['temp_safe'] ) {
						throw new RuntimeException( 'Run-scoped upload temp absence proof failed.' );
					}
					$backup_root = $upgrade_root . '/.nadlan-unit-journey-' . substr( hash( 'sha256', $run_id ), 0, 20 );
					if ( ! empty( $state['backup_root'] ) ) {
						$recorded_backup_root = wp_normalize_path( (string) $state['backup_root'] );
						if ( $backup_root !== $recorded_backup_root ) {
							throw new RuntimeException( 'Backup cleanup failed exact-scope validation.' );
						}
					}
					if ( 0 !== strpos( $backup_root, $upgrade_root . '/' ) ) {
						throw new RuntimeException( 'Derived backup cleanup path escaped its exact scope.' );
					}
					$wp_filesystem = $ensure_filesystem();
					if ( $wp_filesystem->exists( $backup_root ) && ! $wp_filesystem->delete( $backup_root, true, 'd' ) ) {
						throw new RuntimeException( 'Scoped backup cleanup failed.' );
					}
					$backup_deleted = ! $wp_filesystem->exists( $backup_root );
					if ( ! $backup_deleted ) {
						throw new RuntimeException( 'Scoped backup absence could not be verified.' );
					}
					$lock_released = $release_lock();
					if ( ! $lock_released ) {
						throw new RuntimeException( 'Release lock cleanup could not be verified.' );
					}
					delete_option( $state_key );
					if ( false !== get_option( $state_key, false ) ) {
						throw new RuntimeException( 'Release state cleanup could not be verified.' );
					}

					// Keep this authenticated route alive until every release resource has
					// been removed and verified. The driver hard-deletes this exact helper
					// only after this phase succeeds, using an independent cleanup bridge.
					$helper_after = \Code_Snippets\get_snippet( $helper_id, false );
					$helper_retained =
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
					if ( ! $helper_retained ) {
						throw new RuntimeException( 'Helper retention could not be verified after release resource cleanup.' );
					}
					return array(
						'resource_cleanup_complete' => true,
						'backup_deleted'           => $backup_deleted,
						'lock_released'            => $lock_released,
						'state_deleted'            => true,
						'upload_temp_absent'       => true,
						'helper_retained'          => true,
						'helper_cleanup_pending'   => true,
						'helper_id'                => $helper_id,
					);
				} catch ( Throwable $error ) {
					return new WP_Error( 'nadlan_release_finalize_failed', 'Release finalization failed.', array( 'status' => 500 ) );
				}
			}

			return new WP_Error( 'nadlan_release_action_invalid', 'Release action is invalid.', array( 'status' => 400 ) );
		},
	) );
} );
