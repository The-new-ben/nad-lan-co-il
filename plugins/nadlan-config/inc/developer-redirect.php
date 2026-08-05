<?php
/**
 * Direct line to the developer.
 *
 * Owner decision 2026-08-05: until each developer is addressed personally,
 * project pages must offer a DIRECT route to the developer's own project
 * page, so no developer gets the impression that leads are being captured
 * on their name. Where `developer_official_url` meta exists, a prominent
 * in-flow strip renders near the top of the page: name the developer, link
 * their official page, external and nofollow. Additive only - the site's
 * own enquiry surfaces stay untouched until the owner's outreach round
 * settles each relationship.
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) {
		return $content;
	}
	static $done = false;
	if ( $done ) {
		return $content;
	}
	$done = true;
	$url = esc_url( (string) get_post_meta( get_the_ID(), 'developer_official_url', true ) );
	if ( '' === $url ) {
		return $content;
	}
	$dev  = trim( (string) get_post_meta( get_the_ID(), 'developer_name', true ) );
	$lang = function_exists( 'nadlan_current_lang' ) ? nadlan_current_lang() : 'he';
	$strings = array(
		'he' => array( 'לפנייה ישירה ליזם', 'לעמוד הרשמי של %s', 'לעמוד הרשמי של הפרויקט' ),
		'en' => array( 'Contact the developer directly', 'Official page of %s', 'The project\'s official page' ),
		'fr' => array( 'Contacter directement le promoteur', 'Page officielle de %s', 'La page officielle du projet' ),
		'ru' => array( 'Напрямую к застройщику', 'Официальная страница %s', 'Официальная страница проекта' ),
		'ar' => array( 'تواصل مباشرة مع المطور', 'الصفحة الرسمية لـ %s', 'الصفحة الرسمية للمشروع' ),
	);
	$s    = isset( $strings[ $lang ] ) ? $strings[ $lang ] : $strings['he'];
	$rtl  = in_array( $lang, array( 'he', 'ar' ), true );
	$lbl  = ( '' !== $dev ) ? sprintf( $s[1], $dev ) : $s[2];
	$html = '<aside class="nl-devlink" dir="' . ( $rtl ? 'rtl' : 'ltr' ) . '">'
		. '<span>' . esc_html( $s[0] ) . '</span>'
		. '<a href="' . $url . '" target="_blank" rel="nofollow noopener">' . esc_html( $lbl ) . '</a>'
		. '</aside>';

	/* sit right under the intent-first opening block (lead, notice, price
	   line) when it exists; otherwise prepend */
	$pos = 0;
	if ( 0 === strpos( $content, '<div class="nl-lead">' ) ) {
		$pos = strpos( $content, '</div>' );
		$pos = ( false === $pos ) ? 0 : $pos + 6;
		if ( substr( $content, $pos, 28 ) === '<aside class="nl-projnotice"' ) {
			$e = strpos( $content, '</aside>', $pos );
			if ( false !== $e ) {
				$pos = $e + 8;
			}
		}
		if ( substr( $content, $pos, 22 ) === '<p class="nl-areaprice' ) {
			$e = strpos( $content, '</p>', $pos );
			if ( false !== $e ) {
				$pos = $e + 4;
			}
		}
	}
	return substr( $content, 0, $pos ) . $html . substr( $content, $pos );
}, 23 );

add_action( 'wp_enqueue_scripts', function () {
	if ( ! is_singular( 'nadlan_project' ) ) {
		return;
	}
	wp_register_style( 'nadlan-devlink', false, array(), NADLAN_CONFIG_VERSION );
	wp_enqueue_style( 'nadlan-devlink' );
	wp_add_inline_style(
		'nadlan-devlink',
		'.nl-devlink{display:flex;align-items:center;gap:12px;flex-wrap:wrap;background:#FFFDF8;' .
		'border:1px solid #E2DCD0;border-radius:10px;padding:10px 14px;margin:0 0 18px;' .
		'font-family:Heebo,system-ui,sans-serif;font-size:13.5px}' .
		'.nl-devlink span{color:#4B4639;font-weight:600}' .
		'.nl-devlink a{background:transparent;border:1px solid #9C7A3C;color:#6D5A2E;text-decoration:none;' .
		'font-weight:700;border-radius:8px;padding:7px 14px}'
	);
}, 22 );
