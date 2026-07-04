<?php
/**
 * nadlan-config - Archive facets / filters (v1.14.0)
 *
 * Yad2/Madlan-grade filtering on /properties/, /projects/, /professionals/.
 * Server-side `pre_get_posts` translates URL query params (?city=&rooms_min=&
 * price_max=&listing_type=&profession=&project_type=) into the appropriate
 * meta_query so filtered URLs are CRAWLABLE + LINKABLE (great for SEO + share).
 *
 * Client side: a thin filter UI is injected via shortcode [nadlan_facets type=]
 * AND auto-prepended on the archive (just before the loop). Submits as a GET form
 * so URLs stay clean.
 *
 * Cannibalization safety: only certain facet COMBINATIONS are valuable
 * (city alone, city+rooms, city+price-band). Everything else (single price-band
 * across all cities, deep combinations) emits noindex,follow to avoid the
 * scaled-content abuse penalty.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_facets_apply' ) ) {
	function nadlan_facets_apply( $q ) {
		if ( is_admin() || ! $q->is_main_query() ) { return; }
		$pt = $q->get( 'post_type' );
		if ( ! $pt && $q->is_post_type_archive() ) { $pt = $q->queried_object->name ?? ''; }
		if ( ! in_array( $pt, array( 'nadlan_property', 'nadlan_project', 'nadlan_professional' ), true ) ) { return; }
		$mq = (array) $q->get( 'meta_query' );
		$add = array();
		// City: partial, case-insensitive LIKE so "תל אביב" matches "תל אביב יפו"
		// and trailing spaces / inexact typing still find results.
		if ( ! empty( $_GET['city'] ) )         { $add[] = array( 'key' => 'city', 'value' => sanitize_text_field( wp_unslash( $_GET['city'] ) ), 'compare' => 'LIKE' ); }
		if ( $pt === 'nadlan_property' ) {
			if ( ! empty( $_GET['listing_type'] ) ){ $add[] = array( 'key' => 'listing_type', 'value' => sanitize_text_field( wp_unslash( $_GET['listing_type'] ) ) ); }
			if ( ! empty( $_GET['rooms_min'] ) )   { $add[] = array( 'key' => 'rooms', 'value' => (float) $_GET['rooms_min'], 'type' => 'NUMERIC', 'compare' => '>=' ); }
			if ( ! empty( $_GET['price_min'] ) )   { $add[] = array( 'key' => 'price', 'value' => (int) $_GET['price_min'], 'type' => 'NUMERIC', 'compare' => '>=' ); }
			if ( ! empty( $_GET['price_max'] ) )   { $add[] = array( 'key' => 'price', 'value' => (int) $_GET['price_max'], 'type' => 'NUMERIC', 'compare' => '<=' ); }
		} elseif ( $pt === 'nadlan_project' ) {
			if ( ! empty( $_GET['project_type'] ) ){ $add[] = array( 'key' => 'project_type', 'value' => sanitize_text_field( wp_unslash( $_GET['project_type'] ) ) ); }
			if ( ! empty( $_GET['status'] ) )      { $add[] = array( 'key' => 'project_status', 'value' => sanitize_text_field( wp_unslash( $_GET['status'] ) ) ); }
		} elseif ( $pt === 'nadlan_professional' ) {
			if ( ! empty( $_GET['profession'] ) )  { $add[] = array( 'key' => 'profession', 'value' => sanitize_key( $_GET['profession'] ) ); }
		}
		if ( $add ) {
			$mq = array_merge( $mq ? array( $mq ) : array(), $add );
			$q->set( 'meta_query', array_merge( array( 'relation' => 'AND' ), $mq ) );
		}
	}
}
add_action( 'pre_get_posts', 'nadlan_facets_apply' );

/* Noindex on combinations Google would call "scaled doorway" */
add_filter( 'wp_robots', function ( $r ) {
	if ( ! is_post_type_archive( array( 'nadlan_property', 'nadlan_project', 'nadlan_professional' ) ) ) { return $r; }
	$facets = array_intersect_key( $_GET, array_flip( array( 'city','listing_type','rooms_min','price_min','price_max','project_type','status','profession' ) ) );
	if ( ! $facets ) { return $r; }
	// Allow only valuable combos
	$ok = false;
	$keys = array_keys( $facets );
	sort( $keys );
	$allowed = array(
		array( 'city' ),
		array( 'city', 'rooms_min' ),
		array( 'city', 'listing_type' ),
		array( 'city', 'price_max' ),
		array( 'city', 'price_min', 'price_max' ),
		array( 'city', 'project_type' ),
		array( 'city', 'profession' ),
		array( 'profession' ),
		array( 'project_type' ),
	);
	foreach ( $allowed as $combo ) {
		$c = $combo; sort( $c );
		if ( $c === $keys ) { $ok = true; break; }
	}
	if ( ! $ok ) { $r['noindex'] = true; $r['follow'] = true; unset( $r['index'] ); }
	return $r;
}, 25 );

/* Facets UI */
if ( ! function_exists( 'nadlan_facets_render' ) ) {
	function nadlan_facets_render( $atts = array() ) {
		$a = shortcode_atts( array( 'type' => 'nadlan_property' ), $atts );
		$g = function ( $k ) { return isset( $_GET[ $k ] ) ? esc_attr( wp_unslash( $_GET[ $k ] ) ) : ''; };
		ob_start(); ?>
<form class="nlfacets" dir="rtl" method="get">
	<input type="text" name="city" value="<?php echo $g( 'city' ); ?>" placeholder="עיר">
	<?php if ( $a['type'] === 'nadlan_property' ) : ?>
		<select name="listing_type"><option value="">עסקה</option>
			<option value="sale"<?php selected( $g( 'listing_type' ), 'sale' ); ?>>מכירה</option>
			<option value="rent"<?php selected( $g( 'listing_type' ), 'rent' ); ?>>שכירות</option>
		</select>
		<input type="number" name="rooms_min" value="<?php echo $g( 'rooms_min' ); ?>" placeholder="חדרים (מינ׳)" step="0.5">
		<input type="number" name="price_max" value="<?php echo $g( 'price_max' ); ?>" placeholder="מחיר עד">
	<?php elseif ( $a['type'] === 'nadlan_project' ) : ?>
		<select name="project_type"><option value="">סוג פרויקט</option>
			<option value="new"<?php selected( $g( 'project_type' ), 'new' ); ?>>בנייה חדשה</option>
			<option value="tama38"<?php selected( $g( 'project_type' ), 'tama38' ); ?>>תמ"א 38</option>
			<option value="pinui_binui"<?php selected( $g( 'project_type' ), 'pinui_binui' ); ?>>פינוי-בינוי</option>
			<option value="mehir_lamishtaken"<?php selected( $g( 'project_type' ), 'mehir_lamishtaken' ); ?>>מחיר למשתכן</option>
		</select>
	<?php elseif ( $a['type'] === 'nadlan_professional' ) : ?>
		<select name="profession"><option value="">מקצוע</option>
			<option value="kablan"<?php selected( $g( 'profession' ), 'kablan' ); ?>>קבלן</option>
			<option value="shamai"<?php selected( $g( 'profession' ), 'shamai' ); ?>>שמאי</option>
			<option value="bedek_bait"<?php selected( $g( 'profession' ), 'bedek_bait' ); ?>>בדק בית</option>
			<option value="mashkanta"<?php selected( $g( 'profession' ), 'mashkanta' ); ?>>יועץ משכנתאות</option>
			<option value="architect"<?php selected( $g( 'profession' ), 'architect' ); ?>>אדריכל</option>
			<option value="lawyer"<?php selected( $g( 'profession' ), 'lawyer' ); ?>>עו"ד מקרקעין</option>
		</select>
	<?php endif; ?>
	<button type="submit">סננו</button>
	<a href="<?php echo esc_url( strtok( $_SERVER['REQUEST_URI'] ?? '/', '?' ) ); ?>" class="nlfacets-clr">איפוס</a>
</form>
<style>
.nlfacets{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0;padding:14px;background:#FAF7F1;border-radius:6px}
.nlfacets input,.nlfacets select{padding:9px;border:1px solid #ccc;border-radius:4px;font:inherit;flex:1;min-width:120px}
.nlfacets button{padding:9px 22px;background:#1B1A17;color:#FAF7F1;border:0;border-radius:4px;cursor:pointer}
.nlfacets-clr{align-self:center;font-size:13px;color:#777;text-decoration:none}
</style>
		<?php
		return ob_get_clean();
	}
}
add_shortcode( 'nadlan_facets', 'nadlan_facets_render' );

/* Auto-inject on archive - DISABLED v1.31.0: archive-grid.php / directory.php render
 * the facets bar explicitly in the right place, so this loop_start hook produced a
 * duplicate form. Kept as a no-op for back-compat. */
// add_action( 'loop_start', function ( $q ) { ... }, 6 );
