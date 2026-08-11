<?php
/**
 * nadlan-config - City hub DATA blocks (v2, 1.72.188)
 *
 * HISTORY / OWNER LAW (2026-08-11): v1 of this module drew "ghost pages" at
 * /city/<city>/<kind>/ from a rewrite rule - no post behind them, and its
 * <title>/<meta robots> were printed INSIDE THE BODY, which search engines
 * ignore. 168 anonymous pages (title "נדלן") were fed to Google via a private
 * sitemap and cannibalized the head keyword. The owner's standing law: no
 * ghost pages, no invisible index flags, no redirect farms. City hubs are now
 * REAL WordPress pages (hierarchy: city / <עיר> / projects) created explicitly
 * by a seeder with owner approval; this file only provides:
 *   - nadlan_hub_query():       count + sample cards for (city, kind)
 *   - [nadlan_city_hub] :       the live data blocks rendered inside the page
 *   - a one-time rewrite flush that removes the old ghost rules
 * The ghost dispatcher, its body-printed head tags and the private sitemap
 * are DELETED, not disabled. Do not resurrect them.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

const NADLAN_HUB_CARD_FLOOR = 5;

/* ---- query helper: count + sample cards for a (city, kind) ---- */
if ( ! function_exists( 'nadlan_hub_query' ) ) {
	function nadlan_hub_query( $city, $kind, $limit = 24 ) {
		$pt = array( 'contractors' => 'nadlan_professional', 'projects' => 'nadlan_project', 'properties' => 'nadlan_property' )[ $kind ] ?? null;
		if ( ! $pt ) { return null; }
		$mq = array( array( 'key' => 'city', 'value' => $city ) );
		if ( $kind === 'contractors' ) { $mq[] = array( 'key' => 'profession', 'value' => 'kablan' ); }
		$count = (int) ( new WP_Query( array(
			'post_type' => $pt, 'posts_per_page' => 1, 'fields' => 'ids',
			'meta_query' => $mq, 'no_found_rows' => false,
		) ) )->found_posts;
		$items = get_posts( array(
			'post_type' => $pt, 'posts_per_page' => $limit, 'meta_query' => $mq,
			'orderby' => 'modified', 'order' => 'DESC',
		) );
		return array( 'pt' => $pt, 'count' => $count, 'items' => $items );
	}
}

/* ---- the live data blocks: stats + card grid + one contextual uplink ---- */
if ( ! function_exists( 'nadlan_hub_blocks_html' ) ) {
	function nadlan_hub_blocks_html( $city, $kind, $data ) {
		static $css_done = false;
		$stats = function_exists( 'nadlan_neighborhood_stats' )
			? nadlan_neighborhood_stats( $city )
			: array( 'deals_12m' => 0, 'avg_ppsqm' => 0 );
		ob_start();
		if ( ! $css_done ) { $css_done = true; ?>
<style>
.nlhub-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin:16px 0}
.nlhub-stat{background:#FAF7F1;padding:14px;border-radius:6px;text-align:center}
.nlhub-stat .v{font-size:22px;font-weight:700;color:#1B1A17}
.nlhub-stat .l{font-size:12px;color:#777;margin-top:4px}
.nlhub-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px;margin:18px 0}
.nlhub-card{border:1px solid rgba(27,26,23,.1);border-radius:6px;padding:14px;text-decoration:none;color:inherit;background:#fff;display:block}
.nlhub-card:hover{box-shadow:0 4px 14px rgba(27,26,23,.08)}
.nlhub-card h3{margin:0 0 6px;font-size:16px}
.nlhub-card .m{font-size:13px;color:#777}
.nlhub-uplink{margin-top:24px;padding-top:16px;border-top:1px solid rgba(27,26,23,.08);font-size:14px}
</style>
		<?php } ?>
<div class="nlhub-stats" dir="rtl">
	<div class="nlhub-stat"><div class="v"><?php echo (int) $data['count']; ?></div><div class="l">רשומות פעילות</div></div>
	<?php if ( ! empty( $stats['deals_12m'] ) ) : ?>
	<div class="nlhub-stat"><div class="v"><?php echo (int) $stats['deals_12m']; ?></div><div class="l">עסקאות (12 ח׳)</div></div>
	<div class="nlhub-stat"><div class="v">₪<?php echo number_format( (float) $stats['avg_ppsqm'] ); ?></div><div class="l">ממוצע למ״ר</div></div>
	<?php endif; ?>
</div>
<div class="nlhub-grid" dir="rtl">
	<?php foreach ( $data['items'] as $p ) :
		$meta = '';
		if ( $kind === 'contractors' ) {
			$cls  = get_post_meta( $p->ID, 'classification', true );
			$meta = $cls ? mb_substr( $cls, 0, 80 ) : '';
		} elseif ( $kind === 'projects' ) {
			$u    = (int) get_post_meta( $p->ID, 'num_units', true );
			$st   = (string) get_post_meta( $p->ID, 'project_status', true );
			$map  = array( 'planning' => 'בתכנון', 'permits' => 'בהיתרים', 'pre_sale' => 'טרום מכירה',
				'marketing' => 'בשיווק', 'construction' => 'בבנייה', 'completed' => 'הושלם', 'occupancy' => 'באכלוס' );
			$stv  = $map[ $st ] ?? '';
			$meta = trim( ( $u ? $u . ' יח״ד' : '' ) . ( $stv ? ' · ' . $stv : '' ), ' ·' );
		} else {
			$pr = (float) get_post_meta( $p->ID, 'price', true );
			$rm = get_post_meta( $p->ID, 'rooms', true );
			$sq = get_post_meta( $p->ID, 'size_sqm', true );
			$meta = trim( ( $pr ? '₪' . number_format( $pr ) : '' ) . ( $rm ? ' · ' . $rm . ' חד׳' : '' ) . ( $sq ? ' · ' . $sq . ' מ״ר' : '' ), ' ·' );
		}
		?>
	<a class="nlhub-card" href="<?php echo esc_url( get_permalink( $p ) ); ?>">
		<h3><?php echo esc_html( get_the_title( $p ) ); ?></h3>
		<div class="m"><?php echo esc_html( $meta ); ?></div>
	</a>
	<?php endforeach; ?>
</div>
<div class="nlhub-uplink" dir="rtl">
	<?php if ( $kind === 'projects' ) : ?>
		מחפשים את התמונה הארצית? <a href="/projects/">כל הפרויקטים בישראל</a> · <a href="/new-projects/">המדריך המלא לקנייה מקבלן</a>
	<?php elseif ( $kind === 'contractors' ) : ?>
		רוצים להבין מה אומרים הסיווגים? <a href="/real-estate-lawyer/">המדריך לעורך דין מקרקעין</a>
	<?php else : ?>
		<?php echo do_shortcode( '[nadlan_save_search]' ); ?>
	<?php endif; ?>
</div>
		<?php
		return ob_get_clean();
	}
}

/* ---- the shortcode real pages embed ---- */
add_shortcode( 'nadlan_city_hub', function ( $atts ) {
	$a    = shortcode_atts( array( 'city' => '', 'kind' => 'projects' ), $atts );
	$city = sanitize_text_field( $a['city'] );
	$kind = sanitize_key( $a['kind'] );
	if ( '' === $city || ! in_array( $kind, array( 'contractors', 'projects', 'properties' ), true ) ) { return ''; }
	$data = nadlan_hub_query( $city, $kind );
	if ( ! $data || $data['count'] < 1 ) {
		return '<p dir="rtl">אין כרגע רשומות פעילות בעיר זו. הקטלוג מתעדכן שוטף.</p>';
	}
	return nadlan_hub_blocks_html( $city, $kind, $data );
} );

/* ---- one-time cleanup: flush the old ghost rewrite rules OUT ---- */
add_action( 'init', function () {
	if ( (string) get_option( 'nadlan_hub_rules_v', '' ) !== '3' ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_hub_rules_v', '3' );
	}
}, 99 );
