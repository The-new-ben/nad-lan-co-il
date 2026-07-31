<?php
/**
 * nadlan-config - Facility chips (Booking-style at-a-glance badges)
 *
 * One shared system that surfaces a project's facilities (בריכה, ספא, חדר
 * כושר...) as small clickable badges everywhere a project is shown:
 *   - catalog cards (/projects/ premium directory, inc/directory.php),
 *   - premium catalog cards (/premium/, inc/premium-catalog.php),
 *   - the project page hero (the_content priority 8: after the pjx intro
 *     at 7, before the price band at 9 - zero edits to project-experience),
 *   - the OG share image (inc/og-image.php bakes a crop-safe badge strip).
 *
 * Data resolution (fail closed to NOTHING - no facility data, no chips row):
 *   1. `project_facilities` post meta (CSV, CMS-editable override),
 *   2. the curated premium catalog rows (nadlan_premium_catalog_data) matched
 *      by base slug (language suffixes -en/-fr/-ru/-ar stripped),
 *   3. for nadlan_property: the boolean metas that map into the facility set
 *      (protected_room -> ממ"ד, parking -> חניון).
 *
 * Chip click deep-links to /premium/?fac=<name>; the premium catalog footer
 * JS reads the param and applies its client-side filter. Inside card <a>
 * wrappers chips render as [data-fac] spans (nested anchors are invalid
 * HTML) and a tiny delegated handler navigates; real <a> chips are used
 * wherever the DOM allows.
 *
 * CSS/JS ship via wp_enqueue + inline (kses-proof; in-band <style>/<script>
 * are sanitized away in home bands - the sdedov-teaser lesson).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_fc_keys' ) ) {
	/** The canonical facility filter keys - MUST mirror the /premium/ filter
	 *  bar (premium-catalog.php reuses this list so they cannot drift). */
	function nadlan_fc_keys() {
		return array( 'בריכה', 'ספא', 'חדר כושר', 'קולנוע', "קונסיירז'", 'לגונה', "לאונג'", 'אזורי ילדים', 'מסחר', 'חניון', 'ממ"ד' );
	}
}

if ( ! function_exists( 'nadlan_fc_icon' ) ) {
	/** Gold-line SVG for a canonical key (reuses the premium icon set). */
	function nadlan_fc_icon( $key ) {
		if ( ! function_exists( 'nadlan_pc_icons' ) ) { return ''; }
		$icons = nadlan_pc_icons();
		if ( isset( $icons[ $key ] ) ) { return $icons[ $key ]; }
		// icon keys are shorter than some filter keys ('אזורי ילדים' -> 'ילדים')
		foreach ( $icons as $ik => $svg ) {
			if ( $ik !== '' && strpos( $key, $ik ) !== false ) { return $svg; }
		}
		return '';
	}
}

if ( ! function_exists( 'nadlan_fc_canonical' ) ) {
	/** Raw facility labels -> ordered unique canonical keys.
	 *  'לגונה ובריכות' yields בריכה + לגונה; labels that match no filter
	 *  key (e.g. 'לובי Kelly Hoppen') yield nothing here. */
	function nadlan_fc_canonical( $labels ) {
		$out = array();
		foreach ( (array) $labels as $label ) {
			$label = trim( (string) $label );
			if ( '' === $label ) { continue; }
			foreach ( nadlan_fc_keys() as $k ) {
				// 'בריכה' must also catch 'בריכות' - compare on the stem
				$stem = mb_substr( $k, 0, max( 3, mb_strlen( $k ) - 1 ) );
				if ( strpos( $label, $k ) !== false || strpos( $label, $stem ) !== false ) {
					$out[ $k ] = true;
				}
			}
		}
		return array_keys( $out );
	}
}

if ( ! function_exists( 'nadlan_fc_for_project' ) ) {
	/** Canonical facility keys for a nadlan_project. Empty array = no chips. */
	function nadlan_fc_for_project( $id ) {
		$id  = (int) $id;
		$raw = array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $id, 'project_facilities', true ) ) ) );
		if ( ! $raw && function_exists( 'nadlan_premium_catalog_data' ) ) {
			$slug = preg_replace( '/-(en|fr|ru|ar)$/', '', (string) get_post_field( 'post_name', $id ) );
			foreach ( nadlan_premium_catalog_data() as $row ) {
				if ( isset( $row['slug'], $row['fac'] ) && $row['slug'] === $slug && is_array( $row['fac'] ) ) {
					$raw = $row['fac'];
					break;
				}
			}
		}
		$keys = nadlan_fc_canonical( $raw );
		return apply_filters( 'nadlan_fc_project_facilities', $keys, $id );
	}
}

if ( ! function_exists( 'nadlan_fc_for_property' ) ) {
	/** Canonical facility keys for a nadlan_property (boolean metas). */
	function nadlan_fc_for_property( $id ) {
		$id   = (int) $id;
		$keys = array();
		if ( get_post_meta( $id, 'protected_room', true ) ) { $keys[] = 'ממ"ד'; }
		if ( get_post_meta( $id, 'parking', true ) )        { $keys[] = 'חניון'; }
		return apply_filters( 'nadlan_fc_property_facilities', $keys, $id );
	}
}

if ( ! function_exists( 'nadlan_fc_premium_url' ) ) {
	function nadlan_fc_premium_url( $key ) {
		return home_url( '/premium/?fac=' . rawurlencode( $key ) );
	}
}

if ( ! function_exists( 'nadlan_fc_chips_html' ) ) {
	/**
	 * The chips row.
	 *
	 * @param array $keys  canonical keys (from nadlan_fc_for_*).
	 * @param array $opts  'limit' (int, default 5), 'link' (bool - real <a>;
	 *                     false = [data-fac] spans for use INSIDE an <a> card),
	 *                     'class' (extra class on the wrapper).
	 */
	function nadlan_fc_chips_html( $keys, $opts = array() ) {
		$keys = array_values( array_unique( array_filter( (array) $keys ) ) );
		if ( ! $keys ) { return ''; }
		$limit = isset( $opts['limit'] ) ? max( 1, (int) $opts['limit'] ) : 5;
		$link  = ! isset( $opts['link'] ) || $opts['link'];
		$class = 'nlfc' . ( empty( $opts['class'] ) ? '' : ' ' . $opts['class'] );
		$keys  = array_slice( $keys, 0, $limit );
		$out   = '<span class="' . esc_attr( $class ) . '" dir="rtl">';
		foreach ( $keys as $k ) {
			$icon = nadlan_fc_icon( $k );
			$body = ( $icon ? '<i class="nlfc-ic" aria-hidden="true">' . $icon . '</i>' : '' ) . esc_html( $k );
			if ( $link ) {
				$out .= '<a class="nlfc-chip" href="' . esc_url( nadlan_fc_premium_url( $k ) ) . '" title="' . esc_attr( 'כל הפרויקטים עם ' . $k ) . '">' . $body . '</a>';
			} else {
				$out .= '<span class="nlfc-chip" data-fac="' . esc_attr( $k ) . '" role="link" tabindex="0" title="' . esc_attr( 'כל הפרויקטים עם ' . $k ) . '">' . $body . '</span>';
			}
		}
		return $out . '</span>';
	}
}

/* ---------------- project page hero row (surface 2) ----------------
 * Priority 8 the_content: nadlan_pjx_top (7) has already prepended the
 * sticky nav + intro; the chips row slots right AFTER the intro div,
 * before the price band (9). String-insert by class TOKEN, fail OPEN:
 * if the intro is missing the row prepends instead - content is never
 * dropped (the 3,000-word-article lesson). */
if ( ! function_exists( 'nadlan_fc_project_hero' ) ) {
	function nadlan_fc_project_hero( $content ) {
		if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
		// chips carry Hebrew labels - skip the -en/-fr/-ru/-ar language siblings
		if ( preg_match( '/-(en|fr|ru|ar)$/', (string) get_post_field( 'post_name', get_the_ID() ) ) ) { return $content; }
		$keys = nadlan_fc_for_project( get_the_ID() );
		if ( ! $keys ) { return $content; }
		$row = '<div class="nlfc-hero" dir="rtl" aria-label="מתקנים ושירותים בפרויקט">'
			. nadlan_fc_chips_html( $keys, array( 'limit' => 8, 'link' => true ) )
			. '</div>';
		if ( preg_match( '/class="[^"]*\bnlpjx-intro\b[^"]*"/', $content, $m, PREG_OFFSET_CAPTURE ) ) {
			$close = strpos( $content, '</div>', $m[0][1] );
			if ( false !== $close ) {
				return substr( $content, 0, $close + 6 ) . $row . substr( $content, $close + 6 );
			}
		}
		return $row . $content;
	}
}
add_filter( 'the_content', 'nadlan_fc_project_hero', 8 );

/* ---------------- assets: one site-wide handle, kses-proof ---------------- */
add_action( 'wp_enqueue_scripts', function () {
	$ver = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1';
	wp_register_style( 'nlfc', false, array(), $ver );
	wp_enqueue_style( 'nlfc' );
	wp_add_inline_style( 'nlfc', ''
		. '.nlfc{display:flex;flex-wrap:wrap;gap:6px;align-items:center}'
		. '.nlfc-chip{display:inline-flex;align-items:center;gap:5px;font:600 11.5px/1 Heebo,sans-serif;color:#51483A;background:#FAF5EA;border:1px solid #E2DCD0;border-radius:999px;padding:5px 10px;text-decoration:none;cursor:pointer;transition:border-color .15s,color .15s,background .15s}'
		. '.nlfc-chip:hover,.nlfc-chip:focus-visible{border-color:#9C7A3C;color:#9C7A3C;background:#FFFDF8}'
		. '.nlfc-ic{display:inline-flex;color:#9C7A3C;flex:none}'
		. '.nlfc-ic svg{width:13px;height:13px;display:block}'
		. '.nlfc-hero{margin:10px 0 14px}'
		. '.nlfc-hero .nlfc-chip{font-size:12.5px;padding:7px 13px}'
		. '.nlfc-hero .nlfc-ic svg{width:15px;height:15px}'
		. '.nlfc-oncard{margin:4px 0 2px}'
	);
	wp_register_script( 'nlfc', false, array(), $ver, true );
	wp_enqueue_script( 'nlfc' );
	/* Delegated navigation for [data-fac] chips living inside card <a>
	 * wrappers: stop the card link, go to the premium filter deep link.
	 * No-JS degradation: the card link itself still works. */
	wp_add_inline_script( 'nlfc', '(function(){'
		. 'var base=' . wp_json_encode( home_url( '/premium/' ) ) . ';'
		. 'function go(e){var c=e.target.closest(".nlfc-chip[data-fac]");if(!c)return;'
		. 'e.preventDefault();e.stopPropagation();'
		. 'window.location=base+"?fac="+encodeURIComponent(c.getAttribute("data-fac"));}'
		. 'document.addEventListener("click",go);'
		. 'document.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){go(e)}});'
		. '})();' );
}, 20 );
