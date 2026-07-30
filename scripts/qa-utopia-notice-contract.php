<?php
/**
 * Isolated contract test for UTOPIA's project non-affiliation notice.
 *
 * The test executes the actual helper functions extracted from the release
 * source. It does not bootstrap WordPress or contact production.
 */

declare(strict_types=1);

function qa_extract_function( string $source, string $name ): string {
	$needle = 'function ' . $name;
	$start  = strpos( $source, $needle );
	if ( false === $start ) {
		throw new RuntimeException( 'Missing function ' . $name );
	}
	$brace = strpos( $source, '{', $start );
	if ( false === $brace ) {
		throw new RuntimeException( 'Missing opening brace for ' . $name );
	}
	$depth  = 0;
	$length = strlen( $source );
	for ( $index = $brace; $index < $length; $index++ ) {
		if ( '{' === $source[ $index ] ) {
			$depth++;
		} elseif ( '}' === $source[ $index ] ) {
			$depth--;
			if ( 0 === $depth ) {
				return substr( $source, $start, $index - $start + 1 );
			}
		}
	}
	throw new RuntimeException( 'Unclosed function ' . $name );
}

function qa_assert( bool $condition, string $message ): void {
	if ( ! $condition ) {
		throw new RuntimeException( $message );
	}
}

function esc_html( $value ): string {
	return htmlspecialchars( (string) $value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8' );
}

$GLOBALS['qa_utopia_meta'] = array();

function get_post_meta( $post_id, $key, $single = false ) {
	unset( $single );
	return $GLOBALS['qa_utopia_meta'][ $post_id ][ $key ] ?? '';
}

function nadlan_utopia_copy( $lang ): array {
	return array( 'developer' => 'fallback-' . $lang );
}

function nadlan_utopia_rewrite_asset_urls( $html ): string {
	return (string) $html;
}

function wp_strip_all_tags( $html ): string {
	return strip_tags( (string) $html );
}

$root    = dirname( __DIR__ );
$legal   = file_get_contents( $root . '/plugins/nadlan-config/inc/legal-notice.php' );
$utopia  = file_get_contents( $root . '/plugins/nadlan-config/inc/utopia-sde-dov.php' );
$results = array();

qa_assert( false !== $legal && false !== $utopia, 'Release sources could not be read.' );
qa_assert(
	1 === preg_match( "/add_action\\(\\s*'wp'\\s*,\\s*'nadlan_utopia_set_request_language'\\s*,\\s*1\\s*\\)/", $utopia ),
	'UTOPIA language context is not registered at wp priority 1.'
);
qa_assert(
	false !== strpos( $utopia, "return \$notice . nadlan_utopia_compose_public_content" ),
	'Final UTOPIA composition does not preserve the project notice.'
);

eval( qa_extract_function( $legal, 'nadlan_project_notice_strings' ) );
eval( qa_extract_function( $utopia, 'nadlan_utopia_project_notice_html' ) );
eval( qa_extract_function( $utopia, 'nadlan_utopia_compose_public_content' ) );

$developers = array(
	'he' => 'קבוצת נחמיאס',
	'en' => 'Nahmias Group',
	'fr' => 'Groupe Nahmias',
	'ru' => 'Группа Nahmias',
	'ar' => 'مجموعة نحمياس',
);

$post_id = 100;
foreach ( $developers as $lang => $developer ) {
	$GLOBALS['qa_utopia_meta'][ $post_id ] = array( 'developer_name' => $developer );
	$html    = nadlan_utopia_project_notice_html( $post_id, $lang );
	$strings = nadlan_project_notice_strings( $lang );
	$dir     = in_array( $lang, array( 'he', 'ar' ), true ) ? 'rtl' : 'ltr';
	$pass    = 1 === substr_count( $html, 'nl-projnotice' )
		&& false !== strpos( $html, 'dir="' . $dir . '"' )
		&& false !== strpos( $html, esc_html( $strings[0] ) )
		&& false !== strpos( $html, esc_html( $developer ) );
	qa_assert( $pass, 'Localized project notice failed for ' . $lang . '.' );
	$results[ $lang ] = array(
		'pass'   => true,
		'dir'    => $dir,
		'sha256' => hash( 'sha256', $html ),
	);
	$post_id++;
}

$raw = '<aside class="nl-projnotice"><b>duplicate</b></aside>'
	. '<header class="nadlan-project-lead"><p>Lead</p></header>'
	. '<h2>Overview</h2><p>Body</p>';
$composed = nadlan_utopia_compose_public_content(
	$raw,
	100,
	'<section id="utopia-showroom"></section>'
);
$composition = array(
	'embedded_notice_removed' => 0 === substr_count( $composed, 'nl-projnotice' ),
	'lead_before_showroom'     => strpos( $composed, 'Lead' ) < strpos( $composed, 'utopia-showroom' ),
	'showroom_before_body'     => strpos( $composed, 'utopia-showroom' ) < strpos( $composed, 'Overview' ),
);
foreach ( $composition as $name => $pass ) {
	qa_assert( $pass, 'Composition contract failed: ' . $name );
}

echo json_encode(
	array(
		'schema'      => 'nadlan-utopia-notice-contract/v1',
		'languages'   => $results,
		'composition' => $composition,
		'pass'        => true,
	),
	JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT
) . PHP_EOL;
