<?php
/**
 * nadlan-config — Featured upsell on claimed profiles (v1.40.0 / shark #8)
 *
 * When a contractor is logged in viewing their OWN claimed profile (or any
 * verified-claimed profile), show a "your card is in position #X — upgrade to
 * land in top-5 in your city" banner with one-click checkout. The position is
 * computed live from the same featured-sort the directory uses. Conversion
 * driver for the existing Pro/Premier products (476/477) — turns the abstract
 * "upgrade" into a concrete, ego-tickling pitch.
 *
 * Also appended to ALL claimed-but-free profiles (not just the owner's) as a
 * sponsored-pitch — the contractor sees it any time they visit their own page.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_fu_position' ) ) {
	function nadlan_fu_position( $id ) {
		$profession = (string) get_post_meta( $id, 'profession', true );
		$city       = trim( (string) get_post_meta( $id, 'city', true ) );
		if ( ! $profession || ! $city ) { return 0; }
		global $wpdb;
		// Same ordering as directory: featured (menu_order ASC) then date DESC.
		// Rank within profession+city. Cheap query, indexed columns.
		$rows = $wpdb->get_col( $wpdb->prepare(
			"SELECT p.ID FROM {$wpdb->posts} p
			 INNER JOIN {$wpdb->postmeta} m1 ON m1.post_id=p.ID AND m1.meta_key='profession' AND m1.meta_value=%s
			 INNER JOIN {$wpdb->postmeta} m2 ON m2.post_id=p.ID AND m2.meta_key='city'       AND m2.meta_value=%s
			 WHERE p.post_type='nadlan_professional' AND p.post_status='publish'
			 ORDER BY p.menu_order ASC, p.post_date DESC LIMIT 1000",
			$profession, $city
		) );
		$pos = array_search( (int) $id, array_map( 'intval', (array) $rows ), true );
		return $pos === false ? 0 : ( $pos + 1 );
	}
}

if ( ! function_exists( 'nadlan_fu_render' ) ) {
	function nadlan_fu_render( $id ) {
		$claim = (string) get_post_meta( $id, 'claim_status', true );
		$tier  = (string) get_post_meta( $id, 'paid_tier', true ) ?: 'free';
		// only show for claimed-but-not-Pro/Premier — those are the upgrade targets
		if ( $claim !== 'verified' ) { return ''; }
		if ( in_array( $tier, array( 'pro', 'premier' ), true ) ) { return ''; }
		$pos = nadlan_fu_position( $id );
		$prof_label = '';
		if ( function_exists( 'nadlan_dir_prof_meta' ) ) {
			$pm = nadlan_dir_prof_meta( (string) get_post_meta( $id, 'profession', true ) );
			$prof_label = $pm['label'] ?? '';
		}
		$city = (string) get_post_meta( $id, 'city', true );
		$pro_url = home_url( '/?add-to-cart=476&ref=featured-upsell&card_id=' . (int) $id );
		$premier_url = home_url( '/?add-to-cart=477&ref=featured-upsell&card_id=' . (int) $id );
		ob_start(); ?>
<div class="nlfu" dir="rtl">
	<div class="nlfu-eyebrow">📈 שיווק מותאם לעסק שלכם</div>
	<?php if ( $pos > 0 ) : ?>
	<h3>הכרטיס שלכם במקום <span class="nlfu-pos">#<?php echo (int) $pos; ?></span> בקטגוריה <strong><?php echo esc_html( $prof_label ); ?> · <?php echo esc_html( $city ); ?></strong></h3>
	<p>שדרוג ל-Pro או Premier מוביל לחמשת המקומות הראשונים, כפתור התקשרות גלוי ותג מאומת. בדיוק במקום שלקוחות מסתכלים קודם.</p>
	<?php else : ?>
	<h3>קבלו חשיפה מירבית לעסק שלכם</h3>
	<p>שדרוג ל-Pro או Premier מקפיץ את הכרטיס למעלה ופותח את כפתורי יצירת קשר ללקוחות.</p>
	<?php endif; ?>
	<div class="nlfu-cta">
		<a class="nlfu-btn" href="<?php echo esc_url( $pro_url ); ?>">Pro · ₪349 / חודש →</a>
		<a class="nlfu-btn nlfu-premier" href="<?php echo esc_url( $premier_url ); ?>">Premier · ₪749 / חודש →</a>
		<small>חודש ראשון חינם עם הקופון <code>FIRSTMONTHFREE</code></small>
	</div>
</div>
<style>
.nlfu{font-family:var(--font-sans,Heebo,sans-serif);direction:rtl;background:linear-gradient(135deg,#FBF9F5,#F0E9DA);border:1px solid rgba(156,122,60,.3);border-radius:16px;padding:22px;margin:24px 0}
.nlfu-eyebrow{font-size:11px;letter-spacing:.16em;color:#9C7A3C;font-weight:700;text-transform:uppercase;margin-bottom:8px}
.nlfu h3{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:19px;font-weight:600;color:#1B1A17;margin:0 0 8px}
.nlfu-pos{font-family:var(--font-serif,serif);font-size:26px;color:#9C7A3C}
.nlfu p{font-size:14px;color:#5a5a5a;line-height:1.6;margin:0 0 14px}
.nlfu-cta{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.nlfu-btn{background:#9C7A3C;color:#fff;padding:11px 18px;border-radius:9px;text-decoration:none;font-weight:700;font-size:13.5px;transition:transform .15s,filter .2s}
.nlfu-btn:hover{transform:translateY(-2px);filter:brightness(1.08)}
.nlfu-premier{background:linear-gradient(135deg,#1B1A17,#3a3329)}
.nlfu small{font-size:11px;color:#7a7a7a;width:100%}
.nlfu small code{background:#1B1A17;color:#F3D9A6;padding:1px 8px;border-radius:4px}
</style>
<?php
		return ob_get_clean();
	}
}

add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'nadlan_professional' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
	return $content . nadlan_fu_render( get_the_ID() );
}, 26 );
