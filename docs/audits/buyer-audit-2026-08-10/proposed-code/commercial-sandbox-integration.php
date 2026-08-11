<?php
/**
 * PROPOSAL ONLY — NOT APPLIED.
 *
 * Classic-WordPress sandbox enqueue contract for the commercial scene.
 * Copy only into a reviewed sandbox module. Production is fail-closed unless
 * the explicit constant, per-page flag, and private/password guard all pass.
 *
 * @package Nadlan_Proposal
 */

defined( 'ABSPATH' ) || exit;

if ( ! defined( 'NL_PROPOSAL_COMMERCIAL_SCENE_VERSION' ) ) {
	define( 'NL_PROPOSAL_COMMERCIAL_SCENE_VERSION', '1.0.0-proposal' );
}

/**
 * Identify the explicitly flagged protected sandbox page without granting access.
 *
 * This predicate exists only for non-content controls such as robots meta and
 * HTTP headers, which must also cover a password challenge before the visitor
 * authenticates. A public post with an empty password fails closed.
 *
 * @return bool
 */
function nl_proposal_is_commercial_scene_sandbox_page() {
	if (
		! defined( 'NL_PROPOSAL_COMMERCIAL_SCENE_SANDBOX' )
		|| true !== NL_PROPOSAL_COMMERCIAL_SCENE_SANDBOX
		|| is_admin()
		|| ! is_singular()
	) {
		return false;
	}
	$post_id = (int) get_queried_object_id();
	if ( $post_id < 1 || '1' !== (string) get_post_meta( $post_id, '_nl_commercial_scene_sandbox_enabled', true ) ) {
		return false;
	}
	if ( 'private' === (string) get_post_status( $post_id ) ) {
		return true;
	}
	return '' !== (string) get_post_field( 'post_password', $post_id );
}

/**
 * Decide whether the current request may receive protected sandbox content.
 *
 * Only this authenticated predicate may gate proposal assets, configuration,
 * or a signed nonce. The page predicate above does not grant content access.
 *
 * @return bool
 */
function nl_proposal_is_commercial_scene_sandbox_request() {
	if ( ! nl_proposal_is_commercial_scene_sandbox_page() ) {
		return false;
	}
	$post_id = (int) get_queried_object_id();
	return function_exists( 'nl_proposal_commercial_rfp_sandbox_context_allowed' )
		&& nl_proposal_commercial_rfp_sandbox_context_allowed( $post_id );
}

/**
 * Mark the protected sandbox response as ineligible for WordPress page caches.
 *
 * Never redefine a cache constant supplied by the host. A conflicting false
 * value remains false and causes the authenticated content path to fail closed.
 *
 * @return bool Whether this sandbox response is marked uncacheable.
 */
function nl_proposal_commercial_scene_sandbox_disable_page_cache() {
	if ( ! nl_proposal_is_commercial_scene_sandbox_page() ) {
		return false;
	}
	if ( ! defined( 'DONOTCACHEPAGE' ) ) {
		define( 'DONOTCACHEPAGE', true );
	}
	return defined( 'DONOTCACHEPAGE' ) && true === DONOTCACHEPAGE;
}

/**
 * Return whether the exact sandbox cache headers were emitted this request.
 *
 * @return bool
 */
function nl_proposal_commercial_scene_sandbox_cache_headers_ready() {
	return isset( $GLOBALS['_nl_proposal_commercial_scene_sandbox_cache_headers_ready'] )
		&& true === $GLOBALS['_nl_proposal_commercial_scene_sandbox_cache_headers_ready'];
}

/**
 * Detect an unusable header channel. The filter may only force failure.
 *
 * @return bool
 */
function nl_proposal_commercial_scene_sandbox_headers_already_sent() {
	$forced_failure = (bool) apply_filters(
		'nl_proposal_commercial_scene_sandbox_force_headers_sent',
		false
	);
	return headers_sent() || $forced_failure;
}

/**
 * Emit one reviewed response header and expose a fail-only fixture seam.
 *
 * PHP's header() has no success return value. The filter defaults to false and
 * can only make the protected content path stricter by reporting a write error.
 *
 * @param string $name  Header name.
 * @param string $value Header value.
 * @return bool
 */
function nl_proposal_commercial_scene_sandbox_send_header( $name, $value ) {
	header( $name . ': ' . $value, true );
	$write_failed = (bool) apply_filters(
		'nl_proposal_commercial_scene_sandbox_header_write_failed',
		false,
		$name,
		$value
	);
	return ! $write_failed;
}

/**
 * Add noindex/noarchive directives to the guarded sandbox only.
 *
 * @param array $robots Existing robots directives.
 * @return array
 */
function nl_proposal_commercial_scene_sandbox_robots( $robots ) {
	if ( ! nl_proposal_is_commercial_scene_sandbox_page() ) {
		return $robots;
	}
	$robots['noindex']   = true;
	$robots['nofollow']  = true;
	$robots['noarchive'] = true;
	return $robots;
}

/**
 * Send explicit private/no-store and crawler-control headers for the sandbox.
 *
 * WordPress's standard nocache headers run first. The reviewed values below
 * then replace the relevant fields deterministically for page and CDN caches.
 *
 * @return array<string,string> Headers sent, or an empty array when inapplicable.
 */
function nl_proposal_commercial_scene_sandbox_headers() {
	if ( ! nl_proposal_is_commercial_scene_sandbox_page() ) {
		return array();
	}
	nl_proposal_commercial_scene_sandbox_disable_page_cache();
	if ( nl_proposal_commercial_scene_sandbox_headers_already_sent() ) {
		return array();
	}
	nocache_headers();
	if ( nl_proposal_commercial_scene_sandbox_headers_already_sent() ) {
		return array();
	}
	$headers = array(
		'Cache-Control' => 'private, no-store, no-cache, must-revalidate, max-age=0',
		'Pragma'       => 'no-cache',
		'Expires'      => 'Wed, 11 Jan 1984 05:00:00 GMT',
		'X-Robots-Tag' => 'noindex, nofollow, noarchive',
	);
	$headers_ready = true;
	foreach ( $headers as $name => $value ) {
		if ( ! nl_proposal_commercial_scene_sandbox_send_header( $name, $value ) ) {
			$headers_ready = false;
		}
	}
	if ( ! $headers_ready ) {
		return array();
	}
	$GLOBALS['_nl_proposal_commercial_scene_sandbox_cache_headers_ready'] = true;
	return $headers;
}

/**
 * Enqueue the proposal in deterministic dependency order.
 *
 * The exact current showroom stylesheet handle is nadlan-engine-css and the
 * exact current engine handle is nadlan-engine-core. Missing base handles block
 * the proposal; they are never guessed or registered under replacement names.
 *
 * @return void
 */
function nl_proposal_enqueue_commercial_scene_sandbox() {
	if ( ! nl_proposal_is_commercial_scene_sandbox_request() ) {
		return;
	}
	if ( ! nl_proposal_commercial_scene_sandbox_disable_page_cache() ) {
		do_action(
			'nl_proposal_commercial_scene_blocked',
			array( 'reason' => 'page_cache_suppression_unavailable' )
		);
		return;
	}
	if ( ! nl_proposal_commercial_scene_sandbox_cache_headers_ready() ) {
		do_action(
			'nl_proposal_commercial_scene_blocked',
			array( 'reason' => 'response_cache_headers_unavailable' )
		);
		return;
	}
	if (
		! wp_style_is( 'nadlan-engine-css', 'registered' )
		|| ! wp_script_is( 'nadlan-engine-i18n', 'registered' )
		|| ! wp_script_is( 'nadlan-engine-core', 'registered' )
		|| ! defined( 'NL_PROPOSAL_RFP_CONSENT_VERSION' )
		|| ! function_exists( 'nl_proposal_create_commercial_rfp_sandbox_nonce' )
	) {
		do_action(
			'nl_proposal_commercial_scene_blocked',
			array( 'reason' => 'required_showroom_handle_missing' )
		);
		return;
	}
	$sandbox_post_id = (int) get_queried_object_id();
	$sandbox_nonce   = nl_proposal_create_commercial_rfp_sandbox_nonce( $sandbox_post_id );
	if ( '' === $sandbox_nonce ) {
		do_action(
			'nl_proposal_commercial_scene_blocked',
			array( 'reason' => 'sandbox_nonce_unavailable' )
		);
		return;
	}

	$directory = plugin_dir_path( __FILE__ );
	$base_url  = plugin_dir_url( __FILE__ );
	$css_path  = $directory . 'commercial-decision-surface.css';
	if ( ! is_readable( $css_path ) ) {
		do_action(
			'nl_proposal_commercial_scene_blocked',
			array( 'reason' => 'proposal_css_missing' )
		);
		return;
	}
	$css = file_get_contents( $css_path );
	if ( false === $css || '' === trim( $css ) ) {
		do_action(
			'nl_proposal_commercial_scene_blocked',
			array( 'reason' => 'proposal_css_unreadable' )
		);
		return;
	}

	wp_enqueue_style( 'nadlan-engine-css' );
	if ( ! wp_add_inline_style( 'nadlan-engine-css', $css ) ) {
		do_action(
			'nl_proposal_commercial_scene_blocked',
			array( 'reason' => 'inline_style_rejected' )
		);
		return;
	}

	wp_enqueue_script(
		'nl-proposal-commercial-i18n',
		$base_url . 'commercial-i18n-additions.js',
		array( 'nadlan-engine-i18n' ),
		NL_PROPOSAL_COMMERCIAL_SCENE_VERSION,
		true
	);
	wp_enqueue_script(
		'nl-proposal-commercial-decision',
		$base_url . 'commercial-decision-surface.js',
		array( 'nadlan-engine-core', 'nl-proposal-commercial-i18n' ),
		NL_PROPOSAL_COMMERCIAL_SCENE_VERSION,
		true
	);
	wp_enqueue_script(
		'nl-proposal-commercial-floor-selector',
		$base_url . 'commercial-floor-selection.js',
		array( 'nl-proposal-commercial-decision' ),
		NL_PROPOSAL_COMMERCIAL_SCENE_VERSION,
		true
	);
	wp_enqueue_script(
		'nl-proposal-commercial-context-map',
		$base_url . 'commercial-context-map.js',
		array( 'nl-proposal-commercial-decision' ),
		NL_PROPOSAL_COMMERCIAL_SCENE_VERSION,
		true
	);
	wp_enqueue_script(
		'nl-proposal-commercial-rfp-composer',
		$base_url . 'commercial-rfp-composer.js',
		array( 'nl-proposal-commercial-decision', 'nl-proposal-commercial-i18n' ),
		NL_PROPOSAL_COMMERCIAL_SCENE_VERSION,
		true
	);
	wp_localize_script(
		'nl-proposal-commercial-rfp-composer',
		'NadlanCommercialRfpConfig',
		array(
			'endpoint'       => esc_url_raw( rest_url( 'nadlan/v2/commercial-rfp-sandbox' ) ),
			'environment'    => 'test',
			'sandboxPostId'  => $sandbox_post_id,
			'sandboxNonce'   => $sandbox_nonce,
			'consentVersion' => (string) NL_PROPOSAL_RFP_CONSENT_VERSION,
		)
	);
}

add_filter( 'wp_robots', 'nl_proposal_commercial_scene_sandbox_robots' );
add_action( 'wp', 'nl_proposal_commercial_scene_sandbox_disable_page_cache', 0 );
add_action( 'template_redirect', 'nl_proposal_commercial_scene_sandbox_headers', PHP_INT_MAX );
add_action( 'wp_enqueue_scripts', 'nl_proposal_enqueue_commercial_scene_sandbox', 99 );
