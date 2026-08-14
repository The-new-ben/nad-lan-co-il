<?php
/**
 * PROPOSAL ONLY — NOT APPLIED.
 * Dependency-free executable fixture for commercial-data-contract.php.
 * Run: php commercial-data-contract.fixture.test.php
 */

define( 'ABSPATH', __DIR__ . DIRECTORY_SEPARATOR );
define( 'DAY_IN_SECONDS', 86400 );

class WP_Error {
	private $code;
	private $message;
	private $data;
	public function __construct( $code = '', $message = '', $data = null ) {
		$this->code = $code;
		$this->message = $message;
		$this->data = $data;
	}
	public function get_error_code() { return $this->code; }
	public function get_error_message() { return $this->message; }
	public function get_error_data() { return $this->data; }
	public function add_data( $data ) { $this->data = $data; }
}
function is_wp_error( $value ) { return $value instanceof WP_Error; }
function wp_parse_args( $args, $defaults = array() ) { return array_merge( $defaults, is_array( $args ) ? $args : array() ); }
function sanitize_key( $value ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $value ) ); }
function sanitize_text_field( $value ) { return trim( preg_replace( '/[\r\n\t ]+/', ' ', strip_tags( (string) $value ) ) ); }
function sanitize_textarea_field( $value ) { return trim( strip_tags( (string) $value ) ); }
function esc_url_raw( $value, $protocols = null ) {
	$url = filter_var( (string) $value, FILTER_VALIDATE_URL );
	if ( false === $url ) return '';
	$scheme = strtolower( (string) parse_url( $url, PHP_URL_SCHEME ) );
	return is_array( $protocols ) && ! in_array( $scheme, $protocols, true ) ? '' : $url;
}
function wp_parse_url( $value, $component = -1 ) { return parse_url( $value, $component ); }
function home_url( $path = '/' ) { return 'https://nad-lan.co.il' . ( '/' === $path ? '/' : $path ); }
function get_permalink( $post_id ) {
	$map = array(
		999999 => 'https://nad-lan.co.il/projects/fixture-commercial-project/',
		6213   => 'https://nad-lan.co.il/projects/toha-tel-aviv/',
		6182   => 'https://nad-lan.co.il/projects/the-park-bnei-brak/',
	);
	return isset( $map[ (int) $post_id ] ) ? $map[ (int) $post_id ] : false;
}
function add_query_arg( $params, $url ) {
	$parts = parse_url( $url );
	$query = array();
	if ( ! empty( $parts['query'] ) ) parse_str( $parts['query'], $query );
	$query = array_merge( $query, $params );
	$base = $parts['scheme'] . '://' . $parts['host'] . ( isset( $parts['path'] ) ? $parts['path'] : '' );
	return $base . '?' . http_build_query( $query, '', '&', PHP_QUERY_RFC3986 ) . ( isset( $parts['fragment'] ) ? '#' . $parts['fragment'] : '' );
}
function apply_filters( $tag, $value ) { return $value; }
function absint( $value ) { return abs( (int) $value ); }

require __DIR__ . '/commercial-data-contract.php';

function fixture_assert( $condition, $message ) {
	if ( ! $condition ) {
		fwrite( STDERR, "FAIL: {$message}\n" );
		exit( 1 );
	}
}
function fixture_assert_not_error( $value, $message ) {
	if ( is_wp_error( $value ) ) {
		fwrite( STDERR, "FAIL: {$message}: {$value->get_error_code()} {$value->get_error_message()}\n" );
		exit( 1 );
	}
	return $value;
}

$fixture_now          = time();
$fixture_effective_at = gmdate( 'Y-m-d\TH:i:s\Z', $fixture_now - 7200 );
$fixture_retrieved_at = gmdate( 'Y-m-d\TH:i:s\Z', $fixture_now - 5400 );
$fixture_verified_at  = gmdate( 'Y-m-d\TH:i:s\Z', $fixture_now - 3600 );
$fixture_expires_at   = gmdate( 'Y-m-d\TH:i:s\Z', $fixture_now + 21600 );

function fixture_source( $id ) {
	global $fixture_effective_at, $fixture_retrieved_at;
	return array(
		'type'         => 'owner_crm',
		'label'        => 'Fixture source ' . $id,
		'uri'          => 'https://example.invalid/evidence/' . $id,
		'document_id'  => $id,
		'revision'     => 'fixture-v1',
		'published_at' => $fixture_effective_at,
		'retrieved_at' => $fixture_retrieved_at,
	);
}
function fixture_owner() {
	return array(
		'team'             => 'Fixture data',
		'accountable_role' => 'Fixture steward',
		'contact_ref'      => 'fixture-steward',
	);
}
function fixture_positive( $state, $value, $unit, $id ) {
	global $fixture_effective_at, $fixture_verified_at, $fixture_expires_at;
	return array(
		'state'                 => $state,
		'value'                 => $value,
		'unit'                  => $unit,
		'scope'                 => 'fixture scope ' . $id,
		'effective_at'          => $fixture_effective_at,
		'sources'               => array( fixture_source( $id ) ),
		'observations'          => array(),
		'verified_at'           => 'verified' === $state ? $fixture_verified_at : null,
		'expires_at'            => $fixture_expires_at,
		'owner'                 => fixture_owner(),
		'confidence'            => 'verified' === $state ? 'high' : 'medium',
		'reason'                => '',
		'applicability'         => array( 'commercial', $id ),
		'conflict_ids'          => array(),
		'note'                  => 'Fixture note ' . $id,
		'caveat'                => 'source_estimate' === $state ? 'Fixture estimate caveat.' : '',
		'required_document_ids' => array(),
		'decision_grade'        => 'verified' === $state,
	);
}
function fixture_verified( $value, $unit, $id ) { return fixture_positive( 'verified', $value, $unit, $id ); }
function fixture_estimate( $value, $unit, $id ) { return fixture_positive( 'source_estimate', $value, $unit, $id ); }
function fixture_unknown( $reason, $documents, $id ) {
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
		'owner'                 => null,
		'confidence'            => 'unknown',
		'reason'                => $reason,
		'applicability'         => array( $id ),
		'conflict_ids'          => array(),
		'note'                  => 'Unknown note remains separate.',
		'caveat'                => 'Unknown caveat remains separate.',
		'required_document_ids' => $documents,
		'decision_grade'        => false,
	);
}
function fixture_contradictory( $first, $second, $unit, $id ) {
	global $fixture_effective_at;
	$first_id  = $id . '-a';
	$second_id = $id . '-b';
	return array(
		'state'                 => 'contradictory',
		'value'                 => null,
		'unit'                  => $unit,
		'scope'                 => 'fixture contradiction scope ' . $id,
		'effective_at'          => $fixture_effective_at,
		'sources'               => array(),
		'observations'          => array(
			array( 'observation_id' => $first_id, 'value' => $first, 'scope' => 'A', 'source' => fixture_source( $first_id ) ),
			array( 'observation_id' => $second_id, 'value' => $second, 'scope' => 'B', 'source' => fixture_source( $second_id ) ),
		),
		'verified_at'           => null,
		'expires_at'            => null,
		'owner'                 => fixture_owner(),
		'confidence'            => 'medium',
		'reason'                => '',
		'applicability'         => array( 'commercial', $id ),
		'conflict_ids'          => array( $first_id, $second_id ),
		'note'                  => 'Contradiction note.',
		'caveat'                => 'Do not choose either observation.',
		'required_document_ids' => array( 'measurement_report' ),
		'decision_grade'        => false,
	);
}

// Exact first-class envelope fields and the reason/caveat separation.
$verified_roundtrip = fixture_assert_not_error(
	nl_proposal_normalize_evidence_envelope( fixture_verified( 42, 'sqm', 'roundtrip-verified' ), 'decimal', array( 'now' => $fixture_now ) ),
	'verified envelope'
);
fixture_assert( 'fixture scope roundtrip-verified' === $verified_roundtrip['scope'], 'verified scope survives' );
fixture_assert( 'high' === $verified_roundtrip['confidence'], 'confidence is not derived from state' );
fixture_assert( '' === $verified_roundtrip['reason'], 'positive reason remains empty' );
$estimate_roundtrip = fixture_assert_not_error(
	nl_proposal_normalize_evidence_envelope( fixture_estimate( 42, 'sqm', 'roundtrip-estimate' ), 'decimal', array( 'now' => $fixture_now ) ),
	'estimate envelope'
);
fixture_assert( 'source_estimate' === $estimate_roundtrip['state'] && 'medium' === $estimate_roundtrip['confidence'], 'estimate survives exactly' );
$unknown_roundtrip = fixture_assert_not_error(
	nl_proposal_normalize_evidence_envelope( fixture_unknown( 'Explicit missing reason.', array( 'orientation_plan' ), 'roundtrip-unknown' ), 'string', array( 'now' => $fixture_now ) ),
	'unknown envelope'
);
fixture_assert( 'Explicit missing reason.' === $unknown_roundtrip['reason'], 'unknown reason survives separately' );
fixture_assert( 'Unknown caveat remains separate.' === $unknown_roundtrip['caveat'], 'unknown caveat is not promoted to reason' );
$contradiction_roundtrip = fixture_assert_not_error(
	nl_proposal_normalize_evidence_envelope( fixture_contradictory( 10, 11, 'levels', 'roundtrip-conflict' ), 'integer', array( 'now' => $fixture_now ) ),
	'contradictory envelope'
);
fixture_assert( array( 'roundtrip-conflict-a', 'roundtrip-conflict-b' ) === $contradiction_roundtrip['conflict_ids'], 'conflict IDs survive exactly' );
$expired = fixture_estimate( 1, null, 'expired' );
$expired['expires_at'] = gmdate( 'Y-m-d\TH:i:s\Z', $fixture_now - 1 );
fixture_assert( is_wp_error( nl_proposal_normalize_evidence_envelope( $expired, 'integer', array( 'now' => $fixture_now ) ) ), 'expired claim is rejected server-side' );

// Every non-unknown business status survives only inside verified current
// availability evidence. Unknown is the null-evidence presentation state.
foreach ( nl_proposal_commercial_statuses() as $status ) {
	if ( 'unknown' === $status ) {
		continue;
	}
	$normalized_status = fixture_assert_not_error(
		nl_proposal_normalize_commercial_availability(
			fixture_verified( $status, null, 'status-' . $status ),
			array( 'now' => $fixture_now )
		),
		'availability status ' . $status
	);
	fixture_assert( 'verified' === $normalized_status['state'] && $status === $normalized_status['value'], 'status survives exactly: ' . $status );
}
$unknown_availability = fixture_assert_not_error(
	nl_proposal_normalize_commercial_availability( null, array( 'now' => $fixture_now ) ),
	'unknown availability'
);
fixture_assert( 'unknown' === $unknown_availability['state'] && null === $unknown_availability['value'], 'unknown availability remains a null evidence value' );
$unknown_sentinel = fixture_assert_not_error(
	nl_proposal_normalize_commercial_availability(
		fixture_verified( 'unknown', null, 'status-unknown-sentinel' ),
		array( 'now' => $fixture_now )
	),
	'unknown ingestion sentinel'
);
fixture_assert( 'unknown' === $unknown_sentinel['state'] && null === $unknown_sentinel['value'], 'verified unknown sentinel is demoted to null unknown evidence' );

$anchor = array( 'lng' => 34.8, 'lat' => 32.1 ); // Reverse key order must still normalize.
$specs = array(
	array( 'id' => 'north', 'direction' => 'N', 'start' => 315, 'end' => 45, 'coordinate' => array( 'lat' => 32.104, 'lng' => 34.8 ) ),
	array( 'id' => 'east', 'direction' => 'E', 'start' => 45, 'end' => 135, 'coordinate' => array( 'lat' => 32.1, 'lng' => 34.805 ) ),
	array( 'id' => 'south', 'direction' => 'S', 'start' => 135, 'end' => 225, 'coordinate' => array( 'lat' => 32.096, 'lng' => 34.8 ) ),
	array( 'id' => 'west', 'direction' => 'W', 'start' => 225, 'end' => 315, 'coordinate' => array( 'lat' => 32.1, 'lng' => 34.795 ) ),
);
function fixture_facade( $spec ) {
	return array(
		'exposure_id'       => $spec['id'],
		'direction'         => fixture_verified( $spec['direction'], null, $spec['id'] . '-direction' ),
		'azimuth_start_deg' => fixture_verified( $spec['start'], 'degrees_true_north', $spec['id'] . '-start' ),
		'azimuth_end_deg'   => fixture_verified( $spec['end'], 'degrees_true_north', $spec['id'] . '-end' ),
		'facade_share_pct'  => fixture_estimate( 25, 'percent', $spec['id'] . '-share' ),
		'view_context'      => fixture_unknown( 'No view study.', array( 'view_study' ), $spec['id'] . '-view' ),
		'obstructions'      => fixture_unknown( 'No obstruction study.', array( 'view_study' ), $spec['id'] . '-obstruction' ),
	);
}
function fixture_beam_association( $spec, $anchor ) {
	$metrics = nl_proposal_beam_geodesic_metrics( $anchor, $spec['coordinate'] );
	$id = $spec['id'] . '-landmark';
	return array(
		'exposure_id' => $spec['id'],
		'landmarks'   => array(
			array(
				'landmark_id'     => $id,
				'exposure_id'     => $spec['id'],
				'label'           => fixture_verified( $spec['direction'] . ' landmark with complete sourced name', null, $id . '-label' ),
				'compact_label'   => fixture_verified( $spec['direction'] . ' mark', null, $id . '-compact-label' ),
				'coordinates'     => fixture_verified( $spec['coordinate'], null, $id . '-coordinate' ),
				'distance_m'      => fixture_verified( round( $metrics['distance_m'] ), 'metres_ground', $id . '-distance' ),
				'distance_method' => fixture_verified( 'straight_line_geodesic', null, $id . '-method' ),
				'bearing_deg'     => fixture_verified( $metrics['bearing_deg'], 'degrees_true_north', $id . '-bearing' ),
				'caveat'         => 'North-up schematic; not a surveyed sightline.',
			),
		),
	);
}
$facades = array_map( 'fixture_facade', $specs );
$normalized_facades = fixture_assert_not_error(
	nl_proposal_normalize_commercial_exposures( $facades, array( 'now' => $fixture_now ) ),
	'four facade exposures'
);
$raw_beam = array(
	'project_anchor'      => fixture_verified( $anchor, null, 'project-anchor' ),
	'exposures'           => array_map(
		function ( $spec ) use ( $anchor ) { return fixture_beam_association( $spec, $anchor ); },
		$specs
	),
	'illustrative_caveat' => 'Evidenced coordinates; illustrative north-up schematic.',
);
$beam = fixture_assert_not_error(
	nl_proposal_normalize_commercial_beam_scene( $raw_beam, array( 'now' => $fixture_now, 'facade_exposures' => $normalized_facades ) ),
	'four-exposure beam scene'
);
fixture_assert( 'ready' === $beam['scene_state'], 'beam scene is ready' );
fixture_assert( 4 === count( $beam['exposures'] ), 'four facade claims remain four beam associations' );
fixture_assert( array( 'lat' => 32.1, 'lng' => 34.8 ) === $beam['project_anchor']['value'], 'coordinate normalization is key-order independent' );
fixture_assert( 'N mark' === $beam['exposures'][0]['landmarks'][0]['compact_label']['value'], 'compact label remains separate from the full label' );

function fixture_assert_neutral_compact_label_scene( $raw, $facades, $now, $message ) {
	$scene = fixture_assert_not_error(
		nl_proposal_normalize_commercial_beam_scene( $raw, array( 'now' => $now, 'facade_exposures' => $facades ) ),
		$message
	);
	fixture_assert( 'unknown' === $scene['scene_state'], $message . ' is neutral' );
	fixture_assert( 0 === count( $scene['exposures'] ), $message . ' exposes zero cones or landmarks' );
}

// The fixed scene has a separately sourced display label bounded by Unicode
// code points. The complete name may use the general 1000-code-point evidence
// allowance; neither server nor browser is permitted to truncate either value.
$compact_boundary = $raw_beam;
$compact_boundary['exposures'][0]['landmarks'][0]['compact_label'] = fixture_estimate( 'אבגדהוזחטיכל', null, 'compact-boundary-12' );
$compact_boundary_scene = fixture_assert_not_error(
	nl_proposal_normalize_commercial_beam_scene( $compact_boundary, array( 'now' => $fixture_now, 'facade_exposures' => $normalized_facades ) ),
	'12-code-point source estimate compact label'
);
fixture_assert( 'ready' === $compact_boundary_scene['scene_state'], '12 Unicode code points and a current source estimate are accepted exactly' );
fixture_assert( 'אבגדהוזחטיכל' === $compact_boundary_scene['exposures'][0]['landmarks'][0]['compact_label']['value'], '12-code-point compact label is not rewritten' );

$overlong_compact = $raw_beam;
$overlong_compact['exposures'][0]['landmarks'][0]['label']['value'] = str_repeat( 'ל', 1000 );
$overlong_compact['exposures'][0]['landmarks'][0]['compact_label']['value'] = str_repeat( 'מ', 13 );
fixture_assert_neutral_compact_label_scene( $overlong_compact, $normalized_facades, $fixture_now, '1000-code-point full label with overlong compact label' );

$missing_compact = $raw_beam;
unset( $missing_compact['exposures'][0]['landmarks'][0]['compact_label'] );
fixture_assert_neutral_compact_label_scene( $missing_compact, $normalized_facades, $fixture_now, 'missing compact label' );

$malformed_compact = $raw_beam;
$malformed_compact['exposures'][0]['landmarks'][0]['compact_label'] = 'bare compact label';
fixture_assert_neutral_compact_label_scene( $malformed_compact, $normalized_facades, $fixture_now, 'malformed compact label evidence' );

$unknown_compact = $raw_beam;
$unknown_compact['exposures'][0]['landmarks'][0]['compact_label'] = fixture_unknown( 'Compact name not confirmed.', array( 'orientation_plan' ), 'compact-unknown' );
fixture_assert_neutral_compact_label_scene( $unknown_compact, $normalized_facades, $fixture_now, 'unknown compact label' );

$expired_compact = $raw_beam;
$expired_compact['exposures'][0]['landmarks'][0]['compact_label']['expires_at'] = gmdate( 'Y-m-d\TH:i:s\Z', $fixture_now - 1 );
fixture_assert_neutral_compact_label_scene( $expired_compact, $normalized_facades, $fixture_now, 'expired compact label' );

$contradictory_compact = $raw_beam;
$contradictory_compact['exposures'][0]['landmarks'][0]['compact_label'] = fixture_contradictory( 'North mark', 'North hub', null, 'compact-conflict' );
fixture_assert_neutral_compact_label_scene( $contradictory_compact, $normalized_facades, $fixture_now, 'contradictory compact label' );

$invalid_utf8_compact = $raw_beam;
$invalid_utf8_compact['exposures'][0]['landmarks'][0]['compact_label']['value'] = "\xC3\x28";
fixture_assert_neutral_compact_label_scene( $invalid_utf8_compact, $normalized_facades, $fixture_now, 'invalid UTF-8 compact label' );

$duplicate = $raw_beam;
$duplicate['exposures'][] = $duplicate['exposures'][0];
fixture_assert( is_wp_error( nl_proposal_normalize_commercial_beam_scene( $duplicate, array( 'now' => $fixture_now, 'facade_exposures' => $normalized_facades ) ) ), 'duplicate exposure ID is rejected' );
$unknown_association = $raw_beam;
$unknown_association['exposures'][0]['exposure_id'] = 'unknown-exposure';
fixture_assert( is_wp_error( nl_proposal_normalize_commercial_beam_scene( $unknown_association, array( 'now' => $fixture_now, 'facade_exposures' => $normalized_facades ) ) ), 'unknown exposure ID is rejected' );
$missing_association = $raw_beam;
array_pop( $missing_association['exposures'] );
$missing_scene = fixture_assert_not_error(
	nl_proposal_normalize_commercial_beam_scene( $missing_association, array( 'now' => $fixture_now, 'facade_exposures' => $normalized_facades ) ),
	'missing association neutral state'
);
fixture_assert( 'unknown' === $missing_scene['scene_state'] && 0 === count( $missing_scene['exposures'] ), 'missing association fails the whole scene closed' );
$mismatched_landmark = $raw_beam;
$mismatched_landmark['exposures'][0]['landmarks'][0]['exposure_id'] = 'east';
fixture_assert( is_wp_error( nl_proposal_normalize_commercial_beam_scene( $mismatched_landmark, array( 'now' => $fixture_now, 'facade_exposures' => $normalized_facades ) ) ), 'landmark association mismatch is rejected' );
$out_of_sector = $raw_beam;
$out_of_sector['exposures'][0]['landmarks'][0]['bearing_deg']['value'] = 180;
$out_scene = fixture_assert_not_error(
	nl_proposal_normalize_commercial_beam_scene( $out_of_sector, array( 'now' => $fixture_now, 'facade_exposures' => $normalized_facades ) ),
	'out-of-sector neutral state'
);
fixture_assert( 'unknown' === $out_scene['scene_state'] && 0 === count( $out_scene['exposures'] ), 'out-of-sector landmark suppresses every cone' );

// Project/tower identity: repeated visible floor IDs remain distinct through
// composite identities and shareable URLs; suite identity must match parent.
$towers = array(
	array( 'building_id' => 'building-main', 'tower_id' => 'tower-a', 'display_label' => fixture_verified( 'Tower A', null, 'tower-a-label' ) ),
	array( 'building_id' => 'building-main', 'tower_id' => 'tower-b', 'display_label' => fixture_verified( 'Tower B', null, 'tower-b-label' ) ),
);
function fixture_floor( $tower_id, $label, $facades = array(), $beam = null ) {
	$prefix = $tower_id . '-level-10';
	return array(
		'building_id'           => 'building-main',
		'tower_id'              => $tower_id,
		'floor_id'              => 'level-10',
		'legal_floor_label'     => fixture_verified( 'Legal 10', null, $prefix . '-legal' ),
		'elevator_label'        => fixture_verified( '10', null, $prefix . '-elevator' ),
		'marketing_label'       => fixture_verified( $label, null, $prefix . '-marketing' ),
		'zone'                  => fixture_verified( 'Core', null, $prefix . '-zone' ),
		'availability'          => fixture_verified( 'verified_available', null, $prefix . '-availability' ),
		'gross_rentable_sqm'    => fixture_verified( 1000, 'sqm_rentable_gross', $prefix . '-gross' ),
		'usable_sqm'            => fixture_estimate( 800, 'sqm_usable', $prefix . '-usable' ),
		'exposures'             => $facades,
		'beam_scene'            => $beam,
		'suites'                => array(
			array(
				'building_id'       => 'building-main',
				'tower_id'          => $tower_id,
				'floor_id'          => 'level-10',
				'suite_id'          => 'suite-1',
				'label'             => fixture_verified( 'Suite 1', null, $prefix . '-suite-label' ),
				'availability'      => fixture_verified( 'verified_available', null, $prefix . '-suite-availability' ),
				'gross_rentable_sqm'=> fixture_verified( 500, 'sqm_rentable_gross', $prefix . '-suite-gross' ),
				'usable_sqm'        => fixture_estimate( 400, 'sqm_usable', $prefix . '-suite-usable' ),
			),
		),
	);
}
$project_raw = array(
	'project_id'          => 'fixture-commercial-project',
	'wp_post_id'          => 999999,
	'project_url'         => 'https://nad-lan.co.il/projects/fixture-commercial-project/',
	'towers'              => $towers,
	'asset_type'          => 'commercial_office',
	'product_family'      => 'commercial',
	'applicability_tags'  => array( 'three_d_showroom', 'floor_selector', 'suite_selector', 'commercial_rfp', 'context_map', 'decision_surface' ),
	'title'               => 'Fixture commercial project',
	'generated_at'        => gmdate( 'Y-m-d\TH:i:s\Z', $fixture_now ),
	'project_facts'       => array(),
	'floor_inventory'     => fixture_verified( 'fixture-inventory', null, 'floor-inventory' ),
	'floors'              => array(
		fixture_floor( 'tower-a', 'Office A', $facades, $raw_beam ),
		fixture_floor( 'tower-b', 'Office B' ),
	),
	'publication_blockers'=> array(),
);
$project = fixture_assert_not_error(
	nl_proposal_normalize_commercial_project( $project_raw, array( 'now' => $fixture_now ) ),
	'two-tower project'
);
fixture_assert( 2 === count( $project['floors'] ), 'both repeated floor IDs survive across towers' );
fixture_assert( $project['floors'][0]['identity_key'] !== $project['floors'][1]['identity_key'], 'floor identities include tower' );
fixture_assert( false !== strpos( $project['floors'][0]['url'], 'tower_id=tower-a' ), 'tower A URL is exact' );
fixture_assert( false !== strpos( $project['floors'][1]['url'], 'tower_id=tower-b' ), 'tower B URL is exact' );
fixture_assert( false !== strpos( $project['floors'][0]['url'], 'project_contract_id=fixture-commercial-project' ), 'floor URL carries immutable project contract ID' );
fixture_assert( false === strpos( $project['floors'][0]['url'], 'wp_post_id=' ), 'routing-only WordPress post ID is absent from floor URL' );
fixture_assert( false !== strpos( $project['floors'][0]['suites'][0]['url'], 'project_contract_id=fixture-commercial-project' ), 'suite URL carries immutable project contract ID' );

$reserved_url_project = $project_raw;
$reserved_url_project['project_url'] .= '?wp_post_id=991';
$reserved_url_result = nl_proposal_normalize_commercial_project( $reserved_url_project, array( 'now' => $fixture_now ) );
fixture_assert( is_wp_error( $reserved_url_result ) && 'nl_proposal_invalid_project_url' === $reserved_url_result->get_error_code(), 'project URL with routing-only identity data fails closed' );
$foreign_url_project = $project_raw;
$foreign_url_project['project_url'] = 'https://foreign.invalid/projects/fixture-commercial-project/';
$foreign_url_result = nl_proposal_normalize_commercial_project( $foreign_url_project, array( 'now' => $fixture_now ) );
fixture_assert( is_wp_error( $foreign_url_result ) && 'nl_proposal_invalid_project_url' === $foreign_url_result->get_error_code(), 'foreign-origin project URL fails closed' );
$wrong_permalink_project = $project_raw;
$wrong_permalink_project['project_url'] = 'https://nad-lan.co.il/projects/another-project/';
$wrong_permalink_result = nl_proposal_normalize_commercial_project( $wrong_permalink_project, array( 'now' => $fixture_now ) );
fixture_assert( is_wp_error( $wrong_permalink_result ) && 'nl_proposal_invalid_project_url' === $wrong_permalink_result->get_error_code(), 'same-origin URL with a noncanonical permalink path fails closed' );
$wrong_port_project = $project_raw;
$wrong_port_project['project_url'] = 'https://nad-lan.co.il:444/projects/fixture-commercial-project/';
$wrong_port_result = nl_proposal_normalize_commercial_project( $wrong_port_project, array( 'now' => $fixture_now ) );
fixture_assert( is_wp_error( $wrong_port_result ) && 'nl_proposal_invalid_project_url' === $wrong_port_result->get_error_code(), 'same host with a different effective port fails closed' );
fixture_assert( $project['floors'][0]['suites'][0]['identity_key'] !== $project['floors'][1]['suites'][0]['identity_key'], 'suite identities include tower' );
fixture_assert( 'Tower A' === $project['floors'][0]['tower_display_label']['value'], 'tower label never empty' );

$bad_suite_project = $project_raw;
$bad_suite_project['floors'][0]['suites'][0]['tower_id'] = 'tower-b';
fixture_assert( is_wp_error( nl_proposal_normalize_commercial_project( $bad_suite_project, array( 'now' => $fixture_now ) ) ), 'suite parent identity mismatch is rejected' );

$sample_document = json_decode( file_get_contents( __DIR__ . '/example-commercial-project-data.json' ), true );
fixture_assert( is_array( $sample_document ) && 2 === count( $sample_document['projects'] ), 'example JSON contains exactly two honest commercial skeletons' );
foreach ( $sample_document['projects'] as $sample_project ) {
	$sample_normalized = fixture_assert_not_error(
		nl_proposal_normalize_commercial_project( $sample_project, array( 'now' => $fixture_now ) ),
		'example project ' . $sample_project['project_id']
	);
	fixture_assert( false === $sample_normalized['publication_allowed'], 'example project must remain non-publishable' );
	fixture_assert( 0 === count( $sample_normalized['floors'] ), 'example project must not invent floor inventory' );
	fixture_assert( 'unknown' === $sample_normalized['floor_inventory']['state'], 'example inventory must remain unknown' );
	fixture_assert( 1 === count( $sample_normalized['towers'] ), 'current single-tower sample needs one explicit canonical tower' );
	fixture_assert( '' !== $sample_normalized['towers'][0]['display_label']['value'], 'sample tower label cannot be empty' );
}

echo "PASS commercial data contract: exact evidence, all availability statuses, 2 towers, 4 beams, landmark truth and fail-closed identities.\n";
