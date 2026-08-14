<?php
/** Executable contract fixture for the isolated flagship-v3 WordPress seam. */

declare(strict_types=1);

define( 'ABSPATH', __DIR__ . '/wordpress-stub/' );
define( 'NADLAN_CONFIG_VERSION', 'fixture' );

final class WP_Error {
	private $code;
	public function __construct( $code, $message = '' ) {
		unset( $message );
		$this->code = (string) $code;
	}
	public function get_error_code() {
		return $this->code;
	}
}

final class WP_Post {
	public $ID;
	public $post_status;
	public $post_name;
	public $post_password;
	public $post_title;
	public function __construct( int $id, string $slug, string $password, string $title = 'Einstein Tower' ) {
		$this->ID            = $id;
		$this->post_status   = 'publish';
		$this->post_name     = $slug;
		$this->post_password = $password;
		$this->post_title    = $title;
	}
}

final class WP_REST_Response {
	private $data;
	private $headers = array();
	public function __construct( array $data ) { $this->data = $data; }
	public function get_data(): array { return $this->data; }
	public function set_data( $data ): void { $this->data = $data; }
	public function header( $key, $value ): void { $this->headers[ $key ] = $value; }
	public function get_headers(): array { return $this->headers; }
}

$GLOBALS['nl_fixture_posts']      = array();
$GLOBALS['nl_fixture_meta']       = array();
$GLOBALS['nl_fixture_post_types'] = array();
$GLOBALS['nl_fixture_queried']    = 0;
$GLOBALS['nl_fixture_registered'] = array();
$GLOBALS['nl_fixture_assets']     = array();
$GLOBALS['nl_fixture_script_deps']= array();
$GLOBALS['nl_fixture_style_deps'] = array();
$GLOBALS['nl_fixture_can_edit']   = true;

function add_action( $hook, $callback, $priority = 10 ) { unset( $hook, $callback, $priority ); }
function add_filter( $hook, $callback, $priority = 10 ) { unset( $hook, $callback, $priority ); }
function register_post_meta( $post_type, $key, $args ) { $GLOBALS['nl_fixture_registered'][ $key ] = array( $post_type, $args ); return true; }
function current_user_can( $capability, $post_id = 0 ) { unset( $capability, $post_id ); return (bool) $GLOBALS['nl_fixture_can_edit']; }
function absint( $value ) { return abs( (int) $value ); }
function get_post( $post_id ) { return isset( $GLOBALS['nl_fixture_posts'][ (int) $post_id ] ) ? $GLOBALS['nl_fixture_posts'][ (int) $post_id ] : null; }
function get_post_type( $post_id ) { return isset( $GLOBALS['nl_fixture_post_types'][ (int) $post_id ] ) ? $GLOBALS['nl_fixture_post_types'][ (int) $post_id ] : ''; }
function get_post_meta( $post_id, $key, $single = false ) { unset( $single ); return isset( $GLOBALS['nl_fixture_meta'][ (int) $post_id ][ $key ] ) ? $GLOBALS['nl_fixture_meta'][ (int) $post_id ][ $key ] : ''; }
function get_queried_object_id() { return (int) $GLOBALS['nl_fixture_queried']; }
function get_the_title( $post_id ) { $post = get_post( $post_id ); return $post instanceof WP_Post ? $post->post_title : ''; }
function post_password_required( $post_id = 0 ) { unset( $post_id ); return false; }
function is_singular( $post_type = '' ) { return 'nadlan_project' === $post_type; }
function is_wp_error( $value ) { return $value instanceof WP_Error; }
function sanitize_key( $value ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $value ) ); }
function sanitize_text_field( $value ) { return trim( strip_tags( (string) $value ) ); }
function wp_strip_all_tags( $value ) { return strip_tags( (string) $value ); }
function wp_kses( $html, $allowed ) { unset( $allowed ); return (string) $html; }
function wp_parse_url( $url ) { return parse_url( (string) $url ); }
function home_url( $path = '' ) { return 'https://nad-lan.co.il' . ( '/' === $path ? '/' : '/' . ltrim( (string) $path, '/' ) ); }
function wp_make_link_relative( $url ) { $parts = parse_url( (string) $url ); return isset( $parts['path'] ) ? $parts['path'] : ''; }
function esc_url_raw( $url, $protocols = null ) { unset( $protocols ); return filter_var( (string) $url, FILTER_VALIDATE_URL ) ? (string) $url : ''; }
function esc_url( $url ) { return esc_url_raw( $url ); }
function esc_attr( $value ) { return htmlspecialchars( (string) $value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8' ); }
function esc_html( $value ) { return htmlspecialchars( (string) $value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8' ); }
function esc_html__( $value ) { return (string) $value; }
function wp_json_encode( $value, $flags = 0 ) { return json_encode( $value, $flags | JSON_THROW_ON_ERROR ); }
function trailingslashit( $value ) { return rtrim( (string) $value, '/\\' ) . '/'; }
function untrailingslashit( $value ) { return rtrim( (string) $value, '/\\' ); }
function plugins_url( $path = '', $plugin = '' ) { unset( $plugin ); return 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/' . ltrim( (string) $path, '/' ); }
function wp_enqueue_style( $handle, $url, $deps = array(), $version = false ) { unset( $version ); $GLOBALS['nl_fixture_assets'][ $handle ] = $url; $GLOBALS['nl_fixture_style_deps'][ $handle ] = $deps; }
function wp_enqueue_script( $handle, $url, $deps = array(), $version = false, $footer = false ) { unset( $version, $footer ); $GLOBALS['nl_fixture_assets'][ $handle ] = $url; $GLOBALS['nl_fixture_script_deps'][ $handle ] = $deps; }
function wp_script_add_data( $handle, $key, $value ) { unset( $handle, $key, $value ); }
function nocache_headers() {}
function wp_die( $message, $title = '', $args = array() ) { unset( $title, $args ); throw new RuntimeException( (string) $message ); }

require dirname( __DIR__ ) . '/plugins/nadlan-config/inc/flagship-surface.php';

function fixture_json( array $value ): string {
	return json_encode( $value, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR );
}

function fixture_clone( array $value ): array {
	return json_decode( fixture_json( $value ), true, 64, JSON_THROW_ON_ERROR );
}

function fixture_assert( bool $condition, string $message ): void {
	if ( ! $condition ) {
		fwrite( STDERR, "FAIL: {$message}\n" );
		exit( 1 );
	}
}

function fixture_error_code( $value ): string {
	return is_wp_error( $value ) ? (string) $value->get_error_code() : '';
}

$post_id = 9001;
$base    = 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/flagship-v3/projects/einstein-tower/';
$experience_base = $base . 'experience/';
$past    = '2026-01-01T00:00:00+03:00';
$future  = '2030-01-01T00:00:00+03:00';
$source  = array(
	'id'           => 'S001',
	'label'        => 'מקור בדיקה',
	'effective_at' => '2026-08-14',
	'url'          => 'https://example.org/source',
);
$row = function ( string $id, string $label, string $summary, string $state = 'current' ): array {
	return array( 'id' => $id, 'label' => $label, 'summary' => $summary, 'state' => $state, 'source_ids' => array( 'S001' ) );
};

$identity = array(
	'schema'              => 'nadlan-project-identity-contract/v1',
	'project_contract_id' => 'einstein-tower-6885-32',
	'source_id'           => 'einstein-tower-6885-32',
	'canonical_post_id'   => 4867,
	'canonical_slug'      => 'einstein-tower',
	'parcel'              => '6885/32',
	'locale'              => 'he',
	'inventory_contract'  => array(
		'state'          => 'not_supplied',
		'decision_grade' => false,
		'effective_at'   => '2026-08-14',
		'source_ids'     => array( 'S002' ),
		'note'           => 'No verified unit inventory is connected.',
	),
);

$representations = array(
	'schema'              => 'nadlan-project-representation-registry/v1',
	'project_contract_id' => 'einstein-tower-6885-32',
	'calibration'         => array( 'calibration_id' => 'einstein-33a-illustrative-massing-v1', 'north_degrees' => 0 ),
	'default_orbit'       => '35deg 64deg auto',
	'default_target'      => '0m 43m 0m',
	'representations'     => array(
		array( 'role' => 'model_hd', 'url' => $base . 'model-hd.glb', 'sha256' => '71fcca8a0f58743b5f2257684c79957fbbff8e0169f5438bdc78231f27968a53', 'representation_kind' => 'owner_approved_illustration', 'decision_grade' => false, 'owner_decision_id' => 'OWNER-2026-08-14-EINSTEIN-ILLUSTRATIVE-MASSING', 'effective_at' => $past, 'expires_at' => $future ),
		array( 'role' => 'model_lod', 'url' => $base . 'model-lod.glb', 'sha256' => '485161974b6d343956d249d821c893b72a59678e8e8ee2810c90cee5f23079ce', 'representation_kind' => 'owner_approved_illustration', 'decision_grade' => false, 'owner_decision_id' => 'OWNER-2026-08-14-EINSTEIN-ILLUSTRATIVE-MASSING', 'effective_at' => $past, 'expires_at' => $future ),
		array( 'role' => 'poster', 'url' => $base . 'poster.webp', 'sha256' => '5588d09e28f95ac5d6655626027c3ad41f17c5c5c78153ecb2ba138821aa8c85', 'representation_kind' => 'owner_approved_illustration', 'decision_grade' => false, 'owner_decision_id' => 'OWNER-2026-08-14-EINSTEIN-ILLUSTRATIVE-MASSING', 'effective_at' => $past, 'expires_at' => $future ),
	),
);

$visual = array(
	'schema'              => 'nadlan-visual-playground/v1',
	'project_contract_id' => 'einstein-tower-6885-32',
	'locale'              => 'he',
	'decision'            => array( 'owner_decision_id' => 'OWNER-2026-08-13-VISUAL-PLAYGROUND', 'approved_by' => 'site_owner', 'decision_grade' => false, 'effective_at' => $past, 'expires_at' => $future ),
	'comments_delivery'   => 'prepared_no_write',
	'writes_enabled'      => false,
	'tools'               => array(),
);
foreach ( array( 'view' => 'schematic_live_map', 'interior' => 'first_person_door', 'design' => 'illustrative_plan_drag', 'comments' => 'visual_annotation_request' ) as $tool_id => $preview_kind ) {
	$visual['tools'][] = array( 'id' => $tool_id, 'preview_kind' => $preview_kind, 'title' => 'כלי חזותי', 'description' => 'תצוגה אינטראקטיבית', 'open_label' => 'לפתיחה', 'disclosure' => 'המחשה', 'decision_grade' => false );
}

$buyer = array(
	'schema'              => 'nadlan-buyer-decision-contract/v1',
	'project_contract_id' => 'einstein-tower-6885-32',
	'locale'              => 'he',
	'effective_at'        => '2026-08-14',
	'labels'              => array( 'facts' => 'עובדות', 'context' => 'הסביבה', 'sea' => 'הים', 'education' => 'חינוך', 'transit' => 'תחבורה', 'construction' => 'בנייה ונוף', 'overseas_buyer' => 'רוכש מחו״ל', 'sources' => 'מקורות', 'current' => 'כיום', 'future' => 'בעתיד', 'source' => 'מקור' ),
	'sources'             => array( $source ),
	'facts'               => array( array( 'id' => 'parcel', 'label' => 'חלקה', 'value' => '6885/32', 'truth_state' => 'verified', 'source_ids' => array( 'S001' ) ) ),
	'context_map'         => array(
		'title'  => 'מצב נוכחי מול עתידי',
		'layers' => array(
			array( 'id' => 'current', 'label' => 'כיום', 'items' => array( $row( 'current-road', 'הצומת', 'תמונת מצב נוכחית' ) ) ),
			array( 'id' => 'future', 'label' => 'בעתיד', 'items' => array( $row( 'future-line', 'הקו הירוק', 'שירות מתוכנן', 'planned' ) ) ),
		),
	),
	'sea'                 => array( 'label' => 'חוף תל ברוך', 'distance_m' => 975, 'method' => 'straight_line_to_tel_baruch_beach_polygon', 'method_label' => 'קו אווירי לפוליגון החוף', 'source_ids' => array( 'S001' ) ),
	'education'           => array(
		'snapshot_label' => 'תמונת מצב',
		'school_year'    => '2026/27',
		'schools'        => array( array( 'name' => 'בית ספר', 'distance_m' => 362, 'method' => 'קו אווירי', 'source_ids' => array( 'S001' ) ) ),
		'kindergartens'  => array( array( 'name' => 'גן ילדים', 'distance_m' => 250, 'method' => 'קו אווירי', 'source_ids' => array( 'S001' ) ) ),
	),
	'transit'             => array(
		'line_label'      => 'הקו הירוק',
		'current_works'   => array( 'state' => 'observed', 'summary' => 'עבודות תשתית נצפו בצומת.', 'source_ids' => array( 'S001' ) ),
		'planned_service' => array( 'state' => 'planned', 'summary' => 'שירות עתידי מתוכנן; לא נקבע כאן מועד הפעלה.', 'operating_date' => null, 'source_ids' => array( 'S001' ) ),
	),
	'construction_and_views' => array(
		'current_state'  => array( 'label' => 'מצב עבודות', 'summary' => 'עבודות באתר', 'state' => 'current', 'source_ids' => array( 'S001' ) ),
		'future_context' => array( 'label' => 'בנייה רחבה', 'summary' => 'בינוי עתידי בסביבה', 'state' => 'planned', 'source_ids' => array( 'S001' ) ),
		'unit_view_state'=> array( 'label' => 'נוף מדירה', 'summary' => 'לא מחובר למלאי מאומת', 'state' => 'not_verified', 'source_ids' => array( 'S001' ) ),
	),
	'overseas_buyer'      => array(
		'title'              => 'מסלול החלטה לרוכש מחו״ל',
		'purchase_structure' => array( 'label' => 'מבנה רכישה', 'summary' => 'קבוצת רכישה דורשת בדיקה מסמכית.', 'source_ids' => array( 'S001' ) ),
		'steps'              => array( array( 'id' => 'documents', 'title' => 'מסמכים', 'summary' => 'בדיקת מסמכי העסקה', 'source_ids' => array( 'S001' ) ) ),
	),
	'primary_action'      => array( 'label' => 'למסלול הרוכש', 'target_section' => 'overseas-buyer' ),
);

$experiences = array(
	'schema'              => 'nadlan-project-experience-registry/v1',
	'project_contract_id' => 'einstein-tower-6885-32',
	'locale'              => 'he',
	'mapping_crosswalk_sha256' => '42072325c22a87b40b8bb6bfc6a09e29beac01ab84fccbe403a6c0d0abddfb9a',
	'mapping_anchor_summary_sha256' => 'dadc53333e2ca1ac78daae2610c4315559659510dc4b23774caaca5442e6889c',
	'heading'             => 'נכנסים לפרויקט',
	'back_label'          => 'חזרה לפרויקט',
	'previous_label'      => 'הקודם',
	'next_label'          => 'הבא',
	'decision'            => array( 'owner_decision_id' => 'OWNER-2026-08-14-EINSTEIN-INTERIOR-FACILITIES-DEMO', 'approved_by' => 'site_owner', 'representation_kind' => 'owner_approved_illustration', 'decision_grade' => false, 'effective_at' => $past, 'expires_at' => $future ),
	'scenes'              => array(
		array( 'id' => 'living', 'asset_id' => 'representative-apartment-living-v1', 'kind' => 'interior', 'title' => 'חלל מגורים', 'summary' => 'המחשת פנים לבחינת תחושת החלל.', 'open_label' => 'להיכנס לחלל', 'preview_url' => $experience_base . 'representative-apartment-living-v1.webp', 'fullscreen_url' => $experience_base . 'representative-apartment-living-v1.webp', 'mapping_state' => 'owner_approved_illustrative_mapping', 'mapping_owner_decision_id' => 'OWNER-2026-08-14-EINSTEIN-INTERIOR-FACILITIES-DEMO', 'model_hotspot_group' => 'representative-interior-concept', 'representation_kind' => 'owner_approved_illustration', 'decision_grade' => false, 'source_ids' => array(), 'model_hotspot' => array( 'position' => '16m 34.7m 5.8m', 'normal' => '0 0 1', 'calibration_id' => 'einstein-33a-illustrative-massing-v1' ), 'image_hotspots' => array( array( 'id' => 'living-window', 'x_percent' => 35, 'y_percent' => 42, 'label' => 'חלון', 'detail' => 'נקודת עניין בחלל המומחש.' ) ) ),
		array( 'id' => 'arrival', 'asset_id' => 'facility-arrival-gallery-v1', 'kind' => 'facility', 'title' => 'לובי', 'summary' => 'המחשת מתקן משותף לבחינת חוויית הכניסה.', 'open_label' => 'לראות את הלובי', 'preview_url' => $experience_base . 'facility-arrival-gallery-v1.webp', 'fullscreen_url' => $experience_base . 'facility-arrival-gallery-v1.webp', 'mapping_state' => 'owner_approved_illustrative_mapping', 'mapping_owner_decision_id' => 'OWNER-2026-08-14-EINSTEIN-INTERIOR-FACILITIES-DEMO', 'model_hotspot_group' => 'facility-arrival-concept', 'representation_kind' => 'owner_approved_illustration', 'decision_grade' => false, 'source_ids' => array(), 'model_hotspot' => array( 'position' => '12m 9.5m -13.25m', 'normal' => '0 0 -1', 'calibration_id' => 'einstein-33a-illustrative-massing-v1' ), 'image_hotspots' => array( array( 'id' => 'lobby-entry', 'x_percent' => 62, 'y_percent' => 55, 'label' => 'כניסה', 'detail' => 'נקודת עניין במתקן המומחש.' ) ) ),
	),
);
$experiences['scenes'][0] = array_merge( $experiences['scenes'][0], array(
	'model_component'       => 'Tower_28_Level_Massing;Glass_Terrace_Strips;Champagne_Fins',
	'placement_source_refs' => array( 'IVS002', 'IVS001' ),
	'placement_basis'       => 'Source constrains tower glass-facade zone; owner authorizes one shared mid-height clickable interior-gallery anchor just outside the current glass strip',
	'placement_confidence'  => array( 'zone' => 0.68, 'exact_point' => 0.18 ),
	'placement_ambiguity'   => 'No unit floor room boundary view direction or cardinal facade is established',
) );
$experiences['scenes'][1] = array_merge( $experiences['scenes'][1], array(
	'model_component'       => 'Tower_28_Level_Massing;Podium_Double_Level',
	'placement_source_refs' => array( 'IVS003', 'IVS004', 'IVS005', 'IVS008' ),
	'placement_basis'       => 'Source constrains use to the tower/base arrival zone; exact outer-face point at the current tower-podium seam is owner-approved interpolation',
	'placement_confidence'  => array( 'zone' => 0.63, 'exact_point' => 0.20 ),
	'placement_ambiguity'   => 'No official lobby door facade room extent finish reception desk or accessible route point is established',
) );
$second_interior = fixture_clone( $experiences['scenes'][0] );
$second_interior['id'] = 'bedroom';
$second_interior['asset_id'] = 'representative-apartment-bedroom-v1';
$second_interior['title'] = 'חדר שינה';
$second_interior['preview_url'] = $experience_base . 'representative-apartment-bedroom-v1.webp';
$second_interior['fullscreen_url'] = $experience_base . 'representative-apartment-bedroom-v1.webp';
$second_interior['model_hotspot_group'] = 'representative-interior-concept';
$second_interior['placement_basis'] = 'Bedroom shares the aggregate interior-gallery anchor; the scene is owner-approved demonstration media and is not assigned its own floor facade or unit';
$second_interior['placement_ambiguity'] = 'Bedroom existence design dimensions unit floor view and room location are wholly unmapped';
$second_interior['image_hotspots'][0]['id'] = 'bedroom-window';
$second_facility = fixture_clone( $experiences['scenes'][1] );
$second_facility['id'] = 'open-frame';
$second_facility['asset_id'] = 'facility-landscaped-terrace-v1';
$second_facility['title'] = 'מרפסת משותפת';
$second_facility['preview_url'] = $experience_base . 'facility-landscaped-terrace-v1.webp';
$second_facility['fullscreen_url'] = $experience_base . 'facility-landscaped-terrace-v1.webp';
$second_facility['model_hotspot']['position'] = '27m 10m 14m';
$second_facility['model_hotspot']['normal'] = '0 1 0';
$second_facility['model_hotspot_group'] = 'facility-landscaped-open-space-concept';
$second_facility['model_component'] = 'Landscape_Terraces;Podium_Double_Level';
$second_facility['placement_source_refs'] = array( 'IVS003', 'IVS004', 'IVS005', 'IVS012' );
$second_facility['placement_basis'] = 'Source strongly supports the public landscaped-roof/open-space category; selected current Landscape_Terraces slab and exact point are owner-approved interpolation';
$second_facility['placement_confidence'] = array( 'zone' => 0.86, 'exact_point' => 0.24 );
$second_facility['placement_ambiguity'] = 'Exact roof polygon level route planting layout view and whether the generated scene depicts any delivered facility are unresolved';
$second_facility['image_hotspots'][0]['id'] = 'terrace-landscape';
$experiences['scenes'][] = $second_interior;
$experiences['scenes'][] = $second_facility;

$baseline_meta = array(
	'project_surface_version'              => 'flagship-v3',
	'project_contract_id'                  => 'einstein-tower-6885-32',
	'source_id'                            => '',
	'_nadlan_private_unit_journey'         => 'private-unit-journey-v2',
	'_nadlan_flagship_source_post_id'      => 4867,
	'project_model_glb'                    => $base . 'model-hd.glb',
	'project_model_lod_glb'                => $base . 'model-lod.glb',
	'project_model_poster'                 => $base . 'poster.webp',
	'project_3d_units'                     => '[]',
	'project_identity_contract_json'       => fixture_json( $identity ),
	'project_representation_registry_json' => fixture_json( $representations ),
	'project_visual_playground_json'       => fixture_json( $visual ),
	'project_buyer_decision_contract_json' => fixture_json( $buyer ),
	'project_experience_registry_json'     => fixture_json( $experiences ),
);

$GLOBALS['nl_fixture_posts'][ $post_id ]      = new WP_Post( $post_id, 'sandbox-einstein-tower-flagship-v3-review', 'private-review' );
$GLOBALS['nl_fixture_post_types'][ $post_id ] = 'nadlan_project';
$GLOBALS['nl_fixture_meta'][ $post_id ]       = $baseline_meta;
$GLOBALS['nl_fixture_queried']                = $post_id;

nadlan_flagship_v3_register_meta();
fixture_assert( isset( $GLOBALS['nl_fixture_registered']['project_experience_registry_json'] ), 'experience meta is registered' );
fixture_assert( isset( $GLOBALS['nl_fixture_registered']['_nadlan_flagship_source_post_id'] ), 'source-post crosswalk meta is registered' );

$validated = nadlan_flagship_v3_validate_post( $post_id );
fixture_assert( ! is_wp_error( $validated ), 'valid private sandbox contract is accepted: ' . fixture_error_code( $validated ) );
fixture_assert( 'private_sandbox' === $validated['mode'], 'valid fixture remains private sandbox' );
fixture_assert( false === $validated['inventory']['decision_grade'], 'inventory remains non-decision-grade' );
fixture_assert( 4 === count( $validated['experiences']['scenes'] ), 'two interior and two facility scenes survive normalization' );
fixture_assert( array( 'living', 'arrival', 'bedroom', 'open-frame' ) === array_column( $validated['experiences']['scenes'], 'id' ), 'experience registry uses the exact four frozen manifest scene IDs' );
fixture_assert( 4 === count( $validated['visual']['tools'] ) && array( 'view', 'interior', 'design', 'comments' ) === array_column( $validated['visual']['tools'], 'id' ), 'exactly four top-level playground doors are exposed' );
$runtime_config = nadlan_flagship_v3_runtime_config( $validated );

// Consume the generated package/stage artifacts exactly as a WordPress write
// would receive them. The password is injected only into the post fixture;
// every staged meta value remains byte-for-byte unchanged.
$generated_package_path = dirname( __DIR__ ) . '/assets/projects/einstein-tower/contracts/flagship-project.json';
$generated_stage_path = dirname( __DIR__ ) . '/docs/wp-drafts/einstein-tower-flagship-v3-private-stage.json';
fixture_assert( is_readable( $generated_package_path ) && is_readable( $generated_stage_path ), 'generated flagship package and private-stage request are available' );
$generated_package = json_decode( (string) file_get_contents( $generated_package_path ), true, 64, JSON_THROW_ON_ERROR );
$generated_stage = json_decode( (string) file_get_contents( $generated_stage_path ), true, 64, JSON_THROW_ON_ERROR );
fixture_assert( 'nadlan-flagship-project-package/v1' === $generated_package['schema'] && 'nadlan-wordpress-private-stage-request/v1' === $generated_stage['schema'], 'generated artifact schemas are exact' );
fixture_assert( ! array_key_exists( 'password', $generated_stage['body'] ) && '' === $generated_stage['body']['meta']['source_id'], 'generated stage keeps its password secret external and catalog source_id blank' );
$generated_meta = $generated_stage['body']['meta'];
$generated_meta_fingerprint = hash( 'sha256', fixture_json( $generated_meta ) );
foreach ( array(
	'project_identity_contract_json' => 'identity',
	'project_representation_registry_json' => 'representations',
	'project_visual_playground_json' => 'visual',
	'project_buyer_decision_contract_json' => 'buyer_decision',
	'project_experience_registry_json' => 'experiences',
) as $meta_key => $package_key ) {
	fixture_assert( fixture_json( json_decode( (string) $generated_meta[ $meta_key ], true, 64, JSON_THROW_ON_ERROR ) ) === fixture_json( $generated_package['contracts'][ $package_key ] ), 'generated stage losslessly projects package contract: ' . $meta_key );
}
$generated_post_id = 9101;
$GLOBALS['nl_fixture_posts'][ $generated_post_id ] = new WP_Post(
	$generated_post_id,
	(string) $generated_stage['body']['slug'],
	'injected-at-runtime-only',
	(string) $generated_stage['body']['title']
);
$GLOBALS['nl_fixture_post_types'][ $generated_post_id ] = 'nadlan_project';
$GLOBALS['nl_fixture_meta'][ $generated_post_id ] = $generated_meta;
$generated_validated = nadlan_flagship_v3_validate_post( $generated_post_id );
fixture_assert( ! is_wp_error( $generated_validated ), 'generated stage meta passes the actual WordPress validator unchanged: ' . fixture_error_code( $generated_validated ) );
fixture_assert( 'private_sandbox' === $generated_validated['mode'] && array( 'living', 'bedroom', 'arrival', 'open-frame' ) === array_column( $generated_validated['experiences']['scenes'], 'id' ), 'generated stage preserves the private mode and exact scene contract' );
fixture_assert( hash_equals( $generated_meta_fingerprint, hash( 'sha256', fixture_json( $GLOBALS['nl_fixture_meta'][ $generated_post_id ] ) ) ), 'WordPress validation does not mutate generated stage meta' );
$generated_html = nadlan_flagship_v3_render_for( $generated_post_id, (string) $generated_stage['body']['content'] );
fixture_assert( '' !== $generated_html && 1 === substr_count( strtolower( $generated_html ), '<h1' ) && 1 === substr_count( $generated_html, 'data-nlfs-dossier="nadlan-einstein-he-dossier-v1"' ), 'generated stage content composes with one renderer-owned H1 and one dossier' );

if ( isset( $argv ) && in_array( '--emit-runtime-config', $argv, true ) ) {
	fwrite( STDOUT, fixture_json( $runtime_config ) );
	exit( 0 );
}

$dossier = '<article data-nlfs-dossier="nadlan-einstein-he-dossier-v1" lang="he" dir="rtl"><section id="dossier-overview"><h2>מדריך ההחלטה המלא</h2><p>תוכן עברי חדש לרוכש מופיע פעם אחת בלבד.</p></section></article>';
$html = nadlan_flagship_v3_render_for( $post_id, $dossier );
fixture_assert( '' !== $html, 'authorized private sandbox renders' );
fixture_assert( 1 === substr_count( $html, 'הדמיה מאושרת' ), 'one global demo label is rendered' );
fixture_assert( 1 === substr_count( strtolower( $html ), '<h1' ), 'surface owns exactly one visible project H1' );
fixture_assert( false !== strpos( $html, '<h1>EINSTEIN TOWER תל אביב</h1>' ), 'visible H1 comes from the reviewed Hebrew contract, not the sandbox clone title' );
fixture_assert( 1 === substr_count( strtolower( $html ), '<main' ) && 1 === substr_count( $html, 'data-nl-flagship="v3"' ), 'one main flagship page surface renders' );
fixture_assert( 1 === substr_count( $html, 'data-nlfs-dossier="nadlan-einstein-he-dossier-v1"' ) && 1 === substr_count( $html, 'תוכן עברי חדש לרוכש מופיע פעם אחת בלבד.' ), 'staged Hebrew dossier is composed exactly once' );
fixture_assert( false === strpos( strtolower( $html ), '<form' ), 'surface exposes no form or write path' );
fixture_assert( false === stripos( $html, 'olp' ), 'internal delivery terms are absent from public UI' );
fixture_assert( 1 === substr_count( $html, 'nlfs__primary-action' ), 'exactly one primary next action is rendered' );
fixture_assert( false !== strpos( $html, 'data-nlfs-scene="living"' ), 'manifest interior scene is selectable' );
fixture_assert( false !== strpos( $html, 'data-nlfs-scene="arrival"' ), 'manifest facility scene is selectable' );
fixture_assert( 3 === substr_count( $html, 'class="nlfs__model-hotspot"' ), 'three evidence-shaped model anchors render' );
foreach ( array( '16m 34.7m 5.8m', '12m 9.5m -13.25m', '27m 10m 14m' ) as $expected_position ) {
	fixture_assert( false !== strpos( $html, 'data-position="' . $expected_position . '"' ), 'expected illustrative anchor renders: ' . $expected_position );
}
fixture_assert( false !== strpos( $html, 'data-nlfs-decision-contract' ), 'full buyer-decision composition renders' );
foreach ( array( '-facts', 'data-context-layer="current"', 'data-context-layer="future"', '-sea', '-education', '-transit', '-construction', '-overseas-buyer', '-sources' ) as $decision_surface_marker ) {
	fixture_assert( false !== strpos( $html, $decision_surface_marker ), 'buyer-decision section renders: ' . $decision_surface_marker );
}
fixture_assert( false !== strpos( $html, 'straight_line_to_tel_baruch_beach_polygon' ), 'runtime preserves the reviewed straight-line sea method' );
fixture_assert( false !== strpos( $html, 'placement_basis' ) && false !== strpos( $html, 'placement_source_refs' ) && false !== strpos( $html, 'placement_confidence' ) && false !== strpos( $html, 'placement_ambiguity' ), 'runtime config retains the evidence-shaped illustrative placement contract' );
fixture_assert( false !== strpos( $html, '"allowed_evidence_reference_ids":["IVS001","IVS002","IVS003","IVS004","IVS005","IVS008","IVS012"]' ), 'runtime trust allowlist is the exact frozen IVS union' );
fixture_assert( false !== strpos( $html, '"allowed_asset_prefix":"/wp-content/plugins/nadlan-config/assets/flagship-v3/projects/einstein-tower/experience/"' ), 'runtime trust prefix is the exact plugin-local project experience path' );
foreach ( array( '"zone":0.68,"exact_point":0.18', '"zone":0.63,"exact_point":0.2', '"zone":0.86,"exact_point":0.24' ) as $confidence_pair ) {
	fixture_assert( false !== strpos( $html, $confidence_pair ), 'runtime preserves exact frozen confidence pair: ' . $confidence_pair );
}
fixture_assert( false !== strpos( $html, '"model_hotspot_scene_ids":["living","bedroom"]' ), 'manifest interior marker group exposes both individually selectable scenes' );
fixture_assert( false === strpos( $html, 'ajax.googleapis.com' ) && false === strpos( $html, '<model-viewer' ), 'render has no third-party model-viewer dependency' );
fixture_assert( isset( $GLOBALS['nl_fixture_assets']['nadlan-flagship-v3-viewer'] ) && 0 === strpos( $GLOBALS['nl_fixture_assets']['nadlan-flagship-v3-viewer'], 'https://nad-lan.co.il/' ), 'first-party local viewer asset is enqueued' );
fixture_assert( isset( $GLOBALS['nl_fixture_assets']['nadlan-flagship-v3-playground'] ) && 0 === strpos( $GLOBALS['nl_fixture_assets']['nadlan-flagship-v3-playground'], 'https://nad-lan.co.il/' ), 'generic first-party playground runtime is enqueued' );
fixture_assert( array( 'nadlan-flagship-v3-viewer', 'nadlan-flagship-v3-playground' ) === $GLOBALS['nl_fixture_script_deps']['nadlan-flagship-v3'], 'bootstrap depends on both local runtimes in executable order' );
fixture_assert( isset( $GLOBALS['nl_fixture_assets']['nadlan-flagship-v3-playground'] ) && isset( $GLOBALS['nl_fixture_assets']['nadlan-flagship-v3'] ), 'both canonical playground and host styles are enqueued' );
fixture_assert( array( 'nadlan-flagship-v3-playground' ) === $GLOBALS['nl_fixture_style_deps']['nadlan-flagship-v3'], 'host style loads after the exact canonical playground style' );

$GLOBALS['nl_fixture_can_edit'] = false;
$rest_response = new WP_REST_Response( array(
	'content' => array( 'rendered' => '<p><img src="' . $base . 'poster.webp"></p>', 'raw' => 'private', 'protected' => false ),
	'excerpt' => array( 'rendered' => 'private summary', 'raw' => 'private', 'protected' => false ),
	'_links' => array( 'wp:featuredmedia' => array( array( 'href' => $base . 'poster.webp' ) ), 'self' => array( array( 'href' => 'https://nad-lan.co.il/wp-json/wp/v2/nadlan_project/9001' ) ) ),
	'meta' => array(
		'project_experience_registry_json' => fixture_json( $experiences ),
		'project_model_glb' => $base . 'model-hd.glb', 'project_model_lod_glb' => $base . 'model-lod.glb',
		'project_model_poster' => $base . 'poster.webp', 'project_3d_units' => '[]', 'project_3d_facade_images' => fixture_json( array( $base . 'poster.webp' ) ),
		'source_id' => 'einstein-tower-6885-32', '_nadlan_private_unit_journey' => 'private-unit-journey-v2',
		'_nadlan_flagship_source_post_id' => 4867, 'is_demo' => true, 'data_quality' => 'enriched', 'unrelated' => 'kept',
	),
) );
nadlan_flagship_v3_guard_rest_meta( $rest_response, $GLOBALS['nl_fixture_posts'][ $post_id ] );
$rest_data = $rest_response->get_data();
$rest_headers = $rest_response->get_headers();
fixture_assert( array( 'unrelated' => 'kept' ) === $rest_data['meta'], 'anonymous REST response strips all v3, shared model, catalog identity and privacy meta' );
fixture_assert( '' === $rest_data['content']['rendered'] && '' === $rest_data['excerpt']['rendered'] && ! isset( $rest_data['content']['raw'], $rest_data['excerpt']['raw'] ), 'anonymous REST response cannot leak staged body or excerpt asset URLs' );
fixture_assert( ! isset( $rest_data['_links']['wp:featuredmedia'] ) && isset( $rest_data['_links']['self'] ), 'anonymous REST response drops staged media discovery while preserving unrelated links' );
fixture_assert( false !== strpos( $rest_headers['Cache-Control'], 'no-store' ) && false !== strpos( $rest_headers['X-Robots-Tag'], 'noindex' ), 'anonymous REST response receives private no-store/noindex headers' );
$anonymous_query = nadlan_flagship_v3_guard_rest_collection( array( 's' => 'Einstein' ), null );
fixture_assert( isset( $anonymous_query['meta_query'][0]['relation'] ) && 'OR' === $anonymous_query['meta_query'][0]['relation'], 'anonymous REST collection/search excludes the private-stage privacy marker' );
$GLOBALS['nl_fixture_can_edit'] = true;
$editor_query = array( 's' => 'Einstein' );
fixture_assert( $editor_query === nadlan_flagship_v3_guard_rest_collection( $editor_query, null ), 'authorized editors retain REST collection access for private review' );

$canonical_id = 4867;
$GLOBALS['nl_fixture_posts'][ $canonical_id ]      = new WP_Post( $canonical_id, 'einstein-tower', '' );
$GLOBALS['nl_fixture_post_types'][ $canonical_id ] = 'nadlan_project';
$GLOBALS['nl_fixture_meta'][ $canonical_id ]       = $baseline_meta;
$GLOBALS['nl_fixture_meta'][ $canonical_id ]['source_id'] = 'einstein-tower-6885-32';
fixture_assert( 'canonical_release_disabled' === fixture_error_code( nadlan_flagship_v3_validate_post( $canonical_id ) ), 'canonical post is disabled until reviewed release' );

$test_meta = $baseline_meta;
$test_meta['source_id'] = 'einstein-tower-6885-32';
$GLOBALS['nl_fixture_meta'][ $post_id ] = $test_meta;
fixture_assert( 'invalid_private_sandbox' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'private sandbox cannot duplicate canonical catalog source_id' );

$test_meta = $baseline_meta;
$bad_representations = fixture_clone( $representations );
$bad_representations['calibration']['calibration_id'] = 'einstein-33a-illustration-v1';
$test_meta['project_representation_registry_json'] = fixture_json( $bad_representations );
$GLOBALS['nl_fixture_meta'][ $post_id ] = $test_meta;
fixture_assert( 'invalid_representation_registry' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'illustrative anchors cannot bind to a noncanonical model calibration' );

$test_meta = $baseline_meta;
$bad_representations = fixture_clone( $representations );
$bad_representations['representations'][0]['url'] = $base . 'unreviewed-model.glb';
$test_meta['project_representation_registry_json'] = fixture_json( $bad_representations );
$GLOBALS['nl_fixture_meta'][ $post_id ] = $test_meta;
fixture_assert( 'unauthorized_representation_url' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'same-origin but unreviewed model filename is rejected' );

$test_meta = $baseline_meta;
$bad_representations = fixture_clone( $representations );
$bad_representations['representations'][0]['sha256'] = str_repeat( '0', 64 );
$test_meta['project_representation_registry_json'] = fixture_json( $bad_representations );
$GLOBALS['nl_fixture_meta'][ $post_id ] = $test_meta;
fixture_assert( 'invalid_representation' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'unreviewed model hash is rejected' );

$test_meta = $baseline_meta;
$bad_representations = fixture_clone( $representations );
$bad_representations['representations'][0]['owner_decision_id'] = 'OWNER-2026-08-13-MODEL-FIRST-SHOWROOM';
$test_meta['project_representation_registry_json'] = fixture_json( $bad_representations );
$GLOBALS['nl_fixture_meta'][ $post_id ] = $test_meta;
fixture_assert( 'invalid_representation' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'model representation requires its exact owner decision' );

$test_meta = $baseline_meta;
$bad_identity = fixture_clone( $identity );
$bad_identity['source_id'] = 'wrong-project';
$test_meta['project_identity_contract_json'] = fixture_json( $bad_identity );
$GLOBALS['nl_fixture_meta'][ $post_id ] = $test_meta;
fixture_assert( 'identity_mismatch' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'wrong project identity fails closed' );
fixture_assert( '' === nadlan_flagship_v3_dispatch( $post_id, $dossier ), 'selected invalid contract never falls back to legacy renderer' );

$test_meta = $baseline_meta;
$bad_experience = fixture_clone( $experiences );
$bad_experience['scenes'][0]['preview_url'] = 'https://cdn.example.org/einstein-tower/interior.webp';
$test_meta['project_experience_registry_json'] = fixture_json( $bad_experience );
$GLOBALS['nl_fixture_meta'][ $post_id ] = $test_meta;
fixture_assert( 'invalid_experience_scene' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'external experience asset is rejected' );

$bad_experience = fixture_clone( $experiences );
$bad_experience['scenes'][0]['decision_grade'] = true;
$test_meta['project_experience_registry_json'] = fixture_json( $bad_experience );
$GLOBALS['nl_fixture_meta'][ $post_id ] = $test_meta;
fixture_assert( 'invalid_experience_scene' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'decision-grade illustration is rejected' );

$bad_experience = fixture_clone( $experiences );
$bad_experience['scenes'][0]['mapping_state'] = 'source_cited_mapping';
$bad_experience['scenes'][0]['source_ids'] = array();
$test_meta['project_experience_registry_json'] = fixture_json( $bad_experience );
$GLOBALS['nl_fixture_meta'][ $post_id ] = $test_meta;
fixture_assert( 'invalid_experience_scene' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'uncited exact spatial mapping is rejected' );
$bad_experience['scenes'][0]['source_ids'] = array( 'S001' );
$test_meta['project_experience_registry_json'] = fixture_json( $bad_experience );
$GLOBALS['nl_fixture_meta'][ $post_id ] = $test_meta;
fixture_assert( 'invalid_experience_scene' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'generic source cannot unlock exact spatial mapping' );

$bad_experience = fixture_clone( $experiences );
$bad_experience['scenes'][0]['mapping_owner_decision_id'] = 'OWNER-WRONG';
$test_meta['project_experience_registry_json'] = fixture_json( $bad_experience );
$GLOBALS['nl_fixture_meta'][ $post_id ] = $test_meta;
fixture_assert( 'invalid_experience_scene' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'illustrative model mapping requires the exact owner decision' );

$bad_experience = fixture_clone( $experiences );
$bad_experience['scenes'][0]['placement_source_refs'] = array();
$test_meta['project_experience_registry_json'] = fixture_json( $bad_experience );
$GLOBALS['nl_fixture_meta'][ $post_id ] = $test_meta;
fixture_assert( 'invalid_experience_scene' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'illustrative mapping requires evidence-shaped placement references' );

$bad_experience = fixture_clone( $experiences );
$bad_experience['scenes'][0]['placement_confidence'] = 'high';
$test_meta['project_experience_registry_json'] = fixture_json( $bad_experience );
$GLOBALS['nl_fixture_meta'][ $post_id ] = $test_meta;
fixture_assert( 'invalid_experience_scene' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'illustrative mapping cannot claim high placement confidence' );

$test_meta = $baseline_meta;
$bad_visual = fixture_clone( $visual );
$bad_visual['olp_endpoint'] = '';
$test_meta['project_visual_playground_json'] = fixture_json( $bad_visual );
$GLOBALS['nl_fixture_meta'][ $post_id ] = $test_meta;
fixture_assert( 'invalid_visual_playground' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'internal delivery key is rejected even when empty' );

$test_meta = $baseline_meta;
$bad_buyer = fixture_clone( $buyer );
$bad_buyer['lead_endpoint'] = 'https://example.org/write';
$test_meta['project_buyer_decision_contract_json'] = fixture_json( $bad_buyer );
$GLOBALS['nl_fixture_meta'][ $post_id ] = $test_meta;
fixture_assert( 'invalid_buyer_decision_contract' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'buyer contract cannot embed a lead route' );

$test_meta = $baseline_meta;
$test_meta['project_3d_units'] = fixture_json( array( array( 'id' => 'unit-1' ) ) );
$GLOBALS['nl_fixture_meta'][ $post_id ] = $test_meta;
fixture_assert( 'zero_inventory_required' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'nonzero inventory is rejected' );

$GLOBALS['nl_fixture_meta'][ $post_id ] = $baseline_meta;
$GLOBALS['nl_fixture_posts'][ $post_id ]->post_password = '';
fixture_assert( 'invalid_private_sandbox' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'missing password is rejected' );
$GLOBALS['nl_fixture_posts'][ $post_id ]->post_password = 'private-review';
$GLOBALS['nl_fixture_posts'][ $post_id ]->post_name = 'einstein-tower-public-looking';
fixture_assert( 'invalid_private_sandbox' === fixture_error_code( nadlan_flagship_v3_validate_post( $post_id ) ), 'unapproved sandbox slug is rejected' );
$GLOBALS['nl_fixture_posts'][ $post_id ]->post_name = 'sandbox-einstein-tower-flagship-v3-review';

$robots = nadlan_flagship_v3_robots( array() );
fixture_assert( ! empty( $robots['noindex'] ) && ! empty( $robots['nofollow'] ) && ! empty( $robots['noarchive'] ), 'private candidate forces robots protections' );
fixture_assert( false === nadlan_flagship_v3_private_canonical( 'https://nad-lan.co.il/projects/example/' ), 'private candidate suppresses canonical output' );
fixture_assert( '' === nadlan_flagship_v3_asset_url( $base . 'poster.webp?token=secret', 'poster', nadlan_flagship_v3_contract( 'einstein-tower-6885-32' ) ), 'asset query strings are rejected' );
fixture_assert( '' !== nadlan_flagship_v3_source_url( 'https://gis.example.org/query?parcel=32' ), 'HTTPS citation query is accepted' );
fixture_assert( '' === nadlan_flagship_v3_sanitize_json_meta( '{broken' ), 'malformed JSON meta is rejected' );
fixture_assert( '' === nadlan_flagship_v3_safe_article_html( '<article data-nlfs-dossier="nadlan-einstein-he-dossier-v1"><h1>Duplicate</h1></article>', nadlan_flagship_v3_contract( 'einstein-tower-6885-32' ) ), 'dossier cannot inject a second H1' );
fixture_assert( '' === nadlan_flagship_v3_safe_article_html( '<article data-nlfs-dossier="nadlan-einstein-he-dossier-v1"><script>alert(1)</script></article>', nadlan_flagship_v3_contract( 'einstein-tower-6885-32' ) ), 'dossier cannot inject script' );
fixture_assert( '' === nadlan_flagship_v3_safe_article_html( '<article data-nlfs-dossier="nadlan-einstein-he-dossier-v1"><img src="https://cdn.example.org/media.webp" alt=""></article>', nadlan_flagship_v3_contract( 'einstein-tower-6885-32' ) ), 'dossier cannot hotlink external media' );
fixture_assert( '' === nadlan_flagship_v3_safe_article_html( '<article data-nlfs-dossier="nadlan-einstein-he-dossier-v1"><p>Internal OLP term</p></article>', nadlan_flagship_v3_contract( 'einstein-tower-6885-32' ) ), 'dossier cannot expose internal delivery wording' );

$unselected_id = 9002;
$GLOBALS['nl_fixture_posts'][ $unselected_id ]      = new WP_Post( $unselected_id, 'legacy', '' );
$GLOBALS['nl_fixture_post_types'][ $unselected_id ] = 'nadlan_project';
$GLOBALS['nl_fixture_meta'][ $unselected_id ]       = array();
fixture_assert( '<div>legacy</div>' === nadlan_flagship_v3_dispatch( $unselected_id, '<div>legacy</div>' ), 'unselected project keeps legacy renderer' );

$js = file_get_contents( dirname( __DIR__ ) . '/plugins/nadlan-config/assets/flagship-v3/flagship.js' );
fixture_assert( is_string( $js ) && false !== strpos( $js, 'document.body.appendChild(dialog)' ), 'fullscreen experience mounts at body level' );
fixture_assert( false !== strpos( $js, 'restorePage(current.state)' ) && false !== strpos( $js, 'restoreModelState(state.model)' ), 'Back restores page and model state' );
fixture_assert( false !== strpos( $js, 'scene.model_hotspot_scene_ids') && false !== strpos( $js, 'moveScene(-1)') && false !== strpos( $js, 'moveScene(1)' ), 'model marker group can select every scene without closing the fullscreen body layer' );
fixture_assert( 0 === preg_match( '/\b(?:sendBeacon|XMLHttpRequest)\b/', $js ), 'surface runtime has no network-write primitive' );
fixture_assert( false === stripos( $js, 'localStorage' ) && false === stripos( $js, 'sessionStorage' ), 'runtime has no browser persistence path' );
$viewer_js = file_get_contents( dirname( __DIR__ ) . '/plugins/nadlan-config/assets/flagship-v3/flagship-viewer.js' );
fixture_assert( is_string( $viewer_js ) && false !== strpos( $viewer_js, 'target.origin !== window.location.origin' ), 'viewer enforces a same-origin model URL' );
fixture_assert( false !== strpos( $viewer_js, 'method: "GET"' ) && false === strpos( $viewer_js, 'method: "POST"' ), 'viewer network path is read-only GET' );
$playground_js = file_get_contents( dirname( __DIR__ ) . '/plugins/nadlan-config/assets/flagship-v3/flagship-playground.js' );
fixture_assert( is_string( $playground_js ) && false !== strpos( $playground_js, 'view: "schematic_live_map"' ) && false !== strpos( $playground_js, 'comments: "visual_annotation_request"' ), 'generic playground exposes exactly the four approved permanent doors and safe comment token' );
fixture_assert( false !== strpos( $playground_js, 'config.experienceAssets.interior.scenes.concat(config.experienceAssets.facilities.scenes)' ), 'facilities remain selectable inside the Interior experience rather than a fifth tile' );
fixture_assert( false !== strpos( $playground_js, 'document.body.appendChild(dialog)' ) && false !== strpos( $playground_js, 'opts.restoreModelState(cloneSnapshot(state.snapshot.modelState))' ), 'playground fullscreen and Back restore the exact host model/page state' );
fixture_assert( false !== strpos( $playground_js, 'allowedEvidenceReferenceIds' ) && false !== strpos( $playground_js, 'allowedAssetPrefix' ) && false !== strpos( $playground_js, 'placement_confidence' ), 'canonical runtime consumes trusted evidence/prefix options and numeric confidence' );
fixture_assert( false === stripos( $playground_js, 'olp' ), 'canonical runtime contains no internal delivery terminology' );
fixture_assert( 0 === preg_match( '/\b(?:window\.fetch|fetch\s*\(|sendBeacon\s*\(|new\s+XMLHttpRequest|localStorage\.|sessionStorage\.)/', $playground_js ), 'playground owns no executable network, write or persistence primitive' );
fixture_assert( hash_equals( hash_file( 'sha256', dirname( __DIR__ ) . '/assets/showroom/flagship-showroom-runtime.js' ), hash_file( 'sha256', dirname( __DIR__ ) . '/plugins/nadlan-config/assets/flagship-v3/flagship-playground.js' ) ), 'plugin playground runtime is an exact canonical byte copy' );
fixture_assert( hash_equals( hash_file( 'sha256', dirname( __DIR__ ) . '/assets/showroom/flagship-showroom.css' ), hash_file( 'sha256', dirname( __DIR__ ) . '/plugins/nadlan-config/assets/flagship-v3/flagship-playground.css' ) ), 'plugin playground CSS is an exact canonical byte copy' );

$experience_manifest_path = dirname( __DIR__ ) . '/assets/projects/einstein-tower/experience/manifest.json';
fixture_assert( is_readable( $experience_manifest_path ), 'owner-approved experience manifest is available' );
$experience_manifest = json_decode( (string) file_get_contents( $experience_manifest_path ), true, 64, JSON_THROW_ON_ERROR );
$registry_contract = nadlan_flagship_v3_contract( 'einstein-tower-6885-32' );
$plugin_project_path = dirname( __DIR__ ) . '/plugins/nadlan-config/assets/flagship-v3/projects/einstein-tower';
$anchor_projection = static function ( array $anchor ): array {
	return array(
		'hotspot_id' => $anchor['hotspot_id'], 'tool_id' => $anchor['tool_id'], 'open_surface_tool_id' => $anchor['open_surface_tool_id'],
		'scene_ids' => $anchor['scene_ids'], 'model_component_ids' => $anchor['model_component_ids'], 'illustrative_zone_id' => $anchor['illustrative_zone_id'],
		'position' => $anchor['position'], 'surface_normal' => $anchor['surface_normal'],
		'visual_offset_along_normal_m' => $anchor['visual_offset_along_normal_m'], 'confidence' => $anchor['confidence'], 'placement_confidence' => $anchor['placement_confidence'],
	);
};
$wp_anchor_projection = array_map( $anchor_projection, $runtime_config['playground']['experience_mapping']['anchors'] );
$manifest_anchor_projection = array_map( $anchor_projection, $experience_manifest['mapping_policy']['anchors'] );
fixture_assert( fixture_json( $manifest_anchor_projection ) === fixture_json( $wp_anchor_projection ), 'WordPress runtime anchors exactly match frozen GLB/manifest hotspot IDs, scenes, coordinates and model zones' );
$authorized_by_id = array();
foreach ( $registry_contract['authorized_experience_assets'] as $authorized ) {
	$authorized_by_id[ $authorized['asset_id'] ] = $authorized;
}
fixture_assert( 4 === count( $authorized_by_id ), 'registry authorizes exactly the four reviewed experience assets' );
foreach ( $experience_manifest['assets'] as $manifest_asset ) {
	$asset_id = (string) $manifest_asset['asset_id'];
	fixture_assert( isset( $authorized_by_id[ $asset_id ] ), 'manifest asset is in the WordPress allow-list: ' . $asset_id );
	fixture_assert( (string) $manifest_asset['scene_id'] === (string) $authorized_by_id[ $asset_id ]['scene_id'], 'manifest and WordPress scene IDs agree: ' . $asset_id );
	fixture_assert( hash_equals( (string) $manifest_asset['sha256'], (string) $authorized_by_id[ $asset_id ]['fullscreen_sha256'] ), 'manifest and registry hashes agree: ' . $asset_id );
	$local_asset_path = $plugin_project_path . '/experience/' . $manifest_asset['file'];
	fixture_assert( is_readable( $local_asset_path ) && (int) $manifest_asset['bytes'] === filesize( $local_asset_path ) && hash_equals( (string) $manifest_asset['sha256'], hash_file( 'sha256', $local_asset_path ) ), 'plugin-local asset bytes match the reviewed manifest: ' . $asset_id );
}

foreach ( $registry_contract['authorized_representations'] as $authorized_representation ) {
	$local_representation_path = $plugin_project_path . '/' . $authorized_representation['file'];
	fixture_assert( is_readable( $local_representation_path )
		&& (int) $authorized_representation['bytes'] === filesize( $local_representation_path )
		&& hash_equals( (string) $authorized_representation['sha256'], hash_file( 'sha256', $local_representation_path ) ), 'plugin-local model/poster bytes match the frozen registry: ' . $authorized_representation['role'] );
}

fwrite( STDOUT, "flagship-v3 PHP fixture: PASS\n" );
