<?php
/**
 * Deterministic UTOPIA release migration simulation.
 *
 * This is not a WordPress replacement. It implements only the API surface used
 * by inc/utopia-sde-dov.php so the release transaction and rollback paths can be
 * exercised before the production plugin is packaged.
 */

declare(strict_types=1);

define( 'ABSPATH', sys_get_temp_dir() . '/nadlan-utopia-wp-stub/' );
define( 'OBJECT', 'OBJECT' );

class WP_Error {
	private $code;
	private $message;
	public function __construct( $code = '', $message = '' ) {
		$this->code = $code;
		$this->message = $message;
	}
	public function get_error_code() { return $this->code; }
	public function get_error_message() { return $this->message; }
}

class WP_Post {
	public $ID;
	public $post_type;
	public $post_status;
	public $post_name;
	public $post_title;
	public $post_content;
	public $post_content_filtered;
	public $post_excerpt;
	public $post_author;
	public $comment_status;
	public $ping_status;
	public $post_parent;
	public $post_date;
	public $post_date_gmt;
	public $post_modified;
	public $post_modified_gmt;
	public $post_mime_type;
	public $guid;
	public function __construct( array $data ) {
		foreach ( $data as $key => $value ) { $this->{$key} = $value; }
	}
}

class Stub_WPDB {
	public $options = 'wp_options';
	public $posts = 'wp_posts';
	public $postmeta = 'wp_postmeta';
	public $term_relationships = 'wp_term_relationships';
	public $term_taxonomy = 'wp_term_taxonomy';
	private $transaction_snapshot = null;

	public function prepare( $query, ...$args ) {
		return array( 'query' => $query, 'args' => $args );
	}
	public function esc_like( $value ) {
		return addcslashes( (string) $value, '_%\\' );
	}
	public function query( $statement ) {
		if ( is_string( $statement ) ) {
			$sql = strtoupper( trim( $statement ) );
			if ( $sql === 'START TRANSACTION' ) {
				if ( $this->transaction_snapshot !== null ) { return false; }
				$this->transaction_snapshot = stub_database_snapshot();
				$GLOBALS['stub_transaction_log'][] = 'start';
				return 1;
			}
			if ( $sql === 'COMMIT' ) {
				if ( $this->transaction_snapshot === null ) { return false; }
				$this->transaction_snapshot = null;
				$GLOBALS['stub_transaction_log'][] = 'commit';
				return 1;
			}
			if ( $sql === 'ROLLBACK' ) {
				if ( $this->transaction_snapshot === null ) { return false; }
				stub_restore_database_snapshot( $this->transaction_snapshot );
				$this->transaction_snapshot = null;
				$GLOBALS['stub_transaction_log'][] = 'rollback';
				$GLOBALS['stub_last_rollback_base'] = stub_snapshot_base();
				return 1;
			}
			return 0;
		}
		if ( ! is_array( $statement ) || ! isset( $statement['query'], $statement['args'] ) ) {
			return false;
		}
		$query = (string) $statement['query'];
		$args  = (array) $statement['args'];
		if ( count( $args ) === 3 && stripos( $query, 'UPDATE ' . $this->options ) !== false ) {
			list( $serialized_new, $key, $serialized_old ) = $args;
			if ( ! array_key_exists( $key, $GLOBALS['stub_options'] ) ||
				maybe_serialize( $GLOBALS['stub_options'][ $key ] ) !== $serialized_old ) {
				return 0;
			}
			$GLOBALS['stub_options'][ $key ] = maybe_unserialize( $serialized_new );
			return 1;
		}
		if ( count( $args ) === 2 && stripos( $query, 'INSERT INTO ' . $this->options ) !== false ) {
			list( $key, $serialized_value ) = $args;
			$GLOBALS['stub_options'][ (string) $key ] = maybe_unserialize( $serialized_value );
			return 1;
		}
		if ( count( $args ) === 1 && stripos( $query, 'DELETE FROM ' . $this->options ) !== false ) {
			unset( $GLOBALS['stub_options'][ (string) $args[0] ] );
			return 1;
		}
		return 0;
	}
	public function get_var( $prepared ) {
		if ( ! is_array( $prepared ) || ! isset( $prepared['query'], $prepared['args'][0] ) ) {
			return null;
		}
		$query = (string) $prepared['query'];
		$value = (string) $prepared['args'][0];
		if ( stripos( $query, 'information_schema.TABLES' ) !== false ) {
			$GLOBALS['stub_engine_checks'][] = $value;
			return $GLOBALS['stub_table_engines'][ $value ] ?? 'InnoDB';
		}
		if ( stripos( $query, 'SELECT option_value FROM ' . $this->options ) !== false ) {
			return array_key_exists( $value, $GLOBALS['stub_options'] )
				? maybe_serialize( $GLOBALS['stub_options'][ $value ] )
				: null;
		}
		return null;
	}
	public function get_col( $prepared ) {
		if ( ! is_array( $prepared ) || empty( $prepared['args'][0] ) ||
			stripos( $prepared['query'], 'SELECT ID FROM ' . $this->posts ) === false ) {
			return array();
		}
		$pattern = str_replace( array( '\\%', '\\_' ), array( '%', '_' ), (string) $prepared['args'][0] );
		$prefix  = rtrim( $pattern, '%' );
		$ids     = array();
		foreach ( $GLOBALS['stub_posts'] as $post ) {
			$value = isset( $post->post_content_filtered ) ? (string) $post->post_content_filtered : '';
			if ( strpos( $value, $prefix ) === 0 && in_array( $post->post_type, array( 'nadlan_project', 'attachment' ), true ) ) {
				$ids[] = (int) $post->ID;
			}
		}
		return $ids;
	}
	public function update( $table, $data, $where, $format = null, $where_format = null ) {
		if ( $table !== $this->posts || ! isset( $where['ID'] ) ) { return false; }
		$id = (int) $where['ID'];
		if ( ! isset( $GLOBALS['stub_posts'][ $id ] ) ) { return false; }
		foreach ( (array) $data as $field => $value ) {
			$GLOBALS['stub_posts'][ $id ]->{$field} = $value;
		}
		return 1;
	}
}

function is_wp_error( $value ) { return $value instanceof WP_Error; }
function add_action( $hook, $callback, $priority = 10, $accepted_args = 1 ) {
	$GLOBALS['stub_actions'][ (string) $hook ][ (int) $priority ][] = array(
		'callback' => $callback,
		'accepted_args' => (int) $accepted_args,
	);
	return true;
}
function remove_action( $hook, $callback, $priority = 10 ) {
	if ( empty( $GLOBALS['stub_actions'][ (string) $hook ][ (int) $priority ] ) ) { return false; }
	foreach ( $GLOBALS['stub_actions'][ (string) $hook ][ (int) $priority ] as $index => $entry ) {
		if ( $entry['callback'] === $callback ) {
			unset( $GLOBALS['stub_actions'][ (string) $hook ][ (int) $priority ][ $index ] );
			return true;
		}
	}
	return false;
}
function do_action( $hook, ...$args ) {
	if ( empty( $GLOBALS['stub_actions'][ (string) $hook ] ) ) { return; }
	$priorities = array_keys( $GLOBALS['stub_actions'][ (string) $hook ] );
	sort( $priorities, SORT_NUMERIC );
	foreach ( $priorities as $priority ) {
		foreach ( $GLOBALS['stub_actions'][ (string) $hook ][ $priority ] as $entry ) {
			call_user_func_array( $entry['callback'], array_slice( $args, 0, $entry['accepted_args'] ) );
		}
	}
}
function add_filter() { return true; }
function is_admin() { return ! empty( $GLOBALS['stub_is_admin'] ); }
function wp_doing_ajax() { return false; }
function current_user_can( $capability ) { return in_array( $capability, $GLOBALS['stub_caps'], true ); }
function wp_cache_delete( $key = '', $group = '' ) {
	$GLOBALS['stub_cache_deletes'][] = array( 'key' => (string) $key, 'group' => (string) $group );
	return true;
}
function wp_suspend_cache_addition( $suspend = null ) {
	if ( is_bool( $suspend ) ) { $GLOBALS['stub_cache_addition_suspended'] = $suspend; }
	return ! empty( $GLOBALS['stub_cache_addition_suspended'] );
}
function clean_post_cache( $post_id ) {
	$GLOBALS['stub_cleaned_post_ids'][] = (int) $post_id;
}
function sanitize_key( $value ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $value ) ); }
function trailingslashit( $value ) { return rtrim( (string) $value, '/\\' ) . '/'; }
function untrailingslashit( $value ) { return rtrim( (string) $value, '/\\' ); }
function wp_slash( $value ) { return $value; }
function wp_unslash( $value ) { return $value; }
function wp_strip_all_tags( $value ) { return strip_tags( (string) $value ); }
function wp_json_encode( $value, $flags = 0 ) { return json_encode( $value, $flags ); }
function is_serialized( $data, $strict = true ) {
	if ( ! is_string( $data ) ) { return false; }
	$data = trim( $data );
	if ( $data === 'N;' ) { return true; }
	if ( strlen( $data ) < 4 || $data[1] !== ':' ) { return false; }
	if ( $strict ) {
		$last = substr( $data, -1 );
		if ( $last !== ';' && $last !== '}' ) { return false; }
	} else {
		$semicolon = strpos( $data, ';' );
		$brace     = strpos( $data, '}' );
		if ( $semicolon === false && $brace === false ) { return false; }
	}
	$token = $data[0];
	switch ( $token ) {
		case 's':
			if ( $strict && substr( $data, -2, 1 ) !== '"' ) { return false; }
			// Fall through.
		case 'a':
		case 'O':
		case 'E':
			return (bool) preg_match( "/^{$token}:[0-9]+:/s", $data );
		case 'b':
		case 'i':
		case 'd':
			return (bool) preg_match( "/^{$token}:[0-9.E+-]+;$/", $data );
	}
	return false;
}
function maybe_serialize( $value ) {
	if ( is_array( $value ) || is_object( $value ) ) { return serialize( $value ); }
	if ( is_serialized( $value, false ) ) { return serialize( $value ); }
	return $value;
}
function maybe_unserialize( $value ) {
	return is_serialized( $value ) ? @unserialize( trim( $value ) ) : $value;
}
function home_url( $path = '' ) { return 'https://nad-lan.co.il' . ( $path ? '/' . ltrim( $path, '/' ) : '' ); }
function plugins_url( $path = '' ) { return 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/' . ltrim( $path, '/' ); }
function wp_generate_uuid4() { return sprintf( '00000000-0000-4000-8000-%012d', ++$GLOBALS['stub_uuid'] ); }
function wp_normalize_path( $path ) { return str_replace( '\\', '/', (string) $path ); }
function get_queried_object_id() { return (int) $GLOBALS['stub_queried_id']; }
function is_singular( $post_type = '' ) {
	$post = get_post( get_queried_object_id() );
	return $post && ( $post_type === '' || $post->post_type === $post_type );
}
function in_the_loop() { return true; }
function is_main_query() { return true; }
function get_post_type( $post_id ) {
	$post = get_post( $post_id );
	return $post ? $post->post_type : false;
}
function get_post_field( $field, $post_id ) {
	$post = get_post( $post_id );
	return $post && isset( $post->{$field} ) ? $post->{$field} : '';
}
function get_post_status( $post_id ) {
	$post = get_post( $post_id );
	return $post ? $post->post_status : false;
}
function get_the_excerpt( $post_id ) { return get_post_field( 'post_excerpt', $post_id ); }
function get_the_title( $post_id ) { return get_post_field( 'post_title', $post_id ); }
function get_permalink( $post_id ) {
	$post = get_post( $post_id );
	return $post ? home_url( '/projects/' . $post->post_name . '/' ) : '';
}
function esc_url_raw( $value ) { return (string) $value; }

function stub_deep_copy( $value ) {
	return unserialize( serialize( $value ) );
}

function stub_database_snapshot() {
	return stub_deep_copy( array(
		'posts' => $GLOBALS['stub_posts'],
		'meta' => $GLOBALS['stub_meta'],
		'terms' => $GLOBALS['stub_terms'],
		'options' => $GLOBALS['stub_options'],
		'revisions' => $GLOBALS['stub_revisions'],
		'attachment_files' => $GLOBALS['stub_attachment_files'],
		'attachment_metadata' => $GLOBALS['stub_attachment_metadata'],
	) );
}

function stub_restore_database_snapshot( array $snapshot ) {
	$GLOBALS['stub_posts'] = $snapshot['posts'];
	$GLOBALS['stub_meta'] = $snapshot['meta'];
	$GLOBALS['stub_terms'] = $snapshot['terms'];
	$GLOBALS['stub_options'] = $snapshot['options'];
	$GLOBALS['stub_revisions'] = $snapshot['revisions'];
	$GLOBALS['stub_attachment_files'] = $snapshot['attachment_files'];
	$GLOBALS['stub_attachment_metadata'] = $snapshot['attachment_metadata'];
}

function stub_next_timestamp() {
	$offset = (int) $GLOBALS['stub_clock_tick']++;
	$stamp  = strtotime( '2026-07-29 12:00:00 UTC' ) + $offset;
	return gmdate( 'Y-m-d H:i:s', $stamp );
}

function stub_post_defaults( array $data ) {
	$now = stub_next_timestamp();
	return array_merge(
		array(
			'ID' => 0,
			'post_type' => 'nadlan_project',
			'post_status' => 'draft',
			'post_name' => '',
			'post_title' => '',
			'post_content' => '',
			'post_content_filtered' => '',
			'post_excerpt' => '',
			'post_author' => 1,
			'comment_status' => 'closed',
			'ping_status' => 'closed',
			'post_parent' => 0,
			'post_date' => $now,
			'post_date_gmt' => $now,
			'post_modified' => $now,
			'post_modified_gmt' => $now,
			'post_mime_type' => '',
			'guid' => '',
		),
		$data
	);
}

function get_post( $post ) {
	$id = $post instanceof WP_Post ? (int) $post->ID : (int) $post;
	return isset( $GLOBALS['stub_posts'][ $id ] ) ? clone $GLOBALS['stub_posts'][ $id ] : null;
}

function get_page_by_path( $slug, $output = null, $post_type = null ) {
	foreach ( $GLOBALS['stub_posts'] as $post ) {
		if ( $post->post_name === $slug && ( $post_type === null || $post->post_type === $post_type ) ) {
			return clone $post;
		}
	}
	return null;
}

function wp_insert_post( $data, $wp_error = false ) {
	if ( ! empty( $GLOBALS['stub_fail_insert'] ) ) {
		return $wp_error ? new WP_Error( 'insert_failed', 'Simulated insert failure.' ) : 0;
	}
	$id = ++$GLOBALS['stub_next_id'];
	$data['ID'] = $id;
	$slug = (string) $data['post_name'];
	foreach ( $GLOBALS['stub_posts'] as $post ) {
		if ( $post->post_type === ( $data['post_type'] ?? 'post' ) && $post->post_name === $slug ) {
			$data['post_name'] = $slug . '-2';
			break;
		}
	}
	$GLOBALS['stub_posts'][ $id ] = new WP_Post( stub_post_defaults( $data ) );
	return $id;
}

function stub_create_revision( WP_Post $post ) {
	$id = ++$GLOBALS['stub_next_revision_id'];
	$data = get_object_vars( $post );
	$data['ID'] = $id;
	$data['post_type'] = 'revision';
	$data['post_status'] = 'inherit';
	$data['post_parent'] = (int) $post->ID;
	$data['post_name'] = $post->ID . '-revision-v1';
	$data['guid'] = home_url( '/?p=' . $id );
	$GLOBALS['stub_revisions'][ $id ] = new WP_Post( stub_post_defaults( $data ) );
	return $id;
}

function wp_get_post_revisions( $post_id, $args = array() ) {
	$revisions = array();
	foreach ( $GLOBALS['stub_revisions'] as $id => $revision ) {
		if ( (int) $revision->post_parent === (int) $post_id ) {
			$revisions[ (int) $id ] = clone $revision;
		}
	}
	krsort( $revisions, SORT_NUMERIC );
	return $revisions;
}

function wp_update_post( $data, $wp_error = false ) {
	$id = isset( $data['ID'] ) ? (int) $data['ID'] : 0;
	if ( ! isset( $GLOBALS['stub_posts'][ $id ] ) || (int) $GLOBALS['stub_fail_update_id'] === $id ) {
		return $wp_error ? new WP_Error( 'update_failed', 'Simulated update failure.' ) : 0;
	}
	$post = $GLOBALS['stub_posts'][ $id ];
	$noop = (int) $GLOBALS['stub_noop_update_id'] === $id;
	if ( ! $noop && $post->post_type === 'nadlan_project' ) {
		stub_create_revision( clone $post );
	}
	foreach ( $data as $key => $value ) {
		if ( $key === 'post_status' ) {
			$GLOBALS['stub_status_log'][] = array( 'id' => $id, 'status' => $value );
		}
		if ( $key !== 'ID' && ! $noop ) {
			$GLOBALS['stub_posts'][ $id ]->{$key} = $value;
		}
	}
	if ( ! $noop ) {
		$modified = stub_next_timestamp();
		$GLOBALS['stub_posts'][ $id ]->post_modified = $modified;
		$GLOBALS['stub_posts'][ $id ]->post_modified_gmt = $modified;
	}
	return $id;
}

function wp_delete_post( $post_id, $force = false ) {
	if ( isset( $GLOBALS['stub_revisions'][ (int) $post_id ] ) ) {
		unset( $GLOBALS['stub_revisions'][ (int) $post_id ] );
		return true;
	}
	if ( ! isset( $GLOBALS['stub_posts'][ (int) $post_id ] ) ) { return false; }
	unset( $GLOBALS['stub_posts'][ (int) $post_id ], $GLOBALS['stub_meta'][ (int) $post_id ], $GLOBALS['stub_terms'][ (int) $post_id ] );
	foreach ( $GLOBALS['stub_revisions'] as $revision_id => $revision ) {
		if ( (int) $revision->post_parent === (int) $post_id ) {
			unset( $GLOBALS['stub_revisions'][ $revision_id ] );
		}
	}
	return true;
}

function get_post_meta( $post_id, $key = '', $single = false ) {
	$values = $GLOBALS['stub_meta'][ (int) $post_id ][ $key ] ?? array();
	if ( $single ) { return $values ? $values[0] : ''; }
	return array_values( $values );
}

function update_post_meta( $post_id, $key, $value ) {
	if ( $GLOBALS['stub_fail_meta_key'] === $key ) { return false; }
	$GLOBALS['stub_meta'][ (int) $post_id ][ $key ] = array( $value );
	return true;
}

function add_post_meta( $post_id, $key, $value ) {
	$GLOBALS['stub_meta'][ (int) $post_id ][ $key ][] = $value;
	return true;
}

function delete_post_meta( $post_id, $key ) {
	unset( $GLOBALS['stub_meta'][ (int) $post_id ][ $key ] );
	return true;
}

function get_post_thumbnail_id( $post_id ) { return (int) get_post_meta( $post_id, '_thumbnail_id', true ); }
function set_post_thumbnail( $post_id, $attachment_id ) {
	update_post_meta( $post_id, '_thumbnail_id', (int) $attachment_id );
	return true;
}

function wp_get_object_terms( $post_id, $taxonomy, $args = array() ) {
	if ( ! in_array( $taxonomy, array( 'nadlan_city', 'nadlan_compound' ), true ) ) {
		return new WP_Error( 'bad_taxonomy', 'Invalid taxonomy.' );
	}
	return array_values( $GLOBALS['stub_terms'][ (int) $post_id ][ $taxonomy ] ?? array() );
}

function wp_set_object_terms( $post_id, $terms, $taxonomy, $append = false ) {
	if ( ! in_array( $taxonomy, array( 'nadlan_city', 'nadlan_compound' ), true ) ) {
		return new WP_Error( 'bad_taxonomy', 'Invalid taxonomy.' );
	}
	$GLOBALS['stub_terms'][ (int) $post_id ][ $taxonomy ] = array_values( array_map( 'intval', $terms ) );
	return $GLOBALS['stub_terms'][ (int) $post_id ][ $taxonomy ];
}

function add_option( $key, $value, $deprecated = '', $autoload = 'yes' ) {
	if ( array_key_exists( $key, $GLOBALS['stub_options'] ) ) { return false; }
	$GLOBALS['stub_options'][ $key ] = $value;
	return true;
}
function get_option( $key, $default = false ) {
	return array_key_exists( $key, $GLOBALS['stub_options'] ) ? $GLOBALS['stub_options'][ $key ] : $default;
}
function update_option( $key, $value, $autoload = null ) {
	$changed = ! array_key_exists( $key, $GLOBALS['stub_options'] ) || $GLOBALS['stub_options'][ $key ] !== $value;
	$GLOBALS['stub_options'][ $key ] = $value;
	return $changed;
}
function delete_option( $key ) {
	if ( ! array_key_exists( $key, $GLOBALS['stub_options'] ) ) { return false; }
	unset( $GLOBALS['stub_options'][ $key ] );
	return true;
}

function get_posts( $args = array() ) {
	$ids = array();
	foreach ( $GLOBALS['stub_posts'] as $post ) {
		if ( $post->post_type !== ( $args['post_type'] ?? $post->post_type ) ) { continue; }
		if ( isset( $args['meta_key'], $args['meta_value'] ) &&
			get_post_meta( $post->ID, $args['meta_key'], true ) !== $args['meta_value'] ) { continue; }
		$ids[] = $post->ID;
	}
	return $ids;
}

function wp_upload_dir() {
	return array(
		'path' => $GLOBALS['stub_upload_dir'],
		'url' => 'https://nad-lan.co.il/wp-content/uploads/2026/07',
		'basedir' => $GLOBALS['stub_upload_dir'],
		'error' => false,
	);
}
function wp_check_filetype( $name, $mimes = null ) { return array( 'type' => 'image/webp', 'ext' => 'webp' ); }
function wp_insert_attachment( $data, $file, $parent = 0, $wp_error = false ) {
	$data['post_type'] = 'attachment';
	$data['post_name'] = 'utopia-sde-dov-independent-concept-v1';
	$data['post_parent'] = (int) $parent;
	$id = wp_insert_post( $data, $wp_error );
	if ( ! is_wp_error( $id ) && $id ) {
		$GLOBALS['stub_attachment_files'][ (int) $id ] = $file;
		update_post_meta( (int) $id, '_wp_attached_file', (string) $file );
	}
	return $id;
}
function wp_generate_attachment_metadata( $id, $file ) { return array( 'file' => basename( $file ) ); }
function wp_update_attachment_metadata( $id, $metadata ) {
	$GLOBALS['stub_attachment_metadata'][ (int) $id ] = $metadata;
	update_post_meta( (int) $id, '_wp_attachment_metadata', $metadata );
	return true;
}
function get_attached_file( $attachment_id, $unfiltered = false ) {
	return $GLOBALS['stub_attachment_files'][ (int) $attachment_id ] ?? false;
}
function get_post_mime_type( $post_id = null ) {
	$post = get_post( $post_id );
	return $post ? (string) $post->post_mime_type : false;
}
function wp_delete_attachment( $id, $force = false ) {
	$file = get_attached_file( (int) $id, true );
	if ( $file && file_exists( $file ) ) { unlink( $file ); }
	unset( $GLOBALS['stub_attachment_files'][ (int) $id ], $GLOBALS['stub_attachment_metadata'][ (int) $id ] );
	return wp_delete_post( $id, true );
}
function wp_delete_file( $file ) { if ( file_exists( $file ) ) { unlink( $file ); } }

function nadlan_showroom_engine_dir() {
	return dirname( __DIR__ ) . '/plugins/nadlan-config/assets/showroom-engine/';
}
function nadlan_showroom_engine_base_url() {
	return 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/showroom-engine/';
}
function nadlan_showroom_engine_shortcode() {
	return '<div id="nl-root" data-page="project"></div>';
}

function stub_reset( $with_collision = false ) {
	$GLOBALS['wpdb'] = new Stub_WPDB();
	$GLOBALS['stub_posts'] = array();
	$GLOBALS['stub_meta'] = array();
	$GLOBALS['stub_terms'] = array();
	$GLOBALS['stub_options'] = array();
	$GLOBALS['stub_revisions'] = array();
	$GLOBALS['stub_attachment_files'] = array();
	$GLOBALS['stub_attachment_metadata'] = array();
	$GLOBALS['stub_next_id'] = 6000;
	$GLOBALS['stub_next_revision_id'] = 7000;
	$GLOBALS['stub_clock_tick'] = 0;
	$GLOBALS['stub_uuid'] = 0;
	$GLOBALS['stub_fail_insert'] = false;
	$GLOBALS['stub_fail_update_id'] = 0;
	$GLOBALS['stub_fail_meta_key'] = '';
	$GLOBALS['stub_noop_update_id'] = 0;
	$GLOBALS['stub_is_admin'] = true;
	$GLOBALS['stub_caps'] = array( 'manage_options', 'unfiltered_html' );
	$GLOBALS['stub_status_log'] = array();
	$GLOBALS['stub_queried_id'] = 0;
	$GLOBALS['stub_cache_addition_suspended'] = false;
	$GLOBALS['stub_cache_deletes'] = array();
	$GLOBALS['stub_cleaned_post_ids'] = array();
	$GLOBALS['stub_engine_checks'] = array();
	$GLOBALS['stub_transaction_log'] = array();
	$GLOBALS['stub_last_rollback_base'] = null;
	$GLOBALS['stub_table_engines'] = array(
		'wp_posts' => 'InnoDB',
		'wp_postmeta' => 'InnoDB',
		'wp_term_relationships' => 'InnoDB',
		'wp_term_taxonomy' => 'InnoDB',
		'wp_options' => 'InnoDB',
	);
	$GLOBALS['stub_posts'][4749] = new WP_Post( stub_post_defaults( array(
		'ID' => 4749,
		'post_status' => 'publish',
		'post_name' => 'utopia-sde-dov',
		'post_title' => 'UTOPIA שדה דב - קבוצת נחמיאס',
		'post_content' => '<p>Before UTOPIA article</p>',
		'post_excerpt' => 'Before excerpt',
		'post_author' => 7,
		'comment_status' => 'open',
		'ping_status' => 'open',
		'post_date' => '2024-12-11 08:15:00',
		'post_date_gmt' => '2024-12-11 06:15:00',
		'post_modified' => '2026-05-02 17:45:12',
		'post_modified_gmt' => '2026-05-02 14:45:12',
	) ) );
	foreach ( array(
		4601 => array(
			'post_title' => 'UTOPIA baseline revision one',
			'post_content' => '<p>Older UTOPIA content</p>',
			'post_modified' => '2025-02-01 10:00:00',
			'post_modified_gmt' => '2025-02-01 08:00:00',
		),
		4602 => array(
			'post_title' => 'UTOPIA baseline revision two',
			'post_content' => '<p>Newer UTOPIA content</p>',
			'post_modified' => '2026-03-12 15:30:00',
			'post_modified_gmt' => '2026-03-12 13:30:00',
		),
	) as $revision_id => $revision_fields ) {
		$GLOBALS['stub_revisions'][ $revision_id ] = new WP_Post( stub_post_defaults( array_merge(
			array(
				'ID' => $revision_id,
				'post_type' => 'revision',
				'post_status' => 'inherit',
				'post_parent' => 4749,
				'post_name' => '4749-revision-v1',
				'post_author' => 7,
			),
			$revision_fields
		) ) );
	}
	$GLOBALS['stub_meta'][4749] = array(
		'source_url' => array( 'https://utopiatlv.co.il/' ),
		'project_3d_avg_price_per_sqm' => array( '78000' ),
		'_thumbnail_id' => array( '5045' ),
		'unrelated_user_meta' => array( 'preserve-me' ),
	);
	$GLOBALS['stub_terms'][4749] = array( 'nadlan_city' => array( 12 ), 'nadlan_compound' => array( 44 ) );
	if ( $with_collision ) {
		$GLOBALS['stub_posts'][5900] = new WP_Post( stub_post_defaults( array(
			'ID' => 5900,
			'post_status' => 'publish',
			'post_name' => 'utopia-sde-dov-en',
			'post_title' => 'Unrelated project',
		) ) );
	}
	if ( ! is_dir( $GLOBALS['stub_upload_dir'] ) ) { mkdir( $GLOBALS['stub_upload_dir'], 0777, true ); }
	$file = $GLOBALS['stub_upload_dir'] . '/utopia-sde-dov-independent-concept-v1.webp';
	if ( file_exists( $file ) ) { unlink( $file ); }
}

function stub_snapshot_base() {
	$meta = $GLOBALS['stub_meta'][4749];
	ksort( $meta );
	$revisions = array();
	foreach ( wp_get_post_revisions( 4749, array( 'check_enabled' => false ) ) as $revision_id => $revision ) {
		$revisions[ (int) $revision_id ] = get_object_vars( $revision );
	}
	ksort( $revisions, SORT_NUMERIC );
	return array(
		'post' => get_object_vars( get_post( 4749 ) ),
		'meta' => $meta,
		'terms' => $GLOBALS['stub_terms'][4749],
		'revisions' => $revisions,
	);
}

function qa_assert( $condition, $message ) {
	if ( ! $condition ) { throw new RuntimeException( $message ); }
}

$GLOBALS['stub_upload_dir'] = sys_get_temp_dir() . '/nadlan-utopia-release-qa';
$GLOBALS['wpdb'] = new Stub_WPDB();
if ( ! is_dir( ABSPATH . 'wp-admin/includes' ) ) { mkdir( ABSPATH . 'wp-admin/includes', 0777, true ); }
if ( ! file_exists( ABSPATH . 'wp-admin/includes/image.php' ) ) { file_put_contents( ABSPATH . 'wp-admin/includes/image.php', "<?php\n" ); }

require_once dirname( __DIR__ ) . '/plugins/nadlan-config/inc/utopia-sde-dov.php';

$tests = array();

stub_reset();
$GLOBALS['stub_is_admin'] = false;
nadlan_utopia_seed_v172128();
qa_assert( count( $GLOBALS['stub_posts'] ) === 1, 'A public request was allowed to run the release.' );
$GLOBALS['stub_is_admin'] = true;
$GLOBALS['stub_caps'] = array( 'manage_options' );
nadlan_utopia_seed_v172128();
qa_assert( count( $GLOBALS['stub_posts'] ) === 1, 'An admin without unfiltered_html was allowed to run the release.' );
$tests['authorized_admin_gate'] = true;
qa_assert( nadlan_utopia_recovery_context_allowed() === false, 'Recovery context accepted a user without unfiltered_html.' );
$GLOBALS['stub_caps'] = array( 'manage_options', 'unfiltered_html' );
qa_assert( nadlan_utopia_recovery_context_allowed() === true, 'Recovery context rejected an authorized administrator.' );
$tests['recovery_context_unfiltered_html_gate'] = true;

stub_reset();
$before = stub_snapshot_base();
$before_dates = array_intersect_key(
	$before['post'],
	array_flip( array( 'post_date', 'post_date_gmt', 'post_modified', 'post_modified_gmt' ) )
);
$before_revisions = $before['revisions'];
nadlan_utopia_seed_v172128();
qa_assert(
	get_option( 'nadlan_utopia_release_v172128' ) === '1',
	'Successful release did not set completion: ' . json_encode( get_option( 'nadlan_utopia_release_v172128_error', null ), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE )
);
qa_assert( count( array_filter( $GLOBALS['stub_posts'], function ( $post ) { return $post->post_type === 'nadlan_project'; } ) ) === 5, 'Successful release did not produce five project posts.' );
foreach ( nadlan_utopia_release_slugs() as $lang => $slug ) {
	$post = get_page_by_path( $slug, OBJECT, 'nadlan_project' );
	qa_assert( $post && $post->post_status === 'publish', 'Language was not published: ' . $lang );
	qa_assert( get_post_meta( $post->ID, '_nadlan_utopia_identity', true ) === nadlan_utopia_identity_marker( $lang ), 'Identity marker mismatch: ' . $lang );
	qa_assert( get_post_meta( $post->ID, '_yoast_wpseo_canonical', true ) === nadlan_utopia_expected_canonical( $lang ), 'Canonical mismatch: ' . $lang );
	qa_assert( wp_get_object_terms( $post->ID, 'nadlan_city', array( 'fields' => 'ids' ) ) === array( 12 ), 'City taxonomy mismatch: ' . $lang );
	qa_assert( wp_get_object_terms( $post->ID, 'nadlan_compound', array( 'fields' => 'ids' ) ) === array( 44 ), 'Compound taxonomy mismatch: ' . $lang );
	qa_assert( get_post_meta( $post->ID, 'project_status', true ) === 'permits', 'Project status is not permits: ' . $lang );
	qa_assert( count( nadlan_utopia_visible_faq( $post->ID ) ) >= 20, 'Visible FAQ extraction failed: ' . $lang );
}
$tests['project_status_permits'] = true;
qa_assert(
	array_values( array_unique( $GLOBALS['stub_engine_checks'] ) ) === array( 'wp_posts', 'wp_postmeta', 'wp_term_relationships', 'wp_term_taxonomy', 'wp_options' ),
	'Transactional table readiness did not inspect every required WordPress table.'
);
$tests['transactional_table_engine_check'] = true;
$runtime_assets = nadlan_utopia_validate_runtime_assets();
qa_assert( $runtime_assets === true, 'Verified runtime asset validation failed.' );
$concept_ids = get_posts( array(
	'post_type' => 'attachment',
	'post_status' => 'inherit',
	'fields' => 'ids',
	'meta_key' => '_nadlan_utopia_concept_asset',
	'meta_value' => 'exterior-v1',
) );
qa_assert( count( $concept_ids ) === 1, 'Successful release did not create one tracked UTOPIA concept attachment.' );
$concept_id = (int) $concept_ids[0];
qa_assert( nadlan_utopia_validate_concept_attachment( $concept_id ) === true, 'Created UTOPIA concept attachment failed validation.' );
$original_mime = $GLOBALS['stub_posts'][ $concept_id ]->post_mime_type;
$GLOBALS['stub_posts'][ $concept_id ]->post_mime_type = 'image/jpeg';
$reuse_resources = array( 'created_post_ids' => array(), 'created_attachment_ids' => array(), 'created_files' => array() );
$broken_reuse = nadlan_utopia_concept_attachment( $reuse_resources, 'unused-reuse-token' );
qa_assert( is_wp_error( $broken_reuse ), 'A broken reused UTOPIA attachment passed validation.' );
$GLOBALS['stub_posts'][ $concept_id ]->post_mime_type = $original_mime;
qa_assert( nadlan_utopia_validate_concept_attachment( $concept_id ) === true, 'Restored concept attachment did not return to a valid state.' );
$tests['runtime_assets_and_attachment_reuse_validation'] = true;
$released_snapshot = stub_snapshot_base();
$released_dates = array_intersect_key(
	$released_snapshot['post'],
	array_flip( array( 'post_date', 'post_date_gmt', 'post_modified', 'post_modified_gmt' ) )
);
qa_assert( $released_dates !== $before_dates, 'Release simulation did not exercise WordPress modified-timestamp behavior.' );
qa_assert( count( $released_snapshot['revisions'] ) > count( $before_revisions ), 'Release simulation did not create a WordPress revision for the published page update.' );
qa_assert(
	! array_filter( $GLOBALS['stub_status_log'], function ( $row ) { return $row['id'] === 4749 && $row['status'] === 'draft'; } ),
	'The existing published Hebrew page was demoted to draft during staging.'
);
$english = get_page_by_path( 'utopia-sde-dov-en', OBJECT, 'nadlan_project' );
$GLOBALS['stub_queried_id'] = (int) $english->ID;
$legacy_output = '<div class="nlpf" dir="rtl"><h1>Legacy Hebrew heading</h1></div><div class="nlpjx-nav"></div><div class="nlcard"></div>';
$public_output = nadlan_utopia_final_content_filter( $legacy_output );
preg_match_all( '/<h1\b/iu', $public_output, $public_h1s );
qa_assert( count( $public_h1s[0] ) === 1, 'Final UTOPIA composition did not contain exactly one H1.' );
preg_match_all( '/<nav\b/iu', $public_output, $public_navs );
qa_assert( count( $public_navs[0] ) === 1, 'Final UTOPIA composition did not retain exactly one article-authored table of contents.' );
qa_assert( strpos( $public_output, 'nlw-toc' ) === false, 'Final UTOPIA composition retained a generic weaver table of contents.' );
qa_assert( strpos( $public_output, 'Legacy Hebrew heading' ) === false, 'Final UTOPIA composition retained legacy injected content.' );
qa_assert( strpos( $public_output, 'nlpf' ) === false && strpos( $public_output, 'nlpjx-nav' ) === false && strpos( $public_output, 'nlcard' ) === false, 'Final UTOPIA composition retained a legacy project class.' );
qa_assert( strpos( $public_output, '<h1' ) < strpos( $public_output, 'id="nl-root"' ), 'The buyer-facing H1 did not precede the interactive showroom.' );
$GLOBALS['stub_queried_id'] = 0;
$tests['final_filter_chain_composition'] = true;
$post_count = count( $GLOBALS['stub_posts'] );
nadlan_utopia_seed_v172128();
qa_assert( count( $GLOBALS['stub_posts'] ) === $post_count, 'Idempotent rerun changed post count.' );
$tests['success_and_idempotency'] = true;

$restored = nadlan_utopia_restore_backup( array(), true );
qa_assert( $restored === true, 'Manual restore failed after success.' );
$after_restore = stub_snapshot_base();
qa_assert( $after_restore === $before, 'Manual restore did not exactly restore the base target: ' . json_encode( array( 'before' => $before, 'after' => $after_restore ), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) );
$after_dates = array_intersect_key(
	$after_restore['post'],
	array_flip( array( 'post_date', 'post_date_gmt', 'post_modified', 'post_modified_gmt' ) )
);
qa_assert( $after_dates === $before_dates, 'Manual restore did not return all post timestamps exactly.' );
qa_assert( $after_restore['revisions'] === $before_revisions, 'Manual restore did not return revision history exactly.' );
$tests['manual_restore_exact_timestamps_and_revisions'] = true;
qa_assert( count( array_filter( $GLOBALS['stub_posts'], function ( $post ) { return $post->post_type === 'nadlan_project'; } ) ) === 1, 'Manual restore did not remove created translations.' );
qa_assert( get_option( 'nadlan_utopia_release_v172128', false ) === false, 'Manual restore left release completion set.' );
qa_assert( get_option( 'nadlan_utopia_release_v172128_hold', false ) === 'operator', 'Manual restore did not set an operator hold.' );
nadlan_utopia_seed_v172128();
qa_assert( count( $GLOBALS['stub_posts'] ) === 1, 'Operator hold allowed an automatic reseed.' );
qa_assert( nadlan_utopia_resume_release() === true, 'Explicit resume failed after operator restore.' );
nadlan_utopia_seed_v172128();
qa_assert( get_option( 'nadlan_utopia_release_v172128' ) === '1', 'Explicit resume did not permit a subsequent release.' );
$tests['manual_restore_hold_and_resume'] = true;

stub_reset( true );
$before = stub_snapshot_base();
nadlan_utopia_seed_v172128();
qa_assert( get_option( 'nadlan_utopia_release_v172128', false ) === false, 'Collision release was incorrectly completed.' );
qa_assert( stub_snapshot_base() === $before, 'Collision path changed the base target.' );
qa_assert( get_post( 5900 )->post_title === 'Unrelated project', 'Collision path changed the unrelated project.' );
$tests['slug_collision_hard_stop'] = true;

stub_reset();
$before = stub_snapshot_base();
$GLOBALS['stub_fail_meta_key'] = 'architect_name';
nadlan_utopia_seed_v172128();
qa_assert( get_option( 'nadlan_utopia_release_v172128', false ) === false, 'Failed transaction was incorrectly completed.' );
qa_assert( stub_snapshot_base() === $before, 'Automatic rollback did not exactly restore the base target.' );
qa_assert( count( array_filter( $GLOBALS['stub_posts'], function ( $post ) { return $post->post_type === 'nadlan_project'; } ) ) === 1, 'Automatic rollback did not remove translation drafts.' );
qa_assert( count( array_filter( $GLOBALS['stub_posts'], function ( $post ) { return $post->post_type === 'attachment'; } ) ) === 0, 'Automatic rollback did not remove the attachment.' );
qa_assert( ! file_exists( $GLOBALS['stub_upload_dir'] . '/utopia-sde-dov-independent-concept-v1.webp' ), 'Automatic rollback did not remove the copied file.' );
qa_assert( get_option( 'nadlan_utopia_release_v172128_hold', false ) === false, 'A verified automatic rollback incorrectly left a release hold.' );
$tests['automatic_rollback'] = true;

stub_reset();
$before = stub_snapshot_base();
$public_stage_calls = 0;
$fail_after_public_stage = function ( $lang, $post_id ) use ( &$public_stage_calls ) {
	$public_stage_calls++;
	if ( $public_stage_calls === 1 ) {
		throw new RuntimeException( 'Simulated failure immediately after first public UTOPIA stage.' );
	}
};
add_action( 'nadlan_utopia_atomic_after_public_stage', $fail_after_public_stage, 10, 2 );
try {
	nadlan_utopia_seed_v172128();
} finally {
	remove_action( 'nadlan_utopia_atomic_after_public_stage', $fail_after_public_stage, 10 );
}
qa_assert( $public_stage_calls === 1, 'Atomic failure hook did not fire immediately after the first public post was staged.' );
qa_assert( get_option( 'nadlan_utopia_release_v172128', false ) === false, 'Atomic failure was incorrectly marked complete.' );
qa_assert( $GLOBALS['stub_transaction_log'] === array( 'start', 'rollback' ), 'Atomic failure did not execute one database transaction rollback.' );
qa_assert( $GLOBALS['stub_last_rollback_base'] === $before, 'The database rollback itself did not return the published UTOPIA page to its pre-transaction state.' );
qa_assert( stub_snapshot_base() === $before, 'Database rollback exposed or retained a partially staged published UTOPIA page.' );
qa_assert(
	count( array_filter( $GLOBALS['stub_posts'], function ( $post ) { return $post->post_type === 'nadlan_project'; } ) ) === 1,
	'Atomic failure cleanup left translation posts behind.'
);
qa_assert(
	count( array_filter( $GLOBALS['stub_posts'], function ( $post ) { return $post->post_type === 'attachment'; } ) ) === 0,
	'Atomic failure cleanup left the concept attachment behind.'
);
qa_assert( ! file_exists( $GLOBALS['stub_upload_dir'] . '/utopia-sde-dov-independent-concept-v1.webp' ), 'Atomic failure cleanup left the concept file behind.' );
qa_assert( wp_suspend_cache_addition() === false, 'Atomic rollback did not restore the cache-addition state.' );
qa_assert( get_option( 'nadlan_utopia_release_v172128_hold', false ) === false, 'Verified atomic rollback incorrectly left a recovery hold.' );
$tests['atomic_public_stage_failure_rollback'] = true;

stub_reset();
$before = stub_snapshot_base();
$GLOBALS['stub_table_engines']['wp_postmeta'] = 'MyISAM';
nadlan_utopia_seed_v172128();
qa_assert( get_option( 'nadlan_utopia_release_v172128', false ) === false, 'Release completed with a nontransactional WordPress table.' );
qa_assert( stub_snapshot_base() === $before, 'Nontransactional table guard changed the published UTOPIA page.' );
qa_assert(
	count( array_filter( $GLOBALS['stub_posts'], function ( $post ) { return $post->post_type === 'nadlan_project'; } ) ) === 1,
	'Nontransactional table guard left translation drafts behind.'
);
qa_assert( ! file_exists( $GLOBALS['stub_upload_dir'] . '/utopia-sde-dov-independent-concept-v1.webp' ), 'Nontransactional table guard left the concept file behind.' );
$engine_error = get_option( 'nadlan_utopia_release_v172128_error', array() );
qa_assert(
	is_array( $engine_error ) && isset( $engine_error['message'] ) && strpos( $engine_error['message'], 'not transactional' ) !== false,
	'Nontransactional table guard did not record the expected release error.'
);
$tests['nontransactional_table_hard_stop'] = true;

stub_reset();
$before = stub_snapshot_base();
$GLOBALS['stub_options']['nadlan_utopia_release_v172128_run'] = array(
	'schema' => 'nadlan-utopia-release-run/v1',
	'token' => 'invalid-run-token',
	'checksum' => 'not-a-valid-checksum',
);
nadlan_utopia_seed_v172128();
qa_assert( get_option( 'nadlan_utopia_release_v172128_hold', false ) === 'blocked-recovery', 'Invalid run journal did not set blocked-recovery.' );
qa_assert( get_option( 'nadlan_utopia_release_v172128', false ) === false, 'Invalid run journal was incorrectly marked complete.' );
qa_assert( stub_snapshot_base() === $before, 'Invalid run journal path changed the published UTOPIA page.' );
$tests['invalid_run_journal_blocks_recovery'] = true;

stub_reset();
$GLOBALS['stub_options']['nadlan_utopia_release_v172128_lock'] = array( 'token' => 'active', 'acquired_at' => time() );
nadlan_utopia_seed_v172128();
qa_assert( count( $GLOBALS['stub_posts'] ) === 1 && get_option( 'nadlan_utopia_release_v172128', false ) === false, 'Active lock did not block a concurrent release.' );
$GLOBALS['stub_options']['nadlan_utopia_release_v172128_lock']['acquired_at'] = time() - 901;
nadlan_utopia_seed_v172128();
qa_assert( get_option( 'nadlan_utopia_release_v172128' ) === '1', 'Stale lock recovery did not complete the release.' );
$tests['lock_and_stale_recovery'] = true;

stub_reset();
$GLOBALS['stub_options']['nadlan_utopia_release_v172128_lock'] = array( 'token' => 'stale', 'acquired_at' => time() - 901 );
$first_claim = nadlan_utopia_acquire_release_lock();
$second_claim = nadlan_utopia_acquire_release_lock();
qa_assert( $first_claim !== '', 'First stale-lock claimant did not acquire the lock.' );
qa_assert( $second_claim === '', 'A second claimant acquired a freshly replaced lock.' );
nadlan_utopia_release_lock( $first_claim );
$tests['atomic_stale_lock_claim'] = true;

stub_reset();
$baseline_posts = array( 'he' => get_post( 4749 ), 'en' => null, 'fr' => null, 'ru' => null, 'ar' => null );
$backup = nadlan_utopia_backup_state( $baseline_posts );
qa_assert( ! is_wp_error( $backup ), 'Could not create process-death test backup.' );
$dead_token = 'process-death-token';
qa_assert( nadlan_utopia_start_run( $dead_token ) === true, 'Could not create process-death run journal.' );
$dead_post_id = wp_insert_post( array(
	'post_type' => 'nadlan_project',
	'post_status' => 'draft',
	'post_name' => 'utopia-sde-dov-en',
	'post_title' => 'Interrupted UTOPIA translation',
	'post_content_filtered' => nadlan_utopia_run_tag( $dead_token, 'project-en' ),
), true );
$dead_attachment_id = wp_insert_post( array(
	'post_type' => 'attachment',
	'post_status' => 'inherit',
	'post_name' => 'utopia-sde-dov-independent-concept-v1',
	'post_title' => 'Interrupted UTOPIA attachment',
	'post_content_filtered' => nadlan_utopia_run_tag( $dead_token, 'attachment' ),
), true );
$dead_file = $GLOBALS['stub_upload_dir'] . '/utopia-sde-dov-independent-concept-v1.webp';
qa_assert( nadlan_utopia_run_add_resource( $dead_token, 'planned_files', $dead_file ) === true, 'Could not write-ahead journal the interrupted file.' );
file_put_contents( $dead_file, 'interrupted' );
nadlan_utopia_seed_v172128();
qa_assert( get_option( 'nadlan_utopia_release_v172128' ) === '1', 'Incomplete-run reconciliation did not permit a clean retry.' );
qa_assert( ! get_post( $dead_post_id ), 'Token-tagged post from the interrupted run was not removed.' );
qa_assert( ! get_post( $dead_attachment_id ), 'Token-tagged attachment from the interrupted run was not removed.' );
$tests['write_ahead_process_death_recovery'] = true;

stub_reset();
nadlan_utopia_seed_v172128();
qa_assert( get_option( 'nadlan_utopia_release_v172128' ) === '1', 'Restore verification setup release failed.' );
$GLOBALS['stub_noop_update_id'] = 4749;
$failed_restore = nadlan_utopia_restore_backup( array(), true );
qa_assert( is_wp_error( $failed_restore ), 'Restore readback mismatch was not detected.' );
qa_assert( get_option( 'nadlan_utopia_release_v172128_hold', false ) === 'blocked-recovery', 'Restore mismatch did not set blocked recovery.' );
qa_assert( get_option( 'nadlan_utopia_release_v172128' ) === '1', 'Failed restore cleared the completion marker before verification.' );
$tests['restore_readback_block'] = true;

$report = array(
	'schema' => 'nadlan-utopia-release-migration-qa/v3',
	'generated_at' => gmdate( 'c' ),
	'tests' => $tests,
	'pass' => ! in_array( false, $tests, true ),
);
$encoded = json_encode( $report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES ) . PHP_EOL;
file_put_contents( dirname( __DIR__ ) . '/docs/qa/utopia-release-migration-report.json', $encoded );
echo $encoded;
