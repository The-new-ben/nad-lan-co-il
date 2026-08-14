<?php
/**
 * PROPOSAL ONLY — NOT APPLIED.
 *
 * Reference data contract for commercial projects, floors and suites.
 *
 * Target runtime: PHP 7.4+ and classic WordPress. This file deliberately
 * performs no registration, persistence, migration or rendering by itself.
 * Its normalizers are fail-closed: missing data becomes an explicit unknown,
 * while malformed, stale or unsupported claims return WP_Error.
 *
 * @package Nadlan_Proposal
 */

defined( 'ABSPATH' ) || exit;

if ( ! defined( 'NL_PROPOSAL_COMMERCIAL_SCHEMA_VERSION' ) ) {
	define( 'NL_PROPOSAL_COMMERCIAL_SCHEMA_VERSION', '1.0.0' );
}

/**
 * Return the only asset types the proposed engine understands.
 *
 * @return string[]
 */
function nl_proposal_asset_types() {
	return array(
		'residential',
		'commercial_office',
		'retail',
		'mixed_use',
		'hospitality',
		'guide_only',
	);
}

/**
 * Return asset types with a fully implemented browser adapter in this
 * proposal. The canonical asset-type vocabulary is intentionally broader.
 *
 * @return string[]
 */
function nl_proposal_implemented_asset_types() {
	return array( 'commercial_office' );
}

/**
 * Return presentation/product families. These are merchandising groupings,
 * never runtime asset types and never a renderer-selection signal.
 *
 * @return string[]
 */
function nl_proposal_product_families() {
	return array(
		'living',
		'premium',
		'commercial',
		'guide',
	);
}

/**
 * Return capability/applicability tags. Tags describe which optional product
 * surfaces may apply; they cannot override asset_type or enable an adapter.
 *
 * @return string[]
 */
function nl_proposal_applicability_tags() {
	return array(
		'three_d_showroom',
		'floor_selector',
		'suite_selector',
		'commercial_rfp',
		'context_map',
		'decision_surface',
	);
}

/**
 * Return the public commercial availability vocabulary.
 *
 * "available" is intentionally absent. A positive availability claim must be
 * "verified_available" and must carry current evidence.
 *
 * @return string[]
 */
function nl_proposal_commercial_statuses() {
	return array(
		'unknown',
		'verified_available',
		'soft_hold',
		'under_offer',
		'under_loi',
		'leased',
		'delivered',
		'unavailable',
		'not_marketed',
	);
}

/**
 * Return evidence states.
 *
 * @return string[]
 */
function nl_proposal_evidence_states() {
	return array(
		'unknown',
		'source_estimate',
		'verified',
		'contradictory',
	);
}

/**
 * Confidence is independent from truth state. It is never inferred from
 * verified/source_estimate/contradictory.
 *
 * @return string[]
 */
function nl_proposal_confidence_levels() {
	return array( 'unknown', 'low', 'medium', 'high' );
}

/**
 * Canonical landmark distance methods.
 *
 * @return string[]
 */
function nl_proposal_beam_distance_methods() {
	return array(
		'straight_line_geodesic',
		'routed_walking',
		'routed_cycling',
		'routed_driving',
		'routed_transit',
	);
}

/**
 * Maximum Unicode code points permitted in the separately evidenced label
 * rendered inside the fixed beam scene. Full landmark labels remain available
 * to assistive technology and the evidence tool; display labels are never
 * truncated to fit.
 *
 * @return int
 */
function nl_proposal_beam_compact_label_max_code_points() {
	return 12;
}

/**
 * Return allowed source classifications.
 *
 * @return string[]
 */
function nl_proposal_source_types() {
	return array(
		'owner_crm',
		'landlord_schedule',
		'signed_offer',
		'executed_lease_exhibit',
		'developer_document',
		'as_built_drawing',
		'measurement_report',
		'engineering_report',
		'government_register',
		'planning_document',
		'municipal_record',
		'official_transit_feed',
		'broker_written_confirmation',
		'public_listing',
		'other',
	);
}

/**
 * Return supported compass sectors.
 *
 * @return string[]
 */
function nl_proposal_compass_sectors() {
	return array( 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW' );
}

/**
 * Return the canonical server-to-browser vocabulary published with each
 * normalized contract. JavaScript must reject or fail closed on a vocabulary it
 * does not understand; it must never rename states in the browser.
 *
 * @return array
 */
function nl_proposal_commercial_contract_vocabularies() {
	return array(
		'asset_types'             => nl_proposal_asset_types(),
		'implemented_asset_types' => nl_proposal_implemented_asset_types(),
		'product_families'        => nl_proposal_product_families(),
		'applicability_tags'      => nl_proposal_applicability_tags(),
		'evidence_states'         => nl_proposal_evidence_states(),
		'confidence_levels'       => nl_proposal_confidence_levels(),
		'availability_statuses'   => nl_proposal_commercial_statuses(),
		'compass_sectors'         => nl_proposal_compass_sectors(),
		'beam_distance_methods'   => nl_proposal_beam_distance_methods(),
		'source_types'            => nl_proposal_source_types(),
	);
}

/**
 * Return a canonical unknown evidence envelope.
 *
 * The shape is stable so templates never need to infer that an absent key
 * means zero, false, west-facing or available.
 *
 * @param string $reason Human-readable reason.
 * @param array  $required_document_ids IDs that can be requested in one click.
 * @param array|null $owner Optional accountable owner.
 * @param array $applicability Exact field/product applicability identifiers.
 * @return array
 */
function nl_proposal_unknown_evidence( $reason = 'Not supplied.', $required_document_ids = array(), $owner = null, $applicability = array( 'all' ) ) {
	$document_ids = array();
	$applicability_ids = array();

	if ( is_array( $required_document_ids ) ) {
		foreach ( $required_document_ids as $document_id ) {
			$clean = nl_proposal_sanitize_contract_id( $document_id );
			if ( ! is_wp_error( $clean ) ) {
				$document_ids[] = $clean;
			}
		}
	}
	if ( is_array( $applicability ) ) {
		foreach ( $applicability as $applicability_id ) {
			$clean = nl_proposal_sanitize_contract_id( $applicability_id, 'evidence.applicability[]' );
			if ( ! is_wp_error( $clean ) ) {
				$applicability_ids[] = $clean;
			}
		}
	}
	if ( empty( $applicability_ids ) ) {
		$applicability_ids[] = 'all';
	}

	return array(
		'state'                 => 'unknown',
		'value'                 => null,
		'unit'                  => null,
		'scope'                 => null,
		'effective_at'          => null,
		'sources'               => array(),
		'observations'          => array(),
		'verified_at'           => null,
		'expires_at'            => null,
		'owner'                 => is_array( $owner ) ? $owner : null,
		'confidence'            => 'unknown',
		'reason'                => sanitize_textarea_field( (string) $reason ),
		'applicability'         => array_values( array_unique( $applicability_ids ) ),
		'conflict_ids'          => array(),
		'note'                  => '',
		'caveat'                => '',
		'required_document_ids' => array_values( array_unique( $document_ids ) ),
		'decision_grade'        => false,
	);
}

/**
 * Sanitize an immutable machine identifier.
 *
 * @param mixed  $value Raw value.
 * @param string $field Field name for errors.
 * @return string|WP_Error
 */
function nl_proposal_sanitize_contract_id( $value, $field = 'id' ) {
	if ( ! is_scalar( $value ) ) {
		return new WP_Error(
			'nl_proposal_invalid_id',
			sprintf( '%s must be a scalar identifier.', $field )
		);
	}

	$value = strtolower( trim( (string) $value ) );

	if ( '' === $value || strlen( $value ) > 128 || ! preg_match( '/^[a-z0-9][a-z0-9._:-]*$/', $value ) ) {
		return new WP_Error(
			'nl_proposal_invalid_id',
			sprintf( '%s must match [a-z0-9][a-z0-9._:-]* and be at most 128 characters.', $field )
		);
	}

	return $value;
}

/**
 * Sanitize bounded text without silently truncating it.
 *
 * @param mixed  $value Raw value.
 * @param string $field Field name.
 * @param int    $max_length Maximum Unicode characters.
 * @param bool   $allow_empty Whether an empty string is permitted.
 * @return string|WP_Error
 */
function nl_proposal_sanitize_bounded_text( $value, $field, $max_length = 255, $allow_empty = false ) {
	if ( ! is_scalar( $value ) ) {
		return new WP_Error( 'nl_proposal_invalid_text', sprintf( '%s must be text.', $field ) );
	}

	$value = (string) $value;
	if ( 1 !== preg_match( '//u', $value ) ) {
		return new WP_Error( 'nl_proposal_invalid_utf8', sprintf( '%s must be valid UTF-8 text.', $field ) );
	}
	$value = sanitize_text_field( $value );
	if ( 1 !== preg_match( '//u', $value ) ) {
		return new WP_Error( 'nl_proposal_invalid_utf8', sprintf( '%s must be valid UTF-8 text.', $field ) );
	}
	$code_points = array();
	$length      = preg_match_all( '/./us', $value, $code_points );
	if ( false === $length ) {
		return new WP_Error( 'nl_proposal_invalid_utf8', sprintf( '%s must be valid UTF-8 text.', $field ) );
	}

	if ( ! $allow_empty && '' === $value ) {
		return new WP_Error( 'nl_proposal_missing_text', sprintf( '%s is required.', $field ) );
	}

	if ( $length > $max_length ) {
		return new WP_Error(
			'nl_proposal_text_too_long',
			sprintf( '%s exceeds %d characters.', $field, $max_length )
		);
	}

	return $value;
}

/**
 * Normalize an RFC3339 timestamp.
 *
 * @param mixed  $value Raw timestamp.
 * @param string $field Field name.
 * @param bool   $allow_null Whether null/empty is allowed.
 * @return string|null|WP_Error
 */
function nl_proposal_normalize_rfc3339( $value, $field, $allow_null = true ) {
	if ( null === $value || '' === $value ) {
		return $allow_null
			? null
			: new WP_Error( 'nl_proposal_missing_timestamp', sprintf( '%s is required.', $field ) );
	}

	if ( ! is_string( $value ) || ! preg_match( '/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})$/', $value ) ) {
		return new WP_Error(
			'nl_proposal_invalid_timestamp',
			sprintf( '%s must be a full RFC3339 timestamp with timezone.', $field )
		);
	}

	try {
		$date = new DateTimeImmutable( $value );
	} catch ( Exception $exception ) {
		return new WP_Error( 'nl_proposal_invalid_timestamp', sprintf( '%s is not a valid date.', $field ) );
	}

	return $date->format( 'Y-m-d\TH:i:sP' );
}

/**
 * Convert a normalized timestamp to a Unix timestamp.
 *
 * @param string|null $value RFC3339 value.
 * @return int|null
 */
function nl_proposal_timestamp_to_epoch( $value ) {
	if ( null === $value || '' === $value ) {
		return null;
	}

	try {
		return ( new DateTimeImmutable( $value ) )->getTimestamp();
	} catch ( Exception $exception ) {
		return null;
	}
}

/**
 * Normalize a public HTTP(S) evidence URL.
 *
 * @param mixed  $value Raw URL.
 * @param string $field Field name.
 * @param bool   $allow_null Whether an empty URL is allowed.
 * @return string|null|WP_Error
 */
function nl_proposal_normalize_public_url( $value, $field, $allow_null = true ) {
	if ( null === $value || '' === $value ) {
		return $allow_null
			? null
			: new WP_Error( 'nl_proposal_missing_url', sprintf( '%s is required.', $field ) );
	}

	if ( ! is_string( $value ) ) {
		return new WP_Error( 'nl_proposal_invalid_url', sprintf( '%s must be a URL.', $field ) );
	}

	$url    = esc_url_raw( trim( $value ), array( 'http', 'https' ) );
	$scheme = strtolower( (string) wp_parse_url( $url, PHP_URL_SCHEME ) );
	$host   = (string) wp_parse_url( $url, PHP_URL_HOST );

	if ( '' === $url || ! in_array( $scheme, array( 'http', 'https' ), true ) || '' === $host ) {
		return new WP_Error( 'nl_proposal_invalid_url', sprintf( '%s must be a valid public HTTP(S) URL.', $field ) );
	}

	return $url;
}

/**
 * Parse origin and canonical permalink components without treating an omitted
 * default port as different from its explicit equivalent.
 *
 * @param string $url Absolute URL.
 * @return array|null
 */
function nl_proposal_url_contract_parts( $url ) {
	$scheme   = strtolower( (string) wp_parse_url( $url, PHP_URL_SCHEME ) );
	$host     = strtolower( (string) wp_parse_url( $url, PHP_URL_HOST ) );
	$port     = wp_parse_url( $url, PHP_URL_PORT );
	$user     = wp_parse_url( $url, PHP_URL_USER );
	$pass     = wp_parse_url( $url, PHP_URL_PASS );
	$path     = wp_parse_url( $url, PHP_URL_PATH );
	$query    = wp_parse_url( $url, PHP_URL_QUERY );
	$fragment = wp_parse_url( $url, PHP_URL_FRAGMENT );
	if (
		! in_array( $scheme, array( 'http', 'https' ), true )
		|| '' === $host
		|| ( null !== $user && false !== $user && '' !== $user )
		|| ( null !== $pass && false !== $pass && '' !== $pass )
	) {
		return null;
	}
	$effective_port = is_numeric( $port ) ? (int) $port : ( 'https' === $scheme ? 443 : 80 );
	if ( $effective_port < 1 || $effective_port > 65535 ) {
		return null;
	}
	return array(
		'scheme'   => $scheme,
		'host'     => $host,
		'port'     => $effective_port,
		'path'     => ( null === $path || false === $path || '' === $path ) ? '/' : (string) $path,
		'query'    => ( null === $query || false === $query ) ? '' : (string) $query,
		'fragment' => ( null === $fragment || false === $fragment ) ? '' : (string) $fragment,
	);
}

/**
 * Compare normalized scheme, host, and effective port.
 *
 * @param array|null $left Parsed URL parts.
 * @param array|null $right Parsed URL parts.
 * @return bool
 */
function nl_proposal_url_contract_same_origin( $left, $right ) {
	return is_array( $left ) && is_array( $right )
		&& $left['scheme'] === $right['scheme']
		&& $left['host'] === $right['host']
		&& $left['port'] === $right['port'];
}

/**
 * Normalize an accountable data owner.
 *
 * contact_ref is an internal directory/CRM reference, not an email address.
 *
 * @param mixed $raw Raw owner object.
 * @param bool  $required Whether the owner must be present.
 * @return array|null|WP_Error
 */
function nl_proposal_normalize_data_owner( $raw, $required = false ) {
	if ( null === $raw || array() === $raw ) {
		return $required
			? new WP_Error( 'nl_proposal_missing_owner', 'An accountable data owner is required.' )
			: null;
	}

	if ( ! is_array( $raw ) ) {
		return new WP_Error( 'nl_proposal_invalid_owner', 'owner must be an object.' );
	}

	$team = nl_proposal_sanitize_bounded_text(
		isset( $raw['team'] ) ? $raw['team'] : '',
		'owner.team',
		120
	);
	if ( is_wp_error( $team ) ) {
		return $team;
	}

	$role = nl_proposal_sanitize_bounded_text(
		isset( $raw['accountable_role'] ) ? $raw['accountable_role'] : '',
		'owner.accountable_role',
		120
	);
	if ( is_wp_error( $role ) ) {
		return $role;
	}

	$contact_ref = null;
	if ( isset( $raw['contact_ref'] ) && '' !== $raw['contact_ref'] ) {
		$contact_ref = nl_proposal_sanitize_contract_id( $raw['contact_ref'], 'owner.contact_ref' );
		if ( is_wp_error( $contact_ref ) ) {
			return $contact_ref;
		}
	}

	return array(
		'team'             => $team,
		'accountable_role' => $role,
		'contact_ref'      => $contact_ref,
	);
}

/**
 * Normalize one evidence source.
 *
 * At least one of uri or document_id is required. A marketing label alone is
 * not provenance.
 *
 * @param mixed $raw Raw source object.
 * @return array|WP_Error
 */
function nl_proposal_normalize_evidence_source( $raw ) {
	if ( ! is_array( $raw ) ) {
		return new WP_Error( 'nl_proposal_invalid_source', 'Each evidence source must be an object.' );
	}

	$type = isset( $raw['type'] ) ? sanitize_key( $raw['type'] ) : '';
	if ( ! in_array( $type, nl_proposal_source_types(), true ) ) {
		return new WP_Error( 'nl_proposal_invalid_source_type', 'Evidence source type is unsupported.' );
	}

	$label = nl_proposal_sanitize_bounded_text(
		isset( $raw['label'] ) ? $raw['label'] : '',
		'source.label',
		240
	);
	if ( is_wp_error( $label ) ) {
		return $label;
	}

	$uri = nl_proposal_normalize_public_url(
		isset( $raw['uri'] ) ? $raw['uri'] : null,
		'source.uri',
		true
	);
	if ( is_wp_error( $uri ) ) {
		return $uri;
	}

	$document_id = null;
	if ( isset( $raw['document_id'] ) && '' !== $raw['document_id'] ) {
		$document_id = nl_proposal_sanitize_contract_id( $raw['document_id'], 'source.document_id' );
		if ( is_wp_error( $document_id ) ) {
			return $document_id;
		}
	}

	if ( null === $uri && null === $document_id ) {
		return new WP_Error(
			'nl_proposal_source_without_locator',
			'An evidence source needs a public URI or a stable document_id.'
		);
	}

	$published_at = nl_proposal_normalize_rfc3339(
		isset( $raw['published_at'] ) ? $raw['published_at'] : null,
		'source.published_at',
		true
	);
	if ( is_wp_error( $published_at ) ) {
		return $published_at;
	}

	$retrieved_at = nl_proposal_normalize_rfc3339(
		isset( $raw['retrieved_at'] ) ? $raw['retrieved_at'] : null,
		'source.retrieved_at',
		false
	);
	if ( is_wp_error( $retrieved_at ) ) {
		return $retrieved_at;
	}

	$revision = null;
	if ( isset( $raw['revision'] ) && '' !== $raw['revision'] ) {
		$revision = nl_proposal_sanitize_bounded_text( $raw['revision'], 'source.revision', 120 );
		if ( is_wp_error( $revision ) ) {
			return $revision;
		}
	}

	return array(
		'type'         => $type,
		'label'        => $label,
		'uri'          => $uri,
		'document_id'  => $document_id,
		'revision'     => $revision,
		'published_at' => $published_at,
		'retrieved_at' => $retrieved_at,
	);
}

/**
 * Normalize a typed evidence value.
 *
 * @param mixed  $value Raw value.
 * @param string $type One of string, integer, decimal, boolean, date,
 *                     string_list, coordinate, compass, or status.
 * @param array  $args Optional constraints: min, max, allowed.
 * @return mixed|WP_Error
 */
function nl_proposal_normalize_evidence_value( $value, $type, $args = array() ) {
	$args = wp_parse_args(
		$args,
		array(
			'min'               => null,
			'max'               => null,
			'allowed'           => array(),
			'string_max_length' => 1000,
			'string_field'      => 'evidence.value',
		)
	);

	switch ( $type ) {
		case 'string':
			return nl_proposal_sanitize_bounded_text(
				$value,
				(string) $args['string_field'],
				(int) $args['string_max_length'],
				false
			);

		case 'integer':
			if ( is_bool( $value ) || ! is_numeric( $value ) || (float) $value !== (float) (int) $value ) {
				return new WP_Error( 'nl_proposal_invalid_integer', 'Evidence value must be an integer.' );
			}
			$value = (int) $value;
			break;

		case 'decimal':
			if ( is_bool( $value ) || ! is_numeric( $value ) ) {
				return new WP_Error( 'nl_proposal_invalid_decimal', 'Evidence value must be numeric.' );
			}
			$value = (float) $value;
			if ( is_nan( $value ) || is_infinite( $value ) ) {
				return new WP_Error( 'nl_proposal_invalid_decimal', 'Evidence value must be finite.' );
			}
			break;

		case 'boolean':
			if ( ! is_bool( $value ) ) {
				return new WP_Error( 'nl_proposal_invalid_boolean', 'Evidence value must be a boolean.' );
			}
			return $value;

		case 'date':
			if ( ! is_string( $value ) || ! preg_match( '/^\d{4}-\d{2}-\d{2}$/', $value ) ) {
				return new WP_Error( 'nl_proposal_invalid_date', 'Evidence value must use YYYY-MM-DD.' );
			}
			$parts = array_map( 'intval', explode( '-', $value ) );
			if ( 3 !== count( $parts ) || ! checkdate( $parts[1], $parts[2], $parts[0] ) ) {
				return new WP_Error( 'nl_proposal_invalid_date', 'Evidence value is not a calendar date.' );
			}
			return $value;

		case 'string_list':
			if ( ! is_array( $value ) ) {
				return new WP_Error( 'nl_proposal_invalid_list', 'Evidence value must be a list.' );
			}
			$clean = array();
			foreach ( $value as $item ) {
				$item = nl_proposal_sanitize_bounded_text( $item, 'evidence.value[]', 240, false );
				if ( is_wp_error( $item ) ) {
					return $item;
				}
				$clean[] = $item;
			}
			return array_values( array_unique( $clean ) );

		case 'coordinate':
			if (
				! is_array( $value )
				|| 2 !== count( $value )
				|| ! array_key_exists( 'lat', $value )
				|| ! array_key_exists( 'lng', $value )
				|| is_bool( $value['lat'] )
				|| is_bool( $value['lng'] )
				|| ! is_numeric( $value['lat'] )
				|| ! is_numeric( $value['lng'] )
			) {
				return new WP_Error( 'nl_proposal_invalid_coordinate', 'Coordinate evidence must be an exact {lat,lng} object.' );
			}
			$lat = (float) $value['lat'];
			$lng = (float) $value['lng'];
			if (
				is_nan( $lat )
				|| is_infinite( $lat )
				|| is_nan( $lng )
				|| is_infinite( $lng )
				|| $lat < -90
				|| $lat > 90
				|| $lng < -180
				|| $lng > 180
			) {
				return new WP_Error( 'nl_proposal_invalid_coordinate', 'Coordinate latitude/longitude is out of range.' );
			}
			return array( 'lat' => $lat, 'lng' => $lng );

		case 'compass':
			$value = is_scalar( $value ) ? strtoupper( trim( (string) $value ) ) : '';
			if ( ! in_array( $value, nl_proposal_compass_sectors(), true ) ) {
				return new WP_Error( 'nl_proposal_invalid_compass', 'Compass value is unsupported.' );
			}
			return $value;

		case 'status':
			$value = is_scalar( $value ) ? sanitize_key( (string) $value ) : '';
			if ( ! in_array( $value, nl_proposal_commercial_statuses(), true ) ) {
				return new WP_Error( 'nl_proposal_invalid_status', 'Commercial availability status is unsupported.' );
			}
			return $value;

		default:
			return new WP_Error( 'nl_proposal_invalid_value_type', 'Evidence value type is unsupported.' );
	}

	if ( null !== $args['min'] && $value < $args['min'] ) {
		return new WP_Error( 'nl_proposal_value_below_minimum', 'Evidence value is below the allowed minimum.' );
	}

	if ( null !== $args['max'] && $value > $args['max'] ) {
		return new WP_Error( 'nl_proposal_value_above_maximum', 'Evidence value is above the allowed maximum.' );
	}

	if ( ! empty( $args['allowed'] ) && ! in_array( $value, $args['allowed'], true ) ) {
		return new WP_Error( 'nl_proposal_value_not_allowed', 'Evidence value is not in the allowed vocabulary.' );
	}

	return $value;
}

/**
 * Normalize one observation inside a contradictory evidence envelope.
 *
 * @param mixed  $raw Raw observation.
 * @param string $value_type Expected value type.
 * @param array  $value_args Value constraints.
 * @return array|WP_Error
 */
function nl_proposal_normalize_observation( $raw, $value_type, $value_args = array() ) {
	if ( ! is_array( $raw ) ) {
		return new WP_Error( 'nl_proposal_invalid_observation', 'Each observation must be an object.' );
	}

	if ( ! array_key_exists( 'value', $raw ) ) {
		return new WP_Error( 'nl_proposal_missing_observation_value', 'Observation value is required.' );
	}
	$observation_id = nl_proposal_sanitize_contract_id(
		isset( $raw['observation_id'] ) ? $raw['observation_id'] : '',
		'observation.observation_id'
	);
	if ( is_wp_error( $observation_id ) ) {
		return $observation_id;
	}

	$value = nl_proposal_normalize_evidence_value( $raw['value'], $value_type, $value_args );
	if ( is_wp_error( $value ) ) {
		return $value;
	}

	$source = nl_proposal_normalize_evidence_source(
		isset( $raw['source'] ) ? $raw['source'] : null
	);
	if ( is_wp_error( $source ) ) {
		return $source;
	}

	$scope = null;
	if ( isset( $raw['scope'] ) && '' !== $raw['scope'] ) {
		$scope = nl_proposal_sanitize_bounded_text( $raw['scope'], 'observation.scope', 300 );
		if ( is_wp_error( $scope ) ) {
			return $scope;
		}
	}

	return array(
		'observation_id' => $observation_id,
		'value'          => $value,
		'scope'          => $scope,
		'source'         => $source,
	);
}

/**
 * Normalize a complete evidence envelope.
 *
 * Rules:
 * - Missing input is a canonical unknown.
 * - Unknown cannot carry a value or verification timestamps.
 * - Verified facts require value, source, owner, verified_at and a future
 *   expires_at.
 * - Source estimates require value, source, owner and a future expires_at,
 *   but are never marked decision-grade.
 * - Contradictions carry no chosen value and require at least two sourced
 *   observations.
 *
 * @param mixed  $raw Raw evidence object.
 * @param string $value_type Expected value type.
 * @param array  $args Value constraints plus now and default unknown details.
 * @return array|WP_Error
 */
function nl_proposal_normalize_evidence_envelope( $raw, $value_type, $args = array() ) {
	$args = wp_parse_args(
		$args,
		array(
			'min'                           => null,
			'max'                           => null,
			'allowed'                       => array(),
			'string_max_length'             => 1000,
			'string_field'                  => 'evidence.value',
			'unit_allowed'                  => array(),
			'now'                           => time(),
			'unknown_reason'                => 'Not supplied.',
			'applicability'                 => array( 'all' ),
			'required_document_ids'         => array(),
			'max_verified_lifetime_seconds' => 0,
		)
	);

	if ( null === $raw || array() === $raw ) {
		return nl_proposal_unknown_evidence(
			$args['unknown_reason'],
			$args['required_document_ids'],
			null,
			$args['applicability']
		);
	}

	if ( ! is_array( $raw ) ) {
		return new WP_Error( 'nl_proposal_invalid_evidence', 'Evidence must be an object, not a bare value.' );
	}

	$state = isset( $raw['state'] ) ? sanitize_key( $raw['state'] ) : 'unknown';
	if ( ! in_array( $state, nl_proposal_evidence_states(), true ) ) {
		return new WP_Error( 'nl_proposal_invalid_evidence_state', 'Evidence state is unsupported.' );
	}

	$unit = null;
	if ( isset( $raw['unit'] ) && '' !== $raw['unit'] ) {
		$unit = nl_proposal_sanitize_contract_id( $raw['unit'], 'evidence.unit' );
		if ( is_wp_error( $unit ) ) {
			return $unit;
		}
		if ( ! empty( $args['unit_allowed'] ) && ! in_array( $unit, $args['unit_allowed'], true ) ) {
			return new WP_Error( 'nl_proposal_invalid_unit', 'Evidence unit is not allowed for this field.' );
		}
	}

	$note = '';
	if ( isset( $raw['note'] ) && '' !== $raw['note'] ) {
		if ( ! is_scalar( $raw['note'] ) ) {
			return new WP_Error( 'nl_proposal_invalid_note', 'Evidence note must be text.' );
		}
		$note = sanitize_textarea_field( (string) $raw['note'] );
		if ( strlen( $note ) > 3000 ) {
			return new WP_Error( 'nl_proposal_note_too_long', 'Evidence note exceeds 3000 bytes.' );
		}
	}

	$caveat = '';
	if ( isset( $raw['caveat'] ) && '' !== $raw['caveat'] ) {
		if ( ! is_scalar( $raw['caveat'] ) ) {
			return new WP_Error( 'nl_proposal_invalid_caveat', 'Evidence caveat must be text.' );
		}
		$caveat = sanitize_textarea_field( (string) $raw['caveat'] );
		if ( strlen( $caveat ) > 3000 ) {
			return new WP_Error( 'nl_proposal_caveat_too_long', 'Evidence caveat exceeds 3000 bytes.' );
		}
	}

	$scope = null;
	if ( isset( $raw['scope'] ) && '' !== $raw['scope'] ) {
		$scope = nl_proposal_sanitize_bounded_text( $raw['scope'], 'evidence.scope', 500, false );
		if ( is_wp_error( $scope ) ) {
			return $scope;
		}
	}

	$effective_at = nl_proposal_normalize_rfc3339(
		isset( $raw['effective_at'] ) ? $raw['effective_at'] : null,
		'evidence.effective_at',
		true
	);
	if ( is_wp_error( $effective_at ) ) {
		return $effective_at;
	}

	$confidence = isset( $raw['confidence'] ) && is_scalar( $raw['confidence'] )
		? sanitize_key( (string) $raw['confidence'] )
		: 'unknown';
	if ( ! in_array( $confidence, nl_proposal_confidence_levels(), true ) ) {
		return new WP_Error( 'nl_proposal_invalid_confidence', 'Evidence confidence is unsupported.' );
	}

	$applicability = array();
	$raw_applicability = isset( $raw['applicability'] ) ? $raw['applicability'] : $args['applicability'];
	if ( ! is_array( $raw_applicability ) || empty( $raw_applicability ) ) {
		return new WP_Error( 'nl_proposal_invalid_evidence_applicability', 'Evidence applicability must be a non-empty list.' );
	}
	foreach ( $raw_applicability as $applicability_id ) {
		$applicability_id = nl_proposal_sanitize_contract_id( $applicability_id, 'evidence.applicability[]' );
		if ( is_wp_error( $applicability_id ) ) {
			return $applicability_id;
		}
		$applicability[] = $applicability_id;
	}
	$applicability = array_values( array_unique( $applicability ) );

	$conflict_ids = array();
	$raw_conflict_ids = isset( $raw['conflict_ids'] ) ? $raw['conflict_ids'] : array();
	if ( ! is_array( $raw_conflict_ids ) ) {
		return new WP_Error( 'nl_proposal_invalid_conflict_ids', 'conflict_ids must be a list.' );
	}
	foreach ( $raw_conflict_ids as $conflict_id ) {
		$conflict_id = nl_proposal_sanitize_contract_id( $conflict_id, 'evidence.conflict_ids[]' );
		if ( is_wp_error( $conflict_id ) ) {
			return $conflict_id;
		}
		$conflict_ids[] = $conflict_id;
	}
	if ( count( array_unique( $conflict_ids ) ) !== count( $conflict_ids ) ) {
		return new WP_Error( 'nl_proposal_duplicate_conflict_id', 'conflict_ids must be unique.' );
	}

	$required_document_ids = array();
	$raw_document_ids      = isset( $raw['required_document_ids'] ) ? $raw['required_document_ids'] : $args['required_document_ids'];
	if ( ! is_array( $raw_document_ids ) ) {
		return new WP_Error( 'nl_proposal_invalid_document_ids', 'required_document_ids must be a list.' );
	}
	foreach ( $raw_document_ids as $document_id ) {
		$document_id = nl_proposal_sanitize_contract_id( $document_id, 'required_document_ids[]' );
		if ( is_wp_error( $document_id ) ) {
			return $document_id;
		}
		$required_document_ids[] = $document_id;
	}
	$required_document_ids = array_values( array_unique( $required_document_ids ) );

	$sources = array();
	if ( isset( $raw['sources'] ) ) {
		if ( ! is_array( $raw['sources'] ) ) {
			return new WP_Error( 'nl_proposal_invalid_sources', 'sources must be a list.' );
		}
		foreach ( $raw['sources'] as $source ) {
			$source = nl_proposal_normalize_evidence_source( $source );
			if ( is_wp_error( $source ) ) {
				return $source;
			}
			$sources[] = $source;
		}
	}

	$owner = nl_proposal_normalize_data_owner(
		isset( $raw['owner'] ) ? $raw['owner'] : null,
		'unknown' !== $state
	);
	if ( is_wp_error( $owner ) ) {
		return $owner;
	}

	$verified_at = nl_proposal_normalize_rfc3339(
		isset( $raw['verified_at'] ) ? $raw['verified_at'] : null,
		'evidence.verified_at',
		true
	);
	if ( is_wp_error( $verified_at ) ) {
		return $verified_at;
	}

	$expires_at = nl_proposal_normalize_rfc3339(
		isset( $raw['expires_at'] ) ? $raw['expires_at'] : null,
		'evidence.expires_at',
		true
	);
	if ( is_wp_error( $expires_at ) ) {
		return $expires_at;
	}

	$value        = null;
	$observations = array();
	$reason       = '';
	if ( isset( $raw['reason'] ) && '' !== $raw['reason'] ) {
		$reason = nl_proposal_sanitize_bounded_text( $raw['reason'], 'evidence.reason', 1000, false );
		if ( is_wp_error( $reason ) ) {
			return $reason;
		}
	}

	if ( 'unknown' === $state ) {
		if ( array_key_exists( 'value', $raw ) && null !== $raw['value'] ) {
			return new WP_Error( 'nl_proposal_unknown_with_value', 'Unknown evidence cannot carry a value.' );
		}
		if ( null !== $effective_at || null !== $verified_at || null !== $expires_at ) {
			return new WP_Error( 'nl_proposal_unknown_with_verification', 'Unknown evidence cannot be verified or expire.' );
		}
		if ( 'unknown' !== $confidence ) {
			return new WP_Error( 'nl_proposal_unknown_with_confidence', 'Unknown evidence confidence must be unknown.' );
		}
		if ( ! empty( $conflict_ids ) ) {
			return new WP_Error( 'nl_proposal_unknown_with_conflicts', 'Unknown evidence cannot carry conflict_ids.' );
		}
		if ( '' === $reason ) {
			$reason = '' !== $note ? $note : (string) $args['unknown_reason'];
		}
	} elseif ( 'contradictory' === $state ) {
		if ( array_key_exists( 'value', $raw ) && null !== $raw['value'] ) {
			return new WP_Error( 'nl_proposal_contradiction_with_value', 'Contradictory evidence cannot choose a value.' );
		}
		if ( ! isset( $raw['observations'] ) || ! is_array( $raw['observations'] ) ) {
			return new WP_Error( 'nl_proposal_missing_observations', 'Contradictory evidence needs observations.' );
		}
		foreach ( $raw['observations'] as $observation ) {
			$observation = nl_proposal_normalize_observation(
				$observation,
				$value_type,
				array(
					'min'               => $args['min'],
					'max'               => $args['max'],
					'allowed'           => $args['allowed'],
					'string_max_length' => $args['string_max_length'],
					'string_field'      => $args['string_field'],
				)
			);
			if ( is_wp_error( $observation ) ) {
				return $observation;
			}
			$observations[] = $observation;
		}
		if ( count( $observations ) < 2 ) {
			return new WP_Error( 'nl_proposal_insufficient_observations', 'Contradictory evidence needs at least two sourced observations.' );
		}
		if ( null !== $verified_at || null !== $expires_at ) {
			return new WP_Error( 'nl_proposal_contradiction_with_verification', 'A contradiction cannot be verified or expire.' );
		}
		if ( null === $effective_at || null === $scope || '' === $scope || 'unknown' === $confidence ) {
			return new WP_Error( 'nl_proposal_incomplete_contradiction_context', 'Contradictory evidence needs scope, effective_at and explicit confidence.' );
		}
		$effective_epoch = nl_proposal_timestamp_to_epoch( $effective_at );
		if ( null === $effective_epoch || $effective_epoch > (int) $args['now'] + 300 || '' !== $reason ) {
			return new WP_Error( 'nl_proposal_invalid_contradiction_context', 'Contradictory evidence effective_at/reason is invalid.' );
		}
		$observation_ids = array_map(
			function ( $observation ) {
				return $observation['observation_id'];
			},
			$observations
		);
		if ( count( array_unique( $observation_ids ) ) !== count( $observation_ids ) ) {
			return new WP_Error( 'nl_proposal_duplicate_observation_id', 'Contradictory observation IDs must be unique.' );
		}
		$expected_conflict_ids = $observation_ids;
		$actual_conflict_ids   = $conflict_ids;
		sort( $expected_conflict_ids );
		sort( $actual_conflict_ids );
		if ( $expected_conflict_ids !== $actual_conflict_ids ) {
			return new WP_Error( 'nl_proposal_conflict_id_mismatch', 'conflict_ids must identify every contradictory observation exactly.' );
		}
	} else {
		if ( ! array_key_exists( 'value', $raw ) || null === $raw['value'] ) {
			return new WP_Error( 'nl_proposal_missing_evidence_value', 'Verified or estimated evidence needs a value.' );
		}
		$value = nl_proposal_normalize_evidence_value(
			$raw['value'],
			$value_type,
			array(
				'min'               => $args['min'],
				'max'               => $args['max'],
				'allowed'           => $args['allowed'],
				'string_max_length' => $args['string_max_length'],
				'string_field'      => $args['string_field'],
			)
		);
		if ( is_wp_error( $value ) ) {
			return $value;
		}
		if ( empty( $sources ) ) {
			return new WP_Error( 'nl_proposal_evidence_without_source', 'Verified or estimated evidence needs at least one source.' );
		}
		if ( null === $expires_at ) {
			return new WP_Error( 'nl_proposal_evidence_without_expiry', 'Verified or estimated evidence needs expires_at.' );
		}
		if ( null === $effective_at || null === $scope || '' === $scope || 'unknown' === $confidence ) {
			return new WP_Error( 'nl_proposal_incomplete_evidence_context', 'Verified or estimated evidence needs scope, effective_at and explicit confidence.' );
		}
		if ( ! empty( $conflict_ids ) || '' !== $reason ) {
			return new WP_Error( 'nl_proposal_positive_evidence_with_missing_or_conflict_fields', 'Current positive evidence cannot carry reason or conflict_ids.' );
		}
		$effective_epoch = nl_proposal_timestamp_to_epoch( $effective_at );
		if ( null === $effective_epoch || $effective_epoch > (int) $args['now'] + 300 ) {
			return new WP_Error( 'nl_proposal_future_effective_at', 'effective_at cannot be in the future.' );
		}
		$expires_epoch = nl_proposal_timestamp_to_epoch( $expires_at );
		if ( null === $expires_epoch || $expires_epoch <= (int) $args['now'] || $expires_epoch <= $effective_epoch ) {
			return new WP_Error( 'nl_proposal_expired_evidence', 'Evidence has expired and must not be published as current.' );
		}

		if ( 'verified' === $state ) {
			if ( null === $verified_at ) {
				return new WP_Error( 'nl_proposal_verified_without_timestamp', 'Verified evidence needs verified_at.' );
			}
			$verified_epoch = nl_proposal_timestamp_to_epoch( $verified_at );
			if ( null === $verified_epoch || $verified_epoch > (int) $args['now'] + 300 ) {
				return new WP_Error( 'nl_proposal_future_verification', 'verified_at cannot be in the future.' );
			}
			if ( $expires_epoch <= $verified_epoch ) {
				return new WP_Error( 'nl_proposal_invalid_evidence_window', 'expires_at must be after verified_at.' );
			}
			if ( (int) $args['max_verified_lifetime_seconds'] > 0 && ( $expires_epoch - $verified_epoch ) > (int) $args['max_verified_lifetime_seconds'] ) {
				return new WP_Error( 'nl_proposal_evidence_window_too_long', 'Evidence freshness window exceeds the allowed maximum.' );
			}
		} else {
			if ( null !== $verified_at ) {
				return new WP_Error( 'nl_proposal_estimate_marked_verified', 'A source estimate cannot carry verified_at.' );
			}
			if ( (int) $args['max_verified_lifetime_seconds'] > 0 && ( $expires_epoch - (int) $args['now'] ) > (int) $args['max_verified_lifetime_seconds'] ) {
				return new WP_Error( 'nl_proposal_evidence_window_too_long', 'Estimate freshness window exceeds the allowed maximum.' );
			}
		}
	}

	return array(
		'state'                 => $state,
		'value'                 => $value,
		'unit'                  => $unit,
		'scope'                 => $scope,
		'effective_at'          => $effective_at,
		'sources'               => array_values( $sources ),
		'observations'          => array_values( $observations ),
		'verified_at'           => $verified_at,
		'expires_at'            => $expires_at,
		'owner'                 => $owner,
		'confidence'            => $confidence,
		'reason'                => $reason,
		'applicability'         => $applicability,
		'conflict_ids'          => $conflict_ids,
		'note'                  => $note,
		'caveat'                => $caveat,
		'required_document_ids' => $required_document_ids,
		'decision_grade'        => 'verified' === $state,
	);
}

/**
 * Normalize a commercial availability envelope.
 *
 * Any non-unknown status must be verified and may remain current for no more
 * than 24 hours. Legacy "available" therefore fails instead of being promoted.
 *
 * @param mixed $raw Raw status evidence.
 * @param array $args Optional now timestamp.
 * @return array|WP_Error
 */
function nl_proposal_normalize_commercial_availability( $raw, $args = array() ) {
	$args = wp_parse_args( $args, array( 'now' => time() ) );

	if ( null === $raw || array() === $raw ) {
		return nl_proposal_unknown_evidence(
			'No current owner-controlled availability record was supplied.',
			array( 'availability_schedule' )
		);
	}

	$normalized = nl_proposal_normalize_evidence_envelope(
		$raw,
		'status',
		array(
			'now'                           => $args['now'],
			'allowed'                       => nl_proposal_commercial_statuses(),
			'required_document_ids'         => array( 'availability_schedule' ),
			'max_verified_lifetime_seconds' => DAY_IN_SECONDS,
		)
	);

	if ( is_wp_error( $normalized ) ) {
		return $normalized;
	}

	if ( 'unknown' === $normalized['state'] ) {
		return $normalized;
	}

	if ( 'verified' !== $normalized['state'] ) {
		return new WP_Error(
			'nl_proposal_unverified_availability',
			'Commercial availability may only be verified or unknown.'
		);
	}

	if ( 'unknown' === $normalized['value'] ) {
		return nl_proposal_unknown_evidence(
			'The authoritative record explicitly reports unknown.',
			array( 'availability_schedule' ),
			$normalized['owner']
		);
	}

	return $normalized;
}

/**
 * Normalize one verified facade exposure.
 *
 * A whole office floor can have several exposures. No direction is inferred
 * from the 3D camera, model rotation, address, or a legacy "west" default.
 *
 * @param mixed $raw Raw exposure.
 * @param array $args Optional now timestamp.
 * @return array|WP_Error
 */
function nl_proposal_normalize_commercial_exposure( $raw, $args = array() ) {
	$args = wp_parse_args( $args, array( 'now' => time() ) );

	if ( ! is_array( $raw ) ) {
		return new WP_Error( 'nl_proposal_invalid_exposure', 'Each exposure must be an object.' );
	}

	$exposure_id = nl_proposal_sanitize_contract_id(
		isset( $raw['exposure_id'] ) ? $raw['exposure_id'] : '',
		'exposure.exposure_id'
	);
	if ( is_wp_error( $exposure_id ) ) {
		return $exposure_id;
	}

	$direction = nl_proposal_normalize_evidence_envelope(
		isset( $raw['direction'] ) ? $raw['direction'] : null,
		'compass',
		array(
			'now'                           => $args['now'],
			'max_verified_lifetime_seconds' => 365 * DAY_IN_SECONDS,
			'required_document_ids'         => array( 'orientation_plan' ),
		)
	);
	if ( is_wp_error( $direction ) ) {
		return $direction;
	}
	if ( 'verified' !== $direction['state'] ) {
		return new WP_Error(
			'nl_proposal_unverified_exposure_direction',
			'An exposure is renderable only when its direction is verified.'
		);
	}

	$azimuth_start = nl_proposal_normalize_evidence_envelope(
		isset( $raw['azimuth_start_deg'] ) ? $raw['azimuth_start_deg'] : null,
		'decimal',
		array(
			'now'           => $args['now'],
			'min'           => 0,
			'max'           => 360,
			'unit_allowed'  => array( 'degrees_true_north' ),
			'unknown_reason'=> 'Azimuth start was not supplied.',
		)
	);
	if ( is_wp_error( $azimuth_start ) ) {
		return $azimuth_start;
	}

	$azimuth_end = nl_proposal_normalize_evidence_envelope(
		isset( $raw['azimuth_end_deg'] ) ? $raw['azimuth_end_deg'] : null,
		'decimal',
		array(
			'now'           => $args['now'],
			'min'           => 0,
			'max'           => 360,
			'unit_allowed'  => array( 'degrees_true_north' ),
			'unknown_reason'=> 'Azimuth end was not supplied.',
		)
	);
	if ( is_wp_error( $azimuth_end ) ) {
		return $azimuth_end;
	}

	$facade_share = nl_proposal_normalize_evidence_envelope(
		isset( $raw['facade_share_pct'] ) ? $raw['facade_share_pct'] : null,
		'decimal',
		array(
			'now'          => $args['now'],
			'min'          => 0,
			'max'          => 100,
			'unit_allowed' => array( 'percent' ),
		)
	);
	if ( is_wp_error( $facade_share ) ) {
		return $facade_share;
	}

	$views = nl_proposal_normalize_evidence_envelope(
		isset( $raw['view_context'] ) ? $raw['view_context'] : null,
		'string_list',
		array(
			'now'                           => $args['now'],
			'max_verified_lifetime_seconds' => 90 * DAY_IN_SECONDS,
			'required_document_ids'         => array( 'view_study' ),
		)
	);
	if ( is_wp_error( $views ) ) {
		return $views;
	}

	$obstructions = nl_proposal_normalize_evidence_envelope(
		isset( $raw['obstructions'] ) ? $raw['obstructions'] : null,
		'string_list',
		array(
			'now'                           => $args['now'],
			'max_verified_lifetime_seconds' => 90 * DAY_IN_SECONDS,
			'required_document_ids'         => array( 'view_study' ),
		)
	);
	if ( is_wp_error( $obstructions ) ) {
		return $obstructions;
	}

	return array(
		'exposure_id'       => $exposure_id,
		'direction'         => $direction,
		'azimuth_start_deg' => $azimuth_start,
		'azimuth_end_deg'   => $azimuth_end,
		'facade_share_pct'  => $facade_share,
		'view_context'      => $views,
		'obstructions'      => $obstructions,
	);
}

/**
 * Normalize a list of commercial exposures.
 *
 * @param mixed $raw Raw list.
 * @param array $args Optional now timestamp.
 * @return array|WP_Error
 */
function nl_proposal_normalize_commercial_exposures( $raw, $args = array() ) {
	if ( null === $raw || array() === $raw ) {
		return array();
	}
	if ( ! is_array( $raw ) ) {
		return new WP_Error( 'nl_proposal_invalid_exposures', 'exposures must be a list.' );
	}

	$normalized = array();
	$ids        = array();
	foreach ( $raw as $exposure ) {
		$exposure = nl_proposal_normalize_commercial_exposure( $exposure, $args );
		if ( is_wp_error( $exposure ) ) {
			return $exposure;
		}
		if ( isset( $ids[ $exposure['exposure_id'] ] ) ) {
			return new WP_Error( 'nl_proposal_duplicate_exposure', 'Exposure IDs must be unique.' );
		}
		$ids[ $exposure['exposure_id'] ] = true;
		$normalized[]                    = $exposure;
	}

	return $normalized;
}

/**
 * Normalize an optional scalar evidence field using a standard definition.
 *
 * @param array  $raw Source object.
 * @param string $key Field key.
 * @param string $type Value type.
 * @param array  $args Evidence constraints.
 * @return array|WP_Error
 */
function nl_proposal_normalize_evidence_field( $raw, $key, $type, $args = array() ) {
	return nl_proposal_normalize_evidence_envelope(
		isset( $raw[ $key ] ) ? $raw[ $key ] : null,
		$type,
		$args
	);
}

/**
 * Build a stable composite identity. Floor/suite IDs may repeat in another
 * tower, so no consumer may key them without building and tower.
 *
 * @return string
 */
function nl_proposal_commercial_identity_key( $building_id, $tower_id, $floor_id = '', $suite_id = '' ) {
	return implode( '|', array( (string) $building_id, (string) $tower_id, (string) $floor_id, (string) $suite_id ) );
}

/**
 * Build a shareable project/floor/suite URL without placing buyer data in it.
 *
 * @return string
 */
function nl_proposal_commercial_identity_url( $project_url, $project_contract_id, $building_id = '', $tower_id = '', $floor_id = '', $suite_id = '' ) {
	$params = array();
	foreach (
		array(
			'building_id'         => $building_id,
			'floor_id'            => $floor_id,
			'project_contract_id' => $project_contract_id,
			'suite_id'            => $suite_id,
			'tower_id'            => $tower_id,
		) as $key => $value
	) {
		if ( '' !== (string) $value ) {
			$params[ $key ] = (string) $value;
		}
	}
	if ( empty( $params ) ) {
		return (string) $project_url;
	}
	return esc_url_raw( add_query_arg( $params, (string) $project_url ), array( 'https' ) );
}

/**
 * Normalize the immutable building/tower crosswalk and evidenced public label.
 *
 * @return array|WP_Error
 */
function nl_proposal_normalize_commercial_towers( $raw, $args = array() ) {
	$args = wp_parse_args( $args, array( 'now' => time() ) );
	if ( ! is_array( $raw ) || empty( $raw ) ) {
		return new WP_Error( 'nl_proposal_missing_tower_crosswalk', 'A non-empty building/tower crosswalk is required.' );
	}
	$normalized = array();
	$keys       = array();
	foreach ( $raw as $entry ) {
		if ( ! is_array( $entry ) ) {
			return new WP_Error( 'nl_proposal_invalid_tower_crosswalk', 'Each tower crosswalk entry must be an object.' );
		}
		$building_id = nl_proposal_sanitize_contract_id( isset( $entry['building_id'] ) ? $entry['building_id'] : '', 'tower.building_id' );
		$tower_id    = nl_proposal_sanitize_contract_id( isset( $entry['tower_id'] ) ? $entry['tower_id'] : '', 'tower.tower_id' );
		if ( is_wp_error( $building_id ) ) return $building_id;
		if ( is_wp_error( $tower_id ) ) return $tower_id;
		$key = nl_proposal_commercial_identity_key( $building_id, $tower_id );
		if ( isset( $keys[ $key ] ) ) {
			return new WP_Error( 'nl_proposal_duplicate_tower', 'Building/tower crosswalk identities must be unique.' );
		}
		$display_label = nl_proposal_normalize_evidence_field(
			$entry,
			'display_label',
			'string',
			array(
				'now'                           => $args['now'],
				'max_verified_lifetime_seconds' => 365 * DAY_IN_SECONDS,
				'required_document_ids'         => array( 'floor_id_crosswalk' ),
				'applicability'                 => array( 'tower_identity' ),
			)
		);
		if ( is_wp_error( $display_label ) ) return $display_label;
		if ( 'verified' !== $display_label['state'] || '' === trim( (string) $display_label['value'] ) ) {
			return new WP_Error( 'nl_proposal_unverified_tower_label', 'Every canonical tower needs a verified, non-empty display label.' );
		}
		$keys[ $key ] = true;
		$normalized[] = array(
			'building_id'  => $building_id,
			'tower_id'     => $tower_id,
			'identity_key' => $key,
			'display_label'=> $display_label,
		);
	}
	return $normalized;
}

/**
 * Normalize a commercial suite.
 *
 * @param mixed  $raw Raw suite.
 * @param string $floor_id Parent floor ID.
 * @param array  $args Optional now timestamp.
 * @return array|WP_Error
 */
function nl_proposal_normalize_commercial_suite( $raw, $floor_id, $args = array() ) {
	$args = wp_parse_args(
		$args,
		array(
			'now'                 => time(),
			'building_id'         => '',
			'tower_id'            => '',
			'tower_display_label' => null,
			'project_url'         => '',
			'project_contract_id' => '',
		)
	);
	if ( ! is_array( $raw ) ) {
		return new WP_Error( 'nl_proposal_invalid_suite', 'Each suite must be an object.' );
	}

	$suite_id = nl_proposal_sanitize_contract_id(
		isset( $raw['suite_id'] ) ? $raw['suite_id'] : '',
		'suite.suite_id'
	);
	if ( is_wp_error( $suite_id ) ) {
		return $suite_id;
	}
	foreach (
		array(
			'building_id' => $args['building_id'],
			'tower_id'    => $args['tower_id'],
			'floor_id'    => $floor_id,
		) as $identity_field => $expected_identity
	) {
		$actual_identity = nl_proposal_sanitize_contract_id(
			isset( $raw[ $identity_field ] ) ? $raw[ $identity_field ] : '',
			'suite.' . $identity_field
		);
		if ( is_wp_error( $actual_identity ) ) {
			return $actual_identity;
		}
		if ( $actual_identity !== $expected_identity ) {
			return new WP_Error(
				'nl_proposal_suite_identity_mismatch',
				'Suite building_id/tower_id/floor_id must exactly match its parent floor.'
			);
		}
	}

	$label = nl_proposal_normalize_evidence_field(
		$raw,
		'label',
		'string',
		array(
			'now'                           => $args['now'],
			'max_verified_lifetime_seconds' => 365 * DAY_IN_SECONDS,
			'required_document_ids'         => array( 'availability_schedule' ),
		)
	);
	if ( is_wp_error( $label ) ) {
		return $label;
	}

	$availability = nl_proposal_normalize_commercial_availability(
		isset( $raw['availability'] ) ? $raw['availability'] : null,
		$args
	);
	if ( is_wp_error( $availability ) ) {
		return $availability;
	}

	$gross = nl_proposal_normalize_evidence_field(
		$raw,
		'gross_rentable_sqm',
		'decimal',
		array(
			'now'          => $args['now'],
			'min'          => 0,
			'max'          => 1000000,
			'unit_allowed' => array( 'sqm_rentable_gross' ),
			'required_document_ids' => array( 'measurement_report' ),
		)
	);
	if ( is_wp_error( $gross ) ) {
		return $gross;
	}

	$usable = nl_proposal_normalize_evidence_field(
		$raw,
		'usable_sqm',
		'decimal',
		array(
			'now'          => $args['now'],
			'min'          => 0,
			'max'          => 1000000,
			'unit_allowed' => array( 'sqm_usable' ),
			'required_document_ids' => array( 'measurement_report' ),
		)
	);
	if ( is_wp_error( $usable ) ) {
		return $usable;
	}

	$asking_rent = nl_proposal_normalize_evidence_field(
		$raw,
		'asking_rent_nis_sqm_month',
		'decimal',
		array(
			'now'                           => $args['now'],
			'min'                           => 0,
			'max'                           => 100000,
			'unit_allowed'                  => array( 'nis_per_rentable_sqm_month' ),
			'max_verified_lifetime_seconds' => 7 * DAY_IN_SECONDS,
			'required_document_ids'         => array( 'landlord_offer' ),
		)
	);
	if ( is_wp_error( $asking_rent ) ) {
		return $asking_rent;
	}

	$service_charge = nl_proposal_normalize_evidence_field(
		$raw,
		'service_charge_nis_sqm_month',
		'decimal',
		array(
			'now'          => $args['now'],
			'min'          => 0,
			'max'          => 100000,
			'unit_allowed' => array( 'nis_per_rentable_sqm_month' ),
			'required_document_ids' => array( 'service_charge_budget' ),
		)
	);
	if ( is_wp_error( $service_charge ) ) {
		return $service_charge;
	}

	$available_from = nl_proposal_normalize_evidence_field(
		$raw,
		'available_from',
		'date',
		array(
			'now'                   => $args['now'],
			'required_document_ids' => array( 'handover_schedule' ),
		)
	);
	if ( is_wp_error( $available_from ) ) {
		return $available_from;
	}

	$headcount = nl_proposal_normalize_evidence_field(
		$raw,
		'test_fit_headcount',
		'integer',
		array(
			'now'                   => $args['now'],
			'min'                   => 0,
			'max'                   => 100000,
			'unit_allowed'          => array( 'people' ),
			'required_document_ids' => array( 'validated_test_fit' ),
		)
	);
	if ( is_wp_error( $headcount ) ) {
		return $headcount;
	}

	$exposures = nl_proposal_normalize_commercial_exposures(
		isset( $raw['exposures'] ) ? $raw['exposures'] : array(),
		$args
	);
	if ( is_wp_error( $exposures ) ) {
		return $exposures;
	}

	return array(
		'suite_id'                     => $suite_id,
		'floor_id'                     => $floor_id,
		'building_id'                  => $args['building_id'],
		'tower_id'                     => $args['tower_id'],
		'tower_display_label'          => $args['tower_display_label'],
		'identity_key'                 => nl_proposal_commercial_identity_key( $args['building_id'], $args['tower_id'], $floor_id, $suite_id ),
		'url'                          => nl_proposal_commercial_identity_url( $args['project_url'], $args['project_contract_id'], $args['building_id'], $args['tower_id'], $floor_id, $suite_id ),
		'label'                        => $label,
		'selectable'                   => 'verified' === $label['state'],
		'availability'                 => $availability,
		'gross_rentable_sqm'           => $gross,
		'usable_sqm'                   => $usable,
		'asking_rent_nis_sqm_month'    => $asking_rent,
		'service_charge_nis_sqm_month' => $service_charge,
		'available_from'               => $available_from,
		'test_fit_headcount'           => $headcount,
		'exposures'                    => $exposures,
	);
}

/** Return whether a normalized claim may appear in the orientation schematic. */
function nl_proposal_beam_claim_allowed( $claim ) {
	return is_array( $claim ) && in_array( isset( $claim['state'] ) ? $claim['state'] : '', array( 'verified', 'source_estimate' ), true );
}

/** Return whether a true-north bearing belongs to an azimuth sector. */
function nl_proposal_beam_bearing_in_sector( $bearing, $start, $end ) {
	$bearing = fmod( (float) $bearing + 360.0, 360.0 );
	$start   = fmod( (float) $start + 360.0, 360.0 );
	$end     = fmod( (float) $end + 360.0, 360.0 );
	if ( abs( $start - $end ) < 0.000001 ) {
		return abs( $bearing - $start ) <= 1.0;
	}
	return $start < $end
		? $bearing >= $start && $bearing <= $end
		: $bearing >= $start || $bearing <= $end;
}

/** Compute straight-line distance and initial true-north bearing. */
function nl_proposal_beam_geodesic_metrics( $anchor, $coordinate ) {
	$earth_radius = 6371008.8;
	$lat1 = deg2rad( (float) $anchor['lat'] );
	$lat2 = deg2rad( (float) $coordinate['lat'] );
	$dlat = $lat2 - $lat1;
	$dlng = deg2rad( (float) $coordinate['lng'] - (float) $anchor['lng'] );
	$a = sin( $dlat / 2 ) * sin( $dlat / 2 ) + cos( $lat1 ) * cos( $lat2 ) * sin( $dlng / 2 ) * sin( $dlng / 2 );
	$distance = $earth_radius * 2 * atan2( sqrt( $a ), sqrt( max( 0, 1 - $a ) ) );
	$y = sin( $dlng ) * cos( $lat2 );
	$x = cos( $lat1 ) * sin( $lat2 ) - sin( $lat1 ) * cos( $lat2 ) * cos( $dlng );
	$bearing = fmod( rad2deg( atan2( $y, $x ) ) + 360.0, 360.0 );
	return array( 'distance_m' => $distance, 'bearing_deg' => $bearing );
}

/** Build the only safe incomplete beam state: neutral, with no drawable data. */
function nl_proposal_neutral_commercial_beam_scene( $anchor, $caveat = '', $issues = array() ) {
	return array(
		'scene_state'         => 'unknown',
		'projection'          => 'north_up_local_equirectangular_v1',
		'project_anchor'      => $anchor,
		'exposures'           => array(),
		'illustrative_caveat' => (string) $caveat,
		'issues'              => array_values( array_unique( $issues ) ),
	);
}

/**
 * Normalize a complete, north-up, evidenced local orientation schematic.
 * Every floor exposure needs exactly one association. One incomplete or
 * contradictory configured claim makes the whole scene neutral; partial cones
 * are more misleading than an explicit request state.
 */
function nl_proposal_normalize_commercial_beam_scene( $raw, $args = array() ) {
	$args = wp_parse_args( $args, array( 'now' => time(), 'facade_exposures' => array() ) );
	$unknown_anchor = nl_proposal_unknown_evidence(
		'No evidenced project coordinate was supplied.',
		array( 'orientation_plan' ),
		null,
		array( 'beam_scene' )
	);
	if ( null === $raw || array() === $raw ) {
		return nl_proposal_neutral_commercial_beam_scene( $unknown_anchor, '', array( 'beam_scene_not_configured' ) );
	}
	if ( ! is_array( $raw ) ) {
		return new WP_Error( 'nl_proposal_invalid_beam_scene', 'beam_scene must be an object.' );
	}
	if ( isset( $raw['landmarks'] ) ) {
		return new WP_Error( 'nl_proposal_legacy_beam_landmarks', 'Landmarks must be nested under an exposure_id association.' );
	}

	$anchor = nl_proposal_normalize_evidence_envelope(
		isset( $raw['project_anchor'] ) ? $raw['project_anchor'] : null,
		'coordinate',
		array(
			'now'                           => $args['now'],
			'max_verified_lifetime_seconds' => 365 * DAY_IN_SECONDS,
			'required_document_ids'         => array( 'orientation_plan' ),
			'unknown_reason'                => 'No evidenced project coordinate was supplied.',
			'applicability'                 => array( 'beam_scene' ),
		)
	);
	if ( is_wp_error( $anchor ) ) return $anchor;

	$caveat = '';
	if ( isset( $raw['illustrative_caveat'] ) && '' !== $raw['illustrative_caveat'] ) {
		$caveat = nl_proposal_sanitize_bounded_text( $raw['illustrative_caveat'], 'beam_scene.illustrative_caveat', 500, false );
		if ( is_wp_error( $caveat ) ) return $caveat;
	}

	$facade_by_id = array();
	foreach ( $args['facade_exposures'] as $facade ) {
		if ( is_array( $facade ) && ! empty( $facade['exposure_id'] ) ) {
			$facade_by_id[ $facade['exposure_id'] ] = $facade;
		}
	}
	$raw_associations = isset( $raw['exposures'] ) ? $raw['exposures'] : array();
	if ( ! is_array( $raw_associations ) ) {
		return new WP_Error( 'nl_proposal_invalid_beam_exposures', 'beam_scene.exposures must be a list.' );
	}
	$associations = array();
	$association_ids = array();
	$landmark_ids = array();
	$total_landmarks = 0;
	foreach ( $raw_associations as $raw_association ) {
		if ( ! is_array( $raw_association ) ) return new WP_Error( 'nl_proposal_invalid_beam_exposure', 'Each beam exposure association must be an object.' );
		$exposure_id = nl_proposal_sanitize_contract_id( isset( $raw_association['exposure_id'] ) ? $raw_association['exposure_id'] : '', 'beam_scene.exposure_id' );
		if ( is_wp_error( $exposure_id ) ) return $exposure_id;
		if ( isset( $association_ids[ $exposure_id ] ) ) return new WP_Error( 'nl_proposal_duplicate_beam_exposure', 'Beam exposure associations must be unique.' );
		if ( ! isset( $facade_by_id[ $exposure_id ] ) ) return new WP_Error( 'nl_proposal_unknown_beam_exposure', 'Beam exposure_id is absent from floor.exposures.' );
		$association_ids[ $exposure_id ] = true;
		$raw_landmarks = isset( $raw_association['landmarks'] ) ? $raw_association['landmarks'] : array();
		if ( ! is_array( $raw_landmarks ) ) return new WP_Error( 'nl_proposal_invalid_beam_landmarks', 'Beam exposure landmarks must be a list.' );
		if ( empty( $raw_landmarks ) ) return new WP_Error( 'nl_proposal_missing_beam_landmarks', 'Every configured exposure needs at least one evidenced landmark association.' );
		$landmarks = array();
		foreach ( $raw_landmarks as $raw_landmark ) {
			if ( ! is_array( $raw_landmark ) ) return new WP_Error( 'nl_proposal_invalid_beam_landmark', 'Each beam landmark must be an object.' );
			$landmark_exposure_id = nl_proposal_sanitize_contract_id(
				isset( $raw_landmark['exposure_id'] ) ? $raw_landmark['exposure_id'] : '',
				'beam_scene.landmark.exposure_id'
			);
			if ( is_wp_error( $landmark_exposure_id ) ) return $landmark_exposure_id;
			if ( $landmark_exposure_id !== $exposure_id ) {
				return new WP_Error( 'nl_proposal_beam_landmark_exposure_mismatch', 'Landmark exposure_id must exactly match its containing exposure association.' );
			}
			$landmark_id = nl_proposal_sanitize_contract_id( isset( $raw_landmark['landmark_id'] ) ? $raw_landmark['landmark_id'] : '', 'beam_scene.landmark_id' );
			if ( is_wp_error( $landmark_id ) ) return $landmark_id;
			if ( isset( $landmark_ids[ $landmark_id ] ) ) return new WP_Error( 'nl_proposal_duplicate_beam_landmark', 'Landmark IDs must be unique across the scene.' );
			$landmark_ids[ $landmark_id ] = true;
			$total_landmarks++;
			if ( $total_landmarks > 4 ) return new WP_Error( 'nl_proposal_too_many_beam_landmarks', 'The fixed compact beam scene supports at most four evidenced landmark associations; additional context belongs in the full context tool.' );

			$claim_args = array(
				'now'                           => $args['now'],
				'max_verified_lifetime_seconds' => 365 * DAY_IN_SECONDS,
				'required_document_ids'         => array( 'orientation_plan' ),
				'applicability'                 => array( 'beam_scene', $exposure_id ),
			);
			$label = nl_proposal_normalize_evidence_field( $raw_landmark, 'label', 'string', $claim_args );
			$compact_label = nl_proposal_normalize_evidence_field(
				$raw_landmark,
				'compact_label',
				'string',
				array_merge(
					$claim_args,
					array(
						'string_max_length' => nl_proposal_beam_compact_label_max_code_points(),
						'string_field'      => 'beam_scene.landmark.compact_label.value',
					)
				)
			);
			if ( is_wp_error( $compact_label ) ) {
				return nl_proposal_neutral_commercial_beam_scene(
					$anchor,
					$caveat,
					array( 'invalid_landmark_compact_label:' . $landmark_id )
				);
			}
			$coordinates = nl_proposal_normalize_evidence_field( $raw_landmark, 'coordinates', 'coordinate', $claim_args );
			$distance = nl_proposal_normalize_evidence_field(
				$raw_landmark,
				'distance_m',
				'decimal',
				array_merge( $claim_args, array( 'min' => 0, 'max' => 100000, 'unit_allowed' => array( 'metres_ground' ) ) )
			);
			$method = nl_proposal_normalize_evidence_field(
				$raw_landmark,
				'distance_method',
				'string',
				array_merge( $claim_args, array( 'allowed' => nl_proposal_beam_distance_methods() ) )
			);
			$bearing = nl_proposal_normalize_evidence_field(
				$raw_landmark,
				'bearing_deg',
				'decimal',
				array_merge( $claim_args, array( 'min' => 0, 'max' => 359.999999, 'unit_allowed' => array( 'degrees_true_north' ) ) )
			);
			foreach ( array( $label, $coordinates, $distance, $method, $bearing ) as $claim ) {
				if ( is_wp_error( $claim ) ) return $claim;
			}
			$landmark_caveat = '';
			if ( isset( $raw_landmark['caveat'] ) && '' !== $raw_landmark['caveat'] ) {
				$landmark_caveat = nl_proposal_sanitize_bounded_text( $raw_landmark['caveat'], 'beam_scene.landmark.caveat', 300, false );
				if ( is_wp_error( $landmark_caveat ) ) return $landmark_caveat;
			}
			$landmarks[] = array(
				'landmark_id'     => $landmark_id,
				'exposure_id'     => $landmark_exposure_id,
				'label'           => $label,
				'compact_label'   => $compact_label,
				'coordinates'     => $coordinates,
				'distance_m'      => $distance,
				'distance_method' => $method,
				'bearing_deg'     => $bearing,
				'caveat'         => $landmark_caveat,
			);
		}
		$associations[] = array( 'exposure_id' => $exposure_id, 'landmarks' => $landmarks );
	}

	$expected_ids = array_keys( $facade_by_id );
	$actual_ids   = array_keys( $association_ids );
	sort( $expected_ids );
	sort( $actual_ids );
	$issues = array();
	if ( $expected_ids !== $actual_ids ) $issues[] = 'incomplete_exposure_association';
	if ( ! nl_proposal_beam_claim_allowed( $anchor ) ) $issues[] = 'project_anchor_not_current';
	$anchor_value = nl_proposal_beam_claim_allowed( $anchor ) ? $anchor['value'] : null;
	foreach ( $associations as $association ) {
		$facade = $facade_by_id[ $association['exposure_id'] ];
		foreach ( array( 'direction', 'azimuth_start_deg', 'azimuth_end_deg', 'facade_share_pct' ) as $field ) {
			if ( ! nl_proposal_beam_claim_allowed( $facade[ $field ] ) ) $issues[] = 'incomplete_facade_geometry:' . $association['exposure_id'];
		}
		if ( ! empty( $issues ) && null === $anchor_value ) continue;
		$start = isset( $facade['azimuth_start_deg']['value'] ) ? $facade['azimuth_start_deg']['value'] : null;
		$end   = isset( $facade['azimuth_end_deg']['value'] ) ? $facade['azimuth_end_deg']['value'] : null;
		foreach ( $association['landmarks'] as $landmark ) {
			foreach ( array( 'label', 'compact_label', 'coordinates', 'distance_m', 'distance_method', 'bearing_deg' ) as $field ) {
				if ( ! nl_proposal_beam_claim_allowed( $landmark[ $field ] ) ) $issues[] = 'incomplete_landmark_claim:' . $landmark['landmark_id'];
			}
			if ( null === $anchor_value || null === $start || null === $end || ! nl_proposal_beam_claim_allowed( $landmark['coordinates'] ) || ! nl_proposal_beam_claim_allowed( $landmark['bearing_deg'] ) || ! nl_proposal_beam_claim_allowed( $landmark['distance_m'] ) || ! nl_proposal_beam_claim_allowed( $landmark['distance_method'] ) ) continue;
			$metrics = nl_proposal_beam_geodesic_metrics( $anchor_value, $landmark['coordinates']['value'] );
			$reported_bearing = (float) $landmark['bearing_deg']['value'];
			$bearing_delta = abs( $reported_bearing - $metrics['bearing_deg'] );
			$bearing_delta = min( $bearing_delta, 360 - $bearing_delta );
			if ( $bearing_delta > 8 ) $issues[] = 'landmark_coordinate_bearing_mismatch:' . $landmark['landmark_id'];
			if ( ! nl_proposal_beam_bearing_in_sector( $reported_bearing, $start, $end ) ) $issues[] = 'landmark_outside_exposure_sector:' . $landmark['landmark_id'];
			$reported_distance = (float) $landmark['distance_m']['value'];
			$method_value = (string) $landmark['distance_method']['value'];
			if ( 'straight_line_geodesic' === $method_value ) {
				if ( abs( $reported_distance - $metrics['distance_m'] ) > max( 30, $metrics['distance_m'] * 0.15 ) ) $issues[] = 'landmark_geodesic_distance_mismatch:' . $landmark['landmark_id'];
			} elseif ( $reported_distance + 1 < $metrics['distance_m'] * 0.95 ) {
				$issues[] = 'routed_distance_shorter_than_geodesic:' . $landmark['landmark_id'];
			}
		}
	}
	if ( ! empty( $issues ) ) {
		return nl_proposal_neutral_commercial_beam_scene( $anchor, $caveat, $issues );
	}
	return array(
		'scene_state'         => 'ready',
		'projection'          => 'north_up_local_equirectangular_v1',
		'project_anchor'      => $anchor,
		'exposures'           => $associations,
		'illustrative_caveat' => $caveat,
		'issues'              => array(),
	);
}

/**
 * Normalize a commercial floor.
 *
 * A floor is selectable only when the legal identity and elevator label are
 * verified. selectable input is ignored; it is always computed.
 *
 * @param mixed $raw Raw floor.
 * @param array $args Optional now timestamp.
 * @return array|WP_Error
 */
function nl_proposal_normalize_commercial_floor( $raw, $args = array() ) {
	$args = wp_parse_args(
		$args,
		array(
			'now'              => time(),
			'tower_by_key'     => array(),
			'project_url'      => '',
			'project_contract_id' => '',
		)
	);
	if ( ! is_array( $raw ) ) {
		return new WP_Error( 'nl_proposal_invalid_floor', 'Each floor must be an object.' );
	}

	$floor_id = nl_proposal_sanitize_contract_id(
		isset( $raw['floor_id'] ) ? $raw['floor_id'] : '',
		'floor.floor_id'
	);
	if ( is_wp_error( $floor_id ) ) {
		return $floor_id;
	}
	$building_id = nl_proposal_sanitize_contract_id(
		isset( $raw['building_id'] ) ? $raw['building_id'] : '',
		'floor.building_id'
	);
	$tower_id = nl_proposal_sanitize_contract_id(
		isset( $raw['tower_id'] ) ? $raw['tower_id'] : '',
		'floor.tower_id'
	);
	if ( is_wp_error( $building_id ) ) return $building_id;
	if ( is_wp_error( $tower_id ) ) return $tower_id;
	$tower_key = nl_proposal_commercial_identity_key( $building_id, $tower_id );
	if ( ! isset( $args['tower_by_key'][ $tower_key ] ) ) {
		return new WP_Error( 'nl_proposal_unknown_floor_tower', 'Floor building_id/tower_id is absent from the project tower crosswalk.' );
	}
	$tower_display_label = $args['tower_by_key'][ $tower_key ]['display_label'];

	$identity_args = array(
		'now'                           => $args['now'],
		'max_verified_lifetime_seconds' => 365 * DAY_IN_SECONDS,
		'required_document_ids'         => array( 'floor_id_crosswalk' ),
	);

	$legal_label = nl_proposal_normalize_evidence_field( $raw, 'legal_floor_label', 'string', $identity_args );
	if ( is_wp_error( $legal_label ) ) {
		return $legal_label;
	}
	$elevator_label = nl_proposal_normalize_evidence_field( $raw, 'elevator_label', 'string', $identity_args );
	if ( is_wp_error( $elevator_label ) ) {
		return $elevator_label;
	}
	$marketing_label = nl_proposal_normalize_evidence_field( $raw, 'marketing_label', 'string', $identity_args );
	if ( is_wp_error( $marketing_label ) ) {
		return $marketing_label;
	}

	$zone = nl_proposal_normalize_evidence_field(
		$raw,
		'zone',
		'string',
		array(
			'now'                           => $args['now'],
			'max_verified_lifetime_seconds' => 365 * DAY_IN_SECONDS,
			'required_document_ids'         => array( 'floor_id_crosswalk' ),
		)
	);
	if ( is_wp_error( $zone ) ) {
		return $zone;
	}

	$availability = nl_proposal_normalize_commercial_availability(
		isset( $raw['availability'] ) ? $raw['availability'] : null,
		$args
	);
	if ( is_wp_error( $availability ) ) {
		return $availability;
	}

	$gross = nl_proposal_normalize_evidence_field(
		$raw,
		'gross_rentable_sqm',
		'decimal',
		array(
			'now'          => $args['now'],
			'min'          => 0,
			'max'          => 1000000,
			'unit_allowed' => array( 'sqm_rentable_gross' ),
			'required_document_ids' => array( 'measurement_report' ),
		)
	);
	if ( is_wp_error( $gross ) ) {
		return $gross;
	}

	$usable = nl_proposal_normalize_evidence_field(
		$raw,
		'usable_sqm',
		'decimal',
		array(
			'now'          => $args['now'],
			'min'          => 0,
			'max'          => 1000000,
			'unit_allowed' => array( 'sqm_usable' ),
			'required_document_ids' => array( 'measurement_report' ),
		)
	);
	if ( is_wp_error( $usable ) ) {
		return $usable;
	}

	$clear_height = nl_proposal_normalize_evidence_field(
		$raw,
		'clear_height_m',
		'decimal',
		array(
			'now'          => $args['now'],
			'min'          => 0,
			'max'          => 20,
			'unit_allowed' => array( 'metres_clear_finished' ),
			'required_document_ids' => array( 'tenant_technical_manual' ),
		)
	);
	if ( is_wp_error( $clear_height ) ) {
		return $clear_height;
	}

	$floor_load = nl_proposal_normalize_evidence_field(
		$raw,
		'floor_load_kg_m2',
		'decimal',
		array(
			'now'          => $args['now'],
			'min'          => 0,
			'max'          => 100000,
			'unit_allowed' => array( 'kg_per_sqm_live_load' ),
			'required_document_ids' => array( 'structural_load_schedule' ),
		)
	);
	if ( is_wp_error( $floor_load ) ) {
		return $floor_load;
	}

	$power = nl_proposal_normalize_evidence_field(
		$raw,
		'tenant_power_va_m2',
		'decimal',
		array(
			'now'          => $args['now'],
			'min'          => 0,
			'max'          => 100000,
			'unit_allowed' => array( 'va_per_rentable_sqm' ),
			'required_document_ids' => array( 'power_single_line' ),
		)
	);
	if ( is_wp_error( $power ) ) {
		return $power;
	}

	$exposures = nl_proposal_normalize_commercial_exposures(
		isset( $raw['exposures'] ) ? $raw['exposures'] : array(),
		$args
	);
	if ( is_wp_error( $exposures ) ) {
		return $exposures;
	}
	$beam_scene = nl_proposal_normalize_commercial_beam_scene(
		isset( $raw['beam_scene'] ) ? $raw['beam_scene'] : null,
		array_merge( $args, array( 'facade_exposures' => $exposures ) )
	);
	if ( is_wp_error( $beam_scene ) ) {
		return $beam_scene;
	}

	$suites    = array();
	$suite_ids = array();
	$raw_suites = isset( $raw['suites'] ) ? $raw['suites'] : array();
	if ( ! is_array( $raw_suites ) ) {
		return new WP_Error( 'nl_proposal_invalid_suites', 'floor.suites must be a list.' );
	}
	foreach ( $raw_suites as $suite ) {
		$suite = nl_proposal_normalize_commercial_suite(
			$suite,
			$floor_id,
			array_merge(
				$args,
				array(
					'building_id'         => $building_id,
					'tower_id'            => $tower_id,
					'tower_display_label' => $tower_display_label,
					'project_contract_id' => $args['project_contract_id'],
				)
			)
		);
		if ( is_wp_error( $suite ) ) {
			return $suite;
		}
		if ( isset( $suite_ids[ $suite['suite_id'] ] ) ) {
			return new WP_Error( 'nl_proposal_duplicate_suite', 'Suite IDs must be unique within a floor.' );
		}
		$suite_ids[ $suite['suite_id'] ] = true;
		$suites[]                        = $suite;
	}

	$selectable = (
		'verified' === $legal_label['state']
		&& 'verified' === $elevator_label['state']
	);

	return array(
		'floor_id'            => $floor_id,
		'building_id'         => $building_id,
		'tower_id'            => $tower_id,
		'tower_display_label' => $tower_display_label,
		'identity_key'        => nl_proposal_commercial_identity_key( $building_id, $tower_id, $floor_id ),
		'url'                 => nl_proposal_commercial_identity_url( $args['project_url'], $args['project_contract_id'], $building_id, $tower_id, $floor_id ),
		'legal_floor_label'   => $legal_label,
		'elevator_label'      => $elevator_label,
		'marketing_label'     => $marketing_label,
		'zone'                => $zone,
		'selectable'          => $selectable,
		'availability'        => $availability,
		'gross_rentable_sqm'  => $gross,
		'usable_sqm'          => $usable,
		'clear_height_m'      => $clear_height,
		'floor_load_kg_m2'    => $floor_load,
		'tenant_power_va_m2'  => $power,
		'exposures'           => $exposures,
		'beam_scene'          => $beam_scene,
		'suites'              => $suites,
	);
}

/**
 * Return allowed project-fact keys and their value types.
 *
 * @return array
 */
function nl_proposal_commercial_project_fact_types() {
	$types = array(
		'floor_count_total'        => 'integer',
		'office_floor_count'       => 'integer',
		'project_area_sqm'         => 'decimal',
		'office_area_sqm'          => 'decimal',
		'marketable_area_sqm'      => 'decimal',
		'completion_date'          => 'date',
		'occupancy_date'           => 'date',
		'form_4_status'            => 'string',
		'ownership_entity'         => 'string',
		'lease_signing_entity'     => 'string',
		'measurement_standard'     => 'string',
		'certifications'           => 'string_list',
		'parking_stall_count'      => 'integer',
		'passenger_elevator_count' => 'integer',
		'freight_elevator_count'   => 'integer',
	);

	/**
	 * Proposal extension point. Production should freeze and test the resulting
	 * vocabulary; never accept arbitrary fact keys directly from an editor.
	 */
	return apply_filters( 'nl_proposal_commercial_project_fact_types', $types );
}

/**
 * Map project facts to document IDs accepted by the commercial RFP endpoint.
 *
 * @return array
 */
function nl_proposal_commercial_project_fact_document_ids() {
	$map = array(
		'floor_count_total'        => array( 'floor_id_crosswalk' ),
		'office_floor_count'       => array( 'floor_id_crosswalk' ),
		'project_area_sqm'         => array( 'measurement_report' ),
		'office_area_sqm'          => array( 'measurement_report' ),
		'marketable_area_sqm'      => array( 'measurement_report' ),
		'completion_date'          => array( 'handover_schedule', 'commissioning_summary' ),
		'occupancy_date'           => array( 'form_4', 'handover_schedule' ),
		'form_4_status'            => array( 'form_4' ),
		'ownership_entity'         => array( 'lease_draft' ),
		'lease_signing_entity'     => array( 'lease_draft' ),
		'measurement_standard'     => array( 'measurement_report' ),
		'certifications'           => array( 'esg_certificate' ),
		'parking_stall_count'      => array( 'parking_schedule' ),
		'passenger_elevator_count' => array( 'elevator_schedule' ),
		'freight_elevator_count'   => array( 'elevator_schedule' ),
	);

	return apply_filters( 'nl_proposal_commercial_project_fact_document_ids', $map );
}

/**
 * Normalize the complete commercial project contract.
 *
 * @param mixed $raw Raw project data.
 * @param array $args Optional now timestamp.
 * @return array|WP_Error
 */
function nl_proposal_normalize_commercial_project( $raw, $args = array() ) {
	$args = wp_parse_args( $args, array( 'now' => time() ) );
	if ( ! is_array( $raw ) ) {
		return new WP_Error( 'nl_proposal_invalid_project', 'Project contract must be an object.' );
	}

	$project_id = nl_proposal_sanitize_contract_id(
		isset( $raw['project_id'] ) ? $raw['project_id'] : '',
		'project.project_id'
	);
	if ( is_wp_error( $project_id ) ) {
		return $project_id;
	}

	$wp_post_id = isset( $raw['wp_post_id'] ) ? absint( $raw['wp_post_id'] ) : 0;
	if ( $wp_post_id < 1 ) {
		return new WP_Error( 'nl_proposal_invalid_post_id', 'wp_post_id must be a positive integer.' );
	}
	$project_url = nl_proposal_normalize_public_url(
		isset( $raw['project_url'] ) ? $raw['project_url'] : null,
		'project.project_url',
		false
	);
	if ( is_wp_error( $project_url ) ) {
		return $project_url;
	}
	$project_scheme = strtolower( (string) wp_parse_url( $project_url, PHP_URL_SCHEME ) );
	$project_query  = (string) wp_parse_url( $project_url, PHP_URL_QUERY );
	$project_fragment = wp_parse_url( $project_url, PHP_URL_FRAGMENT );
	$project_user   = wp_parse_url( $project_url, PHP_URL_USER );
	$project_pass   = wp_parse_url( $project_url, PHP_URL_PASS );
	$reserved_query = array();
	if ( '' !== $project_query ) {
		parse_str( $project_query, $reserved_query );
	}
	if (
		'https' !== $project_scheme ||
		( null !== $project_user && false !== $project_user && '' !== $project_user ) ||
		( null !== $project_pass && false !== $project_pass && '' !== $project_pass ) ||
		( null !== $project_fragment && false !== $project_fragment && '' !== $project_fragment ) ||
		array_intersect(
			array_keys( is_array( $reserved_query ) ? $reserved_query : array() ),
			array( 'wp_post_id', 'project_id', 'project_contract_id', 'building_id', 'tower_id', 'floor_id', 'suite_id' )
		)
	) {
		return new WP_Error( 'nl_proposal_invalid_project_url', 'project.project_url must be HTTPS, fragment-free, and must not contain routing or asset identity parameters.' );
	}
	$home_url = function_exists( 'home_url' ) ? home_url( '/' ) : '';
	$permalink = function_exists( 'get_permalink' ) ? get_permalink( $wp_post_id ) : false;
	$canonical_permalink = nl_proposal_normalize_public_url(
		is_string( $permalink ) ? $permalink : null,
		'project.canonical_permalink',
		false
	);
	$home_parts      = nl_proposal_url_contract_parts( (string) $home_url );
	$project_parts   = nl_proposal_url_contract_parts( $project_url );
	$permalink_parts = is_wp_error( $canonical_permalink )
		? null
		: nl_proposal_url_contract_parts( $canonical_permalink );
	if (
		! is_array( $home_parts )
		|| ! is_array( $project_parts )
		|| ! is_array( $permalink_parts )
		|| 'https' !== $home_parts['scheme']
		|| 'https' !== $permalink_parts['scheme']
		|| '' !== $permalink_parts['fragment']
		|| ! nl_proposal_url_contract_same_origin( $project_parts, $home_parts )
		|| ! nl_proposal_url_contract_same_origin( $permalink_parts, $home_parts )
		|| $project_parts['path'] !== $permalink_parts['path']
		|| $project_parts['query'] !== $permalink_parts['query']
	) {
		return new WP_Error( 'nl_proposal_invalid_project_url', 'project.project_url must match the canonical same-site WordPress permalink and origin.' );
	}
	$towers = nl_proposal_normalize_commercial_towers(
		isset( $raw['towers'] ) ? $raw['towers'] : null,
		$args
	);
	if ( is_wp_error( $towers ) ) {
		return $towers;
	}
	$tower_by_key = array();
	foreach ( $towers as $tower ) {
		$tower_by_key[ $tower['identity_key'] ] = $tower;
	}

	if ( isset( $raw['asset_type'] ) && ! is_scalar( $raw['asset_type'] ) ) {
		return new WP_Error( 'nl_proposal_invalid_asset_type', 'asset_type is unsupported.' );
	}
	$asset_type = isset( $raw['asset_type'] ) ? sanitize_key( $raw['asset_type'] ) : '';
	if ( ! in_array( $asset_type, nl_proposal_asset_types(), true ) ) {
		return new WP_Error( 'nl_proposal_invalid_asset_type', 'asset_type is unsupported.' );
	}
	if ( isset( $raw['product_family'] ) && ! is_scalar( $raw['product_family'] ) ) {
		return new WP_Error( 'nl_proposal_invalid_product_family', 'product_family is unsupported.' );
	}
	$product_family = isset( $raw['product_family'] ) ? sanitize_key( $raw['product_family'] ) : 'commercial';
	if ( ! in_array( $product_family, nl_proposal_product_families(), true ) ) {
		return new WP_Error( 'nl_proposal_invalid_product_family', 'product_family is unsupported.' );
	}

	$applicability_tags = array();
	$raw_tags            = isset( $raw['applicability_tags'] ) ? $raw['applicability_tags'] : array();
	if ( ! is_array( $raw_tags ) ) {
		return new WP_Error( 'nl_proposal_invalid_applicability_tags', 'applicability_tags must be a list.' );
	}
	foreach ( $raw_tags as $tag ) {
		if ( ! is_scalar( $tag ) ) {
			return new WP_Error( 'nl_proposal_invalid_applicability_tag', 'An applicability tag is unsupported.' );
		}
		$tag = sanitize_key( $tag );
		if ( ! in_array( $tag, nl_proposal_applicability_tags(), true ) ) {
			return new WP_Error( 'nl_proposal_invalid_applicability_tag', 'An applicability tag is unsupported.' );
		}
		$applicability_tags[] = $tag;
	}
	$applicability_tags = array_values( array_unique( $applicability_tags ) );

	$title = nl_proposal_sanitize_bounded_text(
		isset( $raw['title'] ) ? $raw['title'] : '',
		'project.title',
		240
	);
	if ( is_wp_error( $title ) ) {
		return $title;
	}

	$generated_at = nl_proposal_normalize_rfc3339(
		isset( $raw['generated_at'] ) ? $raw['generated_at'] : null,
		'project.generated_at',
		false
	);
	if ( is_wp_error( $generated_at ) ) {
		return $generated_at;
	}

	$fact_types     = nl_proposal_commercial_project_fact_types();
	$fact_documents = nl_proposal_commercial_project_fact_document_ids();
	$raw_facts      = isset( $raw['project_facts'] ) ? $raw['project_facts'] : array();
	if ( ! is_array( $raw_facts ) ) {
		return new WP_Error( 'nl_proposal_invalid_project_facts', 'project_facts must be an object.' );
	}

	$facts = array();
	foreach ( $raw_facts as $fact_key => $evidence ) {
		$fact_key = sanitize_key( $fact_key );
		if ( ! isset( $fact_types[ $fact_key ] ) ) {
			return new WP_Error( 'nl_proposal_unsupported_project_fact', sprintf( 'Unsupported project fact: %s.', $fact_key ) );
		}
		$fact = nl_proposal_normalize_evidence_envelope(
			$evidence,
			$fact_types[ $fact_key ],
			array(
				'now'                   => $args['now'],
				'min'                   => in_array( $fact_types[ $fact_key ], array( 'integer', 'decimal' ), true ) ? 0 : null,
				'required_document_ids' => isset( $fact_documents[ $fact_key ] )
					? $fact_documents[ $fact_key ]
					: array(),
			)
		);
		if ( is_wp_error( $fact ) ) {
			$fact->add_data( array( 'fact_key' => $fact_key ) );
			return $fact;
		}
		$facts[ $fact_key ] = $fact;
	}

	$inventory = nl_proposal_normalize_evidence_envelope(
		isset( $raw['floor_inventory'] ) ? $raw['floor_inventory'] : null,
		'string',
		array(
			'now'                           => $args['now'],
			'max_verified_lifetime_seconds' => DAY_IN_SECONDS,
			'required_document_ids'         => array( 'availability_schedule', 'floor_id_crosswalk' ),
			'unknown_reason'                => 'No current, signed floor inventory was supplied.',
		)
	);
	if ( is_wp_error( $inventory ) ) {
		return $inventory;
	}

	$floors     = array();
	$floor_ids  = array();
	$raw_floors = isset( $raw['floors'] ) ? $raw['floors'] : array();
	if ( ! is_array( $raw_floors ) ) {
		return new WP_Error( 'nl_proposal_invalid_floors', 'floors must be a list.' );
	}
	foreach ( $raw_floors as $floor ) {
		$floor = nl_proposal_normalize_commercial_floor(
			$floor,
			array_merge(
				$args,
				array(
					'tower_by_key'       => $tower_by_key,
					'project_url'        => $project_url,
					'project_contract_id'=> $project_id,
				)
			)
		);
		if ( is_wp_error( $floor ) ) {
			return $floor;
		}
		if ( ! in_array( $asset_type, nl_proposal_implemented_asset_types(), true ) ) {
			$floor['selectable'] = false;
			foreach ( $floor['suites'] as $suite_index => $suite ) {
				$floor['suites'][ $suite_index ]['selectable'] = false;
			}
		}
		if ( isset( $floor_ids[ $floor['identity_key'] ] ) ) {
			return new WP_Error( 'nl_proposal_duplicate_floor', 'Building/tower/floor identities must be unique within a project.' );
		}
		$floor_ids[ $floor['identity_key'] ] = true;
		$floors[]                        = $floor;
	}

	$publication_blockers = array();
	$raw_blockers         = isset( $raw['publication_blockers'] ) ? $raw['publication_blockers'] : array();
	if ( ! is_array( $raw_blockers ) ) {
		return new WP_Error( 'nl_proposal_invalid_blockers', 'publication_blockers must be a list.' );
	}
	foreach ( $raw_blockers as $blocker ) {
		$blocker = nl_proposal_sanitize_bounded_text( $blocker, 'publication_blockers[]', 500 );
		if ( is_wp_error( $blocker ) ) {
			return $blocker;
		}
		$publication_blockers[] = $blocker;
	}

	$publishable_floor_count = 0;
	foreach ( $floors as $floor ) {
		if ( $floor['selectable'] ) {
			$publishable_floor_count++;
		}
	}

	$publication_allowed = (
		in_array( $asset_type, nl_proposal_implemented_asset_types(), true )
		&&
		'verified' === $inventory['state']
		&& $publishable_floor_count > 0
		&& empty( $publication_blockers )
	);

	return array(
		'schema_version'          => NL_PROPOSAL_COMMERCIAL_SCHEMA_VERSION,
		'vocabularies'            => nl_proposal_commercial_contract_vocabularies(),
		'project_id'              => $project_id,
		'wp_post_id'              => $wp_post_id,
		'project_url'             => $project_url,
		'towers'                  => $towers,
		'asset_type'              => $asset_type,
		'product_family'           => $product_family,
		'applicability_tags'       => $applicability_tags,
		'ui_adapter_supported'     => in_array( $asset_type, nl_proposal_implemented_asset_types(), true ),
		'title'                    => $title,
		'generated_at'             => $generated_at,
		'project_facts'            => $facts,
		'floor_inventory'          => $inventory,
		'floors'                   => $floors,
		'publication_blockers'     => array_values( array_unique( $publication_blockers ) ),
		'publication_allowed'      => $publication_allowed,
		'selectable_floor_count'   => $publishable_floor_count,
	);
}

/**
 * Report whether an evidence envelope can support a current transactional
 * claim. This never treats source estimates as verified facts.
 *
 * @param mixed $evidence Normalized evidence.
 * @param int|null $now Current epoch.
 * @return bool
 */
function nl_proposal_is_current_decision_grade_evidence( $evidence, $now = null ) {
	$now = null === $now ? time() : (int) $now;

	if ( ! is_array( $evidence ) || 'verified' !== ( isset( $evidence['state'] ) ? $evidence['state'] : null ) ) {
		return false;
	}
	if ( ! array_key_exists( 'value', $evidence ) || null === $evidence['value'] ) {
		return false;
	}
	if ( empty( $evidence['sources'] ) || empty( $evidence['owner'] ) || empty( $evidence['verified_at'] ) || empty( $evidence['expires_at'] ) ) {
		return false;
	}

	$expires = nl_proposal_timestamp_to_epoch( $evidence['expires_at'] );
	return null !== $expires && $expires > $now;
}

/**
 * Example integration only; intentionally not hooked.
 *
 * A production adapter can call this after reading a revision-controlled JSON
 * document or an owner API. A WP_Error must block publishing and emit an
 * operational alert. It must never fall back to the legacy "available" default.
 *
 * Example:
 *
 * $contract = nl_proposal_normalize_commercial_project( $raw_contract );
 * if ( is_wp_error( $contract ) ) {
 *     do_action( 'nl_commercial_contract_rejected', $post_id, $contract );
 *     $showroom_payload['commercial_contract'] = null;
 *     $showroom_payload['commercial_state']    = 'unknown';
 *     return $showroom_payload;
 * }
 *
 * $showroom_payload['commercial_contract'] = $contract;
 * return $showroom_payload;
 */
