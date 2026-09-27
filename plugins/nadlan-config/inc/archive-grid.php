<?php
/**
 * nadlan-config - Branded archive grid for directory CPTs (v1.28.0)
 *
 * The nadlan_professional / nadlan_project / nadlan_property archives are now linked
 * from the homepage, nav, footer and /catalog/ - but they were rendering through the
 * theme's default archive loop, which shows these data-only CPTs (no editor body) as
 * blank/plain rows. With 1500+ imported professionals that looked broken.
 *
 * This module intercepts those archives (template_redirect, like city-hubs) and renders
 * a clean, branded, paginated CARD GRID built from the real meta - name, city,
 * classification, registry number, claim badge - matching the catalog skin. Facets bar
 * on top (reuses [nadlan_facets]). Keeps the theme header/footer so it stays on-brand.
 *
 * Opt-out: define NADLAN_DISABLE_ARCHIVE_GRID to fall back to the theme template.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_archive_grid_dispatch' ) ) {
	function nadlan_archive_grid_dispatch() {
		if ( defined( 'NADLAN_DISABLE_ARCHIVE_GRID' ) && NADLAN_DISABLE_ARCHIVE_GRID ) { return; }
		// Professionals get the premium dynamic directory (inc/directory.php) instead.
		// v1.36.0: nadlan_project now handled by the premium directory in inc/directory.php
		// (was previously routed here, producing the old paginated archive grid). Property
		// still served here until its premium directory ships.
		if ( ! is_post_type_archive( array( 'nadlan_property' ) ) ) { return; }
		if ( is_admin() ) { return; }
		nadlan_archive_grid_render();
		exit;
	}
}
add_action( 'template_redirect', 'nadlan_archive_grid_dispatch', 6 );

if ( ! function_exists( 'nadlan_archive_grid_render' ) ) {
	function nadlan_archive_grid_render() {
		global $wp_query;
		$pt = get_query_var( 'post_type' );
		if ( is_array( $pt ) ) { $pt = reset( $pt ); }

		$meta = array(
			'nadlan_professional' => array(
				'h1'  => 'בעלי מקצוע רשומים',
				'sub' => 'קבלנים, שמאים ומפקחים מאומתים - מתוך פנקס הקבלנים הרשומים (gov.il). סינון לפי עיר, סיווג וענף.',
				'badge' => 'קבלן רשום',
			),
			'nadlan_project' => array(
				'h1'  => 'פרויקטים והתחדשות עירונית',
				'sub' => 'תמ״א 38, פינוי-בינוי ובנייה חדשה - מספר תוכנית, יזם, סטטוס ויחידות דיור.',
				'badge' => 'פרויקט',
			),
			'nadlan_property' => array(
				'h1'  => 'נכסים למכירה והשקעה',
				'sub' => 'דירות ובתים עם בדיקה משפטית מקדימה - מחיר, חדרים, מ״ר ושכונה.',
				'badge' => 'נכס',
			),
		);
		if ( 'nadlan_property' === $pt && function_exists( 'nadlan_pl_render' ) ) { nadlan_pl_render(); return; } // ListingsPage v46
		$L = $meta[ $pt ] ?? $meta['nadlan_professional'];
		$total = (int) $wp_query->found_posts;
		$paged = max( 1, (int) get_query_var( 'paged' ) );
		$pages = (int) $wp_query->max_num_pages;

		get_header();
		if ( function_exists( 'block_template_part' ) ) { block_template_part( 'header' ); }
		echo nadlan_archive_grid_css();
		?>
<div class="nlag" dir="rtl">
	<nav class="nlag-crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">בית</a><span>›</span><span><?php echo esc_html( $L['h1'] ); ?></span></nav>
	<header class="nlag-head">
		<h1><?php echo esc_html( $L['h1'] ); ?></h1>
		<p class="nlag-sub"><?php echo esc_html( $L['sub'] ); ?></p>
		<p class="nlag-count"><strong><?php echo number_format( $total ); ?></strong> רשומות</p>
	</header>

	<?php if ( shortcode_exists( 'nadlan_facets' ) ) { echo do_shortcode( '[nadlan_facets type="' . esc_attr( $pt ) . '"]' ); } ?>

	<?php
	// ItemList JSON-LD for the visible cards (rich-result eligibility).
	if ( have_posts() ) {
		$items = array(); $pos = 1;
		foreach ( $wp_query->posts as $sp ) {
			$items[] = array( '@type' => 'ListItem', 'position' => $pos++, 'url' => get_permalink( $sp ), 'name' => get_the_title( $sp ) );
		}
		echo '<script type="application/ld+json">' . wp_json_encode( array(
			'@context' => 'https://schema.org', '@type' => 'ItemList',
			'name' => $L['h1'], 'numberOfItems' => $total,
			'itemListElement' => $items,
		), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>';
	}
	?>
	<?php if ( have_posts() ) : ?>
	<div class="nlag-grid">
		<?php while ( have_posts() ) : the_post();
			$id   = get_the_ID();
			$city = nadlan_meta_norm( get_post_meta( $id, 'city', true ) );
			$lat = get_post_meta( $id, 'lat', true ); $lng = get_post_meta( $id, 'lng', true );
			echo '<a class="nlag-card" href="' . esc_url( get_permalink() ) . '"' . ( $lat && $lng ? ' data-lat="' . esc_attr( $lat ) . '" data-lng="' . esc_attr( $lng ) . '"' : '' ) . '>';
			// the real image leads the card (owner decision 1, 2026-07-07)
			$thumb = get_the_post_thumbnail_url( $id, 'medium_large' );
			if ( $thumb ) {
				echo '<span class="nlag-media" style="background-image:url(' . esc_url( $thumb ) . ')"><i class="nlag-km" hidden></i></span>';
			}
			echo '<span class="nlag-badge">' . esc_html( $L['badge'] ) . '</span>';
			echo '<h3>' . esc_html( get_the_title() ) . '</h3>';
			if ( $city ) { echo '<span class="nlag-city">' . esc_html( $city ) . ( $thumb ? '' : ' <i class="nlag-km" hidden></i>' ) . '</span>'; }
			echo nadlan_archive_card_meta( $id, $pt );
			if ( 'nadlan_property' === $pt ) {
				$chips = array();
				foreach ( array( 'protected_room' => 'ממ״ד', 'ac' => 'מיזוג', 'elevator' => 'מעלית', 'parking' => 'חניה', 'storage' => 'מחסן' ) as $mk => $lbl ) {
					if ( get_post_meta( $id, $mk, true ) ) { $chips[] = $lbl; }
				}
				$b = (int) get_post_meta( $id, 'balcony_sqm', true );
				if ( $b ) { array_unshift( $chips, 'מרפסת ' . $b . ' מ״ר' ); }
				if ( $chips ) {
					echo '<span class="nlag-chips">';
					foreach ( array_slice( $chips, 0, 4 ) as $c ) { echo '<em>' . esc_html( $c ) . '</em>'; }
					echo '</span>';
				}
			}
			$claimed = get_post_meta( $id, 'claim_status', true ) === 'verified';
			if ( $claimed ) { echo '<span class="nlag-verified">✓ מאומת</span>'; }
			echo '<span class="nlag-go">לכרטיס ←</span>';
			echo '</a>';
		endwhile; ?>
	</div>

	<?php if ( $pages > 1 ) : ?>
	<nav class="nlag-pager">
		<?php
		echo paginate_links( array(
			'total'     => $pages,
			'current'   => $paged,
			'prev_text' => '← הקודם',
			'next_text' => 'הבא →',
			'mid_size'  => 2,
		) );
		?>
	</nav>
	<?php endif; ?>


<script>
(function(){
	var cards=[].slice.call(document.querySelectorAll(".nlag-card[data-lat]"));
	if(!cards.length)return;
	function show(lat,lng,approx){
		cards.forEach(function(c){
			var la=parseFloat(c.dataset.lat),ln=parseFloat(c.dataset.lng);
			if(!la||!ln)return;
			var R=6371,dLa=(la-lat)*Math.PI/180,dLn=(ln-lng)*Math.PI/180;
			var a=Math.sin(dLa/2)*Math.sin(dLa/2)+Math.cos(lat*Math.PI/180)*Math.cos(la*Math.PI/180)*Math.sin(dLn/2)*Math.sin(dLn/2);
			var km=R*2*Math.atan2(Math.sqrt(a),Math.sqrt(1-a));
			if(km>120)return;
			var el=c.querySelector(".nlag-km");
			if(el){el.hidden=false;el.textContent=(km<1?"פחות מק\u05F4מ":"כ-"+(km<10?km.toFixed(1):Math.round(km))+" ק\u05F4מ")+" ממך"+(approx?" · משוער":"");}
		});
	}
	try{fetch("https://ipwho.is/").then(function(r){return r.json()}).then(function(g){
		if(g&&g.success&&g.country_code==="IL"&&g.latitude){show(g.latitude,g.longitude,true)}
	}).catch(function(){})}catch(e){}
})();
</script>
	<?php else : ?>
	<p class="nlag-empty">לא נמצאו רשומות התואמות את הסינון. <a href="<?php echo esc_url( get_post_type_archive_link( $pt ) ); ?>">איפוס סינון</a></p>
	<?php endif; ?>
</div>
		<?php
		if ( function_exists( 'block_template_part' ) ) { block_template_part( 'footer' ); }
		get_footer();
	}
}

/* ==========================================================================================================
 * ListingsPage (design system v46, 28.9.2026): /properties/ and its filtered forms.
 * One header (the site's), the H1 by the filter, a true lead, the deal tabs with real counts, one filter row, the portal
 * listing card (the deal, the price when published, rooms, area, floor, who publishes and the licence), the seeded demo
 * listings marked and last (never counted, never on the map), the map only when real listings have coordinates.
 * The old page had two H1s, the promise "בדיקה משפטית מקדימה" (no such check), a "נכס" badge on every card, the map as a
 * grid tile and a floating publish pill over the cards; seven demo listings were shown as real homes with prices.
 * ========================================================================================================== */
if ( ! function_exists( 'nadlan_pl_is_demo' ) ) {
	function nadlan_pl_is_demo( $id ) {
		return in_array( (string) get_post_meta( $id, 'is_demo', true ), array( '1', 'true' ), true ) || 'demo_seed' === (string) get_post_meta( $id, 'source', true );
	}
}

if ( ! function_exists( 'nadlan_pl_nodemo' ) ) {
	/** The meta clause "not a demo listing". */
	function nadlan_pl_nodemo() {
		return array( 'relation' => 'OR', array( 'key' => 'is_demo', 'compare' => 'NOT EXISTS' ), array( 'key' => 'is_demo', 'value' => array( '1', 'true' ), 'compare' => 'NOT IN' ) );
	}
}

if ( ! function_exists( 'nadlan_pl_filters' ) ) {
	/** The same filters as inc/facets.php (city, rooms, price), without the deal: the tabs carry it. */
	function nadlan_pl_filters() {
		$f = array();
		if ( ! empty( $_GET['city'] ) ) { // the city or the neighbourhood, as inc/facets.php
			$cv  = sanitize_text_field( wp_unslash( $_GET['city'] ) );
			$f[] = array( 'relation' => 'OR', array( 'key' => 'city', 'value' => $cv, 'compare' => 'LIKE' ), array( 'key' => 'neighborhood', 'value' => $cv, 'compare' => 'LIKE' ) );
		}
		if ( ! empty( $_GET['rooms_min'] ) ) { $f[] = array( 'key' => 'rooms', 'value' => (float) $_GET['rooms_min'], 'type' => 'NUMERIC', 'compare' => '>=' ); }
		if ( ! empty( $_GET['price_min'] ) ) { $f[] = array( 'key' => 'price', 'value' => (int) $_GET['price_min'], 'type' => 'NUMERIC', 'compare' => '>=' ); }
		if ( ! empty( $_GET['price_max'] ) ) { $f[] = array( 'key' => 'price', 'value' => (int) $_GET['price_max'], 'type' => 'NUMERIC', 'compare' => '<=' ); }
		return $f;
	}
}

if ( ! function_exists( 'nadlan_pl_count' ) ) {
	/** Real listings (demos excluded) under the current filters, for one deal ('' = both). */
	function nadlan_pl_count( $deal = '', $extra = array() ) {
		$mq = array_merge( array( 'relation' => 'AND', nadlan_pl_nodemo() ), nadlan_pl_filters(), $extra );
		if ( '' !== $deal ) { $mq[] = array( 'key' => 'listing_type', 'value' => $deal ); }
		return count( get_posts( array( 'post_type' => 'nadlan_property', 'post_status' => 'publish', 'posts_per_page' => -1, 'fields' => 'ids', 'no_found_rows' => true, 'meta_query' => $mq ) ) );
	}
}

/* real listings first, the seeded demos last; twelve to a page (three rows of four on desktop's three columns) */
add_action( 'pre_get_posts', function ( $q ) {
	if ( is_admin() || ! $q->is_main_query() || ! $q->is_post_type_archive( 'nadlan_property' ) ) { return; }
	$q->set( 'posts_per_page', 12 );
}, 20 );
add_filter( 'posts_clauses', function ( $c, $q ) {
	if ( is_admin() || ! $q->is_main_query() || ! $q->is_post_type_archive( 'nadlan_property' ) ) { return $c; }
	global $wpdb;
	$demo = "(SELECT COUNT(*) FROM {$wpdb->postmeta} nlpl_d WHERE nlpl_d.post_id = {$wpdb->posts}.ID AND ( ( nlpl_d.meta_key = 'is_demo' AND nlpl_d.meta_value IN ('1','true') ) OR ( nlpl_d.meta_key = 'source' AND nlpl_d.meta_value = 'demo_seed' ) ))";
	$c['orderby'] = $demo . ' ASC' . ( '' !== trim( (string) $c['orderby'] ) ? ', ' . $c['orderby'] : ", {$wpdb->posts}.post_date DESC" );
	return $c;
}, 10, 2 );

/* the page's one publish button is in its head: no floating pill over the cards (the listing pages keep theirs) */
add_filter( 'nadlan_cta_start_map', function ( $m ) {
	// the archive's publish button is in its head; a demo listing's is in its panel (ListingPage v47): no floating pill over them
	if ( is_post_type_archive( 'nadlan_property' ) ) { return array(); }
	if ( is_singular( 'nadlan_property' ) && nadlan_pl_is_demo( (int) get_queried_object_id() ) ) { return array(); }
	return $m;
} );

if ( ! function_exists( 'nadlan_pl_card' ) ) {
	function nadlan_pl_card( $id ) {
		$demo  = nadlan_pl_is_demo( $id );
		$deal  = (string) get_post_meta( $id, 'listing_type', true );
		$types = array( 'apartment' => 'דירה', 'penthouse' => 'פנטהאוז', 'garden' => 'דירת גן', 'cottage' => 'קוטג׳', 'villa' => 'בית פרטי', 'duplex' => 'דופלקס', 'studio' => 'סטודיו', 'house' => 'בית פרטי', 'land' => 'מגרש', 'office' => 'משרד' );
		$type  = $types[ (string) get_post_meta( $id, 'property_type', true ) ] ?? '';
		$area  = implode( ', ', array_filter( array( nadlan_meta_norm( get_post_meta( $id, 'neighborhood', true ) ), nadlan_meta_norm( get_post_meta( $id, 'city', true ) ) ) ) );
		$kick  = implode( ' · ', array_filter( array( $type, $area ) ) );
		$price = (float) get_post_meta( $id, 'price', true );
		$size  = (float) get_post_meta( $id, 'size_sqm', true );
		$rooms = (float) get_post_meta( $id, 'rooms', true );
		$floor = (int) get_post_meta( $id, 'floor', true );
		$tot   = (int) get_post_meta( $id, 'total_floors', true );
		$num   = function ( $n ) { return ( floor( $n ) == $n ) ? number_format( $n ) : rtrim( rtrim( number_format( $n, 1 ), '0' ), '.' ); };
		$specs = array();
		if ( $rooms > 0 ) { $specs[] = $num( $rooms ) . ' חד׳'; }
		if ( $size > 0 )  { $specs[] = $num( $size ) . ' מ״ר'; }
		if ( $floor > 0 ) { $specs[] = 'קומה ' . $floor . ( $tot >= $floor ? ' מתוך ' . $tot : '' ); }
		$amen = array();
		$bal  = (int) get_post_meta( $id, 'balcony_sqm', true );
		if ( $bal > 0 ) { $amen[] = 'מרפסת ' . $bal . ' מ״ר'; }
		foreach ( array( 'parking' => 'חניה', 'storage' => 'מחסן', 'protected_room' => 'ממ״ד', 'elevator' => 'מעלית', 'ac' => 'מיזוג' ) as $k => $l ) {
			if ( in_array( (string) get_post_meta( $id, $k, true ), array( '1', 'true', 'yes', 'on' ), true ) ) { $amen[] = $l; }
		}
		$amen  = array_slice( $amen, 0, 3 );
		$photo = get_the_post_thumbnail_url( $id, 'medium_large' );
		if ( ! $photo ) { $csv = array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $id, 'photos_csv', true ) ) ) ); $photo = $csv ? reset( $csv ) : ''; }
		$lat   = (float) get_post_meta( $id, 'lat', true );
		$lng   = (float) get_post_meta( $id, 'lng', true );
		// who publishes (Brokers Ethics Regulations, reg. 19(a): the broker's name, status and licence on the publication)
		$by  = '';
		$bid = (int) get_post_meta( $id, 'nl_broker_id', true );
		if ( $demo ) {
			$by = '<span class="nlpl-by"><span>דוגמה למודעה באתר</span></span>';
		} elseif ( $bid > 0 && 'publish' === get_post_status( $bid ) ) {
			$bn    = function_exists( 'nadlan_prof_person_name' ) ? (string) nadlan_prof_person_name( $bid ) : get_the_title( $bid );
			$bn    = trim( wp_strip_all_tags( html_entity_decode( $bn, ENT_QUOTES, 'UTF-8' ) ) );
			$role  = function_exists( 'nadlan_dir_prof_label' ) ? nadlan_dir_prof_label( 'metavech', $bid ) : 'תיווך נדל״ן';
			$lic   = trim( (string) get_post_meta( $bid, 'license_number', true ) );
			$w     = preg_split( '/\s+/u', trim( preg_replace( '/[^\p{L}\s]/u', ' ', $bn ) ) );
			$ini   = mb_substr( (string) ( $w[0] ?? '' ), 0, 1 ) . ( isset( $w[1] ) && '' !== $w[1] ? '.' . mb_substr( $w[1], 0, 1 ) : '' );
			$face  = has_post_thumbnail( $bid ) ? get_the_post_thumbnail( $bid, 'thumbnail', array( 'alt' => '', 'loading' => 'lazy', 'decoding' => 'async' ) ) : esc_html( $ini );
			$by    = '<span class="nlpl-by"><b aria-hidden="true">' . $face . '</b><span>' . esc_html( $bn . ' · ' . $role . ( '' !== $lic ? ' · רישיון ' . $lic : '' ) ) . '</span></span>';
		} elseif ( 'owner_wizard' === (string) get_post_meta( $id, 'source', true ) || (int) get_post_meta( $id, 'owner_user_id', true ) > 0 ) {
			$by = '<span class="nlpl-by"><span>מבעלי הנכס</span></span>';
		}
		if ( $demo ) {
			$badge = '<span class="nlpl-deal nlpl-deal--demo">מודעה לדוגמה</span>';
		} elseif ( 'rent' === $deal ) {
			$badge = '<span class="nlpl-deal nlpl-deal--rent">להשכרה</span>';
		} elseif ( 'sale' === $deal ) {
			$badge = '<span class="nlpl-deal">למכירה</span>';
		} else {
			$badge = '';
		}
		$pr = '';
		if ( $price > 0 ) {
			$pr = '<span class="nlpl-price"><strong>₪' . number_format( $price ) . '</strong>';
			if ( 'rent' === $deal ) {
				$pr .= '<small>לחודש</small>';
			} elseif ( $size > 0 ) {
				$pr .= '<small>' . number_format( round( $price / $size ) ) . ' ₪ למ״ר</small>';
			}
			$pr .= '</span>';
		}
		$h  = '<a class="nlpl-card' . ( $demo ? ' nlpl-card--demo' : '' ) . '" href="' . esc_url( get_permalink( $id ) ) . '"' . ( ! $demo && $lat && $lng ? ' data-lat="' . esc_attr( $lat ) . '" data-lng="' . esc_attr( $lng ) . '"' : '' ) . '>';
		$h .= '<span class="nlpl-media">' . ( $photo ? '<img src="' . esc_url( $photo ) . '" alt="" loading="lazy" decoding="async">' : '' ) . $badge . '<i class="nlag-km" hidden></i></span>';
		$h .= '<span class="nlpl-body">' . ( '' !== $kick ? '<span class="nlpl-kicker">' . esc_html( $kick ) . '</span>' : '' );
		$h .= '<b class="nlpl-title">' . esc_html( html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ) ) . '</b>' . $pr;
		if ( $specs ) { $h .= '<span class="nlpl-specs">' . implode( '', array_map( function ( $s ) { return '<span>' . esc_html( $s ) . '</span>'; }, $specs ) ) . '</span>'; }
		if ( $amen )  { $h .= '<span class="nlpl-amen">' . implode( '', array_map( function ( $s ) { return '<em>' . esc_html( $s ) . '</em>'; }, $amen ) ) . '</span>'; }
		$h .= '<span class="nlpl-foot">' . $by . '<span class="nlpl-go" aria-hidden="true">←</span></span></span></a>';
		return $h;
	}
}

if ( ! function_exists( 'nadlan_pl_render' ) ) {
	function nadlan_pl_render() {
		global $wp_query;
		$deal  = isset( $_GET['listing_type'] ) ? sanitize_key( wp_unslash( $_GET['listing_type'] ) ) : '';
		$deal  = in_array( $deal, array( 'sale', 'rent' ), true ) ? $deal : '';
		$city  = isset( $_GET['city'] ) ? sanitize_text_field( wp_unslash( $_GET['city'] ) ) : '';
		$rooms = isset( $_GET['rooms_min'] ) ? (float) $_GET['rooms_min'] : 0;
		$pmax  = isset( $_GET['price_max'] ) ? (int) $_GET['price_max'] : 0;
		$paged = max( 1, (int) get_query_var( 'paged' ) );
		$pages = (int) $wp_query->max_num_pages;
		$n     = array( '' => nadlan_pl_count( '' ), 'sale' => nadlan_pl_count( 'sale' ), 'rent' => nadlan_pl_count( 'rent' ) );
		$real  = $n[ $deal ];
		$base  = array( '' => 'דירות למכירה ולהשכרה', 'sale' => 'דירות למכירה', 'rent' => 'דירות להשכרה' );
		$h1    = $base[ $deal ] . ( '' !== $city ? ' ב' . $city : '' );
		$what  = array( '' => 'למכירה ולהשכרה', 'sale' => 'למכירה', 'rent' => 'להשכרה' );
		$cnt   = 1 === $real ? 'מודעה אחת' : number_format( $real ) . ' מודעות';
		$lead  = $real > 0
			? $cnt . ' של דירות ובתים ' . $what[ $deal ] . ( '' !== $city ? ' ב' . $city : '' ) . ', ממתווכים עם רישיון ומבעלי נכסים. בכל מודעה המחיר כשפורסם, החדרים, השטח, הקומה ומה יש בדירה.'
			: 'אין כרגע מודעות שמתאימות לחיפוש. אפשר לשנות את הסינון, או לחזור לכל המודעות.';
		$keep  = array_filter( array( 'city' => $city, 'rooms_min' => $rooms ? $rooms : '', 'price_max' => $pmax ? $pmax : '' ), 'strlen' );
		$arch  = get_post_type_archive_link( 'nadlan_property' );
		$tab   = function ( $d ) use ( $keep, $arch ) { return add_query_arg( array_merge( $keep, '' !== $d ? array( 'listing_type' => $d ) : array() ), $arch ); };
		$maps  = $real > 0 ? nadlan_pl_count( $deal, array( array( 'key' => 'lat', 'value' => array( '', '0' ), 'compare' => 'NOT IN' ) ) ) : 0;

		if ( function_exists( 'nadlan_dir_header_single_h1' ) ) { nadlan_dir_header_single_h1(); } else { get_header(); }
		if ( function_exists( 'block_template_part' ) ) { block_template_part( 'header' ); }
		echo '<style id="nadlan-pl-css">' . nadlan_pl_css() . '</style>'; // phpcs:ignore
		?>
<div class="nlpl" dir="rtl" lang="he">
	<nav class="nlpl-crumbs" aria-label="ניווט"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">בית</a><span aria-hidden="true">›</span><?php if ( '' !== $deal || '' !== $city ) : ?><a href="<?php echo esc_url( $arch ); ?>">דירות</a><span aria-hidden="true">›</span><span aria-current="page"><?php echo esc_html( $h1 ); ?></span><?php else : ?><span aria-current="page">דירות</span><?php endif; ?></nav>
	<header class="nlpl-head">
		<div><h1><?php echo esc_html( $h1 ); ?></h1><p class="nlpl-lead"><?php echo esc_html( $lead ); ?></p></div>
		<a class="nlpl-post" href="<?php echo esc_url( home_url( '/post-listing/' ) ); ?>">+ פרסום מודעה בחינם</a>
	</header>
	<nav class="nlpl-tabs" aria-label="סוג עסקה">
		<?php foreach ( array( '' => 'הכל', 'sale' => 'למכירה', 'rent' => 'להשכרה' ) as $d => $l ) : ?><a href="<?php echo esc_url( $tab( $d ) ); ?>"<?php echo $d === $deal ? ' aria-current="page"' : ''; ?>><?php echo esc_html( $l ); ?> <i><?php echo (int) $n[ $d ]; ?></i></a><?php endforeach; ?>
	</nav>
	<form class="nlpl-filters" method="get" action="<?php echo esc_url( $arch ); ?>" role="search" aria-label="סינון מודעות">
		<?php if ( '' !== $deal ) : ?><input type="hidden" name="listing_type" value="<?php echo esc_attr( $deal ); ?>"><?php endif; ?>
		<input class="nlpl-f-city" type="text" name="city" value="<?php echo esc_attr( $city ); ?>" placeholder="עיר או שכונה" aria-label="עיר או שכונה">
		<select name="rooms_min" aria-label="מספר חדרים"><option value="">חדרים: הכל</option><?php foreach ( array( 2, 3, 4, 5 ) as $r ) : ?><option value="<?php echo (int) $r; ?>"<?php selected( (int) $rooms, $r ); ?>>מ־<?php echo (int) $r; ?> חדרים</option><?php endforeach; ?></select>
		<input type="text" name="price_max" inputmode="numeric" pattern="[0-9]*" value="<?php echo $pmax ? (int) $pmax : ''; ?>" placeholder="מחיר עד (₪)" aria-label="מחיר עד">
		<button type="submit">סננו</button>
		<a class="nlpl-clear" href="<?php echo esc_url( '' !== $deal ? add_query_arg( 'listing_type', $deal, $arch ) : $arch ); ?>">ניקוי</a>
	</form>
	<?php if ( $real > 0 ) : /* never "0 מודעות": the lead says there are none */ ?><div class="nlpl-bar"><span><b><?php echo esc_html( number_format( $real ) ); ?></b> <?php echo 1 === $real ? 'מודעה' : 'מודעות'; ?></span></div><?php endif; ?>
	<?php if ( $maps > 0 && function_exists( 'nadlan_map_render' ) ) : ?><div class="nlpl-map"><?php echo nadlan_map_render( array( 'city' => $city, 'listing_type' => $deal, 'height' => '360px' ) ); // phpcs:ignore ?></div><?php endif; ?>
	<?php
	$posts = $wp_query->posts;
	if ( $posts ) {
		$items = array(); $pos = 1;
		foreach ( $posts as $p ) { if ( ! nadlan_pl_is_demo( $p->ID ) ) { $items[] = array( '@type' => 'ListItem', 'position' => $pos++, 'url' => get_permalink( $p ), 'name' => html_entity_decode( get_the_title( $p ), ENT_QUOTES, 'UTF-8' ) ); } }
		if ( $items ) {
			echo '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@type' => 'ItemList', 'name' => $h1, 'numberOfItems' => $real, 'itemListElement' => $items ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>'; // phpcs:ignore
		}
		echo '<div class="nlpl-grid">';
		$sep = false;
		foreach ( $posts as $p ) {
			if ( ! $sep && nadlan_pl_is_demo( $p->ID ) ) {
				$sep = true;
				echo '<p class="nlpl-sep"><b>מודעות לדוגמה.</b> כך נראית מודעה באתר. הן לא נספרות במספר המודעות ולא מופיעות במפה.</p>';
			}
			echo nadlan_pl_card( $p->ID ); // phpcs:ignore
		}
		echo '</div>';
		if ( $pages > 1 ) {
			echo '<nav class="nlpl-pager" aria-label="עמודים">' . paginate_links( array( 'total' => $pages, 'current' => $paged, 'prev_text' => '→ הקודם', 'next_text' => 'הבא ←', 'mid_size' => 2 ) ) . '</nav>'; // phpcs:ignore
		}
	} else {
		echo '<p class="nlpl-empty">אין מודעות שמתאימות לחיפוש. <a href="' . esc_url( $arch ) . '">לכל המודעות</a></p>';
	}
	?>
	<p class="nlpl-postline">יש לכם דירה למכירה או להשכרה? <a href="<?php echo esc_url( home_url( '/post-listing/' ) ); ?>">פרסמו מודעה בחינם</a></p>
<script>
(function(){
	var cards=[].slice.call(document.querySelectorAll(".nlpl-card[data-lat]"));
	if(!cards.length)return;
	function show(lat,lng,approx){
		cards.forEach(function(c){
			var la=parseFloat(c.dataset.lat),ln=parseFloat(c.dataset.lng);
			if(!la||!ln)return;
			var R=6371,dLa=(la-lat)*Math.PI/180,dLn=(ln-lng)*Math.PI/180;
			var a=Math.sin(dLa/2)*Math.sin(dLa/2)+Math.cos(lat*Math.PI/180)*Math.cos(la*Math.PI/180)*Math.sin(dLn/2)*Math.sin(dLn/2);
			var km=R*2*Math.atan2(Math.sqrt(a),Math.sqrt(1-a));
			if(km>120)return;
			var el=c.querySelector(".nlag-km");
			if(el){el.hidden=false;el.textContent=(km<1?"פחות מק״מ":"כ-"+(km<10?km.toFixed(1):Math.round(km))+" ק״מ")+" ממך"+(approx?" · משוער":"");}
		});
	}
	try{fetch("https://ipwho.is/").then(function(r){return r.json()}).then(function(g){
		if(g&&g.success&&g.country_code==="IL"&&g.latitude){show(g.latitude,g.longitude,true)}
	}).catch(function(){})}catch(e){}
})();
</script>
</div>
		<?php
		if ( function_exists( 'block_template_part' ) ) { block_template_part( 'footer' ); }
		get_footer();
	}
}

if ( ! function_exists( 'nadlan_pl_css' ) ) {
	function nadlan_pl_css() {
		return <<<'CSS'
.nlpl{max-width:1240px;margin:0 auto;padding:26px 24px 56px;color:#14212B;font-family:Assistant,Heebo,Arial,sans-serif}
.nlpl-crumbs{display:flex;gap:6px;align-items:center;font-size:13px;color:#57534B;margin:0 0 14px}
.nlpl-crumbs a{color:#2F6F86!important;text-decoration:none!important;font-weight:600}
.nlpl-head{display:flex;align-items:flex-end;justify-content:space-between;gap:18px 28px;flex-wrap:wrap;margin:0 0 18px}
.nlpl-head h1{font:600 clamp(28px,3vw,40px)/1.12 "Noto Serif Hebrew",Georgia,serif!important;margin:0 0 10px!important;color:#14212B!important;letter-spacing:0!important;text-wrap:balance}
.nlpl-lead{font-size:16px!important;line-height:1.55!important;color:#57534B!important;margin:0!important;max-width:62ch}
.nlpl-post{flex:none;display:inline-flex;align-items:center;gap:8px;height:44px;padding:0 18px;border-radius:999px;background:#14212B;color:#fff!important;font-weight:700;font-size:14.5px;text-decoration:none!important;white-space:nowrap}
.nlpl-post:hover{background:#2F6F86}
.nlpl-tabs{display:inline-flex;gap:4px;padding:4px;border-radius:999px;background:#EFEAE0;margin:0 0 14px}
.nlpl-tabs a{display:inline-flex;align-items:center;gap:6px;height:36px;padding:0 16px;border-radius:999px;color:#14212B!important;text-decoration:none!important;font-weight:600;font-size:14.5px}
.nlpl-tabs a i{font-style:normal;font-size:12.5px;color:#8a857b;font-variant-numeric:tabular-nums}
.nlpl-tabs a[aria-current="page"]{background:#fff;box-shadow:0 1px 3px rgba(20,33,43,.12)}
.nlpl-tabs a[aria-current="page"] i{color:#2F6F86}
.nlpl-bar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:18px 0 14px;font-size:14.5px;color:#57534B}
.nlpl-bar b{color:#14212B;font-variant-numeric:tabular-nums}
.nlpl-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.nlpl-card{position:relative;display:flex;flex-direction:column;background:#fff;border:1px solid #E3E1DA;border-radius:16px;overflow:hidden;color:#14212B!important;text-decoration:none!important;transition:border-color .15s,box-shadow .15s,transform .15s}
.nlpl-card:hover{border-color:#2F6F86;box-shadow:0 12px 28px rgba(20,33,43,.10);transform:translateY(-2px)}
.nlpl-card:focus-visible{outline:2px solid #2F6F86;outline-offset:2px}
.nlpl-media{position:relative;display:block;aspect-ratio:4/3;background:#EFEAE0 center/cover no-repeat;overflow:hidden}
.nlpl-media img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.nlpl-deal{position:absolute;top:12px;inset-inline-start:12px;height:26px;display:inline-flex;align-items:center;padding:0 10px;border-radius:999px;font-size:12.5px;font-weight:700;background:#14212B;color:#fff}
.nlpl-deal--rent{background:#fff;color:#14212B}
.nlpl-deal--demo{background:#EFE9DC;color:#57534B;border:1px dashed #8a857b}
.nlpl-body{display:flex;flex-direction:column;gap:6px;padding:14px 16px 12px;flex:1}
.nlpl-kicker{font-size:12.5px;font-weight:700;color:#2F6F86;letter-spacing:.01em}
.nlpl-title{font:500 17px/1.35 "Noto Serif Hebrew",Georgia,serif;margin:0;color:#14212B;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.nlpl-price{display:flex;align-items:baseline;flex-wrap:wrap;gap:4px 10px;margin-top:2px}
.nlpl-price strong{font-size:21px;font-weight:800;line-height:1.2;font-variant-numeric:tabular-nums}
.nlpl-price small{font-size:13px;color:#57534B;font-weight:600}
.nlpl-specs{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:13.5px;color:#14212B;font-weight:600;font-variant-numeric:tabular-nums}
.nlpl-specs span+span::before{content:"·";color:#B7B0A2;margin-inline-end:12px}
.nlpl-amen{display:flex;flex-wrap:wrap;gap:6px;margin-top:2px}
.nlpl-amen em{font-style:normal;height:24px;display:inline-flex;align-items:center;padding:0 9px;border-radius:999px;background:#EEF4F6;color:#1F4B5C;font-size:12px;font-weight:600}
.nlpl-foot{margin-top:auto;display:flex;align-items:center;justify-content:space-between;gap:10px;padding-top:10px;border-top:1px solid #EFEAE0;font-size:12.5px;color:#57534B}
.nlpl-by{display:flex;align-items:center;gap:8px;min-width:0}
.nlpl-by b{flex:none;display:grid;place-items:center;width:26px;height:26px;border-radius:50%;background:#FBF6EE;color:#9C7A3C;font:700 11px/1 "Noto Serif Hebrew",Georgia,serif;overflow:hidden}
.nlpl-by b img{width:26px;height:26px;object-fit:cover}
.nlpl-by span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nlpl-go{flex:none;color:#2F6F86;font-weight:700;font-size:16px}
.nlpl-card--demo{border-style:dashed;border-color:#B7B0A2}
.nlpl-sep{grid-column:1/-1;margin:14px 0 0;padding-top:14px;border-top:1px solid #E3E1DA;font-size:14px;color:#57534B}
.nlpl-sep b{color:#14212B}
.nlpl-pager{display:flex;justify-content:center;gap:6px;flex-wrap:wrap;margin-top:28px}
.nlpl-pager .page-numbers{display:inline-grid;place-items:center;min-width:44px;height:44px;padding:0 14px;border:1px solid #E3E1DA;border-radius:999px;text-decoration:none!important;color:#14212B!important;font-weight:600;background:#fff}
.nlpl-pager .page-numbers.current{background:#14212B;color:#fff!important;border-color:#14212B}
.nlpl-pager a.page-numbers:hover{border-color:#2F6F86;color:#2F6F86!important}
.nlpl-postline{margin:26px 0 0;font-size:15px;color:#57534B}
.nlpl-postline a{color:#2F6F86!important;font-weight:700;text-decoration:underline;text-underline-offset:3px}
.nlpl-empty{padding:40px 0;text-align:center;color:#57534B}
.nlpl-map{margin:0 0 18px;border-radius:16px;overflow:hidden;border:1px solid #E3E1DA}
.nlpl-media .nlag-km{position:absolute;bottom:10px;inset-inline-start:10px;font-style:normal;font:600 11.5px/1 Assistant,Heebo,Arial,sans-serif;color:#14212B;background:rgba(247,246,242,.95);border-radius:999px;padding:6px 10px}
@media (max-width:1060px){.nlpl-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:600px){.nlpl{padding:18px 16px 40px}.nlpl-head{display:block}.nlpl-post{margin-top:14px;width:100%;justify-content:center}.nlpl-tabs{display:flex}.nlpl-tabs a{flex:1;justify-content:center;padding:0 8px}.nlpl-grid{grid-template-columns:minmax(0,1fr);gap:12px}.nlpl-media{aspect-ratio:16/10}.nlpl-title{font-size:16.5px}.nlpl-price strong{font-size:20px}}
@media (prefers-reduced-motion:reduce){.nlpl-card{transition:none}.nlpl-card:hover{transform:none}}
.nlpl-filters{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr) minmax(0,1fr) auto auto;gap:10px;align-items:center;margin:0!important;padding:12px!important;background:#fff!important;border:1px solid #E3E1DA;border-radius:16px}
.nlpl-filters input,.nlpl-filters select{height:46px!important;border:1px solid #E3E1DA!important;border-radius:10px!important;background:#F7F6F2!important;padding:0 14px!important;font:500 15px/1 Assistant,Heebo,Arial,sans-serif!important;color:#14212B!important;min-width:0;width:100%;margin:0!important;box-shadow:none!important}
.nlpl-filters input:focus,.nlpl-filters select:focus{outline:2px solid #2F6F86;outline-offset:1px;background:#fff!important}
.nlpl-filters button{height:46px;padding:0 26px;border:0;border-radius:10px;background:#14212B;color:#fff;font:700 15px/1 Assistant,Heebo,Arial,sans-serif;cursor:pointer}
.nlpl-filters button:hover{background:#2F6F86}
.nlpl-clear{font-size:14px;color:#57534B!important;text-decoration:underline;text-underline-offset:3px;white-space:nowrap;padding:0 6px}
@media (max-width:600px){.nlpl-filters{grid-template-columns:repeat(2,minmax(0,1fr));padding:10px!important;gap:8px}.nlpl-filters .nlpl-f-city{grid-column:1/-1}.nlpl-filters button{grid-column:1/-1;width:100%}.nlpl-clear{grid-column:1/-1;text-align:center}}
CSS;
	}
}

/* type-specific card meta line */
if ( ! function_exists( 'nadlan_meta_norm' ) ) {
	/* collapse the whitespace padding gov.il leaves in CKAN fields */
	function nadlan_meta_norm( $s ) { return trim( preg_replace( '/\s+/u', ' ', (string) $s ) ); }
}
if ( ! function_exists( 'nadlan_archive_card_meta' ) ) {
	function nadlan_archive_card_meta( $id, $pt ) {
		if ( $pt === 'nadlan_professional' ) {
			$cls = nadlan_meta_norm( get_post_meta( $id, 'classification', true ) );
			$reg = nadlan_meta_norm( get_post_meta( $id, 'registry_number', true ) );
			$cls = mb_strlen( $cls ) > 46 ? mb_substr( $cls, 0, 46 ) . '…' : $cls;
			$out = $cls ? '<span class="nlag-spec">' . esc_html( $cls ) . '</span>' : '';
			$out .= $reg ? '<span class="nlag-reg">רשם הקבלנים #' . esc_html( $reg ) . '</span>' : '';
			return $out;
		}
		if ( $pt === 'nadlan_project' ) {
			$u  = (int) get_post_meta( $id, 'num_units', true );
			$st = nadlan_meta_norm( get_post_meta( $id, 'project_status', true ) );
			$bits = array_filter( array( $u ? $u . ' יח״ד' : '', $st ) );
			return $bits ? '<span class="nlag-spec">' . esc_html( implode( ' · ', $bits ) ) . '</span>' : '';
		}
		// property
		$pr = (float) get_post_meta( $id, 'price', true );
		$rm = get_post_meta( $id, 'rooms', true );
		$sq = get_post_meta( $id, 'size_sqm', true );
		$bits = array_filter( array( $rm ? $rm . " חד'" : '', $sq ? $sq . ' מ״ר' : '' ) );
		$out  = $pr ? '<span class="nlag-price">₪' . number_format( $pr ) . '</span>' : '';
		$out .= $bits ? '<span class="nlag-spec">' . esc_html( implode( ' · ', $bits ) ) . '</span>' : '';
		return $out;
	}
}

if ( ! function_exists( 'nadlan_archive_grid_css' ) ) {
	function nadlan_archive_grid_css() {
		return '<style>
.nlag{font-family:var(--font-sans,Heebo,sans-serif);max-width:1240px;margin:0 auto;padding:28px 24px 48px;direction:rtl;color:#1B1A17}
.nlag-crumbs{font-size:13px;color:#9a9a9a;margin-bottom:14px}
.nlag-crumbs a{color:#9C7A3C;text-decoration:none}.nlag-crumbs span{margin:0 6px}
.nlag-head{margin-bottom:22px}
.nlag-head h1{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-weight:500;font-size:34px;margin:0 0 8px;letter-spacing:-.015em}
.nlag-sub{font-size:15px;color:#6b6b6b;margin:0 0 8px;max-width:720px;line-height:1.6}
.nlag-count{font-size:14px;color:#5a5a5a;margin:0}.nlag-count strong{color:#9C7A3C;font-size:16px}
.nlag-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px;margin:22px 0}
.nlag-card{position:relative;display:flex;flex-direction:column;gap:6px;background:linear-gradient(135deg,#fff,#FBF9F5);border:1px solid rgba(27,26,23,.1);border-radius:14px;padding:20px;text-decoration:none;color:inherit;transition:transform .22s,box-shadow .22s,border-color .22s;min-height:170px}
.nlag-card:hover{transform:translateY(-5px);box-shadow:0 14px 32px rgba(27,26,23,.12);border-color:rgba(156,122,60,.45)}
.nlag-badge{align-self:flex-start;background:linear-gradient(135deg,#9C7A3C,#B89254);color:#fff;font-size:10px;letter-spacing:.1em;font-weight:600;padding:4px 10px;border-radius:20px}
.nlag-card h3{font-family:var(--font-serif,serif);font-weight:500;font-size:18px;margin:6px 0 2px;line-height:1.35}
.nlag-city{font-size:12px;letter-spacing:.08em;color:#9C7A3C;font-weight:600}
.nlag-spec{font-size:12.5px;color:#5a5a5a;line-height:1.5}
.nlag-reg{font-size:11px;color:#999}
.nlag-price{font-family:var(--font-serif,serif);font-size:18px;color:#1B1A17;font-weight:500}
.nlag-verified{font-size:11px;color:#2e7d32;font-weight:600}
.nlag-go{margin-top:auto;color:#9C7A3C;font-weight:600;font-size:13px;transition:transform .2s}
.nlag-card:hover .nlag-go{transform:translateX(-4px)}
.nlag-pager{display:flex;justify-content:center;gap:6px;flex-wrap:wrap;margin-top:30px}
.nlag-pager .page-numbers{display:inline-block;padding:9px 14px;border:1px solid rgba(27,26,23,.14);border-radius:8px;text-decoration:none;color:#1B1A17;font-size:14px}
.nlag-pager .page-numbers.current{background:#1B1A17;color:#FAF7F1;border-color:#1B1A17}
.nlag-pager a.page-numbers:hover{background:#9C7A3C;color:#fff;border-color:#9C7A3C}
.nlag-empty{text-align:center;padding:40px;color:#6b6b6b}
.nlag-empty a{color:#9C7A3C}
.nlag-media{display:block;aspect-ratio:4/3;margin:-20px -20px 10px;border-radius:14px 14px 0 0;background:#F3EEE3 center/cover no-repeat;position:relative}
.nlag-chips{display:flex;flex-wrap:wrap;gap:5px;margin:4px 0 2px}
.nlag-chips em{font-style:normal;font:600 11.5px/1 Heebo,sans-serif;color:#51483A;background:#F3EEE3;border:1px solid #E2DCD0;border-radius:7px;padding:5px 8px}
.nlag-km{position:absolute;bottom:10px;inset-inline-start:10px;font-style:normal;font:600 11.5px/1 Heebo,sans-serif;color:#1B1A17;background:rgba(250,247,241,.95);border-radius:999px;padding:6px 10px}
.nlag-city .nlag-km{position:static;margin-inline-start:8px}
@media(max-width:600px){.nlag-head h1{font-size:27px}.nlag-grid{grid-template-columns:repeat(2,1fr);gap:12px}.nlag-card{padding:16px;min-height:150px}}
</style>';
	}
}
