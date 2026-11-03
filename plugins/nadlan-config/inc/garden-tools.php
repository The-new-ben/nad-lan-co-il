<?php
/**
 * nadlan-config - THE TEL AVIV GARDEN-APARTMENTS TOOLS (HAD-669 R12d, 1.72.577; Claude Design v108.0 GardenHub). Ben, 3.11.2026:
 * "the best garden-apartment page in the world: it holds listings, covers every combination, with tools, prices and data". Four
 * instruments of one family in assets/instruments/tools/garden.js, on assets/instruments/data/garden.json
 * (tools/instruments/build_garden_data.py, Tax Authority deals of type 'דירת גן', which stop at 28.8.2024): gdnworth, gdnmap,
 * gdnstreet, gdnground. Plus [nadlan_garden_listings]: the REAL Tel Aviv garden listings (nadlan_property, property_type garden,
 * demos left out in the query, inc/archive-grid.php's own clause and card), or one honest line when there is none.
 * Loaded by inc/instruments.php (only if present, so a rollback that removes this file leaves the engine working).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_gdn_tool_ids' ) ) {

	function nadlan_gdn_tool_ids() { return array( 'gdnworth', 'gdnmap', 'gdnstreet', 'gdnground' ); }

	add_filter( 'nadlan_nli_tools', function ( $tools ) {
		$rel = array( '/tel-aviv-apartment-prices/' => 'מחירי דירות בתל אביב', '/tel-aviv-penthouse-prices/' => 'מחירי פנטהאוזים בתל אביב', '/property-value-estimator/' => 'מחשבון שווי דירה', '/purchase-tax-calculator/' => 'מחשבון מס רכישה' );
		$d = array( 'garden.json' );
		$tools['gdnworth'] = array( 'file' => 'garden', 'name' => 'מחשבון שווי דירת גן בתל אביב', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · דירת גן', 'data' => $d, 'related' => $rel,
			'desc' => 'הערכת שווי לדירת גן בתל אביב לפי עסקאות שנסגרו: השכונה, מספר החדרים והשטח הבנוי, מול המחיר החציוני למ״ר של דירות גן בשכונה (5 עסקאות ומעלה, 2015 עד 2024) או בכל העיר לפי חדרים (2020 עד 2024). רשות המסים, עד אוגוסט 2024.' );
		$tools['gdnmap'] = array( 'file' => 'garden', 'name' => 'מפת עסקאות דירות הגן בתל אביב', 'cat' => 'ReferenceApplication', 'kicker' => 'מפה · דירות גן', 'data' => $d, 'related' => $rel,
			'desc' => '227 עסקאות דירות גן שדווחו לרשות המסים בתל אביב-יפו, במיקום החלקה, בצבע לפי המחיר למ״ר, ולכל שכונה המחיר החציוני למ״ר או מספר העסקאות. עד אוגוסט 2024.' );
		$tools['gdnstreet'] = array( 'file' => 'garden', 'name' => 'עסקאות דירות גן לפי רחוב בתל אביב', 'cat' => 'ReferenceApplication', 'kicker' => 'איתור · רחוב', 'data' => $d, 'related' => $rel,
			'desc' => 'כל עסקת דירת גן שדווחה ברחוב בתל אביב-יפו: התאריך, הכתובת, החדרים, השטח הבנוי והמחיר. רשות המסים, עד אוגוסט 2024.' );
		$tools['gdnground'] = array( 'file' => 'garden', 'name' => 'קומת קרקע מול כל הבניין, לפי שכונה בתל אביב', 'cat' => 'ReferenceApplication', 'kicker' => 'השוואה · קומת קרקע', 'data' => $d, 'related' => $rel,
			'desc' => 'בכל שכונה בתל אביב-יפו: בכמה אחוזים דירה בקומת הקרקע נמכרה מעל או מתחת לשאר הבניין למ״ר, בשנים 2020 עד 2024, לפי עסקאות רשות המסים.' );
		return $tools;
	} );

	add_shortcode( 'nadlan_garden_listings', function () {
		$args = array( 'post_type' => 'nadlan_property', 'post_status' => 'publish', 'posts_per_page' => 12, 'no_found_rows' => true, 'fields' => 'ids',
			'meta_query' => array( 'relation' => 'AND', array( 'key' => 'property_type', 'value' => 'garden' ), array( 'key' => 'city', 'value' => 'תל אביב', 'compare' => 'LIKE' ) ) );
		if ( function_exists( 'nadlan_pl_nodemo' ) ) { $args['meta_query'][] = nadlan_pl_nodemo(); }
		$ids = get_posts( $args );
		if ( function_exists( 'nadlan_pl_is_demo' ) ) { $ids = array_values( array_filter( $ids, function ( $id ) { return ! nadlan_pl_is_demo( $id ); } ) ); }
		$h = '<section class="gdl" id="gdl" dir="rtl" aria-label="דירות גן בתל אביב שמוצעות באתר">';
		if ( ! $ids || ! function_exists( 'nadlan_plist_card' ) ) {
			return $h . '<p class="gdl-empty">כרגע אין באתר דירת גן בתל אביב שמוצעת למכירה או להשכרה. מוכרים או משכירים דירת גן? <a href="' . esc_url( home_url( '/post-listing/' ) ) . '">פרסמו אותה כאן</a>, עם גודל הגינה והאם היא רשומה בטאבו.</p></section>';
		}
		$h .= '<div class="nlpl-grid">';
		foreach ( $ids as $id ) { $h .= nadlan_plist_card( $id ); }
		return $h . '</div></section>';
	} );

	add_action( 'wp_head', function () {
		if ( ! function_exists( 'nadlan_nli_page_ids' ) || ! array_intersect( nadlan_nli_page_ids(), nadlan_gdn_tool_ids() ) ) { return; }
		echo '<style id="nadlan-gdn-css">'
			. 'html body .gdp-cta{display:flex;flex-wrap:wrap;gap:10px;margin:6px 0 20px}'
			. 'html body .gdp-cta a{display:inline-flex;align-items:center;min-height:44px;padding:10px 16px;border:1.5px solid #2f6b3f;border-radius:6px;color:#2f6b3f!important;text-decoration:none!important;font:700 15px/1.3 Assistant,"IBM Plex Sans Hebrew",system-ui,sans-serif;background:#fff}'
			. 'html body .gdp-cta a.is-main{background:#2f6b3f;color:#fff!important}'
			. '.gdp-strip{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border:1px solid #d6dcd6;border-radius:6px;overflow:hidden;margin:0 0 22px;background:#fff}'
			. '@media (min-width:860px){.gdp-strip{grid-template-columns:repeat(4,minmax(0,1fr))}}'
			. '.gdp-strip>div{padding:12px 14px;display:grid;gap:2px;border-inline-start:1px solid #d6dcd6;border-bottom:1px solid #d6dcd6;min-width:0}'
			. 'html body .gdp-strip strong{font:600 22px/1.1 "IBM Plex Mono",ui-monospace,monospace;color:#1f4a2b}'
			. 'html body .gdp-strip span{font:500 13px/1.35 Assistant,"IBM Plex Sans Hebrew",system-ui,sans-serif;color:#3b4753}'
			. '.gdm__map{position:relative;height:min(64vh,540px);min-height:340px;border:1px solid var(--nli-line);border-radius:var(--nli-r-m);overflow:hidden;margin:10px 0;background:#eef4ee}'
			. 'html body .nli .gdm__chips button[aria-pressed="true"]{background:#2f6b3f;border-color:#2f6b3f;color:#fff}'
			. 'html body .nli p.gds__h{font:500 15px/1.4 var(--nli-sans);color:var(--nli-ink2);margin:12px 0 6px}'
			. '.gds__out i{font-style:normal;font:600 11.5px/1 var(--nli-sans);color:#2f6b3f;border:1px solid #a9cdb0;border-radius:999px;padding:2px 6px}'
			. '.gdg__rows{display:grid;gap:6px;margin:6px 0 12px;position:relative}'
			. '.gdg__row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,2fr) 56px;gap:8px;align-items:center;font:400 13.5px/1.3 var(--nli-sans);color:var(--nli-ink2)}'
			. '.gdg__row i{display:block;height:10px;border-radius:1px;width:var(--w);min-width:2px}.gdg__row i.up{background:#2f6b3f}.gdg__row i.dn{background:#c7cfc8}'
			. '.gdg__row b{font:500 13.5px/1 var(--nli-mono);color:var(--nli-ink);text-align:end}'
			. '.gdl{margin:8px 0 24px}html body .gdl p.gdl-empty{border:1px dashed #a9cdb0;border-radius:8px;padding:14px 16px;font:500 15px/1.55 Assistant,"IBM Plex Sans Hebrew",system-ui,sans-serif;color:#3b4753;background:#fafcfa;margin:0}'
			. 'html body .gdl p.gdl-empty a{color:#2f6b3f!important;text-decoration:underline!important}'
			. '</style>';
		if ( function_exists( 'nadlan_pl_css' ) ) { echo '<style id="nadlan-gdl-cards">' . nadlan_pl_css() . '</style>'; } // phpcs:ignore -- the listing cards' own CSS, only on this page
	}, 31 );
}
