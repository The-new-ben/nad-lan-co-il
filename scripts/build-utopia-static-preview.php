<?php
/**
 * Build five local UTOPIA previews from the exact release article and payload
 * helpers. This is a static QA harness only; it does not contact WordPress.
 */

declare( strict_types=1 );

$root = dirname( __DIR__ );
define( 'ABSPATH', $root . DIRECTORY_SEPARATOR );

function add_action() {}
function add_filter() {}
function trailingslashit( $value ) { return rtrim( (string) $value, '/\\' ) . '/'; }
function plugins_url( $path = '' ) { return '/plugins/nadlan-config/' . ltrim( (string) $path, '/' ); }
function sanitize_key( $value ) { return strtolower( preg_replace( '/[^a-z0-9_\-]/', '', (string) $value ) ); }
function wp_json_encode( $value, $flags = 0 ) { return json_encode( $value, $flags ); }
function nadlan_showroom_engine_base_url() { return '/plugins/nadlan-config/assets/showroom-engine/'; }

require_once $root . '/plugins/nadlan-config/inc/utopia-sde-dov.php';

$langs = array( 'he', 'en', 'fr', 'ru', 'ar' );
$lang_urls = array();
foreach ( $langs as $lang ) {
	$lang_urls[ $lang ] = '/docs/previews/utopia-sde-dov-' . $lang . '-preview.html';
}

$out_dir = $root . '/docs/previews';
if ( ! is_dir( $out_dir ) ) { mkdir( $out_dir, 0777, true ); }

foreach ( $langs as $lang ) {
	$c = nadlan_utopia_copy( $lang );
	$article_path = $root . '/content/projects/utopia-sde-dov/article-' . $lang . '.html';
	$article = (string) file_get_contents( $article_path );
	preg_match( '#<header\b[^>]*class="[^"]*nadlan-project-lead[^"]*"[^>]*>.*?</header>#is', $article, $lead_match );
	$lead = isset( $lead_match[0] ) ? $lead_match[0] : '';
	$rest = $lead !== '' ? str_replace( $lead, '', $article ) : $article;
	$rest = preg_replace( '#^\s*<article\b[^>]*>#i', '', $rest );
	$rest = preg_replace( '#</article>\s*$#i', '', (string) $rest );

	$slug = 'utopia-sde-dov' . ( $lang === 'he' ? '' : '-' . $lang );
	$project = array(
		'slug' => $slug,
		'wp_id' => 4749,
		'name' => $c['post_title'],
		'name_key' => $c['post_title'],
		'area' => 'area_' . $slug,
		'content' => array( $lang => array( 'tagline' => $c['excerpt'] ), 'en' => array( 'tagline' => $c['excerpt'] ) ),
		'sub' => $c['excerpt'],
		'floors' => 34,
		'floor_height_m' => 3.15,
		'frame_radius_m' => 220,
		'model_glb' => '/plugins/nadlan-config/assets/showroom-engine/models/utopia-rich-v1.glb',
		'model_generic' => false,
		'model_poster' => '/plugins/nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia-concept-exterior-v1.webp',
		'hero_image' => '/plugins/nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia-concept-exterior-v1.webp',
		'default_interior' => '/plugins/nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia-concept-interior-v1.webp',
		'facade_image' => '',
		'facade_concept_image' => '/plugins/nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia-concept-exterior-v1.webp',
		'facade_is_concept' => true,
		'concept' => true,
		'orientation' => $c['orientation'],
		'geo' => array( 'lat' => 32.105979267060775, 'lng' => 34.78452395444623, 'confidence' => 'planning-lot-centroid' ),
		'url' => $lang_urls[ $lang ],
		'lang_urls' => $lang_urls,
		'self_lang' => $lang,
		'price' => array( 'avg_psqm' => 0, 'source' => $c['price_note'], 'date' => '', 'comps' => array() ),
		'faq' => array(),
		'units' => array(),
		'units_total' => 337,
		'buildings' => nadlan_utopia_buildings( $lang ),
		'sample_plans' => nadlan_utopia_sample_plans( $lang ),
		'building_mode' => $c['building_mode'],
		'media_note' => $c['media_note'],
		'media_alt' => $c['media_alt'],
		'default_orbit' => '-28deg 68deg 220m',
		'default_target' => '0m 42m 0m',
		'public_home_url' => '/',
		'suppress_empty_seo' => true,
		'preserve_document_title' => true,
		'lock_server_language' => true,
	);
	$payload = array(
		'config' => array(
			'lead_endpoint' => '',
			'brochure_endpoint' => '',
			'cotour_endpoint' => '',
			'whatsapp' => '',
			'phone' => '',
			'mapbox_token' => '',
			'demo' => false,
			'default_project' => $slug,
			'default_lang' => $lang,
			'languages' => $langs,
			'rtl_languages' => array( 'he', 'ar' ),
			'home_url' => '/',
			'studio' => 'off',
		),
		'projects' => array( $slug => $project ),
		'order' => array( $slug ),
		'areas' => array(
			'area_' . $slug => array(
				'label_key' => 'area_sde_dov',
				'blurb_key' => 'area_sde_dov_blurb',
				'map' => array( 'center' => $project['geo'], 'project_pin' => array( 'x' => 50, 'y' => 50 ), 'pins' => array(), 'coast_x' => 16 ),
				'spoke_groups' => array(),
				'stats' => array(),
			),
		),
		'spokes' => array(),
	);
	$dir = in_array( $lang, array( 'he', 'ar' ), true ) ? 'rtl' : 'ltr';
	$locale = array( 'he' => 'he-IL', 'en' => 'en-US', 'fr' => 'fr-FR', 'ru' => 'ru-RU', 'ar' => 'ar' )[ $lang ];
	$html = '<!doctype html><html lang="' . $locale . '" dir="' . $dir . '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
		. '<title>' . htmlspecialchars( $c['seo_title'], ENT_QUOTES, 'UTF-8' ) . '</title>'
		. '<meta name="description" content="' . htmlspecialchars( $c['seo_desc'], ENT_QUOTES, 'UTF-8' ) . '">'
		. '<link rel="stylesheet" href="/plugins/nadlan-config/assets/showroom-engine/tokens.css">'
		. '<link rel="stylesheet" href="/plugins/nadlan-config/assets/showroom-engine/showroom.css">'
		. '<link rel="stylesheet" href="/plugins/nadlan-config/assets/showroom-engine/editorial.css">'
		. '<link rel="stylesheet" href="/plugins/nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia.css">'
		. '<style>body{margin:0;background:#fbf8f1}</style>'
		. '<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.3.1/model-viewer.min.js"></script></head><body>'
		. '<div class="nadlan-project-article nadlan-guide nadlan-project-lead-wrap utopia-project-content">' . $lead . '</div>'
		. '<div id="nl-root" data-page="project"></div>'
		. '<div class="nadlan-project-article nadlan-guide utopia-project-content">' . $rest . '</div>'
		. '<script src="/plugins/nadlan-config/assets/showroom-engine/i18n.js"></script>'
		. '<script src="/plugins/nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia-i18n.js"></script>'
		. '<script>window.NADLAN_SHOWROOM=' . json_encode( $payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . ';</script>'
		. '<script src="/plugins/nadlan-config/assets/showroom-engine/engine.js"></script>'
		. '</body></html>';
	$html = (string) preg_replace( '/[ \t]+(?=\r?$)/m', '', $html );
	file_put_contents( $out_dir . '/utopia-sde-dov-' . $lang . '-preview.html', $html );
}

echo "Built five UTOPIA previews in docs/previews\n";
