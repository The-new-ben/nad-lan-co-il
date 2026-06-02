<?php
/**
 * nadlan-config — Dynamic OG image for social sharing (v1.40.0 / shark #16)
 *
 * When someone shares a profile/term/article on WhatsApp/Twitter/FB, the
 * preview card shows an image. We don't have hand-made images for 2,700
 * contractors, so we generate SVG previews on the fly — branded cards that
 * look professional + carry the title.
 *
 * Endpoint: GET /nadlan/v1/og/<post_id>.svg
 * Sets og:image / twitter:image to that URL on profile + term + project pages.
 *
 * Why SVG (not PNG): zero dependencies (no Imagick/GD heavy work), browsers
 * render fine, social-card scrapers handle SVG. Lightning fast.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_og_supported_pt' ) ) {
	function nadlan_og_supported_pt( $pt ) {
		return in_array( $pt, array( 'nadlan_professional', 'nadlan_project', 'nadlan_term' ), true );
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/og/(?P<id>\d+)\.svg', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function ( $req ) {
			$id = (int) $req['id'];
			$post = get_post( $id );
			if ( ! $post || ! nadlan_og_supported_pt( $post->post_type ) ) {
				return new WP_Error( 'not_found', 'not_found', array( 'status' => 404 ) );
			}
			$title = get_the_title( $post );
			$kind = array(
				'nadlan_professional' => 'בעל מקצוע מאומת',
				'nadlan_project' => 'פרויקט נדל"ן',
				'nadlan_term' => 'מילון נדל"ן',
			)[ $post->post_type ];
			$color = '#9C7A3C';
			if ( $post->post_type === 'nadlan_professional' && function_exists( 'nadlan_dir_prof_meta' ) ) {
				$pm = nadlan_dir_prof_meta( (string) get_post_meta( $id, 'profession', true ) );
				$color = $pm['color'];
			} elseif ( $post->post_type === 'nadlan_project' && function_exists( 'nadlan_dir_pt_meta' ) ) {
				$pm = nadlan_dir_pt_meta( (string) get_post_meta( $id, 'project_type', true ) );
				$color = $pm['color'];
			}
			// title fits ~28 chars per line; soft-wrap
			$lines = array(); $line = '';
			foreach ( preg_split( '/\s+/u', $title ) as $w ) {
				if ( mb_strlen( $line . ' ' . $w ) > 26 ) { $lines[] = $line; $line = $w; }
				else { $line = trim( $line . ' ' . $w ); }
			}
			if ( $line !== '' ) { $lines[] = $line; }
			$lines = array_slice( $lines, 0, 3 );

			$svg = '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">'
				 . '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1B1A17"/><stop offset="1" stop-color="#3a3329"/></linearGradient></defs>'
				 . '<rect width="1200" height="630" fill="url(#bg)"/>'
				 . '<rect x="0" y="0" width="1200" height="14" fill="' . esc_attr( $color ) . '"/>'
				 . '<text x="1140" y="80" font-family="serif" font-size="24" fill="#F3D9A6" text-anchor="end" direction="rtl">' . esc_html( $kind ) . '</text>';
			$y = 240;
			foreach ( $lines as $ln ) {
				$svg .= '<text x="1140" y="' . $y . '" font-family="serif" font-size="72" font-weight="600" fill="#fff" text-anchor="end" direction="rtl">' . esc_html( $ln ) . '</text>';
				$y += 90;
			}
			$svg .= '<text x="1140" y="580" font-family="sans-serif" font-size="28" fill="rgba(255,255,255,.6)" text-anchor="end" direction="rtl">נדל"ן חכם · nad-lan.co.il</text>';
			$svg .= '</svg>';

			$resp = new WP_REST_Response( $svg );
			$resp->header( 'Content-Type', 'image/svg+xml; charset=utf-8' );
			$resp->header( 'Cache-Control', 'public, max-age=86400' );
			return $resp;
		},
	) );
} );

add_action( 'wp_head', function () {
	if ( ! is_singular() ) { return; }
	$id = get_queried_object_id();
	$pt = get_post_type( $id );
	if ( ! nadlan_og_supported_pt( $pt ) ) { return; }
	// Don't fight Yoast on pages it covers with a featured image
	if ( has_post_thumbnail( $id ) ) { return; }
	$url = esc_url( rest_url( 'nadlan/v1/og/' . (int) $id . '.svg' ) );
	echo "\n<meta property=\"og:image\" content=\"$url\">\n";
	echo "<meta property=\"og:image:width\" content=\"1200\">\n";
	echo "<meta property=\"og:image:height\" content=\"630\">\n";
	echo "<meta name=\"twitter:image\" content=\"$url\">\n";
	echo "<meta name=\"twitter:card\" content=\"summary_large_image\">\n";
}, 28 );
