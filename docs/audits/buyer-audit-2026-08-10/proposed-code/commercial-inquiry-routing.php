<?php
/**
 * PROPOSAL ONLY — NOT APPLIED.
 *
 * Accountable commercial RFP route for classic WordPress.
 *
 * This reference endpoint is independent of project-claim or paid-tier state.
 * It accepts a request only when the project is commercial, the selected asset
 * is validated by the commercial inventory adapter, consent is current, and a
 * non-expired accountable project route or explicitly configured commercial
 * desk route exists.
 *
 * Target runtime: PHP 7.4+, WordPress 5.8+, HTTPS and OpenSSL.
 *
 * @package Nadlan_Proposal
 */

defined( 'ABSPATH' ) || exit;

if ( ! defined( 'NL_PROPOSAL_RFP_SCHEMA_VERSION' ) ) {
	define( 'NL_PROPOSAL_RFP_SCHEMA_VERSION', '1.0.0' );
}

if ( ! defined( 'NL_PROPOSAL_RFP_CONSENT_VERSION' ) ) {
	define( 'NL_PROPOSAL_RFP_CONSENT_VERSION', 'commercial-rfp-2026-08-10-v1' );
}

/**
 * Return the supported one-click commercial question IDs.
 *
 * @return string[]
 */
function nl_proposal_commercial_question_ids() {
	$ids = array(
		'live_availability',
		'floor_identity',
		'asking_rent',
		'service_charge',
		'arnona',
		'parking_price_and_ratio',
		'net_to_gross',
		'usable_area',
		'divisibility',
		'contiguous_floors',
		'handover_date',
		'fit_out_access',
		'fit_out_allowance',
		'lease_term_and_breaks',
		'indexation',
		'deposit_and_guarantees',
		'clear_height',
		'floor_load',
		'power_capacity',
		'generator_and_ups',
		'hvac_capacity_and_hours',
		'after_hours_hvac',
		'fiber_carriers_and_diversity',
		'elevator_bank_and_wait_time',
		'loading_and_deliveries',
		'security_and_access',
		'accessibility_route',
		'fire_and_life_safety',
		'protected_space',
		'certifications',
		'commute_and_transport',
		'nearby_facilities',
		'building_operations',
	);

	return apply_filters( 'nl_proposal_commercial_question_ids', $ids );
}

/**
 * Return supported one-click document request IDs.
 *
 * @return string[]
 */
function nl_proposal_commercial_document_ids() {
	$ids = array(
		'availability_schedule',
		'floor_id_crosswalk',
		'landlord_offer',
		'floor_plan_pdf',
		'cad_dwg',
		'bim_extract',
		'measurement_report',
		'validated_test_fit',
		'tenant_technical_manual',
		'structural_load_schedule',
		'power_single_line',
		'hvac_specification',
		'fiber_carrier_letters',
		'elevator_schedule',
		'fire_life_safety_report',
		'accessibility_report',
		'parking_schedule',
		'building_rules',
		'service_charge_budget',
		'arnona_assessment',
		'handover_schedule',
		'fit_out_guide',
		'lease_draft',
		'insurance_requirements',
		'esg_certificate',
		'form_4',
		'commissioning_summary',
		'view_study',
		'orientation_plan',
	);

	return apply_filters( 'nl_proposal_commercial_document_ids', $ids );
}

/**
 * Create a REST-safe error.
 *
 * @param string $code Stable code.
 * @param string $message Safe client message.
 * @param int    $status HTTP status.
 * @param array  $safe_data Optional non-PII recovery metadata. Status cannot be overridden.
 * @return WP_Error
 */
function nl_proposal_rfp_error( $code, $message, $status, $safe_data = array() ) {
	$data = is_array( $safe_data ) ? $safe_data : array();
	unset( $data['status'] );
	$data['status'] = (int) $status;

	return new WP_Error(
		$code,
		$message,
		$data
	);
}

/**
 * Create a deterministic, user-correctable field error without echoing input.
 *
 * The field path is a closed server-owned identifier. It allows the client to
 * move the buyer to the right step and focus the right control; it never
 * contains the submitted value or any other PII.
 *
 * @param string $field Canonical request field path.
 * @param string $message Safe client message.
 * @param int    $status HTTP status.
 * @return WP_Error
 */
function nl_proposal_rfp_field_error( $field, $message, $status = 422 ) {
	return nl_proposal_rfp_error(
		'invalid_field',
		$message,
		$status,
		array( 'field' => (string) $field )
	);
}

/**
 * Resolve the active consent-copy version through one narrowly scoped seam.
 *
 * The constant is the release default. The filter exists so an accountable
 * consent-copy deployment can rotate the version without editing request code.
 * Invalid filter output fails closed: no submitted version can equal an empty
 * server version.
 *
 * @return string
 */
function nl_proposal_current_commercial_rfp_consent_version() {
	$value = apply_filters(
		'nl_proposal_commercial_rfp_consent_version',
		NL_PROPOSAL_RFP_CONSENT_VERSION
	);
	if ( ! is_string( $value ) || ! preg_match( '/^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/', $value ) ) {
		return '';
	}

	return $value;
}

/**
 * Return a recoverable consent-version error with no buyer data.
 *
 * @return WP_Error
 */
function nl_proposal_rfp_consent_version_error() {
	$current_version = nl_proposal_current_commercial_rfp_consent_version();
	return nl_proposal_rfp_error(
		'consent_version_expired',
		'Please review the current consent text and submit again.',
		409,
		array(
			'field'                   => 'consent.privacy',
			'current_consent_version' => $current_version,
		)
	);
}

/**
 * Return true when an array is a zero-based list.
 *
 * @param mixed $value Value.
 * @return bool
 */
function nl_proposal_rfp_is_list( $value ) {
	if ( ! is_array( $value ) ) {
		return false;
	}

	return array_keys( $value ) === range( 0, count( $value ) - 1 ) || array() === $value;
}

/**
 * Reject undeclared keys rather than accepting shadow fields.
 *
 * @param mixed    $value Object to inspect.
 * @param string[] $allowed Allowed keys.
 * @param string   $path Error path.
 * @return true|WP_Error
 */
function nl_proposal_rfp_reject_unknown_keys( $value, $allowed, $path ) {
	// json_decode() represents both {} and [] as an empty PHP array. Permit the
	// empty object case; a non-empty numeric list is still rejected.
	if ( ! is_array( $value ) || ( ! empty( $value ) && nl_proposal_rfp_is_list( $value ) ) ) {
		return nl_proposal_rfp_error( 'invalid_request', sprintf( '%s must be an object.', $path ), 400 );
	}

	foreach ( array_keys( $value ) as $key ) {
		if ( ! is_string( $key ) || ! in_array( $key, $allowed, true ) ) {
			return nl_proposal_rfp_error( 'invalid_request', sprintf( '%s contains an unsupported field.', $path ), 400 );
		}
	}

	return true;
}

/**
 * Sanitize bounded single-line input without truncation.
 *
 * @param mixed  $value Raw value.
 * @param string $field Field.
 * @param int    $max Maximum Unicode length.
 * @param bool   $required Whether required.
 * @return string|WP_Error
 */
function nl_proposal_rfp_text( $value, $field, $max, $required = false ) {
	if ( null === $value || '' === $value ) {
		return $required
			? nl_proposal_rfp_field_error( $field, sprintf( '%s is required.', $field ) )
			: '';
	}
	if ( ! is_scalar( $value ) ) {
		return nl_proposal_rfp_field_error( $field, sprintf( '%s must be text.', $field ) );
	}

	$value  = sanitize_text_field( (string) $value );
	$length = function_exists( 'mb_strlen' ) ? mb_strlen( $value, 'UTF-8' ) : strlen( $value );

	if ( $required && '' === $value ) {
		return nl_proposal_rfp_field_error( $field, sprintf( '%s is required.', $field ) );
	}
	if ( $length > $max ) {
		return nl_proposal_rfp_field_error( $field, sprintf( '%s is too long.', $field ) );
	}

	return $value;
}

/**
 * Sanitize bounded multi-line input.
 *
 * @param mixed  $value Raw value.
 * @param string $field Field.
 * @param int    $max Maximum Unicode length.
 * @return string|WP_Error
 */
function nl_proposal_rfp_textarea( $value, $field, $max ) {
	if ( null === $value || '' === $value ) {
		return '';
	}
	if ( ! is_scalar( $value ) ) {
		return nl_proposal_rfp_field_error( $field, sprintf( '%s must be text.', $field ) );
	}

	$value  = sanitize_textarea_field( (string) $value );
	$length = function_exists( 'mb_strlen' ) ? mb_strlen( $value, 'UTF-8' ) : strlen( $value );
	if ( $length > $max ) {
		return nl_proposal_rfp_field_error( $field, sprintf( '%s is too long.', $field ) );
	}

	return $value;
}

/**
 * Normalize a nullable contract identifier.
 *
 * @param mixed  $value Raw ID.
 * @param string $field Field.
 * @return string|null|WP_Error
 */
function nl_proposal_rfp_contract_id( $value, $field ) {
	if ( null === $value || '' === $value ) {
		return null;
	}
	if ( ! is_scalar( $value ) ) {
		return nl_proposal_rfp_field_error( $field, sprintf( '%s is invalid.', $field ) );
	}

	$value = strtolower( trim( (string) $value ) );
	if ( strlen( $value ) > 128 || ! preg_match( '/^[a-z0-9][a-z0-9._:-]*$/', $value ) ) {
		return nl_proposal_rfp_field_error( $field, sprintf( '%s is invalid.', $field ) );
	}

	return $value;
}

/**
 * Normalize an optional integer.
 *
 * @param mixed  $value Raw value.
 * @param string $field Field.
 * @param int    $min Minimum.
 * @param int    $max Maximum.
 * @return int|null|WP_Error
 */
function nl_proposal_rfp_integer( $value, $field, $min, $max ) {
	if ( null === $value || '' === $value ) {
		return null;
	}
	if ( is_bool( $value ) || ! is_numeric( $value ) || (float) $value !== (float) (int) $value ) {
		return nl_proposal_rfp_field_error( $field, sprintf( '%s must be an integer.', $field ) );
	}

	$value = (int) $value;
	if ( $value < $min || $value > $max ) {
		return nl_proposal_rfp_field_error( $field, sprintf( '%s is outside the accepted range.', $field ) );
	}

	return $value;
}

/**
 * Normalize an optional finite decimal.
 *
 * @param mixed  $value Raw value.
 * @param string $field Field.
 * @param float  $min Minimum.
 * @param float  $max Maximum.
 * @return float|null|WP_Error
 */
function nl_proposal_rfp_decimal( $value, $field, $min, $max ) {
	if ( null === $value || '' === $value ) {
		return null;
	}
	if ( is_bool( $value ) || ! is_numeric( $value ) ) {
		return nl_proposal_rfp_field_error( $field, sprintf( '%s must be numeric.', $field ) );
	}

	$value = (float) $value;
	if ( is_nan( $value ) || is_infinite( $value ) || $value < $min || $value > $max ) {
		return nl_proposal_rfp_field_error( $field, sprintf( '%s is outside the accepted range.', $field ) );
	}

	return $value;
}

/**
 * Normalize an ID list against a fixed allowlist.
 *
 * @param mixed    $value Raw list.
 * @param string[] $allowed Allowed IDs.
 * @param string   $field Field.
 * @param int      $max Maximum count.
 * @return string[]|WP_Error
 */
function nl_proposal_rfp_id_list( $value, $allowed, $field, $max ) {
	if ( null === $value ) {
		return array();
	}
	if ( ! nl_proposal_rfp_is_list( $value ) || count( $value ) > $max ) {
		return nl_proposal_rfp_field_error( $field, sprintf( '%s must be a bounded list.', $field ) );
	}

	$normalized = array();
	foreach ( $value as $id ) {
		$id = nl_proposal_rfp_contract_id( $id, $field . '[]' );
		if ( is_wp_error( $id ) ) {
			return $id;
		}
		if ( null === $id || ! in_array( $id, $allowed, true ) ) {
			return nl_proposal_rfp_field_error( $field, sprintf( '%s contains an unsupported ID.', $field ) );
		}
		$normalized[] = $id;
	}

	return array_values( array_unique( $normalized ) );
}

/**
 * Normalize a YYYY-MM target month.
 *
 * @param mixed $value Raw value.
 * @return string|null|WP_Error
 */
function nl_proposal_rfp_target_month( $value ) {
	if ( null === $value || '' === $value ) {
		return null;
	}
	if ( ! is_string( $value ) || ! preg_match( '/^\d{4}-(0[1-9]|1[0-2])$/', $value ) ) {
		return nl_proposal_rfp_field_error( 'requirements.target_move_in', 'requirements.target_move_in must use YYYY-MM.' );
	}
	return $value;
}

/**
 * Normalize a same-site page URL to its path only.
 *
 * Query strings and fragments are discarded to avoid capturing identifiers.
 *
 * @param mixed $value Raw URL.
 * @return string|null|WP_Error
 */
function nl_proposal_rfp_page_path( $value ) {
	if ( null === $value || '' === $value ) {
		return null;
	}
	if ( ! is_string( $value ) ) {
		return nl_proposal_rfp_error( 'invalid_request', 'page_url is invalid.', 400 );
	}

	$url    = esc_url_raw( $value, array( 'https' ) );
	$scheme = strtolower( (string) wp_parse_url( $url, PHP_URL_SCHEME ) );
	$host   = strtolower( (string) wp_parse_url( $url, PHP_URL_HOST ) );
	$port   = wp_parse_url( $url, PHP_URL_PORT );
	$user   = wp_parse_url( $url, PHP_URL_USER );
	$pass   = wp_parse_url( $url, PHP_URL_PASS );
	$path   = (string) wp_parse_url( $url, PHP_URL_PATH );
	$origin = $scheme . '://' . ( false !== strpos( $host, ':' ) ? '[' . trim( $host, '[]' ) . ']' : $host );
	if ( null !== $port && false !== $port ) {
		$origin .= ':' . (int) $port;
	}
	$request_origin = nl_proposal_normalize_http_origin( $origin, false );
	$site_origin    = nl_proposal_normalize_http_origin( home_url( '/' ), true );

	if (
		'' === $url
		|| '' === $host
		|| ( null !== $user && false !== $user && '' !== $user )
		|| ( null !== $pass && false !== $pass && '' !== $pass )
		|| '' === $request_origin
		|| '' === $site_origin
		|| ! hash_equals( $site_origin, $request_origin )
		|| '' === $path
	) {
		return nl_proposal_rfp_error( 'invalid_request', 'page_url must be an HTTPS page on this site.', 400 );
	}

	return '/' . ltrim( sanitize_text_field( $path ), '/' );
}

/**
 * Normalize the entire request payload.
 *
 * @param mixed $raw Raw JSON object.
 * @return array|WP_Error
 */
function nl_proposal_normalize_commercial_rfp_payload( $raw ) {
	$check = nl_proposal_rfp_reject_unknown_keys(
		$raw,
		array(
			'schema_version',
			'environment',
			'sandbox_post_id',
			'project_id',
			'project_contract_id',
			'asset',
			'locale',
			'company',
			'contact',
			'requirements',
			'question_ids',
			'document_ids',
			'question_text',
			'consent',
			'page_url',
			'website_confirm',
		),
		'request'
	);
	if ( is_wp_error( $check ) ) {
		return $check;
	}

	if ( ! empty( $raw['website_confirm'] ) ) {
		return nl_proposal_rfp_error( 'invalid_request', 'The request could not be accepted.', 400 );
	}

	if ( ! isset( $raw['schema_version'] ) || ! is_scalar( $raw['schema_version'] ) || NL_PROPOSAL_RFP_SCHEMA_VERSION !== (string) $raw['schema_version'] ) {
		return nl_proposal_rfp_error( 'unsupported_schema', 'The request schema is unsupported.', 400 );
	}
	$environment = isset( $raw['environment'] ) && is_scalar( $raw['environment'] )
		? sanitize_key( (string) $raw['environment'] )
		: '';
	if ( ! in_array( $environment, array( 'production', 'test' ), true ) ) {
		return nl_proposal_rfp_error( 'invalid_environment', 'The request environment is invalid.', 400 );
	}
	$sandbox_post_id = nl_proposal_rfp_integer(
		isset( $raw['sandbox_post_id'] ) ? $raw['sandbox_post_id'] : null,
		'sandbox_post_id',
		1,
		PHP_INT_MAX
	);
	if ( is_wp_error( $sandbox_post_id ) ) {
		return $sandbox_post_id;
	}
	if ( ( 'test' === $environment && null === $sandbox_post_id ) || ( 'production' === $environment && null !== $sandbox_post_id ) ) {
		return nl_proposal_rfp_error( 'invalid_environment', 'The request environment is invalid.', 400 );
	}

	$project_id = nl_proposal_rfp_integer(
		isset( $raw['project_id'] ) ? $raw['project_id'] : null,
		'project_id',
		1,
		PHP_INT_MAX
	);
	if ( is_wp_error( $project_id ) || null === $project_id ) {
		return is_wp_error( $project_id )
			? $project_id
			: nl_proposal_rfp_error( 'invalid_request', 'project_id is required.', 400 );
	}
	$project_contract_id = nl_proposal_rfp_contract_id(
		isset( $raw['project_contract_id'] ) ? $raw['project_contract_id'] : null,
		'project_contract_id'
	);
	if ( is_wp_error( $project_contract_id ) || null === $project_contract_id ) {
		return is_wp_error( $project_contract_id )
			? $project_contract_id
			: nl_proposal_rfp_error( 'invalid_request', 'project_contract_id is required.', 400 );
	}

	$asset_raw = isset( $raw['asset'] ) ? $raw['asset'] : array();
	$check     = nl_proposal_rfp_reject_unknown_keys( $asset_raw, array( 'building_id', 'tower_id', 'floor_id', 'suite_id' ), 'asset' );
	if ( is_wp_error( $check ) ) {
		return $check;
	}
	$building_id = nl_proposal_rfp_contract_id(
		isset( $asset_raw['building_id'] ) ? $asset_raw['building_id'] : null,
		'asset.building_id'
	);
	if ( is_wp_error( $building_id ) || null === $building_id ) {
		return is_wp_error( $building_id ) ? $building_id : nl_proposal_rfp_error( 'invalid_request', 'asset.building_id is required.', 400 );
	}
	$tower_id = nl_proposal_rfp_contract_id(
		isset( $asset_raw['tower_id'] ) ? $asset_raw['tower_id'] : null,
		'asset.tower_id'
	);
	if ( is_wp_error( $tower_id ) || null === $tower_id ) {
		return is_wp_error( $tower_id ) ? $tower_id : nl_proposal_rfp_error( 'invalid_request', 'asset.tower_id is required.', 400 );
	}
	$floor_id = nl_proposal_rfp_contract_id(
		isset( $asset_raw['floor_id'] ) ? $asset_raw['floor_id'] : null,
		'asset.floor_id'
	);
	if ( is_wp_error( $floor_id ) || null === $floor_id ) {
		return is_wp_error( $floor_id ) ? $floor_id : nl_proposal_rfp_error( 'invalid_request', 'asset.floor_id is required.', 400 );
	}
	$suite_id = nl_proposal_rfp_contract_id(
		isset( $asset_raw['suite_id'] ) ? $asset_raw['suite_id'] : null,
		'asset.suite_id'
	);
	if ( is_wp_error( $suite_id ) ) {
		return $suite_id;
	}

	if ( isset( $raw['locale'] ) && ! is_scalar( $raw['locale'] ) ) {
		return nl_proposal_rfp_error( 'invalid_request', 'locale is unsupported.', 400 );
	}
	$locale = isset( $raw['locale'] ) ? strtolower( sanitize_key( $raw['locale'] ) ) : 'en';
	if ( ! in_array( $locale, array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ) {
		return nl_proposal_rfp_error( 'invalid_request', 'locale is unsupported.', 400 );
	}

	$company_raw = isset( $raw['company'] ) ? $raw['company'] : array();
	$check       = nl_proposal_rfp_reject_unknown_keys(
		$company_raw,
		array( 'name', 'registration_country', 'website', 'size_band' ),
		'company'
	);
	if ( is_wp_error( $check ) ) {
		return $check;
	}
	$company_name = nl_proposal_rfp_text(
		isset( $company_raw['name'] ) ? $company_raw['name'] : null,
		'company.name',
		180,
		true
	);
	if ( is_wp_error( $company_name ) ) {
		return $company_name;
	}
	if ( isset( $company_raw['registration_country'] ) && ! is_scalar( $company_raw['registration_country'] ) ) {
		return nl_proposal_rfp_error( 'invalid_request', 'company.registration_country must be an ISO alpha-2 code.', 400 );
	}
	$country = isset( $company_raw['registration_country'] ) ? strtoupper( trim( (string) $company_raw['registration_country'] ) ) : '';
	if ( '' !== $country && ! preg_match( '/^[A-Z]{2}$/', $country ) ) {
		return nl_proposal_rfp_error( 'invalid_request', 'company.registration_country must be an ISO alpha-2 code.', 400 );
	}
	$company_website = '';
	if ( ! empty( $company_raw['website'] ) ) {
		if ( ! is_scalar( $company_raw['website'] ) ) {
			return nl_proposal_rfp_error( 'invalid_request', 'company.website must be a valid HTTPS URL.', 400 );
		}
		$company_website = esc_url_raw( (string) $company_raw['website'], array( 'https' ) );
		if ( '' === $company_website || '' === wp_parse_url( $company_website, PHP_URL_HOST ) ) {
			return nl_proposal_rfp_error( 'invalid_request', 'company.website must be a valid HTTPS URL.', 400 );
		}
	}
	if ( isset( $company_raw['size_band'] ) && ! is_scalar( $company_raw['size_band'] ) ) {
		return nl_proposal_rfp_error( 'invalid_request', 'company.size_band is unsupported.', 400 );
	}
	$size_band = isset( $company_raw['size_band'] ) ? (string) $company_raw['size_band'] : '';
	if ( '' !== $size_band && ! in_array( $size_band, array( '1-10', '11-50', '51-200', '201-500', '501-1000', '1001+' ), true ) ) {
		return nl_proposal_rfp_error( 'invalid_request', 'company.size_band is unsupported.', 400 );
	}

	$contact_raw = isset( $raw['contact'] ) ? $raw['contact'] : array();
	$check       = nl_proposal_rfp_reject_unknown_keys(
		$contact_raw,
		array( 'name', 'role', 'email', 'phone', 'preferred_channel' ),
		'contact'
	);
	if ( is_wp_error( $check ) ) {
		return $check;
	}
	$contact_name = nl_proposal_rfp_text(
		isset( $contact_raw['name'] ) ? $contact_raw['name'] : null,
		'contact.name',
		160,
		true
	);
	if ( is_wp_error( $contact_name ) ) {
		return $contact_name;
	}
	$role = nl_proposal_rfp_text(
		isset( $contact_raw['role'] ) ? $contact_raw['role'] : '',
		'contact.role',
		160,
		false
	);
	if ( is_wp_error( $role ) ) {
		return $role;
	}
	if ( isset( $contact_raw['email'] ) && ! is_scalar( $contact_raw['email'] ) ) {
		return nl_proposal_rfp_field_error( 'contact.email', 'contact.email is invalid.' );
	}
	$email = isset( $contact_raw['email'] ) ? sanitize_email( (string) $contact_raw['email'] ) : '';
	if ( '' !== $email && ! is_email( $email ) ) {
		return nl_proposal_rfp_field_error( 'contact.email', 'contact.email is invalid.' );
	}
	if ( isset( $contact_raw['phone'] ) && ! is_scalar( $contact_raw['phone'] ) ) {
		return nl_proposal_rfp_field_error( 'contact.phone', 'contact.phone is invalid.' );
	}
	$phone = isset( $contact_raw['phone'] ) ? trim( (string) $contact_raw['phone'] ) : '';
	if ( '' !== $phone ) {
		$phone = preg_replace( '/[^\d+().\-\s]/', '', $phone );
		if ( ! is_string( $phone ) || strlen( $phone ) < 7 || strlen( $phone ) > 30 || ! preg_match( '/\d{6}/', preg_replace( '/\D/', '', $phone ) ) ) {
			return nl_proposal_rfp_field_error( 'contact.phone', 'contact.phone is invalid.' );
		}
	}
	if ( '' === $email && '' === $phone ) {
		return nl_proposal_rfp_field_error( 'contact.email', 'An email address or phone number is required.' );
	}
	if ( isset( $contact_raw['preferred_channel'] ) && ! is_scalar( $contact_raw['preferred_channel'] ) ) {
		return nl_proposal_rfp_error( 'invalid_request', 'contact.preferred_channel is unsupported.', 400 );
	}
	$preferred_channel = isset( $contact_raw['preferred_channel'] ) ? sanitize_key( $contact_raw['preferred_channel'] ) : '';
	if ( '' !== $preferred_channel && ! in_array( $preferred_channel, array( 'email', 'phone', 'whatsapp', 'video_call' ), true ) ) {
		return nl_proposal_rfp_error( 'invalid_request', 'contact.preferred_channel is unsupported.', 400 );
	}
	if ( 'email' === $preferred_channel && '' === $email ) {
		return nl_proposal_rfp_field_error( 'contact.email', 'Email is required for the selected contact preference.' );
	}
	if ( in_array( $preferred_channel, array( 'phone', 'whatsapp' ), true ) && '' === $phone ) {
		return nl_proposal_rfp_field_error( 'contact.phone', 'Phone is required for the selected contact preference.' );
	}

	$requirements_raw = isset( $raw['requirements'] ) ? $raw['requirements'] : array();
	$check            = nl_proposal_rfp_reject_unknown_keys(
		$requirements_raw,
		array(
			'headcount',
			'target_move_in',
			'lease_term_months',
			'area_min_sqm',
			'area_max_sqm',
			'budget_monthly',
			'budget_currency',
			'attendance_ratio_pct',
			'special_uses',
		),
		'requirements'
	);
	if ( is_wp_error( $check ) ) {
		return $check;
	}

	$headcount = nl_proposal_rfp_integer(
		isset( $requirements_raw['headcount'] ) ? $requirements_raw['headcount'] : null,
		'requirements.headcount',
		1,
		100000
	);
	if ( is_wp_error( $headcount ) ) {
		return $headcount;
	}
	$target_move_in = nl_proposal_rfp_target_month(
		isset( $requirements_raw['target_move_in'] ) ? $requirements_raw['target_move_in'] : null
	);
	if ( is_wp_error( $target_move_in ) ) {
		return $target_move_in;
	}
	$lease_term = nl_proposal_rfp_integer(
		isset( $requirements_raw['lease_term_months'] ) ? $requirements_raw['lease_term_months'] : null,
		'requirements.lease_term_months',
		1,
		360
	);
	if ( is_wp_error( $lease_term ) ) {
		return $lease_term;
	}
	$area_min = nl_proposal_rfp_decimal(
		isset( $requirements_raw['area_min_sqm'] ) ? $requirements_raw['area_min_sqm'] : null,
		'requirements.area_min_sqm',
		1,
		1000000
	);
	if ( is_wp_error( $area_min ) ) {
		return $area_min;
	}
	$area_max = nl_proposal_rfp_decimal(
		isset( $requirements_raw['area_max_sqm'] ) ? $requirements_raw['area_max_sqm'] : null,
		'requirements.area_max_sqm',
		1,
		1000000
	);
	if ( is_wp_error( $area_max ) ) {
		return $area_max;
	}
	if ( null !== $area_min && null !== $area_max && $area_min > $area_max ) {
		return nl_proposal_rfp_error( 'invalid_request', 'Minimum area cannot exceed maximum area.', 400 );
	}
	$budget = nl_proposal_rfp_decimal(
		isset( $requirements_raw['budget_monthly'] ) ? $requirements_raw['budget_monthly'] : null,
		'requirements.budget_monthly',
		0,
		1000000000
	);
	if ( is_wp_error( $budget ) ) {
		return $budget;
	}
	if ( isset( $requirements_raw['budget_currency'] ) && ! is_scalar( $requirements_raw['budget_currency'] ) ) {
		return nl_proposal_rfp_error( 'invalid_request', 'requirements.budget_currency is unsupported.', 400 );
	}
	$currency = isset( $requirements_raw['budget_currency'] ) ? strtoupper( trim( (string) $requirements_raw['budget_currency'] ) ) : '';
	if ( '' !== $currency && ! in_array( $currency, array( 'ILS', 'USD', 'EUR', 'GBP' ), true ) ) {
		return nl_proposal_rfp_error( 'invalid_request', 'requirements.budget_currency is unsupported.', 400 );
	}
	if ( null !== $budget && '' === $currency ) {
		return nl_proposal_rfp_error( 'invalid_request', 'A budget currency is required with a budget.', 400 );
	}
	$attendance = nl_proposal_rfp_decimal(
		isset( $requirements_raw['attendance_ratio_pct'] ) ? $requirements_raw['attendance_ratio_pct'] : null,
		'requirements.attendance_ratio_pct',
		0,
		100
	);
	if ( is_wp_error( $attendance ) ) {
		return $attendance;
	}
	$special_uses = nl_proposal_rfp_id_list(
		isset( $requirements_raw['special_uses'] ) ? $requirements_raw['special_uses'] : array(),
		array( 'standard_office', 'secure_room', 'lab', 'studio', 'trading_floor', 'customer_center', 'server_room', 'training_center' ),
		'requirements.special_uses',
		8
	);
	if ( is_wp_error( $special_uses ) ) {
		return $special_uses;
	}

	$question_ids = nl_proposal_rfp_id_list(
		isset( $raw['question_ids'] ) ? $raw['question_ids'] : array(),
		nl_proposal_commercial_question_ids(),
		'question_ids',
		40
	);
	if ( is_wp_error( $question_ids ) ) {
		return $question_ids;
	}
	$document_ids = nl_proposal_rfp_id_list(
		isset( $raw['document_ids'] ) ? $raw['document_ids'] : array(),
		nl_proposal_commercial_document_ids(),
		'document_ids',
		40
	);
	if ( is_wp_error( $document_ids ) ) {
		return $document_ids;
	}
	$question_text = nl_proposal_rfp_textarea(
		isset( $raw['question_text'] ) ? $raw['question_text'] : '',
		'question_text',
		4000
	);
	if ( is_wp_error( $question_text ) ) {
		return $question_text;
	}
	if ( empty( $question_ids ) && empty( $document_ids ) && '' === $question_text ) {
		return nl_proposal_rfp_field_error( 'question_ids', 'Select at least one question, document or written request.' );
	}

	$consent_raw = isset( $raw['consent'] ) ? $raw['consent'] : array();
	$check       = nl_proposal_rfp_reject_unknown_keys(
		$consent_raw,
		array( 'privacy', 'terms', 'marketing', 'text_version' ),
		'consent'
	);
	if ( is_wp_error( $check ) ) {
		return $check;
	}
	if ( true !== ( isset( $consent_raw['privacy'] ) ? $consent_raw['privacy'] : false ) || true !== ( isset( $consent_raw['terms'] ) ? $consent_raw['terms'] : false ) ) {
		return nl_proposal_rfp_error(
			'consent_required',
			'Privacy and request-processing consent are required.',
			400,
			array( 'field' => 'consent.privacy' )
		);
	}
	if ( isset( $consent_raw['marketing'] ) && ! is_bool( $consent_raw['marketing'] ) ) {
		return nl_proposal_rfp_field_error( 'consent.marketing', 'consent.marketing must be a boolean.' );
	}
	if ( isset( $consent_raw['text_version'] ) && ! is_scalar( $consent_raw['text_version'] ) ) {
		return nl_proposal_rfp_consent_version_error();
	}
	$consent_version = isset( $consent_raw['text_version'] ) ? (string) $consent_raw['text_version'] : '';
	$current_consent_version = nl_proposal_current_commercial_rfp_consent_version();
	if ( '' === $current_consent_version || ! hash_equals( $current_consent_version, $consent_version ) ) {
		return nl_proposal_rfp_consent_version_error();
	}

	$page_path = nl_proposal_rfp_page_path( isset( $raw['page_url'] ) ? $raw['page_url'] : null );
	if ( is_wp_error( $page_path ) ) {
		return $page_path;
	}

	return array(
		'schema_version' => NL_PROPOSAL_RFP_SCHEMA_VERSION,
		'environment'    => $environment,
		'sandbox_post_id'=> $sandbox_post_id,
		'project_id'     => $project_id,
		'project_contract_id' => $project_contract_id,
		'asset'          => array(
			'building_id' => $building_id,
			'tower_id'    => $tower_id,
			'floor_id'    => $floor_id,
			'suite_id'    => $suite_id,
		),
		'locale'         => $locale,
		'company'        => array(
			'name'                 => $company_name,
			'registration_country' => $country,
			'website'              => $company_website,
			'size_band'            => $size_band,
		),
		'contact'        => array(
			'name'              => $contact_name,
			'role'              => $role,
			'email'             => $email,
			'phone'             => $phone,
			'preferred_channel' => $preferred_channel,
		),
		'requirements'   => array(
			'headcount'           => $headcount,
			'target_move_in'      => $target_move_in,
			'lease_term_months'   => $lease_term,
			'area_min_sqm'        => $area_min,
			'area_max_sqm'        => $area_max,
			'budget_monthly'      => $budget,
			'budget_currency'     => $currency,
			'attendance_ratio_pct'=> $attendance,
			'special_uses'        => $special_uses,
		),
		'question_ids'   => $question_ids,
		'document_ids'   => $document_ids,
		'question_text'  => $question_text,
		'consent'        => array(
			'privacy'     => true,
			'terms'       => true,
			'marketing'   => true === ( isset( $consent_raw['marketing'] ) ? $consent_raw['marketing'] : false ),
			'text_version'=> $current_consent_version,
		),
		'page_path'      => $page_path,
	);
}

/**
 * Verify the exact project/building/tower/floor and nullable suite tuple.
 *
 * The inventory adapter must explicitly return true for a selected asset.
 * The default is false; there is no "looks like floor 20" fallback.
 *
 * @param array $payload Normalized request.
 * @return true|WP_Error
 */
function nl_proposal_validate_commercial_rfp_target( $payload ) {
	$project_id = (int) $payload['project_id'];
	$post       = get_post( $project_id );
	if ( ! $post || 'publish' !== $post->post_status ) {
		return nl_proposal_rfp_error( 'invalid_project', 'The selected project is unavailable.', 404 );
	}

	$asset_type = sanitize_key( (string) get_post_meta( $project_id, '_nl_asset_type', true ) );
	$asset_type = apply_filters( 'nl_proposal_commercial_project_asset_type', $asset_type, $project_id );
	// The current proposal ships one implemented enquiry/UI adapter only.
	// Product-family or applicability tags must never enable an asset type.
	if ( 'commercial_office' !== $asset_type ) {
		return nl_proposal_rfp_error( 'invalid_project', 'The selected project is not configured for commercial enquiries.', 409 );
	}
	$expected_contract_id = get_post_meta( $project_id, '_nl_commercial_project_contract_id', true );
	$expected_contract_id = apply_filters(
		'nl_proposal_commercial_project_contract_id',
		$expected_contract_id,
		$project_id
	);
	$expected_contract_id = nl_proposal_rfp_contract_id( $expected_contract_id, 'configured_project_contract_id' );
	if ( is_wp_error( $expected_contract_id ) || ! hash_equals( (string) $expected_contract_id, (string) $payload['project_contract_id'] ) ) {
		return nl_proposal_rfp_error( 'invalid_project', 'The selected project identity could not be verified.', 409 );
	}

	$building_id = $payload['asset']['building_id'];
	$tower_id    = $payload['asset']['tower_id'];
	$floor_id = $payload['asset']['floor_id'];
	$suite_id = $payload['asset']['suite_id'];
	$exists = apply_filters(
		'nl_proposal_commercial_asset_exists',
		false,
		$project_id,
		$payload['project_contract_id'],
		$building_id,
		$tower_id,
		$floor_id,
		$suite_id
	);
	if ( true !== $exists ) {
		return nl_proposal_rfp_error( 'invalid_asset', 'The selected building, tower, floor or suite could not be verified.', 409 );
	}

	return true;
}

/**
 * Parse a strict RFC3339 timestamp for routing configuration.
 *
 * @param mixed $value Raw value.
 * @return int|WP_Error
 */
function nl_proposal_rfp_route_timestamp( $value ) {
	if ( ! is_string( $value ) || ! preg_match( '/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})$/', $value ) ) {
		return new WP_Error( 'invalid_route_timestamp', 'Route timestamp is invalid.' );
	}
	try {
		return ( new DateTimeImmutable( $value ) )->getTimestamp();
	} catch ( Exception $exception ) {
		return new WP_Error( 'invalid_route_timestamp', 'Route timestamp is invalid.' );
	}
}

/**
 * Normalize and validate an accountable route.
 *
 * @param mixed  $raw Raw route config.
 * @param string $kind project_team or commercial_desk.
 * @return array|WP_Error
 */
function nl_proposal_normalize_commercial_rfp_route( $raw, $kind ) {
	if ( ! is_array( $raw ) || true !== ( isset( $raw['enabled'] ) ? $raw['enabled'] : false ) ) {
		return new WP_Error( 'route_not_configured', 'Commercial route is not configured.' );
	}

	$team_key = nl_proposal_rfp_contract_id(
		isset( $raw['team_key'] ) ? $raw['team_key'] : null,
		'route.team_key'
	);
	if ( is_wp_error( $team_key ) || null === $team_key ) {
		return new WP_Error( 'route_not_configured', 'Commercial route team is missing.' );
	}

	$mailbox = isset( $raw['mailbox'] ) ? sanitize_email( (string) $raw['mailbox'] ) : '';
	if ( '' === $mailbox || ! is_email( $mailbox ) ) {
		return new WP_Error( 'route_not_configured', 'Commercial route mailbox is invalid.' );
	}

	$accountable_user_id = isset( $raw['accountable_user_id'] ) ? absint( $raw['accountable_user_id'] ) : 0;
	$accountable_user    = $accountable_user_id > 0 ? get_user_by( 'id', $accountable_user_id ) : false;
	if ( ! $accountable_user || 0 !== (int) $accountable_user->user_status ) {
		return new WP_Error( 'route_not_configured', 'Commercial route has no active accountable user.' );
	}

	$sla_hours = isset( $raw['sla_hours'] ) ? absint( $raw['sla_hours'] ) : 0;
	if ( $sla_hours < 1 || $sla_hours > 168 ) {
		return new WP_Error( 'route_not_configured', 'Commercial route SLA is invalid.' );
	}

	$verified_at = nl_proposal_rfp_route_timestamp( isset( $raw['verified_at'] ) ? $raw['verified_at'] : null );
	$expires_at  = nl_proposal_rfp_route_timestamp( isset( $raw['expires_at'] ) ? $raw['expires_at'] : null );
	if ( is_wp_error( $verified_at ) || is_wp_error( $expires_at ) ) {
		return new WP_Error( 'route_not_configured', 'Commercial route evidence is invalid.' );
	}

	$now = time();
	if ( $verified_at > $now + 300 || $expires_at <= $now || $expires_at <= $verified_at || ( $expires_at - $verified_at ) > 90 * DAY_IN_SECONDS ) {
		return new WP_Error( 'route_expired', 'Commercial route is stale.' );
	}

	return array(
		'kind'                => $kind,
		'team_key'            => $team_key,
		'mailbox'             => $mailbox,
		'accountable_user_id' => $accountable_user_id,
		'sla_hours'           => $sla_hours,
		'verified_at'         => gmdate( 'c', $verified_at ),
		'expires_at'          => gmdate( 'c', $expires_at ),
	);
}

/**
 * Resolve a per-project route, then an explicitly configured commercial desk.
 *
 * There is intentionally no implicit admin_email fallback and no paid-tier or
 * claim-state check. Missing/stale project routes emit a non-PII operational
 * hook before the configured desk is considered.
 *
 * @param int $project_id Project post ID.
 * @return array|WP_Error
 */
function nl_proposal_resolve_commercial_rfp_route( $project_id ) {
	$project_route = array(
		'enabled'             => (bool) get_post_meta( $project_id, '_nl_commercial_rfp_route_enabled', true ),
		'team_key'            => get_post_meta( $project_id, '_nl_commercial_rfp_team_key', true ),
		'mailbox'             => get_post_meta( $project_id, '_nl_commercial_rfp_mailbox', true ),
		'accountable_user_id' => get_post_meta( $project_id, '_nl_commercial_rfp_accountable_user_id', true ),
		'sla_hours'           => get_post_meta( $project_id, '_nl_commercial_rfp_sla_hours', true ),
		'verified_at'         => get_post_meta( $project_id, '_nl_commercial_rfp_route_verified_at', true ),
		'expires_at'          => get_post_meta( $project_id, '_nl_commercial_rfp_route_expires_at', true ),
	);
	$project_route = apply_filters( 'nl_proposal_commercial_rfp_project_route', $project_route, $project_id );
	$normalized    = nl_proposal_normalize_commercial_rfp_route( $project_route, 'project_team' );
	if ( ! is_wp_error( $normalized ) ) {
		return $normalized;
	}

	do_action(
		'nl_proposal_commercial_rfp_route_attention',
		array(
			'project_id' => (int) $project_id,
			'route_kind' => 'project_team',
			'error_code' => $normalized->get_error_code(),
		)
	);

	$desk_route = get_option( 'nl_commercial_rfp_fallback_route', array() );
	$desk_route = apply_filters( 'nl_proposal_commercial_rfp_desk_route', $desk_route, $project_id );
	$normalized = nl_proposal_normalize_commercial_rfp_route( $desk_route, 'commercial_desk' );
	if ( is_wp_error( $normalized ) ) {
		do_action(
			'nl_proposal_commercial_rfp_route_attention',
			array(
				'project_id' => (int) $project_id,
				'route_kind' => 'commercial_desk',
				'error_code' => $normalized->get_error_code(),
			)
		);
		return nl_proposal_rfp_error(
			'route_unavailable',
			'The commercial response team is temporarily unavailable. Please try again later.',
			503
		);
	}

	return $normalized;
}

/**
 * Return whether encrypted-at-rest storage is available.
 *
 * @return bool
 */
function nl_proposal_rfp_crypto_ready() {
	return function_exists( 'openssl_encrypt' )
		&& function_exists( 'openssl_decrypt' )
		&& in_array( 'aes-256-gcm', openssl_get_cipher_methods(), true );
}

/**
 * Derive a site-specific encryption key from WordPress salts.
 *
 * @return string
 */
function nl_proposal_rfp_encryption_key() {
	return hash(
		'sha256',
		wp_salt( 'auth' ) . '|' . wp_salt( 'secure_auth' ) . '|nl-commercial-rfp-v1',
		true
	);
}

/**
 * Encrypt the PII-bearing operational payload.
 *
 * Rotating WordPress salts requires a controlled re-encryption migration.
 *
 * @param array $payload Normalized payload.
 * @return string|WP_Error JSON envelope.
 */
function nl_proposal_encrypt_commercial_rfp_payload( $payload ) {
	if ( ! nl_proposal_rfp_crypto_ready() ) {
		return new WP_Error( 'crypto_unavailable', 'Encrypted request storage is unavailable.' );
	}

	try {
		$iv = random_bytes( 12 );
	} catch ( Exception $exception ) {
		return new WP_Error( 'crypto_unavailable', 'Secure randomness is unavailable.' );
	}

	$plaintext = wp_json_encode( $payload, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
	if ( false === $plaintext ) {
		return new WP_Error( 'encoding_failed', 'Request encoding failed.' );
	}

	$tag        = '';
	$ciphertext = openssl_encrypt(
		$plaintext,
		'aes-256-gcm',
		nl_proposal_rfp_encryption_key(),
		OPENSSL_RAW_DATA,
		$iv,
		$tag,
		'nl-commercial-rfp-v1',
		16
	);

	if ( false === $ciphertext || 16 !== strlen( $tag ) ) {
		return new WP_Error( 'encryption_failed', 'Request encryption failed.' );
	}

	$envelope = wp_json_encode(
		array(
			'version'    => 1,
			'algorithm'  => 'aes-256-gcm',
			'iv'         => base64_encode( $iv ),
			'tag'        => base64_encode( $tag ),
			'ciphertext' => base64_encode( $ciphertext ),
		),
		JSON_UNESCAPED_SLASHES
	);

	return false === $envelope
		? new WP_Error( 'encoding_failed', 'Encrypted envelope encoding failed.' )
		: $envelope;
}

/**
 * Decrypt a stored operational payload.
 *
 * @param mixed $stored Stored JSON envelope.
 * @return array|WP_Error
 */
function nl_proposal_decrypt_commercial_rfp_payload( $stored ) {
	if ( ! nl_proposal_rfp_crypto_ready() || ! is_string( $stored ) || '' === $stored ) {
		return new WP_Error( 'decryption_failed', 'Encrypted request cannot be read.' );
	}

	$envelope = json_decode( $stored, true );
	if ( ! is_array( $envelope ) || 1 !== ( isset( $envelope['version'] ) ? (int) $envelope['version'] : 0 ) || 'aes-256-gcm' !== ( isset( $envelope['algorithm'] ) ? $envelope['algorithm'] : '' ) ) {
		return new WP_Error( 'decryption_failed', 'Encrypted request format is unsupported.' );
	}

	$iv         = isset( $envelope['iv'] ) ? base64_decode( $envelope['iv'], true ) : false;
	$tag        = isset( $envelope['tag'] ) ? base64_decode( $envelope['tag'], true ) : false;
	$ciphertext = isset( $envelope['ciphertext'] ) ? base64_decode( $envelope['ciphertext'], true ) : false;
	if ( false === $iv || false === $tag || false === $ciphertext || 12 !== strlen( $iv ) || 16 !== strlen( $tag ) ) {
		return new WP_Error( 'decryption_failed', 'Encrypted request is malformed.' );
	}

	$plaintext = openssl_decrypt(
		$ciphertext,
		'aes-256-gcm',
		nl_proposal_rfp_encryption_key(),
		OPENSSL_RAW_DATA,
		$iv,
		$tag,
		'nl-commercial-rfp-v1'
	);
	if ( false === $plaintext ) {
		return new WP_Error( 'decryption_failed', 'Encrypted request authentication failed.' );
	}

	$payload = json_decode( $plaintext, true );
	if ( ! is_array( $payload ) ) {
		return new WP_Error( 'decryption_failed', 'Encrypted request payload is invalid.' );
	}

	return $payload;
}

/**
 * Register the private case post type.
 *
 * @return void
 */
function nl_proposal_register_commercial_rfp_post_type() {
	register_post_type(
		'nl_commercial_rfp',
		array(
			'labels'              => array( 'name' => 'Commercial RFP cases' ),
			'public'              => false,
			'publicly_queryable'  => false,
			'show_ui'             => false,
			'show_in_rest'        => false,
			'exclude_from_search' => true,
			'supports'            => array( 'title' ),
			'rewrite'             => false,
			'query_var'           => false,
		)
	);
}

/**
 * Generate an opaque case identifier without project/date/email information.
 *
 * @return string|WP_Error
 */
function nl_proposal_generate_commercial_rfp_case_id() {
	try {
		return 'NLC-' . strtoupper( bin2hex( random_bytes( 12 ) ) );
	} catch ( Exception $exception ) {
		return new WP_Error( 'case_id_failed', 'A secure case ID could not be generated.' );
	}
}

/**
 * Store a minimal case record with encrypted PII and a bounded retention date.
 *
 * @param string $case_id Case ID.
 * @param array  $payload Normalized request.
 * @param array  $route Accountable route.
 * @param array  $idempotency Durable idempotency identity/signature.
 * @return int|WP_Error Post ID.
 */
function nl_proposal_store_commercial_rfp_case( $case_id, $payload, $route, $idempotency = array() ) {
	$received_at = isset( $idempotency['created_at'] )
		? (int) $idempotency['created_at']
		: time();
	$payload['server_record'] = array(
		'received_at'            => gmdate( 'c', $received_at ),
		'consent_recorded_at'    => gmdate( 'c', $received_at ),
		'consent_text_version'   => isset( $payload['consent']['text_version'] )
			? (string) $payload['consent']['text_version']
			: '',
	);

	$encrypted = nl_proposal_encrypt_commercial_rfp_payload( $payload );
	if ( is_wp_error( $encrypted ) ) {
		return $encrypted;
	}

	$idempotency_hash = isset( $idempotency['hash'] ) ? (string) $idempotency['hash'] : '';
	$signature        = isset( $idempotency['signature'] ) ? (string) $idempotency['signature'] : '';
	$post_slug        = $idempotency_hash
		? 'rfp-' . substr( $idempotency_hash, 0, 40 )
		: '';
	$existing_post    = $post_slug
		? get_page_by_path( $post_slug, OBJECT, 'nl_commercial_rfp' )
		: null;
	if ( $existing_post ) {
		if ( (string) $existing_post->post_title !== (string) $case_id ) {
			return new WP_Error( 'idempotency_case_collision', 'The durable idempotency case identity is inconsistent.' );
		}
		$post_id = (int) $existing_post->ID;
	} else {
		$post_id = wp_insert_post(
			array(
				'post_type'    => 'nl_commercial_rfp',
				'post_status'  => 'private',
				'post_title'   => $case_id,
				'post_name'    => $post_slug,
				'post_content' => '',
			),
			true
		);
		if ( is_wp_error( $post_id ) ) {
			return $post_id;
		}
	}

	$retention_days  = (int) apply_filters( 'nl_proposal_commercial_rfp_retention_days', 30 );
	$retention_days  = max( 1, min( 365, $retention_days ) );
	$retention_until = $received_at + ( $retention_days * DAY_IN_SECONDS );
	$sla_due_at      = $received_at + ( (int) $route['sla_hours'] * HOUR_IN_SECONDS );

	update_post_meta( $post_id, '_nl_rfp_case_id', $case_id );
	update_post_meta( $post_id, '_nl_rfp_project_id', (int) $payload['project_id'] );
	update_post_meta( $post_id, '_nl_rfp_project_contract_id', $payload['project_contract_id'] );
	update_post_meta( $post_id, '_nl_rfp_building_id', $payload['asset']['building_id'] );
	update_post_meta( $post_id, '_nl_rfp_tower_id', $payload['asset']['tower_id'] );
	update_post_meta( $post_id, '_nl_rfp_floor_id', $payload['asset']['floor_id'] );
	update_post_meta( $post_id, '_nl_rfp_suite_id', null === $payload['asset']['suite_id'] ? '' : $payload['asset']['suite_id'] );
	update_post_meta( $post_id, '_nl_rfp_route_kind', $route['kind'] );
	update_post_meta( $post_id, '_nl_rfp_route_team_key', $route['team_key'] );
	update_post_meta( $post_id, '_nl_rfp_accountable_user_id', (int) $route['accountable_user_id'] );
	update_post_meta( $post_id, '_nl_rfp_received_at', $received_at );
	update_post_meta( $post_id, '_nl_rfp_sla_due_at', $sla_due_at );
	update_post_meta( $post_id, '_nl_rfp_retention_until', $retention_until );
	update_post_meta( $post_id, '_nl_rfp_case_status', 'open' );
	update_post_meta( $post_id, '_nl_rfp_delivery_status', 'received' );
	update_post_meta( $post_id, '_nl_rfp_delivery_attempts', 0 );
	update_post_meta( $post_id, '_nl_rfp_payload_v1', $encrypted );
	if ( $idempotency_hash && $signature ) {
		update_post_meta( $post_id, '_nl_rfp_idempotency_hash', $idempotency_hash );
		update_post_meta( $post_id, '_nl_rfp_idempotency_signature', $signature );
	}

	if ( ! wp_next_scheduled( 'nl_proposal_delete_commercial_rfp_case', array( $post_id ) ) ) {
		wp_schedule_single_event( $retention_until, 'nl_proposal_delete_commercial_rfp_case', array( $post_id ) );
	}
	if ( ! wp_next_scheduled( 'nl_proposal_check_commercial_rfp_sla', array( $post_id ) ) ) {
		wp_schedule_single_event( $sla_due_at, 'nl_proposal_check_commercial_rfp_sla', array( $post_id ) );
	}

	return $post_id;
}

/**
 * Format a plain-text operational message.
 *
 * @param string $case_id Case ID.
 * @param array  $payload Decrypted normalized payload.
 * @return string
 */
function nl_proposal_format_commercial_rfp_message( $case_id, $payload ) {
	$lines = array(
		'Commercial RFP case: ' . $case_id,
		'Project post ID: ' . (int) $payload['project_id'],
		'Project contract ID: ' . $payload['project_contract_id'],
		'Building ID: ' . $payload['asset']['building_id'],
		'Tower ID: ' . $payload['asset']['tower_id'],
		'Floor ID: ' . $payload['asset']['floor_id'],
		'Suite ID: ' . ( $payload['asset']['suite_id'] ? $payload['asset']['suite_id'] : 'not selected' ),
		'Locale: ' . $payload['locale'],
		'Page path: ' . ( $payload['page_path'] ? $payload['page_path'] : 'not supplied' ),
		'',
		'Company: ' . $payload['company']['name'],
		'Registration country: ' . ( $payload['company']['registration_country'] ? $payload['company']['registration_country'] : 'not supplied' ),
		'Company website: ' . ( $payload['company']['website'] ? $payload['company']['website'] : 'not supplied' ),
		'Company size: ' . ( $payload['company']['size_band'] ? $payload['company']['size_band'] : 'not supplied' ),
		'',
		'Contact: ' . $payload['contact']['name'],
		'Role: ' . ( $payload['contact']['role'] ? $payload['contact']['role'] : 'not supplied' ),
		'Email: ' . ( $payload['contact']['email'] ? $payload['contact']['email'] : 'not supplied' ),
		'Phone: ' . ( $payload['contact']['phone'] ? $payload['contact']['phone'] : 'not supplied' ),
		'Preferred channel: ' . ( $payload['contact']['preferred_channel'] ? $payload['contact']['preferred_channel'] : 'not supplied' ),
		'',
		'Question IDs: ' . ( $payload['question_ids'] ? implode( ', ', $payload['question_ids'] ) : 'none' ),
		'Document IDs: ' . ( $payload['document_ids'] ? implode( ', ', $payload['document_ids'] ) : 'none' ),
		'Written request:',
		$payload['question_text'] ? $payload['question_text'] : 'none',
		'',
		'Requirements:',
		wp_json_encode( $payload['requirements'], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ),
		'',
		'Privacy consent: yes',
		'Terms/request-processing consent: yes',
		'Marketing consent: ' . ( $payload['consent']['marketing'] ? 'yes' : 'no' ),
		'Consent text version: ' . $payload['consent']['text_version'],
		'Consent recorded by server: ' . $payload['server_record']['consent_recorded_at'],
	);

	return implode( "\n", $lines );
}

/**
 * Attempt accountable delivery for a stored case.
 *
 * @param int        $post_id Case post ID.
 * @param array|null $route_override Already validated route for the first
 *                                   synchronous attempt. Retries re-resolve.
 * @return array|WP_Error Safe delivery summary.
 */
function nl_proposal_dispatch_commercial_rfp_case( $post_id, $route_override = null ) {
	$post = get_post( $post_id );
	if ( ! $post || 'nl_commercial_rfp' !== $post->post_type ) {
		return new WP_Error( 'case_not_found', 'Commercial case was not found.' );
	}

	$payload = nl_proposal_decrypt_commercial_rfp_payload(
		get_post_meta( $post_id, '_nl_rfp_payload_v1', true )
	);
	if ( is_wp_error( $payload ) ) {
		return $payload;
	}

	$route = is_array( $route_override )
		? $route_override
		: nl_proposal_resolve_commercial_rfp_route( (int) $payload['project_id'] );
	if ( is_wp_error( $route ) ) {
		return $route;
	}

	$case_id  = (string) get_post_meta( $post_id, '_nl_rfp_case_id', true );
	$subject  = sprintf( '[Commercial RFP] %s / project %d', $case_id, (int) $payload['project_id'] );
	$body     = nl_proposal_format_commercial_rfp_message( $case_id, $payload );
	$headers  = array( 'Content-Type: text/plain; charset=UTF-8' );
	if ( ! empty( $payload['contact']['email'] ) && is_email( $payload['contact']['email'] ) ) {
		$headers[] = sprintf( 'Reply-To: <%s>', $payload['contact']['email'] );
	}

	$attempts = (int) get_post_meta( $post_id, '_nl_rfp_delivery_attempts', true ) + 1;
	update_post_meta( $post_id, '_nl_rfp_delivery_attempts', $attempts );
	update_post_meta( $post_id, '_nl_rfp_last_attempt_at', time() );

	$sent = wp_mail( $route['mailbox'], $subject, $body, $headers );
	if ( ! $sent ) {
		update_post_meta( $post_id, '_nl_rfp_delivery_status', 'delivery_pending' );
		return new WP_Error( 'delivery_pending', 'Case is stored but delivery is pending.' );
	}

	update_post_meta( $post_id, '_nl_rfp_delivery_status', 'routed' );
	update_post_meta( $post_id, '_nl_rfp_routed_at', time() );
	update_post_meta( $post_id, '_nl_rfp_route_kind', $route['kind'] );
	update_post_meta( $post_id, '_nl_rfp_route_team_key', $route['team_key'] );
	update_post_meta( $post_id, '_nl_rfp_accountable_user_id', (int) $route['accountable_user_id'] );

	return array(
		'delivery_state' => 'routed',
		'route_kind'     => $route['kind'],
		'sla_hours'      => (int) $route['sla_hours'],
	);
}

/**
 * Schedule bounded retry delivery without exposing contact data in cron args.
 *
 * @param int $post_id Case post ID.
 * @return void
 */
function nl_proposal_schedule_commercial_rfp_retry( $post_id ) {
	$attempts = (int) get_post_meta( $post_id, '_nl_rfp_delivery_attempts', true );
	if ( $attempts >= 5 ) {
		update_post_meta( $post_id, '_nl_rfp_delivery_status', 'dead_letter' );
		do_action(
			'nl_proposal_commercial_rfp_delivery_attention',
			array(
				'case_post_id' => (int) $post_id,
				'project_id'   => (int) get_post_meta( $post_id, '_nl_rfp_project_id', true ),
				'state'        => 'dead_letter',
			)
		);
		return;
	}

	$delay = min( 6 * HOUR_IN_SECONDS, 5 * MINUTE_IN_SECONDS * (int) pow( 2, max( 0, $attempts ) ) );
	if ( ! wp_next_scheduled( 'nl_proposal_retry_commercial_rfp_case', array( (int) $post_id ) ) ) {
		wp_schedule_single_event( time() + $delay, 'nl_proposal_retry_commercial_rfp_case', array( (int) $post_id ) );
	}
}

/**
 * Cron callback for a pending route.
 *
 * @param int $post_id Case post ID.
 * @return void
 */
function nl_proposal_retry_commercial_rfp_case( $post_id ) {
	if ( 'routed' === get_post_meta( $post_id, '_nl_rfp_delivery_status', true ) ) {
		return;
	}

	$result = nl_proposal_dispatch_commercial_rfp_case( $post_id );
	if ( is_wp_error( $result ) ) {
		nl_proposal_schedule_commercial_rfp_retry( $post_id );
	}
}

/**
 * Delete an expired case and its encrypted payload.
 *
 * @param int $post_id Case post ID.
 * @return void
 */
function nl_proposal_delete_commercial_rfp_case( $post_id ) {
	$retention_until = (int) get_post_meta( $post_id, '_nl_rfp_retention_until', true );
	if ( $retention_until > time() ) {
		if ( ! wp_next_scheduled( 'nl_proposal_delete_commercial_rfp_case', array( (int) $post_id ) ) ) {
			wp_schedule_single_event( $retention_until, 'nl_proposal_delete_commercial_rfp_case', array( (int) $post_id ) );
		}
		return;
	}
	wp_delete_post( $post_id, true );
}

/**
 * Raise a PII-free alert when a recorded case has not been marked responded or
 * closed by its accountable team before the promised time.
 *
 * CRM/mail integrations must update _nl_rfp_case_status to responded or closed.
 *
 * @param int $post_id Case post ID.
 * @return void
 */
function nl_proposal_check_commercial_rfp_sla( $post_id ) {
	$post = get_post( $post_id );
	if ( ! $post || 'nl_commercial_rfp' !== $post->post_type ) {
		return;
	}

	$status = (string) get_post_meta( $post_id, '_nl_rfp_case_status', true );
	if ( in_array( $status, array( 'responded', 'closed', 'privacy_erased' ), true ) ) {
		return;
	}

	do_action(
		'nl_proposal_commercial_rfp_sla_attention',
		array(
			'case_post_id' => (int) $post_id,
			'project_id'   => (int) get_post_meta( $post_id, '_nl_rfp_project_id', true ),
			'route_kind'   => (string) get_post_meta( $post_id, '_nl_rfp_route_kind', true ),
			'team_key'     => (string) get_post_meta( $post_id, '_nl_rfp_route_team_key', true ),
			'case_status'  => '' === $status ? 'open' : $status,
			'sla_due_at'   => (int) get_post_meta( $post_id, '_nl_rfp_sla_due_at', true ),
		)
	);
}

/**
 * Build a non-reversible, short-lived client fingerprint for rate limiting.
 *
 * The raw IP is never stored or emitted to analytics.
 *
 * @return string
 */
function nl_proposal_rfp_client_fingerprint() {
	$ip = isset( $_SERVER['REMOTE_ADDR'] ) ? (string) wp_unslash( $_SERVER['REMOTE_ADDR'] ) : 'unknown';
	return hash_hmac( 'sha256', $ip, wp_salt( 'nonce' ) );
}

/**
 * Acquire an atomic database-option mutex for one rate bucket.
 *
 * add_option() is used because its unique option_name constraint is atomic
 * across PHP workers, unlike a transient get/increment/set sequence.
 *
 * @param string $fingerprint HMAC fingerprint.
 * @return string|false Opaque owner token, or false when no lock was acquired.
 */
function nl_proposal_acquire_commercial_rfp_rate_lock( $fingerprint ) {
	global $wpdb;

	try {
		$token = bin2hex( random_bytes( 16 ) );
	} catch ( Exception $exception ) {
		return false;
	}

	$name  = 'nlp_rfp_rate_lock_' . substr( $fingerprint, 0, 40 );
	$value = array(
		'token'      => $token,
		'expires_at' => time() + 10,
	);
	if ( add_option( $name, $value, '', 'no' ) ) {
		return $token;
	}

	$existing = get_option( $name, null );
	if (
		! is_array( $existing )
		|| empty( $existing['token'] )
		|| empty( $existing['expires_at'] )
		|| (int) $existing['expires_at'] >= time()
	) {
		return false;
	}

	// Reclaim an expired mutex with one compare-and-swap. A read/delete/add
	// sequence is forbidden because it can delete a newer worker's lock.
	$updated = $wpdb->query(
		$wpdb->prepare(
			"UPDATE {$wpdb->options}
			 SET option_value = %s
			 WHERE option_name = %s
			   AND option_value = %s",
			maybe_serialize( $value ),
			$name,
			maybe_serialize( $existing )
		)
	);
	if ( 1 === $updated ) {
		wp_cache_delete( $name, 'options' );
		return $token;
	}

	return false;
}

/**
 * Release a rate-bucket mutex.
 *
 * @param string $fingerprint HMAC fingerprint.
 * @param string $token Lock-owner token returned by the acquire function.
 * @return void
 */
function nl_proposal_release_commercial_rfp_rate_lock( $fingerprint, $token ) {
	global $wpdb;

	$name     = 'nlp_rfp_rate_lock_' . substr( $fingerprint, 0, 40 );
	$existing = get_option( $name, null );
	if (
		! is_array( $existing )
		|| empty( $existing['token'] )
		|| ! is_string( $token )
		|| ! hash_equals( (string) $existing['token'], $token )
	) {
		return;
	}

	$wpdb->query(
		$wpdb->prepare(
			"DELETE FROM {$wpdb->options}
			 WHERE option_name = %s
			   AND option_value = %s",
			$name,
			maybe_serialize( $existing )
		)
	);
	wp_cache_delete( $name, 'options' );
}

/**
 * Apply an atomic fixed-window rate limit.
 *
 * @return true|WP_Error
 */
function nl_proposal_check_commercial_rfp_rate_limit() {
	$fingerprint = nl_proposal_rfp_client_fingerprint();
	$lock_token  = nl_proposal_acquire_commercial_rfp_rate_lock( $fingerprint );
	if ( false === $lock_token ) {
		// Fail closed rather than permit a request whose quota cannot be
		// updated atomically.
		return nl_proposal_rfp_error(
			'rate_limit_unavailable',
			'Request protection is temporarily busy. Please try again.',
			503
		);
	}

	try {
		$key    = 'nlp_rfp_rate_' . substr( $fingerprint, 0, 40 );
		$bucket = get_transient( $key );
		$now    = time();
		$limit  = (int) apply_filters( 'nl_proposal_commercial_rfp_rate_limit', 6 );
		$limit  = max( 1, min( 30, $limit ) );

		if ( ! is_array( $bucket ) || empty( $bucket['reset_at'] ) || (int) $bucket['reset_at'] <= $now ) {
			$bucket = array(
				'count'    => 0,
				'reset_at' => $now + HOUR_IN_SECONDS,
			);
		}

		if ( (int) $bucket['count'] >= $limit ) {
			return nl_proposal_rfp_error( 'rate_limited', 'Too many requests. Please try again later.', 429 );
		}

		$bucket['count'] = (int) $bucket['count'] + 1;
		if ( ! set_transient( $key, $bucket, max( 60, (int) $bucket['reset_at'] - $now ) ) ) {
			return nl_proposal_rfp_error(
				'rate_limit_unavailable',
				'Request protection is temporarily unavailable. Please try again.',
				503
			);
		}
		return true;
	} finally {
		nl_proposal_release_commercial_rfp_rate_lock( $fingerprint, $lock_token );
	}
}

/**
 * Validate and hash the required idempotency key.
 *
 * @param WP_REST_Request $request Request.
 * @return array|WP_Error Raw key is returned only in request memory.
 */
function nl_proposal_get_commercial_rfp_idempotency( $request ) {
	$key = trim( (string) $request->get_header( 'idempotency-key' ) );
	if ( strlen( $key ) < 16 || strlen( $key ) > 128 || ! preg_match( '/^[A-Za-z0-9._:-]+$/', $key ) ) {
		return nl_proposal_rfp_error( 'idempotency_required', 'A valid Idempotency-Key header is required.', 400 );
	}

	return array(
		'key'  => $key,
		'hash' => hash_hmac( 'sha256', $key, wp_salt( 'nonce' ) ),
	);
}

/**
 * Recursively canonicalize the parsed JSON value for an immutable request
 * signature. Object keys are sorted, while list order and scalar types remain
 * significant. No raw value is stored; the caller persists only an HMAC.
 *
 * @param mixed $value Parsed JSON value.
 * @param bool  $valid Set false for a non-JSON runtime value.
 * @return mixed
 */
function nl_proposal_canonicalize_commercial_rfp_request_value( $value, &$valid ) {
	if ( null === $value || is_string( $value ) || is_int( $value ) || is_bool( $value ) ) {
		return $value;
	}
	if ( is_float( $value ) ) {
		if ( ! is_finite( $value ) ) {
			$valid = false;
		}
		return $value;
	}
	if ( ! is_array( $value ) ) {
		$valid = false;
		return null;
	}

	if ( nl_proposal_rfp_is_list( $value ) ) {
		$result = array();
		foreach ( $value as $item ) {
			$result[] = nl_proposal_canonicalize_commercial_rfp_request_value( $item, $valid );
			if ( ! $valid ) {
				return null;
			}
		}
		return $result;
	}

	$keys = array_keys( $value );
	foreach ( $keys as $key ) {
		if ( ! is_string( $key ) ) {
			$valid = false;
			return null;
		}
	}
	sort( $keys, SORT_STRING );
	$result = array();
	foreach ( $keys as $key ) {
		$result[ $key ] = nl_proposal_canonicalize_commercial_rfp_request_value( $value[ $key ], $valid );
		if ( ! $valid ) {
			return null;
		}
	}

	return $result;
}

/**
 * Compute the stable pre-validation request signature used for durable replay.
 *
 * This deliberately happens before mutable consent, publication, inventory and
 * route checks. An already accepted exact request can therefore retrieve its
 * opaque case after those facts change. A new key still traverses every current
 * gate. The endpoint context is signed to isolate production from the test sink.
 *
 * @param mixed  $raw Parsed JSON body.
 * @param string $endpoint_context production or sandbox-test.
 * @return string|WP_Error
 */
function nl_proposal_commercial_rfp_request_signature( $raw, $endpoint_context ) {
	if ( ! in_array( $endpoint_context, array( 'production', 'sandbox-test' ), true ) ) {
		return nl_proposal_rfp_error( 'request_encoding_failed', 'The request could not be processed.', 500 );
	}
	$valid     = true;
	$canonical = nl_proposal_canonicalize_commercial_rfp_request_value( $raw, $valid );
	if ( ! $valid || ! is_array( $canonical ) ) {
		return nl_proposal_rfp_error( 'invalid_request', 'The request body must be a JSON object.', 400 );
	}
	$encoded = wp_json_encode(
		$canonical,
		JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_PRESERVE_ZERO_FRACTION
	);
	if ( false === $encoded ) {
		return nl_proposal_rfp_error( 'request_encoding_failed', 'The request could not be processed.', 500 );
	}

	return hash_hmac(
		'sha256',
		'nl-commercial-rfp-request-v2|' . $endpoint_context . '|' . $encoded,
		wp_salt( 'secure_auth' )
	);
}

/**
 * Return a completed durable replay before mutable business-state validation.
 *
 * A reused key with any different canonical body receives the same opaque 409;
 * the prior case ID and response are never exposed. In-progress reservations
 * return null so their token-owned crash/resume path continues under the lock.
 *
 * @param string   $hash Idempotency-key HMAC.
 * @param string   $signature Canonical request HMAC.
 * @param string[] $allowed_route_kinds Route kinds permitted by this endpoint.
 * @return WP_REST_Response|WP_Error|null
 */
function nl_proposal_replay_completed_commercial_rfp_request( $hash, $signature, $allowed_route_kinds ) {
	$existing = nl_proposal_get_commercial_rfp_idempotency_record( $hash );
	if ( ! is_array( $existing ) || (int) $existing['expires_at'] <= time() ) {
		return null;
	}
	if ( ! hash_equals( (string) $existing['signature'], $signature ) ) {
		return nl_proposal_rfp_error( 'idempotency_conflict', 'The Idempotency-Key was already used for a different request.', 409 );
	}
	if ( ! in_array( $existing['route_kind'], $allowed_route_kinds, true ) ) {
		return nl_proposal_rfp_error( 'idempotency_conflict', 'The Idempotency-Key was already used for a different request.', 409 );
	}
	if ( 'complete' !== $existing['state'] || ! is_array( $existing['response'] ) ) {
		return null;
	}

	$response                       = $existing['response'];
	$response['idempotent_replay'] = true;
	return new WP_REST_Response( $response, 200 );
}

/**
 * Acquire a short atomic option lock for one idempotency key.
 *
 * @param string $hash HMAC.
 * @return string|false Opaque lock-owner token.
 */
function nl_proposal_acquire_commercial_rfp_lock( $hash ) {
	global $wpdb;

	try {
		$token = bin2hex( random_bytes( 16 ) );
	} catch ( Exception $exception ) {
		return false;
	}
	$name  = 'nlp_rfp_lock_' . substr( $hash, 0, 40 );
	$value = array(
		'token'      => $token,
		'expires_at' => time() + 30,
	);
	if ( add_option( $name, $value, '', 'no' ) ) {
		return $token;
	}

	$existing = get_option( $name, null );
	if (
		! is_array( $existing )
		|| empty( $existing['token'] )
		|| empty( $existing['expires_at'] )
		|| (int) $existing['expires_at'] >= time()
	) {
		return false;
	}
	$updated = $wpdb->query(
		$wpdb->prepare(
			"UPDATE {$wpdb->options}
			 SET option_value = %s
			 WHERE option_name = %s
			   AND option_value = %s",
			maybe_serialize( $value ),
			$name,
			maybe_serialize( $existing )
		)
	);
	if ( 1 === $updated ) {
		wp_cache_delete( $name, 'options' );
		return $token;
	}
	return false;
}

/**
 * Release an idempotency lock.
 *
 * @param string $hash HMAC.
 * @param string $token Exact owner token returned by acquire.
 * @return void
 */
function nl_proposal_release_commercial_rfp_lock( $hash, $token ) {
	global $wpdb;

	$name     = 'nlp_rfp_lock_' . substr( $hash, 0, 40 );
	$existing = get_option( $name, null );
	if (
		! is_array( $existing )
		|| empty( $existing['token'] )
		|| ! is_string( $token )
		|| ! hash_equals( (string) $existing['token'], $token )
	) {
		return;
	}
	$wpdb->query(
		$wpdb->prepare(
			"DELETE FROM {$wpdb->options}
			 WHERE option_name = %s
			   AND option_value = %s",
			$name,
			maybe_serialize( $existing )
		)
	);
	wp_cache_delete( $name, 'options' );
}

function nl_proposal_commercial_rfp_idempotency_option_name( $hash ) {
	return 'nlp_rfp_idem_' . substr( $hash, 0, 40 );
}

/**
 * Validate the durable replay record before any field is read or returned.
 * Corrupt or partially injected options fail closed instead of producing PHP
 * notices, replaying an unsafe response, or being treated as a free key.
 *
 * @param mixed $record Stored option value.
 * @return array|null Exact normalized record or null.
 */
function nl_proposal_normalize_commercial_rfp_idempotency_record( $record ) {
	$keys = array(
		'record_token',
		'signature',
		'state',
		'case_id',
		'post_id',
		'route_kind',
		'sla_hours',
		'created_at',
		'expires_at',
		'response',
	);
	if ( ! is_array( $record ) || array_keys( $record ) !== $keys ) {
		return null;
	}
	if (
		! is_string( $record['record_token'] )
		|| ! is_string( $record['case_id'] )
		|| ! hash_equals( $record['record_token'], $record['case_id'] )
		|| ! preg_match( '/^(?:NLC-[A-F0-9]{24}|TEST-[A-F0-9]{20})$/', $record['case_id'] )
		|| ! is_string( $record['signature'] )
		|| ! preg_match( '/^[a-f0-9]{64}$/', $record['signature'] )
		|| ! in_array( $record['state'], array( 'reserved', 'stored', 'complete' ), true )
		|| ! in_array( $record['route_kind'], array( 'project_team', 'commercial_desk', 'test_sink' ), true )
		|| ! is_int( $record['post_id'] )
		|| $record['post_id'] < 0
		|| ! is_int( $record['sla_hours'] )
		|| $record['sla_hours'] < ( 'test_sink' === $record['route_kind'] ? 0 : 1 )
		|| $record['sla_hours'] > 168
		|| ! is_int( $record['created_at'] )
		|| ! is_int( $record['expires_at'] )
		|| $record['created_at'] < 1
		|| $record['expires_at'] <= $record['created_at']
		|| ( null !== $record['response'] && ! is_array( $record['response'] ) )
		|| ( 'complete' === $record['state'] ) !== is_array( $record['response'] )
	) {
		return null;
	}

	if ( null !== $record['response'] ) {
		$is_test_sink = 'test_sink' === $record['route_kind'];
		$response_keys = $is_test_sink
			? array(
				'accepted',
				'case_id',
				'status',
				'environment',
				'delivery_state',
				'route_kind',
				'route_status',
				'recipient_label',
				'received_at',
				'response_due_at',
				'sla_hours',
				'idempotent_replay',
			)
			: array(
				'accepted',
				'case_id',
				'status',
				'delivery_state',
				'received_at',
				'response_due_at',
				'sla_hours',
				'route_kind',
				'idempotent_replay',
			);
		if (
			array_keys( $record['response'] ) !== $response_keys
			|| true !== $record['response']['accepted']
			|| ! hash_equals( $record['case_id'], (string) $record['response']['case_id'] )
			|| 'received' !== $record['response']['status']
			|| ! in_array( $record['response']['delivery_state'], $is_test_sink ? array( 'test_sink' ) : array( 'routed', 'processing' ), true )
			|| ! is_string( $record['response']['received_at'] )
			|| ! is_string( $record['response']['response_due_at'] )
			|| (int) $record['response']['sla_hours'] !== $record['sla_hours']
			|| ! hash_equals( $record['route_kind'], (string) $record['response']['route_kind'] )
			|| ! is_bool( $record['response']['idempotent_replay'] )
			|| ( $is_test_sink && (
				'test' !== $record['response']['environment']
				|| 'test_sink' !== $record['response']['route_status']
				|| ! is_string( $record['response']['recipient_label'] )
				|| '' === trim( $record['response']['recipient_label'] )
			) )
		) {
			return null;
		}
	}

	return $record;
}

function nl_proposal_get_commercial_rfp_idempotency_record( $hash ) {
	$record = get_option( nl_proposal_commercial_rfp_idempotency_option_name( $hash ), null );
	return nl_proposal_normalize_commercial_rfp_idempotency_record( $record );
}

function nl_proposal_write_commercial_rfp_idempotency_record( $hash, $record, $create = false ) {
	$record = nl_proposal_normalize_commercial_rfp_idempotency_record( $record );
	if ( null === $record ) {
		return false;
	}
	$name = nl_proposal_commercial_rfp_idempotency_option_name( $hash );
	$ok   = $create
		? add_option( $name, $record, '', 'no' )
		: update_option( $name, $record, false );
	$stored = get_option( $name, null );
	return (
		( $ok || is_array( $stored ) )
		&& is_array( $stored )
		&& isset( $stored['record_token'], $record['record_token'] )
		&& hash_equals( (string) $record['record_token'], (string) $stored['record_token'] )
		&& isset( $stored['signature'], $record['signature'] )
		&& hash_equals( (string) $record['signature'], (string) $stored['signature'] )
		&& isset( $stored['state'], $record['state'] )
		&& $stored['state'] === $record['state']
	);
}

function nl_proposal_delete_commercial_rfp_idempotency_record( $hash, $record_token ) {
	$lock_token = nl_proposal_acquire_commercial_rfp_lock( $hash );
	if ( false === $lock_token ) {
		return;
	}
	try {
		$record = nl_proposal_get_commercial_rfp_idempotency_record( $hash );
		if (
			is_array( $record )
			&& isset( $record['record_token'], $record['expires_at'] )
			&& hash_equals( (string) $record['record_token'], (string) $record_token )
			&& (int) $record['expires_at'] <= time()
		) {
			delete_option( nl_proposal_commercial_rfp_idempotency_option_name( $hash ) );
		}
	} finally {
		nl_proposal_release_commercial_rfp_lock( $hash, $lock_token );
	}
}

/**
 * Normalize an HTTP origin as scheme://host[:non-default-port].
 *
 * Browser Origin headers must not contain credentials, query, fragment, or an
 * application path. The home URL may contain a WordPress subdirectory, which
 * is intentionally ignored when deriving the site's origin.
 *
 * @param mixed $value Raw URL/origin.
 * @param bool  $allow_application_path Whether a site URL path is permitted.
 * @return string
 */
function nl_proposal_normalize_http_origin( $value, $allow_application_path = false ) {
	if ( ! is_string( $value ) || '' === trim( $value ) ) {
		return '';
	}

	$parts = wp_parse_url( trim( $value ) );
	if ( ! is_array( $parts ) ) {
		return '';
	}

	$scheme = isset( $parts['scheme'] ) ? strtolower( $parts['scheme'] ) : '';
	$host   = isset( $parts['host'] ) ? strtolower( rtrim( $parts['host'], '.' ) ) : '';
	$path   = isset( $parts['path'] ) ? $parts['path'] : '';
	if (
		! in_array( $scheme, array( 'http', 'https' ), true )
		|| '' === $host
		|| isset( $parts['user'] )
		|| isset( $parts['pass'] )
		|| isset( $parts['query'] )
		|| isset( $parts['fragment'] )
		|| ( ! $allow_application_path && ! in_array( $path, array( '', '/' ), true ) )
	) {
		return '';
	}

	$port = isset( $parts['port'] ) ? (int) $parts['port'] : 0;
	if ( ( isset( $parts['port'] ) && $port < 1 ) || $port > 65535 ) {
		return '';
	}
	if ( ( 'https' === $scheme && 443 === $port ) || ( 'http' === $scheme && 80 === $port ) ) {
		$port = 0;
	}

	$display_host = false !== strpos( $host, ':' ) ? '[' . trim( $host, '[]' ) . ']' : $host;
	return $scheme . '://' . $display_host . ( $port ? ':' . $port : '' );
}

/**
 * Return whether a private/password sandbox post is authenticated now.
 *
 * The feature constant and per-post flag are both mandatory. A private post
 * additionally needs read_post capability; a password-protected post needs a
 * valid WordPress post-password cookie. Merely knowing the post ID is not
 * authorization.
 *
 * @param int $post_id Sandbox post ID.
 * @return bool
 */
function nl_proposal_commercial_rfp_sandbox_context_allowed( $post_id ) {
	$post_id = (int) $post_id;
	if (
		$post_id < 1
		|| ! defined( 'NL_PROPOSAL_COMMERCIAL_SCENE_SANDBOX' )
		|| true !== NL_PROPOSAL_COMMERCIAL_SCENE_SANDBOX
		|| '1' !== (string) get_post_meta( $post_id, '_nl_commercial_scene_sandbox_enabled', true )
	) {
		return false;
	}
	$post = get_post( $post_id );
	if ( ! $post ) {
		return false;
	}
	if ( 'private' === (string) $post->post_status ) {
		return current_user_can( 'read_post', $post_id );
	}
	if ( '' !== (string) $post->post_password ) {
		return ! post_password_required( $post );
	}
	return false;
}

/** Create a short-lived signed sandbox nonce bound to one guarded post. */
function nl_proposal_create_commercial_rfp_sandbox_nonce( $post_id, $lifetime_seconds = 900 ) {
	$post_id = (int) $post_id;
	if ( ! nl_proposal_commercial_rfp_sandbox_context_allowed( $post_id ) ) {
		return '';
	}
	$lifetime_seconds = max( 60, min( 1800, (int) $lifetime_seconds ) );
	$expires_at = time() + $lifetime_seconds;
	$signature = hash_hmac(
		'sha256',
		implode( '|', array( 'commercial-rfp-sandbox-v1', $post_id, $expires_at ) ),
		wp_salt( 'nonce' )
	);
	return $expires_at . '.' . $signature;
}

/** Verify the exact signed sandbox nonce without exposing rejection details. */
function nl_proposal_verify_commercial_rfp_sandbox_nonce( $token, $post_id ) {
	if ( ! is_string( $token ) || strlen( $token ) > 160 || ! preg_match( '/^(\d{10})\.([a-f0-9]{64})$/', $token, $matches ) ) {
		return false;
	}
	$expires_at = (int) $matches[1];
	if ( $expires_at <= time() || $expires_at > time() + 1800 ) {
		return false;
	}
	$expected = hash_hmac(
		'sha256',
		implode( '|', array( 'commercial-rfp-sandbox-v1', (int) $post_id, $expires_at ) ),
		wp_salt( 'nonce' )
	);
	return hash_equals( $expected, $matches[2] );
}

/**
 * Validate transport, origin and content type before payload handling.
 *
 * @param WP_REST_Request $request Request.
 * @return true|WP_Error
 */
function nl_proposal_commercial_rfp_permission_check( $request ) {
	$allow_insecure = (bool) apply_filters( 'nl_proposal_commercial_rfp_allow_insecure_transport', false );
	if ( ! is_ssl() && ! $allow_insecure ) {
		return nl_proposal_rfp_error( 'https_required', 'Secure transport is required.', 503 );
	}

	$content_type = strtolower( (string) $request->get_header( 'content-type' ) );
	if ( 0 !== strpos( $content_type, 'application/json' ) ) {
		return nl_proposal_rfp_error( 'json_required', 'Content-Type must be application/json.', 415 );
	}

	if ( strlen( (string) $request->get_body() ) > 32768 ) {
		return nl_proposal_rfp_error( 'request_too_large', 'The request is too large.', 413 );
	}

	$origin = (string) $request->get_header( 'origin' );
	if ( '' !== $origin ) {
		$request_origin = nl_proposal_normalize_http_origin( $origin, false );
		$site_origin    = nl_proposal_normalize_http_origin( home_url( '/' ), true );
		if ( '' === $request_origin || '' === $site_origin || ! hash_equals( $site_origin, $request_origin ) ) {
			return nl_proposal_rfp_error( 'origin_rejected', 'Cross-site requests are not accepted.', 403 );
		}
	}

	return true;
}

/** Permission gate for the isolated, non-delivering sandbox endpoint. */
function nl_proposal_commercial_rfp_sandbox_permission_check( $request ) {
	$base = nl_proposal_commercial_rfp_permission_check( $request );
	if ( is_wp_error( $base ) ) {
		return $base;
	}
	$raw = $request->get_json_params();
	$post_id = is_array( $raw ) && isset( $raw['sandbox_post_id'] ) && is_numeric( $raw['sandbox_post_id'] )
		? (int) $raw['sandbox_post_id']
		: 0;
	$environment = is_array( $raw ) && isset( $raw['environment'] ) && is_scalar( $raw['environment'] )
		? (string) $raw['environment']
		: '';
	$nonce = (string) $request->get_header( 'x-nadlan-sandbox-nonce' );
	if (
		'test' !== $environment
		|| ! nl_proposal_commercial_rfp_sandbox_context_allowed( $post_id )
		|| ! nl_proposal_verify_commercial_rfp_sandbox_nonce( $nonce, $post_id )
	) {
		return nl_proposal_rfp_error( 'sandbox_rejected', 'The sandbox request was not accepted.', 403 );
	}
	return true;
}

/**
 * REST callback for POST /wp-json/nadlan/v2/commercial-rfp.
 *
 * @param WP_REST_Request $request Request.
 * @return WP_REST_Response|WP_Error
 */
function nl_proposal_handle_commercial_rfp_request( $request ) {
	$idempotency = nl_proposal_get_commercial_rfp_idempotency( $request );
	if ( is_wp_error( $idempotency ) ) {
		return $idempotency;
	}
	$raw_payload = $request->get_json_params();
	$signature   = nl_proposal_commercial_rfp_request_signature( $raw_payload, 'production' );
	if ( is_wp_error( $signature ) ) {
		return $signature;
	}
	$early_replay = nl_proposal_replay_completed_commercial_rfp_request(
		$idempotency['hash'],
		$signature,
		array( 'project_team', 'commercial_desk' )
	);
	if ( null !== $early_replay ) {
		return $early_replay;
	}

	$payload = nl_proposal_normalize_commercial_rfp_payload( $raw_payload );
	if ( is_wp_error( $payload ) ) {
		return $payload;
	}
	if ( 'production' !== $payload['environment'] || null !== $payload['sandbox_post_id'] ) {
		return nl_proposal_rfp_error( 'invalid_environment', 'The request environment is invalid.', 400 );
	}

	$target = nl_proposal_validate_commercial_rfp_target( $payload );
	if ( is_wp_error( $target ) ) {
		return $target;
	}

	$existing  = nl_proposal_get_commercial_rfp_idempotency_record( $idempotency['hash'] );

	if ( is_array( $existing ) && (int) $existing['expires_at'] > time() ) {
		if ( ! isset( $existing['signature'] ) || ! hash_equals( (string) $existing['signature'], $signature ) ) {
			return nl_proposal_rfp_error( 'idempotency_conflict', 'The Idempotency-Key was already used for a different request.', 409 );
		}
		$response                       = isset( $existing['response'] ) && is_array( $existing['response'] ) ? $existing['response'] : array();
		if ( $response ) {
			$response['idempotent_replay'] = true;
			return new WP_REST_Response( $response, 200 );
		}
	}

	$rate = nl_proposal_check_commercial_rfp_rate_limit();
	if ( is_wp_error( $rate ) ) {
		return $rate;
	}

	$lock_token = nl_proposal_acquire_commercial_rfp_lock( $idempotency['hash'] );
	if ( false === $lock_token ) {
		return nl_proposal_rfp_error( 'request_in_progress', 'An identical request is already being processed.', 409 );
	}

	try {
		$existing = nl_proposal_get_commercial_rfp_idempotency_record( $idempotency['hash'] );
		if ( is_array( $existing ) && (int) $existing['expires_at'] <= time() ) {
			delete_option( nl_proposal_commercial_rfp_idempotency_option_name( $idempotency['hash'] ) );
			$existing = null;
		}
		$record_was_present = is_array( $existing );
		if ( is_array( $existing ) ) {
			if ( ! isset( $existing['signature'] ) || ! hash_equals( (string) $existing['signature'], $signature ) ) {
				return nl_proposal_rfp_error( 'idempotency_conflict', 'The Idempotency-Key was already used for a different request.', 409 );
			}
			$response                      = isset( $existing['response'] ) && is_array( $existing['response'] ) ? $existing['response'] : array();
			if ( $response ) {
				$response['idempotent_replay'] = true;
				return new WP_REST_Response( $response, 200 );
			}
		}

		$route = nl_proposal_resolve_commercial_rfp_route( (int) $payload['project_id'] );
		if ( is_wp_error( $route ) ) {
			return $route;
		}

		if ( ! is_array( $existing ) ) {
			$case_id = nl_proposal_generate_commercial_rfp_case_id();
			if ( is_wp_error( $case_id ) ) {
				return nl_proposal_rfp_error( 'request_unavailable', 'The request service is temporarily unavailable.', 503 );
			}
			$created_at = time();
			$existing   = array(
				'record_token' => $case_id,
				'signature'    => $signature,
				'state'        => 'reserved',
				'case_id'      => $case_id,
				'post_id'      => 0,
				'route_kind'   => $route['kind'],
				'sla_hours'    => (int) $route['sla_hours'],
				'created_at'   => $created_at,
				'expires_at'   => $created_at + DAY_IN_SECONDS,
				'response'     => null,
			);
			if ( ! nl_proposal_write_commercial_rfp_idempotency_record( $idempotency['hash'], $existing, true ) ) {
				return nl_proposal_rfp_error( 'request_unavailable', 'The request service is temporarily unavailable.', 503 );
			}
			if ( ! wp_next_scheduled(
				'nl_proposal_delete_commercial_rfp_idempotency_record',
				array( $idempotency['hash'], $existing['record_token'] )
			) ) {
				wp_schedule_single_event(
					(int) $existing['expires_at'],
					'nl_proposal_delete_commercial_rfp_idempotency_record',
					array( $idempotency['hash'], $existing['record_token'] )
				);
			}
		}
		$case_id = (string) $existing['case_id'];

		$post_id = isset( $existing['post_id'] ) ? (int) $existing['post_id'] : 0;
		$post    = $post_id ? get_post( $post_id ) : null;
		if ( ! $post || 'nl_commercial_rfp' !== $post->post_type ) {
			$post_id = nl_proposal_store_commercial_rfp_case(
				$case_id,
				$payload,
				$route,
				array(
					'hash'       => $idempotency['hash'],
					'signature'  => $signature,
					'created_at' => (int) $existing['created_at'],
				)
			);
			if ( is_wp_error( $post_id ) ) {
				do_action(
					'nl_proposal_commercial_rfp_storage_attention',
					array(
						'project_id' => (int) $payload['project_id'],
						'error_code' => $post_id->get_error_code(),
					)
				);
				return nl_proposal_rfp_error( 'request_unavailable', 'The request service is temporarily unavailable.', 503 );
			}
			$existing['post_id'] = (int) $post_id;
			$existing['state']   = 'stored';
			if ( ! nl_proposal_write_commercial_rfp_idempotency_record( $idempotency['hash'], $existing ) ) {
				return nl_proposal_rfp_error( 'request_unavailable', 'The request was stored but its replay record is unavailable.', 503 );
			}
		}

		$stored_delivery_state = (string) get_post_meta( $post_id, '_nl_rfp_delivery_status', true );
		if ( 'routed' === $stored_delivery_state ) {
			$delivery_state = 'routed';
		} elseif ( in_array( $stored_delivery_state, array( 'delivery_pending', 'dead_letter' ), true ) ) {
			$delivery_state = 'processing';
		} else {
			$delivery = nl_proposal_dispatch_commercial_rfp_case( $post_id, $route );
			if ( is_wp_error( $delivery ) ) {
				nl_proposal_schedule_commercial_rfp_retry( $post_id );
				$delivery_state = 'processing';
			} else {
				$delivery_state = 'routed';
				$route          = array_merge( $route, $delivery );
			}
		}

		$received_at = (int) get_post_meta( $post_id, '_nl_rfp_received_at', true );
		$sla_due_at  = (int) get_post_meta( $post_id, '_nl_rfp_sla_due_at', true );
		$response    = array(
			'accepted'          => true,
			'case_id'           => $case_id,
			'status'            => 'received',
			'delivery_state'    => $delivery_state,
			'received_at'       => gmdate( 'c', $received_at ),
			'response_due_at'   => gmdate( 'c', $sla_due_at ),
			'sla_hours'         => (int) $route['sla_hours'],
			'route_kind'        => $route['kind'],
			'idempotent_replay' => $record_was_present,
		);
		$existing['state']    = 'complete';
		$existing['post_id']  = (int) $post_id;
		$existing['response'] = $response;
		if ( ! nl_proposal_write_commercial_rfp_idempotency_record( $idempotency['hash'], $existing ) ) {
			return nl_proposal_rfp_error( 'request_unavailable', 'The request was stored but its replay record is unavailable.', 503 );
		}

		/**
		 * The only analytics event. It deliberately excludes case ID, company,
		 * contact, IP/fingerprint, free text, page path and requested values.
		 */
		do_action(
			'nl_proposal_commercial_rfp_analytics_safe',
			array(
				'project_id'     => (int) $payload['project_id'],
				'has_floor'      => null !== $payload['asset']['floor_id'],
				'has_suite'      => null !== $payload['asset']['suite_id'],
				'question_count' => count( $payload['question_ids'] ),
				'document_count' => count( $payload['document_ids'] ),
				'locale'         => $payload['locale'],
				'route_kind'     => $route['kind'],
				'delivery_state' => $delivery_state,
			)
		);

		return new WP_REST_Response( $response, $record_was_present ? 200 : 202 );
	} finally {
		nl_proposal_release_commercial_rfp_lock( $idempotency['hash'], $lock_token );
	}
}

/**
 * Handle the isolated sandbox route without storage, delivery, CRM hooks,
 * project routes, fallback mailboxes or production analytics.
 *
 * Only an HMAC signature and synthetic response are placed in the durable
 * idempotency record. The normalized buyer payload remains request-local.
 */
function nl_proposal_handle_commercial_rfp_sandbox_request( $request ) {
	$idempotency = nl_proposal_get_commercial_rfp_idempotency( $request );
	if ( is_wp_error( $idempotency ) ) {
		return $idempotency;
	}
	$raw_payload = $request->get_json_params();
	$payload = nl_proposal_normalize_commercial_rfp_payload( $raw_payload );
	if ( is_wp_error( $payload ) ) {
		return $payload;
	}
	if ( 'test' !== $payload['environment'] || null === $payload['sandbox_post_id'] ) {
		return nl_proposal_rfp_error( 'sandbox_rejected', 'The sandbox request was not accepted.', 403 );
	}
	$signature = nl_proposal_commercial_rfp_request_signature( $raw_payload, 'sandbox-test' );
	if ( is_wp_error( $signature ) ) {
		return $signature;
	}
	$record_hash = hash( 'sha256', 'sandbox-test|' . (int) $payload['sandbox_post_id'] . '|' . $idempotency['hash'] );
	$lock_token = nl_proposal_acquire_commercial_rfp_lock( $record_hash );
	if ( false === $lock_token ) {
		return nl_proposal_rfp_error( 'request_in_progress', 'An identical request is already being processed.', 409 );
	}
	try {
		$existing = nl_proposal_get_commercial_rfp_idempotency_record( $record_hash );
		if ( is_array( $existing ) && (int) $existing['expires_at'] <= time() ) {
			delete_option( nl_proposal_commercial_rfp_idempotency_option_name( $record_hash ) );
			$existing = null;
		}
		if ( is_array( $existing ) ) {
			if ( ! isset( $existing['signature'] ) || ! hash_equals( (string) $existing['signature'], $signature ) ) {
				return nl_proposal_rfp_error( 'idempotency_conflict', 'The Idempotency-Key was already used for a different request.', 409 );
			}
			$response = isset( $existing['response'] ) && is_array( $existing['response'] ) ? $existing['response'] : array();
			if ( ! empty( $response ) ) {
				$response['idempotent_replay'] = true;
				return new WP_REST_Response( $response, 200 );
			}
		}

		$created_at = time();
		$case_id = 'TEST-' . strtoupper(
			substr(
				hash_hmac( 'sha256', $record_hash . '|' . $signature, wp_salt( 'secure_auth' ) ),
				0,
				20
			)
		);
		$response = array(
			'accepted'          => true,
			'case_id'           => $case_id,
			'status'            => 'received',
			'environment'       => 'test',
			'delivery_state'    => 'test_sink',
			'route_kind'        => 'test_sink',
			'route_status'      => 'test_sink',
			'recipient_label'   => 'Sandbox test sink — no message delivered',
			'received_at'       => gmdate( 'c', $created_at ),
			'response_due_at'   => gmdate( 'c', $created_at ),
			'sla_hours'         => 0,
			'idempotent_replay' => false,
		);
		$record = array(
			'record_token' => $case_id,
			'signature'    => $signature,
			'state'        => 'complete',
			'case_id'      => $case_id,
			'post_id'      => 0,
			'route_kind'   => 'test_sink',
			'sla_hours'    => 0,
			'created_at'   => $created_at,
			'expires_at'   => $created_at + DAY_IN_SECONDS,
			'response'     => $response,
		);
		if ( ! nl_proposal_write_commercial_rfp_idempotency_record( $record_hash, $record, true ) ) {
			return nl_proposal_rfp_error( 'request_unavailable', 'The sandbox request service is temporarily unavailable.', 503 );
		}
		if ( ! wp_next_scheduled( 'nl_proposal_delete_commercial_rfp_idempotency_record', array( $record_hash, $case_id ) ) ) {
			wp_schedule_single_event(
				(int) $record['expires_at'],
				'nl_proposal_delete_commercial_rfp_idempotency_record',
				array( $record_hash, $case_id )
			);
		}
		return new WP_REST_Response( $response, 202 );
	} finally {
		nl_proposal_release_commercial_rfp_lock( $record_hash, $lock_token );
	}
}

/**
 * Register the proposal endpoint.
 *
 * @return void
 */
function nl_proposal_register_commercial_rfp_rest_route() {
	register_rest_route(
		'nadlan/v2',
		'/commercial-rfp',
		array(
			'methods'             => WP_REST_Server::CREATABLE,
			'callback'            => 'nl_proposal_handle_commercial_rfp_request',
			'permission_callback' => 'nl_proposal_commercial_rfp_permission_check',
		)
	);
	register_rest_route(
		'nadlan/v2',
		'/commercial-rfp-sandbox',
		array(
			'methods'             => WP_REST_Server::CREATABLE,
			'callback'            => 'nl_proposal_handle_commercial_rfp_sandbox_request',
			'permission_callback' => 'nl_proposal_commercial_rfp_sandbox_permission_check',
		)
	);
}

/**
 * Export encrypted cases that match a privacy request email.
 *
 * @param string $email_address Email.
 * @param int    $page Page.
 * @return array
 */
function nl_proposal_commercial_rfp_privacy_exporter( $email_address, $page = 1 ) {
	$email = sanitize_email( $email_address );
	if ( '' === $email || ! is_email( $email ) ) {
		return array( 'data' => array(), 'done' => true );
	}

	$query = new WP_Query(
		array(
			'post_type'      => 'nl_commercial_rfp',
			'post_status'    => 'private',
			'posts_per_page' => 50,
			'paged'          => max( 1, (int) $page ),
			'fields'         => 'ids',
			'orderby'        => 'ID',
			'order'          => 'ASC',
		)
	);

	$data = array();
	foreach ( $query->posts as $post_id ) {
		$payload = nl_proposal_decrypt_commercial_rfp_payload( get_post_meta( $post_id, '_nl_rfp_payload_v1', true ) );
		if ( is_wp_error( $payload ) || empty( $payload['contact']['email'] ) || 0 !== strcasecmp( $payload['contact']['email'], $email ) ) {
			continue;
		}

		$data[] = array(
			'group_id'    => 'nl-commercial-rfp',
			'group_label' => 'Commercial property requests',
			'item_id'     => 'nl-commercial-rfp-' . (int) $post_id,
			'data'        => array(
				array( 'name' => 'Case ID', 'value' => get_post_meta( $post_id, '_nl_rfp_case_id', true ) ),
				array( 'name' => 'Project ID', 'value' => $payload['project_id'] ),
				array( 'name' => 'Selected asset', 'value' => wp_json_encode( $payload['asset'] ) ),
				array( 'name' => 'Company', 'value' => wp_json_encode( $payload['company'], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) ),
				array( 'name' => 'Contact', 'value' => wp_json_encode( $payload['contact'], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) ),
				array( 'name' => 'Requirements', 'value' => wp_json_encode( $payload['requirements'], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) ),
				array( 'name' => 'Questions', 'value' => implode( ', ', $payload['question_ids'] ) ),
				array( 'name' => 'Documents', 'value' => implode( ', ', $payload['document_ids'] ) ),
				array( 'name' => 'Written request', 'value' => $payload['question_text'] ),
				array( 'name' => 'Consent', 'value' => wp_json_encode( $payload['consent'] ) ),
			),
		);
	}

	return array(
		'data' => $data,
		'done' => $query->max_num_pages <= max( 1, (int) $page ),
	);
}

/**
 * Erase expired or user-requested cases matching an email.
 *
 * @param string $email_address Email.
 * @param int    $page Page.
 * @return array
 */
function nl_proposal_commercial_rfp_privacy_eraser( $email_address, $page = 1 ) {
	$email = sanitize_email( $email_address );
	if ( '' === $email || ! is_email( $email ) ) {
		return array(
			'items_removed'  => false,
			'items_retained' => false,
			'messages'       => array(),
			'done'           => true,
		);
	}

	$query = new WP_Query(
		array(
			'post_type'      => 'nl_commercial_rfp',
			'post_status'    => 'private',
			'posts_per_page' => 50,
			'paged'          => max( 1, (int) $page ),
			'fields'         => 'ids',
			'orderby'        => 'ID',
			'order'          => 'ASC',
		)
	);

	$removed = false;
	foreach ( $query->posts as $post_id ) {
		$payload = nl_proposal_decrypt_commercial_rfp_payload( get_post_meta( $post_id, '_nl_rfp_payload_v1', true ) );
		if ( is_wp_error( $payload ) || empty( $payload['contact']['email'] ) || 0 !== strcasecmp( $payload['contact']['email'], $email ) ) {
			continue;
		}
		delete_post_meta( $post_id, '_nl_rfp_payload_v1' );
		update_post_meta( $post_id, '_nl_rfp_case_status', 'privacy_erased' );
		update_post_meta( $post_id, '_nl_rfp_delivery_status', 'privacy_erased' );
		update_post_meta( $post_id, '_nl_rfp_privacy_erased_at', time() );
		wp_clear_scheduled_hook( 'nl_proposal_retry_commercial_rfp_case', array( (int) $post_id ) );
		wp_clear_scheduled_hook( 'nl_proposal_check_commercial_rfp_sla', array( (int) $post_id ) );
		$removed = true;
	}

	return array(
		'items_removed'  => $removed,
		'items_retained' => false,
		'messages'       => array(),
		'done'           => $query->max_num_pages <= max( 1, (int) $page ),
	);
}

/**
 * Register the privacy exporter.
 *
 * @param array $exporters Existing exporters.
 * @return array
 */
function nl_proposal_register_commercial_rfp_privacy_exporter( $exporters ) {
	$exporters['nl-commercial-rfp'] = array(
		'exporter_friendly_name' => 'Commercial property requests',
		'callback'               => 'nl_proposal_commercial_rfp_privacy_exporter',
	);
	return $exporters;
}

/**
 * Register the privacy eraser.
 *
 * @param array $erasers Existing erasers.
 * @return array
 */
function nl_proposal_register_commercial_rfp_privacy_eraser( $erasers ) {
	$erasers['nl-commercial-rfp'] = array(
		'eraser_friendly_name' => 'Commercial property requests',
		'callback'             => 'nl_proposal_commercial_rfp_privacy_eraser',
	);
	return $erasers;
}

add_action( 'init', 'nl_proposal_register_commercial_rfp_post_type', 5 );
add_action( 'rest_api_init', 'nl_proposal_register_commercial_rfp_rest_route' );
add_action( 'nl_proposal_retry_commercial_rfp_case', 'nl_proposal_retry_commercial_rfp_case' );
add_action( 'nl_proposal_delete_commercial_rfp_case', 'nl_proposal_delete_commercial_rfp_case' );
add_action( 'nl_proposal_check_commercial_rfp_sla', 'nl_proposal_check_commercial_rfp_sla' );
add_action(
	'nl_proposal_delete_commercial_rfp_idempotency_record',
	'nl_proposal_delete_commercial_rfp_idempotency_record',
	10,
	2
);
add_filter( 'wp_privacy_personal_data_exporters', 'nl_proposal_register_commercial_rfp_privacy_exporter' );
add_filter( 'wp_privacy_personal_data_erasers', 'nl_proposal_register_commercial_rfp_privacy_eraser' );
