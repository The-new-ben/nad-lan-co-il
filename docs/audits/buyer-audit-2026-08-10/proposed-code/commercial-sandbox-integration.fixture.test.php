<?php
/**
 * PROPOSAL ONLY — NOT APPLIED.
 * Executable fixture for the guarded classic-WordPress enqueue seam.
 */

declare(strict_types=1);

define( 'ABSPATH', __DIR__ . DIRECTORY_SEPARATOR );
define( 'NL_PROPOSAL_COMMERCIAL_SCENE_SANDBOX', true );
define( 'NL_PROPOSAL_RFP_CONSENT_VERSION', 'fixture-consent-v1' );
$fixture_arguments              = isset( $argv ) && is_array( $argv ) ? $argv : array();
$fixture_predefined_cache_false = in_array( '--predefined-cache-false', $fixture_arguments, true );
if ( $fixture_predefined_cache_false ) {
	define( 'DONOTCACHEPAGE', false );
}

$GLOBALS['fixture_request'] = array(
	'admin'    => false,
	'singular' => true,
	'post_id'  => 55,
	'meta'     => '0',
	'status'   => 'publish',
	'password' => '',
	'authenticated' => false,
);
$GLOBALS['fixture_registered_styles'] = array( 'nadlan-engine-css' => true );
$GLOBALS['fixture_registered_scripts'] = array( 'nadlan-engine-i18n' => true, 'nadlan-engine-core' => true );
$GLOBALS['fixture_styles']      = array();
$GLOBALS['fixture_inline']      = array();
$GLOBALS['fixture_scripts']     = array();
$GLOBALS['fixture_localized']   = array();
$GLOBALS['fixture_actions']     = array();
$GLOBALS['fixture_hooks']       = array();
$GLOBALS['fixture_inline_ok']   = true;
$GLOBALS['fixture_nonce_requests'] = array();
$GLOBALS['fixture_nocache_calls']  = 0;
$GLOBALS['fixture_force_headers_sent']  = false;
$GLOBALS['fixture_force_header_failure'] = false;

function fixture_assert( $condition, $message ) {
	if ( ! $condition ) throw new RuntimeException( $message );
}

function add_filter( $hook, $callback, $priority = 10 ) {
	$GLOBALS['fixture_hooks'][] = array( 'filter', $hook, $callback, $priority );
}
function add_action( $hook, $callback, $priority = 10 ) {
	$GLOBALS['fixture_hooks'][] = array( 'action', $hook, $callback, $priority );
}
function apply_filters( $hook, $value ) {
	if ( 'nl_proposal_commercial_scene_sandbox_force_headers_sent' === $hook && $GLOBALS['fixture_force_headers_sent'] ) {
		return true;
	}
	if ( 'nl_proposal_commercial_scene_sandbox_header_write_failed' === $hook && $GLOBALS['fixture_force_header_failure'] ) {
		return true;
	}
	return $value;
}
function do_action( $hook, $payload = null ) {
	$GLOBALS['fixture_actions'][] = array( $hook, $payload );
}
function nocache_headers() { $GLOBALS['fixture_nocache_calls']++; }
function is_admin() { return $GLOBALS['fixture_request']['admin']; }
function is_singular() { return $GLOBALS['fixture_request']['singular']; }
function get_queried_object_id() { return $GLOBALS['fixture_request']['post_id']; }
function get_post_meta( $post_id = 0, $key = '', $single = false ) { return $GLOBALS['fixture_request']['meta']; }
function get_post_status( $post_id = 0 ) { return $GLOBALS['fixture_request']['status']; }
function get_post_field( $field = '', $post_id = 0 ) { return $GLOBALS['fixture_request']['password']; }
function nl_proposal_commercial_rfp_sandbox_context_allowed( $post_id ) {
	if ( (int) $post_id !== (int) $GLOBALS['fixture_request']['post_id'] || '1' !== $GLOBALS['fixture_request']['meta'] ) return false;
	if ( 'private' === $GLOBALS['fixture_request']['status'] ) return true === $GLOBALS['fixture_request']['authenticated'];
	return '' !== $GLOBALS['fixture_request']['password'] && true === $GLOBALS['fixture_request']['authenticated'];
}
function nl_proposal_create_commercial_rfp_sandbox_nonce( $post_id ) {
	$GLOBALS['fixture_nonce_requests'][] = (int) $post_id;
	return nl_proposal_commercial_rfp_sandbox_context_allowed( $post_id ) ? '1700000000.' . str_repeat( 'a', 64 ) : '';
}
function plugin_dir_path() { return __DIR__ . DIRECTORY_SEPARATOR; }
function plugin_dir_url() { return 'https://nad-lan.co.il/proposal-assets/'; }
function wp_style_is( $handle, $state ) { return 'registered' === $state && ! empty( $GLOBALS['fixture_registered_styles'][ $handle ] ); }
function wp_script_is( $handle, $state ) { return 'registered' === $state && ! empty( $GLOBALS['fixture_registered_scripts'][ $handle ] ); }
function wp_enqueue_style( $handle ) { $GLOBALS['fixture_styles'][] = $handle; }
function wp_add_inline_style( $handle, $css ) {
	if ( ! $GLOBALS['fixture_inline_ok'] ) return false;
	$GLOBALS['fixture_inline'][] = array( 'handle' => $handle, 'css' => $css );
	return true;
}
function wp_enqueue_script( $handle, $src, $dependencies, $version, $footer ) {
	$GLOBALS['fixture_scripts'][ $handle ] = array(
		'src'          => $src,
		'dependencies' => $dependencies,
		'version'      => $version,
		'footer'       => $footer,
	);
}
function wp_localize_script( $handle, $name, $value ) {
	$GLOBALS['fixture_localized'][ $handle ] = array( 'name' => $name, 'value' => $value );
	return true;
}
function rest_url( $path ) { return 'https://nad-lan.co.il/wp-json/' . ltrim( $path, '/' ); }
function esc_url_raw( $url ) { return $url; }

function fixture_reset_enqueue_state() {
	$GLOBALS['fixture_styles']         = array();
	$GLOBALS['fixture_inline']         = array();
	$GLOBALS['fixture_scripts']        = array();
	$GLOBALS['fixture_localized']      = array();
	$GLOBALS['fixture_actions']        = array();
	$GLOBALS['fixture_nonce_requests'] = array();
	$GLOBALS['fixture_nocache_calls']  = 0;
}

function fixture_expected_sandbox_headers() {
	return array(
		'Cache-Control' => 'private, no-store, no-cache, must-revalidate, max-age=0',
		'Pragma'       => 'no-cache',
		'Expires'      => 'Wed, 11 Jan 1984 05:00:00 GMT',
		'X-Robots-Tag' => 'noindex, nofollow, noarchive',
	);
}

function fixture_render_sandbox_response() {
	fixture_reset_enqueue_state();
	$headers = nl_proposal_commercial_scene_sandbox_headers();
	nl_proposal_enqueue_commercial_scene_sandbox();
	return array(
		'authorized'     => nl_proposal_is_commercial_scene_sandbox_request(),
		'body_kind'      => empty( $GLOBALS['fixture_localized'] ) ? 'password-challenge' : 'authenticated-sandbox-html',
		'headers'        => $headers,
		'styles'         => $GLOBALS['fixture_styles'],
		'inline'         => $GLOBALS['fixture_inline'],
		'scripts'        => $GLOBALS['fixture_scripts'],
		'localized'      => $GLOBALS['fixture_localized'],
		'nonce_requests' => $GLOBALS['fixture_nonce_requests'],
		'nocache_calls'  => $GLOBALS['fixture_nocache_calls'],
	);
}

function fixture_shared_cache_eligible( $response ) {
	if ( ! isset( $response['headers']['Cache-Control'] ) ) return true;
	$cache_control = strtolower( (string) $response['headers']['Cache-Control'] );
	return false === strpos( $cache_control, 'private' )
		&& false === strpos( $cache_control, 'no-store' )
		&& false === strpos( $cache_control, 'no-cache' );
}

function fixture_shared_cache_fetch( &$cache, $key ) {
	if ( isset( $cache[ $key ] ) ) {
		return array( 'source' => 'shared-cache', 'response' => $cache[ $key ] );
	}
	$response = fixture_render_sandbox_response();
	if ( fixture_shared_cache_eligible( $response ) ) {
		$cache[ $key ] = $response;
	}
	return array( 'source' => 'origin', 'response' => $response );
}

require __DIR__ . '/commercial-sandbox-integration.php';

if ( $fixture_predefined_cache_false ) {
	$GLOBALS['fixture_request']['meta']          = '1';
	$GLOBALS['fixture_request']['status']        = 'publish';
	$GLOBALS['fixture_request']['password']      = 'fixture-password-hash';
	$GLOBALS['fixture_request']['authenticated'] = true;
	fixture_assert( nl_proposal_is_commercial_scene_sandbox_request(), 'the conflict fixture must otherwise satisfy authenticated sandbox access' );
	fixture_assert( false === nl_proposal_commercial_scene_sandbox_disable_page_cache(), 'a pre-existing false cache constant must remain a fail-closed conflict' );
	fixture_assert( defined( 'DONOTCACHEPAGE' ) && false === DONOTCACHEPAGE, 'the integration must never redefine a host-supplied DONOTCACHEPAGE value' );
	fixture_assert( fixture_expected_sandbox_headers() === nl_proposal_commercial_scene_sandbox_headers(), 'the conflict response must still emit the explicit private/no-store header set' );
	fixture_assert( 1 === $GLOBALS['fixture_nocache_calls'], 'the conflict response must still invoke WordPress no-cache headers' );
	fixture_reset_enqueue_state();
	nl_proposal_enqueue_commercial_scene_sandbox();
	fixture_assert( array() === $GLOBALS['fixture_styles'] && array() === $GLOBALS['fixture_scripts'] && array() === $GLOBALS['fixture_localized'], 'a false cache constant must block all protected assets and configuration' );
	fixture_assert( array() === $GLOBALS['fixture_nonce_requests'], 'a false cache constant must block signed nonce creation' );
	fixture_assert( 'page_cache_suppression_unavailable' === $GLOBALS['fixture_actions'][0][1]['reason'], 'a false cache constant must emit the dedicated fail-closed reason' );
	echo "PASS sandbox integration cache-conflict fixture: no unsafe DONOTCACHEPAGE redefinition, explicit no-store headers, and authenticated payload blocked.\n";
	exit( 0 );
}

$expected_hooks = array(
	array( 'filter', 'wp_robots', 'nl_proposal_commercial_scene_sandbox_robots', 10 ),
	array( 'action', 'wp', 'nl_proposal_commercial_scene_sandbox_disable_page_cache', 0 ),
	array( 'action', 'template_redirect', 'nl_proposal_commercial_scene_sandbox_headers', PHP_INT_MAX ),
	array( 'action', 'wp_enqueue_scripts', 'nl_proposal_enqueue_commercial_scene_sandbox', 99 ),
);
fixture_assert( $expected_hooks === $GLOBALS['fixture_hooks'], 'integration must register only the scoped robots, cache, header, and enqueue hooks' );
fixture_assert( ! defined( 'DONOTCACHEPAGE' ), 'loading the integration alone must not leak a no-cache constant onto unrelated pages' );
fixture_assert( ! nl_proposal_is_commercial_scene_sandbox_page(), 'an unflagged page must not be treated as a protected sandbox page' );
fixture_assert( ! nl_proposal_is_commercial_scene_sandbox_request(), 'an unflagged page must not receive protected sandbox content' );
fixture_assert( false === nl_proposal_commercial_scene_sandbox_disable_page_cache(), 'an unflagged page must not activate the page-cache seam' );
nl_proposal_enqueue_commercial_scene_sandbox();
fixture_assert( array() === $GLOBALS['fixture_styles'] && array() === $GLOBALS['fixture_scripts'], 'public unflagged pages must enqueue nothing' );
fixture_assert( array() === $GLOBALS['fixture_actions'], 'public unflagged pages must not emit sandbox operational hooks' );
fixture_assert( array( 'index' => true ) === nl_proposal_commercial_scene_sandbox_robots( array( 'index' => true ) ), 'public robots directives must be untouched' );
fixture_assert( array() === nl_proposal_commercial_scene_sandbox_headers(), 'public unflagged pages must receive no sandbox cache or crawler headers' );
fixture_assert( 0 === $GLOBALS['fixture_nocache_calls'], 'public unflagged pages must not invoke WordPress no-cache headers' );
fixture_assert( ! defined( 'DONOTCACHEPAGE' ), 'public unflagged callbacks must not define DONOTCACHEPAGE' );
fixture_assert( ! nl_proposal_commercial_scene_sandbox_cache_headers_ready(), 'public unflagged callbacks must not mark protected cache headers ready' );

$GLOBALS['fixture_request']['meta']   = '1';
$GLOBALS['fixture_request']['status'] = 'publish';
$GLOBALS['fixture_request']['password'] = '';
$GLOBALS['fixture_request']['authenticated'] = true;
fixture_assert( ! nl_proposal_is_commercial_scene_sandbox_page(), 'a flagged public post with an empty password must fail the non-content predicate closed' );
fixture_assert( ! nl_proposal_is_commercial_scene_sandbox_request(), 'an empty password must never grant protected sandbox content access' );
fixture_assert( false === nl_proposal_commercial_scene_sandbox_disable_page_cache(), 'an empty-password public post must not activate sandbox cache controls' );
fixture_assert( array( 'index' => true ) === nl_proposal_commercial_scene_sandbox_robots( array( 'index' => true ) ), 'an empty-password public post must retain its existing robots directives' );
fixture_assert( array() === nl_proposal_commercial_scene_sandbox_headers(), 'an empty-password public post must not receive sandbox cache or crawler headers' );
fixture_assert( 0 === $GLOBALS['fixture_nocache_calls'], 'an empty-password public post must not invoke WordPress no-cache headers' );
fixture_assert( ! defined( 'DONOTCACHEPAGE' ), 'an empty-password public post must not define DONOTCACHEPAGE' );
fixture_assert( ! nl_proposal_commercial_scene_sandbox_cache_headers_ready(), 'an empty-password public post must not mark protected cache headers ready' );
fixture_reset_enqueue_state();
nl_proposal_enqueue_commercial_scene_sandbox();
fixture_assert( array() === $GLOBALS['fixture_styles'] && array() === $GLOBALS['fixture_scripts'] && array() === $GLOBALS['fixture_localized'], 'an empty-password public post must receive no proposal assets or configuration' );
fixture_assert( array() === $GLOBALS['fixture_nonce_requests'], 'an empty-password public post must not request a signed nonce' );
fixture_assert( array() === $GLOBALS['fixture_actions'], 'an empty-password public post must not emit sandbox operational hooks' );

$GLOBALS['fixture_request']['password'] = 'fixture-password-hash';
$GLOBALS['fixture_request']['authenticated'] = true;
fixture_reset_enqueue_state();
$GLOBALS['fixture_force_headers_sent'] = true;
fixture_assert( array() === nl_proposal_commercial_scene_sandbox_headers(), 'a headers-sent response must fail before emitting sandbox cache headers' );
fixture_assert( 0 === $GLOBALS['fixture_nocache_calls'], 'a headers-sent response must not claim WordPress no-cache headers ran' );
fixture_assert( ! nl_proposal_commercial_scene_sandbox_cache_headers_ready(), 'a headers-sent response must leave exact-header readiness false' );
nl_proposal_enqueue_commercial_scene_sandbox();
fixture_assert( array() === $GLOBALS['fixture_styles'] && array() === $GLOBALS['fixture_inline'] && array() === $GLOBALS['fixture_scripts'], 'headers_sent must block every authenticated proposal asset' );
fixture_assert( array() === $GLOBALS['fixture_localized'] && array() === $GLOBALS['fixture_nonce_requests'], 'headers_sent must block authenticated config and nonce creation' );
fixture_assert( 'response_cache_headers_unavailable' === $GLOBALS['fixture_actions'][0][1]['reason'], 'headers_sent must emit the dedicated response-header block reason' );
$GLOBALS['fixture_force_headers_sent'] = false;

fixture_reset_enqueue_state();
$GLOBALS['fixture_force_header_failure'] = true;
fixture_assert( array() === nl_proposal_commercial_scene_sandbox_headers(), 'an explicit header-write failure must fail the exact-header seam' );
fixture_assert( 1 === $GLOBALS['fixture_nocache_calls'], 'a header-write failure may occur only after WordPress no-cache headers run' );
fixture_assert( ! nl_proposal_commercial_scene_sandbox_cache_headers_ready(), 'a header-write failure must leave exact-header readiness false' );
nl_proposal_enqueue_commercial_scene_sandbox();
fixture_assert( array() === $GLOBALS['fixture_styles'] && array() === $GLOBALS['fixture_inline'] && array() === $GLOBALS['fixture_scripts'], 'a header-write failure must block every authenticated proposal asset' );
fixture_assert( array() === $GLOBALS['fixture_localized'] && array() === $GLOBALS['fixture_nonce_requests'], 'a header-write failure must block authenticated config and nonce creation' );
fixture_assert( 'response_cache_headers_unavailable' === $GLOBALS['fixture_actions'][0][1]['reason'], 'a header-write failure must emit the dedicated response-header block reason' );
$GLOBALS['fixture_force_header_failure'] = false;

fixture_reset_enqueue_state();
$GLOBALS['fixture_request']['authenticated'] = false;
fixture_assert( nl_proposal_is_commercial_scene_sandbox_page(), 'the explicitly flagged password challenge must match the non-content sandbox predicate before authentication' );
fixture_assert( ! nl_proposal_is_commercial_scene_sandbox_request(), 'the password challenge must not pass the authenticated content predicate' );
fixture_assert( nl_proposal_commercial_scene_sandbox_disable_page_cache(), 'the password challenge must set the guarded page-cache constant before authentication' );
fixture_assert( defined( 'DONOTCACHEPAGE' ) && true === DONOTCACHEPAGE, 'the protected password challenge must define DONOTCACHEPAGE as literal true' );
$robots = nl_proposal_commercial_scene_sandbox_robots( array() );
fixture_assert( true === $robots['noindex'] && true === $robots['nofollow'] && true === $robots['noarchive'], 'the unauthorized password challenge must receive noindex, nofollow, and noarchive meta directives' );
fixture_assert( fixture_expected_sandbox_headers() === nl_proposal_commercial_scene_sandbox_headers(), 'the unauthorized password challenge must receive explicit private/no-store and crawler headers' );
fixture_assert( 1 === $GLOBALS['fixture_nocache_calls'], 'the unauthorized password challenge must invoke WordPress no-cache headers exactly once' );
fixture_assert( nl_proposal_commercial_scene_sandbox_cache_headers_ready(), 'successful exact challenge headers must mark the response-header seam ready' );
fixture_reset_enqueue_state();
nl_proposal_enqueue_commercial_scene_sandbox();
fixture_assert( array() === $GLOBALS['fixture_styles'] && array() === $GLOBALS['fixture_inline'] && array() === $GLOBALS['fixture_scripts'], 'the unauthorized password challenge must receive no proposal assets' );
fixture_assert( array() === $GLOBALS['fixture_localized'], 'the unauthorized password challenge must receive no proposal configuration' );
fixture_assert( array() === $GLOBALS['fixture_nonce_requests'], 'the unauthorized password challenge must not request a signed nonce' );

$GLOBALS['fixture_request']['authenticated'] = true;
fixture_assert( nl_proposal_is_commercial_scene_sandbox_page(), 'the authorized password response must remain inside the non-content sandbox predicate' );
fixture_assert( nl_proposal_is_commercial_scene_sandbox_request(), 'the authorized password response may receive protected sandbox content' );
$robots = nl_proposal_commercial_scene_sandbox_robots( array() );
fixture_assert( true === $robots['noindex'] && true === $robots['nofollow'] && true === $robots['noarchive'], 'the authorized password response must retain noindex, nofollow, and noarchive meta directives' );
fixture_assert( fixture_expected_sandbox_headers() === nl_proposal_commercial_scene_sandbox_headers(), 'the authorized password response must receive explicit private/no-store and crawler headers' );
fixture_assert( 1 === $GLOBALS['fixture_nocache_calls'], 'the authorized password response must invoke WordPress no-cache headers exactly once' );
fixture_assert( defined( 'DONOTCACHEPAGE' ) && true === DONOTCACHEPAGE, 'the authorized password response must retain the literal page-cache opt-out' );
fixture_assert( nl_proposal_commercial_scene_sandbox_cache_headers_ready(), 'the authorized response must retain exact-header readiness before protected enqueue' );

fixture_reset_enqueue_state();
nl_proposal_enqueue_commercial_scene_sandbox();
fixture_assert( array( 'nadlan-engine-css' ) === $GLOBALS['fixture_styles'], 'exact existing showroom stylesheet handle must be enqueued' );
fixture_assert( 1 === count( $GLOBALS['fixture_inline'] ) && 'nadlan-engine-css' === $GLOBALS['fixture_inline'][0]['handle'], 'proposal CSS must be attached through wp_add_inline_style to the exact base handle' );
fixture_assert( false !== strpos( $GLOBALS['fixture_inline'][0]['css'], 'PROPOSAL ONLY — NOT APPLIED' ), 'inline CSS must retain the proposal-only header' );

$expected_order = array(
	'nl-proposal-commercial-i18n',
	'nl-proposal-commercial-decision',
	'nl-proposal-commercial-floor-selector',
	'nl-proposal-commercial-context-map',
	'nl-proposal-commercial-rfp-composer',
);
fixture_assert( $expected_order === array_keys( $GLOBALS['fixture_scripts'] ), 'proposal scripts must enqueue in deterministic order' );
fixture_assert( array( 'nadlan-engine-i18n' ) === $GLOBALS['fixture_scripts']['nl-proposal-commercial-i18n']['dependencies'], 'commercial dictionary must follow the live i18n handle' );
fixture_assert( array( 'nadlan-engine-core', 'nl-proposal-commercial-i18n' ) === $GLOBALS['fixture_scripts']['nl-proposal-commercial-decision']['dependencies'], 'decision surface must follow the live engine and complete dictionary' );
fixture_assert( array( 'nl-proposal-commercial-decision', 'nl-proposal-commercial-i18n' ) === $GLOBALS['fixture_scripts']['nl-proposal-commercial-rfp-composer']['dependencies'], 'RFP composer must follow decision and dictionary modules' );
fixture_assert( true === $GLOBALS['fixture_scripts']['nl-proposal-commercial-rfp-composer']['footer'], 'all proposal scripts must remain footer scripts' );
fixture_assert( 'NadlanCommercialRfpConfig' === $GLOBALS['fixture_localized']['nl-proposal-commercial-rfp-composer']['name'], 'composer configuration must use the documented safe global' );
fixture_assert( 'https://nad-lan.co.il/wp-json/nadlan/v2/commercial-rfp-sandbox' === $GLOBALS['fixture_localized']['nl-proposal-commercial-rfp-composer']['value']['endpoint'], 'private sandbox must use only the isolated non-delivering REST route' );
fixture_assert( 'test' === $GLOBALS['fixture_localized']['nl-proposal-commercial-rfp-composer']['value']['environment'], 'sandbox environment must be explicit test' );
fixture_assert( 55 === $GLOBALS['fixture_localized']['nl-proposal-commercial-rfp-composer']['value']['sandboxPostId'], 'sandbox post ID must be immutable in composer config' );
fixture_assert( '' !== $GLOBALS['fixture_localized']['nl-proposal-commercial-rfp-composer']['value']['sandboxNonce'], 'sandbox composer needs its signed test nonce' );
fixture_assert( 'fixture-consent-v1' === $GLOBALS['fixture_localized']['nl-proposal-commercial-rfp-composer']['value']['consentVersion'], 'localized consent version must match the endpoint contract' );
fixture_assert( array( 55 ) === $GLOBALS['fixture_nonce_requests'], 'only the authorized response may request the signed sandbox nonce' );

$shared_cache = array();
$cache_key    = 'https://nad-lan.co.il/commercial-acceptance/';
$GLOBALS['fixture_request']['authenticated'] = true;
$authorized_fetch    = fixture_shared_cache_fetch( $shared_cache, $cache_key );
$authorized_response = $authorized_fetch['response'];
fixture_assert( 'origin' === $authorized_fetch['source'], 'the first authenticated request must render at the protected origin' );
fixture_assert( true === $authorized_response['authorized'], 'the cache simulation must begin with an authenticated sandbox response' );
fixture_assert( 'authenticated-sandbox-html' === $authorized_response['body_kind'], 'the authenticated simulation must model the HTML response carrying protected config' );
fixture_assert( fixture_expected_sandbox_headers() === $authorized_response['headers'], 'the authenticated simulated response must carry the complete explicit no-store header set' );
fixture_assert( 1 === $authorized_response['nocache_calls'], 'the authenticated simulated response must invoke WordPress no-cache headers' );
fixture_assert( ! empty( $authorized_response['styles'] ) && ! empty( $authorized_response['scripts'] ) && ! empty( $authorized_response['localized'] ), 'the authenticated simulated response must contain the protected proposal payload' );
fixture_assert( array( 55 ) === $authorized_response['nonce_requests'], 'the authenticated simulated response must create exactly one signed nonce' );
fixture_assert( ! fixture_shared_cache_eligible( $authorized_response ), 'private/no-store must make the authenticated response ineligible for the shared cache' );
fixture_assert( array() === $shared_cache, 'the shared cache must never store authenticated sandbox HTML, config, or nonce material' );

$GLOBALS['fixture_request']['authenticated'] = false;
$anonymous_fetch    = fixture_shared_cache_fetch( $shared_cache, $cache_key );
$anonymous_response = $anonymous_fetch['response'];
fixture_assert( 'origin' === $anonymous_fetch['source'], 'the anonymous follow-up must reach the origin because no authenticated response was cached' );
fixture_assert( false === $anonymous_response['authorized'], 'the anonymous follow-up must remain on the password challenge' );
fixture_assert( 'password-challenge' === $anonymous_response['body_kind'], 'the anonymous follow-up must render only password-challenge HTML' );
fixture_assert( fixture_expected_sandbox_headers() === $anonymous_response['headers'], 'the anonymous challenge must retain the complete explicit no-store header set' );
fixture_assert( 1 === $anonymous_response['nocache_calls'], 'the anonymous challenge must invoke WordPress no-cache headers' );
fixture_assert( array() === $anonymous_response['styles'] && array() === $anonymous_response['inline'] && array() === $anonymous_response['scripts'], 'the anonymous follow-up must receive no protected proposal assets' );
fixture_assert( array() === $anonymous_response['localized'] && array() === $anonymous_response['nonce_requests'], 'the anonymous follow-up must receive no config or signed nonce' );
fixture_assert( ! fixture_shared_cache_eligible( $anonymous_response ), 'the anonymous challenge must also be ineligible for the shared cache' );
fixture_assert( array() === $shared_cache, 'the anonymous password challenge must also remain absent from the shared cache' );

$GLOBALS['fixture_request']['authenticated'] = true;
fixture_reset_enqueue_state();
$GLOBALS['fixture_registered_scripts']['nadlan-engine-core'] = false;
nl_proposal_enqueue_commercial_scene_sandbox();
fixture_assert( array() === $GLOBALS['fixture_styles'] && array() === $GLOBALS['fixture_scripts'], 'missing exact live handle must fail closed before any proposal asset loads' );
fixture_assert( 'required_showroom_handle_missing' === $GLOBALS['fixture_actions'][0][1]['reason'], 'missing dependency must emit the documented operational gate' );
fixture_assert( array() === $GLOBALS['fixture_nonce_requests'], 'missing dependencies must block nonce creation as well as proposal assets' );

$GLOBALS['fixture_registered_scripts']['nadlan-engine-core'] = true;
$GLOBALS['fixture_request']['status']   = 'private';
$GLOBALS['fixture_request']['password'] = '';
$GLOBALS['fixture_request']['authenticated'] = false;
fixture_assert( nl_proposal_is_commercial_scene_sandbox_page(), 'a flagged private singular page must match the non-content predicate before authorization' );
fixture_assert( ! nl_proposal_is_commercial_scene_sandbox_request(), 'an unauthorized private request must not receive protected sandbox content' );
$robots = nl_proposal_commercial_scene_sandbox_robots( array() );
fixture_assert( true === $robots['noindex'] && true === $robots['noarchive'], 'an unauthorized private sandbox response must retain noindex and noarchive meta directives' );
fixture_assert( fixture_expected_sandbox_headers() === nl_proposal_commercial_scene_sandbox_headers(), 'an unauthorized private sandbox response must receive explicit private/no-store and crawler headers' );
fixture_assert( 1 === $GLOBALS['fixture_nocache_calls'], 'an unauthorized private sandbox response must invoke WordPress no-cache headers' );
fixture_reset_enqueue_state();
nl_proposal_enqueue_commercial_scene_sandbox();
fixture_assert( array() === $GLOBALS['fixture_styles'] && array() === $GLOBALS['fixture_scripts'] && array() === $GLOBALS['fixture_localized'], 'an unauthorized private request must receive no proposal assets or configuration' );
fixture_assert( array() === $GLOBALS['fixture_nonce_requests'], 'an unauthorized private request must not request a signed nonce' );
$GLOBALS['fixture_request']['authenticated'] = true;
fixture_assert( nl_proposal_is_commercial_scene_sandbox_request(), 'an authorized private sandbox may receive protected sandbox content' );

$GLOBALS['fixture_request']['admin'] = true;
fixture_assert( ! nl_proposal_is_commercial_scene_sandbox_page(), 'admin requests must remain outside the non-content page predicate' );
fixture_assert( ! nl_proposal_is_commercial_scene_sandbox_request(), 'admin requests must remain outside the public scene integration' );
fixture_assert( array( 'index' => true ) === nl_proposal_commercial_scene_sandbox_robots( array( 'index' => true ) ), 'admin robots directives must remain untouched' );
fixture_assert( array() === nl_proposal_commercial_scene_sandbox_headers(), 'admin requests must not receive sandbox cache or crawler headers' );
fixture_assert( 0 === $GLOBALS['fixture_nocache_calls'], 'admin callbacks must not invoke WordPress no-cache headers' );

echo "PASS sandbox integration fixture: pre-auth robots/no-store headers, DONOTCACHEPAGE/nocache/header-ready seam, headers-sent/write-failure blocking, shared-cache replay prevention, authenticated-only payload, and public-page isolation.\n";
