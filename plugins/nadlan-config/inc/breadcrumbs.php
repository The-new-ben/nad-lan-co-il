<?php
/**
 * nadlan-config - Breadcrumbs (visible + BreadcrumbList JSON-LD) (v1.14.0)
 *
 * Output a Hebrew breadcrumb trail on every NadLan CPT single and on archives,
 * and emit BreadcrumbList JSON-LD for Google rich results (eligible site-wide
 * link sitelinks improvement). Skips if Yoast already prints its own
 * BreadcrumbList to avoid duplicate schema.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_breadcrumbs_profession' ) ) {
	/** The profession level of a professional card's trail: array( label, url ), or null. One source for the visible trail and the schema. */
	function nadlan_breadcrumbs_profession( $id ) {
		$prof  = (string) get_post_meta( $id, 'profession', true );
		$label = array(
			'kablan' => 'קבלנים', 'shamai' => 'שמאים', 'bedek_bait' => 'בדק בית', 'mashkanta' => 'יועצי משכנתאות',
			'architect' => 'אדריכלים', 'lawyer' => 'עורכי דין', 'inspector' => 'מפקחי בנייה', 'mefakeach' => 'מפקחי בנייה',
			'metavech' => 'מתווכים', 'interior_designer' => 'מעצבי פנים', 'engineer' => 'מהנדסי בניין', 'accountant' => 'רואי חשבון',
			'surveyor' => 'מודדים', 'property_manager' => 'ניהול נכסים', 'urban_planner' => 'מתכנני ערים',
		)[ $prof ] ?? '';
		if ( '' === $label && function_exists( 'nadlan_pro_registry' ) ) {
			$reg   = nadlan_pro_registry();
			$label = isset( $reg[ $prof ] ) ? $reg[ $prof ]['plural'] : '';
		}
		return '' === $label ? null : array( $label, add_query_arg( 'profession', $prof, home_url( '/professionals/' ) ) );
	}
}

if ( ! function_exists( 'nadlan_breadcrumbs_items' ) ) {
	function nadlan_breadcrumbs_items() {
		if ( function_exists( 'nadlan_unit_journey_is_private_lab' ) && nadlan_unit_journey_is_private_lab() ) {
			return array();
		}
		$items = array( array( 'name' => 'בית', 'url' => home_url( '/' ) ) );
		if ( is_singular( 'nadlan_property' ) ) {
			$items[] = array( 'name' => 'דירות', 'url' => home_url( '/properties/' ) );
			$city = (string) get_post_meta( get_the_ID(), 'city', true );
			$items[] = array( 'name' => get_the_title(), 'url' => get_permalink() );
		} elseif ( is_singular( 'nadlan_project' ) ) {
			$items[] = array( 'name' => 'פרויקטים', 'url' => home_url( '/projects/' ) );
			$city = (string) get_post_meta( get_the_ID(), 'city', true );
			$items[] = array( 'name' => get_the_title(), 'url' => get_permalink() );
		} elseif ( is_singular( 'nadlan_professional' ) ) {
			$items[] = array( 'name' => 'אנשי מקצוע', 'url' => home_url( '/professionals/' ) );
			$level = nadlan_breadcrumbs_profession( get_the_ID() );
			if ( $level ) { $items[] = array( 'name' => $level[0], 'url' => $level[1] ); }
			$items[] = array( 'name' => get_the_title(), 'url' => get_permalink() );
		} elseif ( is_post_type_archive( 'nadlan_property' ) ) { $items[] = array( 'name' => 'דירות', 'url' => home_url( '/properties/' ) ); }
		elseif ( is_post_type_archive( 'nadlan_project' ) )    { $items[] = array( 'name' => 'פרויקטים', 'url' => home_url( '/projects/' ) ); }
		elseif ( is_post_type_archive( 'nadlan_professional' ) ){ $items[] = array( 'name' => 'אנשי מקצוע', 'url' => home_url( '/professionals/' ) ); }
		else { return array(); }
		// a language page starts at its own language's home (inc/lang-pages.php, 28.9.2026)
		return (array) apply_filters( 'nadlan_breadcrumbs_items', $items );
	}
}

if ( ! function_exists( 'nadlan_breadcrumbs_render' ) ) {
	function nadlan_breadcrumbs_render() {
		$items = nadlan_breadcrumbs_items();
		if ( count( $items ) < 2 ) { return ''; }
		ob_start(); ?>
<nav class="nlbc" dir="rtl" aria-label="ניווט">
	<?php $n = count( $items ); $i = 0; foreach ( $items as $it ) : $i++; ?>
		<a href="<?php echo esc_url( $it['url'] ); ?>"><?php echo esc_html( $it['name'] ); ?></a>
		<?php if ( $i < $n ) : ?><span class="nlbc-sep">›</span><?php endif; ?>
	<?php endforeach; ?>
</nav>
<style>.nlbc{font-size:13px;color:#777;margin:8px 0 18px}.nlbc a{color:#777;text-decoration:none}.nlbc a:hover{color:#1B1A17}.nlbc-sep{margin:0 6px;color:#bbb}</style>
		<?php
		return ob_get_clean();
	}
}
add_filter( 'the_content', function ( $content ) {
	if ( is_singular( array( 'nadlan_property', 'nadlan_project', 'nadlan_professional' ) ) && in_the_loop() && is_main_query() ) {
		/* Owner evidence 2026-08-09: on showroom-engine project pages this
		 * visual nav was re-attached AFTER the theater (the engine keeps
		 * everything filters prepend), reading as "the page starts again with
		 * breadcrumbs" mid-scroll. The engine topbar owns wayfinding there;
		 * BreadcrumbList schema in wp_head is unaffected. */
		/* One visible trail per page (owner 24.9.2026, "breadcrumbs twice"): where the theme prints Yoast's trail
		 * at the top, this one stays out. Yoast's trail is on professional cards and on listings without an
		 * owner; an owned listing drops Yoast's (property-owner.php), so it keeps this one. */
		if ( is_singular( 'nadlan_professional' ) ) {
			return $content;
		}
		if ( is_singular( 'nadlan_property' ) && ! ( function_exists( 'nadlan_property_is_owned' ) && nadlan_property_is_owned( get_the_ID() ) ) ) {
			return $content;
		}
		if ( is_singular( 'nadlan_project' )
			&& function_exists( 'nadlan_showroom_engine_active_for' )
			&& nadlan_showroom_engine_active_for( get_the_ID() ) ) {
			return $content;
		}
		return nadlan_breadcrumbs_render() . $content;
	}
	return $content;
}, 5 );

add_action( 'wp_head', function () {
	$items = nadlan_breadcrumbs_items();
	if ( count( $items ) < 2 ) { return; }
	/* Source-audit 30.8.2026: modern Yoast ships a breadcrumb piece in its schema
	 * graph regardless of the breadcrumbs feature toggle, so the old option check
	 * let BOTH graphs print. This emitter mirrors the visible trail and is the
	 * single owner; Yoast's piece is suppressed via the filter below. */
	$ld = array( '@context' => 'https://schema.org', '@type' => 'BreadcrumbList',
		'itemListElement' => array_map( function ( $it, $i ) {
			return array( '@type' => 'ListItem', 'position' => $i + 1, 'name' => $it['name'], 'item' => $it['url'] );
		}, array_values( $items ), array_keys( $items ) ) );
	$ld['@id'] = nadlan_breadcrumbs_id(); // 1.72.512: the id Yoast's WebPage points to (the filter below), so the reference resolves
	echo "\n<script type=\"application/ld+json\">" . wp_json_encode( $ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
}, 22 );

/* 1.72.512 (Ben 25.10.2026, Search Console on /projects/: "BreadcrumbList, Missing field itemListElement"): Yoast's WebPage
 * piece points to "<url>#breadcrumb" on every page although its own breadcrumb piece is dropped (wpseo_schema_needs_breadcrumb,
 * below), so Google read an empty BreadcrumbList on every page but the [nadlan_crumbs] pages. Now the pointer names the list
 * this page really prints (the catalog trail above, or the page trail below), and a page that prints none points to nothing. */
if ( ! function_exists( 'nadlan_breadcrumbs_id' ) ) {
	function nadlan_breadcrumbs_id() {
		$qid = get_queried_object_id();
		if ( count( nadlan_breadcrumbs_items() ) >= 2 ) {
			foreach ( array( 'nadlan_property', 'nadlan_project', 'nadlan_professional' ) as $pt ) {
				if ( is_post_type_archive( $pt ) ) { return get_post_type_archive_link( $pt ) . '#breadcrumb'; }
			}
			return get_permalink( $qid ) . '#breadcrumb';
		}
		if ( is_page() && count( nadlan_page_crumbs( $qid ) ) >= 2 ) { return get_permalink( $qid ) . '#breadcrumb'; }
		return '';
	}
}
add_filter( 'wpseo_schema_webpage', function ( $data ) {
	if ( ! is_array( $data ) || ! isset( $data['breadcrumb'] ) ) { return $data; }
	$id = nadlan_breadcrumbs_id();
	if ( '' === $id ) { unset( $data['breadcrumb'] ); } else { $data['breadcrumb'] = array( '@id' => $id ); }
	return $data;
}, 20 );

/* 1.72.498 (HAD-592, Ben 22.10.2026: "title, breadcrumbs and h1 are never the same"): an opt-in trail for regular pages.
 * A page that holds [nadlan_crumbs] gets a visible trail at the top (above its H1, inc/page-h1.php) and a BreadcrumbList with
 * the @id Yoast's WebPage already points to (#breadcrumb), so that reference resolves. Labels: each level's Yoast breadcrumb
 * title (_yoast_wpseo_bctitle), else its title; the page's own level from label="..." (short, never the H1). A page without a
 * WordPress parent names its hub with hub="/path/|label". Only pages that carry the shortcode change; no other page does. */
if ( ! function_exists( 'nadlan_page_crumbs' ) ) {
	function nadlan_page_crumbs( $post = null ) {
		$post = $post ? get_post( $post ) : get_post();
		if ( ! $post || 'page' !== $post->post_type || false === strpos( (string) $post->post_content, '[nadlan_crumbs' ) ) { return array(); }
		if ( ! preg_match( '/\[nadlan_crumbs([^\]]*)\]/', $post->post_content, $m ) ) { return array(); }
		$a     = shortcode_parse_atts( trim( $m[1] ) );
		$a     = is_array( $a ) ? $a : array();
		$label = function ( $id ) { $b = trim( (string) get_post_meta( $id, '_yoast_wpseo_bctitle', true ) ); return '' !== $b ? $b : wp_strip_all_tags( get_the_title( $id ) ); };
		$pl    = function_exists( 'nadlan_pglang_lang' ) ? nadlan_pglang_lang() : '';  // 1.72.591 (HAD-675): a page under /en/, /fr/, /ru/ or /ar/ starts at that language's home
		$homes = array( 'en' => 'Home', 'fr' => 'Accueil', 'ru' => 'Главная', 'ar' => 'الرئيسية' );
		$items = array( isset( $homes[ $pl ] ) ? array( 'name' => $homes[ $pl ], 'url' => home_url( '/' . $pl . '/' ) ) : array( 'name' => 'בית', 'url' => home_url( '/' ) ) );
		foreach ( array_reverse( get_post_ancestors( $post ) ) as $anc ) { if ( isset( $homes[ $pl ] ) && ! wp_get_post_parent_id( $anc ) && get_post_field( 'post_name', $anc ) === $pl ) { continue; } $items[] = array( 'name' => $label( $anc ), 'url' => get_permalink( $anc ) ); }
		// hub="/global/|השקעות בחו״ל;/global/greece/|יוון": one or more levels above a page that has no WordPress parent (1.72.499)
		if ( ! empty( $a['hub'] ) ) {
			foreach ( explode( ';', $a['hub'] ) as $lvl ) {
				if ( false === strpos( $lvl, '|' ) ) { continue; }
				list( $path, $name ) = array_map( 'trim', explode( '|', $lvl, 2 ) );
				if ( '' !== $path && '' !== $name ) { $items[] = array( 'name' => $name, 'url' => home_url( $path ) ); }
			}
		}
		$items[] = array( 'name' => ! empty( $a['label'] ) ? sanitize_text_field( $a['label'] ) : $label( $post->ID ), 'url' => get_permalink( $post ) );
		return $items;
	}
}
add_shortcode( 'nadlan_crumbs', function () {
	if ( ! is_page() || ! in_the_loop() ) { return ''; }
	$items = nadlan_page_crumbs();
	if ( count( $items ) < 2 ) { return ''; }
	$pl = function_exists( 'nadlan_pglang_lang' ) ? nadlan_pglang_lang() : ''; $rtl = in_array( $pl, array( '', 'ar' ), true );  // 1.72.591: the trail speaks the page's language
	$n = count( $items ); $h = '<nav class="nlbc nlbc--page" dir="' . ( $rtl ? 'rtl' : 'ltr' ) . '" aria-label="' . ( '' === $pl ? 'מיקום בעמוד' : ( 'ar' === $pl ? 'مسار التنقل' : 'Breadcrumb' ) ) . '">';
	foreach ( array_values( $items ) as $i => $it ) {
		$h .= $i + 1 < $n ? '<a href="' . esc_url( $it['url'] ) . '">' . esc_html( $it['name'] ) . '</a><span class="nlbc-sep" aria-hidden="true">›</span>'
			: '<span aria-current="page">' . esc_html( $it['name'] ) . '</span>';
	}
	return $h . '</nav><style>.nlbc--page{font:500 13px/18px var(--sa-sans,"IBM Plex Sans Hebrew",system-ui,sans-serif);color:#5E6A75;margin:4px 0 10px;display:flex;flex-wrap:wrap;gap:2px 0}.nlbc--page a{color:#2F6F86;text-decoration:none}.nlbc--page a:hover{text-decoration:underline}.nlbc--page .nlbc-sep{margin:0 6px;color:#9AA6B0}.nlbc--page [aria-current]{color:#3E4C58}</style>';
} );
add_action( 'wp_head', function () {
	if ( ! is_page() ) { return; }
	$items = nadlan_page_crumbs( get_queried_object_id() );
	if ( count( $items ) < 2 ) { return; }
	$ld = array( '@context' => 'https://schema.org', '@type' => 'BreadcrumbList', '@id' => get_permalink( get_queried_object_id() ) . '#breadcrumb',
		'itemListElement' => array_map( function ( $it, $i ) { return array( '@type' => 'ListItem', 'position' => $i + 1, 'name' => $it['name'], 'item' => $it['url'] ); }, array_values( $items ), array_keys( array_values( $items ) ) ) );
	echo "\n<script type=\"application/ld+json\" id=\"nadlan-page-crumbs\">" . wp_json_encode( $ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
}, 22 );

/* Single BreadcrumbList owner (source-audit 30.8.2026): drop Yoast's graph piece. */
add_filter( 'wpseo_schema_needs_breadcrumb', '__return_false' );

/* The theme's Yoast breadcrumb names a catalog section by its admin label ("NadLan Professionals",
 * "NadLan Properties"; the admin labels stay English on purpose). On the site the crumb speaks Hebrew,
 * the same words as the plugin trail above (HAD-249, 24.9.2026). Matched by the crumb's archive key
 * or by its URL, whichever the Yoast version provides. */
add_filter( 'wpseo_breadcrumb_links', function ( $links ) {
	if ( ! is_array( $links ) ) { return $links; }
	$labels = array( 'nadlan_professional' => 'אנשי מקצוע', 'nadlan_property' => 'דירות', 'nadlan_project' => 'פרויקטים' );
	$urls   = array();
	foreach ( $labels as $pt => $label ) {
		$u = get_post_type_archive_link( $pt );
		if ( $u ) { $urls[ untrailingslashit( $u ) ] = $label; }
	}
	/* the profession level on a professional card, the same level the schema trail carries */
	if ( is_singular( 'nadlan_professional' ) ) {
		$level = nadlan_breadcrumbs_profession( get_queried_object_id() );
		if ( $level && count( $links ) >= 2 ) {
			array_splice( $links, count( $links ) - 1, 0, array( array( 'url' => $level[1], 'text' => $level[0], 'allow_html' => false ) ) );
		}
	}
	foreach ( $links as $i => $link ) {
		if ( ! is_array( $link ) ) { continue; }
		$pt = isset( $link['ptarchive'] ) ? (string) $link['ptarchive'] : '';
		if ( '' !== $pt && isset( $labels[ $pt ] ) ) {
			$links[ $i ]['text'] = $labels[ $pt ];
		} elseif ( ! empty( $link['url'] ) && isset( $urls[ untrailingslashit( (string) $link['url'] ) ] ) ) {
			$links[ $i ]['text'] = $urls[ untrailingslashit( (string) $link['url'] ) ];
		}
	}
	return $links;
}, 20 );
