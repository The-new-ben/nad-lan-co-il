<?php
/**
 * nadlan-config - A listing with an owner (v1.0.0, 24.9.2026, Linear HAD-251)
 *
 * Owner rule: a listing that belongs to someone is that person's page, not a portal page.
 * When a nadlan_property has an owner, the portal's own layers are not printed at all,
 * server side (before this module they were printed and then hidden by CSS copied into
 * every listing: EXTRA_LISTING in the Meital runner and nl_drop_css in broker-drop.php,
 * so every new theme layer came back on these pages, and the portal scheduler even
 * injected a dead "תיאום מועד ביומן" button into the broker's own card):
 *   - the showroom layer .nlps-* (generic 3D, price box, facts, facade, costs, map) with its
 *     assets (model-viewer, mv-ux, Leaflet); one visually hidden H1 with the title stays;
 *   - the card layer .nlcard (facts table, photo grid, "זה הכרטיס שלכם?");
 *   - the "כדאי לדעת" band, the portal engagement block (portal WhatsApp, visit form, tours
 *     promo, generic similar listings) and the date-booking band;
 *   - the portal's floating WhatsApp pill and "פרסמו את הדירה שלכם" pill, the Yoast
 *     breadcrumb block and the theme's featured image (the owner's page has its own cover).
 * On a broker's listing, "similar listings" shows only the same broker's other live listings,
 * and the broker's name links to the broker's site.
 *
 * Who owns a listing:
 *   - a professional (broker): the nadlan_professional id in nl_broker_id (written by the
 *     broker drop box on every listing it builds, and on Meital Katzir's 11 listings),
 *     or in nl_broker_site, or a claimed (claim_status=verified) nadlan_professional whose
 *     owner_user_id is the listing's owner_user_id;
 *   - a private owner whose page was built by the listing engine (nl_owner=1, /post-listing/).
 *     An old-wizard listing without its own page (e.g. Ofakim, 7622) is not covered: it still
 *     needs the portal's price, facts and map.
 * Broker pages (the site pages and the English, Russian and French listing twins) carry the
 * same meta; there only the floating portal WhatsApp pill is dropped.
 *
 * Helpers for other modules:
 *   nadlan_property_owner( $post_id )    -> int, the owning nadlan_professional id, 0 if none
 *   nadlan_property_is_owned( $post_id ) -> bool, true for a professional or an engine-built owner page
 * Kill switch: option nadlan_owned_rule = '0'.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! defined( 'NADLAN_OWNED_VERSION' ) ) { define( 'NADLAN_OWNED_VERSION', '1.0.0' ); }

if ( ! function_exists( 'nadlan_property_owner' ) ) {
	/** The nadlan_professional that owns a listing or a broker page, 0 when there is none. */
	function nadlan_property_owner( $post_id ) {
		static $memo = array();
		$post_id = (int) $post_id;
		if ( $post_id <= 0 ) { return 0; }
		if ( array_key_exists( $post_id, $memo ) ) { return $memo[ $post_id ]; }
		$owner = 0;
		$type  = get_post_type( $post_id );
		if ( 'nadlan_property' === $type || 'page' === $type ) {
			foreach ( array( 'nl_broker_id', 'nl_broker_site', 'nl_broker_auto' ) as $key ) {
				$pro = (int) get_post_meta( $post_id, $key, true );
				if ( $pro > 0 && 'nadlan_professional' === get_post_type( $pro ) && 'trash' !== get_post_status( $pro ) ) {
					$owner = $pro;
					break;
				}
			}
			if ( ! $owner && 'nadlan_property' === $type ) {
				$uid = (int) get_post_meta( $post_id, 'owner_user_id', true );
				if ( $uid > 0 ) {
					$found = get_posts( array(
						'post_type'        => 'nadlan_professional',
						'post_status'      => 'publish',
						'numberposts'      => 1,
						'fields'           => 'ids',
						'no_found_rows'    => true,
						'suppress_filters' => true,
						'meta_query'       => array(
							array( 'key' => 'owner_user_id', 'value' => $uid, 'type' => 'NUMERIC' ),
							array( 'key' => 'claim_status', 'value' => 'verified' ),
						),
					) );
					if ( $found ) { $owner = (int) $found[0]; }
				}
			}
		}
		$owner            = (int) apply_filters( 'nadlan_property_owner', $owner, $post_id );
		$memo[ $post_id ] = $owner;
		return $owner;
	}
}

if ( ! function_exists( 'nadlan_property_is_owned' ) ) {
	/** True when the listing is someone's own page: a professional's, or a private owner's engine-built page. */
	function nadlan_property_is_owned( $post_id ) {
		$post_id = (int) $post_id;
		if ( nadlan_property_owner( $post_id ) > 0 ) { return true; }
		return 'nadlan_property' === get_post_type( $post_id ) && '1' === (string) get_post_meta( $post_id, 'nl_owner', true );
	}
}

if ( ! function_exists( 'nadlan_owned_rule_on' ) ) {
	function nadlan_owned_rule_on() {
		return '0' !== (string) get_option( 'nadlan_owned_rule', '1' );
	}
}

if ( ! function_exists( 'nadlan_owned_unhook' ) ) {
	/** Removes named callbacks from a hook whatever their priority. */
	function nadlan_owned_unhook( $hook, $names ) {
		global $wp_filter;
		if ( empty( $wp_filter[ $hook ] ) || ! is_object( $wp_filter[ $hook ] ) ) { return; }
		foreach ( $wp_filter[ $hook ]->callbacks as $priority => $callbacks ) {
			foreach ( $callbacks as $cb ) {
				if ( is_string( $cb['function'] ) && in_array( $cb['function'], $names, true ) ) {
					remove_filter( $hook, $cb['function'], $priority );
				}
			}
		}
	}
}

/* ---------------- the request: decide once, after the query is known ---------------- */
add_action( 'wp', function () {
	if ( is_admin() || ! nadlan_owned_rule_on() ) { return; }
	$listing = is_singular( 'nadlan_property' );
	if ( ! $listing && ! is_page() ) { return; }
	$id = (int) get_queried_object_id();
	if ( $listing ? ! nadlan_property_is_owned( $id ) : ! nadlan_property_owner( $id ) ) { return; }

	// the portal's floating WhatsApp pill: the owner's page carries the owner's own buttons
	add_filter( 'pre_option_nadlan_owner_whatsapp', '__return_empty_string' );
	if ( ! $listing ) { return; }

	// the portal layers on the listing are not printed at all
	nadlan_owned_unhook( 'the_content', array( 'nadlan_pshow_render', 'nadlan_card_append_content', 'nadlan_listing_append' ) );
	nadlan_owned_unhook( 'wp_enqueue_scripts', array( 'nadlan_pshow_assets' ) );
	add_filter( 'pre_option_nadlan_relcontent_enabled', function () { return '0'; } );   // "כדאי לדעת"
	add_filter( 'pre_option_nadlan_feature_scheduler', function () { return '0'; } );    // the booking band and its injected button
	add_filter( 'nadlan_cta_start_map', '__return_empty_array' );                         // "פרסמו את הדירה שלכם"
	add_filter( 'render_block', 'nadlan_owned_render_block', 20, 2 );
	add_filter( 'the_content', 'nadlan_owned_title', 6 );
	add_filter( 'the_content', 'nadlan_owned_more', 23 );
	add_action( 'wp_enqueue_scripts', 'nadlan_owned_assets', 100 );
}, 20 );

if ( ! function_exists( 'nadlan_owned_render_block' ) ) {
	/** The theme's Yoast breadcrumb block and featured image do not print on an owner's listing. */
	function nadlan_owned_render_block( $html, $block ) {
		$name = isset( $block['blockName'] ) ? (string) $block['blockName'] : '';
		if ( 'yoast-seo/breadcrumbs' === $name || 'core/post-featured-image' === $name ) { return ''; }
		return $html;
	}
}

if ( ! function_exists( 'nadlan_owned_title' ) ) {
	/** One H1 for search and screen readers; the owner's page shows its own title block. */
	function nadlan_owned_title( $content ) {
		if ( ! is_singular( 'nadlan_property' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
		return '<h1 class="nlo-title">' . esc_html( get_the_title() ) . '</h1>' . $content;
	}
}

if ( ! function_exists( 'nadlan_owned_assets' ) ) {
	function nadlan_owned_assets() {
		wp_dequeue_script( 'nadlan-model-viewer' );
		wp_dequeue_script( 'nadlan-mv-ux' );
		wp_register_style( 'nadlan-owned', false, array(), NADLAN_OWNED_VERSION );
		wp_enqueue_style( 'nadlan-owned' );
		wp_add_inline_style( 'nadlan-owned', nadlan_owned_css() );
	}
}

/* ---------------- the broker's site, name and other listings ---------------- */
if ( ! function_exists( 'nadlan_owner_name' ) ) {
	function nadlan_owner_name( $pro ) {
		$name = trim( (string) get_post_meta( $pro, 'nl_name_he', true ) );
		if ( '' === $name ) {
			$parts = preg_split( '/\s+[·|\-]\s+/u', (string) get_the_title( $pro ) );
			$name  = trim( (string) $parts[0] );
		}
		return $name;
	}
}

if ( ! function_exists( 'nadlan_owner_site_url' ) ) {
	/** The broker's own site: the Hebrew site page when it is live, else the website field, else the directory profile. */
	function nadlan_owner_site_url( $pro ) {
		$site = (int) get_post_meta( $pro, 'nl_site_he', true );
		if ( $site && 'publish' === get_post_status( $site ) ) { return (string) get_permalink( $site ); }
		$web = trim( (string) get_post_meta( $pro, 'website', true ) );
		if ( preg_match( '#^https?://[^\s/]+#i', $web ) ) { return $web; }
		return 'publish' === get_post_status( $pro ) ? (string) get_permalink( $pro ) : '';
	}
}

if ( ! function_exists( 'nadlan_owner_listings' ) ) {
	/** The broker's other live listings: same deal type first, newest first. */
	function nadlan_owner_listings( $pro, $exclude, $limit = 3 ) {
		$pro = (int) $pro;
		$base = array(
			'post_type'        => 'nadlan_property',
			'post_status'      => 'publish',
			'numberposts'      => 24,
			'fields'           => 'ids',
			'orderby'          => 'date',
			'order'            => 'DESC',
			'no_found_rows'    => true,
			'suppress_filters' => true,
			'post__not_in'     => array( (int) $exclude ),
		);
		$ids = get_posts( array_merge( $base, array( 'meta_query' => array(
			'relation' => 'OR',
			array( 'key' => 'nl_broker_id', 'value' => (string) $pro ),
			array( 'key' => 'nl_broker_site', 'value' => (string) $pro ),
		) ) ) );
		$uid = (int) get_post_meta( $pro, 'owner_user_id', true );
		if ( $uid > 0 && 'verified' === (string) get_post_meta( $pro, 'claim_status', true ) ) {
			$ids = array_merge( $ids, get_posts( array_merge( $base, array( 'meta_query' => array(
				array( 'key' => 'owner_user_id', 'value' => $uid, 'type' => 'NUMERIC' ),
			) ) ) ) );
		}
		$deal = (string) get_post_meta( (int) $exclude, 'listing_type', true );
		$rows = array();
		foreach ( array_values( array_unique( array_map( 'intval', $ids ) ) ) as $i => $id ) {
			$st = (string) get_post_meta( $id, 'nl_status', true );
			if ( 'sold' === $st || 'rented' === $st || get_post_meta( $id, 'is_demo', true ) ) { continue; }
			$rows[] = array( 'id' => $id, 'same' => (string) get_post_meta( $id, 'listing_type', true ) === $deal ? 0 : 1, 'i' => $i );
		}
		usort( $rows, function ( $a, $b ) { return $a['same'] === $b['same'] ? $a['i'] - $b['i'] : $a['same'] - $b['same']; } );
		return array_slice( wp_list_pluck( $rows, 'id' ), 0, max( 0, (int) $limit ) );
	}
}

if ( ! function_exists( 'nadlan_owned_more' ) ) {
	/** "Similar listings" on a broker's listing = the same broker's other live listings. */
	function nadlan_owned_more( $content ) {
		if ( ! is_singular( 'nadlan_property' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
		$id  = (int) get_the_ID();
		$pro = nadlan_property_owner( $id );
		if ( ! $pro ) { return $content; }
		$list = nadlan_owner_listings( $pro, $id, 3 );
		if ( ! $list ) { return $content; }
		$name = nadlan_owner_name( $pro );
		$site = nadlan_owner_site_url( $pro );
		$who  = '' !== $site ? '<a href="' . esc_url( $site ) . '">' . esc_html( $name ) . '</a>' : esc_html( $name );
		$h    = '<section class="nlo-more" dir="rtl" aria-labelledby="nlo-more-h"><div class="nlo-wrap">';
		$h   .= '<div class="nlo-head"><h2 class="nlo-h" id="nlo-more-h">עוד נכסים של ' . $who . '</h2>';
		if ( '' !== $site ) {
			$h .= '<a class="nlo-all" href="' . esc_url( $site ) . '">לכל הנכסים של ' . esc_html( $name ) . ' <span aria-hidden="true">←</span></a>';
		}
		$h .= '</div><ul class="nlo-grid" role="list">';
		foreach ( $list as $lid ) {
			$deal  = 'rent' === (string) get_post_meta( $lid, 'listing_type', true ) ? 'rent' : 'sale';
			$area  = trim( (string) get_post_meta( $lid, 'neighborhood', true ) );
			if ( '' === $area ) { $area = trim( (string) get_post_meta( $lid, 'city', true ) ); }
			$price = (int) get_post_meta( $lid, 'price', true );
			$rooms = (float) get_post_meta( $lid, 'rooms', true );
			$sqm   = (int) get_post_meta( $lid, 'size_sqm', true );
			$thumb = (int) get_post_thumbnail_id( $lid );
			$specs = array();
			if ( $rooms > 0 ) { $specs[] = '<span class="nlo-num">' . esc_html( rtrim( rtrim( number_format( $rooms, 1, '.', '' ), '0' ), '.' ) ) . '</span> חדרים'; }
			if ( $sqm > 0 ) { $specs[] = '<span class="nlo-num">' . esc_html( number_format( $sqm ) ) . '</span> מ״ר'; }
			$h .= '<li><a class="nlo-card" href="' . esc_url( get_permalink( $lid ) ) . '">';
			$h .= '<span class="nlo-media">' . ( $thumb ? wp_get_attachment_image( $thumb, 'medium_large', false, array( 'alt' => '', 'loading' => 'lazy', 'decoding' => 'async', 'sizes' => '(max-width: 700px) 78vw, 380px' ) ) : '' ) . '</span>';
			$h .= '<span class="nlo-body"><span class="nlo-kicker">' . ( 'rent' === $deal ? 'להשכרה' : 'למכירה' ) . ( '' !== $area ? ' · ' . esc_html( $area ) : '' ) . '</span>';
			$h .= '<span class="nlo-card-t">' . esc_html( get_the_title( $lid ) ) . '</span>';
			if ( $price > 0 ) {
				$h .= '<span class="nlo-price"><span class="nlo-num">' . esc_html( number_format( $price ) ) . '</span>&nbsp;₪' . ( 'rent' === $deal ? ' <small>לחודש</small>' : '' ) . '</span>';
			}
			if ( $specs ) { $h .= '<span class="nlo-specs">' . implode( ' · ', $specs ) . '</span>'; }
			$h .= '</span></a></li>';
		}
		$h .= '</ul></div></section>';
		return $content . $h;
	}
}

if ( ! function_exists( 'nadlan_owned_css' ) ) {
	function nadlan_owned_css() {
		return '.nlo-title{position:absolute!important;width:1px!important;height:1px!important;margin:-1px!important;padding:0!important;border:0!important;overflow:hidden!important;clip:rect(0 0 0 0)!important;clip-path:inset(50%)!important;white-space:nowrap!important}
.nlo-more{--nlo-ink:#14212B;--nlo-ink2:#3B4753;--nlo-mute:#6B7680;--nlo-line:#E3E1DA;--nlo-sea:#2F6F86;--nlo-seah:#255C70;--nlo-sand:#EEE9DD;--nlo-serif:"Noto Serif Hebrew","Noto Serif","David Libre",Georgia,serif;--nlo-sans:Assistant,"Segoe UI",Arial,sans-serif;font-family:var(--nlo-sans);color:var(--nlo-ink);border-top:1px solid var(--nlo-line);margin:clamp(32px,5vw,64px) 0 0;padding:clamp(28px,4vw,48px) 0 clamp(8px,2vw,24px)}
.entry-content>.nlo-more{max-width:none!important}
.nlo-more .nlo-wrap{max-width:1180px;margin-inline:auto;padding-inline:clamp(16px,3vw,28px)}
.nlo-more .nlo-head{display:flex;align-items:baseline;justify-content:space-between;gap:10px 20px;flex-wrap:wrap;margin:0 0 20px}
.nlo-more .nlo-h{font-family:var(--nlo-serif)!important;font-weight:600!important;font-size:clamp(24px,2.4vw,30px)!important;line-height:1.25!important;color:var(--nlo-ink)!important;margin:0!important;text-wrap:balance}
.nlo-more .nlo-h a{color:inherit!important;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:5px;text-decoration-color:var(--nlo-line)}
.nlo-more .nlo-h a:hover{text-decoration-color:var(--nlo-sea)}
.nlo-more .nlo-all{font-size:15px;font-weight:600;color:var(--nlo-sea)!important;text-decoration:none;white-space:nowrap}
.nlo-more .nlo-all:hover{color:var(--nlo-seah)!important;text-decoration:underline}
.nlo-more .nlo-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin:0;padding:0;list-style:none}
.nlo-more .nlo-grid li{margin:0;padding:0}
.nlo-more .nlo-card{display:flex;flex-direction:column;height:100%;background:#fff;border:1px solid var(--nlo-line);border-radius:8px;overflow:hidden;text-decoration:none!important;color:inherit!important;transition:border-color .2s ease,box-shadow .2s ease}
.nlo-more .nlo-card:hover{border-color:var(--nlo-sea);box-shadow:0 8px 24px rgba(17,17,15,.07),0 2px 6px rgba(17,17,15,.04)}
.nlo-more .nlo-card:focus-visible{outline:2px solid var(--nlo-sea);outline-offset:3px}
.nlo-more .nlo-media{display:block;aspect-ratio:4/5;background:var(--nlo-sand);overflow:hidden}
.nlo-more .nlo-media img{width:100%;height:100%;object-fit:cover;display:block;max-width:none;transition:transform .6s ease}
.nlo-more .nlo-card:hover .nlo-media img{transform:scale(1.03)}
.nlo-more .nlo-body{display:flex;flex-direction:column;gap:6px;padding:16px 18px 18px}
.nlo-more .nlo-kicker{font-size:13px;font-weight:700;letter-spacing:.03em;color:var(--nlo-sea)}
.nlo-more .nlo-card-t{font-family:var(--nlo-serif);font-weight:600;font-size:19px;line-height:1.35;color:var(--nlo-ink);text-wrap:balance}
.nlo-more .nlo-price{font-size:19px;font-weight:700;line-height:1.3;color:var(--nlo-ink)}
.nlo-more .nlo-price small{font-size:14px;font-weight:600;color:var(--nlo-mute)}
.nlo-more .nlo-specs{font-size:14.5px;color:var(--nlo-ink2)}
.nlo-more .nlo-num{font-variant-numeric:tabular-nums lining-nums;direction:ltr;unicode-bidi:isolate;display:inline-block}
@media (max-width:700px){.nlo-more .nlo-grid{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:12px;padding-bottom:8px;-webkit-overflow-scrolling:touch;scrollbar-width:thin}.nlo-more .nlo-grid li{flex:0 0 78%;scroll-snap-align:start}}
@media (prefers-reduced-motion:reduce){.nlo-more .nlo-card,.nlo-more .nlo-media img{transition:none}.nlo-more .nlo-card:hover .nlo-media img{transform:none}}';
	}
}

/* Health: the rule is visible to the release checks. */
add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	if ( is_array( $out ) ) {
		$out['owned_rule'] = array( 'version' => NADLAN_OWNED_VERSION, 'on' => nadlan_owned_rule_on() );
	}
	return $out;
} );
