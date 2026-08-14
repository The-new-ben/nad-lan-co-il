<?php
/**
 * PROPOSAL ONLY — NOT APPLIED.
 * Executable seam fixture for token-owned locks and durable crash recovery.
 */

declare(strict_types=1);

define( 'ABSPATH', __DIR__ . DIRECTORY_SEPARATOR );
define( 'HOUR_IN_SECONDS', 3600 );
define( 'DAY_IN_SECONDS', 86400 );
define( 'OBJECT', 'OBJECT' );
define( 'NL_PROPOSAL_COMMERCIAL_SCENE_SANDBOX', true );

final class WP_Error {
	private $code;
	private $message;
	private $data;

	public function __construct( $code = '', $message = '', $data = null ) {
		$this->code    = $code;
		$this->message = $message;
		$this->data    = $data;
	}

	public function get_error_code() {
		return $this->code;
	}
	public function get_error_message() { return $this->message; }
	public function get_error_data() { return $this->data; }
}

final class WP_REST_Response {
	public $data;
	public $status;
	public function __construct( $data, $status = 200 ) { $this->data = $data; $this->status = $status; }
	public function get_data() { return $this->data; }
	public function get_status() { return $this->status; }
}

function is_wp_error( $value ) {
	return $value instanceof WP_Error;
}

$GLOBALS['fixture_options']      = array();
$GLOBALS['fixture_posts']        = array();
$GLOBALS['fixture_post_meta']    = array();
$GLOBALS['fixture_insert_count'] = 0;
$GLOBALS['fixture_next_post_id'] = 700;
$GLOBALS['fixture_crash_once']   = false;
$GLOBALS['fixture_schedules']    = array();
$GLOBALS['fixture_filter_calls'] = array();
$GLOBALS['fixture_action_calls'] = array();
$GLOBALS['fixture_mail_calls']   = 0;
$GLOBALS['fixture_filter_overrides'] = array();
$GLOBALS['fixture_transients']   = array();

final class FixtureWpdb {
	public $options = 'wp_options';

	public function prepare( $query, ...$args ) {
		return array( 'query' => $query, 'args' => $args );
	}

	public function query( $prepared ) {
		$query = $prepared['query'];
		$args  = $prepared['args'];
		if ( 0 === strpos( ltrim( $query ), 'UPDATE ' ) ) {
			$new_value = $args[0];
			$name      = $args[1];
			$expected  = $args[2];
			if ( ! array_key_exists( $name, $GLOBALS['fixture_options'] ) || maybe_serialize( $GLOBALS['fixture_options'][ $name ] ) !== $expected ) {
				return 0;
			}
			$GLOBALS['fixture_options'][ $name ] = unserialize( $new_value, array( 'allowed_classes' => false ) );
			return 1;
		}
		if ( 0 === strpos( ltrim( $query ), 'DELETE ' ) ) {
			$name     = $args[0];
			$expected = $args[1];
			if ( ! array_key_exists( $name, $GLOBALS['fixture_options'] ) || maybe_serialize( $GLOBALS['fixture_options'][ $name ] ) !== $expected ) {
				return 0;
			}
			unset( $GLOBALS['fixture_options'][ $name ] );
			return 1;
		}
		throw new RuntimeException( 'Unexpected fixture SQL.' );
	}
}

$GLOBALS['wpdb'] = new FixtureWpdb();

function fixture_assert( $condition, $message ) {
	if ( ! $condition ) {
		throw new RuntimeException( $message );
	}
}

function add_action() {}
function add_filter() {}
function apply_filters( $hook, $value, ...$args ) {
	$GLOBALS['fixture_filter_calls'][] = $hook;
	if ( ! array_key_exists( $hook, $GLOBALS['fixture_filter_overrides'] ) ) return $value;
	$override = $GLOBALS['fixture_filter_overrides'][ $hook ];
	return is_callable( $override ) ? $override( $value, ...$args ) : $override;
}
function do_action( $hook ) { $GLOBALS['fixture_action_calls'][] = $hook; }
function register_post_type() {}
function register_rest_route() {}
function wp_cache_delete() {}
function wp_clear_scheduled_hook() {}
function wp_unslash( $value ) { return $value; }
function maybe_serialize( $value ) { return serialize( $value ); }
function wp_json_encode( $value, $flags = 0 ) { return json_encode( $value, $flags ); }
function wp_salt( $scheme = 'auth' ) { return 'fixture-salt-' . $scheme . '-not-a-secret'; }
function wp_parse_url( $url, $component = -1 ) { return parse_url( $url, $component ); }
function wp_parse_args( $args, $defaults = array() ) { return array_merge( $defaults, is_array( $args ) ? $args : array() ); }
function sanitize_key( $value ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $value ) ); }
function sanitize_text_field( $value ) { return trim( preg_replace( '/[\r\n\t ]+/', ' ', strip_tags( (string) $value ) ) ); }
function sanitize_textarea_field( $value ) { return trim( strip_tags( (string) $value ) ); }
function sanitize_email( $value ) { return filter_var( (string) $value, FILTER_SANITIZE_EMAIL ); }
function is_email( $value ) { return false !== filter_var( (string) $value, FILTER_VALIDATE_EMAIL ); }
function esc_url_raw( $value, $protocols = null ) {
	$url = filter_var( (string) $value, FILTER_VALIDATE_URL );
	if ( false === $url ) return '';
	$scheme = strtolower( (string) parse_url( $url, PHP_URL_SCHEME ) );
	return is_array( $protocols ) && ! in_array( $scheme, $protocols, true ) ? '' : $url;
}
function home_url() { return 'https://nad-lan.co.il/'; }
function is_ssl() { return true; }
function current_user_can() { return true; }
function post_password_required() { return false; }
function absint( $value ) { return abs( (int) $value ); }
function wp_mail() { $GLOBALS['fixture_mail_calls']++; return true; }
function get_user_by( $field, $value ) {
	return 'id' === $field && (int) $value > 0 ? (object) array( 'ID' => (int) $value, 'user_status' => 0 ) : false;
}
function get_transient( $key ) {
	return array_key_exists( $key, $GLOBALS['fixture_transients'] ) ? $GLOBALS['fixture_transients'][ $key ] : false;
}
function set_transient( $key, $value ) {
	$GLOBALS['fixture_transients'][ $key ] = $value;
	return true;
}

function add_option( $name, $value ) {
	if ( array_key_exists( $name, $GLOBALS['fixture_options'] ) ) return false;
	$GLOBALS['fixture_options'][ $name ] = $value;
	return true;
}

function get_option( $name, $default = false ) {
	return array_key_exists( $name, $GLOBALS['fixture_options'] ) ? $GLOBALS['fixture_options'][ $name ] : $default;
}

function update_option( $name, $value ) {
	$changed = ! array_key_exists( $name, $GLOBALS['fixture_options'] ) || $GLOBALS['fixture_options'][ $name ] !== $value;
	$GLOBALS['fixture_options'][ $name ] = $value;
	return $changed;
}

function delete_option( $name ) {
	if ( ! array_key_exists( $name, $GLOBALS['fixture_options'] ) ) return false;
	unset( $GLOBALS['fixture_options'][ $name ] );
	return true;
}

function get_page_by_path( $slug ) {
	foreach ( $GLOBALS['fixture_posts'] as $post ) {
		if ( $post->post_name === $slug ) return $post;
	}
	return null;
}

function get_post( $post_id ) {
	return isset( $GLOBALS['fixture_posts'][ $post_id ] ) ? $GLOBALS['fixture_posts'][ $post_id ] : null;
}

function wp_insert_post( $postarr ) {
	$post_id = ++$GLOBALS['fixture_next_post_id'];
	$post    = (object) array(
		'ID'         => $post_id,
		'post_title' => $postarr['post_title'],
		'post_name'  => $postarr['post_name'],
		'post_type'  => $postarr['post_type'],
	);
	$GLOBALS['fixture_posts'][ $post_id ] = $post;
	$GLOBALS['fixture_insert_count']++;
	return $post_id;
}

function update_post_meta( $post_id, $key, $value ) {
	if ( $GLOBALS['fixture_crash_once'] ) {
		$GLOBALS['fixture_crash_once'] = false;
		throw new RuntimeException( 'synthetic_crash_after_case_insert' );
	}
	if ( ! isset( $GLOBALS['fixture_post_meta'][ $post_id ] ) ) $GLOBALS['fixture_post_meta'][ $post_id ] = array();
	$GLOBALS['fixture_post_meta'][ $post_id ][ $key ] = $value;
	return true;
}

function get_post_meta( $post_id, $key, $single = false ) {
	return isset( $GLOBALS['fixture_post_meta'][ $post_id ][ $key ] ) ? $GLOBALS['fixture_post_meta'][ $post_id ][ $key ] : '';
}

function wp_next_scheduled() { return false; }
function wp_schedule_single_event( $timestamp, $hook, $args = array() ) {
	$GLOBALS['fixture_schedules'][] = array( $timestamp, $hook, $args );
	return true;
}

require __DIR__ . '/commercial-inquiry-routing.php';

final class FixtureRestRequest {
	private $headers;
	private $payload;
	public function __construct( $payload, $headers ) {
		$this->payload = $payload;
		$this->headers = array_change_key_case( $headers, CASE_LOWER );
	}
	public function get_header( $name ) {
		$name = strtolower( (string) $name );
		return isset( $this->headers[ $name ] ) ? $this->headers[ $name ] : '';
	}
	public function get_json_params() { return $this->payload; }
	public function get_body() { return json_encode( $this->payload ); }
}

fixture_assert( 'https://nad-lan.co.il' === nl_proposal_normalize_http_origin( 'https://NAD-LAN.CO.IL:443/' ), 'default HTTPS port must normalize to the full site origin' );
fixture_assert( 'https://nad-lan.co.il:8443' === nl_proposal_normalize_http_origin( 'https://nad-lan.co.il:8443' ), 'non-default port must remain part of the origin' );
fixture_assert( '' === nl_proposal_normalize_http_origin( 'https://nad-lan.co.il:8444/path' ), 'browser Origin with an application path must fail closed' );
fixture_assert( 'https://nad-lan.co.il:8444' === nl_proposal_normalize_http_origin( 'https://nad-lan.co.il:8444/wordpress/', true ), 'trusted home URL may supply an application path while retaining scheme, host, and port' );
fixture_assert( '' === nl_proposal_normalize_http_origin( 'https://user@nad-lan.co.il' ), 'credential-bearing origin must be rejected' );
fixture_assert( '' === nl_proposal_normalize_http_origin( 'https://nad-lan.co.il/?x=1' ), 'query-bearing origin must be rejected' );
fixture_assert( '/projects/toha/' === nl_proposal_rfp_page_path( 'https://nad-lan.co.il/projects/toha/?campaign=private#suite' ), 'same-origin page URL must reduce to a non-PII path' );
fixture_assert( is_wp_error( nl_proposal_rfp_page_path( 'https://nad-lan.co.il:8443/projects/toha/' ) ), 'page URL on a different port must fail the full-origin check' );
fixture_assert( is_wp_error( nl_proposal_rfp_page_path( 'https://buyer:secret@nad-lan.co.il/projects/toha/' ) ), 'credential-bearing page URL must fail closed' );

$hash      = hash( 'sha256', 'lock-fixture' );
$lock_name = 'nlp_rfp_lock_' . substr( $hash, 0, 40 );
$owner_a   = nl_proposal_acquire_commercial_rfp_lock( $hash );
fixture_assert( is_string( $owner_a ) && '' !== $owner_a, 'first worker must acquire the idempotency lock' );
$GLOBALS['fixture_options'][ $lock_name ]['expires_at'] = time() - 1;
$owner_b = nl_proposal_acquire_commercial_rfp_lock( $hash );
fixture_assert( is_string( $owner_b ) && $owner_b !== $owner_a, 'replacement worker must atomically own an expired lock' );
nl_proposal_release_commercial_rfp_lock( $hash, $owner_a );
fixture_assert( get_option( $lock_name )['token'] === $owner_b, 'stale worker must not release the replacement lock' );
nl_proposal_release_commercial_rfp_lock( $hash, $owner_b );
fixture_assert( null === get_option( $lock_name, null ), 'current owner must release its exact lock' );

$created_at = time();
$case_id    = 'NLC-ABCDEF0123456789ABCDEF01';
$signature  = hash( 'sha256', 'same-normalized-payload' );
$record     = array(
	'record_token' => $case_id,
	'signature'    => $signature,
	'state'        => 'reserved',
	'case_id'      => $case_id,
	'post_id'      => 0,
	'route_kind'   => 'project_team',
	'sla_hours'    => 8,
	'created_at'   => $created_at,
	'expires_at'   => $created_at + DAY_IN_SECONDS,
	'response'     => null,
);
fixture_assert( nl_proposal_write_commercial_rfp_idempotency_record( $hash, $record, true ), 'durable reservation must be written before case dispatch' );

$payload = array(
	'environment'         => 'production',
	'sandbox_post_id'     => null,
	'project_id'          => 991,
	'project_contract_id' => 'fixture-project',
	'asset'               => array(
		'building_id' => 'building-main',
		'tower_id'    => 'tower-main',
		'floor_id'    => 'floor-18',
		'suite_id'    => 'suite-18-a',
	),
	'contact'             => array( 'name' => 'Synthetic Fixture', 'email' => 'fixture@example.test' ),
);
$route = array(
	'kind'                => 'project_team',
	'team_key'            => 'fixture-team',
	'accountable_user_id' => 77,
	'sla_hours'           => 8,
);
$idempotency = array( 'hash' => $hash, 'signature' => $signature, 'created_at' => $created_at );

$GLOBALS['fixture_crash_once'] = true;
$crashed = false;
try {
	nl_proposal_store_commercial_rfp_case( $case_id, $payload, $route, $idempotency );
} catch ( RuntimeException $exception ) {
	$crashed = 'synthetic_crash_after_case_insert' === $exception->getMessage();
}
fixture_assert( $crashed, 'fixture must crash after durable case insertion' );
fixture_assert( 1 === $GLOBALS['fixture_insert_count'], 'crash window must contain exactly one inserted case' );

$post_id = nl_proposal_store_commercial_rfp_case( $case_id, $payload, $route, $idempotency );
fixture_assert( ! is_wp_error( $post_id ) && 701 === $post_id, 'retry must resume the deterministic existing case' );
fixture_assert( 1 === $GLOBALS['fixture_insert_count'], 'crash retry must not create a duplicate case' );
fixture_assert( get_post_meta( $post_id, '_nl_rfp_idempotency_signature', true ) === $signature, 'resumed case must retain the payload signature' );
fixture_assert( 'fixture-project' === get_post_meta( $post_id, '_nl_rfp_project_contract_id', true ), 'case must retain immutable project contract ID' );
fixture_assert( 'building-main' === get_post_meta( $post_id, '_nl_rfp_building_id', true ), 'case must retain immutable building ID' );
fixture_assert( 'tower-main' === get_post_meta( $post_id, '_nl_rfp_tower_id', true ), 'case must retain immutable tower ID' );

$record['post_id'] = $post_id;
$record['state']   = 'stored';
fixture_assert( nl_proposal_write_commercial_rfp_idempotency_record( $hash, $record ), 'stored state must update durably' );
$record['state']    = 'complete';
$record['response'] = array(
	'accepted'          => true,
	'case_id'           => $case_id,
	'status'            => 'received',
	'delivery_state'    => 'routed',
	'received_at'       => gmdate( 'c', $created_at ),
	'response_due_at'   => gmdate( 'c', $created_at + 8 * HOUR_IN_SECONDS ),
	'sla_hours'         => 8,
	'route_kind'        => 'project_team',
	'idempotent_replay' => false,
);
fixture_assert( nl_proposal_write_commercial_rfp_idempotency_record( $hash, $record ), 'safe complete replay record must persist' );
fixture_assert( nl_proposal_get_commercial_rfp_idempotency_record( $hash )['post_id'] === $post_id, 'replay must resolve the exact stored case' );

$malformed_name = nl_proposal_commercial_rfp_idempotency_option_name( hash( 'sha256', 'malformed' ) );
$GLOBALS['fixture_options'][ $malformed_name ] = array( 'expires_at' => PHP_INT_MAX );
fixture_assert( null === nl_proposal_get_commercial_rfp_idempotency_record( hash( 'sha256', 'malformed' ) ), 'malformed durable record must fail closed without field access' );

$expired_hash = hash( 'sha256', 'record-token-fixture' );
$expired      = $record;
$expired['record_token'] = 'NLC-111111111111111111111111';
$expired['case_id']      = $expired['record_token'];
$expired['created_at']   = time() - 100;
$expired['expires_at']   = time() - 1;
$expired['response']     = null;
$expired['state']        = 'reserved';
$expired['post_id']      = 0;
fixture_assert( nl_proposal_write_commercial_rfp_idempotency_record( $expired_hash, $expired, true ), 'expired fixture record must be stored' );
$replacement = $expired;
$replacement['record_token'] = 'NLC-222222222222222222222222';
$replacement['case_id']      = $replacement['record_token'];
update_option( nl_proposal_commercial_rfp_idempotency_option_name( $expired_hash ), $replacement, false );
nl_proposal_delete_commercial_rfp_idempotency_record( $expired_hash, $expired['record_token'] );
fixture_assert( nl_proposal_get_commercial_rfp_idempotency_record( $expired_hash )['case_id'] === $replacement['case_id'], 'stale cleanup token must not delete a replacement replay record' );

// The private sandbox uses a separate signed test endpoint. It validates the
// full composer payload and idempotency semantics but can never resolve a real
// route, store a case, call wp_mail, invoke CRM hooks or publish PII analytics.
$sandbox_post_id = 55;
$GLOBALS['fixture_posts'][ $sandbox_post_id ] = (object) array(
	'ID'            => $sandbox_post_id,
	'post_status'   => 'private',
	'post_password' => '',
	'post_type'     => 'page',
	'post_name'     => 'sandbox-commercial-fixture',
	'post_title'    => 'Sandbox fixture',
);
$GLOBALS['fixture_post_meta'][ $sandbox_post_id ]['_nl_commercial_scene_sandbox_enabled'] = '1';
$sandbox_nonce = nl_proposal_create_commercial_rfp_sandbox_nonce( $sandbox_post_id, 300 );
fixture_assert( '' !== $sandbox_nonce, 'authenticated guarded sandbox must receive a signed nonce' );
$sandbox_payload = array(
	'schema_version'      => NL_PROPOSAL_RFP_SCHEMA_VERSION,
	'environment'         => 'test',
	'sandbox_post_id'     => $sandbox_post_id,
	'project_id'          => 999999,
	'project_contract_id' => 'fixture-commercial-project',
	'asset'               => array(
		'building_id' => 'building-main',
		'tower_id'    => 'tower-main',
		'floor_id'    => 'level-10',
		'suite_id'    => null,
	),
	'locale'              => 'en',
	'company'             => array(
		'name'                 => 'Synthetic Company',
		'registration_country' => 'US',
		'website'              => 'https://example.test/',
		'size_band'            => '51-200',
	),
	'contact'             => array(
		'name'              => 'Synthetic Buyer',
		'role'              => 'Operations',
		'email'             => 'buyer@example.test',
		'phone'             => '',
		'preferred_channel' => 'email',
	),
	'requirements'        => array(
		'headcount'           => 75,
		'target_move_in'      => '2027-01',
		'lease_term_months'   => 60,
		'area_min_sqm'        => 500,
		'area_max_sqm'        => 900,
		'budget_monthly'      => null,
		'budget_currency'     => '',
		'attendance_ratio_pct'=> 65,
		'special_uses'        => array( 'standard_office' ),
	),
	'question_ids'        => array( 'live_availability' ),
	'document_ids'        => array( 'availability_schedule' ),
	'question_text'       => '',
	'consent'             => array(
		'privacy'     => true,
		'terms'       => true,
		'marketing'   => false,
		'text_version'=> NL_PROPOSAL_RFP_CONSENT_VERSION,
	),
	'page_url'            => 'https://nad-lan.co.il/projects/sandbox-unit-scene/',
	'website_confirm'     => '',
);

// Stable, non-PII recovery contracts let the five-step composer return to the
// exact control instead of trapping the buyer behind a generic retry message.
function fixture_assert_field_error( $payload, $expected_field, $message ) {
	$error = nl_proposal_normalize_commercial_rfp_payload( $payload );
	fixture_assert( is_wp_error( $error ) && 'invalid_field' === $error->get_error_code(), $message . ' must use the stable invalid_field code' );
	$data = $error->get_error_data();
	fixture_assert( is_array( $data ) && $expected_field === $data['field'] && 422 === $data['status'], $message . ' must expose only its safe canonical field path' );
}

$invalid = $sandbox_payload;
$invalid['company']['name'] = '';
fixture_assert_field_error( $invalid, 'company.name', 'missing company name' );
$invalid = $sandbox_payload;
$invalid['contact']['email'] = 'not-an-email';
fixture_assert_field_error( $invalid, 'contact.email', 'invalid email' );
$invalid = $sandbox_payload;
$invalid['contact']['email'] = '';
$invalid['contact']['phone'] = '12';
$invalid['contact']['preferred_channel'] = 'phone';
fixture_assert_field_error( $invalid, 'contact.phone', 'invalid phone' );
$invalid = $sandbox_payload;
$invalid['requirements']['headcount'] = 'many';
fixture_assert_field_error( $invalid, 'requirements.headcount', 'invalid headcount' );
$invalid = $sandbox_payload;
$invalid['requirements']['target_move_in'] = 'January';
fixture_assert_field_error( $invalid, 'requirements.target_move_in', 'invalid move-in month' );
$invalid = $sandbox_payload;
$invalid['question_ids'] = array( 'not_in_allowlist' );
fixture_assert_field_error( $invalid, 'question_ids', 'invalid question ID' );
$invalid = $sandbox_payload;
$invalid['document_ids'] = array( 'not_in_allowlist' );
fixture_assert_field_error( $invalid, 'document_ids', 'invalid document ID' );
$invalid = $sandbox_payload;
$invalid['question_text'] = array( 'not', 'text' );
fixture_assert_field_error( $invalid, 'question_text', 'invalid written question' );
$invalid = $sandbox_payload;
$invalid['consent']['marketing'] = 'yes';
fixture_assert_field_error( $invalid, 'consent.marketing', 'invalid marketing consent' );
$invalid = $sandbox_payload;
$invalid['consent']['privacy'] = false;
$consent_required = nl_proposal_normalize_commercial_rfp_payload( $invalid );
fixture_assert( is_wp_error( $consent_required ) && 'consent_required' === $consent_required->get_error_code(), 'missing required consent must keep its stable consent_required code' );
fixture_assert( 'consent.privacy' === $consent_required->get_error_data()['field'], 'missing required consent must focus the privacy control without echoing buyer data' );
$invalid = $sandbox_payload;
$invalid['consent']['text_version'] = 'expired-fixture-version';
$consent_expired = nl_proposal_normalize_commercial_rfp_payload( $invalid );
fixture_assert( is_wp_error( $consent_expired ) && 'consent_version_expired' === $consent_expired->get_error_code(), 'stale consent must use the stable consent_version_expired code' );
$consent_data = $consent_expired->get_error_data();
fixture_assert( NL_PROPOSAL_RFP_CONSENT_VERSION === $consent_data['current_consent_version'], 'stale consent response must safely expose the current version for in-place recovery' );
fixture_assert( 'consent.privacy' === $consent_data['field'] && 409 === $consent_data['status'], 'stale consent recovery must return to the privacy control' );

$sandbox_headers = array(
	'content-type'            => 'application/json',
	'origin'                  => 'https://nad-lan.co.il',
	'idempotency-key'         => 'fixture-sandbox-intent-0001',
	'x-nadlan-sandbox-nonce'  => $sandbox_nonce,
);
$invalid_nonce_request = new FixtureRestRequest( $sandbox_payload, array_merge( $sandbox_headers, array( 'x-nadlan-sandbox-nonce' => 'invalid' ) ) );
$invalid_nonce = nl_proposal_commercial_rfp_sandbox_permission_check( $invalid_nonce_request );
fixture_assert( is_wp_error( $invalid_nonce ) && 'sandbox_rejected' === $invalid_nonce->get_error_code(), 'invalid sandbox nonce must receive one opaque rejection' );
$invalid_environment_payload = $sandbox_payload;
$invalid_environment_payload['environment'] = 'production';
$invalid_environment = nl_proposal_commercial_rfp_sandbox_permission_check( new FixtureRestRequest( $invalid_environment_payload, $sandbox_headers ) );
fixture_assert( is_wp_error( $invalid_environment ) && 'sandbox_rejected' === $invalid_environment->get_error_code(), 'non-test sandbox environment must receive the same opaque rejection' );

$GLOBALS['fixture_filter_calls'] = array();
$GLOBALS['fixture_action_calls'] = array();
$sandbox_request = new FixtureRestRequest( $sandbox_payload, $sandbox_headers );
fixture_assert( true === nl_proposal_commercial_rfp_sandbox_permission_check( $sandbox_request ), 'signed same-origin test request must pass the sandbox permission gate' );
$sandbox_response = nl_proposal_handle_commercial_rfp_sandbox_request( $sandbox_request );
fixture_assert(
	$sandbox_response instanceof WP_REST_Response && 202 === $sandbox_response->get_status(),
	'first sandbox intent must return a synthetic accepted response' . ( is_wp_error( $sandbox_response ) ? ': ' . $sandbox_response->get_error_code() . ' ' . $sandbox_response->get_error_message() : '' )
);
$sandbox_body = $sandbox_response->get_data();
fixture_assert( 0 === strpos( $sandbox_body['case_id'], 'TEST-' ), 'sandbox case ID must be visibly synthetic' );
fixture_assert( 'test_sink' === $sandbox_body['route_kind'] && 'test_sink' === $sandbox_body['route_status'], 'sandbox route is hard-bound to the test sink' );
fixture_assert( 'test_sink' === $sandbox_body['delivery_state'], 'sandbox must never claim real delivery' );
fixture_assert( 0 === $GLOBALS['fixture_mail_calls'], 'sandbox handler must never call wp_mail' );
fixture_assert( 1 === $GLOBALS['fixture_insert_count'], 'sandbox handler must not insert any additional case post' );
fixture_assert( ! in_array( 'nl_proposal_commercial_rfp_project_route', $GLOBALS['fixture_filter_calls'], true ), 'sandbox must not resolve a project mailbox' );
fixture_assert( ! in_array( 'nl_proposal_commercial_rfp_desk_route', $GLOBALS['fixture_filter_calls'], true ), 'sandbox must not resolve the fallback desk' );
fixture_assert( ! in_array( 'nl_proposal_commercial_asset_exists', $GLOBALS['fixture_filter_calls'], true ), 'sandbox must not invoke production inventory/CRM target hooks' );
fixture_assert( ! in_array( 'nl_proposal_commercial_rfp_analytics_safe', $GLOBALS['fixture_action_calls'], true ), 'sandbox must not emit production analytics' );

$replay_response = nl_proposal_handle_commercial_rfp_sandbox_request( $sandbox_request );
$replay_body = $replay_response->get_data();
fixture_assert( 200 === $replay_response->get_status() && true === $replay_body['idempotent_replay'], 'same sandbox intent must replay the exact synthetic case' );
fixture_assert( $sandbox_body['case_id'] === $replay_body['case_id'], 'sandbox retry must not create a second synthetic case' );
$changed_payload = $sandbox_payload;
$changed_payload['question_text'] = 'Changed intent';
$conflict = nl_proposal_handle_commercial_rfp_sandbox_request( new FixtureRestRequest( $changed_payload, $sandbox_headers ) );
fixture_assert( is_wp_error( $conflict ) && 'idempotency_conflict' === $conflict->get_error_code(), 'changed payload with a frozen key must fail as an idempotency conflict' );

// A completed production acceptance is an immutable acknowledgement. Exact
// retries must recover that same opaque case before current consent,
// publication, inventory or route state is consulted. New intent is not
// grandfathered and must traverse every current gate.
$production_project_id = 991;
$GLOBALS['fixture_posts'][ $production_project_id ] = (object) array(
	'ID'          => $production_project_id,
	'post_status' => 'publish',
	'post_type'   => 'project',
	'post_name'   => 'fixture-commercial-project',
	'post_title'  => 'Fixture commercial project',
);
$GLOBALS['fixture_post_meta'][ $production_project_id ] = array(
	'_nl_asset_type'                       => 'commercial_office',
	'_nl_commercial_project_contract_id'   => 'fixture-commercial-project',
	'_nl_commercial_rfp_route_enabled'     => '1',
	'_nl_commercial_rfp_team_key'          => 'fixture-team',
	'_nl_commercial_rfp_mailbox'           => 'commercial@example.test',
	'_nl_commercial_rfp_accountable_user_id'=> 77,
	'_nl_commercial_rfp_sla_hours'         => 8,
	'_nl_commercial_rfp_route_verified_at' => gmdate( 'c', time() - 60 ),
	'_nl_commercial_rfp_route_expires_at'  => gmdate( 'c', time() + DAY_IN_SECONDS ),
);
$GLOBALS['fixture_filter_overrides']['nl_proposal_commercial_asset_exists'] = true;

$production_payload = $sandbox_payload;
$production_payload['environment']         = 'production';
$production_payload['sandbox_post_id']     = null;
$production_payload['project_id']          = $production_project_id;
$production_payload['project_contract_id'] = 'fixture-commercial-project';
$production_payload['page_url']            = 'https://nad-lan.co.il/projects/toha/';
$production_headers = array(
	'content-type'    => 'application/json',
	'origin'          => 'https://nad-lan.co.il',
	'idempotency-key' => 'fixture-production-intent-0001',
);
$production_request = new FixtureRestRequest( $production_payload, $production_headers );
$accepted = nl_proposal_handle_commercial_rfp_request( $production_request );
fixture_assert(
	$accepted instanceof WP_REST_Response && 202 === $accepted->get_status(),
	'first production intent must be accepted before replay-state mutation' . ( is_wp_error( $accepted ) ? ': ' . $accepted->get_error_code() : '' )
);
$accepted_body = $accepted->get_data();
fixture_assert( 0 === strpos( $accepted_body['case_id'], 'NLC-' ), 'production acceptance must expose only its opaque case ID' );
$insert_count_after_acceptance = $GLOBALS['fixture_insert_count'];

// Rotate all mutable acceptance gates after the case was safely accepted.
$GLOBALS['fixture_filter_overrides']['nl_proposal_commercial_rfp_consent_version'] = 'commercial-rfp-2026-08-11-v2';
$GLOBALS['fixture_filter_overrides']['nl_proposal_commercial_asset_exists'] = false;
$GLOBALS['fixture_posts'][ $production_project_id ]->post_status = 'draft';
$GLOBALS['fixture_post_meta'][ $production_project_id ]['_nl_commercial_rfp_route_enabled'] = '';
$GLOBALS['fixture_filter_calls'] = array();

$replayed_after_mutation = nl_proposal_handle_commercial_rfp_request( $production_request );
fixture_assert( $replayed_after_mutation instanceof WP_REST_Response && 200 === $replayed_after_mutation->get_status(), 'exact accepted retry must replay before mutable gates' );
$replayed_after_mutation_body = $replayed_after_mutation->get_data();
fixture_assert( true === $replayed_after_mutation_body['idempotent_replay'], 'accepted retry after mutation must be labelled as replay' );
fixture_assert( $accepted_body['case_id'] === $replayed_after_mutation_body['case_id'], 'accepted retry after mutation must return the exact same case' );
fixture_assert( ! in_array( 'nl_proposal_commercial_rfp_consent_version', $GLOBALS['fixture_filter_calls'], true ), 'completed replay must not consult rotated consent' );
fixture_assert( ! in_array( 'nl_proposal_commercial_asset_exists', $GLOBALS['fixture_filter_calls'], true ), 'completed replay must not consult disabled inventory' );

// Associative JSON member order is not intent. The canonical signature must
// still replay the same accepted case when the parser supplies a new key order.
$reordered_payload = array_reverse( $production_payload, true );
$reordered_replay = nl_proposal_handle_commercial_rfp_request( new FixtureRestRequest( $reordered_payload, $production_headers ) );
fixture_assert( $reordered_replay instanceof WP_REST_Response && $accepted_body['case_id'] === $reordered_replay->get_data()['case_id'], 'canonical key ordering must retain exact accepted replay' );

$changed_production_payload = $production_payload;
$changed_production_payload['question_text'] = 'Changed intent after acceptance';
$changed_production = nl_proposal_handle_commercial_rfp_request( new FixtureRestRequest( $changed_production_payload, $production_headers ) );
fixture_assert( is_wp_error( $changed_production ) && 'idempotency_conflict' === $changed_production->get_error_code(), 'changed body with accepted key must receive opaque 409 even after mutable gates change' );
$changed_error_data = $changed_production->get_error_data();
fixture_assert( array( 'status' => 409 ) === $changed_error_data, 'idempotency conflict must not disclose the prior case or request' );

$new_key_headers = $production_headers;
$new_key_headers['idempotency-key'] = 'fixture-production-intent-0002';
$new_old_consent = nl_proposal_handle_commercial_rfp_request( new FixtureRestRequest( $production_payload, $new_key_headers ) );
fixture_assert( is_wp_error( $new_old_consent ) && 'consent_version_expired' === $new_old_consent->get_error_code(), 'new intent must use the rotated current consent gate' );
$new_current_payload = $production_payload;
$new_current_payload['consent']['text_version'] = 'commercial-rfp-2026-08-11-v2';
$new_key_headers['idempotency-key'] = 'fixture-production-intent-0003';
$new_unpublished = nl_proposal_handle_commercial_rfp_request( new FixtureRestRequest( $new_current_payload, $new_key_headers ) );
fixture_assert( is_wp_error( $new_unpublished ) && 'invalid_project' === $new_unpublished->get_error_code(), 'new intent with current consent must still fail the current publication gate' );
fixture_assert( $insert_count_after_acceptance === $GLOBALS['fixture_insert_count'], 'replay, conflict and rejected new intent must never create another case' );

echo "PASS inquiry durability + sandbox fixture: owned locks, crash/resume one-case guarantee, exact tower tuple, stable field/consent recovery, signed opaque test gate, hard test sink, no mail/CRM/analytics, canonical pre-validation signature, immutable accepted replay after consent/inventory/publication/route mutation, and opaque changed-body conflict.\n";
