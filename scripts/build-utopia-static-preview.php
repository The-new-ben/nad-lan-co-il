<?php
/**
 * Build five local UTOPIA previews from the exact release article and payload
 * helpers. This is a static QA harness only; it does not contact WordPress.
 */

declare( strict_types=1 );

$root = dirname( __DIR__ );
define( 'ABSPATH', $root . DIRECTORY_SEPARATOR );
define( 'OBJECT', 'OBJECT' );

function add_action() {}
function add_filter() {}
function trailingslashit( $value ) { return rtrim( (string) $value, '/\\' ) . '/'; }
function plugins_url( $path = '' ) { return '/plugins/nadlan-config/' . ltrim( (string) $path, '/' ); }
function sanitize_key( $value ) { return strtolower( preg_replace( '/[^a-z0-9_\-]/', '', (string) $value ) ); }
function sanitize_text_field( $value ) { return trim( strip_tags( (string) $value ) ); }
function wp_json_encode( $value, $flags = 0 ) { return json_encode( $value, $flags ); }
function nadlan_showroom_engine_base_url() { return '/plugins/nadlan-config/assets/showroom-engine/'; }
function wp_dequeue_script() {}
function wp_enqueue_style() {}
function wp_enqueue_script() {}
function wp_script_add_data() {}
function get_option( $key, $default = '' ) { return $default; }
function rest_url( $path = '' ) { return '/wp-json/' . ltrim( (string) $path, '/' ); }
function home_url( $path = '' ) { return '/' . ltrim( (string) $path, '/' ); }
function esc_attr( $value ) { return htmlspecialchars( (string) $value, ENT_QUOTES, 'UTF-8' ); }
function esc_html( $value ) { return htmlspecialchars( (string) $value, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $value ) { return htmlspecialchars( (string) $value, ENT_QUOTES, 'UTF-8' ); }
function esc_url_raw( $value ) { return (string) $value; }
function number_format_i18n( $value, $decimals = 0 ) { return number_format( (float) $value, (int) $decimals, '.', ',' ); }

$preview_lang = 'he';
function get_queried_object_id() { return 4749; }
function get_post_type() { return 'nadlan_project'; }
function get_post_field( $field, $post_id = 0 ) {
	global $preview_lang;
	if ( $field === 'post_name' ) { return 'utopia-sde-dov' . ( $preview_lang === 'he' ? '' : '-' . $preview_lang ); }
	return '';
}
function get_the_title() {
	global $preview_lang;
	$c = nadlan_utopia_copy( $preview_lang );
	return $c['post_title'];
}
function get_post_meta( $post_id, $key, $single = true ) {
	global $preview_lang;
	if ( $key === '_nadlan_utopia_identity' ) { return nadlan_utopia_identity_marker( $preview_lang ); }
	if ( $key === 'lat' ) { return 0; }
	if ( $key === 'lng' ) { return 0; }
	return '';
}
function get_page_by_path( $slug ) {
	$slugs = array_flip( nadlan_utopia_release_slugs() );
	if ( ! isset( $slugs[ $slug ] ) ) { return null; }
	return (object) array( 'ID' => 4749 + array_search( $slug, array_keys( $slugs ), true ), 'post_name' => $slug );
}
function get_post_status() { return 'publish'; }
function get_permalink( $post_id ) {
	foreach ( nadlan_utopia_release_slugs() as $lang => $slug ) {
		if ( $post_id >= 4749 && $post_id <= 4753 ) {
			$index = $post_id - 4749;
			$languages = array_keys( nadlan_utopia_release_slugs() );
			return '/docs/previews/utopia-sde-dov-' . $languages[ $index ] . '-preview.html';
		}
	}
	return '/docs/previews/utopia-sde-dov-he-preview.html';
}

require_once $root . '/plugins/nadlan-config/inc/utopia-sde-dov.php';

$langs = array( 'he', 'en', 'fr', 'ru', 'ar' );
$out_dir = $root . '/docs/previews';
if ( ! is_dir( $out_dir ) ) { mkdir( $out_dir, 0777, true ); }
$public_urls = array();
foreach ( nadlan_utopia_release_slugs() as $public_lang => $public_slug ) {
	$public_urls[ $public_lang ] = 'https://nad-lan.co.il/projects/' . $public_slug . '/';
}

foreach ( $langs as $lang ) {
	$preview_lang = $lang;
	$c = nadlan_utopia_copy( $lang );
	$article_path = $root . '/content/projects/utopia-sde-dov/article-' . $lang . '.html';
	$article = nadlan_utopia_rewrite_asset_urls( (string) file_get_contents( $article_path ) );
	preg_match( '#<header\b[^>]*class="[^"]*nadlan-project-lead[^"]*"[^>]*>.*?</header>#is', $article, $lead_match );
	$lead = isset( $lead_match[0] ) ? $lead_match[0] : '';
	$rest = $lead !== '' ? str_replace( $lead, '', $article ) : $article;
	$rest = preg_replace( '#^\s*<article\b[^>]*>#i', '', $rest );
	$rest = preg_replace( '#</article>\s*$#i', '', (string) $rest );

	$showroom = nadlan_utopia_showroom_render( 4749 );
	$dir = in_array( $lang, array( 'he', 'ar' ), true ) ? 'rtl' : 'ltr';
	$locale = array( 'he' => 'he-IL', 'en' => 'en-US', 'fr' => 'fr-FR', 'ru' => 'ru-RU', 'ar' => 'ar' )[ $lang ];
	$alternate_links = '';
	foreach ( $public_urls as $alternate_lang => $alternate_url ) {
		$alternate_links .= '<link rel="alternate" hreflang="' . $alternate_lang . '" href="' . $alternate_url . '">';
	}
	$alternate_links .= '<link rel="alternate" hreflang="x-default" href="' . $public_urls['he'] . '">';
	$html = '<!doctype html><html lang="' . $locale . '" dir="' . $dir . '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="google" content="notranslate">'
		. '<title>' . htmlspecialchars( $c['seo_title'], ENT_QUOTES, 'UTF-8' ) . '</title>'
		. '<meta name="description" content="' . htmlspecialchars( $c['seo_desc'], ENT_QUOTES, 'UTF-8' ) . '">'
		. '<link rel="canonical" href="' . $public_urls[ $lang ] . '">'
		. $alternate_links
		. '<link rel="stylesheet" href="/plugins/nadlan-config/assets/showroom-engine/tokens.css">'
		. '<link rel="stylesheet" href="/plugins/nadlan-config/assets/showroom-engine/showroom.css">'
		. '<link rel="stylesheet" href="/plugins/nadlan-config/assets/showroom-engine/editorial.css">'
		. '<link rel="stylesheet" href="/plugins/nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia.css">'
		. '<style>body{margin:0;background:#fbf8f1}</style>'
		. '<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.3.1/model-viewer.min.js"></script></head><body>'
		. '<div class="nadlan-project-article nadlan-guide nadlan-project-lead-wrap utopia-project-content">' . $lead . '</div>'
		. $showroom
		. '<div class="nadlan-project-article nadlan-guide utopia-project-content">' . $rest . '</div>'
		. '<script src="/plugins/nadlan-config/assets/showroom-engine/projects/utopia-sde-dov/utopia-showroom.js"></script>'
		. '</body></html>';
	$html = (string) preg_replace( '/[ \t]+(?=\r?$)/m', '', $html );
	file_put_contents( $out_dir . '/utopia-sde-dov-' . $lang . '-preview.html', $html );
}

echo "Built five UTOPIA previews in docs/previews\n";
