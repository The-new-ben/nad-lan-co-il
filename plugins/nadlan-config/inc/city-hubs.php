<?php
/**
 * nadlan-config — Programmatic SEO city hubs (v1.10.0)
 *
 * Auto-generates city/neighborhood hub pages that target GENERIC keyword intent
 * ("קבלנים רשומים ב<עיר>", "פרויקטים ב<עיר>", "דירות למכירה ב<עיר>") and link DOWN
 * to the branded cards. Cannibalization-safe: hub keyword ≠ branded card keyword.
 *
 * 2026 best practice (research): ≥25-30% UNIQUE data per hub, quality > volume.
 * 10 strong city hubs beat 100 thin ones. Doorway/scaled-content abuse is a real
 * Google penalty now. Therefore:
 *   - Floor: each hub must have ≥ NADLAN_HUB_CARD_FLOOR cards (default 5) of the
 *     relevant type, else 404 (no thin pages enter the index).
 *   - Per-hub unique data = card count + neighborhood AVG ₪/sqm (from wp_nadlan_deals)
 *     + deal volume + top 8 cards rendered inline. Not "nice place to live".
 *   - JSON-LD CollectionPage + ItemList for rich results.
 *
 * Three rewrite endpoints (front-end only, no DB pages — clean and cache-friendly):
 *   /city/<city>/contractors/   → contractors hub
 *   /city/<city>/projects/      → projects hub
 *   /city/<city>/properties/    → properties hub (listings)
 *
 * Cross-link: each hub links UP to the relevant pillar (e.g. /real-estate-lawyer/
 * for property hubs; the encyclopedia/glossary hubs once those exist).
 *
 * BLANK (owner): the "top N priority cities" allow-list lives in an option so we
 * can publish the high-quality 10-20 first per the research recommendation; until
 * set, the floor + noindex guard prevents any thin page from ranking.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

const NADLAN_HUB_CARD_FLOOR = 5;

if ( ! function_exists( 'nadlan_hub_rewrites' ) ) {
	function nadlan_hub_rewrites() {
		add_rewrite_rule( '^city/([^/]+)/(contractors|projects|properties)/?$',
			'index.php?nadlan_hub_city=$matches[1]&nadlan_hub_kind=$matches[2]', 'top' );
		add_rewrite_tag( '%nadlan_hub_city%', '([^&]+)' );
		add_rewrite_tag( '%nadlan_hub_kind%', '(contractors|projects|properties)' );
	}
}
add_action( 'init', 'nadlan_hub_rewrites' );

/* Flush once when the rules change */
register_activation_hook( dirname( __DIR__ ) . '/nadlan-config.php', function () {
	nadlan_hub_rewrites();
	flush_rewrite_rules();
} );
add_action( 'init', function () {
	if ( (string) get_option( 'nadlan_hub_rules_v', '' ) !== '1' ) {
		nadlan_hub_rewrites();
		flush_rewrite_rules( false );
		update_option( 'nadlan_hub_rules_v', '1' );
	}
}, 99 );

/* ---- query helper: count + sample cards for a (city, kind) ---- */
if ( ! function_exists( 'nadlan_hub_query' ) ) {
	function nadlan_hub_query( $city, $kind, $limit = 24 ) {
		$pt = array( 'contractors' => 'nadlan_professional', 'projects' => 'nadlan_project', 'properties' => 'nadlan_property' )[ $kind ] ?? null;
		if ( ! $pt ) { return null; }
		$mq = array( array( 'key' => 'city', 'value' => $city ) );
		if ( $kind === 'contractors' ) { $mq[] = array( 'key' => 'profession', 'value' => 'kablan' ); }
		// Count
		$count = (int) ( new WP_Query( array(
			'post_type' => $pt, 'posts_per_page' => 1, 'fields' => 'ids',
			'meta_query' => $mq, 'no_found_rows' => false,
		) ) )->found_posts;
		// Sample
		$items = get_posts( array(
			'post_type' => $pt, 'posts_per_page' => $limit, 'meta_query' => $mq,
			'orderby' => 'modified', 'order' => 'DESC',
		) );
		return array( 'pt' => $pt, 'count' => $count, 'items' => $items );
	}
}

/* ---- render: intercept template_redirect ---- */
if ( ! function_exists( 'nadlan_hub_dispatch' ) ) {
	function nadlan_hub_dispatch() {
		$city = get_query_var( 'nadlan_hub_city' );
		$kind = get_query_var( 'nadlan_hub_kind' );
		if ( ! $city || ! $kind ) { return; }
		$city = sanitize_text_field( urldecode( $city ) );
		$data = nadlan_hub_query( $city, $kind );
		if ( ! $data || $data['count'] < NADLAN_HUB_CARD_FLOOR ) {
			status_header( 404 ); nocache_headers();
			include get_query_template( '404' ); exit;
		}
		nadlan_hub_render( $city, $kind, $data );
		exit;
	}
}
add_action( 'template_redirect', 'nadlan_hub_dispatch', 5 );

if ( ! function_exists( 'nadlan_hub_render' ) ) {
	function nadlan_hub_render( $city, $kind, $data ) {
		$labels = array(
			'contractors' => array( 'h1' => "קבלנים רשומים ב$city", 'desc' => "אינדקס קבלנים רשומים בעיר  מתוך פנקס הקבלנים: סינון לפי סיווג, ענפי בנייה ופרטי קשר.", 'kw' => "קבלנים $city" ),
			'projects'    => array( 'h1' => "פרויקטים חדשים והתחדשות עירונית ב$city", 'desc' => "פרויקטי מגורים בעיר $city: תמ\"א 38, פינוי-בינוי, בנייה חדשה, עם מספר יחידות, סטטוס ופרטי תוכנית.", 'kw' => "פרויקטים $city" ),
			'properties'  => array( 'h1' => "דירות ב$city", 'desc' => "לוח דירות בעיר $city: מחיר, חדרים, מ\"ר ושכונה.", 'kw' => "דירות $city" ),
		);
		$L = $labels[ $kind ];
		$stats = nadlan_neighborhood_stats( $city );
		$title = $L['h1'] . " | נדל\"ן חכם";

		get_header();
		if ( function_exists( 'block_template_part' ) ) { block_template_part( 'header' ); }
		?>
<style>
.nlhub{max-width:1100px;margin:0 auto;padding:24px;font-family:var(--font-sans,Heebo,sans-serif);direction:rtl}
.nlhub h1{font-size:30px;margin:0 0 8px}
.nlhub .lede{color:#555;margin:0 0 18px}
.nlhub-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin:16px 0}
.nlhub-stat{background:#FAF7F1;padding:14px;border-radius:6px;text-align:center}
.nlhub-stat .v{font-size:22px;font-weight:700;color:#1B1A17}
.nlhub-stat .l{font-size:12px;color:#777;margin-top:4px}
.nlhub-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px;margin:18px 0}
.nlhub-card{border:1px solid rgba(27,26,23,.1);border-radius:6px;padding:14px;text-decoration:none;color:inherit;background:#fff}
.nlhub-card:hover{box-shadow:0 4px 14px rgba(27,26,23,.08)}
.nlhub-card h3{margin:0 0 6px;font-size:16px}
.nlhub-card .m{font-size:13px;color:#777}
.nlhub-uplink{margin-top:24px;padding-top:16px;border-top:1px solid rgba(27,26,23,.08);font-size:14px}
</style>
<title><?php echo esc_html( $title ); ?></title>
<meta name="description" content="<?php echo esc_attr( $L['desc'] . ' ' . (int) $data['count'] . ' רשומות.' ); ?>">
<meta name="robots" content="<?php echo ( $data['count'] >= NADLAN_HUB_CARD_FLOOR * 2 ) ? 'index,follow' : 'noindex,follow'; ?>">
<script type="application/ld+json"><?php echo wp_json_encode( array(
	'@context' => 'https://schema.org', '@type' => 'CollectionPage',
	'name' => $L['h1'], 'description' => $L['desc'],
	'mainEntity' => array( '@type' => 'ItemList', 'numberOfItems' => (int) $data['count'],
		'itemListElement' => array_map( function ( $p, $i ) {
			return array( '@type' => 'ListItem', 'position' => $i + 1, 'url' => get_permalink( $p ), 'name' => get_the_title( $p ) );
		}, array_values( $data['items'] ), array_keys( $data['items'] ) ) ),
), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ); ?></script>

<div class="nlhub">
	<h1><?php echo esc_html( $L['h1'] ); ?></h1>
	<p class="lede"><?php echo esc_html( $L['desc'] ); ?> סה"כ <strong><?php echo (int) $data['count']; ?></strong> רשומות, מעודכן.</p>

	<div class="nlhub-stats">
		<div class="nlhub-stat"><div class="v"><?php echo (int) $data['count']; ?></div><div class="l">רשומות</div></div>
		<?php if ( $stats['deals_12m'] > 0 ) : ?>
		<div class="nlhub-stat"><div class="v"><?php echo (int) $stats['deals_12m']; ?></div><div class="l">עסקאות (12 ח')</div></div>
		<div class="nlhub-stat"><div class="v">₪<?php echo number_format( $stats['avg_ppsqm'] ); ?></div><div class="l">ממוצע למ"ר</div></div>
		<?php endif; ?>
	</div>

	<div class="nlhub-grid">
		<?php foreach ( $data['items'] as $p ) :
			$meta = '';
			if ( $kind === 'contractors' ) {
				$cls  = get_post_meta( $p->ID, 'classification', true );
				$meta = $cls ? mb_substr( $cls, 0, 80 ) : '';
			} elseif ( $kind === 'projects' ) {
				$u    = (int) get_post_meta( $p->ID, 'num_units', true );
				$st   = (string) get_post_meta( $p->ID, 'project_status', true );
				$meta = trim( ( $u ? "$u יח\"ד" : '' ) . ( $st ? " · $st" : '' ), ' ·' );
			} else {
				$pr = (float) get_post_meta( $p->ID, 'price', true );
				$rm = get_post_meta( $p->ID, 'rooms', true );
				$sq = get_post_meta( $p->ID, 'size_sqm', true );
				$meta = trim( ( $pr ? '₪' . number_format( $pr ) : '' ) . ( $rm ? " · $rm חד'" : '' ) . ( $sq ? " · $sq מ\"ר" : '' ), ' ·' );
			}
			?>
		<a class="nlhub-card" href="<?php echo esc_url( get_permalink( $p ) ); ?>">
			<h3><?php echo esc_html( get_the_title( $p ) ); ?></h3>
			<div class="m"><?php echo esc_html( $meta ); ?></div>
		</a>
		<?php endforeach; ?>
	</div>

	<div class="nlhub-uplink">
		<?php if ( $kind === 'contractors' ) : ?>
			רוצים להבין מה אומרים הסיווגים? קראו את <a href="/real-estate-lawyer/">המדריך לעורך דין מקרקעין</a>.
		<?php elseif ( $kind === 'projects' ) : ?>
			שוקלים רכישה? <a href="/contract-audit/">בדיקת חוזה דירה</a> תוך 48 שעות.
		<?php else : ?>
			לקבלת התראות על דירות חדשות ב<?php echo esc_html( $city ); ?>: <?php echo do_shortcode( '[nadlan_save_search]' ); ?>
		<?php endif; ?>
	</div>
</div>
		<?php
		if ( function_exists( 'block_template_part' ) ) { block_template_part( 'footer' ); }
		get_footer();
	}
}

/* ---- sitemap entries via Yoast filter ---- */
add_filter( 'wpseo_sitemap_index', function ( $smap ) {
	// We add one extra sitemap entry; the actual URLs come from the dynamic generator below.
	$url = home_url( '/sitemap-nadlan-hubs.xml' );
	$smap .= "<sitemap><loc>$url</loc><lastmod>" . gmdate( 'c' ) . "</lastmod></sitemap>";
	return $smap;
} );
add_action( 'init', function () {
	add_rewrite_rule( '^sitemap-nadlan-hubs\.xml$', 'index.php?nadlan_hubs_sitemap=1', 'top' );
	add_rewrite_tag( '%nadlan_hubs_sitemap%', '1' );
} );
add_action( 'template_redirect', function () {
	if ( ! get_query_var( 'nadlan_hubs_sitemap' ) ) { return; }
	global $wpdb;
	$cities = $wpdb->get_col( "SELECT DISTINCT meta_value FROM {$wpdb->postmeta} WHERE meta_key='city' AND meta_value<>'' LIMIT 5000" );
	header( 'Content-Type: application/xml; charset=UTF-8' );
	echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
	echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
	foreach ( (array) $cities as $c ) {
		foreach ( array( 'contractors', 'projects', 'properties' ) as $k ) {
			$data = nadlan_hub_query( $c, $k );
			if ( $data && $data['count'] >= NADLAN_HUB_CARD_FLOOR ) {
				$url = home_url( '/city/' . rawurlencode( $c ) . '/' . $k . '/' );
				echo '<url><loc>' . esc_url( $url ) . '</loc><changefreq>weekly</changefreq></url>';
			}
		}
	}
	echo '</urlset>'; exit;
}, 0 );
