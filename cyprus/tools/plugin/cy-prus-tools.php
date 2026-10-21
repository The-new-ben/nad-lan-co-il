<?php
/**
 * Plugin Name: CY-PRUS Tools
 * Description: Interactive tools (CY-PRUS Instruments) on selected guide pages: the full purchase-cost calculator, the net rental yield calculator the bank-account documents wizard the 5% VAT eligibility checker the residency-by-investment checker the Israel-Cyprus tax map and the title-deeds risk check. Each tool is printed by the server with a worked example, uses dated official rules, and loads nothing from third parties.
 * Version: 0.7.0
 * Author: CY-PRUS
 * Requires at least: 6.5
 * Requires PHP: 7.4
 * Text Domain: cy-prus-tools
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'CYPT_VERSION', '0.7.0' );
define( 'CYPT_DIR', plugin_dir_path( __FILE__ ) );
define( 'CYPT_URL', plugin_dir_url( __FILE__ ) );

/** The tools and the existing pages that host them (registry.json, written by the build). */
function cypt_registry() {
	static $reg = null;
	if ( null === $reg ) {
		$reg = json_decode( (string) @file_get_contents( CYPT_DIR . 'registry.json' ), true );
		if ( ! is_array( $reg ) ) {
			$reg = array();
		}
	}
	return $reg;
}

function cypt_tools_for( $post_id ) {
	$out = array();
	foreach ( cypt_registry() as $t ) {
		if ( isset( $t['page_id'] ) && (int) $t['page_id'] === (int) $post_id ) {
			$out[] = $t;
		}
	}
	return $out;
}

function cypt_read( $rel ) {
	$file = CYPT_DIR . $rel;
	return is_readable( $file ) ? (string) file_get_contents( $file ) : '';
}

function cypt_is_host() {
	return ! is_admin() && is_singular( 'page' ) && (bool) cypt_tools_for( get_queried_object_id() );
}

/**
 * Places each tool after the n-th paragraph of its host page (the page's own answer comes first) and its FAQ at the end.
 * Adds only; never removes or rewrites the page's text. With fewer paragraphs than expected, the tool goes at the end.
 */
add_filter(
	'the_content',
	function ( $content ) {
		static $done = array();
		if ( ! cypt_is_host() ) {
			return $content;
		}
		$id = (int) get_queried_object_id();
		if ( (int) get_the_ID() !== $id || isset( $done[ $id ] ) ) {
			return $content;
		}
		$done[ $id ] = true;
		foreach ( cypt_tools_for( $id ) as $t ) {
			$section = cypt_read( 'tools/' . $t['id'] . '/section.' . $t['lang'] . '.html' );
			if ( '' === $section ) {
				continue;
			}
			$pos = 0;
			for ( $i = 0; $i < max( 1, (int) $t['after_paragraph'] ); $i++ ) {
				$j = strpos( $content, '</p>', $pos );
				if ( false === $j ) {
					$pos = -1;
					break;
				}
				$pos = $j + 4;
			}
			$content = ( $pos > 0 )
				? substr( $content, 0, $pos ) . "\n" . $section . "\n" . substr( $content, $pos )
				: $content . "\n" . $section;
			$faq = cypt_read( 'tools/' . $t['id'] . '/faq.' . $t['lang'] . '.html' );
			if ( '' !== $faq ) {
				$content .= "\n" . $faq;
			}
		}
		return $content;
	},
	20
);

/** Styles, self-hosted fonts and scripts, only on host pages. */
add_action(
	'wp_enqueue_scripts',
	function () {
		if ( ! cypt_is_host() ) {
			return;
		}
		wp_enqueue_style( 'cypt-fonts', CYPT_URL . 'assets/fonts.css', array(), CYPT_VERSION );
		wp_enqueue_style( 'cypt-style', CYPT_URL . 'assets/style.css', array( 'cypt-fonts' ), CYPT_VERSION );
		foreach ( cypt_tools_for( get_queried_object_id() ) as $t ) {
			$deps    = array();
			$engines = ( isset( $t['engines'] ) && is_array( $t['engines'] ) ) ? $t['engines'] : array( $t['id'] );
			foreach ( $engines as $e ) {
				$h = 'cypt-engine-' . sanitize_key( $e );
				wp_enqueue_script( $h, CYPT_URL . 'assets/engine-' . sanitize_key( $e ) . '.js', $deps, CYPT_VERSION, array( 'in_footer' => true, 'strategy' => 'defer' ) );
				$deps[] = $h;
			}
			wp_enqueue_script( 'cypt-ui-' . $t['id'], CYPT_URL . 'assets/ui-' . $t['id'] . '.js', $deps, CYPT_VERSION, array( 'in_footer' => true, 'strategy' => 'defer' ) );
		}
	}
);

/** Structured data for each tool (WebApplication and the FAQ that is visible on the page). */
add_action(
	'wp_head',
	function () {
		if ( ! cypt_is_host() ) {
			return;
		}
		foreach ( cypt_tools_for( get_queried_object_id() ) as $t ) {
			$ld = cypt_read( 'tools/' . $t['id'] . '/ld.' . $t['lang'] . '.json' );
			if ( '' !== $ld && null !== json_decode( $ld ) && false === stripos( $ld, '</script' ) ) {
				echo '<script type="application/ld+json">' . $ld . "</script>\n"; // phpcs:ignore WordPress.Security.EscapeOutput
			}
		}
	},
	30
);

/** Public version check: GET /wp-json/cy-prus-tools/v1/health */
add_action(
	'rest_api_init',
	function () {
		register_rest_route(
			'cy-prus-tools/v1',
			'/health',
			array(
				'methods'             => 'GET',
				'permission_callback' => '__return_true',
				'callback'            => function () {
					$tools = array();
					foreach ( cypt_registry() as $t ) {
						$tools[] = array( 'id' => $t['id'], 'page_id' => (int) $t['page_id'], 'lang' => $t['lang'] );
					}
					return array( 'version' => CYPT_VERSION, 'tools' => $tools );
				},
			)
		);
	}
);
