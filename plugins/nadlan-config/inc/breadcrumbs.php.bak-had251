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
			$prof = (string) get_post_meta( get_the_ID(), 'profession', true );
			$prof_label = array( 'kablan' => 'קבלנים', 'shamai' => 'שמאים', 'bedek_bait' => 'בדק בית', 'mashkanta' => 'יועצי משכנתאות',
				'architect' => 'אדריכלים', 'lawyer' => 'עורכי דין', 'inspector' => 'מפקחי בנייה' )[ $prof ] ?? '';
			if ( $prof_label ) { $items[] = array( 'name' => $prof_label, 'url' => add_query_arg( 'profession', $prof, home_url( '/professionals/' ) ) ); }
			$items[] = array( 'name' => get_the_title(), 'url' => get_permalink() );
		} elseif ( is_post_type_archive( 'nadlan_property' ) ) { $items[] = array( 'name' => 'דירות', 'url' => home_url( '/properties/' ) ); }
		elseif ( is_post_type_archive( 'nadlan_project' ) )    { $items[] = array( 'name' => 'פרויקטים', 'url' => home_url( '/projects/' ) ); }
		elseif ( is_post_type_archive( 'nadlan_professional' ) ){ $items[] = array( 'name' => 'אנשי מקצוע', 'url' => home_url( '/professionals/' ) ); }
		else { return array(); }
		return $items;
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
	echo "\n<script type=\"application/ld+json\">" . wp_json_encode( $ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
}, 22 );

/* Single BreadcrumbList owner (source-audit 30.8.2026): drop Yoast's graph piece. */
add_filter( 'wpseo_schema_needs_breadcrumb', '__return_false' );
